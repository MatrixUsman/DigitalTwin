# Independent technical review of normal-only feasibility v0.21

19 October 2026. A separate Codex agent reviewed the frozen plan, implementation and saved result arrays. This is AI-assisted source/result verification, not independent human peer review. The reviewer did not train a model, generate a trajectory, alter a frozen file, inspect protected public test observations or revise the manuscript.

## Finding

**The coupled polynomial estimator fails the frozen advancement gate.** Ordinary Kalman filtering has lower standardized state RMSE in every declared sensing regime. The code and saved metrics support rejecting this candidate for another attack campaign in this cycle. This is a completed, useful method-selection outcome; it does not establish a new detector or repair the previous failed improvement result.

| Sensing regime | Raw | Mean | Uncoupled | Coupled | Kalman |
|---|---:|---:|---:|---:|---:|
| All, balanced pooled grid | 0.107858 | 0.033935 | 0.057587 | 0.057659 | 0.049746 |
| Independent Gaussian | 0.010669 | 0.024675 | 0.008317 | 0.008135 | 0.007252 |
| AR(1) Gaussian | 0.010635 | 0.025546 | 0.010641 | 0.010503 | 0.009937 |
| Quantized encoder / differentiated velocity | 0.186207 | 0.046833 | 0.098825 | 0.098981 | 0.085279 |

These are RMSEs after division by the fixed per-channel training scales. They are not errors in radians or radians/second. Coupled RMSE is 15.91% above Kalman overall, and 12.18%, 5.69% and 16.07% above it in the respective sensing regimes. Coupling improves on the uncoupled fit by 2.18% for independent noise and 1.30% for AR(1), but is 0.16% worse in the encoder case. The ordinary-control comparison therefore matters even before the difficult sensing shift.

The five families use 54 paired normal episodes, 270 method outcomes and 75,600 eligible timestamps per family. Two command shapes, three perturbed parameter sets and three sensing cases with three noise seeds form a finite simulator grid. Noise seeds are not independent robot acquisitions. No attack was generated or evaluated.

## Source and leakage review

The implemented sequence matches the frozen study contract:

- K13 observations fit the working noise and jerk scales; M13 next-observation targets select the finite settings. Source reading of `records` shows that it requests only measurements, commands and the existing base reference from those archives. It does not request their hidden simulated state.
- `selection.json` is written before L13 calibration opens. The access records contain 54 K13/M13 records followed by 27 L13 records. Calibration is width-setting only; it does not select an estimator, window or KF setting.
- Every plant selects window 5 for mean, uncoupled and coupled fits, and jerk multiplier 10 for the KF. That is the best setting in the declared grid, not a claim of globally optimal parameters. The KF winner is on the grid boundary; any expanded tuning would require a new development plan.
- Third-difference position and second-difference velocity weights are implemented as documented in this new version. The earlier prototype is not silently changed. The variance interpretation remains a working independent-noise approximation.
- Both polynomial variants fit causal endpoints; future observations are development targets only. The raw/mean predictors assume zero acceleration, while polynomial/KF predictors use estimated acceleration, as declared. Selection uses prospective prediction error rather than hidden endpoint truth. This is a permitted selection objective, but not a guarantee of best endpoint estimation.
- KF has a finite four-value development grid, uses the same four observations, and has no attack-aware reset. The warmup covers initialization for all methods. This review found no intentionally weaker information contract for the KF.
- The reference is computed once per episode and shared by all five estimators. Truth arrays are joined after all estimated-state/score arrays are sealed. Source review found no hidden truth feeding selection, calibration, estimates or reference correction.
- The independently reimplemented global interval readout exactly reproduces every saved alarm/band stream. It is the same rule across families, with each width learned on its own normal-calibration residuals. This is matched calibration procedure, not a common numeric width.

The frozen plan differs from the earlier advisory suggestion by using per-sensing RMSE comparisons and benign alarm occupancy as its cost clauses. Its actual 11 clauses were frozen before launch and are the controlling criterion. This review reconstructs those clauses; it does not substitute a post-result p99 criterion.

## Interpretation cautions that affect conclusions

**The encoder condition is a combined sensing shift.** It changes velocity noise magnitude through differencing, q/v error correlation, quantization and the timing interpretation of velocity. It cannot isolate correlation as the cause of degradation. Independent read-back gives raw encoder velocity RMSE about 0.0421 and 0.0423 rad/s, versus 0.00238 and 0.00237 rad/s under independent Gaussian sensing. The comparison uses a deliberately unchanged commissioning calibration under that shift. It is not a calibrated claim about a particular robot encoder.

**Zero mean-filter alarms do not establish good detection or recovery.** Its calibrated widths are approximately 0.179, 0.173 and 0.254, all above the readout's 0.1 tolerance. All 75,600 eligible mean-filter observations lie in the uncertainty band; the initially inactive state remains inactive. This explains why low alarm occupancy must not be interpreted alone. Coupled has 20,585 benign alarm points versus raw's 24,030, but its other advancement requirements fail. Every alarm occurs in the encoder regime; no method alarms in the independent or AR(1) normal episodes.

**Normal residual coverage is not a state-confidence guarantee.** The saved `width_coverage` is the fraction of estimated-reference residual scores below an empirical calibration width. It does not prove an interval encloses the physical state, and its failure under a sensing shift cannot establish a formal confidence level. The interval rule's undefined operational cost remains an obstacle to turning this normal-only finding into a recovery guarantee.

**Finite estimation gain is narrower than original contribution.** The classical KF is a stronger state-estimation control in this study. The coupled method preserves the expected polynomial behavior in synthetic tests, but that alone supplies neither new mathematics nor a security advantage. Do not send this rejected representation to a fresh attack test merely to search for a favorable result.

## Independent arithmetic and preservation checks

The read-only [verifier](verify21.py) imports no worker, estimator, reference-model or evaluation function. It reads saved arrays and independently recomputes standardized errors, native per-channel RMSE, counts, coverage, maximum/channel and p99 errors, complete alarm/band streams, all pooled summaries and all 11 prospective clauses. It also checks finite shapes, raw-observation identity, selection minimizers, access-role records and timestamp/hash relationships.

Executed from `manufacturing/`:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv-reproduction-v02/bin/python research_cycles/observer_feasibility_v0.21/verify21.py
```

The audit passed **331,344 checked values/logical assertions**, comprising 324,000 raw-observation identity values and 7,344 remaining arithmetic, identity and logical assertions. This count is not a count of independent scientific tests. All 140 scientific-freeze bindings and saved completion/score identities match. The reconstructed overall admission result is false. Numerical substep refinement is 1.2073e-6 native units against the declared 1e-4 limit. This review did not regenerate that trajectory or fit the models again.

The successful worker reports 5.929 s CPU. The supervisor reports 6.142 s wall time, 48,480,256 bytes sampled peak RSS and 21,069,702 output bytes; process `getrusage` independently reports a 49,332,224-byte lifetime peak. Sampled RSS and lifetime peak are different observations, not contradictory resource claims.

Preparation/import failures and the initial process-monitor permission failure remain preserved. `normal_001` has no worker provenance, no worker-log content and zero RSS samples. That supports the narrow statement that it produced no recorded scientific outputs; those observations alone cannot prove that not one instruction executed before the process was terminated. The separately recorded monitor-resume adapter launched the same hash-bound scientific worker in `normal_002`. It did not change method settings or frozen conditions.

## Handoff

Preserve the failed coupled-estimator admission and leave v1.7 unchanged. The current result supports ordinary estimation as the stronger explanation and exposes the consequences of sensing mismatch. It does not justify an immediate attack extension of this rejected candidate. A subsequent distinct mechanism must first explain what information or decision target changes beyond ordinary estimation and include the KF as a strong control. Root should include these concrete completed outcomes and limitations in STATUS/WORK_LOG, with the independent reviewer-package work kept separate from scientific novelty.
