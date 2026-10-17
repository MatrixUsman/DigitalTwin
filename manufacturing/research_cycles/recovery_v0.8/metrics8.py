import numpy as np
from metrics import evaluate
from mfg_twin.metrics import average_precision

def summarize(records,pools,c):
    rows=[]
    groups=['pooled']+[p['id'] for p in c['plants8']]+[t['id'] for t in c['tasks8']]
    for group in groups:
        sub=[(item,e) for item,e in pools if group=='pooled' or group in [item['plant'],item['task']]]
        labels=np.concatenate([e['attack'][c['warmup']:] for _,e in sub]).astype(int).tolist()
        for j,method in enumerate(c['methods8']):
            rr=[r for r in records if r['method']==method and (group=='pooled' or group in [r['plant'],r['task']])]
            benign=[r for r in rr if r['benign_episode']];events=[r for r in rr if r['attack_present']]
            tp,fp,fn=[sum(r[k] for r in rr) for k in ['tp','fp','fn']]
            n=sum(r['eligible'] for r in benign);a=sum(r['normal_alarms'] for r in benign)
            returned=[r for r in events if r['eligible_return_event']]
            delays=[r['clear_delay_from_return_seconds'] for r in returned if r['clear_delay_from_return_seconds'] is not None]
            scores=np.concatenate([np.where(e['unknown'][:,j],-1,e['scores'][:,j])[c['warmup']:] for _,e in sub])
            rows.append(dict(method=method,stratum=group,eligible=sum(r['eligible'] for r in rr),unknown=sum(r['unknown'] for r in rr),
                tp=tp,fp=fp,fn=fn,precision=tp/(tp+fp) if tp+fp else 0.,recall=tp/(tp+fn) if tp+fn else 0.,
                f1=2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 0.,ap=average_precision(labels,scores.tolist()),benign_points=n,benign_alarms=a,
                benign_fraction=a/n,benign_episodes_per_hour=sum(r['normal_episodes'] for r in benign)/(n*c['dt']/3600),
                events=len(events),overlap_hits=sum(r['overlap_hit'] for r in events),fresh_hits=sum(r['fresh_hit'] for r in events),
                misses=sum(not r['overlap_hit'] for r in events),premature_clear_events=sum(r['premature_clear'] for r in events),
                gap_points=sum(r['gap_before_return_points'] or 0 for r in events),returned_detected=len(returned),cleared=len(delays),
                max_clear_delay=max(delays,default=None),physical_return_missing=sum(r['physical_return_steps'] is None for r in events)))
    by={r['method']:r for r in rows if r['stratum']=='pooled'};a=by['learned_uncertainty_return'];b=by['nominal_fixed_return'];h=by['learned_hysteresis']
    tests=dict(benign_reduction=bool(b['benign_alarms']>0 and a['benign_alarms']<=.75*b['benign_alarms']),
        misses=a['misses']<=b['misses'],premature=a['premature_clear_events']<=b['premature_clear_events'],
        timely_return=bool(a['returned_detected'] and a['cleared']/a['returned_detected']>=.95),
        commissioning_control_cost=a['benign_alarms']<=1.1*h['benign_alarms'])
    return dict(rows=rows,primary=dict(passed=all(tests.values()),tests=tests,benign_reduction_fraction=1-a['benign_alarms']/b['benign_alarms'] if b['benign_alarms'] else None))
