"""Evaluator-only labels and same-plant counterfactual physical return."""
import numpy as np

def average_precision(labels,scores):
    y=np.asarray(labels,dtype=bool);s=np.asarray(scores,dtype=float)
    if y.shape!=s.shape or not np.isfinite(s).all():raise ValueError('Invalid AP inputs')
    total=int(y.sum())
    if not total:return None
    order=np.argsort(-s,kind='stable');y=y[order];s=s[order]
    ends=np.r_[np.flatnonzero(s[1:]!=s[:-1]),len(s)-1]
    tp=np.cumsum(y)[ends];p=tp/(ends+1);recall=tp/total
    return float(np.sum(np.diff(np.r_[0.,recall])*p))

def evaluate(alarm,attack,state,truth,scale,c):
    alarm=np.asarray(alarm,bool);attack=np.asarray(attack,bool);start=c['warmup'];dt=.02
    if alarm.shape!=attack.shape or state.shape!=truth.shape or state.shape!=(len(alarm),4):raise ValueError('Alignment')
    if not np.isfinite(state).all() or not np.isfinite(truth).all():raise ValueError('Nonfinite truth')
    a=alarm[start:];y=attack[start:]
    rising=alarm & ~np.r_[False,alarm[:-1]]
    row=dict(eligible=len(a),tp=int((a&y).sum()),fp=int((a&~y).sum()),fn=int((~a&y).sum()),
             tn=int((~a&~y).sum()),benign=not bool(attack.any()),alarm_points=int(a.sum()),
             alarm_episodes=int(rising[start:].sum()),event=bool(attack.any()),overlap=False,fresh=False,
             detection_delay=None,fresh_delay=None,physical_return=None,return_missing=False,
             premature=False,gap_points=None,returned_detected=False,clear_delay=None,clear_timely=False,already_clear_at_return=False)
    indices=np.flatnonzero(attack)
    if not len(indices):return row
    onset,end=int(indices[0]),int(indices[-1])+1
    if not attack[onset:end].all() or onset<start:raise ValueError('Expected one eligible interval')
    row.update(onset=onset,end=end)
    hits=np.flatnonzero(alarm[onset:end]);fresh=np.flatnonzero(rising[onset:end])
    row['overlap']=bool(len(hits));row['fresh']=bool(len(fresh))
    if len(hits):row['detection_delay']=float(hits[0]*dt)
    if len(fresh):row['fresh_delay']=float(fresh[0]*dt)
    distance=np.max(np.abs((state-truth)/scale),axis=1)
    good=distance[end:]<=c['return_tolerance'];dwell=c['dwell']
    windows=np.convolve(good.astype(int),np.ones(dwell,dtype=int),'valid') if len(good)>=dwell else np.array([])
    runs=np.flatnonzero(windows==dwell)
    returned=end+int(runs[0]) if len(runs) else None
    row['physical_return']=returned;row['return_missing']=returned is None
    if len(hits):
        first=onset+int(hits[0]);stop=returned if returned is not None else len(alarm)
        row['gap_points']=int((~alarm[first:stop]).sum())
        falls=np.flatnonzero(alarm[:-1]&~alarm[1:])+1
        row['premature']=bool(np.any((falls>first)&(falls<stop)))
        if returned is not None:
            row['returned_detected']=True;row['already_clear_at_return']=not bool(alarm[returned])
            free=np.flatnonzero(~alarm[returned:min(len(alarm),returned+c['recovery_horizon']+1)])
            if len(free):row['clear_delay']=float(free[0]*dt);row['clear_timely']=True
    return row

def aggregate(rows,methods):
    output=[]
    for stratum in ['pooled','Q1','Q2','Q3']:
        for method in methods:
            rr=[r for r in rows if r['method']==method and (stratum=='pooled' or r['plant']==stratum)]
            benign=[r for r in rr if r['benign']];events=[r for r in rr if r['event']]
            tp,fp,fn,tn=[sum(r[k] for r in rr) for k in ['tp','fp','fn','tn']]
            n=sum(r['eligible'] for r in benign);alarms=sum(r['alarm_points'] for r in benign);eps=sum(r['alarm_episodes'] for r in benign)
            output.append(dict(stratum=stratum,method=method,episodes=len(rr),eligible=sum(r['eligible'] for r in rr),
              tp=tp,fp=fp,fn=fn,tn=tn,precision=tp/(tp+fp) if tp+fp else 0.,recall=tp/(tp+fn),
              f1=2*tp/(2*tp+fp+fn),benign_points=n,benign_alarms=alarms,benign_fraction=alarms/n,
              benign_episodes=eps,benign_episodes_per_hour=eps/(n*.02/3600),
              events=len(events),hits=sum(r['overlap'] for r in events),fresh_hits=sum(r['fresh'] for r in events),
              misses=sum(not r['overlap'] for r in events),premature=sum(r['premature'] for r in events),
              gap_points=sum(r['gap_points'] or 0 for r in events),return_missing=sum(r['return_missing'] for r in events),
              returned_detected=sum(r['returned_detected'] for r in events),clear_timely=sum(r['clear_timely'] for r in events),
              already_clear_at_return=sum(r['already_clear_at_return'] for r in events)))
    return output

def primary(rows,c):
    tests={}
    for plant in ['Q1','Q2','Q3']:
        d={r['method']:r for r in rows if r['stratum']==plant};a=d[c['primary_candidate']];b=d[c['primary_control']]
        tests[plant]={k:(a[k]>=b[k]) for k in ['hits','fresh_hits','clear_timely']}
        tests[plant].update({k:(a[k]<=b[k]) for k in ['premature','benign_alarms','gap_points']})
    d={r['method']:r for r in rows if r['stratum']=='pooled'};a=d[c['primary_candidate']];b=d[c['primary_control']]
    effects={k:(1-a[k]/b[k] if b[k]>0 else None) for k in ['benign_alarms','gap_points']}
    benefit=any(v is not None and v>=c['benefit_fraction'] for v in effects.values())
    return dict(passed=bool(benefit and all(all(v.values()) for v in tests.values())),noninferiority=tests,
                pooled_reduction_fractions=effects,benefit_pass=benefit)
