"""Read-only independent saved-result audit; does not import the study worker.

Run from manufacturing with its existing isolated Python. This is descriptive
verification of exposed synthetic results, not another scientific experiment.
"""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import numpy as np

PROJECT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OUT = PROJECT / 'local/observer_feasibility_v0.21/normal_002'
FAMILIES = ('raw', 'mean', 'uncoupled', 'coupled', 'kf')
checks = 0


def check(value, label):
    global checks
    assert bool(value), label
    checks += 1


def close(a, b, label):
    global checks
    aa, bb = np.asarray(a), np.asarray(b)
    assert aa.shape == bb.shape, label + ': shape'
    assert np.allclose(aa, bb, rtol=2e-12, atol=2e-14), label
    checks += max(1, aa.size)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def read(p):
    return json.loads(Path(p).read_text())


def main():
    freeze = read(HERE / 'FREEZE.json')
    for p, expected in freeze['bindings'].items():
        check(sha(PROJECT / p) == expected, 'frozen identity ' + p)
    completed = read(OUT / 'completion.json')
    for p, expected in completed['artifact_sha256'].items():
        check(sha(OUT / p) == expected, 'completed identity ' + p)
    sealed = read(OUT / 'SCORES_SEALED.json')
    for p, expected in sealed['files'].items():
        check(sha(OUT / p) == expected, 'score identity ' + p)
    launch = read(OUT / 'launch.json')
    check(datetime.fromisoformat(freeze['utc']) < datetime.fromisoformat(launch['utc']), 'freeze before launch')
    check(datetime.fromisoformat(launch['utc']) < datetime.fromisoformat(sealed['utc']), 'launch before seal')
    check(launch['freeze_sha256'] == sha(HERE / 'FREEZE.json'), 'launch scientific freeze')
    selection = read(OUT / 'selection.json')
    calibration = read(OUT / 'calibration.json')
    check(selection['truth_access'] is False and selection['calibration_access'] is False, 'selection declaration')
    check(calibration['selection_sha256'] == sha(OUT / 'selection.json'), 'selection calibration identity')
    check(sealed['selection_sha256'] == sha(OUT / 'selection.json'), 'selection score identity')
    selection_access = read(OUT / 'selection_access.json')
    access = read(OUT / 'access.json')
    check(len(selection_access) == 54 and len(access) == 81, 'partition access counts')
    check(access[:54] == selection_access, 'selection access prefix')
    for record in selection_access:
        check(('normal_K13_' in record['path']) or ('normal_M13_' in record['path']), 'selection permitted partition')
        check(record['members'] == ['measurements', 'commands', 'references/base'], 'selection permitted members')
    for record in access[54:]:
        check('normal_L13_' in record['path'], 'calibration permitted partition')
    for plant, choices in selection['settings'].items():
        for family, setting in choices.items():
            candidates = [r for r in selection['losses'] if r['plant'] == plant and r['family'] == family]
            expected = min(candidates, key=lambda r: (r['development_mse'], r['setting']))['setting']
            check(expected == setting, 'finite development minimizer')

    scales = {}
    for plant in ('Q1', 'Q2', 'Q3'):
        with np.load(PROJECT / f'local/residual_twin_v0.13/runs/pilot_001/base_{plant}.npz', allow_pickle=False) as z:
            scales[plant] = z['scale'].copy()
    catalog = read(OUT / 'catalog.json')
    check(len(catalog) == 54, 'episode count')
    check(len({r['id'] for r in catalog}) == 54, 'unique episodes')
    check(len({r['noise_seed'] for r in catalog}) == 54, 'unique noise realizations')
    published_rows = {(r['id'], r['family']): r for r in read(OUT / 'outcomes.json')}
    check(len(published_rows) == 270, 'method outcome count')
    recomputed = []
    native = {}
    for episode in catalog:
        with np.load(OUT / ('scores_' + episode['id'] + '.npz'), allow_pickle=False) as data, np.load(OUT / ('truth_' + episode['id'] + '.npz'), allow_pickle=False) as truth:
            state, ref, scale = truth['state'], data['reference'], scales[episode['plant']]
            check(state.shape == ref.shape == (1500, 4), 'state/reference alignment')
            check(data['estimates'].shape == (1500, 5, 4), 'estimate alignment')
            for name in data.files:
                check(np.isfinite(data[name]).all(), 'finite saved ' + name)
            close(data['estimates'][:, 0], data['measurements'], 'raw identity')
            reference_rmse = np.sqrt(np.mean(((ref[100:] - state[100:]) / scale) ** 2))
            for j, family in enumerate(FAMILIES):
                x = data['estimates'][:, j]
                score = np.abs((x - ref) / scale).max(axis=1)
                width = calibration['widths'][episode['plant']][family]
                lower, upper = np.maximum(0, score - width), score + width
                expected_alarm = np.zeros(1500, dtype=bool)
                active = False
                for t in range(100, 1500):
                    if lower[t] > .1:
                        active = True
                    elif upper[t] <= .1:
                        active = False
                    expected_alarm[t] = active
                check(np.array_equal(expected_alarm, data['alarms'][:, j]), 'complete alarm replay')
                expected_band = (lower <= .1) & (upper > .1)
                check(np.array_equal(expected_band, data['bands'][:, j]), 'complete band replay')
                e = (x[100:] - state[100:]) / scale
                alarm = expected_alarm[100:]
                row = dict(episode, family=family, points=1400, scalar_values=5600,
                           squared_error_sum=float(np.square(e).sum()),
                           rmse=float(np.sqrt(np.square(e).mean())),
                           max_channel_abs_error=np.abs(e).max(axis=0).tolist(),
                           p99_infinity_error=float(np.quantile(np.abs(e).max(axis=1), .99)),
                           alarm_points=int(alarm.sum()),
                           starts=int(np.count_nonzero(alarm & ~np.concatenate(([False], alarm[:-1])))),
                           unknown_band_points=int(expected_band[100:].sum()),
                           width_coverage=float(np.mean(score[100:] <= width)),
                           reference_rmse=float(reference_rmse))
                published = published_rows[episode['id'], family]
                for key in row:
                    if isinstance(row[key], (int, float, list)):
                        close(row[key], published[key], 'outcome ' + key)
                    else:
                        check(row[key] == published[key], 'outcome ' + key)
                recomputed.append(row)
                key = episode['noise'], family
                sums, n = native.get(key, (np.zeros(4), 0))
                native[key] = (sums + ((x[100:] - state[100:]) ** 2).sum(axis=0), n + 1400)

    published = read(OUT / 'results.json')
    derived = {}
    for noise in ('all', 'iid', 'ar1', 'encoder'):
        for family in FAMILIES:
            rows = [r for r in recomputed if r['family'] == family and (noise == 'all' or r['noise'] == noise)]
            totals = dict(noise=noise, family=family, episodes=len(rows),
                          points=sum(r['points'] for r in rows),
                          rmse=float(np.sqrt(sum(r['squared_error_sum'] for r in rows) / sum(r['scalar_values'] for r in rows))),
                          alarm_points=sum(r['alarm_points'] for r in rows),
                          starts=sum(r['starts'] for r in rows),
                          unknown_band_points=sum(r['unknown_band_points'] for r in rows),
                          mean_width_coverage=float(np.mean([r['width_coverage'] for r in rows])),
                          max_episode_p99_infinity_error=max(r['p99_infinity_error'] for r in rows))
            expected = next(r for r in published['summary'] if r['noise'] == noise and r['family'] == family)
            for key in totals:
                if key not in ('noise', 'family'):
                    close(totals[key], expected[key], 'summary ' + key)
            derived[noise, family] = totals
    clauses = {}
    for family in ('raw', 'mean', 'uncoupled', 'kf'):
        clauses['pooled_rmse_lower_than_' + family] = derived['all', 'coupled']['rmse'] < derived['all', family]['rmse']
    for noise in ('iid', 'ar1', 'encoder'):
        for family in ('uncoupled', 'kf'):
            clauses[noise + '_rmse_not_worse_than_' + family] = derived[noise, 'coupled']['rmse'] <= derived[noise, family]['rmse']
    clauses['benign_points_not_above_raw'] = derived['all', 'coupled']['alarm_points'] <= derived['all', 'raw']['alarm_points']
    for key, value in clauses.items():
        check(value == published['admission']['clauses'][key], 'prospective clause ' + key)
    check(all(clauses.values()) == published['admission']['passed'], 'prospective combined decision')
    check(published['attack_metrics'] is None and published['novelty_established'] is False, 'scope flags')
    print(json.dumps({'status': 'passed', 'checks': checks, 'freeze_bindings': len(freeze['bindings']),
                      'episodes': len(catalog), 'outcomes': len(recomputed),
                      'admission_passed': all(clauses.values()), 'prospective_clauses': clauses,
                      'native_channel_rmse': {f'{k[0]}/{k[1]}': np.sqrt(s/n).tolist() for k, (s,n) in native.items()},
                      'no_worker_import': True, 'no_training_or_simulation': True}, indent=2))


if __name__ == '__main__':
    main()
