# Matched no-dwell replay and descriptive reporting

## Material Passport

19 October 2026; manufacturing; academic-research-suite experiment guidance. Executed AI-assisted replay of exposed synthetic v0.14 artifacts, not a fresh test, new simulation, training study, or human review. Original v1.6 and v0.14 remain unchanged.

## Matched control result

The occupancy reduction from removing dwell does not depend materially on the RBF correction. Base no-dwell yields 1,198 benign alarm points; RBF no-dwell yields 1,195: three fewer points (0.2504%). Compared with their dwell-10 forms, reductions are 83.259% and 82.958%. Both no-dwell methods overlap and freshly detect all 108 scheduled events. Their observed physical-outside-tolerance inactive counts are zero; the same is true for the simpler base point rule. This is a bounded simulator finding, not a safety guarantee. The original RBF primary criterion remains failed.

All rows below have 89,100 eligible wholly benign observations (0.495 pooled hours) and 108 events. Starts/hour is an exposure-normalized descriptive rate, not an established deployment frequency.

| Method | Benign points | Occupancy % | Starts/hour | Overlap / fresh | Registered gaps | Median clearance s | p95 clearance s |
|---|---:|---:|---:|---:|---:|---:|---:|
| base_point | 853 | 0.9574 | 1537.37 | 108 / 108 | 38 | 0.080 | 0.780 |
| base_dual | 7156 | 8.0314 | 1208.08 | 108 / 101 | 2 | 0.920 | 1.073 |
| base_dual_nodwell | 1198 | 1.3446 | 1537.37 | 108 / 108 | 2 | 0.650 | 0.780 |
| rbf_point | 835 | 0.9371 | 1501.01 | 108 / 108 | 39 | 0.080 | 0.780 |
| rbf_dual | 7012 | 7.8698 | 1191.92 | 108 / 105 | 3 | 0.940 | 1.073 |
| rbf_dual_nodwell | 1195 | 1.3412 | 1501.01 | 108 / 108 | 1 | 0.650 | 0.780 |

Base starts rise from 598 to 761 when dwell is removed; RBF starts rise from 590 to 743. Thus reduced occupancy comes with more fragmented alarms. The median benign run falls from 0.20 to 0.02 s for both references; the 95th percentile falls from 0.42 to 0.06 s. Removing dwell alone is an ablation, not a new detector contribution.

## Diagnosed interaction

| Method | Current score exceedances | Retained despite valid clearance evidence | Retained without clearance evidence | Total |
|---|---:|---:|---:|---:|
| base_dual | 853 | 5958 | 345 | 7156 |
| base_dual_nodwell | 853 | 0 | 345 | 1198 |
| rbf_dual | 835 | 5817 | 360 | 7012 |
| rbf_dual_nodwell | 835 | 0 | 360 | 1195 |

The dominant occupancy component is the interaction of noisy score entries and dwell: 5,958/7,156 base alarm points (83.26%) and 5,817/7,012 RBF points (82.96%) are held while return evidence already passes. Noiseless plant-to-reference error exceeds the entry threshold at 150 base and 147 RBF benign points, whereas noisy measured scores exceed it at 853 and 835 points. Only 125 and 123 observed exceedances coincide with reference-error-only exceedances. Noise-only scores exceed those thresholds at 459 and 477 points. These sets overlap and cannot be added as causal fractions; this decomposition does not attribute all remaining points solely to noise.

Legitimate offsets remain a secondary concentrated source: in the first second following onset/removal, 270/467 base raw exceedances and 286/466 RBF raw exceedances occur within only 2,700/29,700 observations. Equivalent clock windows contain 19/188 and 16/174 exceedances in unchanged operation. This boundary analysis was specified descriptively after the replay and is exploratory. A context-dependent error model is plausible to investigate, but these results do not establish it as the dominant solution. Entry calibration, noise and alarm persistence need matched controls.

## Heterogeneity

| Stratum | Base no-dwell benign points | RBF no-dwell benign points | Base / RBF starts per hour |
|---|---:|---:|---:|
| plant: Q1 | 355 | 381 | 1454.55 / 1521.21 |
| plant: Q2 | 509 | 498 | 1703.03 / 1636.36 |
| plant: Q3 | 334 | 316 | 1454.55 / 1345.45 |
| task: N14 | 234 | 245 | 1169.70 / 1254.55 |
| task: O14 | 308 | 320 | 1193.94 / 1260.61 |
| task: P14 | 656 | 630 | 2248.48 / 1987.88 |
| condition: authorized_offset | 582 | 586 | 2290.91 / 2272.73 |
| condition: authorized_slow | 313 | 315 | 1181.82 / 1175.76 |
| condition: normal | 303 | 294 | 1139.39 / 1054.55 |

RBF worsens Q1 and tasks N14/O14 under the matched no-dwell policy; its pooled three-point reduction is not a uniform benefit. Every plant/task has 36 overlap and fresh detections for both no-dwell methods. Registered gaps are base two and RBF one, while physical-outside-tolerance inactive points are zero. These are different definitions; retain both.

## Timing and conditional denominators

| Method | Misses | Detection median / p95 s | Clearance median / p95 s | Already inactive at return | Outside-tolerance inactive points after detection |
|---|---:|---:|---:|---:|---:|
| base_point | 0 | 0.020 / 0.080 | 0.080 / 0.780 | 2 | 0 |
| base_return1 | 0 | 0.020 / 0.080 | 0.920 / 1.040 | 0 | 0 |
| base_long | 0 | 0.020 / 0.080 | 0.920 / 1.073 | 0 | 0 |
| base_dual | 0 | 0.020 / 0.080 | 0.920 / 1.073 | 0 | 0 |
| linear_point | 0 | 0.020 / 0.080 | 0.080 / 0.780 | 2 | 0 |
| linear_dual | 0 | 0.020 / 0.080 | 0.920 / 1.073 | 0 | 0 |
| rbf_point | 0 | 0.020 / 0.093 | 0.080 / 0.780 | 2 | 0 |
| rbf_return1 | 0 | 0.020 / 0.080 | 0.920 / 1.040 | 0 | 0 |
| rbf_long | 0 | 0.020 / 0.080 | 0.940 / 1.073 | 0 | 0 |
| rbf_dual | 0 | 0.020 / 0.080 | 0.940 / 1.073 | 0 | 0 |
| rbf_dual_nodwell | 0 | 0.020 / 0.093 | 0.650 / 0.780 | 0 | 0 |
| following_point | 0 | 0.020 / 0.080 | 0.000 / 0.000 | 105 | 6984 |
| following_dual | 0 | 0.020 / 0.080 | 0.000 / 0.100 | 78 | 3310 |
| rbf_following_dual | 0 | 0.020 / 0.080 | 0.000 / 0.100 | 79 | 3318 |
| persistence_point | 41 | 0.020 / 0.040 | 0.000 / 0.000 | 67 | 15957 |
| mean21_point | 60 | 0.060 / 0.240 | 0.000 / 0.000 | 48 | 11780 |
| base_cusum | 0 | 0.040 / 0.173 | — / — | 0 | 0 |
| base_dual_nodwell | 0 | 0.020 / 0.080 | 0.650 / 0.780 | 0 | 0 |

Clearance means first inactive observation at/after stable physical return within five seconds. Already inactive counts zero; consequently the literal label is **inactive by physical return + 5 s**, not evidence of retaining an alarm throughout recovery. Following point is already inactive in 105/108 returned events; persistence and mean21 have 41 and 60 misses, excluded from their conditional clearance samples. CUSUM has 108 detected returned events and 108 censored clearances within the horizon. All absent/censored outcomes and n/missing fields remain in summary.json. Physical-outside inactivity is counted across eligible episode support; its after-detection variant does not count pre-detection points. Neither replaces the original gap metric.

Physical tolerance 0.1 is coordinate-specific: position scales give approximately 0.01992–0.02007 and 0.02290–0.02297 rad; velocity scales give 0.01614–0.01639 and 0.01555–0.01579 rad/s. Exact per-plant values are in summary.json. These are study tolerances, not safety limits.

## Execution and validation

Twelve synthetic tests passed. One initial launch failed before the worker executed because the sandbox denied /bin/ps; its zero-output receipt remains in replay_001. REPAIR_FREEZE.json preserves an unchanged scientific worker and an explicit environmental retry. replay_002 completed: 1.632672 s supervised wall, 1.295682 s worker CPU, 74.0 MiB sampled RSS, 89.16 MiB getrusage peak and approximately 6.06 MiB output. All 400 original frozen bindings remain identical. 71,523 worker parity checks passed; 112,847 fresh-process read-back checks passed, including all 3,213 original outcome records and every old alarm stream.

The worker-side seal was taken before the terminal log line, so that streaming log is bound by VERIFICATION.json after completion; scientific output hashes verify unchanged. No scientific artifact or frozen source was patched. Source/environment/configuration/input provenance and every attempt are preserved.

## Reproduction and output schema

From manufacturing/, the original consumed execution command was `.venv-reproduction-v02/bin/python research_cycles/review_extension_v0.18/run.py`; the recorded environmental continuation was `.../resume.py`. Do not rerun either into the same attempt. `test_replay.py` needs only synthetic fixtures; `present.py` regenerates this report from local saved artifacts. `verify.py` writes a non-overwriting verification receipt. A reviewer replay in a fresh destination can use `worker.py --output PATH` through the same supervisor/limits after preserving input identities.

- `runs/replay_002/outcomes.json`: 3,402 episode-method rows; original metric fields unchanged plus alarm-run lengths, physical outside inactivity and conditional-censor fields.
- `runs/replay_002/summary.json`: 18 methods, pooled/plant/task/condition/plant-condition strata; delay distributions include n/missing/median/p90/p95/max.
- `runs/replay_002/diagnostics.json`: benign score/retention/reference-error decomposition.
- `runs/replay_002/matched_alarms.npz`: all 189 new base no-dwell alarm streams with ordered episode IDs.
- `REPORTING.json`: manuscript-facing summaries, source identities and explicit exploratory scope.
- `FREEZE.json`, `REPAIR_FREEZE.json`, `VERIFICATION.json`: immutable inputs, preserved failure repair and completed outputs.

No fresh evaluation was consumed. Further mechanism development remains exploratory and requires a prospectively frozen new condition set for confirmation. This replay establishes a missing ablation and reporting detail, not originality or journal readiness.
