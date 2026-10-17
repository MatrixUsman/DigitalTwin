"""Post-exposure presentation from saved evidence only."""
from pathlib import Path
import json,csv,hashlib
from datetime import datetime,timezone
import numpy as np
from common import HERE,PROJECT,LOCAL,sha,write_json
RUN=LOCAL/'runs/confirmation_002'
a=json.loads((RUN/'aggregate.json').read_text());s=json.loads((RUN/'summary.json').read_text());v=json.loads((HERE/'VERIFICATION.json').read_text())
rows=[r for r in a['rows'] if r['stratum']=='pooled'];out=PROJECT/'output/recovery_v0.8';out.mkdir(parents=True,exist_ok=True)
with (out/'all_methods.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(a['rows'][0]));w.writeheader();w.writerows(a['rows'])
cal=json.loads((RUN/'calibration.json').read_text())['plants'];d=json.loads((RUN/'reference_disagreements.json').read_text())
report=['# Recovery study v0.8: measured results','',f"Frozen primary criterion: **{'passed' if a['primary']['passed'] else 'failed'}**.",'',
 '| Method | Benign alarms | F1 | Overlap / fresh | Premature clear | Cleared / returned detected |','|---|---:|---:|---:|---:|---:|']
for r in rows:report.append(f"| {r['method']} | {r['benign_alarms']}/{r['benign_points']} | {r['f1']:.4f} | {r['overlap_hits']}/{r['fresh_hits']} | {r['premature_clear_events']} | {r['cleared']}/{r['returned_detected']} |")
report+=['','## Declared criterion',json.dumps(a['primary'],indent=2),'','## Commissioning and uncertainty','']
for pid,rec in cal.items():report.append(f"- {pid}: reference spectral radius {rec['reference_radius']:.6f}; empirical allowance {rec['allowance']:.6f}; return tolerance 0.1.")
report+=['',f"Paired-plant versus nominal-model return differs in {sum(r['paired_return']!=r['nominal_return'] for r in d)}/{len(d)} intervention episodes. This is a comparison of definitions, not a retroactive change to v0.7.",
 f"The reference-error envelope covers the entire eligible counterfactual trajectory in {sum(r['reference_envelope_covered'] for r in v['truth_diagnostics'])}/216 episodes. This is measured test coverage, not a distribution-free guarantee.",'',
 '## Scope and computation',f"The completed run has {s['episodes']} synthetic episodes, {s['methods']} methods and {s['outcomes']} outcomes. {v['checks']} verification checks passed. All three noise seeds are retained; they are dependent replicates of the same physical conditions.",
 f"Worker elapsed time: {s['wall_seconds']:.3f} s. Full costs and supervisor memory/CPU/output measurements are in the saved run. The prior launch failed before the worker began because /bin/ps was blocked; the unchanged experiment then ran under scoped monitoring permission.",
 'The functional-CP row uses a separate episode-level threshold. The two matched ablations reuse the candidate entry threshold; neither is presented as an equal-calibration-budget competitor. Missing command context remains unknown for the rest of an episode. Missed events and absent fresh onsets stay in all denominators.',
 'This study does not reproduce a complete recent paper experiment. The references and comparator adaptations are described in PRIOR_ART.md. It establishes neither physical robot validation nor algorithmic novelty by itself. No outcomes may be reused as fresh confirmation for a redesigned mechanism.']
(HERE/'RESULTS.md').write_text('\n'.join(report)+'\n')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
chosen=['following_hysteresis','nominal_fixed_return','learned_hysteresis','learned_fixed_return','learned_uncertainty_return'];rr=[next(r for r in rows if r['method']==m) for m in chosen]
fig,ax=plt.subplots(1,2,figsize=(9,3.7),layout='constrained')
names=[m.replace('_',' ') for m in chosen]
ax[0].barh(names,[100*r['benign_fraction'] for r in rr]);ax[0].set_xlabel('Benign alarm observations (%)');ax[0].invert_yaxis()
ax[1].barh(names,[r['premature_clear_events'] for r in rr],color='#a96f31');ax[1].set_xlabel('Events with premature clearing');ax[1].invert_yaxis()
fig.savefig(out/'recovery_tradeoff.pdf');fig.savefig(out/'recovery_tradeoff.png',dpi=180);plt.close(fig)
manifest={str(p.relative_to(PROJECT)):sha(p) for p in [RUN/'aggregate.json',RUN/'summary.json',RUN/'calibration.json',RUN/'reference_disagreements.json',HERE/'VERIFICATION.json',HERE/'RESULTS.md',out/'all_methods.csv',out/'recovery_tradeoff.pdf',out/'recovery_tradeoff.png']}
write_json(HERE/'PRESENTATION.json',dict(utc=datetime.now(timezone.utc).isoformat(),sha256=manifest,source_sha256=sha(__file__)))
print(json.dumps({'primary':a['primary'],'allowances':{k:val['allowance'] for k,val in cal.items()},'results':str(HERE/'RESULTS.md')}))
