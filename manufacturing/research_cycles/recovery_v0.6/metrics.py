"""Delayed-label evaluation, including every premature alarm-clear interval."""
import numpy as np
from observer import outcome

def evaluate(alarm, unknown, ep, fit, cfg):
    row = outcome(alarm, unknown, ep['attack'], ep['authorized'], ep['state'],
                  ep['reference'], fit['scale'], cfg)
    row.update(premature_clear=False, gap_before_return_points=None,
               clear_delay_from_return_seconds=None, eligible_return_event=False,
               benign_episode=not bool(ep['attack'].any()))
    pos = np.flatnonzero(ep['attack'])
    if len(pos):
        onset, end = int(pos[0]), int(pos[-1])+1
        hit = np.flatnonzero(alarm[onset:end] & ~unknown[onset:end])
        if len(hit):
            first = onset+int(hit[0]); returned = row['physical_return_steps']
            # A pre-return loss of alarm evidence counts even if the alarm relatches.
            stop = end+returned if returned is not None else min(len(alarm),end+250)
            gaps = ~alarm[first:stop] & ~unknown[first:stop]
            row['gap_before_return_points'] = int(gaps.sum())
            falls = alarm[:-1] & ~alarm[1:] & ~unknown[:-1] & ~unknown[1:]
            row['premature_clear'] = bool(np.any(falls[first:max(first,stop-1)]))
            if returned is not None:
                row['eligible_return_event'] = True
                start = end+returned
                clear = np.flatnonzero(~alarm[start:min(len(alarm),start+251)] & ~unknown[start:min(len(alarm),start+251)])
                if len(clear): row['clear_delay_from_return_seconds'] = float(clear[0]*cfg['dt'])
    return {k:(v.item() if isinstance(v,np.generic) else v) for k,v in row.items()}

def aggregate(records, cfg):
    results = []
    for stratum in ['within_range','extrapolation']:
        for method in cfg['methods']:
            rows = [r for r in records if r['stratum']==stratum and r['method']==method]
            normal = [r for r in rows if r['benign_episode']]
            events = [r for r in rows if r['attack_present']]
            tp,fp,fn = [sum(r[k] for r in rows) for k in ['tp','fp','fn']]
            benign_n = sum(r['eligible'] for r in normal)
            returned = [r for r in events if r['eligible_return_event']]
            cleared = [r for r in returned if r['clear_delay_from_return_seconds'] is not None]
            results.append(dict(stratum=stratum, method=method, episodes=len(rows),
                eligible=sum(r['eligible'] for r in rows), unknown=sum(r['unknown'] for r in rows),
                tp=tp,fp=fp,fn=fn, precision=tp/(tp+fp) if tp+fp else 0., recall=tp/(tp+fn),
                f1=2*tp/(2*tp+fp+fn), benign_points=benign_n,
                benign_alarms=sum(r['normal_alarms'] for r in normal),
                benign_alarm_fraction=sum(r['normal_alarms'] for r in normal)/benign_n,
                benign_episodes_per_hour=sum(r['normal_episodes'] for r in normal)/(benign_n*cfg['dt']/3600),
                events=len(events), overlap_hits=sum(r['overlap_hit'] for r in events),
                fresh_hits=sum(r['fresh_hit'] for r in events),
                premature_clear_events=sum(r['premature_clear'] for r in events),
                clear_during_corruption=sum(r['clear_while_corruption'] for r in events),
                pre_return_gap_points=sum(r['gap_before_return_points'] or 0 for r in events),
                returned_detected_events=len(returned), cleared_within_five_seconds=len(cleared),
                clear_delay_max=max((r['clear_delay_from_return_seconds'] for r in cleared), default=None),
                physical_return_missing=sum(r['physical_return_steps'] is None for r in events),
                misses=sum(not r['overlap_hit'] for r in events)))
    by = {r['method']:r for r in results if r['stratum']=='within_range'}
    candidate = by['envelope_fixed_return']
    comparisons = {}
    for method in ['fused_hysteresis','mode_hysteresis']:
        control = by[method]
        comparisons[method] = dict(
            benign_reduction_fraction=1-candidate['benign_alarms']/control['benign_alarms'] if control['benign_alarms'] else None,
            reduction_pass=candidate['benign_alarms'] <= .75*control['benign_alarms'] if control['benign_alarms'] else False,
            overlap_pass=candidate['overlap_hits'] >= control['overlap_hits'],
            fresh_pass=candidate['fresh_hits'] >= control['fresh_hits'],
            premature_clear_pass=candidate['premature_clear_events'] <= control['premature_clear_events'])
    recovery_pass = (candidate['returned_detected_events']>0 and
        candidate['cleared_within_five_seconds']/candidate['returned_detected_events']>=.95)
    passed = recovery_pass and all(all(v[k] for k in ['reduction_pass','overlap_pass','fresh_pass','premature_clear_pass']) for v in comparisons.values())
    return dict(rows=results, primary_test=dict(passed=passed, recovery_pass=recovery_pass, comparisons=comparisons))
