"""Additional descriptive reporting of a completed, exposed final campaign."""
import json,csv
from io19 import *
from mechanism19 import METHODS
out=LOCAL/'final_001';result=json.loads((out/'results.json').read_text());rows=json.loads((out/'outcomes.json').read_text())
summary=result['summary'];pooled=[r for r in summary if r['group']=='pooled']
model=json.loads((LOCAL/'development_001/selected.json').read_text());catalog=json.loads((out/'catalog.json').read_text())
scales={k:v['base']['scale'] for k,v in bases().items()};diagnostics=[]
for item in catalog:
    z=load_npz(out/('score_'+item['id']+'.npz'));t=load_npz(out/('truth_'+item['id']+'.npz'))
    distance=np.max(np.abs((t['state']-t['counterfactual'])/scales[item['parent']]),axis=1)
    mask=np.arange(len(distance))>=100;inside=z['upper']<=.1;outside=z['lower']>.1
    diagnostics.append(dict(**item,eligible=int(mask.sum()),context_extrapolation=int(z['context_extrapolation'][mask].sum()),
        unresolved=int((~inside&~outside&mask).sum()),inside_evidence=int((inside&mask).sum()),
        inside_evidence_while_physical_outside=int((inside&(distance>.1)&mask).sum()),
        outside_evidence=int((outside&mask).sum()),outside_evidence_while_physical_inside=int((outside&(distance<=.1)&mask).sum())))
for r in summary:
    events=[x for x in rows if x['event'] and x['method']==r['method'] and (r['group']=='pooled' or x[r['group']]==r['value'])]
    r['detection_missing']=sum(x['detection_delay'] is None for x in events)
    r['fresh_delay_missing']=sum(x['fresh_delay'] is None for x in events)
    r['clearance_censored']=sum(x['returned_detected'] and x['clear_delay'] is None for x in events)
    r['clearance_missing_total']=sum(x['clear_delay'] is None for x in events)
verification=json.loads((HERE/'VERIFICATION.json').read_text());supervisor=json.loads((out/'supervisor.json').read_text());completion=json.loads((out/'completion.json').read_text())
payload=dict(scope='Original prospective outcome plus explicitly additional descriptive diagnostics; no new tuning',
    primary=result['primary'],selection=model,summary=summary,diagnostics=diagnostics,
    resources=dict(supervisor=supervisor,worker_usage=completion['usage']),verification=verification,
    diagnostics_prespecified=False,original_results_sha256=sha(out/'results.json'))
write(HERE/'REPORTING.json',payload)
lines=['# Contextual recovery investigation: measured outcome','',
 '19 October 2026. Completed user-authorized bounded investigation; all conditions are synthetic. Original v0.14 and v1.6 remain unchanged. The original-contribution objective remains open.','',
 '## Selection, execution and validation','',
 'Two command-memory choices (10/40 samples) were fitted separately on each plant: K13 command context, L13 empirical allowances, M13 normal development selection. Memory40 was selected globally. Each plant has9,900 context-training and9,900 allowance-calibration observations; pooled selection uses29,700 observations. Both candidates had zero development alarm points; the stated tie rule selected the narrower average allowance. No attack label selected a setting. All source records were previously exposed synthetic development.','',
 'The single fresh campaign completed216episodes and2,376 method–episode outcomes with756,000 eligible points. There are144attack episodes and72benign episodes, totaling2.36eligible benign hours. New Lissajous/quintic paths and three perturbed plant configurations supplement their three parent configurations. No independent physical robot or real attack acquisition is claimed.','',
 f"Actual final cost: {supervisor['wall_seconds']:.3f}s wall, {completion['usage']['process_cpu_seconds']:.3f}s CPU, {supervisor['sampled_peak_rss_bytes']/1048576:.2f}MiB sampled RSS, {supervisor['output_bytes']/1048576:.2f}MiB outputs. All caps respected. Twelve synthetic tests passed; {verification['checks']} read-back checks passed, with full inference reconstruction confirming every retained reference and every score exactly. All133 final frozen bindings remain intact.",'',
 'The initial cost-admission pilot and subsequent full-storage estimate failed before final generation. A separately bound cache-aware estimate and compact lossless export admitted the unchanged scientific study. See RESOURCE_DECISION.md. Final evaluation ran once, with all scores sealed before joint scoring.','',
 '## Full roster','',
 '| Method | Benign points | Starts/h | Fresh/144 | Outside-inactive points | Joint/144 | Fresh delay p95(s) | Clearance median(s) |',
 '|---|---:|---:|---:|---:|---:|---:|---:|']
for r in pooled:
    lines.append(f"| {r['method']} | {r['benign_alarms']} | {r['starts_per_hour']:.2f} | {r['fresh']} | {r['outside_inactive']} | {r['joint']} | {r['fresh_delay']['p95']:.3f} | {r['clearance_delay']['median']:.3f} |")
lines += ['', 'All methods overlap144/144 attacks and are inactive by return+5seconds. That conditional clearance result does not imply continuous alarm support. Joint outcomes require detection, no post-onset outside-tolerance inactive point (including detection delay), and timely inactivity after sustained physical return. Unlike the original registered gap measure, inside-tolerance onset/recovery intervals do not count as physical support loss. Additional comparisons across the two metric definitions must remain explicit.','',
 '## Prospective criterion','',f"Overall passed: **{result['primary']['passed']}**. Every declared clause:",'']
for name,value in result['primary']['clauses'].items():lines.append(f'- `{name}`: {value}.')
lines += ['', 'The candidate reduces benign points99.21% and starts97.19% against original base dual, but violates its delay and outside-support constraints; joint success falls144→62. Therefore the composite improvement criterion fails. This does not retroactively change the original RBF failure.','',
 'Against matched contextual hysteresis, outside-inactive points fall1,016→679 and joint outcomes rise12→62. Benign points increase201→332; starts decrease105→94. Fresh delay is identical because entry is identical. The stricter recovery evidence accounts for a measured continuity/occupancy tradeoff; it is built from established interval inversion and hysteresis. The global-envelope control has305benign points,108starts,767outside-inactive points and62joint outcomes, so context conditioning is not uniformly superior.','',
 'Physical-tolerance point and3-of-5 controls demonstrate competing costs. Following point is fast but loses support during substantial physical deviation. None of these measurements licenses the claim that an original detector or superiority over a complete published robotic-security system has been established.','',
 '## Scope and remaining scientific work','',
 'The lower/upper evidence uses empirical99th-percentile residual allowances, not certified bounds. Top-bin extrapolation is recorded. REPORTING.json includes additional post-evaluation descriptive diagnostics of inside/outside evidence versus evaluator truth; these did not select models or alter the primary criterion. Plant/task/intervention strata and explicit missing/censored delay counts are included. Distribution percentiles describe the finite grid; adjacent samples and seeds are not independent robots.','',
 'Closest prior art establishes input-dependent thresholds, contextual motion margins, set reasoning and supervised recovery. The new numerical comparison identifies a specific tradeoff but does not prove method originality. The bounded investigation has finished; another mechanism would require a genuinely distinct rationale and another fresh protocol. Do not continue searching these final outcomes for a passing variant. Compatible independent recovery evidence and full published-system reproduction remain unavailable in this study.','',
 'The full evidence is preserved for the user to decide the next original-contribution direction. This report is not a decision to replace that objective with a negative-results paper.']
(HERE/'RESULTS.md').write_text('\n'.join(lines)+'\n')
print('Saved RESULTS.md and REPORTING.json')
