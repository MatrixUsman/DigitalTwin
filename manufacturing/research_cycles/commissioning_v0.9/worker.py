import argparse,sys,json,time,platform,subprocess,traceback
from pathlib import Path
from datetime import datetime,timezone
from common9 import HERE,PROJECT,LOCAL,OLD,INPUT,check,sha,packed,bank,normal_catalog,np,old_generate
from models import fit,predict,select,Observation
from normal_io import NormalReader,observation_from_synthetic
from metrics9 import errors,opportunities,summarize
from mfg_twin.supervisor import BudgetWriter,Limits,install_worker_limits,worker_usage

def main(out):
    start=time.monotonic();f=check();c=f['configuration'];lim=Limits(**c['limits']);enforcement=install_worker_limits(lim)
    w=BudgetWriter(out,limit_bytes=lim.output_bytes,reserve_bytes=lim.parent_reserve_bytes);now=lambda:datetime.now(timezone.utc).isoformat()
    w.write_json('provenance.json',dict(utc=now(),command=sys.argv,cwd=str(Path.cwd()),python=sys.version,platform=platform.platform(),owner='Haiqa Mushtaq',operator='Codex',
        synthetic=True,attack_generation=False,configuration=c,freeze_sha256=sha(HERE/'FREEZE.json'),enforcement=enforcement,
        dependencies=subprocess.check_output([sys.executable,'-m','pip','freeze'],text=True),git_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=PROJECT,text=True).strip(),
        git_status=subprocess.check_output(['git','status','--short'],cwd=PROJECT,text=True),threads={k:__import__('os').environ[k] for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS']}))
    reader=NormalReader(c,f['normal_files']);catalog=normal_catalog(c);fits={};selections={};candidates=[];role_maps={};allowances={};costs={}
    tick=time.perf_counter()
    for plant in ['Q1','Q2','Q3']:
        train=[reader.read(r['name'],'train') for r in catalog if r['plant']==plant and r['stage']=='train']
        dev=[reader.read(r['name'],'development') for r in catalog if r['plant']==plant and r['stage']=='development'];records=[];fits[plant]={}
        for spec in bank(c):
            begun=time.perf_counter();record=dict(plant=plant,**spec)
            try:
                model=fit(train,spec,c['warmup']);w.write_bytes(f'fit_{plant}_{spec["id"]}.npz',packed(**model));fits[plant][spec['id']]=model
                record.update(radius=float(model['radius']),parameter_count=int(model['beta'].size))
                if spec['kind']=='arx' and float(model['radius'])>=1:
                    record.update(status='rejected_unstable');records.append(record);continue
                mm=[]
                for i,e in enumerate(dev):
                    pred=predict(e,model,c['warmup']);_,r=errors(e.measurements,pred,model['scale'],c['warmup']);mm.append(dict(development_index=i,**r))
                record.update(status='eligible',development=mm,worst_development_q99=max(r['q99'] for r in mm),mean_development_rmse=float(np.mean([r['standardized_rmse'] for r in mm])))
            except Exception as exc:record.update(status='failed',error=repr(exc),traceback=traceback.format_exc())
            finally:record['fit_and_development_seconds']=time.perf_counter()-begun
            records.append(record)
        chosen=dict(overall=select(records),arx=select(records,'arx'),fir=select(records,'fir'));selections[plant]=chosen;candidates.extend(records)
        base='arx_04_1e-07';assert base in fits[plant]
        # Explicit coefficient parity with the preserved original fit, no old outcomes loaded.
        with np.load(INPUT/f'fit_{plant}.npz',allow_pickle=False) as old:
            for key in ['beta','mean','scale','radius']:np.testing.assert_array_equal(fits[plant][base][key],old[key])
        roles=dict(selected_reference=chosen['overall'],selected_arx=chosen['arx'],selected_fir=chosen['fir'],baseline_arx4=base,one_step_arx4=base,command='command')
        role_maps[plant]=roles;allowances[plant]={role:0. for role in roles}
        for row in catalog:
            if row['plant']!=plant or row['stage']!='allowance':continue
            e=reader.read(row['name'],'allowance')
            for role,mid in roles.items():
                model=fits[plant][base if mid=='command' else mid]
                pred=e.commands.copy() if mid=='command' else predict(e,model,c['warmup'],following=role=='one_step_arx4')
                s,_=errors(e.measurements,pred,model['scale'],c['warmup']);allowances[plant][role]=max(allowances[plant][role],float(s[c['warmup']:].max()))
        print('Normal fitting/selection/allowance complete: '+plant+' '+json.dumps(chosen),flush=True)
    costs['fit_select_allowance_seconds']=time.perf_counter()-tick
    w.write_json('candidates.json',candidates);w.write_json('selection.json',dict(selected=selections,roles=role_maps,allowances=allowances))
    w.write_json('SELECTION_SEALED.json',dict(utc=now(),normal_checks_opened=False,fresh_normal_generated=False,
        sha256={x.name:sha(x) for x in out.iterdir() if x.name.startswith('fit_') or x.name in ['candidates.json','selection.json']}))
    rows=[];roster=[]
    def record(e,identifier,plant,stage,condition='archived',seed=None,task=None):
        refs=[];scores=[];scale=fits[plant]['arx_04_1e-07']['scale'];roles=role_maps[plant]
        for role,mid in roles.items():
            model=fits[plant]['arx_04_1e-07' if mid=='command' else mid]
            pred=e.commands.copy() if mid=='command' else predict(e,model,c['warmup'],following=role=='one_step_arx4')
            score,er=errors(e.measurements,pred,scale,c['warmup']);op=opportunities(score,allowances[plant][role],c)
            rows.append(dict(id=identifier,plant=plant,stage=stage,role=role,model=mid,condition=condition,seed=seed,task=task,**er,**op));refs.append(pred);scores.append(score)
        w.write_bytes(identifier+'.npz',packed(measurements=e.measurements,commands=e.commands,valid=e.valid,references=np.stack(refs,axis=1),scores=np.column_stack(scores)))
        roster.append(dict(id=identifier,plant=plant,stage=stage,condition=condition,seed=seed,task=task,roles=list(roles)))
    for row in catalog:
        if row['stage']=='archived_check':record(reader.read(row['name'],'archived_check'),'check_'+row['name'][:-4],row['plant'],'archived_check')
    w.write_json('BEFORE_FRESH_NORMAL.json',dict(utc=now(),selection_seal_sha256=sha(out/'SELECTION_SEALED.json'),fresh_generated=False))
    old=json.loads((OLD/'FREEZE.json').read_text())['configuration'];cache={};tick=time.perf_counter()
    for ti,task in enumerate(c['tasks']):
        for pi,plant in enumerate(old['plants8']):
            for seed in c['seeds']:
                for condition in c['normal_conditions']:
                    assert condition in ['normal','authorized_offset','authorized_slow']
                    noise_seed=210000+ti*10000+pi*3000+seed
                    ep=old_generate(old,task,plant,condition,noise_seed,cache);obs=observation_from_synthetic(ep)
                    record(obs,f'normal_{task["id"]}_{plant["id"]}_{seed}_{condition}',plant['id'],'fresh_normal',condition,seed,task['id'])
        print('Fresh normal task complete: '+task['id'],flush=True)
    costs['fresh_generation_and_scoring_seconds']=time.perf_counter()-tick
    w.write_json('normal_roster.json',roster);w.write_json('access.json',reader.access)
    w.write_json('NORMAL_SCORES_SEALED.json',dict(utc=now(),sha256={x.name:sha(x) for x in out.iterdir() if x.suffix=='.npz' or x.name in ['selection.json','candidates.json','normal_roster.json','access.json']}))
    w.write_json('metrics.json',rows);w.write_json('fresh_summary.json',summarize([r for r in rows if r['stage']=='fresh_normal'],c));w.write_json('archived_summary.json',summarize([r for r in rows if r['stage']=='archived_check'],c))
    check();w.write_json('summary.json',dict(status='completed',utc=now(),normal_files_read=len(reader.access),candidate_attempts=len(candidates),candidate_failures=sum(r['status']!='eligible' for r in candidates),
        fresh_normal_episodes=81,archived_normal_checks=15,role_outcomes=len(rows),costs=costs,wall_seconds=time.monotonic()-start,usage=worker_usage()))
    print('Completed normal-only reference adequacy study.',flush=True)

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--output',type=Path,required=True);args=a.parse_args()
    try:main(args.output)
    except BaseException:
        err=traceback.format_exc();print(err,flush=True)
        try:BudgetWriter(args.output,limit_bytes=209715200).write_json('failure.json',dict(traceback=err,usage=worker_usage()))
        except Exception:pass
        raise
