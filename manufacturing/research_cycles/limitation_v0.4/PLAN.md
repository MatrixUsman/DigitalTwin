# Brief and persistent deviations: frozen-predictor experiment

## Material Passport

Manufacturing; owner Haiqa Mushtaq; operator Codex under the user's explicit execution request. Date: 17 October 2026. Mode: bounded experiment, using the academic-research-suite experiment workflow inline. This protocol is written before intervention execution. `FREEZE.json` will bind its exact bytes, code, tests and upstream inputs.

## Question and scope

Does a recent-history predictor's error diminish during a persistent deviation because its inputs have incorporated the changed measurements? Can causal accumulation retain useful evidence at the same normal-calibration percentile, and what false-alarm/delay/recovery cost does it incur?

Use the six saved v0.3 references: mean, persistence, AR(4), CNN seeds 17/42/2026. No retraining, checkpoint reselection, new raw file parsing, original final exposure or parameter search. All nine standardized IMU channels and fitted preprocessing remain unchanged. The CNNs reached the earlier 30-epoch cap; results are conditional on those artifacts and do not prove that the published method universally fails.

This is **exploratory synthetic measurement replay on one already exposed normal-development block**. It is not a new independent acquisition or final benchmark. Even the normal blocks below were previously used in checkpoint selection; their new roles cannot retroactively make them held out. No physical robot model, authenticated commands, cyber intent or hydraulic/water data is implied.

## Population and causal boundaries

Reuse `prepared_development.npz`, with 16,429 observations and 16,384 eligible targets. Target index `j` maps to raw numeric row `65845+j` (header excluded); source observation index is `45+j`. Require exact consecutive indices, known gap-free support and all finite arrays. Reject any mismatch.

Target coordinates `[0,4096)` estimate each model's normal error scale; `[4096,8192)` calibrate only; `[8192,16384)` measure paired nominal and synthetic outcomes. Score histories run continuously from zero, with no reset at these roles, event onset or end. Observation windows are the original causal 45-step histories; crossing these score-role boundaries is permitted because there is no model fitting here. Future observations/labels cannot influence past scores.

Every model/scorer uses the same 4,096 normal calibration targets. Threshold is ascending order statistic rank **4,056**, with alarm strictly `score > threshold`. No percentile optimization, intervention-based tuning or best-seed selection. Actual normal evaluation alarms must be reported; calibration does not guarantee a future 1% rate.

## Synthetic interventions

All 189 cases are declared in config: 7 fixed onset coordinates × 3 durations (5,45,450 observations) × 9 family/severity settings. Each case starts from the same unmodified normal block; changes only its assigned half-open interval; returns to the unmodified trace immediately at the interval's end. This discontinuity and post-event alarms remain visible.

- **Hold blend:** replace all nine channels by `(1-a)*y_t+a*y_(onset-1)`, `a=0.25,0.5,1`. Full hold is a constant telemetry segment, not proof of a physically stopped robot.
- **Slow playback:** for offset `j`, linearly interpolate the original trace at observation coordinate `onset-1+r*(j+1)`, `r=0.75,0.5,0.25`. Source coordinates never exceed the current coordinate. This stretches measurements, not a dynamics-consistent simulation of slower motion; acceleration scaling is not modeled.
- **Sensor offset:** add `0.5,1,2` training standard deviations to gyroX only. This is a measurement corruption diagnostic, not a physical command deviation.

No case is discarded for weak effect, a miss, awkward baseline behavior or undesirable false alarms. Cases share a recording and are dependent perturbations. No p-values, confidence intervals over cases or claims of independent robots.

## Scores and targeted improvement

Let `e_t = mean_c((prediction_t,c-y_t,c)^2)` in training-standardized coordinates. Point score is `e_t`; its threshold alarms are identical to thresholding RMSE. The ordinary smoothing controls are trailing means over 45 and 450 errors (partial window at stream start, fully warmed by calibration).

The targeted improvement is a fixed, one-sided **CUSUM-style evidence accumulator**:

`m = mean(e[0:4096]); u_t = min(e_t/m,25)-1.5; C_t=max(0,C_(t-1)+u_t); C_-1=0`.

Require finite positive `m`; no refit during replay. Cap and drift are declared constants, not tuned to interventions. Calibrate each scorer separately at the same percentile. An accumulator can retain false alarms or lose evidence when prediction error becomes small; measure both. Rolling means distinguish accumulation from ordinary smoothing. All scorers have the same available measurements; only their declared causal memory differs.

CUSUM is established background, not a novel twin mechanism. The primary [NIST control-chart reference](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc323.htm), checked 17 October 2026, gives the reflected one-sided recurrence. Our capped, normalized residual-energy application and empirical thresholds are explicitly specified here; NIST's distributional/ARL guarantees are not asserted for correlated robot residuals. This is a tested improvement candidate/control that determines whether a more elaborate mechanism is warranted.

## Isolating history assimilation

For each intervention compare actual predictions from altered past observations with the saved predictions from the **unmodified histories**, both against the same altered targets. The latter is an oracle counterfactual, unavailable online and excluded from the detector ranking. It isolates the effect of changed model inputs at fixed weights, targets and coordinates; it cannot establish malicious intent or security on a physical plant.

Save every affected prediction and energy plus the oracle energy, along with the unchanged full normal trajectory of scores. Only endpoints from onset through event-end+45 can change; verify this support rule. These overrides losslessly reconstruct complete raw-error time courses and all score streams. Never reset the model/score at known labels. Mean is history independent; persistence's full-hold error should be exactly zero after the first held sample, an analytic control check.

Early and late summaries use the first/last `min(duration,45)` event targets; for the shortest durations these overlap and are not evidence of temporal decay. Report actual and oracle early/late MSE, actual late/oracle late ratio (undefined if denominator zero), event overlap hits, fresh alarm onsets, misses, delays in observations, point precision/recall/F1 and post-event alarms. Event overlap with an already active alarm is not a fresh detection. Delays for misses remain null with miss counts. Primary case comparisons are paired by model/family/severity/onset/duration; do not pool model seeds as independent acquisitions.

Normal evaluation reports point-alarm fraction and episodes per 1,000 observations. Clocks are unresolved, so no seconds/hours conversion. Post-event summary covers the next 512 observations; any uncleared alarm is right-censored. Event labels are joined only after all prediction/score artifacts and the normal calibration receipt have been written and hashed.

## Execution, verification and interpretation

Synthetic tests must verify interval support/causality, unchanged sources, analytic holds, calibration rank/ties/independence, CUSUM against a loop, smoothing, label-free score generation, missing/fresh event semantics and complete roster. Then freeze code/configuration/source artifacts before running one named supervised attempt. Limits: 600s wall,300s CPU,1GiB sampled RSS,50MiB outputs. Keep failures, no silent overwrite. Existing isolated training environment and supervisor are reused; no packages installed.

An independent arithmetic verifier will reconstruct all streams and metrics from saved artifacts, compare a full-replay case against the optimized changed-window inference, verify original artifact hashes and resource limits, and retain all discrepancies. Analysis/figures are generated from saved outcomes with fixed aggregate definitions. First-onset medium-severity examples are selected here, not by best result. The descriptive report must answer which families support the hypothesis, whether accumulation improves the declared metrics, and whether smoothing/false alarms explain any gain. It may support, narrow or reject the candidate; it does not establish publication novelty.
