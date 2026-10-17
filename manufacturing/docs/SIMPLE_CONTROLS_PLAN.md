# Simple controls: normal-only fitting and selection

## Material Passport

- Project: manufacturing / Haiqa Mushtaq.
- Date: 17 October 2026, Asia/Karachi.
- Skill: academic-research-suite, bounded experiment planning/execution guidance; user instructions and project rules take precedence.
- Version: `manufacturing-casper-right-arm-controls-v0.1`.
- Status at declaration: **specified before new real-data fitting**. Subsequent implementation, test and run receipts establish actual execution; this plan is not a result.
- Scope: independent ordinary controls, not digital twins, recent-paper reproductions or attack benchmarks.
- Authorization: the user requested tested simple methods fitted using a finite normal-only procedure, with selected artifacts for later calibration. Existing pilot v0.1 is already successful and will not be replayed. This is a separately versioned study.

The [machine-readable specification](../configs/casper_right_arm_controls_v0.1.json) fixes the candidate set and resources. The [data contract](ANNOTATION_FEATURE_SPLIT_CONTRACT.md), [evaluation protocol](EVALUATION_PROTOCOL.md), [metrics](METRIC_DEFINITIONS.md) and [final protection](FINAL_TEST_PROTECTION.md) remain unchanged. Calibration and both final slices are closed.

## Information and fitting populations

Let x(t) contain the six actual joint positions followed by six actual joint velocities. Only these twelve channels and the relative native time increment are available to the predictors. The velocity control uses the six-velocity subset. No labels, absolute times, row IDs, safety status or other modality are model inputs. The runner retains coordinates outside the model for alignment. No network, GPU, model download or new dependency is required.

| Purpose | Raw half-open rows | Eligible endpoints |
|---|---|---:|
| Fit scaling, references and coefficients | [0, 540002) | 536,946 |
| Select within each declared predictor family | [540002, 702002) | 160,472 |
| Calibration and final evaluation | Not opened | None |

The common warmup is 1,528 preceding observations. Training restarts at row 16,571 after the documented gap; development initializes independently. Every eligible training endpoint is a fitting target. Warmup observations may initialize past history/phase but do not become scaler/coefficient/final-template fitting targets. Each iterator must be exhausted and its source/support checks completed. Full-source byte hashing verifies identity only; it does not authorize protected-feature parsing.

For each channel fit the training mean mu and population standard deviation sigma using Welford updates over exactly 536,946 eligible endpoints. Define z=(x-mu)/sigma. Any nonfinite update or nonpositive variance fails explicitly; no epsilon, channel dropping, clipping or development-fitted fallback. The twelve-channel standardizer is shared by template and AR candidates so their normal-development objectives have the same units. The velocity reference uses the equivalent six-channel calculation independently.

## Velocity deviation

Score(t) = max over the six velocity channels of abs((qdot_j(t)-mu_j)/sigma_j).

This deterministic singleton has no configuration search, history or fitted update during replay. Its development mean score is a diagnostic, not compared numerically with predictor MSE and not an optimization criterion. Preserve the existing tested implementation and fit a new full-training reference; do not promote the earlier subset reference to a full-training artifact.

## Frozen periodic template

This control asks whether a repeated, fixed-clock nominal trajectory is sufficient. It is not a validated physical twin or proof of a unique robot cycle.

1. Retain at most the first 20,000 observations of the first continuous training segment; use only its eligible endpoints to estimate/fill the bootstrap template. No data after the first gap enters this prefix. Sample every twentieth eligible endpoint for period estimation and require at least 4 times the maximum candidate lag plus one sampled point (481).
2. For sampled standardized vectors, calculate mean squared lag difference across all twelve channels and valid pairs for lags 1 through 121. Candidate lags 2 through 120 must be no greater than either neighbor and strictly smaller than at least one. Choose minimum objective, then smaller lag for an exact tie. No local minimum or insufficient samples is a recorded failure. There is no outcome-informed fallback period.
3. Convert the selected lag to seconds using the mean **actual elapsed-time difference** between its sampled pairs. Do not assume that twenty observations are exactly one second. This training-only estimator may find a harmonic/subharmonic; record its definition and selected artifact without claiming physical-cycle validation.
4. For each declared bin count B in {32,64}, form a bootstrap trajectory of standardized channel means in piecewise-constant phase bins. Bin index is floor(((elapsed modulo period)/period) times B). Empty bins fail; do not fill them from development or interpolate.
5. Initialize each training segment using its first 1,528 warmup observations. Against the bootstrap trajectory, evaluate all B integer bin offsets and choose the smallest summed twelve-channel squared residual, then smallest offset. Freeze that offset for the segment and advance by relative time only. Accumulate a final template from **all eligible training endpoints**, then freeze its bin means and period.
6. At development or later replay initialization, use only the preceding warmup observations to choose the offset against the final frozen template. At an eligible endpoint, predict its bin from the prior elapsed clock plus the available current dt, **before looking at the current feature values for phase selection**. Score mean over twelve channels of (z_j(t)-template_j(predicted phase)) squared. Update the clock afterward. The phase offset stays fixed; no observation-driven phase correction occurs after warmup.

This state initialization is not fitting template values on development. Warmup can cover less than an inferred period and phase can be ambiguous; deterministic tie handling does not establish correct physical phase. Gaps reset causal state, not the fitted template. Score-current alignment, offline development-wide alignment and changing phase to minimize the current error are prohibited.

## Channelwise autoregressive ridge predictor

For each standardized channel j independently, predict:

z_hat_j(t) = a_j + sum over k=1..p of b_jk times z_j(t-k).

The four candidates are p in {1,4} crossed with lambda in {0.001,0.1}. Fit each channel by minimizing **mean** eligible-training squared prediction error plus lambda times the sum of squared lag coefficients. The intercept is unpenalized. Solve the normalized Gram system using deterministic finite arithmetic; singular/nonfinite systems fail rather than silently changing regularization. Histories reset at gaps and partition starts. All eligible targets have the required preceding history under the common warmup; an unexpected shortage is a failure.

At scoring, use only preceding observations for prediction. Score the mean twelve-channel squared standardized prediction residual, then append the current observation to history. The predictor is teacher-forced one-step monitoring, not an autonomous free-running simulation. Coefficients and the standardizer never change during development or later replay. No multivariate cross-channel VAR, physical constraints, online adaptation or stability claim is implied by this small control.

## Finite selection and preservation

There are seven declared candidates: one velocity reference, two templates and four AR models. Every candidate must produce exactly one finite score on all 160,472 eligible development endpoints. Keep each candidate's immutable fitted reference, complete aligned score output or its exact integrity evidence, objective and failure status. A failed candidate is retained; do not silently remove it, replace its period or expand the grid. Complete-study admission requires the declared candidates to pass.

Select one template and one AR candidate using the mean of their standardized prediction-MSE scores on **the entire fixed normal development support**. Exact ties follow declared candidate order: smaller bin count; smaller AR order, then smaller ridge. There is no cross-family winner selection and no attack-oriented tuning. The singleton velocity control is retained regardless of the other losses. Report all candidate objectives so an unfavorable result remains visible.

Do not refit on development after selection. Save three selected immutable parameter artifacts and a manifest binding them to source/configuration, split/feature policy, environment, training counts and selection evidence. Those artifacts may later supply calibration; they do not authorize it, complete the final campaign freeze or establish attack sensitivity. No threshold, alarm, F1, AP, event-delay or final-normal burden is computed in this task.

## Software checks and bounded execution

Synthetic fixtures must test known numerical fits, constant/nonfinite failure, serialization, immutability, past-only predictions, future-suffix invariance, score-before-update, gap/partition reset, phase warmup/ties, period failure, all candidate coverage and selection. Runner tests must bind the complete tested source/config inventory and interpreter, reject protected population access and changed receipts, preserve worker failures and prevent attempt replay.

Reuse the tested supervisor for one CPU worker: **600 seconds wall, 300 seconds CPU, 1 GiB monitored RSS, 50 MiB total outputs**, at most one second between memory polls. Sampled RSS is not an instantaneous kernel ceiling. Keep worker/log/output budgets, timestamps, hardware/dependency versions, code revision and dirty/source snapshots, counts, model hashes before/after development and all terminal failures. The loader's full-byte hashes, sequential positioning and actual selected feature parsing are counted separately.

Compact training buffers and small sufficient statistics keep this finite standard-library study feasible in principle. Its actual resources must be measured, not inferred from the earlier smaller pilot. Use synthetic timing to detect implementation costs before starting; do not broaden limits or retry automatically after a real failure. An attempted run and any change require their own preserved record.

The executable command will be bound to a new successful test receipt:

```sh
.venv/bin/python scripts/run_control_study.py --execute --test-receipt <matching receipt path>
```

Run from `manufacturing/`. The launch manifest replaces the placeholder with actual values. The earlier pilot attempt ledger and fitted artifacts remain intact. A compact CNN is deferred: it is optional and the essential controls should be understood and validated first.
