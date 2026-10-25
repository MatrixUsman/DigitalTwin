# Normal-only representation feasibility: measured outcome

19 October 2026. All observations in this report are synthetic. This is a prospectively specified normal-transfer feasibility test, not an attack experiment, an independent robot acquisition or an original-method claim. The completed v1.7 manuscript and its failed criterion remain unchanged.

## Decision

**Reject the coupled endpoint estimator for a new attack campaign in this cycle.** Its frozen advancement criterion failed. An ordinary constant-acceleration Kalman filter achieves lower state RMSE in all three sensing regimes. The proposed coupling therefore has not earned an advantage beyond standard state estimation. No new attack grid was generated.

## What ran

Training weights used K13; finite parameter selection used next-observation prediction on M13; L13 supplied residual calibration after selected settings were saved. These are task-separated normal episodes, not chronological slices of one acquisition. Every time series remains ordered, and windows never cross episode boundaries. The raw-trained ARX reference and interval alarm logic stayed fixed across representations.

Fresh evaluation: two new analytic command families, three fixed shifted plant parameterizations, three sensing regimes and seeds17/42/2026:54 episodes and270 method–episode outcomes,75,600 eligible timestamps per method. All episodes contain authorized normal motion. Truth is evaluator-only and joined after estimated states and readouts were saved. The regimes are independent Gaussian noise, temporally correlated Gaussian noise, and a combined sensing shift with quantized position and backward-differenced velocity. The last changes correlation, velocity-noise amplitude and timing simultaneously; it does not isolate the causal effect of noise correlation.

## State-estimation error

RMSE uses the same four frozen training channel scales for every method. It is dimensionless, not radians or a safety bound. Rows have equal counts; the pooled figure weighs the three declared regimes equally. Lower values indicate more accurate actual-state estimation.

| Representation | Independent noise | AR(1) noise | Encoder-derived velocity | Pooled |
|---|---:|---:|---:|---:|
| Raw observations | 0.010669 | 0.010635 | 0.186207 | 0.107858 |
| Trailing mean | 0.024675 | 0.025546 | 0.046833 | 0.033935 |
| Uncoupled endpoint fit | 0.008317 | 0.010641 | 0.098825 | 0.057587 |
| Coupled endpoint fit | 0.008135 | 0.010503 | 0.098981 | 0.057659 |
| Constant-acceleration KF | 0.007252 | 0.009937 | 0.085279 | 0.049746 |

Coupling improves on uncoupled fitting under independent and AR(1) noise, but the difference does not survive comparison with KF. It is slightly worse than the uncoupled fit under the combined encoder sensing shift. Ordinary averaging has the best pooled error because it suppresses the much larger differentiated velocity noise, while introducing motion lag and worse error in the two other regimes. No best-method generalization follows from this deliberately constructed grid.

## Fixed-readout diagnostics

| Representation | Normal alarm points /75,600 | Alarm starts | Unknown-band points /75,600 |
|---|---:|---:|---:|
| Raw observations | 24,030 | 856 | 4,905 |
| Trailing mean | 0 | 0 | 75,600 |
| Uncoupled endpoint fit | 20,548 | 1,986 | 26,670 |
| Coupled endpoint fit | 20,585 | 1,977 | 27,185 |
| Constant-acceleration KF | 18,601 | 1,962 | 30,751 |

All recorded alarms occur under the combined encoder sensing shift. The mean produces zero alarms because **all eligible observations remain in the uncertainty band** under this fixed readout. That is not evidence of successful recovery recognition or attack sensitivity. The interval widths were calibrated under the earlier independent-noise commissioning process; their coverage is not guaranteed after a change of sensing mechanism.

## Selected settings and criterion

All three plants selected w=5 (80ms between first and last sample) for the mean, uncoupled and coupled families, and the jerk-density multiplier10 for KF. Each family used its own normally selected setting. KF reaching the edge of its finite grid is a tuning-range limitation, not permission to expand it after seeing these outcomes.

| Frozen clause | Outcome |
|---|---|
| `ar1_rmse_not_worse_than_kf` | fail |
| `ar1_rmse_not_worse_than_uncoupled` | pass |
| `benign_points_not_above_raw` | pass |
| `encoder_rmse_not_worse_than_kf` | fail |
| `encoder_rmse_not_worse_than_uncoupled` | fail |
| `iid_rmse_not_worse_than_kf` | fail |
| `iid_rmse_not_worse_than_uncoupled` | pass |
| `pooled_rmse_lower_than_kf` | fail |
| `pooled_rmse_lower_than_mean` | fail |
| `pooled_rmse_lower_than_raw` | pass |
| `pooled_rmse_lower_than_uncoupled` | fail |

The zero-direction advancement rule asks whether coupling adds any measured value beyond ordinary controls, without inventing a physical cost allowance for false alarms versus missed departures. It is not a practical-benefit certification. It does not replace, relax or reinterpret the earlier v0.19 failure.

## Execution and checks

Six synthetic unit tests passed before freezing140 source/input identities. The completed worker used6.142s wall,5.929s CPU,46.23MiB sampled RSS and20.09MiB output. Limits were180s wall,120s CPU,1GiB sampled RSS and50MiB output. Double-substep refinement is recorded in `numerical_check.json`; independent saved-stream verification is recorded separately in `INDEPENDENT_REVIEW.md`.

Preparation initially failed because a new helper shadowed a historical `common` module. Renaming the new helper resolved that before freeze. The first supervised launch then failed immediately because the sandbox denied `/bin/ps`; it had no worker provenance or output. Its terminal receipt remains in `normal_001`. The explicitly restricted monitoring adapter resumed the unchanged frozen worker in `normal_002` with monitoring permitted. No scientific failure was automatically rerun.

Exact commands from `manufacturing/`:

```sh
.venv-reproduction-v02/bin/python -m unittest discover -s research_cycles/observer_feasibility_v0.21 -p 'test_*.py' -v
.venv-reproduction-v02/bin/python research_cycles/observer_feasibility_v0.21/freeze.py
.venv-reproduction-v02/bin/python research_cycles/observer_feasibility_v0.21/run.py
.venv-reproduction-v02/bin/python research_cycles/observer_feasibility_v0.21/resume_monitor.py
python3 research_cycles/observer_feasibility_v0.21/report.py
```

Receipts, selected parameters, calibration, all estimated states, evaluator truths and outcomes remain under ignored `local/observer_feasibility_v0.21/normal_002/`. No raw real dataset, protected robot test or external API was used. No manuscript, old archive, threshold rule or earlier result was changed.

## Scientific implication

This experiment rules out promoting this particular coupled estimator merely because it beats raw measurements. It leaves the original-contribution objective open. A subsequent mechanism requires a specific baseline limitation, a defensible information contract and a distinction that survives ordinary-estimator controls. Repeating new attack grids with renamed filters would not resolve those requirements. These normal conditions are now exposed and can only serve future exploratory development.
