"""Stdlib-only descriptive replay from saved outcomes; no training/simulation/data access."""
from pathlib import Path
import argparse, csv, hashlib, json, math

ROOT = Path(__file__).resolve().parent.parent

def quantile(values, q):
    x = sorted(values)
    if not x:
        return None
    h = (len(x) - 1) * q
    lo, hi = math.floor(h), math.ceil(h)
    return x[lo] + (x[hi] - x[lo]) * (h - lo)

def describe(values):
    finite = [x for x in values if x is not None]
    if any(not math.isfinite(x) for x in finite):
        raise ValueError('Nonfinite saved outcome')
    return {'n': len(finite), 'missing': len(values) - len(finite),
            'median': quantile(finite, .5), 'p95': quantile(finite, .95),
            'maximum': max(finite) if finite else None}

def aggregate(rows, version):
    groups = [('pooled', 'all')]
    fields = ['plant', 'task', 'condition'] + (['plant_group'] if version == 19 else [])
    groups += [(k, v) for k in fields for v in sorted({r[k] for r in rows})]
    methods = sorted({r['method'] for r in rows})
    result = []
    for group, value in groups:
        for method in methods:
            rr = [r for r in rows if r['method'] == method and (group == 'pooled' or r[group] == value)]
            benign = [r for r in rr if r['benign']]
            attack = [r for r in rr if r['event']]
            eligible = sum(r['eligible'] for r in benign)
            alarms = sum(r['alarm_points'] for r in benign)
            starts = sum(r['alarm_episodes'] for r in benign)
            durations = [v for r in benign for v in r['alarm_run_seconds' if version == 18 else 'alarm_durations_seconds']]
            tp, fp, fn = [sum(r[k] for r in rr) for k in ['tp', 'fp', 'fn']]
            result.append({'group': group, 'stratum': value, 'method': method,
                           'episodes': len(rr), 'benign_points': eligible, 'benign_alarms': alarms,
                           'occupancy': alarms / eligible if eligible else None,
                           'starts': starts, 'benign_hours': eligible * .02 / 3600,
                           'starts_per_hour': starts / (eligible * .02 / 3600) if eligible else None,
                           'benign_run_seconds': describe(durations),
                           'events': len(attack), 'hits': sum(r['overlap'] for r in attack),
                           'fresh': sum(r['fresh'] for r in attack), 'misses': sum(not r['overlap'] for r in attack),
                           'outside_inactive': sum(r['outside_inactive_points' if version == 18 else 'outside_inactive'] for r in attack),
                           'outside_points': sum(r['physical_outside_points' if version == 18 else 'outside_points'] for r in attack),
                           'joint': sum(r['joint_detected_continuous_outside_timely' if version == 18 else 'joint'] for r in attack),
                           'inactive_by_return_plus_5': sum(r['clear_timely'] for r in attack),
                           'already_inactive_at_return': sum(r['already_clear_at_return'] for r in attack),
                           'absent_return': sum(r['return_missing'] for r in attack),
                           'clearance_censored': sum(bool(r['returned_detected'] and r['clear_delay'] is None) for r in attack),
                           'detection_delay': describe([r['detection_delay'] for r in attack]),
                           'fresh_delay': describe([r['fresh_delay'] for r in attack]),
                           'clearance_delay': describe([r['clear_delay'] for r in attack]),
                           'f1': 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else 0.})
    return result

def equal(a, b):
    return a == b if a is None or b is None or isinstance(a, (str, bool)) else math.isclose(a, b, abs_tol=1e-12, rel_tol=1e-12)

def compare(ours, saved, version):
    index = {(r['group'], r['stratum' if version == 18 else 'value'], r['method']): r for r in saved}
    checks = 0
    mapping = {k: k for k in ['episodes', 'benign_points', 'benign_alarms', 'benign_hours', 'events', 'hits', 'misses', 'f1']}
    mapping.update({'occupancy': 'benign_fraction' if version == 18 else 'occupancy',
                    'starts': 'benign_starts' if version == 18 else 'starts',
                    'starts_per_hour': 'benign_starts_per_hour' if version == 18 else 'starts_per_hour',
                    'fresh': 'fresh_hits' if version == 18 else 'fresh',
                    'outside_inactive': 'outside_inactive_points' if version == 18 else 'outside_inactive',
                    'outside_points': 'physical_outside_points' if version == 18 else 'outside_points',
                    'joint': 'joint_detected_continuous_outside_timely' if version == 18 else 'joint',
                    'inactive_by_return_plus_5': 'inactive_by_return_plus_5s' if version == 18 else 'inactive_by_return_plus_5',
                    'already_inactive_at_return': 'already_inactive_at_return',
                    'absent_return': 'return_missing' if version == 18 else 'absent_return'})
    for row in ours:
        key = (row['group'], row['stratum'], row['method'])
        ref = index[key]
        for own, original in mapping.items():
            if not equal(row[own], ref[original]):
                raise AssertionError((key, own, row[own], ref[original]))
            checks += 1
        for own, original in [('detection_delay', 'detection_delay_seconds'), ('fresh_delay', 'fresh_delay_seconds'), ('clearance_delay', 'clearance_delay_seconds'), ('benign_run_seconds', 'benign_alarm_duration_seconds')]:
            original = original if version == 18 else ('alarm_duration' if own == 'benign_run_seconds' else own)
            for metric in ['n', 'median', 'p95']:
                if not equal(row[own][metric], ref[original][metric]):
                    raise AssertionError((key, own, metric))
                checks += 1
    return checks

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', required=True, type=Path, help='Fresh output directory, never a saved run')
    p.add_argument('--allow-pending-v019', action='store_true', help='Development-only partial replay before the final study exists')
    args = p.parse_args()
    if args.output.exists():
        p.error('Refusing to overwrite an existing directory')
    args.output.mkdir(parents=True)
    sources = [(18, ROOT / 'research_cycles/review_extension_v0.18/runs/replay_002')]
    final = ROOT / 'local/context_recovery_v0.19/final_001'
    if (final / 'outcomes.json').exists():
        sources.append((19, final))
    elif not args.allow_pending_v019:
        p.error('Completed v0.19 outcomes missing; no partial package success is claimed')
    receipt = {'scope': 'Saved-outcome descriptive replay, not an experiment', 'checks': 0, 'studies': [], 'inputs': {}}
    for version, run in sources:
        outcomes = run / 'outcomes.json'
        saved_path = run / ('summary.json' if version == 18 else 'results.json')
        saved = json.loads(saved_path.read_text())
        rows = aggregate(json.loads(outcomes.read_text()), version)
        checks = compare(rows, saved['rows' if version == 18 else 'summary'], version)
        receipt['checks'] += checks
        receipt['studies'].append(version)
        for q in [outcomes, saved_path]:
            receipt['inputs'][q.relative_to(ROOT).as_posix()] = hashlib.sha256(q.read_bytes()).hexdigest()
        (args.output / f'v0.{version}-tables.json').write_text(json.dumps(rows, indent=2) + '\n')
        fields = ['group', 'stratum', 'method', 'benign_points', 'benign_alarms', 'occupancy', 'starts_per_hour', 'events', 'hits', 'fresh', 'misses', 'outside_inactive', 'outside_points', 'joint', 'inactive_by_return_plus_5', 'already_inactive_at_return', 'absent_return', 'clearance_censored', 'f1']
        with (args.output / f'v0.{version}-tables.tsv').open('w', newline='') as f:
            writer = csv.DictWriter(f, fields, delimiter='\t', extrasaction='ignore')
            writer.writeheader(); writer.writerows(rows)
    receipt['status'] = 'passed'
    receipt['complete_requested_studies'] = receipt['studies'] == [18, 19]
    (args.output / 'REPLAY_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))

if __name__ == '__main__':
    main()
