"""Tables and figures generated only from the saved normal-only artifacts."""
from pathlib import Path
import os,json,hashlib,csv
HERE=Path(__file__).resolve().parent;PROJECT=HERE.parents[1];run=PROJECT/'local/commissioning_v0.9/runs/normal_002'
cache=PROJECT/'local/commissioning_v0.9/matplotlib';cache.mkdir(parents=True,exist_ok=True);os.environ['MPLCONFIGDIR']=str(cache);os.environ['XDG_CACHE_HOME']=str(cache)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
a=json.loads((run/'fresh_summary.json').read_text());old=json.loads((run/'archived_summary.json').read_text());su=json.loads((run/'summary.json').read_text());sup=json.loads((run/'supervisor.json').read_text());noise=json.loads((HERE/'NOISE_DIAGNOSTIC.json').read_text());cand=json.loads((run/'candidates.json').read_text())
output=PROJECT/'output/commissioning_v0.9';output.mkdir(parents=True,exist_ok=True)
lines=['# Normal-only reference adequacy results','',
'17 October 2026. All observations are synthetic. This study uses commissioning and normal operation only; no attack experiment or attack recovery claim. AFTER remains a proposed title.','',
'## Outcome','',
'The normal-only search selected ARX orders 8, 16 and 32 for Q1, Q2 and Q3 respectively (ridge 1e-7). All improve the matched ARX(4) normal prediction error. Q2 changes from an infeasible allowance to 108/108 normal clearing opportunities. The overall normal-admission criterion still fails: Q2 has 93.32% eligible points satisfying the inequality (required 95%); Q3 retains an allowance above the 0.1 tolerance. These are normal forced-latch diagnostics, not detected attacks or physical recovery events.','',
'## Selected references versus matched ordinary control','',
'Both references use the same 100-observation initialization, training-only scales and three commissioning episodes. The same ARX(4) coefficients match the old saved fit exactly. The allowance here uses five normal episodes, not v0.8\'s nineteen; compare the paired columns here, not different-cycle allowance numbers.','',
'| Plant | Selected order | ARX(4) allowance | Selected allowance | Allowance decrease | ARX(4) mean RMSE | Selected mean RMSE | Selected feasible normal points | Normal clearances | Admission |',
'|---|---:|---:|---:|---:|---:|---:|---:|---:|---|']
for plant in ['Q1','Q2','Q3']:
 b=next(r for r in a['rows'] if r['plant']==plant and r['role']=='baseline_arx4');s=next(r for r in a['rows'] if r['plant']==plant and r['role']=='selected_reference')
 lines.append(f"| {plant} | {int(s['model'].split('_')[1])} | {b['allowance']:.6f} | {s['allowance']:.6f} | {100*(1-s['allowance']/b['allowance']):.2f}% | {b['mean_standardized_rmse']:.6f} | {s['mean_standardized_rmse']:.6f} | {100*s['feasible_fraction']:.2f}% | {s['cleared_probes']}/{s['probes']} | {'Pass' if s['normal_admission'] else 'Fail'} |")
lines+=['','RMSE is standardized across four state channels and averaged over episodes. Every plant has 29,700 fresh eligible observations and 108 probe starts. A probe forces an active diagnostic latch and checks ten consecutive qualifying observations within five seconds. It ignores alarm entry priority and cannot establish attack sensitivity.','',
'## All roles on fresh normal conditions','',
'| Plant | Role | Model | Allowance | Worst episode q99 error | Feasible fraction | Cleared/probes |', '|---|---|---|---:|---:|---:|---:|']
for r in a['rows']:lines.append(f"| {r['plant']} | {r['role']} | {r['model']} | {r['allowance']:.6f} | {r['worst_episode_q99']:.6f} | {100*r['feasible_fraction']:.2f}% | {r['cleared_probes']}/{r['probes']} |")
lines+=['','The selected reference equals the selected ARX on every plant; those duplicated roles are not independent methods or corroboration. FIR(64), selected from nine FIR configurations per plant, is worse in this search. One-step ARX uses measured history and is not a free reference. The command-as-state control is deliberately simple.','',
'## Sensor-noise diagnostic','',
'This analysis was added after the normal results and changes no consumed choice. For a hypothetical perfect reference, use the declared independent Gaussian noise and fixed training scales. Let F be the CDF of the maximum absolute standardized sensor noise. The empirical maximum B from 5,500 allowance points has CDF F(b)^5500. A future population feasibility of at least 95% requires B <= 0.1 - F^-1(0.95).','',
'| Plant | Single-point noise q95 | Maximum allowance compatible with 95% population feasibility | Probability that noise-only calibration leaves that margin |', '|---|---:|---:|---:|']
for r in noise['records']:lines.append(f"| {r['plant']} | {r['point_discrepancy_q95']:.6f} | {r['largest_allowance_compatible_with_95pct_population_coverage']:.6f} | {r['probability_noise_only_calibration_max_leaves_95pct_population_coverage']:.6g} |")
lines+=['','For Q3 this probability is about 2.19e-9 even with a perfect reference. This is a conditional Gaussian calculation, not a measured probability across robots, a general impossibility theorem or proof about arbitrary noise. It shows why reducing model error alone is insufficient for this particular maximum-plus-discrepancy rule. Ordinary noise-aware estimation/testing is established prior art; the calculation itself is not a novel algorithm. Independent numerical implementations agree.','',
'## Execution and limitations','',f"- 63 candidate fits: 21 per plant; {su['candidate_failures']} rejected/failed candidates. Nine development episodes per plant selected models; five estimated allowances; five archived episodes checked them.",
'- 81 newly generated normal episodes, plus fifteen archived checks; six recorded roles and 576 outcomes, including duplicated selected-reference/ARX roles. No attack observations were loaded for model fitting or generation.',
'- Twenty-three pre-run synthetic tests passed after one test-exception correction. The reporting retry has one additional merge regression. Post-run verification passed 10,293 checks, including exact refitting, selection, predictions, independent clearance arithmetic and admission.',
f"- Completed run: {sup['wall_seconds']:.3f} s wall, {su['usage']['process_cpu_seconds']:.3f} s CPU, {sup['sampled_peak_rss_bytes']/2**20:.2f} MiB sampled RSS, {su['usage']['peak_rss_bytes']/2**20:.2f} MiB worker peak, {sup['output_bytes']/2**20:.2f} MiB outputs.",
'- The first attempt stopped on a duplicate reporting key after selection, before fresh generation (2.603 s wall / 2.278 s CPU). It is preserved. A separately versioned reporting fix verified byte-identical fit files and identical scientific candidate/selection records before proceeding. No scientific retry or changed configuration.',
'- Existing Q1/Q2/Q3 plants, controller, simulator and noise assumptions; dependent seeds. New command conditions are not independent physical acquisitions. Old normal data were reused with explicitly recorded roles, not relabeled unseen evidence.',
'- ARX/FIR model selection is ordinary system identification. Full recent paper-level reproductions, a distinct new mechanism and author approval remain unresolved. This study is complete as normal-only development and is not a journal-readiness decision.',
'', '[Finite plan](PLAN.md) · [prior art](PRIOR_ART.md) · [verification](VERIFICATION.json) · [noise calculation](NOISE_DIAGNOSTIC.json) · [next mechanism requirements](DECISION.md).','']
(HERE/'RESULTS.md').write_text('\n'.join(lines))
lines=['# Complete development model bank','', 'All models use training only; selection uses archived normal development indices 0–8. No fresh check is used for model selection.','', '| Plant | Model | Status | Radius | Worst development q99 | Mean development RMSE | Parameters |','|---|---|---|---:|---:|---:|---:|']
for r in cand:lines.append(f"| {r['plant']} | {r['id']} | {r['status']} | {r.get('radius',float('nan')):.6f} | {r.get('worst_development_q99',float('nan')):.6f} | {r.get('mean_development_rmse',float('nan')):.6f} | {r.get('parameter_count','n/a')} |")
(HERE/'MODEL_BANK.md').write_text('\n'.join(lines)+'\n')
fig,ax=plt.subplots(1,2,figsize=(10,4.1),layout='constrained');xs=np.arange(3);roles=['baseline_arx4','selected_reference','selected_fir'];colors=['#667085','#007f86','#c56917'];labels=['ARX(4) control','Selected ARX','Selected FIR']
for i,(role,color,label) in enumerate(zip(roles,colors,labels)):
 rr=[next(r for r in a['rows'] if r['plant']==plant and r['role']==role) for plant in ['Q1','Q2','Q3']]
 ax[0].bar(xs+(i-1)*.24,[r['allowance'] for r in rr],.22,label=label,color=color)
 ax[1].bar(xs+(i-1)*.24,[100*r['feasible_fraction'] for r in rr],.22,color=color)
ax[0].axhline(.1,color='#b42318',ls='--',lw=1.3,label='Return tolerance (0.1)');ax[1].axhline(95,color='#b42318',ls='--',lw=1.3,label='95% normal requirement');ax[1].legend(loc='upper right',fontsize=8,frameon=True)
for a0 in ax:a0.set_xticks(xs,['Q1','Q2','Q3']);a0.spines[['top','right']].set_visible(False);a0.set_axisbelow(True);a0.grid(axis='y',alpha=.15)
ax[0].set_ylabel('Empirical normal discrepancy allowance');ax[1].set_ylabel('Fresh normal points satisfying clearance (%)');ax[1].set_ylim(0,107);ax[0].legend(fontsize=8,frameon=False);fig.suptitle('Normal-only reference adequacy | synthetic robot motion',fontsize=12)
for ext in ['png','svg']:fig.savefig(output/f'normal_reference_adequacy.{ext}',dpi=180)
plt.close(fig)
receipt=dict(source_sha256={str(p.relative_to(PROJECT)):sha(p) for p in [run/'fresh_summary.json',run/'archived_summary.json',run/'summary.json',run/'supervisor.json',run/'candidates.json',HERE/'NOISE_DIAGNOSTIC.json']},outputs={str(p.relative_to(PROJECT)):sha(p) for p in list(output.glob('*'))+[HERE/'RESULTS.md',HERE/'MODEL_BANK.md']},generator_sha256=sha(__file__))
(HERE/'PRESENTATION.json').write_text(json.dumps(receipt,indent=2)+'\n');print('Saved all-method report, complete 63-model bank and normal-feasibility figure.')
