"""Fresh-process inference replay and separately computed event arithmetic."""
import os
for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[key]='1'
import json,time
import numpy as np
from io14 import HERE,PROJECT,RUN,MODELS,sha,check,load_npz,Observation
from audit_core import infer,alarm_scores,ROLES,specification,settings
from mfg_twin.metrics import average_precision as reference_ap

begun=time.monotonic();f=check();c=f['configuration'];dc=settings(c);nchecks=0
def require(ok,msg):
    global nchecks
    nchecks+=1
    if not ok:raise AssertionError(msg)
def close(a,b,msg):require(np.allclose(a,b,rtol=1e-10,atol=1e-12),msg)
require(json.loads((RUN/'supervisor.json').read_text())['status']=='completed','supervision')
for name in ['CALIBRATION_SEALED.json','SCORES_SEALED.json']:
    for rel,h in json.loads((RUN/name).read_text())['sha256'].items():require(sha(RUN/rel)==h,'seal '+rel)
cal=json.loads((RUN/'calibration.json').read_text());prior=json.loads((MODELS/'selection.json').read_text());models={}
for p in ['Q1','Q2','Q3']:
    models[p]={'base':load_npz(MODELS/f'base_{p}.npz')}
    for role in ['linear','rbf']:models[p][role]=load_npz(MODELS/f'fit_{p}_{prior["models"][p][role]}.npz')
    t=load_npz(RUN/f'training_statistic_{p}.npz')['scores'];require(len(t)==3300,'training count')
    close(np.mean(t)+np.std(t),cal['cusum_k'][p],'CUSUM training statistic')
    s=np.concatenate([load_npz(RUN/f'calibration_{p}_{i:02d}.npz')['scores'][100:] for i in range(5)])
    require(s.shape==(5500,8),'calibration coverage')
    for i,role in enumerate(ROLES):close(np.sort(s[:,i])[5444],cal['thresholds'][p][role],'threshold rank')
    for role in ['base','linear','rbf']:require(cal['thresholds'][p][role]==prior['thresholds'][p][role],'unchanged threshold')
access=json.loads((RUN/'access.json').read_text());require(len(access)==24,'normal accesses')
require(len({r['file'] for r in access})==24,'disjoint file accesses')
require(all(r['file'] in f['inputs'] and r['members']==['measurements','available','valid'] for r in access),'allowed access boundary')
rows=json.loads((RUN/'outcomes.json').read_text());summary=json.loads((RUN/'summary.json').read_text());catalog=json.loads((RUN/'catalog.json').read_text())
require(len(catalog)==189 and len(rows)==3213,'complete campaign')
by={(r['id'],r['method']):r for r in rows};require(len(by)==3213,'unique outcomes')
pool={p:[] for p in ['pooled','Q1','Q2','Q3']}
for item in catalog:
    rid=item['id'];p=item['plant'];z=load_npz(RUN/('score_'+rid+'.npz'));t=load_npz(RUN/('truth_'+rid+'.npz'))
    obs=Observation(z['measurements'],z['commands'],z['valid']);ref,res,score=infer(obs,models[p],cal['cusum_k'][p],dc)
    close(ref,z['references'],'reference replay');close(score,z['scores'],'score replay')
    require(np.array_equal(alarm_scores(score,res,obs.valid,cal['thresholds'][p],dc),z['alarms']),'alarm replay')
    changed=z['measurements'].copy();changed[100:]+=500
    second=infer(Observation(changed,z['commands'],z['valid']),models[p],cal['cusum_k'][p],dc)[0]
    require(np.array_equal(ref[:,:3],second[:,:3]),'protected reference isolation')
    for group in ['pooled',p]:pool[group].append((t['attack'][100:],score[100:]))
    indices=np.flatnonzero(t['attack']);onset=int(indices[0]) if len(indices) else None;end=int(indices[-1])+1 if len(indices) else None
    returned=None
    if len(indices):
        dist=np.max(np.abs((t['state']-t['counterfactual'])/models[p]['base']['scale']),axis=1)
        returned=next((i for i in range(end,len(dist)-9) if all(dist[i:i+10]<=.1)),None)
    for j,method in enumerate(c['methods']):
        row=by[rid,method];a=z['alarms'][:,j];y=t['attack'];aa=a[100:];yy=y[100:]
        require(row['eligible']==1100,'coverage')
        for key,val in [('tp',np.count_nonzero(aa&yy)),('fp',np.count_nonzero(aa&~yy)),('fn',np.count_nonzero(~aa&yy)),('tn',np.count_nonzero(~aa&~yy))]:require(row[key]==val,'contingency '+key)
        starts=[i for i in range(100,1200) if a[i] and not a[i-1]]
        require(row['alarm_points']==int(aa.sum()) and row['alarm_episodes']==len(starts),'alarm burden')
        if onset is not None:
            hits=[i for i in range(onset,end) if a[i]];fresh=[i for i in starts if onset<=i<end]
            require(row['overlap']==bool(hits) and row['fresh']==bool(fresh),'event outcomes')
            require(row['physical_return']==returned,'counterfactual return')
            require(row['detection_delay']==((hits[0]-onset)*.02 if hits else None),'delay includes misses')
            if hits:
                stop=returned if returned is not None else 1200
                gaps=sum(not a[i] for i in range(hits[0],stop))
                premature=any(a[i-1] and not a[i] for i in range(hits[0]+1,stop))
                require(row['gap_points']==gaps and row['premature']==premature,'all pre-return gaps')
                free=next((i for i in range(returned,min(1200,returned+251)) if not a[i]),None) if returned is not None else None
                require(row['clear_delay']==((free-returned)*.02 if free is not None else None),'clear/censor')
            else:require(row['clear_delay'] is None and not row['returned_detected'],'miss not hidden')
for sr in summary['rows']:
    rr=[r for r in rows if r['method']==sr['method'] and (sr['stratum']=='pooled' or sr['stratum']==r['plant'])]
    for key in ['tp','fp','fn','tn','eligible']:require(sr[key]==sum(r[key] for r in rr),'aggregate '+key)
    den=2*sr['tp']+sr['fp']+sr['fn'];close(sr['f1'],2*sr['tp']/den,'F1')
    benign=[r for r in rr if r['benign']];events=[r for r in rr if r['event']]
    require(sr['benign_alarms']==sum(r['alarm_points'] for r in benign),'benign denominator')
    for key,field in [('hits','overlap'),('fresh_hits','fresh'),('premature','premature'),('clear_timely','clear_timely')]:require(sr[key]==sum(r[field] for r in events),'aggregate event')
    require(sr['events']==len(events) and sr['misses']==sum(not r['overlap'] for r in events),'all missed events')
for stratum,parts in pool.items():
    labels=np.concatenate([a for a,b in parts]).astype(int).tolist();scores=np.concatenate([b for a,b in parts])
    for i,role in enumerate(ROLES):
        ap=reference_ap(labels,scores[:,i].tolist())
        for row in summary['rows']:
            if row['stratum']==stratum and specification(row['method'])[0]==role:close(row['average_precision'],ap,'independent AP')
tests={}
for p in ['Q1','Q2','Q3']:
    d={r['method']:r for r in summary['rows'] if r['stratum']==p};a=d['rbf_dual'];b=d['base_dual']
    tests[p]={k:a[k]>=b[k] for k in ['hits','fresh_hits','clear_timely']}
    tests[p].update({k:a[k]<=b[k] for k in ['premature','benign_alarms','gap_points']})
require(tests==summary['primary']['noninferiority'],'primary plant checks')
d={r['method']:r for r in summary['rows'] if r['stratum']=='pooled'};a=d['rbf_dual'];b=d['base_dual']
effects={k:1-a[k]/b[k] if b[k] else None for k in ['benign_alarms','gap_points']}
require(effects==summary['primary']['pooled_reduction_fractions'],'effect sizes')
require(summary['primary']['passed']==(all(all(v.values()) for v in tests.values()) and any(v is not None and v>=.1 for v in effects.values())),'primary verdict')
check();record=dict(status='passed',scope='deterministic saved inference replay and independently recomputed metrics; not independent physical validation',checks=nchecks,seconds=time.monotonic()-begun,
 freeze_sha256=sha(HERE/'FREEZE.json'),run_sha256={p.name:sha(p) for p in RUN.iterdir() if p.is_file()})
with (HERE/'VERIFICATION.json').open('x') as f:json.dump(record,f,indent=2);f.write('\n')
print(json.dumps({k:v for k,v in record.items() if k!='run_sha256'},indent=2))
