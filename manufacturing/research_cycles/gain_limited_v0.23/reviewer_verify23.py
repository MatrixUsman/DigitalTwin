"""Independent saved-artifact audit. No training, raw-array load or core imports."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import math
import sys
import numpy as np

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
RUN = PROJECT / 'local/gain_limited_v0.23/normal_001'
checks = 0
reads = []
errors = {}


def require(condition, label):
    global checks
    checks += 1
    if not condition:
        raise AssertionError(label)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path):
    reads.append(str(path.relative_to(PROJECT)))
    return json.loads(path.read_text())


def read_arrays(path):
    reads.append(str(path.relative_to(PROJECT)))
    with np.load(path, allow_pickle=False) as saved:
        return {key: saved[key] for key in saved.files}


def near(a, b, label, atol=2e-11, rtol=2e-11):
    if a is None or b is None:
        require(a is None and b is None, label)
    else:
        require(bool(np.allclose(a, b, atol=atol, rtol=rtol)), label)


def rms(values):
    a = np.asarray(values, dtype=np.float64).ravel()
    return math.sqrt(math.fsum(float(x) * float(x) for x in a) / len(a))


def preceding(values, lag_count):
    # Separate episode axis; current and future samples cannot enter.
    n, t, channels = values.shape
    result = np.zeros((n, t, channels * lag_count), dtype=np.float64)
    for index in range(lag_count):
        lag = index + 1
        result[:, lag:, index * channels:(index + 1) * channels] = values[:, :-lag]
    return result


def command_features(commands):
    past = preceding(commands, 1)
    delta = np.zeros_like(past)
    delta[:, 1:] = past[:, 1:] - past[:, :-1]
    return np.concatenate((past, delta), axis=2)


def neural_forward(weights, residual, context):
    # Independent NumPy implementation, with the stored float32 weights.
    previous = preceding(residual, 1).astype(np.float32)
    context = context.astype(np.float32)
    state = np.zeros((len(residual), 8), dtype=np.float32)
    out = np.empty_like(residual, dtype=np.float64)
    for t in range(residual.shape[1]):
        state = np.tanh(state @ weights['wh'].T + previous[:, t] @ weights['wz'].T
                        + context[:, t] @ weights['wc'].T + weights['bias'])
        out[:, t] = state @ weights['wo'].T
    return out


def independent_l1_projection(value, radius):
    # Bisection, unlike the implementation's sorting-based projection.
    if np.abs(value).sum() <= radius:
        return value.copy()
    lo, hi = 0., float(np.abs(value).max())
    for _ in range(80):
        mid = (lo + hi) / 2
        if np.maximum(np.abs(value) - mid, 0.).sum() > radius:
            lo = mid
        else:
            hi = mid
    return np.sign(value) * np.maximum(np.abs(value) - hi, 0.)


cfg = read_json(HERE / 'config.json')
freeze = read_json(HERE / 'FREEZE.json')
release = read_json(HERE / 'REVIEW_RELEASE.json')
test = read_json(HERE / 'TEST_RECEIPT.json')
for receipt in (freeze, release, test):
    for relative, expected in receipt['bindings'].items():
        require(digest(PROJECT / relative) == expected, 'unchanged binding ' + relative)
require(release['admitted'] and test['status'] == 'passed', 'pre-run release and tests')
require(cfg['tanh']['epochs'] == 40, 'fixed 40 epochs')
seal = read_json(RUN / 'MODEL_AND_PREDICTION_SEAL.json')
for filename, expected in seal['bindings'].items():
    require(digest(RUN / filename) == expected, 'sealed output ' + filename)

contract = read_json(RUN / 'common_contract.json')
common = read_arrays(RUN / 'normalized_records.npz')
reference = read_arrays(RUN / 'common_reference.npz')
methods = read_json(RUN / 'methods.json')
by_id = {item['id']: item for item in methods}
require(len(methods) == len(by_id) == 33, '33 unique methods')
require(len(contract['fit_rows']) == len(contract['development_rows']) == 9, 'nine episodes per role')
for role, task in [('fit', 'K13'), ('development', 'M13')]:
    rows = contract[role + '_rows']
    require({(r['condition'], r['episode_seed']) for r in rows} ==
            {(c, s) for c in cfg['conditions'] for s in cfg['episode_seeds']}, 'complete ' + role + ' grid')
    require(all(r['plant'] == 'Q1' and r['task'] == task for r in rows), 'only admitted task ' + role)
    for member in ['y', 'u', 'base', 'context']:
        array = common[role + '_' + member]
        require(array.shape == (9, 1200, 8 if member == 'context' else 4), 'common shape ' + role + member)
        require(np.isfinite(array).all(), 'common finite ' + role + member)
    expected_context = command_features(common[role + '_u'])
    require(np.array_equal(expected_context, common[role + '_context']), 'causal command context ' + role)
    features = np.concatenate((preceding(common[role + '_u'], 16), np.ones((9, 1200, 1))), axis=2)
    baseline = features @ reference['reference']
    near(baseline, common[role + '_base'], 'common command-only reference ' + role)

for member in ['y', 'u']:
    fitted = common['fit_' + member][:, 100:].reshape(-1, 4)
    near(fitted.mean(axis=0), np.zeros(4), 'train-normalized zero means ' + member, atol=1e-10)
    near(fitted.std(axis=0), np.ones(4), 'train-normalized unit scales ' + member, atol=1e-10)

# Audit the common ridge normal equations without refitting any model.
x = np.concatenate((preceding(common['fit_u'], 16), np.ones((9, 1200, 1))), axis=2)[:, 100:].reshape(-1, 65)
y = common['fit_y'][:, 100:].reshape(-1, 4)
regularizer = np.eye(65) * cfg['reference']['ridge']
regularizer[-1, -1] = 0.
gradient = (x.T @ x / len(x) + regularizer) @ reference['reference'] - x.T @ y / len(x)
require(float(np.abs(gradient).max()) < 1e-10, 'reference ridge stationarity')
errors['reference_normal_equation_max_abs'] = float(np.abs(gradient).max())

zfit = common['fit_y'] - common['fit_base']
zdev = common['development_y'] - common['development_base']
predictions = {}
computed_certificates = {}
context_fit = {}
underfit = {}
history_improvement = {}

for method in methods:
    name, family = method['id'], method['family']
    saved = read_arrays(RUN / ('prediction_' + name + '.npz'))
    require(set(saved) == {'correction', 'residual'}, 'prediction fields ' + name)
    for array in saved.values():
        require(array.shape == (9, 1200, 4) and np.isfinite(array).all(), 'prediction support ' + name)
    require(np.array_equal(zdev - saved['correction'], saved['residual']), 'exact saved residual arithmetic ' + name)
    predictions[name] = saved
    if family in ('context', 'constrained', 'unconstrained'):
        weights = read_arrays(RUN / ('model_' + name + '.npz'))
        require(set(weights) == {'wh', 'wz', 'wc', 'bias', 'wo'}, 'neural weight keys ' + name)
        for key, shape in [('wh', (8, 8)), ('wz', (8, 4)), ('wc', (8, 8)), ('bias', (8,)), ('wo', (4, 8))]:
            require(weights[key].shape == shape and weights[key].dtype == np.float32 and np.isfinite(weights[key]).all(), 'weight ' + name + key)
        r, b, g = [float(np.abs(weights[key].astype(np.float64)).sum(axis=1).max()) for key in ['wh', 'wz', 'wo']]
        cert = {'rho': r, 'beta': b, 'gamma': g,
                'K': 0. if family == 'context' else (g * b / (1-r) if r < 1 else None),
                'C': 0. if family == 'context' else g}
        if family == 'context':
            require(np.count_nonzero(weights['wz']) == 0, 'context observation path zero ' + name)
        if family == 'constrained':
            k, rb = method['kappa_budget'], method['metrics']['certificate']['rho_budget']
            require(r < rb and b <= 1-rb and g <= k and cert['K'] <= k, 'complete final weight constraints ' + name)
        expected = neural_forward(weights, zdev, common['development_context'])
        max_error = float(np.abs(expected - saved['correction']).max())
        errors['numpy_forward_' + name] = max_error
        near(expected, saved['correction'], 'independent neural forward ' + name, atol=3e-6, rtol=3e-6)
        if family == 'context':
            context_fit[name] = neural_forward(weights, zfit, common['fit_context'])
        history = read_json(RUN / ('history_' + name + '.json'))
        require([h['epoch'] for h in history] == list(range(1, 41)), 'fixed complete history ' + name)
        for entry in history:
            require(np.isfinite([entry['training_window_mse'], entry['development_window_mse']]).all(), 'finite history ' + name)
            hcert = entry['certificate']
            if family == 'constrained':
                require(hcert['rho'] < rb and hcert['beta'] <= 1-rb and hcert['gamma'] <= k and hcert['K'] <= k, 'each epoch norm certificate ' + name)
        for key in cert:
            near(history[-1]['certificate'][key], cert[key], 'last epoch actual weights ' + name + key)
        gain = (history[30]['training_window_mse'] - history[39]['training_window_mse']) / max(abs(history[30]['training_window_mse']), 1e-12)
        underfit[name] = gain > .01
        history_improvement[name] = gain
        require(underfit[name] == method['extra']['underfit_flag'], 'predeclared underfit flag ' + name)
        require(method['extra']['epochs'] == 40 and method['extra']['parameter_count'] == 200, 'fixed fit metadata ' + name)
    elif family == 'direct':
        cert = {'K': 0., 'C': 0.}
        require(np.count_nonzero(saved['correction']) == 0, 'direct correction zero')
    elif family in ('fir', 'additive_fir'):
        weights = read_arrays(RUN / ('model_' + name + '.npz'))['weight']
        metadata = read_json(RUN / ('model_' + name + '.json'))
        require(weights.shape == (29, 4) and np.isfinite(weights).all(), 'linear weights ' + name)
        k = float(np.abs(weights[:20]).sum(axis=0).max())
        cert = {'K': k, 'C': None}
        near(k, metadata['K'], 'actual linear gain ' + name)
        if method['kappa_budget'] is not None:
            require(k <= method['kappa_budget'] + 1e-12, 'linear gain budget ' + name)
        if family == 'additive_fir':
            context_name = name.split('_fir_')[0]
            train_z = zfit - context_fit[context_name]
            dev_z = zdev - predictions[context_name]['correction']
            extra = predictions[context_name]['correction']
        else:
            train_z, dev_z, extra = zfit, zdev, 0.
        features = np.concatenate((preceding(dev_z, 5), common['development_context'], np.ones((9, 1200, 1))), axis=2)
        expected = features @ weights + extra
        near(expected, saved['correction'], 'independent FIR prediction ' + name, atol=2e-10)
        xx = np.concatenate((preceding(train_z, 5), common['fit_context'], np.ones((9, 1200, 1))), axis=2)[:, 100:].reshape(-1, 29)
        yy = train_z[:, 100:].reshape(-1, 4)
        gram = xx.T @ xx / len(xx) + np.diag([.001] * 28 + [0.])
        rhs = xx.T @ yy / len(xx)
        step = 1 / float(np.linalg.eigvalsh(gram)[-1])
        candidate = weights - step * (gram @ weights - rhs)
        if method['kappa_budget'] is not None:
            for j in range(4):
                candidate[:20, j] = independent_l1_projection(candidate[:20, j], method['kappa_budget'])
        gap = float(np.abs(candidate - weights).max() / step)
        errors['linear_gradient_mapping_' + name] = gap
        require(gap <= 1.5e-7, 'independent convex stationarity ' + name)
        require(metadata['converged'], 'declared solver converged ' + name)
    elif family == 'saturated_fir':
        weights = read_arrays(RUN / 'model_unconstrained_fir.npz')['weight']
        cap = method['extra']['cap']
        observed = preceding(zdev, 5) @ weights[:20]
        trusted = np.concatenate((common['development_context'], np.ones((9, 1200, 1))), axis=2) @ weights[20:]
        expected = np.clip(observed, -cap, cap) + trusted
        near(expected, saved['correction'], 'independent clipped linear prediction ' + name)
        cert = {'K': float(np.abs(weights[:20]).sum(axis=0).max()), 'C': cap}
    elif family in ('leaky', 'kalman'):
        k = method['kappa_budget'] if family == 'leaky' else 1.
        if family == 'leaky':
            retention = method['extra']['rho']
        else:
            ratio = method['extra']['ratio']
            prior = (ratio + math.sqrt(ratio * ratio + 4 * ratio)) / 2
            kalman_gain = prior / (prior + 1)
            near(kalman_gain, method['extra']['gain'], 'ordinary KF gain ' + name)
            retention = 1 - kalman_gain
        expected = np.zeros_like(zdev)
        for t in range(1, 1200):
            expected[:, t] = retention * expected[:, t-1] + (1-retention) * k * zdev[:, t-1]
        near(expected, saved['correction'], 'independent causal filter ' + name)
        cert = {'K': k, 'C': None}
    else:
        raise AssertionError('Unexpected family ' + family)
    computed_certificates[name] = cert
    for key, value in cert.items():
        near(value, method['metrics']['certificate'][key], 'actual certificate ' + name + key)

metrics = {}
for method in methods:
    name = method['id']
    residual = predictions[name]['residual'][:, 100:]
    point_scores = np.abs(residual).max(axis=2).ravel()
    rank = math.ceil(.99 * len(point_scores)) - 1
    maximum = float(max(point_scores))
    threshold = float(sorted(point_scores)[rank])
    k, cap = computed_certificates[name]['K'], computed_certificates[name]['C']
    gain_radius = (maximum + threshold) / (1-k) if k is not None and k < 1 else None
    cap_radius = maximum + threshold + 2*cap if cap is not None else None
    available = [v for v in [gain_radius, cap_radius] if v is not None]
    computed = {'points': len(point_scores), 'rank': rank, 'Edev': maximum, 'tau_dev': threshold,
                'rmse': rms(residual), 'episode_rmse': [rms(item) for item in residual],
                'gain_radius': gain_radius, 'cap_radius': cap_radius,
                'primary_radius': min(available) if available else None}
    for key, value in computed.items():
        near(value, method['metrics'][key], 'independent metric ' + name + key)
    conditions = {}
    for condition in cfg['conditions']:
        indices = [i for i, row in enumerate(contract['development_rows']) if row['condition'] == condition]
        conditions[condition] = rms(residual[indices])
        near(conditions[condition], method['condition_rmse'][condition], 'condition RMSE ' + name + condition)
    computed['conditions'] = conditions
    metrics[name] = computed

key = lambda name: (metrics[name]['primary_radius'], metrics[name]['rmse'], name)
candidate = min([m['id'] for m in methods if m['family'] == 'constrained'], key=key)
simple = min([m['id'] for m in methods if m['simple_comparator'] and metrics[m['id']]['primary_radius'] is not None], key=key)
same = min([m['id'] for m in methods if m['family'] in ['fir', 'additive_fir'] and m['kappa_budget'] == by_id[candidate]['kappa_budget']], key=key)
a, b, c = metrics[candidate], metrics[simple], metrics[same]
radius_improvement = 1 - a['primary_radius'] / b['primary_radius']
rmse_improvement = 1 - a['rmse'] / b['rmse']
linear_status = read_json(RUN / 'linear_solver_status.json')
require(len(linear_status) == 10, 'ten linear fits')
clauses = {'radius_5pct': radius_improvement >= .05, 'rmse_2pct': rmse_improvement >= .02,
           'all_episodes_within_5pct': all(x <= 1.05*y for x, y in zip(a['episode_rmse'], b['episode_rmse'])),
           'all_conditions_within_5pct': all(a['conditions'][condition] <= 1.05*b['conditions'][condition] for condition in cfg['conditions']),
           'same_budget_fir_radius_lower': a['primary_radius'] < c['primary_radius'],
           'same_budget_fir_rmse_not_higher': a['rmse'] <= c['rmse'],
           'linear_solvers_converged': all(item['converged'] for item in linear_status),
           'complete_roster': len(methods) == 33}
decision = read_json(RUN / 'admission.json')
require((candidate, simple, same) == (decision['candidate'], decision['simple_comparator'], decision['same_budget_fir']), 'independent finite selection')
require(clauses == decision['clauses'], 'all scientific clauses independently reproduced')
require(all(clauses.values()) == decision['passed'], 'scientific decision')
near(radius_improvement, decision['radius_reduction'], 'radius comparison')
near(rmse_improvement, decision['rmse_reduction'], 'RMSE comparison')
require(underfit[candidate] == decision['candidate_underfit_flag'], 'selected optimization flag')

supervisor = read_json(RUN / 'supervisor.json')
result = read_json(RUN / 'result.json')
final = read_json(RUN / 'FINAL_ADMISSION.json')
limits = cfg['limits']
output_bytes = sum(p.stat().st_size for p in RUN.rglob('*') if p.is_file())
execution = {'supervisor_completed': supervisor['status'] == 'completed',
             'wall_within_cap': supervisor['wall_seconds'] <= limits['wall_seconds'],
             'cpu_within_cap': result['usage']['process_cpu_seconds'] <= limits['cpu_seconds'],
             'sampled_rss_within_cap': supervisor['sampled_peak_rss_bytes'] <= limits['rss_bytes'],
             'outputs_within_cap': output_bytes <= limits['output_bytes'],
             'frozen_inputs_unchanged': all(digest(PROJECT / p) == h for p, h in freeze['bindings'].items()),
             'synthetic_tests_passed': test['status'] == 'passed', 'complete_methods': result['methods'] == 33}
require(execution == final['execution_clauses'], 'external execution clauses')
require(final['passed'] == (all(clauses.values()) and all(execution.values())), 'external final decision')
require(not any(final[key] for key in ['fresh_attack_admitted', 'novelty_established', 'operational_tolerance_established']), 'interpretation boundaries retained')
access = read_json(RUN / 'access.json')
require(len(access) == 18 and all(set(entry['members']) == {'measurements', 'commands', 'valid'} for entry in access), 'declared normal-only access')
require({entry['role'] for entry in access} == {'fit', 'development'}, 'no calibration/test role')

receipt = {'utc': datetime.now(timezone.utc).isoformat(), 'status': 'passed', 'checks': checks,
           'reviewer_script_sha256': digest(Path(__file__)), 'interpreter': sys.executable,
           'python': sys.version, 'numpy': np.__version__, 'core_modules_imported': False,
           'raw_signal_arrays_loaded': False, 'training_or_optimization_run': False,
           'frozen_bindings_checked': len(freeze['bindings']), 'sealed_outputs_checked': len(seal['bindings']),
           'methods': 33, 'neural_weight_sets': 9, 'linear_weight_sets': 10,
           'development_residual_values': 33*9*1200*4, 'eligible_development_rows_per_method': 9900,
           'selected': {'candidate': candidate, 'simple': simple, 'same_budget_fir': same},
           'selected_metrics': {name: metrics[name] for name in [candidate, simple, same]},
           'scientific_clauses': clauses, 'execution_clauses': execution, 'final_passed': final['passed'],
           'radius_relative_improvement': radius_improvement, 'rmse_relative_improvement': rmse_improvement,
           'underfit_flags': underfit, 'last_quarter_training_relative_improvements': history_improvement,
           'maximum_numeric_differences': errors, 'run_output_bytes_at_audit': output_bytes,
           'accessed_artifacts': sorted(set(reads)),
           'used_output_bindings': {str(p.relative_to(PROJECT)): digest(p) for p in RUN.iterdir() if p.is_file()},
           'limits': ['Saved-input and saved-weight replay, not independent acquisition',
                      'Normalization means/scales not refitted from original raw arrays',
                      'NumPy neural replay permits numerical tolerance; no floating-point proof',
                      'No inference about attacks, recovery, originality or journal readiness']}
with (HERE / 'REVIEWER_VERIFICATION.json').open('x') as stream:
    json.dump(receipt, stream, indent=2, sort_keys=True)
    stream.write('\n')
print(json.dumps({'status': 'passed', 'checks': checks, 'candidate': candidate,
                  'scientific_passed': decision['passed'], 'final_passed': final['passed'],
                  'max_neural_forward_difference': max(v for k, v in errors.items() if k.startswith('numpy_forward_')),
                  'receipt_sha256': digest(HERE / 'REVIEWER_VERIFICATION.json')}))
