"""Generate reporting tables/figure from verified saved results; no model changes."""
import json,csv,sys,os
from pathlib import Path
cache=Path(__file__).resolve().parents[2]/'local/residual_twin_v0.13/plot_cache'
cache.mkdir(parents=True,exist_ok=True)
os.environ['MPLCONFIGDIR']=str(cache)
os.environ['XDG_CACHE_HOME']=str(cache)
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io13 import HERE,RUN,sha,check

check();verification=json.loads((HERE/'VERIFICATION.json').read_text())
for name,h in verification['run_sha256'].items():
    if sha(RUN/name)!=h:raise ValueError('Changed verified artifact '+name)
s=json.loads((RUN/'summary.json').read_text());sup=json.loads((RUN/'supervisor.json').read_text())
selection=json.loads((RUN/'selection.json').read_text());candidates=json.loads((RUN/'candidates.json').read_text())
outcomes=json.loads((RUN/'outcomes.json').read_text())
lines=['# Candidate-model pilot: measured results','',
 '## Material Passport','',
 '- Project: manufacturing; operator: Codex at the user’s request.',
 '- Artifact: normal-only candidate-model experiment report, 17 October 2026.',
 '- Evidence: saved synthetic observations and fitted models; no new public dataset or attack outcomes.',
 '- Verification: deterministic prediction replay and independent arithmetic passed; this is not an independent experimental replication.',
 '', '## Main finding','',
 '**The declared all-plant improvement criterion failed.** The RBF correction gives a modest RMSE reduction on Q2 and a smaller one on Q3. Q1 RMSE is slightly worse; Q3 tail error is slightly worse. All 30 fits completed without numerical failure. This supports an implemented candidate and a comparison result, not superiority over CASPER or a validated new detector.',
 '', '## Prediction and benign alarms','',
 'Each row pools27episodes and29,700eligible observations. RMSE averages squared standardized errors across four channels. q99 is the99thpercentile of the maximum absolute standardized channel residual. Point alarms use the separately calibrated, frozen threshold for each role. Alarm-state occupancy includes persistence and must not be confused with point exceedance.', '',
 '| Plant | Reference | RMSE | q99 residual | Point alarms /29,700 | Dual-rule alarm-state points /29,700 |',
 '|---|---|---:|---:|---:|---:|']
for r in s['rows']:
    lines.append(f'| {r["plant"]} | {r["role"]} | {r["rmse"]:.8f} | {r["q99"]:.8f} | {r["point_alarms"]} | {r["gate"]["dual"]["alarm_points"]} |')
lines+=['','| Plant | RBF RMSE change vs base | RBF q99 change vs base | Declared plant check |','|---|---:|---:|---|']
for p in ['Q1','Q2','Q3']:
    d={r['role']:r for r in s['rows'] if r['plant']==p};b,n=d['base'],d['rbf']
    lines.append(f'| {p} | {100*(n["rmse"]/b["rmse"]-1):+.4f}% | {100*(n["q99"]/b["q99"]-1):+.4f}% | {"pass" if all(s["primary"][p].values()) else "fail"} |')
lines+=['','These differences are descriptive. No confidence interval or statistical-significance claim is made. The result is not rescued by reporting only Q2. The base predictor already has small measured error under these settings.',
 '', '## Model selection','',
 'Each plant:3training episodes (3,300eligible targets),9development episodes (9,900targets),5calibration episodes (5,500targets). The partitions are disjoint within this procedure but reused from earlier synthetic development. Training means/scales and coefficients do not use the calibration population. Selection uses the declared development criterion. Calibration uses ascending rank5,445 of5,500, with strict exceedance; this does not guarantee1% future alarms.',
 '', '| Plant | Selected RBF centers | Width multiplier | Ridge | Selected actual width | Linear ridge |', '|---|---:|---:|---:|---:|---:|']
for p in ['Q1','Q2','Q3']:
    rid=selection['models'][p]['rbf'];r=next(x for x in candidates if x['plant']==p and x['id']==rid)
    with np.load(RUN/f'fit_{p}_{rid}.npz',allow_pickle=False) as z:width=float(z['width'])
    lines.append(f'| {p} | {r["count"]} | {r["width_factor"]} | {r["ridge"]} | {width:.8f} | 0.01 |')
lines+=['','All candidates, per-episode development metrics and timing are in `local/residual_twin_v0.13/runs/pilot_001/candidates.json`. The selected settings are best within the declared search, not globally optimal. Every selected RBF has132output coefficients plus640center coordinates and40feature normalization values; the ARX state and parameters are additional.',
 '', '## Return-rule diagnostics','',
 '| Plant | Reference | Point evidence | Long evidence | Dual evidence | Dual evidence-availability probes |', '|---|---|---:|---:|---:|---:|']
for r in s['rows']:
    g=r['gate'];lines.append(f'| {r["plant"]} | {r["role"]} | {g["point"]["evidence_points"]} | {g["long"]["evidence_points"]} | {g["dual"]["evidence_points"]} | {g["dual"]["probe_success"]}/{g["dual"]["probes"]} |')
lines+=['','The denominator is29,700scored endpoints. Long/dual evidence can first exist at index140, excluding40additional points per episode;28,620is their maximum evidence count. Every role reaches that maximum here. Consequently these normal checks do not demonstrate a return-evidence advantage for the nonlinear model. The probe is only evidence availability; see [reporting clarifications](REPORTING_NOTES.md). No attacked recovery, premature clear or attack F1 was measured.',
 '', '## Validation and resource use','',
 f'-18synthetic software tests passed, including training-only fitting, causal prediction, save/reload, nonfinite channels and missing-context gate behavior.',
 f'-{verification["checks"]:,}saved-artifact checks passed in a fresh process, including full post-initialization measurement perturbation, all243reference outcomes and independent window/metric arithmetic.',
 f'-One supervised attempt: {sup["wall_seconds"]:.3f}s wall, {s["usage"]["process_cpu_seconds"]:.3f}s worker CPU, {sup["sampled_peak_rss_bytes"]/2**20:.2f}MiB sampled peak RSS, {sup["output_bytes"]/2**20:.2f}MiB monitored output. Limits:120s/90s/1GiB/50MiB. RSS sampling is not an instantaneous ceiling.',
 '-The sandbox denied the `/bin/ps` preflight. The scoped launcher ran with approved process-monitor access; no experiment failed or was retried. A later status read looked for `stdout.log`, but the supervisor uses `worker.log`; that failed read did not change the experiment.',
 '-All configurations, seeds, commands, dependencies, old/current source hashes, input identities, selection/score seals, logs and failures are retained. No CASPER observations, new attack slice, external upload or system-package change occurred.',
 '', '## Statistical and interpretation audit','',
 '| Check | Finding / handling |','|---|---|',
 '| Simpson reversal | Plant-level results are visible; no pooled claim substitutes for the failed all-plant criterion. Task/condition descriptive outcomes remain in outcomes.json. |',
 '| Ecological inference | No claim about other robots, tasks or individual attacks. |',
 '| Selection/Berkson bias | Finite normal synthetic settings; not a sample of industrial deployments. |',
 '| Collider bias | No post-outcome filtering; all81episodes and30fits retained. |',
 '| Base rates | All episodes are normal. Attack precision, recall and F1 are undefined here. |',
 '| Regression to mean | Paired same-observation controls reported; reused development acknowledged. |',
 '| Survivorship | Zero failed fits; all required outcomes present. |',
 '| Look-elsewhere | Full grid preserved and primary failure retained; no significance search. |',
 '| Forking paths | Scientific plan/code frozen before fitting and fresh generation; reporting clarifications explicit. |',
 '| Causal scope | Controlled software comparison only; no causal claim about real industrial security. |',
 '| Reverse causality | Training/selection/calibration precede fresh generation; no test-to-model update path. |',
 '', '11/11 categories considered using the research skill guidance. These are same-assistant checks, not external peer review. Three paired noise seeds do not constitute81independent robots or replications.',
 '', '## Decision','',
 'Keep this as a measured candidate and preserve the simple controls. Do not advance its nonlinear correction as a proven contribution or begin a confirmatory attack campaign under an improvement claim. The next model-design decision should be driven by a demonstrable failure mode and a distinguishable mechanism, with a new version and fresh evaluation conditions. The implemented reference and gate provide concrete material for the teacher’s proposed-model discussion; their existence does not settle novelty or journal readiness.',
 '', '## Reproduction commands','',
 'From `/Users/matrixusman/CUI/DigitalTwin`:', '', '```sh',
 'manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/residual_twin_v0.13/freeze.py',
 'manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/residual_twin_v0.13/run.py',
 'manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/residual_twin_v0.13/verify.py',
 'manufacturing/.venv-plots-v03/bin/python manufacturing/research_cycles/residual_twin_v0.13/present.py',
 '```', '',
 'The freeze, run and verification commands refuse to overwrite completed artifacts. Reproduction belongs in a separate authorized copy/version; do not delete the consumed run to repeat it.',
 '', '![Normal-only model comparison](normal_reference_comparison.png)']
# Normalize spacing in generated explanatory prose without touching identifiers or numbers.
replacements={'27episodes':'27 episodes','29,700eligible':'29,700 eligible','the99thpercentile':'the 99th percentile',
 '3training':'3 training','3,300eligible':'3,300 eligible','9development':'9 development','9,900targets':'9,900 targets',
 '5calibration':'5 calibration','5,500targets':'5,500 targets','rank5,445':'rank 5,445','of5,500':'of 5,500',
 'guarantee1%':'guarantee 1%','has132output':'has 132 output','plus640center':'plus 640 center','and40feature':'and 40 feature',
 '29,700scored':'29,700 scored','index140':'index 140','excluding40additional':'excluding 40 additional',
 '28,620is':'28,620 is','-18synthetic':'- 18 synthetic','saved-artifact checks':' saved-artifact checks',
 'all243reference':'all 243 reference','Limits:120s/90s/1GiB/50MiB':'Limits: 120 s / 90 s / 1 GiB / 50 MiB',
 'all81episodes':'all 81 episodes','and30fits':'and 30 fits','constitute81independent':'constitute 81 independent'}
text='\n'.join(lines)+'\n'
for a,b in replacements.items():text=text.replace(a,b)
for a,b in {'pools27':'pools 27','and29,700':'and 29,700','plant:3':'plant: 3',
            '),9':'), 9','),5':'), 5','is29,700':'is 29,700',';28,620':'; 28,620',
            '\n-4,080':'\n- 4,080','\n-One':'\n- One','\n-The':'\n- The','\n-All':'\n- All',
            '16.115s':'16.115 s','15.189s':'15.189 s','53.23MiB':'53.23 MiB','22.15MiB':'22.15 MiB'}.items():
    text=text.replace(a,b)
(HERE/'RESULTS.md').write_text(text)
with (HERE/'metrics.csv').open('w',newline='') as f:
    fields=['plant','role','episodes','eligible','rmse','q99','point_alarms'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
    w.writerows({k:r[k] for k in fields} for r in s['rows'])
fig,axes=plt.subplots(1,3,figsize=(10.5,3.8),layout='constrained')
colors=['#3f5c76','#b08036','#3b8e83'];plants=['Q1','Q2','Q3'];x=np.arange(3);width=.25
for j,role in enumerate(['base','linear','rbf']):
    rows=[next(r for r in s['rows'] if r['plant']==p and r['role']==role) for p in plants]
    for ax,key in zip(axes,['rmse','q99','point_alarms']):
        val=[r[key] if key!='point_alarms' else 100*r[key]/r['eligible'] for r in rows]
        ax.bar(x+(j-1)*width,val,width,color=colors[j],label=role)
for ax,title in zip(axes,['Standardized RMSE','99th-percentile residual','Normal point alarms (%)']):
    ax.set_xticks(x,plants);ax.set_title(title,fontsize=10);ax.set_ylim(bottom=0);ax.spines[['top','right']].set_visible(False)
axes[0].legend(frameon=False,fontsize=8);fig.suptitle('Synthetic normal-motion pilot — all reference variants',fontsize=12)
fig.savefig(HERE/'normal_reference_comparison.png',dpi=180);fig.savefig(HERE/'normal_reference_comparison.svg');plt.close(fig)
svg=HERE/'normal_reference_comparison.svg'
svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
(HERE/'PRESENTATION.json').write_text(json.dumps(dict(interpreter=sys.executable,numpy=np.__version__,matplotlib=matplotlib.__version__,
    input_sha256={n:sha(RUN/n) for n in ['summary.json','selection.json','candidates.json','supervisor.json']},
    outputs={n:sha(HERE/n) for n in ['RESULTS.md','metrics.csv','normal_reference_comparison.png','normal_reference_comparison.svg']}),indent=2)+'\n')
print('Generated RESULTS.md, metrics.csv and two figure formats from verified artifacts.')
