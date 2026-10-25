from pathlib import Path
import hashlib,json
import numpy as np
H=Path(__file__).resolve().parent;P=H.parents[2]
METHODS=('rapt_model','rapt_hybrid')
START=100

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def check():
    f=json.loads((H/'FREEZE.json').read_text())
    for path,digest in f['bindings'].items():
        if sha(P/path)!=digest:raise ValueError('Frozen binding changed: '+path)
    return f

def validate_population(rows):
    expected={(t,s,c) for t in ['L19','S19'] for s in [17,42,2026] for c in ['normal','authorized_changes','brief_offset','persistent_offset','hold','slow']}
    if len(rows)!=36 or len({r['id'] for r in rows})!=36 or {(r['task'],r['seed'],r['condition']) for r in rows}!=expected or any(r['plant']!='Q1' for r in rows):
        raise ValueError('Expected complete unique 36-episode Q1 grid')

def decisions(risk,start=START):
    x=np.asarray(risk,float)
    if x.ndim!=1 or not np.isfinite(x).all():raise ValueError('Invalid risk')
    a=x>1.;a[:start]=False
    return a

def quarters(risk,alarm,attack,state,truth,scale):
    ii=np.flatnonzero(attack)
    if not len(ii):return None
    lo,hi=int(ii[0]),int(ii[-1])+1
    if not np.asarray(attack)[lo:hi].all():raise ValueError('Noncontiguous interval')
    n=max(1,(hi-lo)//4);outside=np.max(np.abs((state-truth)/scale),axis=1)>.1
    result=dict(interval_points=hi-lo,quarter_points=n)
    for name,sl in [('first',slice(lo,lo+n)),('last',slice(hi-n,hi))]:
        x=np.asarray(risk)[sl];a=np.asarray(alarm)[sl];o=outside[sl]
        result[name]=dict(risk_median=float(np.median(x)),risk_max=float(x.max()),alarm_points=int(a.sum()),points=len(x),outside_points=int(o.sum()),outside_inactive=int((o&~a).sum()))
    return result

def distribution(x):
    y=np.asarray([v for v in x if v is not None],float)
    return dict(n=len(y),median=float(np.median(y)) if len(y) else None,p95=float(np.quantile(y,.95)) if len(y) else None,max=float(y.max()) if len(y) else None)

def summarize(rows):
    result=[]
    groups=[('pooled','all')]+[(k,v) for k in ['task','condition'] for v in sorted({r[k] for r in rows})]
    for key,value in groups:
      for method in METHODS:
        rr=[r for r in rows if r['method']==method and (key=='pooled' or r[key]==value)]
        b=[r for r in rr if r['benign']];ev=[r for r in rr if r['event']]
        tp,fp,fn,tn=[sum(r[k] for r in rr) for k in ['tp','fp','fn','tn']]
        n=sum(r['eligible'] for r in b);alarms=sum(r['alarm_points'] for r in b);starts=sum(r['alarm_episodes'] for r in b)
        outside=sum(r['outside_points'] for r in ev);inactive=sum(r['outside_inactive'] for r in ev)
        result.append(dict(group=key,value=value,method=method,episodes=len(rr),eligible=sum(r['eligible'] for r in rr),tp=tp,fp=fp,fn=fn,tn=tn,
            precision=tp/(tp+fp) if tp+fp else 0.,recall=tp/(tp+fn) if tp+fn else None,f1=2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 0.,
            benign_points=n,benign_alarms=alarms,benign_fraction=alarms/n if n else None,benign_starts=starts,benign_hours=n*.02/3600,benign_starts_per_hour=starts/(n*.02/3600) if n else None,
            events=len(ev),hits=sum(r['overlap'] for r in ev),fresh=sum(r['fresh'] for r in ev),misses=sum(not r['overlap'] for r in ev),premature=sum(r['premature'] for r in ev),
            outside_points=outside,outside_inactive=inactive,outside_inactive_fraction=inactive/outside if outside else None,
            absent_return=sum(r['return_missing'] for r in ev),inactive_by_return_plus_5=sum(r['clear_timely'] for r in ev),already_inactive_at_return=sum(r['already_clear_at_return'] for r in ev),
            detection_delay=distribution([r['detection_delay'] for r in ev]),fresh_delay=distribution([r['fresh_delay'] for r in ev]),clearance_delay=distribution([r['clear_delay'] for r in ev])))
    return result
