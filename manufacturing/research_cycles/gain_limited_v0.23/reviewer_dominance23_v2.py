"""Post-gate descriptive comparison, separate from frozen advancement criteria."""
from pathlib import Path
import hashlib
import json
import math
from datetime import datetime, timezone
import numpy as np

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
RUN = PROJECT / 'local/gain_limited_v0.23/normal_001'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
verified = json.loads((HERE / 'REVIEWER_VERIFICATION.json').read_text())
assert verified['status'] == 'passed' and verified['final_passed'] is False
methods = json.loads((RUN / 'methods.json').read_text())
selected = [m for m in methods if m['family'] == 'constrained' or m['id'] == 'saturated_fir_cap0.25']
stats = {}
bindings = {}
checks = 0
for method in selected:
    name = method['id']
    prediction_path = RUN / ('prediction_' + name + '.npz')
    bindings[str(prediction_path.relative_to(PROJECT))] = sha(prediction_path)
    with np.load(prediction_path, allow_pickle=False) as saved:
        residual = saved['residual'][:, 100:]
    scores = np.abs(residual).max(axis=2).ravel()
    e = float(max(scores))
    tau = float(sorted(scores)[math.ceil(.99 * len(scores)) - 1])
    rmse = math.sqrt(math.fsum(float(v) ** 2 for v in residual.ravel()) / residual.size)
    model_name = name if method['family'] == 'constrained' else 'unconstrained_fir'
    weights_path = RUN / ('model_' + model_name + '.npz')
    bindings[str(weights_path.relative_to(PROJECT))] = sha(weights_path)
    with np.load(weights_path, allow_pickle=False) as weights:
        if method['family'] == 'constrained':
            rho, beta, cap = [float(np.abs(weights[key].astype(np.float64)).sum(axis=1).max()) for key in ['wh', 'wz', 'wo']]
            gain = cap * beta / (1-rho)
        else:
            gain = float(np.abs(weights['weight'][:20]).sum(axis=0).max())
            cap = .25
    gain_radius = (e+tau)/(1-gain) if gain < 1 else None
    cap_radius = e+tau+2*cap
    primary = min(v for v in [gain_radius, cap_radius] if v is not None)
    for key, value in [('primary_radius', primary), ('rmse', rmse), ('Edev', e), ('tau_dev', tau)]:
        assert math.isclose(value, method['metrics'][key], rel_tol=2e-12, abs_tol=2e-12), (name, key)
        checks += 1
    stats[name] = dict(Edev=e, tau_dev=tau, rmse=rmse, K=gain, C=cap,
                       gain_radius=gain_radius, cap_radius=cap_radius, primary_radius=primary,
                       active_radius='cap' if cap_radius <= (gain_radius if gain_radius is not None else math.inf) else 'gain')
control = stats['saturated_fir_cap0.25']
comparisons = {}
for name, outcome in stats.items():
    if name == 'saturated_fir_cap0.25':
        continue
    radius_lower = control['primary_radius'] < outcome['primary_radius']
    error_lower = control['rmse'] < outcome['rmse']
    assert radius_lower and error_lower
    checks += 2
    comparisons[name] = dict(control_radius_strictly_lower=radius_lower, control_rmse_strictly_lower=error_lower,
                              control_radius_relative_reduction=1-control['primary_radius']/outcome['primary_radius'],
                              control_rmse_relative_reduction=1-control['rmse']/outcome['rmse'])
assert len(comparisons) == 6
checks += 1
receipt = dict(utc=datetime.now(timezone.utc).isoformat(), status='passed', checks=checks,
               classification='Exploratory post-gate description; not a new advancement criterion or causal attribution',
               all_six_candidates_strictly_dominated_on_both_reported_quantities=True,
               stats=stats, comparisons=comparisons, verified_gate_unchanged=True, verified_primary_gate_passed=False,
               supersedes='REVIEWER_DOMINANCE.json: ambiguous metadata field corrected; numeric findings unchanged',
               primary_audit_sha256=sha(HERE/'REVIEWER_VERIFICATION.json'), script_sha256=sha(Path(__file__)),
               output_bindings=bindings, training=False, raw_signal_array_access=False, core_imports=False)
with (HERE / 'REVIEWER_DOMINANCE_V2.json').open('x') as f:
    json.dump(receipt, f, indent=2, sort_keys=True)
    f.write('\n')
print(json.dumps(dict(status='passed', checks=checks, control=control, all_six_dominated=True,
                      receipt_sha256=sha(HERE/'REVIEWER_DOMINANCE_V2.json'))))
