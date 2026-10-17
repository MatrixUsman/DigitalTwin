"""Recompute saved predictions and diagnostics, without fitting or simulation."""
import json,sys,time
import numpy as np
from io13 import HERE,PROJECT,RUN,LOCAL,OLD,sha,check
from model import correct
sys.path.insert(0,str(OLD))
from models import Observation,predict

started=time.monotonic();f=check();c=f['configuration'];checks=0
def require(ok,message):
    global checks
    checks+=1
    if not ok:raise AssertionError(message)
def equal(a,b,message):require(np.allclose(a,b,rtol=1e-11,atol=1e-12),message)
def read(name):
    with np.load(RUN/name,allow_pickle=False) as z:return {k:z[k] for k in z.files}

supervisor=json.loads((RUN/'supervisor.json').read_text());require(supervisor['status']=='completed','supervision')
for filename in ['SELECTION_SEALED.json','SCORES_SEALED.json']:
    for name,h in json.loads((RUN/filename).read_text())['sha256'].items():require(sha(RUN/name)==h,'seal '+name)
selection=json.loads((RUN/'selection.json').read_text());cand=json.loads((RUN/'candidates.json').read_text())
summary=json.loads((RUN/'summary.json').read_text());outcomes=json.loads((RUN/'outcomes.json').read_text())
require(len(cand)==30,'all fits accounted for');require(len(outcomes)==243,'all reference outcomes')
access=json.loads((RUN/'access.json').read_text())
require(len(access)==51 and len({x['file'] for x in access})==51,'unique allowlisted files')
require(all(x['file'] in f['inputs'] and x['members']==['measurements','available','valid'] for x in access),'input boundary')
bases={p:read(f'base_{p}.npz') for p in ['Q1','Q2','Q3']};models={}
for p in bases:
    models[p]={}
    for role in ['base','linear','rbf']:
        if role!='base':
            eligible=[r for r in cand if r['plant']==p and r['kind']==role and r['status']=='eligible']
            chosen=min(eligible,key=lambda r:(r['worst_q99'],r['mean_rmse'],r['parameters'],r['id']))['id']
            require(chosen==selection['models'][p][role],'declared selection')
            models[p][role]=read(f'fit_{p}_{chosen}.npz')
        cal=read(f'calibration_{p}_{role}.npz');require(cal['scores'].shape==(5500,),'calibration population')
        require(int(cal['rank'])==5445,'calibration rank');equal(np.sort(cal['scores'])[5444],selection['thresholds'][p][role],'threshold')
require(summary['candidate_failures']==sum(r['status']!='eligible' for r in cand),'failures retained')
pooled={(p,r):[] for p in bases for r in ['base','linear','rbf']};groups={}
for row in outcomes:groups.setdefault(row['id'],[]).append(row)
require(len(groups)==81,'unique episodes')
for rid,rr in groups.items():
    z=read(rid+'.npz');p=rr[0]['plant'];base=bases[p]
    obs=Observation(z['measurements'],z['commands'],z['valid']);b=predict(obs,base,c['warmup'])
    changed=z['measurements'].copy();changed[100:]+=1000.
    other=predict(Observation(changed,z['commands'],z['valid']),base,c['warmup'])
    require(np.array_equal(b,other),'post-initialization measurement isolation')
    for j,role in enumerate(['base','linear','rbf']):
        row=next(r for r in rr if r['role']==role)
        r=b if role=='base' else correct(b,obs.commands,models[p][role],base['scale'],100,c['command_lags'])
        equal(r,z['references'][:,j],'reference reload');e=(obs.measurements-r)/base['scale']
        equal(e,z['residuals'][:,j],'residual');part=e[100:];pooled[p,role].append(part)
        score=np.max(np.abs(e),axis=1);threshold=selection['thresholds'][p][role]
        equal(np.sqrt(np.mean(part**2)),row['rmse'],'episode rmse');equal(np.quantile(score[100:],.99),row['q99'],'episode q99')
        require(row['eligible']==1100,'coverage');require(int((score[100:]>threshold).sum())==row['point_alarms'],'point alarms')
        # Independently use direct convolution, rather than the implementation's cumulative sums.
        for gate,widths in [('point',[1]),('long',[41]),('dual',[5,41])]:
            ok=np.zeros(1200,bool);ok[100:]=True
            for width in widths:
                means=np.column_stack([np.convolve(e[:,k],np.ones(width)/width,'valid') for k in range(4)])
                a=np.zeros(1200,bool);a[width-1:]=np.max(np.abs(means),axis=1)<=.1;a[:100+width-1]=False;ok &= a
            require(int(ok[100:].sum())==row['gate'][gate]['evidence_points'],'direct mean evidence')
            active=False;streak=0;alarm_count=0
            for t in range(100,1200):
                if score[t]>threshold:active=True;streak=0
                elif active:
                    streak=streak+1 if ok[t] else 0
                    if streak>=10:active=False;streak=0
                alarm_count+=int(active)
            require(alarm_count==row['gate'][gate]['alarm_points'],'alarm state replay')
            success=0
            for start in c['probe_indices']:
                mask=ok[start:min(1200,start+250)]
                success+=int(np.any(np.convolve(mask.astype(int),np.ones(10,dtype=int),'valid')==10))
            require(success==row['gate'][gate]['probe_success'],'probe diagnostic')
for row in summary['rows']:
    e=np.concatenate(pooled[row['plant'],row['role']]);require(len(e)==29700,'pooled coverage')
    equal(np.sqrt(np.mean(e**2)),row['rmse'],'pooled rmse');equal(np.quantile(np.max(np.abs(e),axis=1),.99),row['q99'],'pooled q99')
    rr=[r for r in outcomes if r['plant']==row['plant'] and r['role']==row['role']]
    require(sum(r['point_alarms'] for r in rr)==row['point_alarms'],'pooled alarms')
    for gate in ['point','long','dual']:
        for metric in ['evidence_points','probe_success','probes','alarm_points']:
            require(sum(r['gate'][gate][metric] for r in rr)==row['gate'][gate][metric],'pooled gate')
primary={}
for p in bases:
    d={r['role']:r for r in summary['rows'] if r['plant']==p}
    primary[p]=dict(rmse_improved=d['rbf']['rmse']<d['base']['rmse'],q99_not_increased=d['rbf']['q99']<=d['base']['q99'])
require(primary==summary['primary'],'primary checks');require(all(all(v.values()) for v in primary.values())==summary['primary_pass'],'primary conclusion')
check()
record=dict(status='passed',scope='saved-artifact deterministic prediction replay and independent metric arithmetic; no independent experiment',checks=checks,seconds=time.monotonic()-started,freeze_sha256=sha(HERE/'FREEZE.json'),run_sha256={p.name:sha(p) for p in RUN.iterdir() if p.is_file()})
with (HERE/'VERIFICATION.json').open('x') as out:json.dump(record,out,indent=2);out.write('\n')
print(json.dumps({k:v for k,v in record.items() if k!='run_sha256'},indent=2))
