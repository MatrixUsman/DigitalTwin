import numpy as np
from metrics import evaluate
from mfg_twin.metrics import average_precision

def summarize(records,pools,c):
    rows=[]
    for stratum in ['pooled','P1','P2','P3']:
        eps=[e for item,e in pools if stratum=='pooled' or item['plant']==stratum]
        labels=np.concatenate([e['attack'][100:] for e in eps]).astype(int).tolist()
        scores=np.concatenate([np.where(e['unknown'],-1,e['scores'])[100:] for e in eps])
        for j,method in enumerate(c['methods7']):
            rr=[r for r in records if r['method']==method and (stratum=='pooled' or r['plant']==stratum)]
            benign=[r for r in rr if r['benign_episode']];events=[r for r in rr if r['attack_present']]
            returned=[r for r in events if r['eligible_return_event']]
            tp,fp,fn=[sum(r[k] for r in rr) for k in ['tp','fp','fn']]
            n=sum(r['eligible'] for r in benign);a=sum(r['normal_alarms'] for r in benign);ne=sum(r['normal_episodes'] for r in benign)
            delays=[r['clear_delay_from_return_seconds'] for r in returned if r['clear_delay_from_return_seconds'] is not None]
            rows.append(dict(method=method,stratum=stratum,eligible=sum(r['eligible'] for r in rr),unknown=sum(r['unknown'] for r in rr),
                tp=tp,fp=fp,fn=fn,precision=tp/(tp+fp) if tp+fp else 0.,recall=tp/(tp+fn),f1=2*tp/(2*tp+fp+fn),
                ap=average_precision(labels,scores[:,j].tolist()),benign_points=n,benign_alarms=a,benign_fraction=a/n,
                benign_episodes=ne,benign_episodes_per_hour=ne/(n*c['dt']/3600),events=len(events),
                overlap_hits=sum(r['overlap_hit'] for r in events),fresh_hits=sum(r['fresh_hit'] for r in events),
                premature_clear_events=sum(r['premature_clear'] for r in events),
                pre_return_gap_points=sum(r['gap_before_return_points'] or 0 for r in events),
                physical_return_missing=sum(r['physical_return_steps'] is None for r in events),
                returned_detected_events=len(returned),cleared_within_five_seconds=len(delays),max_clear_delay=max(delays,default=None),
                missed_events=sum(not r['overlap_hit'] for r in events)))
    by={r['method']:r for r in rows if r['stratum']=='pooled'};candidate=by['nominal_fixed_return'];tests={}
    for name in ['fused_hysteresis','mode_hysteresis']:
        b=by[name];tests[name]=dict(reduction=1-candidate['benign_alarms']/b['benign_alarms'] if b['benign_alarms'] else None,
            reduction_pass=bool(b['benign_alarms'] and candidate['benign_alarms']<=.75*b['benign_alarms']),
            episodes_pass=candidate['benign_episodes']<=b['benign_episodes'],overlap_pass=candidate['overlap_hits']>=b['overlap_hits'],
            fresh_pass=candidate['fresh_hits']>=b['fresh_hits'],early_pass=candidate['premature_clear_events']<=b['premature_clear_events'])
    recovery=bool(candidate['returned_detected_events'] and candidate['cleared_within_five_seconds']/candidate['returned_detected_events']>=.95)
    passed=recovery and all(all(v[k] for k in ['reduction_pass','episodes_pass','overlap_pass','fresh_pass','early_pass']) for v in tests.values())
    return dict(rows=rows,primary_test=dict(passed=passed,recovery_pass=recovery,comparisons=tests))
