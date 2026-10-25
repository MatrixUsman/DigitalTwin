"""Regenerate concise reporting from the sealed replay, never train or simulate."""
import json
from common import HERE,OLD,PROJECT,load,sha
run=HERE/'runs/replay_002';s=json.loads((run/'summary.json').read_text());d=json.loads((run/'diagnostics.json').read_text())
rows=s['rows'];selected=['base_point','base_dual','base_dual_nodwell','rbf_point','rbf_dual','rbf_dual_nodwell']
pooled={r['method']:r for r in rows if r['group']=='pooled'}
cat=json.loads((OLD/'catalog.json').read_text());cfg=json.loads((PROJECT/'research_cycles/attack_audit_v0.14/config.json').read_text());boundary=[]
for cond in ['normal','authorized_offset','authorized_slow']:
    for method in ['base_point','rbf_point','base_dual','rbf_dual']:
        total=within=0
        for item in cat:
            if item['condition']!=cond:continue
            a=load(OLD/('score_'+item['id']+'.npz'))['alarms'][:,cfg['methods'].index(method)]
            total+=int(a[100:].sum());within+=int(a[347:397].sum()+a[653:703].sum())
        boundary.append(dict(condition=cond,method=method,alarm_points=total,
          points_first_second_after_two_scheduled_boundaries=within,eligible_window_points=2700,total_eligible_points=29700))
bd=dict(scope='post-replay exploratory descriptive diagnosis; boundary windows [347,397),[653,703); same clock windows in normal control; no method tuning',rows=boundary)
(HERE/'BOUNDARY_DIAGNOSTIC.json').write_text(json.dumps(bd,indent=2)+'\n')
report=['# Matched no-dwell replay and descriptive reporting','',
'## Material Passport','',
'19 October 2026; manufacturing; academic-research-suite experiment guidance. Executed AI-assisted replay of exposed synthetic v0.14 artifacts, not a fresh test, new simulation, training study, or human review. Original v1.6 and v0.14 remain unchanged.','',
'## Matched control result','',
'The occupancy reduction from removing dwell does not depend materially on the RBF correction. Base no-dwell yields 1,198 benign alarm points; RBF no-dwell yields 1,195: three fewer points (0.2504%). Compared with their dwell-10 forms, reductions are 83.259% and 82.958%. Both no-dwell methods overlap and freshly detect all 108 scheduled events. Their observed physical-outside-tolerance inactive counts are zero; the same is true for the simpler base point rule. This is a bounded simulator finding, not a safety guarantee. The original RBF primary criterion remains failed.','',
'All rows below have 89,100 eligible wholly benign observations (0.495 pooled hours) and 108 events. Starts/hour is an exposure-normalized descriptive rate, not an established deployment frequency.','',
'| Method | Benign points | Occupancy % | Starts/hour | Overlap / fresh | Registered gaps | Median clearance s | p95 clearance s |',
'|---|---:|---:|---:|---:|---:|---:|---:|']
for name in selected:
    r=pooled[name];report.append(f"| {name} | {r['benign_alarms']} | {100*r['benign_fraction']:.4f} | {r['benign_starts_per_hour']:.2f} | {r['hits']} / {r['fresh_hits']} | {r['gap_points']} | {r['clearance_delay_seconds']['median']:.3f} | {r['clearance_delay_seconds']['p95']:.3f} |")
report += ['',
'Base starts rise from 598 to 761 when dwell is removed; RBF starts rise from 590 to 743. Thus reduced occupancy comes with more fragmented alarms. The median benign run falls from 0.20 to 0.02 s for both references; the 95th percentile falls from 0.42 to 0.06 s. Removing dwell alone is an ablation, not a new detector contribution.','',
'## Diagnosed interaction','',
'| Method | Current score exceedances | Retained despite valid clearance evidence | Retained without clearance evidence | Total |',
'|---|---:|---:|---:|---:|']
for name in ['base_dual','base_dual_nodwell','rbf_dual','rbf_dual_nodwell']:
    rr=[r for r in d if r['method']==name];v={k:sum(r[k] for r in rr) for k in ['score_exceedances','retained_with_clearance_evidence','retained_without_clearance_evidence','alarm_points']}
    report.append('| '+name+' | '+' | '.join(str(v[k]) for k in ['score_exceedances','retained_with_clearance_evidence','retained_without_clearance_evidence','alarm_points'])+' |')
report += ['',
'The dominant occupancy component is the interaction of noisy score entries and dwell: 5,958/7,156 base alarm points (83.26%) and 5,817/7,012 RBF points (82.96%) are held while return evidence already passes. Noiseless plant-to-reference error exceeds the entry threshold at 150 base and 147 RBF benign points, whereas noisy measured scores exceed it at 853 and 835 points. Only 125 and 123 observed exceedances coincide with reference-error-only exceedances. Noise-only scores exceed those thresholds at 459 and 477 points. These sets overlap and cannot be added as causal fractions; this decomposition does not attribute all remaining points solely to noise.','',
'Legitimate offsets remain a secondary concentrated source: in the first second following onset/removal, 270/467 base raw exceedances and 286/466 RBF raw exceedances occur within only 2,700/29,700 observations. Equivalent clock windows contain 19/188 and 16/174 exceedances in unchanged operation. This boundary analysis was specified descriptively after the replay and is exploratory. A context-dependent error model is plausible to investigate, but these results do not establish it as the dominant solution. Entry calibration, noise and alarm persistence need matched controls.','',
'## Heterogeneity','',
'| Stratum | Base no-dwell benign points | RBF no-dwell benign points | Base / RBF starts per hour |',
'|---|---:|---:|---:|']
for group in ['plant','task','condition']:
    for label in sorted(set(r['stratum'] for r in rows if r['group']==group)):
        rr={r['method']:r for r in rows if r['group']==group and r['stratum']==label}
        a,b=rr['base_dual_nodwell'],rr['rbf_dual_nodwell']
        if not a['benign_points']:continue
        report.append(f"| {group}: {label} | {a['benign_alarms']} | {b['benign_alarms']} | {a['benign_starts_per_hour']:.2f} / {b['benign_starts_per_hour']:.2f} |")
report += ['',
'RBF worsens Q1 and tasks N14/O14 under the matched no-dwell policy; its pooled three-point reduction is not a uniform benefit. Every plant/task has 36 overlap and fresh detections for both no-dwell methods. Registered gaps are base two and RBF one, while physical-outside-tolerance inactive points are zero. These are different definitions; retain both.','',
'## Timing and conditional denominators','',
'| Method | Misses | Detection median / p95 s | Clearance median / p95 s | Already inactive at return | Outside-tolerance inactive points after detection |',
'|---|---:|---:|---:|---:|---:|']
fmt=lambda x:'—' if x is None else f'{x:.3f}'
for name in s['methods']:
    r=pooled[name];dd=r['detection_delay_seconds'];cd=r['clearance_delay_seconds']
    report.append(f"| {name} | {r['misses']} | {fmt(dd['median'])} / {fmt(dd['p95'])} | {fmt(cd['median'])} / {fmt(cd['p95'])} | {r['already_inactive_at_return']} | {r['outside_inactive_after_detection_points']} |")
report += ['',
'Clearance means first inactive observation at/after stable physical return within five seconds. Already inactive counts zero; consequently the literal label is **inactive by physical return + 5 s**, not evidence of retaining an alarm throughout recovery. Following point is already inactive in 105/108 returned events; persistence and mean21 have 41 and 60 misses, excluded from their conditional clearance samples. CUSUM has 108 detected returned events and 108 censored clearances within the horizon. All absent/censored outcomes and n/missing fields remain in summary.json. Physical-outside inactivity is counted across eligible episode support; its after-detection variant does not count pre-detection points. Neither replaces the original gap metric.','',
'Physical tolerance 0.1 is coordinate-specific: position scales give approximately 0.01992–0.02007 and 0.02290–0.02297 rad; velocity scales give 0.01614–0.01639 and 0.01555–0.01579 rad/s. Exact per-plant values are in summary.json. These are study tolerances, not safety limits.','',
'## Execution and validation','',
'Twelve synthetic tests passed. One initial launch failed before the worker executed because the sandbox denied /bin/ps; its zero-output receipt remains in replay_001. REPAIR_FREEZE.json preserves an unchanged scientific worker and an explicit environmental retry. replay_002 completed: 1.632672 s supervised wall, 1.295682 s worker CPU, 74.0 MiB sampled RSS, 89.16 MiB getrusage peak and approximately 6.06 MiB output. All 400 original frozen bindings remain identical. 71,523 worker parity checks passed; 112,847 fresh-process read-back checks passed, including all 3,213 original outcome records and every old alarm stream.','',
'The worker-side seal was taken before the terminal log line, so that streaming log is bound by VERIFICATION.json after completion; scientific output hashes verify unchanged. No scientific artifact or frozen source was patched. Source/environment/configuration/input provenance and every attempt are preserved.','',
'## Reproduction and output schema','',
'From manufacturing/, the original consumed execution command was `.venv-reproduction-v02/bin/python research_cycles/review_extension_v0.18/run.py`; the recorded environmental continuation was `.../resume.py`. Do not rerun either into the same attempt. `test_replay.py` needs only synthetic fixtures; `present.py` regenerates this report from local saved artifacts. `verify.py` writes a non-overwriting verification receipt. A reviewer replay in a fresh destination can use `worker.py --output PATH` through the same supervisor/limits after preserving input identities.','',
'- `runs/replay_002/outcomes.json`: 3,402 episode-method rows; original metric fields unchanged plus alarm-run lengths, physical outside inactivity and conditional-censor fields.\n- `runs/replay_002/summary.json`: 18 methods, pooled/plant/task/condition/plant-condition strata; delay distributions include n/missing/median/p90/p95/max.\n- `runs/replay_002/diagnostics.json`: benign score/retention/reference-error decomposition.\n- `runs/replay_002/matched_alarms.npz`: all 189 new base no-dwell alarm streams with ordered episode IDs.\n- `REPORTING.json`: manuscript-facing summaries, source identities and explicit exploratory scope.\n- `FREEZE.json`, `REPAIR_FREEZE.json`, `VERIFICATION.json`: immutable inputs, preserved failure repair and completed outputs.','',
'No fresh evaluation was consumed. Further mechanism development remains exploratory and requires a prospectively frozen new condition set for confirmation. This replay establishes a missing ablation and reporting detail, not originality or journal readiness.']
(HERE/'RESULTS.md').write_text('\n'.join(report)+'\n')
reporting=dict(scope='exploratory exposed-synthetic replay',pooled=[pooled[m] for m in s['methods']],strata=[r for r in rows if r['group'] in ['plant','task','condition']],
 native_tolerance=s['native_tolerance'],diagnostics=d,boundary_diagnostic=bd,
 source_sha256={str(p.relative_to(PROJECT)):sha(p) for p in [run/'summary.json',run/'outcomes.json',run/'diagnostics.json',HERE/'present.py']})
(HERE/'REPORTING.json').write_text(json.dumps(reporting,indent=2,sort_keys=True)+'\n')
print('Wrote RESULTS.md, REPORTING.json, BOUNDARY_DIAGNOSTIC.json')
