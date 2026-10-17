import argparse,json,sys,time,platform,subprocess,traceback
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
from common import HERE,PROJECT,sha,arrays,packed,check
from mechanism import fit_reference,decide,calibrate
from simulation import generate,monitor_inputs,commissioning_task,calibration_task
from metrics8 import evaluate,summarize
from mfg_twin.supervisor import BudgetWriter,Limits,install_worker_limits,worker_usage

def main(out):
    start=time.monotonic();c=check()['configuration'];lim=Limits(**c['limits']);enforcement=install_worker_limits(lim)
    w=BudgetWriter(out,limit_bytes=lim.output_bytes,reserve_bytes=lim.parent_reserve_bytes);now=lambda:datetime.now(timezone.utc).isoformat()
    w.write_json('provenance.json',dict(utc=now(),configuration=c,command=sys.argv,cwd=str(Path.cwd()),python=sys.version,platform=platform.platform(),
        owner='Haiqa Mushtaq',operator='Codex',synthetic=True,enforcement=enforcement,raw_access=False,freeze_sha256=sha(HERE/'FREEZE.json'),
        git_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=PROJECT,text=True).strip(),git_status=subprocess.check_output(['git','status','--short'],cwd=PROJECT,text=True),
        dependencies=subprocess.check_output([sys.executable,'-m','pip','freeze'],text=True)))
    fits={};calibrations={};costs={};cache={};started=time.perf_counter()
    for pi,p in enumerate(c['plants8']):
        train=[]
        for i in range(3):
            e=generate(c,commissioning_task(i),p,['normal','authorized_offset','authorized_slow'][i],120000+1000*pi+i,cache)
            assert not e['attack'].any();train.append(e);w.write_bytes(f'train_{p["id"]}_{i}.npz',packed(**e))
        fit=fit_reference(train,c['order'],c['ridge'],c['warmup']);fits[p['id']]=fit
        w.write_bytes(f'fit_{p["id"]}.npz',packed(**fit));normal=[]
        for i in range(c['calibration_episodes']):
            ep=generate(c,calibration_task(i),p,['normal','authorized_offset','authorized_slow'][i%3],130000+1000*pi+i,cache)
            comp=monitor_inputs(ep,fit,c);normal.append(comp);w.write_bytes(f'cal_{p["id"]}_{i:02d}.npz',packed(**ep,**{k:v for k,v in comp.items() if k!='valid'}))
        b=float(max(e['learned_error'][c['warmup']:].max() for e in normal));records=[]
        for j,name in enumerate(c['methods8']):
            if j==10:r=dict(threshold=b,source='episode_maximum_separate_track')
            elif j in [11,12]:r=dict(threshold=records[9]['threshold'],source='matched_candidate_entry')
            else:r=dict(calibrate(normal,j,b,c),source='normal_budget')
            r['actual_alarms']=sum(int((decide(e,j,r['threshold'],b,c)[0]&~decide(e,j,r['threshold'],b,c)[1])[c['warmup']:].sum()) for e in normal)
            records.append(r)
        calibrations[p['id']]=dict(allowance=b,reference_radius=float(fit['radius']),records=records,population=20900)
        print('Commissioning and calibration completed: '+p['id'],flush=True)
    costs['commissioning_calibration_seconds']=time.perf_counter()-started
    w.write_json('calibration.json',dict(utc=now(),plants=calibrations))
    before={p.name:sha(p) for p in out.iterdir() if p.suffix=='.npz' or p.name=='calibration.json'}
    w.write_json('BEFORE_FRESH_GENERATION.json',dict(utc=now(),sha256=before,fresh_generated=False));cache={}
    roster=[dict(id=f'eval_{t["id"]}_{p["id"]}_{seed}_{condition}',task=t['id'],plant=p['id'],seed=seed,condition=condition,
        noise_seed=140000+ti*10000+pi*1000+seed) for ti,t in enumerate(c['tasks8']) for pi,p in enumerate(c['plants8']) for seed in c['seeds'] for condition in c['conditions']]
    w.write_json('roster.json',roster);timings=np.zeros(13);started=time.perf_counter()
    for number,item in enumerate(roster):
        task=next(t for t in c['tasks8'] if t['id']==item['task']);p=next(p for p in c['plants8'] if p['id']==item['plant']);fit=fits[p['id']];cal=calibrations[p['id']]
        ep=generate(c,task,p,item['condition'],item['noise_seed'],cache);comp=monitor_inputs(ep,fit,c);aa=[];uu=[]
        for j in range(13):
            tick=time.perf_counter();a,u=decide(comp,j,cal['records'][j]['threshold'],cal['allowance'],c);timings[j]+=time.perf_counter()-tick;aa.append(a);uu.append(u)
        w.write_bytes(item['id']+'.npz',packed(**ep,**{k:v for k,v in comp.items() if k!='valid'},alarm=np.column_stack(aa),unknown=np.column_stack(uu)))
        if (number+1)%36==0:print('Scored '+str(number+1)+' episodes',flush=True)
    costs['generation_scoring_seconds']=time.perf_counter()-started;costs['decision_seconds']=timings.tolist()
    for n,h in before.items():assert sha(out/n)==h
    w.write_json('SCORES_SEALED.json',dict(utc=now(),sha256={p.name:sha(p) for p in out.iterdir() if p.suffix=='.npz' or p.name in ['roster.json','calibration.json']},outcomes_computed=False))
    rows=[];pools=[];disagreements=[]
    for item in roster:
        ep=arrays(out/(item['id']+'.npz'));pools.append((item,ep));fit=fits[item['plant']]
        for j,name in enumerate(c['methods8']):
            evaluation=dict(ep,reference=ep['truth_reference'])
            r=evaluate(ep['alarm'][:,j],ep['unknown'][:,j],evaluation,fit,c)
            rows.append(dict(**item,method=name,**r))
            if j==9 and r['attack_present']:
                old=evaluate(ep['alarm'][:,j],ep['unknown'][:,j],dict(ep,reference=ep['nominal_reference']),fit,c)
                disagreements.append(dict(id=item['id'],paired_return=r['physical_return_steps'],nominal_return=old['physical_return_steps'],paired_early=r['premature_clear'],nominal_early=old['premature_clear']))
    w.write_json('outcomes.json',rows);w.write_json('aggregate.json',summarize(rows,pools,c));w.write_json('reference_disagreements.json',disagreements)
    check();w.write_json('summary.json',dict(status='completed',utc=now(),episodes=len(roster),methods=13,outcomes=len(rows),usage=worker_usage(),wall_seconds=time.monotonic()-start,costs=costs,scores_seal_sha256=sha(out/'SCORES_SEALED.json')))
    print('Completed all scores and jointly evaluated outcomes.',flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);arg=parser.parse_args()
    try:main(arg.output)
    except BaseException:
        error=traceback.format_exc();print(error,flush=True)
        try:BudgetWriter(arg.output,limit_bytes=268435456).write_json('failure.json',dict(traceback=error,usage=worker_usage()))
        except Exception:pass
        raise
