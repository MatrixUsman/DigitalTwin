import argparse
from datetime import datetime,timezone
import json
from pathlib import Path
import platform
import subprocess
import sys
import time
import traceback
import numpy as np
from v7_common import HERE,PROJECT,OLD,LOCAL,RUN6,sha,arrays,packed,check,roster,permitted
from support import OLD_RUN
from core import bank_predictions,following_predictions
from v7_core import commands7,physical,make_components,decide,calibrate7
from v7_metrics import evaluate,summarize
from mfg_twin.supervisor import BudgetWriter,Limits,install_worker_limits,worker_usage

def main(out):
    start=time.monotonic();c=check()['configuration'];lim=Limits(**c['limits']);enforce=install_worker_limits(lim)
    w=BudgetWriter(out,limit_bytes=lim.output_bytes,reserve_bytes=lim.parent_reserve_bytes)
    now=lambda:datetime.now(timezone.utc).isoformat()
    w.write_json('provenance.json',dict(utc=now(),command=sys.argv,cwd=str(Path.cwd()),python=sys.version,platform=platform.platform(),
        owner='Haiqa Mushtaq',operator='Codex',synthetic=True,raw_access=False,configuration=c,enforcement=enforce,
        git_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=PROJECT,text=True).strip(),
        git_status=subprocess.check_output(['git','status','--short'],cwd=PROJECT,text=True),
        dependencies=subprocess.check_output([sys.executable,'-m','pip','freeze'],text=True),freeze_sha256=sha(HERE/'FREEZE.json')))
    fit=arrays(RUN6/'fit.npz');w.write_bytes('fit.npz',(RUN6/'fit.npz').read_bytes())
    oldc=json.loads((HERE.parent/'recovery_v0.6/FREEZE.json').read_text())['configuration'];settings=permitted(oldc)
    cache={};cost=dict(bank_propagation_seconds=0.,following_seconds=0.,physical_generation_seconds=0.,score_assembly_seconds=0.,
        decision_seconds=[0.]*23,normal_calibration_seconds=0.)
    def bank(u,setting):
        key=(u.tobytes(),tuple(setting['amplitude']),setting['phase_offset'])
        if key not in cache:
            tick=time.perf_counter();cache[key]=bank_predictions(u,setting);cost['bank_propagation_seconds']+=time.perf_counter()-tick
        return cache[key]
    normal=[];tick=time.monotonic()
    for p in sorted(OLD_RUN.glob('calibration_*.npz')):
        ep=arrays(p);assert not ep['attack'].any()
        comp=make_components(ep['measurements'],ep['available'],ep['valid'],ep['following'],bank(ep['available'],settings),fit,settings)
        np.testing.assert_array_equal(comp['scores'][:,:13],arrays(RUN6/p.name)['scores'])
        normal.append(comp);w.write_bytes(p.name,packed(**comp))
    oldcal=json.loads((RUN6/'calibration.json').read_text());records=[]
    for j,name in enumerate(c['methods7']):
        if j<13:r=dict(oldcal['records'][j],source='unchanged_v0.6')
        elif j in [18,19,20,21]:r=dict(threshold=oldcal['records'][11]['threshold'],source='matched_candidate_entry_diagnostic')
        else:r=dict(calibrate7(normal,j,c),source='same_normal_population')
        n=sum(int((decide(e,j,r['threshold'],settings)[0]&~decide(e,j,r['threshold'],settings)[1])[100:].sum()) for e in normal)
        r['actual_normal_alarms']=n;records.append(r)
        if j not in [18,19,20,21]:assert n<=162
    cost['normal_calibration_seconds']=time.monotonic()-tick
    w.write_json('calibration.json',dict(utc=now(),population=16200,methods=c['methods7'],records=records,old_calibration_sha256=sha(RUN6/'calibration.json')))
    before={p.name:sha(p) for p in out.iterdir() if p.suffix=='.npz' or p.name=='calibration.json'}
    w.write_json('BEFORE_FRESH_GENERATION.json',dict(utc=now(),sha256=before,fresh_generated=False))
    print('Saved thresholds and additional normal-only calibration sealed.',flush=True)
    items=roster(c);w.write_json('roster.json',items);physics={}
    for number,item in enumerate(items):
        task=next(t for t in c['tasks7'] if t['id']==item['task']);pp=next(p for p in c['plants7'] if p['id']==item['plant'])
        cc=dict(c);cc.update(task);setting=permitted(cc);ep=commands7(c,task,item['condition'])
        p=dict(c['nominal']);p['m1']*=pp['mass'][0];p['m2']*=pp['mass'][1];p['b']=(np.asarray(p['b'])*pp['damping']).tolist()
        key=(item['task'],item['plant'],item['condition'])
        if key not in physics:
            tick=time.perf_counter();physics[key]=physical(np.r_[ep['approved'][0,:2],0.,0.],ep['executed'],p,setting,pp['lag'])
            cost['physical_generation_seconds']+=time.perf_counter()-tick
        state=physics[key];noise=np.random.default_rng(item['noise_seed']).normal(size=(len(state),4))*np.asarray(c['sensor_sigma'])*pp['noise']
        y=state[:,:4]+noise;bb=bank(ep['available'],setting)
        tick=time.perf_counter();following=following_predictions(y,ep['available'],setting);cost['following_seconds']+=time.perf_counter()-tick
        tick=time.perf_counter();comp=make_components(y,ep['available'],ep['valid'],following,bb,fit,setting);cost['score_assembly_seconds']+=time.perf_counter()-tick
        alarms=[];unknown=[]
        for j in range(23):
            tick=time.perf_counter();a,u=decide(comp,j,records[j]['threshold'],setting);cost['decision_seconds'][j]+=time.perf_counter()-tick
            alarms.append(a);unknown.append(u)
        w.write_bytes(item['id']+'.npz',packed(**ep,state=state[:,:4],actuator=state[:,4:],measurements=y,following=following,bank=bb,
            reference=bb[:,1],alarm=np.column_stack(alarms),unknown=np.column_stack(unknown),**{k:v for k,v in comp.items() if k!='valid'}))
        if (number+1)%24==0:print(json.dumps(dict(stage='scored',episodes=number+1)),flush=True)
    for p,h in before.items():assert sha(out/p)==h
    seal={p.name:sha(p) for p in out.iterdir() if p.suffix=='.npz' or p.name in ['roster.json','calibration.json']}
    w.write_json('SCORES_SEALED.json',dict(utc=now(),sha256=seal,outcomes_computed=False))
    outcomes=[];pools=[]
    for item in items:
        ep=arrays(out/(item['id']+'.npz'));pools.append((item,ep))
        for j,name in enumerate(c['methods7']):outcomes.append(dict(**item,method=name,**evaluate(ep['alarm'][:,j],ep['unknown'][:,j],ep,fit,c)))
    w.write_json('outcomes.json',outcomes);w.write_json('aggregate.json',summarize(outcomes,pools,c));check()
    w.write_json('summary.json',dict(status='completed',utc=now(),episodes=144,methods=23,outcomes=len(outcomes),
        eligible_per_method=158400,costs=cost,usage=worker_usage(),wall_seconds=time.monotonic()-start,
        cost_scope='Measured shared component and decision replay totals, not independent per-method inference latency',scores_seal_sha256=sha(out/'SCORES_SEALED.json')))
    print('Complete: all scores sealed and joint outcomes saved.',flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    try:main(a.output)
    except BaseException:
        t=traceback.format_exc();print(t,flush=True)
        try:BudgetWriter(a.output,limit_bytes=167772160).write_json('failure.json',dict(traceback=t,usage=worker_usage()))
        except Exception:pass
        raise
