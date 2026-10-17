"""Post-run saved-artifact check, in a fresh process; no raw data or new CNN fit."""
import os
for key in ['TF_NUM_INTRAOP_THREADS', 'TF_NUM_INTEROP_THREADS', 'OPENBLAS_NUM_THREADS',
            'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS']:
    os.environ[key] = '1'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import json
import time
from pathlib import Path
from datetime import datetime, timezone
import numpy as np
from io_utils import sha256, verify_frozen
from model10 import restore, predict

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
RUN = PROJECT / 'local/casper_convergence_v0.11/runs/pilot_001'
OLD_RUN = PROJECT / 'local/casper_comparison_v0.10/runs/pilot_002'
checks = 0
start = time.monotonic()

def ok(condition, label):
    global checks
    if not condition:
        raise AssertionError(label)
    checks += 1

def same(actual, expected, label):
    ok(np.array_equal(actual, expected), label)

def near(actual, expected, label):
    ok(np.allclose(actual, expected, rtol=1e-12, atol=1e-12), label)

def read(name):
    with np.load(RUN / name, allow_pickle=False) as archive:
        return {key: archive[key] for key in archive.files}

def check_bindings(bindings):
    for name, expected in bindings.items():
        ok(sha256(PROJECT / name) == expected, 'preserved: ' + name)

freeze = json.loads((HERE / 'FREEZE.json').read_text())
verify_frozen(PROJECT, freeze)
check_bindings(freeze['source_sha256'])
c = freeze['configuration']
prior = json.loads((PROJECT / 'research_cycles/commissioning_v0.9/FREEZE.json').read_text())
check_bindings(prior['source_sha256'])
check_bindings(prior['input_sha256'])
packages = {}
for rel in ['research_cycles/commissioning_v0.9/PACKAGE_MANIFEST.json',
            'manuscript_after_v1.0/PACKAGE_MANIFEST.json',
            'research_cycles/casper_comparison_v0.10/PACKAGE_MANIFEST.json']:
    bindings = json.loads((PROJECT / rel).read_text())['sha256']
    check_bindings(bindings)
    packages[rel] = len(bindings)

s = json.loads((RUN / 'summary.json').read_text())
supervisor = json.loads((RUN / 'supervisor.json').read_text())
ok(s['status'] == supervisor['status'] == 'completed', 'completed worker and supervisor')
ok(s['threshold'] is None and s['attack_metrics'] is None and not s['final_access'], 'normal-only outcome')
ok(s['usage']['process_cpu_seconds'] < c['limits']['cpu_seconds'], 'CPU bound')
ok(supervisor['wall_seconds'] < c['limits']['wall_seconds'], 'wall bound')
ok(supervisor['sampled_peak_rss_bytes'] < c['limits']['rss_bytes'], 'sampled RSS bound')
ok(s['usage']['peak_rss_bytes'] < c['limits']['rss_bytes'], 'worker lifetime RSS bound')
ok(supervisor['output_bytes'] < c['limits']['output_bytes'], 'output bound')
access = json.loads((RUN / 'access.json').read_text())
ok(access['attack_files'] == [] and not access['final_access'], 'access record')
ok(access['maximum_parsed_numeric_rows'] == 12007, 'prefix limit')
authorization = json.loads((HERE/'RUN_AUTHORIZATION.json').read_text())
from authorization import check_authorization
check_authorization(authorization, sha256(HERE/'FREEZE.json'), c['limits'])
receipt = json.loads((RUN.parent.parent/'execution_authorization.json').read_text())
ok(receipt['authorization_sha256'] == sha256(HERE/'RUN_AUTHORIZATION.json'), 'recorded actual user approval unchanged')
ok(authorization['user_response'] == 'Approve the bounded local run', 'actual user response')
ok(len(list(RUN.parent.iterdir())) == 1, 'single declared execution attempt')

d = read('prepared.npz')
with np.load(OLD_RUN/'prepared.npz', allow_pickle=False) as old_prepared:
    ok(set(old_prepared.files) == set(d), 'unchanged prepared inventory')
    for key in d: same(d[key], old_prepared[key], 'unchanged prepared ' + key)
old_summary = json.loads((OLD_RUN/'summary.json').read_text())
train, dev = d['training'], d['development']
ti, di = d['training_indices'], d['development_indices']
target = dev[di].astype(np.float64)
same(ti, np.arange(755, 8947), 'training endpoints')
same(di, np.arange(755, 2803), 'development endpoints')
same(d['training_raw_indices'], np.arange(993, 9185), 'training lineage')
same(d['development_raw_indices'], np.arange(9959, 12007), 'development lineage')
ok(np.isfinite(train).all() and np.isfinite(dev).all(), 'finite prepared observations')
ok(np.all(d['scale'] > 0), 'positive scale')
ok(np.max(np.abs(train.astype(float).mean(axis=0))) < 1e-7, 'training centering')
ok(np.max(np.abs(train.astype(float).std(axis=0)-1)) < 1e-7, 'training population scale')
roster = ['mean', 'persistence', 'ar4'] + [f'{a}_seed{seed}' for a in c['architectures'] for seed in c['seeds']]
ok([r['model'] for r in s['models']] == roster, 'complete frozen roster')
weights = read('ar4_weights.npz')['coefficients']

# Independently build the AR design rather than invoke the worker's batching code.
def ar_design(values, indices):
    return np.array([np.r_[values[i-4:i].astype(float).reshape(-1), 1.] for i in indices])

xt = ar_design(train, ti)
penalty = np.eye(37) * .001
penalty[-1, -1] = 0
refitted = np.linalg.solve(xt.T @ xt / len(xt) + penalty, xt.T @ train[ti] / len(xt))
near(weights, refitted, 'independent training-only AR calculation')
xd = ar_design(dev, di)

for record in s['models']:
    name = record['model']
    saved = read(record['score_artifact'])
    ok(sha256(RUN / record['score_artifact']) == record['score_sha256'], name + ' score hash')
    ok(json.loads((RUN / (name + '_record.json')).read_text()) == record, name + ' record equality')
    if name == 'mean':
        pred = np.zeros_like(target)
    elif name == 'persistence':
        pred = dev[di-1]
    elif name == 'ar4':
        pred = xd @ weights
    else:
        ok(sha256(RUN / record['weight_artifact']) == record['weight_sha256'], name + ' weight hash')
        model = restore(record['architecture'], RUN / record['weight_artifact'])
        before = [v.copy() for v in model.get_weights()]
        pred = predict(model, dev, di, record['history_length'], 64)
        for a, b in zip(model.get_weights(), before):
            same(a, b, name + ' inference does not mutate weights')
        ok(model.count_params() == record['parameters'], name + ' parameter count')
        best, epoch, stale = float('inf'), 0, 0
        hist = record['history']
        ok(len(hist) == record['epochs'] <= c['maximum_epochs'], name + ' completed epochs')
        cumulative = 0.
        for j, h in enumerate(hist):
            ok(h['epoch'] == j+1, name + ' epoch sequence')
            accepted = h['development_mse'] < best - 1e-6
            ok(accepted == h['accepted'], name + ' acceptance rule')
            if accepted:
                best, epoch, stale = h['development_mse'], j+1, 0
            else:
                stale += 1
            if j:
                ok(cumulative + 1.25*hist[j-1]['cpu_seconds'] + 1 < c['fit_cpu_seconds_per_model'],
                   name + ' epoch CPU admission lower bound')
            cumulative += h['cpu_seconds']
        ok(record['selected_epoch'] == epoch, name + ' earliest accepted best checkpoint')
        ok(record['standardized_mse'] == best, name + ' checkpoint metric')
        if record['stopping_reason'] == 'declared_cpu_admission_budget':
            ok(record['fit_cpu_seconds'] + 1.25*hist[-1]['cpu_seconds'] + 1 >= c['fit_cpu_seconds_per_model'],
               name + ' budget stopping justified')
        elif record['stopping_reason'] == 'maximum_epochs':
            ok(len(hist) == c['maximum_epochs'], name + ' epoch cap')
        else:
            ok(stale >= 5, name + ' patience')
        old_record = next(r for r in old_summary['models'] if r['model'] == name)
        for old_h, new_h in zip(old_record['history'], hist):
            for key in ['epoch', 'training_mse', 'development_mse', 'accepted']:
                ok(old_h[key] == new_h[key], name + ' deterministic shared training trajectory ' + key)
        del model
    # CNN outputs must reproduce exactly. Independent AR BLAS grouping can differ at roundoff.
    if name == 'ar4':
        near(pred, saved['predictions'], name + ' prediction replay')
    else:
        same(pred, saved['predictions'], name + ' exact prediction replay')
    if name in ['mean', 'persistence', 'ar4']:
        with np.load(OLD_RUN/record['score_artifact'], allow_pickle=False) as old_saved:
            for key in saved: same(saved[key], old_saved[key], name + ' unchanged control artifact ' + key)
    error = saved['predictions'].astype(float) - target
    square, native = error**2, (error*d['scale'])**2
    score, native_score = np.sqrt(square.mean(axis=1)), np.sqrt(native.mean(axis=1))
    near(score, saved['scores'], name + ' RMSE')
    near(native_score, saved['native_scores'], name + ' native RMSE')
    for raw, key in [(score, 'rolling_standardized'), (native_score, 'rolling_native')]:
        independent = np.array([sum(raw[i:i+755]) for i in range(len(raw)-754)])
        near(independent, saved[key], name + ' independent rolling sum')
        ok(len(independent) == 1294, name + ' aggregate count')
    near(square.mean(), record['standardized_mse'], name + ' mean standardized error')
    near(native.mean(), record['native_mse'], name + ' mean native error')
    near(square.mean(axis=0), record['channel_standardized_mse'], name + ' channel errors')
    near(native.mean(axis=0), record['channel_native_mse'], name + ' native channel errors')
    same(saved['raw_indices'], d['development_raw_indices'], name + ' score lineage')
    same(saved['aggregate_raw_indices'], np.arange(10713, 12007), name + ' aggregate lineage')
    ok(record['eligible_observations'] == 2048, name + ' full coverage')

verify_frozen(PROJECT, freeze)
result = dict(utc=datetime.now(timezone.utc).isoformat(), status='passed', checks=checks,
              elapsed_seconds=time.monotonic()-start, verified_models=len(roster),
              prior_scientific_sources=len(prior['source_sha256']), prior_input_bindings=len(prior['input_sha256']),
              prior_packages=packages, raw_data_opened=False, attack_data_opened=False,
              cnn_refitting=False, predecessor_model_trajectories_checked=True, scope='Saved-artifact integrity and numerical consistency; not attack, physics or novelty validation.',
              freeze_sha256=sha256(HERE/'FREEZE.json'), verifier_sha256=sha256(__file__),
              summary_sha256=sha256(RUN/'summary.json'))
destination = HERE / 'VERIFICATION.json'
with destination.open('x') as handle:
    handle.write(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
