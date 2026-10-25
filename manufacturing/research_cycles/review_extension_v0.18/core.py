"""Replay-only alarm logic and evaluator-only descriptive diagnostics."""
import numpy as np
from common import model,evaluation

def replay(score,residual,valid,threshold,*,dwell=1,start=100,tolerance=.1):
    known=np.logical_and.accumulate(valid);known[:start]=False
    evidence,_=model.return_evidence(residual,valid,windows=(5,41),tolerance=tolerance,start=start)
    return model.alarm_machine(score,known,evidence,threshold,dwell),evidence

def runs(alarm,start=0):
    a=np.asarray(alarm,bool)[start:]
    begins=np.flatnonzero(a&~np.r_[False,a[:-1]])
    ends=np.flatnonzero(a&~np.r_[a[1:],False])+1
    return (ends-begins).tolist()

def extra(alarm,attack,state,truth,scale,c,original):
    start=c['warmup'];dt=c['dt'];a=np.asarray(alarm,bool)
    lengths=runs(a,start);distance=np.max(np.abs((state-truth)/scale),axis=1)
    outside=distance>c['return_tolerance'];outside[:start]=False
    inactive=outside&~a
    first=None
    if original['event']:
        hits=np.flatnonzero(a[original['onset']:original['end']])
        first=original['onset']+int(hits[0]) if len(hits) else None
    mask=np.arange(len(a))>=first if first is not None else np.zeros(len(a),bool)
    ret=original['physical_return'];end=original.get('end')
    return dict(alarm_run_lengths_points=lengths,alarm_run_seconds=[v*dt for v in lengths],
      physical_outside_points=int(outside.sum()),outside_inactive_points=int(inactive.sum()),
      outside_inactive_after_detection_points=int((inactive&mask).sum()),
      outside_inactive=bool(inactive.any()),outside_inactive_after_detection=bool((inactive&mask).any()),
      alarm_falls_outside_points=int((a[:-1]&~a[1:]&outside[1:]).sum()),
      attack_alarm_starts=int((a&~np.r_[False,a[:-1]]&attack).sum()),
      physical_return_delay_seconds=(ret-end)*dt if ret is not None else None,
      clearance_censored=bool(original['returned_detected'] and original['clear_delay'] is None),
      joint_detected_continuous_outside_timely=bool(original['overlap'] and not (inactive&mask).any() and original['clear_timely']),
      clearance_label='inactive by physical return + 5 seconds; already inactive counts zero')

def dist(values):
    x=np.array([v for v in values if v is not None],dtype=float)
    return dict(n=len(x),missing=len(values)-len(x),median=float(np.median(x)) if len(x) else None,
      p90=float(np.quantile(x,.9)) if len(x) else None,p95=float(np.quantile(x,.95)) if len(x) else None,
      maximum=float(x.max()) if len(x) else None)

def summarize(rows,methods,c):
    groups=[('pooled','all',lambda r:True)]
    for field in ['plant','task','condition']:
        for value in sorted(set(r[field] for r in rows)):
            groups.append((field,value,lambda r,f=field,v=value:r[f]==v))
    for p in sorted(set(r['plant'] for r in rows)):
        for cond in sorted(set(r['condition'] for r in rows)):
            groups.append(('plant_condition',p+'/'+cond,lambda r,p=p,co=cond:r['plant']==p and r['condition']==co))
    out=[]
    for kind,label,match in groups:
        for method in methods:
            rr=[r for r in rows if r['method']==method and match(r)];bb=[r for r in rr if r['benign']];ee=[r for r in rr if r['event']]
            sums={k:sum(r[k] for r in rr) for k in ['eligible','tp','fp','fn','tn']}
            eligible=sum(r['eligible'] for r in bb);points=sum(r['alarm_points'] for r in bb);starts=sum(r['alarm_episodes'] for r in bb)
            lengths=[v for r in bb for v in r['alarm_run_seconds']];hours=eligible*c['dt']/3600
            out.append(dict(group=kind,stratum=label,method=method,episodes=len(rr),**sums,
              f1=2*sums['tp']/(2*sums['tp']+sums['fp']+sums['fn']) if 2*sums['tp']+sums['fp']+sums['fn'] else 0.,
              benign_episodes=len(bb),benign_points=eligible,benign_alarms=points,benign_fraction=points/eligible if eligible else None,
              benign_hours=hours,benign_starts=starts,benign_starts_per_hour=starts/hours if hours else None,
              benign_alarm_duration_seconds=dist(lengths),events=len(ee),hits=sum(r['overlap'] for r in ee),fresh_hits=sum(r['fresh'] for r in ee),
              misses=sum(not r['overlap'] for r in ee),fresh_misses=sum(not r['fresh'] for r in ee),
              premature=sum(r['premature'] for r in ee),gap_points=sum(r['gap_points'] or 0 for r in ee),
              outside_inactive_points=sum(r['outside_inactive_points'] for r in ee),
              outside_inactive_events=sum(r['outside_inactive'] for r in ee),
              outside_inactive_after_detection_points=sum(r['outside_inactive_after_detection_points'] for r in ee),
              outside_inactive_after_detection_events=sum(r['outside_inactive_after_detection'] for r in ee),
              physical_outside_points=sum(r['physical_outside_points'] for r in ee),
              alarm_falls_outside_points=sum(r['alarm_falls_outside_points'] for r in ee),
              attack_alarm_starts=sum(r['attack_alarm_starts'] for r in ee),
              return_missing=sum(r['return_missing'] for r in ee),returned_detected=sum(r['returned_detected'] for r in ee),
              inactive_by_return_plus_5s=sum(r['clear_timely'] for r in ee),already_inactive_at_return=sum(r['already_clear_at_return'] for r in ee),
              clearance_censored=sum(r['clearance_censored'] for r in ee),
              joint_detected_continuous_outside_timely=sum(r['joint_detected_continuous_outside_timely'] for r in ee),
              detection_delay_seconds=dist([r['detection_delay'] for r in ee]),fresh_delay_seconds=dist([r['fresh_delay'] for r in ee]),
              clearance_delay_seconds=dist([r['clear_delay'] for r in ee]),
              physical_return_delay_seconds=dist([r['physical_return_delay_seconds'] for r in ee])))
    return out
