"""Read-only arithmetic and checkpoint verification; never fits or selects a model."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, sys, time
import numpy as np

H = Path(__file__).resolve().parent
P = H.parents[1]
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def verify(method):
    import torch
    from adapter import create, predict, configuration
    from worker import check
    started = time.monotonic()
    freeze = check()
    root = P / 'local/forecast_baselines_v0.17/full_001' / method
    checks = []

    def require(name, value):
        checks.append({'check': name, 'passed': bool(value)})
        if not value:
            raise AssertionError(name)

    with np.load(P / freeze['prepared'], allow_pickle=False) as z:
        d = {k: z[k] for k in z.files}
    summary = json.loads((root / 'summary.json').read_text())
    supervisor = json.loads((root / 'supervisor.json').read_text())
    seal = json.loads((root / 'OUTPUT_SEAL.json').read_text())
    for name, digest in seal['sha256'].items():
        require('sealed output: ' + name, sha(root / name) == digest)
    require('completed once', summary['status'] == supervisor['status'] == 'completed' and supervisor['attempts'] == 1)
    provenance = json.loads((root/'provenance.json').read_text())
    access = json.loads((root/'access.json').read_text())
    require('dependency lock matches actual worker', provenance['dependencies'] == (H/'requirements-macos-arm64.txt').read_text())
    require('resolved configuration matches frozen adapter', provenance['configuration'] == configuration(method))
    require('upstream provenance matches freeze', provenance['upstream'] == freeze['upstream'][method])
    require('prepared source matches worker', provenance['prepared_sha256'] == sha(P/freeze['prepared']))
    require('normal derived access only', not access['raw_access'] and not access['final_access'] and access['file'] == freeze['prepared'])
    require('all seeds', [r['seed'] for r in summary['records']] == [17, 42, 2026])
    require('no attacks or calibration', summary['attack_metrics'] is None and summary['threshold'] is None and not summary['final_access'])
    lim = freeze['phases']['full']['limits']
    require('wall bound', supervisor['wall_seconds'] <= lim['wall_seconds'])
    require('sampled memory bound', supervisor['sampled_peak_rss_bytes'] <= lim['rss_bytes'])
    require('output bound', supervisor['output_bytes'] <= lim['output_bytes'])
    replay = []
    for r in summary['records']:
        seed = r['seed']
        require(f'{seed}: score identity', sha(root / f'seed{seed}_scores.npz') == r['scores_sha256'])
        require(f'{seed}: weight identity', sha(root / f'seed{seed}_weights.pt') == r['weights_sha256'])
        with np.load(root / f'seed{seed}_scores.npz', allow_pickle=False) as z:
            a = {k: z[k] for k in z.files}
        target = d['development'][d['development_indices']]
        require(f'{seed}: target identity', np.array_equal(a['target'], target))
        require(f'{seed}: raw-row identity', np.array_equal(a['raw_indices'], d['development_raw_indices']))
        require(f'{seed}: full coverage', a['predictions'].shape == (2048, 9) and r['targets'] == 2048)
        require(f'{seed}: finite predictions', np.isfinite(a['predictions']).all())
        error = a['predictions'] - target
        mse = np.mean(error ** 2, axis=1)
        require(f'{seed}: score arithmetic', np.array_equal(a['scores'], mse))
        require(f'{seed}: MSE arithmetic', abs(float(mse.mean()) - r['standardized_mse']) < 1e-12)
        require(f'{seed}: MAE arithmetic', abs(float(np.abs(error).mean()) - r['standardized_mae']) < 1e-12)
        require(f'{seed}: native score arithmetic', np.array_equal(a['native_scores'], np.mean((error * d['scale']) ** 2, axis=1)))
        require(f'{seed}: channel RMSE arithmetic', np.allclose(r['native_channel_rmse'], np.sqrt(np.mean((error * d['scale']) ** 2, axis=0)), rtol=0, atol=1e-12))
        history = r['history']
        require(f'{seed}: complete epoch log', history == [json.loads(line) for line in (root / f'seed{seed}_epochs.jsonl').read_text().splitlines()])
        best, selected = float('inf'), None
        for item in history:
            accepted = item['development_mse'] < best - 1e-6
            require(f'{seed}: epoch {item["epoch"]} selection', accepted == item['selected'])
            if accepted:
                best, selected = item['development_mse'], item['epoch']
        require(f'{seed}: selected checkpoint', selected == r['selected_epoch'] and abs(best - r['standardized_mse']) < 1e-12)
        require(f'{seed}: complete epoch count', len(history) == r['epochs'])
        require(f'{seed}: stopping disclosed', r['stopping_reason'] in ('declared_cpu_admission', 'normal_development_patience', 'maximum_epochs'))
        model = create(method, seed)
        state = torch.load(root / f'seed{seed}_weights.pt', map_location='cpu', weights_only=True)
        model.load_state_dict(state)
        require(f'{seed}: parameter count', sum(v.numel() for v in model.parameters()) == r['parameters'])
        prediction = predict(method, model, d['development'], d['development_indices']).astype(float)
        require(f'{seed}: exact checkpoint replay', np.array_equal(prediction, a['predictions']))
        require(f'{seed}: evaluation preserves fitted state', all(torch.equal(state[k], v) for k, v in model.state_dict().items()))
        replay.append({'seed': seed, 'exact_predictions': True, 'targets': len(prediction)})
        del model, state
    check()
    result = {'utc': datetime.now(timezone.utc).isoformat(), 'method': method, 'passed': True,
              'scope': 'Saved outputs and exact inference replay; no fitting, new selection, calibration or final access',
              'command': sys.argv, 'cwd': str(Path.cwd()), 'python': sys.executable,
              'checks': len(checks), 'details': checks, 'replay': replay,
              'wall_seconds': time.monotonic() - started,
              'source_sha256': sha(Path(__file__)), 'freeze_sha256': sha(H/'FREEZE.json'),
              'summary_sha256': sha(root/'summary.json'), 'seal_sha256': sha(root/'OUTPUT_SEAL.json')}
    destination = H / ('VERIFICATION_' + method + '.json')
    if destination.exists():
        raise FileExistsError(destination)
    destination.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['method', 'passed', 'checks', 'wall_seconds']}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--method', required=True, choices=['ModernTCN', 'iTransformer', 'TimeMixer'])
    verify(parser.parse_args().method)
