# Independent implementation and result review — v0.19

## Material Passport

19 October 2026; manufacturing. A separate Codex agent reviewed the completed cycle, without changing methods, sources, freezes, observations or outcomes. This is AI-assisted technical verification, not independent human peer review or a new physical experiment. It follows a separate pre-execution code review. No training or simulation was run by this reviewer.

## Verification scope

- All **133 final-freeze bindings** and **61 historical v1.6 manuscript bindings** match their SHA-256 identities.
- The final freeze timestamp, `2026-10-18T21:10:39.265652+00:00`, precedes the final launch, `2026-10-18T21:10:57.471403+00:00` (both 19 October locally).
- Independently computed contingency counts, alarm starts, outside-tolerance support, first physical return, conditional clearance and joint outcomes from saved arrays: **29,381 scalar/row checks** across 216 episodes and 2,376 method outcomes pass. This arithmetic did not call `evaluate`, `extra_metrics`, `summarize` or `criterion`.
- Separately reconstructed all **11 primary clauses**, their relative reductions and the final pass/fail Boolean from pooled counts; all agree.
- The root verifier additionally records full reference/score and decision replay. This review did not duplicate its inference replay or treat its 4,107 checks as this review's independent checks.
- The original v0.14 configuration retains its frozen identity and original failed primary result: 2.0123% benign-point reduction, below 10%, with the original plant/gap failures. No later result converts that failure to success.

Read-back commands used the existing `.venv-reproduction-v02/bin/python`, with `PYTHONDONTWRITEBYTECODE=1`, from the workspace root. They read only admitted source/metadata, saved models/scales and completed synthetic result arrays. The only file this review creates is this document.

## Prospective outcome

**The candidate fails its frozen composite criterion.** It achieves the benign-burden reductions, but loses the required outside-tolerance support and joint performance against base dual and exceeds its allowed fresh-detection delay cost. A favorable matched-hysteresis comparison does not replace the failed overall criterion.

The common final population has 424,800 wholly benign eligible points (2.36 pooled hours), 144 attack episodes and 66,357 post-onset physical-outside-tolerance points. All listed methods overlap all 144 events. Rates describe this simulation grid; they are not validated operating rates for real robots.

| Method | Benign points | Starts | Starts/hour | Fresh events | Outside-inactive points | Joint successes | Fresh-delay p95, s |
|---|---:|---:|---:|---:|---:|---:|---:|
| Base dual | 42,193 | 3,341 | 1,415.68 | 136 | 0 | 144 | 0.040 |
| Base dual, no dwell | 6,628 | 4,941 | 2,093.64 | 144 | 1 | 143 | 0.040 |
| Three-of-five entry | 2,143 | 316 | 133.90 | 144 | 256 | 12 | 0.080 |
| Global envelope | 305 | 108 | 45.76 | 144 | 767 | 62 | 0.777 |
| Contextual hysteresis | 201 | 105 | 44.49 | 144 | 1,016 | 12 | 0.731 |
| Contextual two-sided envelope | 332 | 94 | 39.83 | 144 | 679 | 62 | 0.731 |

Candidate versus base: benign points decrease **99.2131%** and starts **97.1865%**, but outside inactivity becomes **679/66,357 = 1.0233%**, joint successes fall 144→62, and p95 fresh delay rises 0.040→0.731 s (cost 0.691 s; permitted increase 0.200 s). The eight baseline events lacking a fresh onset are not overlap misses: the alarm already overlaps their schedule. Both definitions remain necessary.

Against matched contextual hysteresis, two-sided return evidence reduces outside inactivity 1,016→679 (337 points, 33.17%) and raises joint successes 12→62. It also raises benign points 201→332 while reducing starts 105→94. The global envelope already obtains 62 joint successes with 305 benign points; context changes a tradeoff rather than establishing universal dominance or novelty.

All 144 events have a recorded physical return and conditional inactivity by return + 5 s; none has a censored clearance in this campaign. This count alone is not successful continuous support. Contextual hysteresis is already inactive at return in 116 cases; context/global two-sided methods in two each. Their conditional clearance medians/p95s are 0/0.020 s, 0.060/0.120 s and 0.060/0.120 s, respectively. Base dual is 0.920/1.060 s. Early inactivity explains apparently fast clearance for some methods.

## Where the 679 candidate inactive points occur

Additional decomposition below is **post-final exploratory diagnosis**; it is not a revised success criterion or a new selection rule.

| Method | Before first schedule-overlapping alarm | After first alarm | After alarm but before first sustained return | After first sustained return |
|---|---:|---:|---:|---:|
| Base dual | 0 | 0 | 0 | 0 |
| Three-of-five entry | 251 | 5 | 5 | 0 |
| Global envelope | 363 | 404 | 55 | 349 |
| Contextual hysteresis | 299 | 717 | 371 | 346 |
| Contextual two-sided envelope | 299 | 380 | 59 | 321 |

The candidate's 299 pre-detection points occur in 23 events; its 380 later points occur in 64 events. These event sets overlap. Most initial-delay points come from slowdown: 297/299; the smoothstep family contributes 296/299. The candidate's first-entry condition is deliberately conservative, `s > 0.1 + b`, so delay is a direct performance cost to investigate, not an implementation error to silently repair after the final test.

The 321 points after first sustained return require particular care. The frozen return definition is the **first ten consecutive post-corruption points within tolerance**, not permanent convergence for the remainder of the trajectory. Physical distance later recrosses tolerance in 39 of 144 events; the candidate is inactive during such recrossings in 38 events. The frozen outside-inactivity metric intentionally covers all post-onset samples, including these later excursions. Removing them would change the criterion after exposure.

Example: `L19_Q1_17_slow` first returns at index 1111, then has nine outside/inactive points at 1124–1132. Their true standardized distances range from approximately 0.1046 to 0.1165. Its lower evidence remains below 0.1 while upper evidence exceeds 0.1; the inactive alarm state persists in the uncertainty band.

Across all 679 candidate outside/inactive points:

- **678 satisfy L ≤ 0.1 < U**: the algorithm retains the inactive state in the ambiguous band.
- **One satisfies U ≤ 0.1**, illustrating that an empirical calibration allowance is not a guaranteed physical enclosure.
- **Zero satisfy L > 0.1**: no saved state violates the declared entry logic.
- True distance ranges from 0.100006 to 0.156051; median 0.111843, p95 0.139405.
- There are **zero falling edges occurring while outside tolerance**. Inactivity therefore includes late initial entry and missed or delayed re-entry after an earlier inside-tolerance period, rather than simply clearing at an outside state.

| Candidate stratum | Pre-detection points | Later points | Total outside/inactive points |
|---|---:|---:|---:|
| Lissajous | 3 | 215 | 218 |
| Smoothstep | 296 | 165 | 461 |
| Original plant configurations | 170 | 165 | 335 |
| Perturbed plant configurations | 129 | 215 | 344 |
| Brief offset | 0 | 94 | 94 |
| Persistent offset | 0 | 117 | 117 |
| Hold | 2 | 118 | 120 |
| Slowdown | 297 | 51 | 348 |

These findings locate the failed tradeoff. They do not authorize an outcome-tuned redesign on the same final conditions or establish that any suggested next mechanism will improve it.

## Scientific and publication interpretation

The completed bounded investigation demonstrates a useful component effect against its matched contextual-hysteresis ablation, while failing the broader prospectively declared advantage. Ordinary global-envelope and simpler temporal controls remain necessary comparisons. Existing literature already includes conditional thresholds, uncertainty envelopes and hysteresis; these results do not independently establish an original algorithm. `novelty_established: false` is consistent with the inspected evidence.

The results are synthetic transfer conditions within one simulator family. Added plant parameterizations and paired seeds are not independent real robots. There is no new CASPER attack reproduction, no public-robot recovery validation, and no human author approval established here. The original-contribution objective remains open; this review does not replace it with a negative-results publication objective.

## Evidence identities

- Final freeze: `research_cycles/context_recovery_v0.19/FINAL_FREEZE.json`.
- All episode outcomes: `local/context_recovery_v0.19/final_001/outcomes.json`, SHA-256 `19df9960e668f5a0564e250655ae4486da7e129011f6b65c2c5e3275ac63754b`.
- Summary/primary result: `local/context_recovery_v0.19/final_001/results.json`, SHA-256 `c96bb96a36b760fb77825b28b24d97ab55bc491c15162f8de41abe6f4506371b`.
- Streams: `score_<id>.npz` and `truth_<id>.npz`, bound by `SCORES_SEALED.json` and `completion.json`.
- The primary rule remains in the pre-final `PLAN.md` and `mechanism19.py`, bound by the final freeze. No criterion, model or outcome was edited during this independent review.
