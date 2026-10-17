"""Generate descriptive tables and learning curves from saved run artifacts only."""
import os
from pathlib import Path
HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
LOCAL = PROJECT/'local/casper_convergence_v0.11'
os.environ['MPLCONFIGDIR'] = str(LOCAL/'plot_cache')
import csv
import hashlib
import io
import json
from datetime import datetime, timezone
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

RUN = LOCAL/'runs/pilot_001'
summary = json.loads((RUN/'summary.json').read_text())
old = json.loads((PROJECT/'local/casper_comparison_v0.10/runs/pilot_002/summary.json').read_text())
verification = json.loads((HERE/'VERIFICATION.json').read_text())
assert summary['status'] == 'completed' and verification['status'] == 'passed'
out = HERE/'figures'
out.mkdir(exist_ok=False)

fields = ['model', 'seed', 'previous_standardized_mse', 'standardized_mse', 'native_mse',
          'relative_mse_change_percent', 'epochs', 'selected_epoch', 'stopping_reason',
          'fit_cpu_seconds', 'score_cpu_seconds', 'control_fit_and_score_cpu_seconds']
rows = []
for r in summary['models']:
    previous = next(x for x in old['models'] if x['model'] == r['model'])
    rows.append(dict(model=r['model'], seed=r['seed'], previous_standardized_mse=previous['standardized_mse'],
        standardized_mse=r['standardized_mse'], native_mse=r['native_mse'],
        relative_mse_change_percent=100*(r['standardized_mse']/previous['standardized_mse']-1),
        epochs=r.get('epochs'), selected_epoch=r.get('selected_epoch'),
        stopping_reason=r.get('stopping_reason', 'closed_form'), fit_cpu_seconds=r.get('fit_cpu_seconds'),
        score_cpu_seconds=r.get('score_cpu_seconds'), control_fit_and_score_cpu_seconds=r.get('cpu_seconds')))
with (HERE/'all_outcomes.csv').open('w', newline='') as handle:
    writer = csv.DictWriter(handle, fieldnames=fields)
    writer.writeheader(); writer.writerows(rows)
columns = json.loads((HERE/'config.json').read_text())['columns']
with (HERE/'per_channel_errors.csv').open('w', newline='') as handle:
    writer = csv.DictWriter(handle, fieldnames=['model', 'channel', 'standardized_mse', 'native_mse'])
    writer.writeheader()
    for r in summary['models']:
        for j, channel in enumerate(columns):
            writer.writerow(dict(model=r['model'], channel=channel,
                standardized_mse=r['channel_standardized_mse'][j], native_mse=r['channel_native_mse'][j]))

fig, axes = plt.subplots(1, 2, figsize=(10, 4.4), sharey=True, layout='constrained')
colors = ['#2563a6', '#c45e19', '#187b62']
for axis, architecture, title, old_cap in zip(axes,
        ['casper_cnn', 'edge_cnn'], ['CASPER-style CNN', 'Compact Edge-style CNN'], [3, 30]):
    for seed, color in zip([17, 42, 2026], colors):
        r = next(x for x in summary['models'] if x['model'] == f'{architecture}_seed{seed}')
        axis.plot([h['epoch'] for h in r['history']], [h['development_mse'] for h in r['history']],
                  color=color, linewidth=1.5, label=f'Seed {seed}')
        axis.plot(r['selected_epoch'], r['standardized_mse'], marker='*', color=color,
                  markersize=10, markeredgewidth=.4, markeredgecolor='white', linestyle='none')
    for name, color, style in [('ar4', '#282828', '--'), ('persistence', '#8d8d8d', ':')]:
        r = next(x for x in summary['models'] if x['model'] == name)
        axis.axhline(r['standardized_mse'], color=color, linestyle=style, linewidth=1.2,
                     label='AR(4)' if name == 'ar4' else 'Persistence')
    axis.axvline(old_cap, color='#cccccc', linewidth=1, linestyle='-.', label='Prior pilot limit')
    axis.set_title(title); axis.set_xlabel('Completed epoch'); axis.set_yscale('log')
    axis.grid(True, alpha=.16); axis.set_axisbelow(True)
axes[0].set_ylabel('Normal-development standardized MSE')
axes[1].legend(loc='upper right', fontsize=8)
fig.suptitle('Same IMU inputs and development observations; stars mark saved checkpoints', fontsize=11)
for extension in ['png', 'svg']:
    fig.savefig(out/f'normal_learning_curves.{extension}', dpi=170)
plt.close(fig)

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
receipt = dict(utc=datetime.now(timezone.utc).isoformat(), status='generated', source_summary_sha256=sha(RUN/'summary.json'),
               predecessor_summary_sha256=sha(PROJECT/'local/casper_comparison_v0.10/runs/pilot_002/summary.json'),
               script_sha256=sha(Path(__file__)), matplotlib_version=matplotlib.__version__,
               scope='Descriptive normal-development table and learning curves; no raw data or statistical significance claims.',
               artifacts={str(p.relative_to(HERE)):sha(p) for p in [HERE/'all_outcomes.csv', HERE/'per_channel_errors.csv', *sorted(out.iterdir())]})
(HERE/'PRESENTATION.json').write_text(json.dumps(receipt, indent=2)+'\n')
print(json.dumps(receipt, indent=2))
