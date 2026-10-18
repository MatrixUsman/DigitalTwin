"""Assemble verified outcomes after the entire frozen campaign completes."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json

H = Path(__file__).resolve().parent
P = H.parents[1]
R = P / 'local/forecast_baselines_v0.17/full_001'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
campaign = json.loads((R/'CAMPAIGN.json').read_text())
assert len(campaign['outcomes']) == 3
rows, resources, identities, checks = [], [], {}, []
for kind in ['ModernTCN', 'iTransformer', 'TimeMixer']:
    verification = json.loads((H/f'VERIFICATION_{kind}.json').read_text())
    assert verification['passed']
    summary = json.loads((R/kind/'summary.json').read_text())
    supervisor = json.loads((R/kind/'supervisor.json').read_text())
    assert summary['status'] == supervisor['status'] == 'completed'
    assert summary['usage']['process_cpu_seconds'] <= 480
    rows.extend(summary['records'])
    resources.append({'method': kind, 'wall_seconds': supervisor['wall_seconds'],
        'worker_cpu_seconds': summary['usage']['process_cpu_seconds'],
        'sampled_peak_rss_bytes': supervisor['sampled_peak_rss_bytes'],
        'worker_peak_rss_bytes': summary['usage']['peak_rss_bytes'],
        'monitored_output_bytes': supervisor['output_bytes']})
    checks.extend(verification['details'])
    for path in [H/f'VERIFICATION_{kind}.json',R/kind/'summary.json',R/kind/'supervisor.json',R/kind/'OUTPUT_SEAL.json']:
        identities[str(path.relative_to(P))] = sha(path)
assert len(rows) == 9 and all(r['targets'] == 2048 for r in rows)
totals = {'campaign_wall_seconds': campaign['wall_seconds'],
    'worker_cpu_seconds': sum(r['worker_cpu_seconds'] for r in resources),
    'sampled_peak_rss_bytes': max(r['sampled_peak_rss_bytes'] for r in resources),
    'monitored_output_bytes': sum(r['monitored_output_bytes'] for r in resources)}
assert totals['campaign_wall_seconds'] <= 1800 and totals['worker_cpu_seconds'] <= 1440
assert totals['sampled_peak_rss_bytes'] <= 1073741824 and totals['monitored_output_bytes'] <= 157286400
result = {'utc': datetime.now(timezone.utc).isoformat(), 'passed': True, 'checks': len(checks),
    'scope': 'Three author models under modified normal-development forecasting; no attack results',
    'outcomes': 9, 'failures': 0, 'rows': rows, 'resources': resources, 'totals': totals,
    'sha256': identities, 'freeze_sha256': sha(H/'FREEZE.json'),
    'campaign_sha256': sha(R/'CAMPAIGN.json'), 'report_source_sha256': sha(Path(__file__))}
(H/'VERIFICATION.json').write_text(json.dumps(result, indent=2)+'\n')
lines = ['# Recent author-code forecasting results', '',
    'Manufacturing, 18 October 2026. All nine registered outcomes completed once under the approved local budget. '
    'The three ICLR 2024 model classes are unchanged author code; the data, history, horizon, preprocessing, optimizer schedule and budget form our modified protocol. '
    'These are normal-development prediction measurements, not published-benchmark reproductions or attack-detection results.', '',
    '| Model | Seed | Completed / selected epochs | Standardized MSE | Standardized MAE | CPU seconds per seed | Stop |',
    '|---|---:|---:|---:|---:|---:|---|']
for r in rows:
    lines.append(f'| {r["method"]} | {r["seed"]} | {r["epochs"]} / {r["selected_epoch"]} | {r["standardized_mse"]:.9f} | {r["standardized_mae"]:.9f} | {r["cpu_seconds"]:.3f} | {r["stopping_reason"]} |')
lines += ['', 'Each outcome covers the identical 2,048 development targets. All seeds are shown. '
    'The checkpoint rule uses normal development and the observations were already exposed in the prior study. '
    'These measurements therefore characterize the bounded development procedure, not an independent generalization estimate. '
    'Different histories and budgets in the earlier independent CNN study remain disclosed. '
    'Budget-stopped runs cannot be presented as converged; a favorable seed cannot substitute for the complete roster.', '',
    f'Total campaign wall time: {totals["campaign_wall_seconds"]:.3f} s; summed worker CPU: {totals["worker_cpu_seconds"]:.3f} s; '
    f'maximum sampled RSS: {totals["sampled_peak_rss_bytes"]/2**20:.2f} MiB; monitored outputs: {totals["monitored_output_bytes"]/2**20:.2f} MiB. '
    'Memory is sampled, not an instantaneous ceiling. No paid compute was used.', '',
    f'Three synthetic model tests, 33 pilot arithmetic/seal checks and {len(checks)} full-study saved-artifact/checkpoint checks passed. '
    'All nine checkpoints exactly reproduce their saved predictions and retain their fitted state during evaluation. '
    'No final attacks, calibration thresholds or voraus-AD process signals were accessed.', '',
    '## Reproducibility', '',
    'Commands from `/Users/matrixusman/CUI/DigitalTwin/manufacturing`:', '', '```sh',
    '.venv-forecast-v016/bin/python research_cycles/forecast_baselines_v0.17/run.py --phase full',
    '.venv-forecast-v016/bin/python research_cycles/forecast_baselines_v0.17/verify.py --method ModernTCN',
    '.venv-forecast-v016/bin/python research_cycles/forecast_baselines_v0.17/verify.py --method iTransformer',
    '.venv-forecast-v016/bin/python research_cycles/forecast_baselines_v0.17/verify.py --method TimeMixer',
    '.venv-forecast-v016/bin/python research_cycles/forecast_baselines_v0.17/report.py', '```', '',
    'The training command is consumed and intentionally refuses to overwrite its run directory. '
    'Do not rerun it automatically. Verification performs inference only. `FREEZE.json`, `RUN_AUTHORIZATION.json`, '
    '`HARDWARE.json`, dependency lock, per-method provenance/access logs and output seals retain the full correspondence. '
    'The separate package manifest binds the resulting report. Original licenses remain in the ignored vendor checkouts.', '',
    '## Scientific consequence', '',
    'These executions resolve whether the three recent forecasting model classes can run on the common IMU task within a measured budget. '
    'They do not provide the protected command input or physical-return labels needed for the ARX–RBF simulation track. '
    'The prior failed attack-improvement criterion remains unchanged. MVT-Flow and full published robotic detector reproductions remain separate work.', '']
(H/'RESULTS.md').write_text('\n'.join(lines))
print(json.dumps({'outcomes':len(rows),'checks':len(checks),'totals':totals}))
