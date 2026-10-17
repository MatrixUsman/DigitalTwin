"""Descriptive reporting only: all declared outcomes, no model selection."""
import json
from pathlib import Path
import numpy as np
from common import HERE,PROJECT,LOCAL,sha

def main():
    run=LOCAL/'runs/reporting_001';verified=LOCAL/'verification/verify_001/verification.json'
    v=json.loads(verified.read_text())
    if v['status']!='passed':raise ValueError('Verification required')
    for p,h in v['run_sha256'].items():
        if sha(run/p)!=h:raise ValueError('Verified artifact changed')
    cfg=json.loads((HERE/'config.json').read_text());rows=json.loads((run/'outcomes.json').read_text())
    def group(records):
        tp=sum(r['tp'] for r in records);fp=sum(r['fp'] for r in records);fn=sum(r['fn'] for r in records)
        events=[r for r in records if r['attack_present']];normal=[r for r in records if not r['attack_present']]
        clean_total=sum(r['normal_points'] for r in normal);clean_alarms=sum(r['normal_alarms'] for r in normal)
        cleared=[r for r in events if r['first_clear_steps'] is not None]
        known_return=[r for r in cleared if r['physical_return_steps'] is not None]
        return dict(tp=tp,fp=fp,fn=fn,precision=tp/(tp+fp) if tp+fp else 0.,recall=tp/(tp+fn) if tp+fn else None,
            f1=2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 0.,events=len(events),overlap_hits=sum(r['overlap_hit'] for r in events),
            fresh_hits=sum(r['fresh_hit'] for r in events),eligible=sum(r['eligible'] for r in records),unknown=sum(r['unknown'] for r in records),
            clean_normal_points=clean_total,clean_normal_alarms=clean_alarms,clean_normal_fraction=clean_alarms/clean_total if clean_total else None,
            clean_normal_episodes=sum(r['normal_episodes'] for r in normal),
            clean_normal_episodes_per_hour=sum(r['normal_episodes'] for r in normal)/(clean_total*cfg['dt']/3600) if clean_total else None,
            delay_seconds=[r['delay_steps']*cfg['dt'] if r['delay_steps'] is not None else None for r in events],
            cleared_after_hit=len(cleared),detected_but_not_cleared=sum(r['overlap_hit'] and r['first_clear_steps'] is None for r in events),
            missed_events=sum(not r['overlap_hit'] for r in events),
            post_alarm_points=sum(r['post_alarm_points'] for r in events),post_points=sum(r['post_points'] for r in events),
            episodes_cleared_during_corruption=sum(r['clear_while_corruption']>0 for r in events),
            clear_transitions_during_corruption=sum(r['clear_while_corruption'] for r in events),
            first_clear_seconds=[r['first_clear_steps']*cfg['dt'] if r['first_clear_steps'] is not None else None for r in events],
            clear_before_physical_return=sum(r['first_clear_steps']<r['physical_return_steps'] for r in known_return),
            comparable_clear_and_return=len(known_return))
    result=dict(synthetic=True,scope='Two specified plants and paired noise seeds; exploratory; no confidence intervals or physical generalization',
        all_methods={name:group([r for r in rows if r['method']==name]) for name in cfg['decision_names']},
        per_condition={condition:{name:group([r for r in rows if r['method']==name and r['condition']==condition])
                       for name in cfg['decision_names']} for condition in cfg['evaluation_conditions']},
        experiment=json.loads((run/'summary.json').read_text()),supervisor=json.loads((run/'supervisor.json').read_text()),
        verification=dict(total=v['total'],passed=v['passed'],integration_max_abs_error_by_state=v['integration_max_abs_error_by_state']),
        source_outcomes_sha256=sha(run/'outcomes.json'),verification_sha256=sha(verified))
    path=HERE/'RESULTS.json'
    with path.open('x') as f:f.write(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print('| Method | Clean normal alarms | Attack-command recall | Point F1 | Event overlap / fresh | Clears during corruption | Post-command alarm points |')
    print('|---|---:|---:|---:|---:|---:|---:|')
    for name,r in result['all_methods'].items():
        print(f"| {name} | {100*r['clean_normal_fraction']:.2f}% | {100*r['recall']:.2f}% | {r['f1']:.3f} | {r['overlap_hits']}/{r['events']} ; {r['fresh_hits']}/{r['events']} | {r['episodes_cleared_during_corruption']}/{r['events']} | {r['post_alarm_points']}/{r['post_points']} |")
    print(json.dumps(dict(experiment=result['experiment'],supervisor=result['supervisor'],verification=result['verification']),indent=2))

if __name__=='__main__':main()
