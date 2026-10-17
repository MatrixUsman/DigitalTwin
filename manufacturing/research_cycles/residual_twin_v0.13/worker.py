import argparse,json,sys,time,platform,subprocess,traceback
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
from io13 import HERE,PROJECT,INPUT,FITS,OLD,check,sha,packed
from model import fit,features,correct,return_evidence,alarm_machine
sys.path.insert(0,str(OLD))
from models import Observation,predict
from common9 import old_generate
from mfg_twin.supervisor import Limits,BudgetWriter,install_worker_limits,worker_usage

def main(out):
    begun=time.monotonic();f=check();c=f['configuration'];lim=Limits(**c['limits'])
    enforcement=install_worker_limits(lim)
    w=BudgetWriter(out,limit_bytes=lim.output_bytes,reserve_bytes=lim.parent_reserve_bytes)
    now=lambda:datetime.now(timezone.utc).isoformat()
    w.write_json('provenance.json',dict(utc=now(),configuration=c,command=sys.argv,cwd=str(Path.cwd()),
      python=sys.version,platform=platform.platform(),operator='Codex',requested_author='Muhammad Usman',
      synthetic=True,raw_dataset_access=False,enforcement=enforcement,freeze_sha256=sha(HERE/'FREEZE.json'),
      git_revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=PROJECT,text=True).strip(),
      git_status=subprocess.check_output(['git','status','--short'],cwd=PROJECT,text=True),
      dependencies=subprocess.check_output([sys.executable,'-m','pip','freeze'],text=True)))
    selection=json.loads((FITS/'selection.json').read_text());access=[];bases={};models={};chosen={};candidates=[];thresholds={}
    def read(plant,index,stage):
        name=f'train_{plant}_{index}.npz' if stage=='train' else f'cal_{plant}_{index:02d}.npz'
        path=INPUT/name
        if str(path.relative_to(PROJECT)) not in f['inputs']:raise ValueError('Unadmitted observation file')
        with np.load(path,allow_pickle=False) as z:e=Observation(z['measurements'],z['available'],z['valid'])
        access.append(dict(file=str(path.relative_to(PROJECT)),stage=stage,members=['measurements','available','valid']))
        return e
    def ref(e,plant,mid):
        b=predict(e,bases[plant],c['warmup'])
        return b if mid=='base' else correct(b,e.commands,models[plant][mid],bases[plant]['scale'],c['warmup'],c['command_lags'])
    for plant in ['Q1','Q2','Q3']:
        selected=selection['selected'][plant]['overall']
        with np.load(FITS/f'fit_{plant}_{selected}.npz',allow_pickle=False) as z:bases[plant]={k:z[k] for k in z.files}
        w.write_bytes(f'base_{plant}.npz',packed(**bases[plant]))
        train=[read(plant,j,'train') for j in range(3)]
        dev=[read(plant,j,'development') for j in c['development_indices']]
        xx=[];yy=[]
        for e in train:
            b=predict(e,bases[plant],c['warmup']);xx.append(features(b,e.commands,c['warmup'],c['command_lags']))
            yy.append(((e.measurements-b)/bases[plant]['scale'])[c['warmup']:])
        x=np.concatenate(xx);y=np.concatenate(yy);models[plant]={};rr=[]
        specs=[dict(kind='rbf',count=n,width_factor=h,ridge=r) for n in c['basis_counts'] for h in c['width_factors'] for r in c['ridges']]
        specs += [dict(kind='linear',count=0,width_factor=1.,ridge=r) for r in c['ridges']]
        for spec in specs:
            mid=f'{spec["kind"]}_{spec["count"]}_{spec["width_factor"]}_{spec["ridge"]}'
            tick=time.perf_counter();row=dict(plant=plant,id=mid,**spec)
            try:
                m=fit(x,y,**spec);models[plant][mid]=m;w.write_bytes(f'fit_{plant}_{mid}.npz',packed(**m));devrows=[]
                for e in dev:
                    r=ref(e,plant,mid);res=((e.measurements-r)/bases[plant]['scale'])[c['warmup']:]
                    devrows.append(dict(rmse=float(np.sqrt(np.mean(res**2))),q99=float(np.quantile(np.max(np.abs(res),axis=1),.99))))
                row.update(status='eligible',worst_q99=max(z['q99'] for z in devrows),mean_rmse=float(np.mean([z['rmse'] for z in devrows])),parameters=int(m['beta'].size),development=devrows)
            except Exception as exc:row.update(status='failed',error=repr(exc),traceback=traceback.format_exc())
            row['seconds']=time.perf_counter()-tick;rr.append(row)
        candidates.extend(rr);chosen[plant]={'base':'base'}
        for kind in ['linear','rbf']:
            eligible=[r for r in rr if r['kind']==kind and r['status']=='eligible']
            if not eligible:raise ValueError('No eligible '+kind+' for '+plant)
            chosen[plant][kind]=min(eligible,key=lambda r:(r['worst_q99'],r['mean_rmse'],r['parameters'],r['id']))['id']
        cal=[read(plant,j,'normal_calibration') for j in c['calibration_indices']];thresholds[plant]={}
        for role,mid in chosen[plant].items():
            scores=np.concatenate([np.max(np.abs((e.measurements-ref(e,plant,mid))/bases[plant]['scale']),axis=1)[c['warmup']:] for e in cal])
            rank=int(np.ceil(c['entry_quantile']*len(scores)));thresholds[plant][role]=float(np.sort(scores)[rank-1])
            assert len(scores)==5500 and rank==5445
            w.write_bytes(f'calibration_{plant}_{role}.npz',packed(scores=scores,rank=np.array(rank)))
        print('Selected '+plant+' '+json.dumps(chosen[plant]),flush=True)
    w.write_json('candidates.json',candidates);w.write_json('selection.json',dict(models=chosen,thresholds=thresholds))
    w.write_json('access.json',access)
    w.write_json('SELECTION_SEALED.json',dict(utc=now(),fresh_generated=False,sha256={p.name:sha(p) for p in out.iterdir() if p.suffix=='.npz' or p.name in ['candidates.json','selection.json','access.json']}))
    sim=json.loads((PROJECT/'research_cycles/recovery_v0.8/FREEZE.json').read_text())['configuration'];cache={};rows=[]
    for ti,task in enumerate(c['tasks']):
        for pi,plant in enumerate(sim['plants8']):
            name=plant['id'];scale=bases[name]['scale']
            for seed in c['seeds']:
                for condition in c['normal_conditions']:
                    noise_seed=310000+ti*10000+pi*3000+seed
                    episode=old_generate(sim,task,plant,condition,noise_seed,cache)
                    # Explicit observed-data boundary: models never receive episode truth.
                    e=Observation(episode['measurements'],episode['available'],episode['valid'])
                    rid=f'normal_{task["id"]}_{name}_{seed}_{condition}';refs=[];residuals=[]
                    for role,mid in chosen[name].items():
                        tick=time.perf_counter();r=ref(e,name,mid);res=(e.measurements-r)/scale
                        score=np.max(np.abs(res),axis=1);part=res[c['warmup']:]
                        row=dict(id=rid,plant=name,task=task['id'],seed=seed,condition=condition,role=role,model=mid,eligible=len(part),rmse=float(np.sqrt(np.mean(part**2))),q99=float(np.quantile(score[c['warmup']:],.99)),point_alarms=int(np.sum(score[c['warmup']:] > thresholds[name][role])),gate={})
                        for gate,windows in [('point',[1]),('long',[41]),('dual',c['return_windows'])]:
                            ok,known=return_evidence(res,e.valid,windows=windows,tolerance=c['return_tolerance'],start=c['warmup'])
                            known[:c['warmup']]=False
                            alarm=alarm_machine(score,known,ok,thresholds[name][role],c['dwell'])
                            successes=0
                            for start in c['probe_indices']:
                                streak=0
                                for t in range(start,min(len(ok),start+c['probe_horizon'])):
                                    streak=streak+1 if ok[t] else 0
                                    if streak>=c['dwell']:successes+=1;break
                            row['gate'][gate]=dict(evidence_points=int(ok[c['warmup']:].sum()),probe_success=successes,probes=4,alarm_points=int(alarm[c['warmup']:].sum()))
                        row['prediction_and_gate_seconds']=time.perf_counter()-tick;rows.append(row);refs.append(r);residuals.append(res)
                    w.write_bytes(rid+'.npz',packed(measurements=e.measurements,commands=e.commands,valid=e.valid,references=np.stack(refs,axis=1),residuals=np.stack(residuals,axis=1)))
        print('Scored fresh normal task '+task['id'],flush=True)
    w.write_json('SCORES_SEALED.json',dict(utc=now(),sha256={p.name:sha(p) for p in out.iterdir() if p.suffix=='.npz'}))
    w.write_json('outcomes.json',rows);summary=[]
    for plant in ['Q1','Q2','Q3']:
        for role in ['base','linear','rbf']:
            rr=[r for r in rows if r['plant']==plant and r['role']==role]
            parts=[]
            for r in rr:
                with np.load(out/(r['id']+'.npz'),allow_pickle=False) as z:
                    parts.append(z['residuals'][c['warmup']:,['base','linear','rbf'].index(role)])
            residual=np.concatenate(parts)
            summary.append(dict(plant=plant,role=role,model=chosen[plant][role],episodes=len(rr),eligible=len(residual),rmse=float(np.sqrt(np.mean(residual**2))),q99=float(np.quantile(np.max(np.abs(residual),axis=1),.99)),point_alarms=sum(r['point_alarms'] for r in rr),gate={gate:{key:sum(r['gate'][gate][key] for r in rr) for key in ['evidence_points','probe_success','probes','alarm_points']} for gate in ['point','long','dual']}))
    tests={}
    for plant in ['Q1','Q2','Q3']:
        d={r['role']:r for r in summary if r['plant']==plant}
        tests[plant]=dict(rmse_improved=d['rbf']['rmse']<d['base']['rmse'],q99_not_increased=d['rbf']['q99']<=d['base']['q99'])
    check();w.write_json('summary.json',dict(status='completed',utc=now(),candidate_attempts=len(candidates),candidate_failures=sum(r['status']!='eligible' for r in candidates),fresh_normal_episodes=81,reference_outcomes=len(rows),rows=summary,primary=tests,primary_pass=all(all(r.values()) for r in tests.values()),wall_seconds=time.monotonic()-begun,usage=worker_usage(),attack_metrics=None,novelty_established=False))

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--output',type=Path,required=True);out=a.parse_args().output
    try:main(out)
    except BaseException:
        error=traceback.format_exc();print(error,flush=True)
        try:BudgetWriter(out,limit_bytes=52428800).write_json('failure.json',dict(traceback=error,usage=worker_usage()))
        except Exception:pass
        raise
