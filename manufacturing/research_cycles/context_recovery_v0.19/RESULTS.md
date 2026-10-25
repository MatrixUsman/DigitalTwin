# Contextual recovery investigation: measured outcome

19 October 2026. Completed user-authorized bounded investigation; all conditions are synthetic. Original v0.14 and v1.6 remain unchanged. The original-contribution objective remains open.

## Selection, execution and validation

Two command-memory choices (10/40 samples) were fitted separately on each plant: K13 command context, L13 empirical allowances, M13 normal development selection. Memory40 was selected globally. Each plant has9,900 context-training and9,900 allowance-calibration observations; pooled selection uses29,700 observations. Both candidates had zero development alarm points; the stated tie rule selected the narrower average allowance. No attack label selected a setting. All source records were previously exposed synthetic development.

The single fresh campaign completed216episodes and2,376 method–episode outcomes with756,000 eligible points. There are144attack episodes and72benign episodes, totaling2.36eligible benign hours. New Lissajous/quintic paths and three perturbed plant configurations supplement their three parent configurations. No independent physical robot or real attack acquisition is claimed.

Actual final cost: 103.197s wall, 102.722s CPU, 78.42MiB sampled RSS, 205.36MiB outputs. All caps respected. Twelve synthetic tests passed; 4107 read-back checks passed, with full inference reconstruction confirming every retained reference and every score exactly. All133 final frozen bindings remain intact.

The initial cost-admission pilot and subsequent full-storage estimate failed before final generation. A separately bound cache-aware estimate and compact lossless export admitted the unchanged scientific study. See RESOURCE_DECISION.md. Final evaluation ran once, with all scores sealed before joint scoring.

## Full roster

| Method | Benign points | Starts/h | Fresh/144 | Outside-inactive points | Joint/144 | Fresh delay p95(s) | Clearance median(s) |
|---|---:|---:|---:|---:|---:|---:|---:|
| base_dual | 42193 | 1415.68 | 136 | 0 | 144 | 0.040 | 0.920 |
| base_dual_nodwell | 6628 | 2093.64 | 144 | 1 | 143 | 0.040 | 0.590 |
| rbf_dual | 43141 | 1438.98 | 136 | 0 | 144 | 0.040 | 0.920 |
| rbf_dual_nodwell | 6883 | 2137.71 | 144 | 1 | 143 | 0.040 | 0.600 |
| following_point | 5106 | 1844.92 | 144 | 8124 | 0 | 0.040 | 0.000 |
| tolerance_point | 441 | 100.85 | 144 | 284 | 40 | 0.197 | 0.000 |
| entry_3of5 | 2143 | 133.90 | 144 | 256 | 12 | 0.080 | 0.140 |
| global_set | 305 | 45.76 | 144 | 767 | 62 | 0.777 | 0.060 |
| context_point | 148 | 44.49 | 144 | 1831 | 0 | 0.731 | 0.000 |
| context_hysteresis | 201 | 44.49 | 144 | 1016 | 12 | 0.731 | 0.000 |
| context_set | 332 | 39.83 | 144 | 679 | 62 | 0.731 | 0.060 |

All methods overlap144/144 attacks and are inactive by return+5seconds. That conditional clearance result does not imply continuous alarm support. Joint outcomes require detection, no post-onset outside-tolerance inactive point (including detection delay), and timely inactivity after sustained physical return. Unlike the original registered gap measure, inside-tolerance onset/recovery intervals do not count as physical support loss. Additional comparisons across the two metric definitions must remain explicit.

## Prospective criterion

Overall passed: **False**. Every declared clause:

- `base_delay_cost`: False.
- `base_fresh_not_lower`: True.
- `base_joint_not_lower`: False.
- `base_outside_not_worse`: False.
- `matched_hysteresis_delay_cost`: True.
- `matched_hysteresis_fresh_not_lower`: True.
- `matched_hysteresis_joint_not_lower`: True.
- `matched_hysteresis_outside_not_worse`: True.
- `occupancy_20pct`: True.
- `recovery_component_gain`: True.
- `starts_10pct`: True.

The candidate reduces benign points99.21% and starts97.19% against original base dual, but violates its delay and outside-support constraints; joint success falls144→62. Therefore the composite improvement criterion fails. This does not retroactively change the original RBF failure.

Against matched contextual hysteresis, outside-inactive points fall1,016→679 and joint outcomes rise12→62. Benign points increase201→332; starts decrease105→94. Fresh delay is identical because entry is identical. The stricter recovery evidence accounts for a measured continuity/occupancy tradeoff; it is built from established interval inversion and hysteresis. The global-envelope control has305benign points,108starts,767outside-inactive points and62joint outcomes, so context conditioning is not uniformly superior.

Physical-tolerance point and3-of-5 controls demonstrate competing costs. Following point is fast but loses support during substantial physical deviation. None of these measurements licenses the claim that an original detector or superiority over a complete published robotic-security system has been established.

## Scope and remaining scientific work

The lower/upper evidence uses empirical99th-percentile residual allowances, not certified bounds. Top-bin extrapolation is recorded. REPORTING.json includes additional post-evaluation descriptive diagnostics of inside/outside evidence versus evaluator truth; these did not select models or alter the primary criterion. Plant/task/intervention strata and explicit missing/censored delay counts are included. Distribution percentiles describe the finite grid; adjacent samples and seeds are not independent robots.

Closest prior art establishes input-dependent thresholds, contextual motion margins, set reasoning and supervised recovery. The new numerical comparison identifies a specific tradeoff but does not prove method originality. The bounded investigation has finished; another mechanism would require a genuinely distinct rationale and another fresh protocol. Do not continue searching these final outcomes for a passing variant. Compatible independent recovery evidence and full published-system reproduction remain unavailable in this study.

The full evidence is preserved for the user to decide the next original-contribution direction. This report is not a decision to replace that objective with a negative-results paper.
