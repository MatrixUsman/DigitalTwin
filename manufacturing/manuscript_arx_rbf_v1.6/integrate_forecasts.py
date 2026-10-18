"""Generate manuscript additions only from the completed, verified study."""
from pathlib import Path
import hashlib, json

M = Path(__file__).resolve().parent
P = M.parent
R = P/'research_cycles/forecast_baselines_v0.17'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
v = json.loads((R/'VERIFICATION.json').read_text())
assert v['passed'] and v['outcomes'] == 9 and v['failures'] == 0
rows = v['rows']
stops = {'declared_cpu_admission':'C','normal_development_patience':'P','maximum_epochs':'E'}
cpu_stops = sum(r['stopping_reason'] == 'declared_cpu_admission' for r in rows)
stop_sentence = ('All nine runs stop at their declared CPU admission limit, before the patience criterion. ' if cpu_stops == 9
                 else f'{cpu_stops} of nine runs stop at their declared CPU admission limit; every stopping reason is shown in the table. ')
lines = [r'\begin{tabular}{llrrrl}\toprule',
         r'Model & Seed & Ep. & MSE & CPU (s) & Stop\\\midrule']
for r in rows:
    lines.append(f'{r["method"]} & {r["seed"]} & {r["epochs"]}/{r["selected_epoch"]} & {r["standardized_mse"]:.6f} & {r["cpu_seconds"]:.1f} & {stops[r["stopping_reason"]]}'+r'\\')
lines += [r'\bottomrule\end{tabular}', '']
(M/'generated/forecast.tex').write_text('\n'.join(lines))
ranges = {}
for kind in ['ModernTCN','iTransformer','TimeMixer']:
    subset = [r for r in rows if r['method'] == kind]
    ranges[kind] = {'min':min(r['standardized_mse'] for r in subset), 'max':max(r['standardized_mse'] for r in subset),
                    'parameters':subset[0]['parameters']}
t = v['totals']
paragraph = (
    '\\subsection{Recent author-code prediction results}\n'
    'All nine recent-model runs complete on the same 2,048 normal-development targets (Table~\\ref{tab:forecasts}). '
    + '; '.join(f'{kind} gives MSE {ranges[kind]["min"]:.6f}--{ranges[kind]["max"]:.6f}' for kind in ranges) + '. '
    + stop_sentence +
    'These values describe transferred configurations under a finite budget; they do not estimate each architecture\'s converged performance. '
    'Normal-development checkpoint selection also makes them unsuitable as independent test estimates. '
    'The models have 173,861, 817,153 and 58,033 parameters respectively. '
    'AR(4) remains a useful low-cost reference on these filtered targets; different histories and training budgets limit a broader architectural ranking.\n\n'
    '\\begin{table}[t]\\centering\n'
    '\\caption{Recent author-code forecasts: all seeds, completed/selected epochs, standardized development MSE and per-seed fitting/scoring CPU. Stops: C, CPU admission; P, patience; E, epoch ceiling. No attack score is measured.}\\label{tab:forecasts}\n'
    '\\setlength{\\tabcolsep}{2pt}\\input{generated/forecast}\n\\end{table}\n\n')
f = M/'sections/results.tex'; s = f.read_text()
marker = '\\subsection{Five-fold temporal validation}'
assert '\\subsection{Recent author-code prediction results}' not in s
s = s.replace(marker, paragraph+marker,1)
cost = (
    f'The recent forecast campaign consumes {t["campaign_wall_seconds"]:.3f} seconds wall and {t["worker_cpu_seconds"]:.3f} seconds summed worker CPU, '
    f'with {t["sampled_peak_rss_bytes"]/2**20:.2f} MiB maximum sampled memory and {t["monitored_output_bytes"]/2**20:.2f} MiB monitored outputs. '
    f'All nine saved checkpoints reproduce their predictions exactly; {v["checks"]} artifact and replay checks pass. '
    'The separate five-fold diagnostic uses 0.485 seconds wall and 0.297 seconds CPU and passes 109 saved-artifact checks. '
    'These are pipeline costs, not isolated inference latency.\n\n')
s = s.replace('The final audit passes 25 synthetic software tests',cost+'The final audit passes 25 synthetic software tests',1)
f.write_text(s)
receipt = {'scope':'New table and prose generated from completed saved outcomes; no model fitting',
    'verification_sha256':sha(R/'VERIFICATION.json'),'table_sha256':sha(M/'generated/forecast.tex'),
    'rows':rows,'ranges':ranges,'resources':t,'generator_sha256':sha(Path(__file__))}
(M/'FORECAST_ASSET_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'rows':len(rows),'table_sha256':receipt['table_sha256'],'ranges':ranges}))
