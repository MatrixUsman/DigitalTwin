# Scientific review of the nominal motion observer

## Material Passport

- Project: manufacturing; owner: Haiqa Mushtaq; date: 17 October 2026, Asia/Karachi.
- Scope: internal design review, primary-source terminology check and pre-execution validation recommendations for a causal motion observer. This is not external peer review or a paper reproduction.
- Workflow: shared academic-research-suite experiment planning/validation guidance, constrained by project instructions and the user's explicit design-and-validation request.
- Evidence available at review start: the frozen question, threat model, data/evaluation contracts, completed normal-control study and selected artifacts. This reviewer did not open raw CASPER observations or run fitting.
- Status: original pre-execution review retained below, followed by a separately identified post-run interpretation of saved aggregate artifacts. Proposed criteria in the original review are not themselves measurements; the final declared plan and run govern the recorded outcomes.

## Decision and scope

The proposed finite-phase model is a defensible **candidate motion observer**: it maintains an evolving, asset-specific phase distribution, propagates that distribution under a nominal timing rule, predicts joint observations, and corrects its distribution with newly received measurements. None of those structural properties establishes that its phase corresponds to the robot's actual task progression. That claim needs the normal-data checks below, and remains limited without independently labelled task phase.

Use **motion observer** as the working designation. A successful software run establishes correct execution of the specified model; it does not establish a validated physical digital twin. If recurrence, prediction or kinematic consistency fails, preserve the result and revise the representation before calibration. Do not select a new phase model from attack outcomes.

The frozen question concerns whether retaining synchronization evidence changes detection, not whether a more complicated model must have the lowest normal prediction error. A simple AR predictor can outperform the observer and must remain visible. Normal-only results cannot establish attack sensitivity or the usefulness of adding correction evidence.

## Primary-source grounding

| Source and access | What it supports | What it does not establish here |
|---|---|---|
| Guodong Shao, **Use Case Scenarios for Digital Twin Implementation Based on ISO 23247**, NIST AMS 400-2, May 2021, DOI [10.6028/NIST.AMS.400-2](https://doi.org/10.6028/NIST.AMS.400-2); [official full report](https://nvlpubs.nist.gov/nistpubs/ams/NIST.AMS.400-2.pdf), 30 PDF pages, read through the official service on 17 October 2026 local date | Section 2.1, printed p. 5, connects a manufacturing twin to a purpose-specific representation and synchronization of an observable manufacturing element. Sections 3.1–3.4 explain synchronization and information exchange. The report includes offline analytical uses. | This 2021 report describes the then-draft ISO framework; it is not proof of our compliance with a current standard. It does not require every research representation to model the whole plant, nor does it validate this phase model. Offline replay alone demonstrates no live connection. |
| NIST, [Digital Twins for Advanced Manufacturing](https://www.nist.gov/programs-projects/digital-twins-advanced-manufacturing), created 15 April 2024, updated 20 July 2026; official page inspected | Emphasizes synchronized representations and the need to verify and validate models with quantified uncertainty. | Does not grant physical fidelity merely because a model has a state variable or receives telemetry. Our posterior diagnostics are not validated uncertainty intervals. |
| Karl J. Åström and Richard M. Murray, [Feedback Systems: Output Feedback](https://www.cds.caltech.edu/~murray/FBS/Output_Feedback.html), official author-hosted chapter materials; accompanying [state-estimator lecture](https://www.cds.caltech.edu/~murray/courses/cds110/wi07/L1-2_estimators.pdf), 5 January 2007 | An observer estimates a system state from measurements and dynamics; prediction and measurement correction have distinct roles. The linear examples make observability assumptions explicit. | The linear convergence results do not transfer to an empirical phase mixture without a new analysis. We have no proof of observability, convergence, calibrated probability or stability for this design. |

These are methodological background, not recent detector baselines. The official author-hosted 2019 chapter PDF returned an internal parsing error in the current browser tool; the accessible author chapter page and lecture support the limited statements above. No paywall or access restriction was bypassed.

## State, progression and correction

The proposed state is a vector of nonnegative weights over a fixed, circular reference grid, plus its prior timestamp and initialization state. Its physical interpretation is **uncertainty over where the observed arm lies along one learned repetitive trajectory**, not a measured production stage or complete robot state. The reference maps phase to six joint angles and six joint velocities in documented units. Model parameters, normalization, bandwidth, nominal period and score scales must remain frozen during development and future evaluation; evolving phase weights are state assimilation, not parameter adaptation.

At each observation, propagate the previous weights using the actual elapsed timestamp and fixed nominal period. Produce the prediction from that prior, compare it with the new observation, compute proposed correction evidence, emit the score, and only then retain the corrected weights for the next record. A posterior reconstruction that already used the current observation is a separate diagnostic. It cannot replace the prospective prediction residual.

The principal contrast is valid only if the progression-aware and progression-omitted scores use **identical prior/posterior states, predictions, feature transformations and initialization**. The contrast changes whether correction evidence enters the score, not how either model is allowed to track the arm. A separate following or free-running policy is a different ablation and must not be substituted for that matched contrast.

For the proposed score `R / mean_train(R) + C / mean_train(C)` versus `R / mean_train(R)`, `R` is prospective standardized observation MSE and `C` is Jensen–Shannon divergence between prior and proposed posterior. `C` measures the distributional correction demanded by a measurement. It is unsigned: it is not a direct estimate of slowdown, acceleration, distance travelled or maliciousness. Both positive, finite training means and their distributions must be recorded. A small correction mean can make small absolute corrections influential; that fact must not be hidden by undocumented clipping.

If measurement weights are proportional to `exp(-mean_squared_distance / (2*tau))`, call this an **RBF pseudo-likelihood** unless a corresponding twelve-dimensional noise model is actually justified. A bandwidth estimated from training nearest-reference errors is not automatically a calibrated Gaussian variance. Use stable log weights, explicit underflow/invalid-input behavior and no silent substitution of arbitrary confidence. Specify whether uniform mixing is per observation or per elapsed second; per-second mixing avoids unintentionally changing the nominal process when the sampling rate changes.

## Main risks to examine before a twin claim

1. **Previously selected reference.** The 32-bin template was selected using this same normal-development partition, and the approximately 38-second period was estimated on the first training segment. Reusing that reference is legitimate development, but subsequent normal-development performance is not independent confirmation. Report this selection history. A new period search after a negative result would be another disclosed development version.
2. **Coarse state grid.** Thirty-two bins over approximately 38 seconds gives about 1.19 seconds per bin, much coarser than the nominal 20 Hz sampling. Strong apparent confidence in a bin does not imply fine physical timing accuracy. A discrete circular shift with repeated linear redistribution can introduce numerical diffusion; document the transition and test its behavior without measurements.
3. **Nonunique phase.** Pauses, returns through similar poses, symmetric motion and velocity sign changes can produce several plausible phases. Keep the full distribution. A circular mean can lie between modes or become undefined; maximum weight alone can hide a second separated mode.
4. **Independently averaged position and velocity.** The existing template learned angle and velocity channels separately. Its position derivative need not equal its stored velocity. The fact that both fields come from real telemetry does not make the averaged reference kinematically coherent.
5. **Assimilation can explain a deviation.** Prediction-before-update prevents the current observation from directly erasing its own residual, but repeated corrections may still follow sustained changed motion. The matched correction-evidence ablation is therefore necessary; it is not evidence of benefit before attack evaluation.
6. **Shared information.** Velocity is both an input to phase correction and the directly manipulated observable in the restricted scenario. Any eventual improvement must be compared with the already fitted velocity and AR controls. A correction score is not an independent sensor or a trusted authorization signal.
7. **Model uncertainty is incomplete.** Entropy, circular concentration and mode mass describe this model's phase weights. They exclude unmodelled task changes, model misspecification, clock attacks and telemetry compromise. They cannot be reported as credible intervals or measured phase accuracy without additional validation.

## Finite normal-only validation recommendations

Freeze the concrete choices, formulas, horizons, sampling/tolerance rules and resource envelope before execution. The following are proposed falsifiable gates; the versioned run configuration records the adopted exact rules. They are engineering diagnostics, not universal standards or significance tests.

| Question | Required computation and reporting | A defensible negative outcome |
|---|---|---|
| Does the nominal period recur? | Compare mean standardized observation discrepancy at `0.5T`, `0.9T`, `T`, `1.1T` on the **same** training/development origins. Match actual timestamps; use a declared tolerance, exclude gaps consistently, and show paired counts and lag errors. | If `T` is not lower than its declared alternatives, the chosen nominal cycle is not supported by that test. Do not relabel a harmonic as a validated cycle or select another lag silently. |
| Is the reference kinematically coherent? | Compute a declared periodic finite-difference derivative of reference angles in radians/s; compare with reference velocities. Report every joint's discrepancy, baseline denominator and aggregate normalized discrepancy against training-mean velocity. | Failure to improve on a constant velocity reference, substantial disagreement, or undefined denominators weakens a physical trajectory claim. No joint may be dropped to obtain a passing aggregate. |
| Are states distinguishable? | Inspect pairwise reference distances and separated competing modes; report posterior entropy, concentration, top weights and nonadjacent competing mass. State the separation rule. | Persistent multiple modes support an ambiguous phase interpretation. Low entropy alone does not verify phase accuracy. |
| Is prediction genuinely prospective? | At the next observation and predeclared one- and five-second horizons, freeze the state at the forecast origin and propagate without intervening measurements. Compare standardized joint prediction errors with fixed/free-running, following, constant-mean and AR controls when their rollout is well specified. Use matched origins and target rows for every comparison. | Lower reconstruction error but no useful prospective prediction fails the intended predictive representation. Failure to beat AR is preserved and does not by itself invalidate the simpler observer label. |
| Does synchronization help normally? | Compare corrected and matched free-running forecasts on the same horizons and origins. Separate correction during initialization from later state updates. Show all declared horizons even when one worsens. | No improvement, larger errors, or rapid state diffusion fails to support a synchronization benefit; do not select the favorable horizon after inspecting outcomes. |
| Does nominal progress remain identifiable? | Summarize wrapped phase increments, mass movements and discrepancy from nominal `dt/T`, while retaining uncertainty. Do not infer task boundaries from attack schedules or claim a ground-truth cycle count. | Corrections dominate every step or phase jumps among aliases: a timing variable exists computationally but is not established as physical progression. |
| Is software/run integrity complete? | Full native-rate eligible score coverage, finite outputs, unchanged fitted references, matched principal states, causal replay, bounded resources and artifact hashes. Tail exclusions apply only to explicitly prospective diagnostics with unavailable targets, never to main score coverage. | Missing coverage, nonfinite values, mutable parameters, leakage, failed provenance or exceeded bounds prevents artifact admission irrespective of attractive loss values. |

A computationally modest design can replay every eligible normal record once for the main score/state checks and maintain fixed-size delayed forecasts for a deterministic subset of diagnostic origins. For example, every twentieth eligible origin can reduce multi-horizon diagnostic cost if it is predeclared and reported; it is not permission to reduce the main score denominator. Timestamp matching is an evaluation operation on normal data and must not feed future targets back to the model.

For finite go/no-go decisions, reasonable predeclared comparisons are: recurrence at `T` strictly improves on all three lag alternatives; prospective error beats the training-mean reference at every declared horizon; synchronized forecasts improve over matched free-running forecasts at at least one predeclared horizon with every difference retained; and aggregate reference kinematic discrepancy improves over the constant-velocity reference. These choices are transparent internal acceptance rules, not proof of true phase or a guarantee of a publishable result. Report numerical values and all failed gates, rather than a single opaque “validated” label.

## What remains unknowable from this recording

The normal commissioning label is an assumption about a scheduled-zero prefix, not forensic proof that the stream is clean. The dataset supplies no independently labelled phase, trusted intended command schedule, authorized changeovers or repeated independent acquisitions for this study. Offline replay can validate causality and normal predictive behavior within the stated assumption; it cannot establish a live twin, security of the telemetry path, arbitrary attack robustness, robot safety or generalization across factories.

The cautious successful outcome is therefore **a tested, normal-development-supported motion observer for this specific recording**, with separately reported uncertainty and limitations. A negative normal result is a completed feasibility finding and a reason to revise the state representation or narrow the research question before final evaluation, not a reason to discard simple-control results or inspect final attacks.

## Review handoff

The parent implementation task must record which recommendations were adopted, changed or left diagnostic. This document's pre-run review is independent of code authorship within the same shared-context assistant team; it is neither blinded nor externally peer reviewed. The actual run report should link implementation tests, resource measurements, every gate outcome and the final supported model designation. No raw observations, model parameters or dataset extracts were uploaded during this source/design review.

### Review of the declared plan, before execution

The [observer validation plan](OBSERVER_VALIDATION_PLAN.md) and [versioned configuration](../configs/casper_right_arm_observer_v0.1.json) adopt the matched score contrast, training-fitted bandwidth, per-second mixing, timestamp-based forecasts, recurrence alternatives, full coverage, fixed parameter state and cautious observer terminology. They explicitly disclose reuse of the selected template/development partition and retain AR as a one-step comparator; a multi-second AR rollout is unavailable because no causal irregular-time rollout rule has been declared. This is an acceptable disclosed boundary, not an omitted favorable result.

One implementation issue was identified before execution: sampling both recurrence origins **and** history every twentieth observation leaves roughly one-second history spacing, which cannot reliably match fractional-cycle lags with the declared 0.075-second tolerance. Native-rate observations must be retained for matching while only the diagnostic origins are subsampled. Losses for the four lags must use a common paired support. The issue was sent to the implementation owner before a run; correction and synthetic coverage remain subject to the final code review.

Further pre-execution clarifications requested: explicitly define separated modes and the physical finite-difference convention; keep the posterior concentration cutoff descriptive unless a separate justified gate is declared. A concentrated distribution is not evidence that the selected phase is correct. Resource feasibility must be checked with labelled synthetic throughput measurements because the earlier ordinary-control runtime does not establish this observer's computational cost.

### Final preflight disposition

The revised implementation resolves the recurrence issue by retaining native-rate history and evaluating all four lag matches on one shared diagnostic-origin support. It records attempts, matched pairs and unmatched reasons. The reference derivative uses the circular central position difference over `2T/B`; observed motion uses the backward position difference over actual `dt`, compared with the current reported velocity. These are explicitly different diagnostic constructions.

The final plan defines the separated competitor as the largest mass outside the MAP bin and its two circular neighbours. This is a descriptive competitor, not necessarily another local mode. Entropy/resultant cutoffs remain descriptive; they do not decide scientific validity. The added progression summaries use shortest signed circular MAP-bin displacements between diagnostic origins, compare them with nominal elapsed progression, and report unchanged/backward/large-jump fractions. They reset at segment boundaries and are not phase-accuracy measurements.

Read-only review covered `observer.py`, `observer_study.py`, the bounded entry script, their synthetic tests, the plan and configuration. No remaining blocking discrepancy was identified in the ready state. Prospective residuals use prior state; proposed corrections are committed after score formation; the principal pair shares one proposal; forecasts are frozen at their origins and evaluated before target assimilation; fitted references/bandwidth/scales remain training-derived and immutable. Source/pinned-reference admission, exact score support, resource limits, failure preservation and saved-artifact readback are present. A failed scientific criterion remains visible even when the implementation executes successfully.

The model owner reported 32 passing synthetic core tests and the runner owner reported 17 passing synthetic tests; this reviewer inspected those tests without rerunning them. The parent task's integrated test receipt and actual source hashes govern execution admission. Exact static-review identities and checks are saved in ignored `local/observer_review/preflight_review.json`. This preflight finding is not a result from real data, and does not change the observer designation or establish any validation gate as passed.

## Post-run scientific interpretation — completed normal-only study

This section was added only after the parent reported terminal completion of `normal_observer_v0.1_20261016T201310_830939Z`. The reviewer then opened the saved aggregate `observer_results.json`, `run.json` and synthetic-test receipt. No raw observations, score arrays, new fits, reruns, post-hoc tests or rematching were used in this interpretation.

The manifest SHA-256 matches the supplied identity, `7e28d3955f244058f3ce4767ed90b8f9362b727f69bd7c11d5f5328a4fe53fc0`; the aggregate-results SHA-256 is `27efd84e073c7dd167c72a60f5c0b8695a63aae673b7b188b14ae3af23986318`. The run is technically completed/accepted. Its receipt records 254 passing synthetic tests, no failures/errors/skips, 536,946 eligible training endpoints, 160,472 eligible development scores for each of four score variants, unchanged fitted parameters and complete saved-artifact readback. Measured supervised wall time was 169.945 seconds, worker CPU 169.649 seconds, peak RSS 330.188 MiB and total outputs 14.053 MiB. These are software/resource observations, not attack results.

### What the declared checks support

**All seven predeclared checks passed**, with the following scope:

| Evidence | Observed aggregate | Supported interpretation |
|---|---|---|
| Recurrence in training | At nominal approximately 38 seconds: MSE `0.00064498`, versus `2.20738`, `2.05860`, `2.05948` at the three declared alternative lags; 26,765 paired origins | A repetitive structure at the chosen lag is strongly supported in this training recording. This finite comparison does not prove a globally unique physical cycle. |
| Recurrence in development | Nominal-lag MSE `0.00060564`, versus `2.26147`, `2.09204`, `2.09660`; 7,982 paired origins from 8,024 attempted, with 42 excluded for ineligible past endpoints | The same temporal structure persists in the reused development block. The comparison does not supply independent task labels. |
| Prospective prediction | Synchronized observer beats the fixed training-mean predictor at native one-step, nominal one-second and nominal five-second horizons | The representation has predictive content beyond a constant mean, including forecasts issued before receiving their targets. |
| Synchronization | Synchronized prediction is better than the declared free-running variant at all reported development horizons | Measurement correction helps this particular probabilistic phase model. Its diffusion policy limits any broader inference about fixed references. |
| Reference kinematics | Aggregate standardized derivative-versus-velocity MSE `0.00542858`, versus `0.25279433` for the training-mean-velocity reference; all six joint ratios range from `0.00932` to `0.03698` | The learned position and velocity curves are substantially more mutually consistent than the stated constant reference. This is not a dynamics, command-response or safety validation. |

The development observed-position backward-difference diagnostic also has aggregate standardized MSE `0.00336173` against current reported velocity, versus `0.99864145` for mean velocity. This supports the documented angle/velocity/time correspondence in the permitted observations; it is distinct from the quality of the observer's own predictions.

### The simple predictors remain stronger at one step

All native one-step entries below use the same 160,472 development targets and the same twelve-channel standardization:

| Predictor | Standardized development MSE |
|---|---:|
| Selected AR(4), ridge 0.001 | **0.00209357** |
| Persistence | **0.00633542** |
| Synchronized observer | 0.33891060 |
| Unconstrained following observer | 0.47125746 |
| Declared free-running observer | 0.99780915 |
| Fixed training mean | 0.99875429 |

The synchronized observer is therefore **not a competitive one-step predictor against these simple controls in this study**. Passing a gate against the training mean does not reverse that finding. It remains reasonable to study whether correction evidence has detection value, because normal predictive MSE is not attack detection performance. That hypothesis is still untested; the observer's complexity is not yet justified as a superior detector.

At the nominal one-second horizon, synchronized MSE is `0.42705331`, compared with `0.60235991` for unconstrained following, `0.96428278` for persistence, `1.02218256` for free-running and `1.02308942` for the mean. At nominal five seconds the respective values are `0.52924750`, `0.80243809`, `2.14922792`, `1.02257310` and `1.02354735`. These are paired comparisons at 8,023 and 8,019 matched targets; one and five issued forecasts respectively were censored. Actual matched development horizons averaged `1.00989` and `5.00988` seconds and reached approximately `1.05` and `5.05` seconds, within the declared tolerance. These are nominal-horizon results with explicit timestamp matching, not exact one- or five-second measurements. No multi-second AR result exists.

The previous control study reported `0.37422287` MSE for its fixed periodic template. That is retained contextual evidence from an earlier run, not a new direct rerun here. In particular, the new free-running observer is not equivalent to that ordinary template. Its posterior becomes almost uniform under the declared mixing and numerical diffusion: development mean entropy `0.99923`, resultant `0.00356`, and maximum-bin mass `0.03176` compared with uniform mass `1/32`. Its near-mean predictions therefore cannot establish that all fixed nominal references need continuous correction. Any eventual paper must distinguish this mechanism-specific ablation from the ordinary fixed-template control.

### Progression is ordered, but phase uncertainty remains material

Across 8,023 successive development diagnostic pairs, the synchronized observer's mean shortest MAP displacement is `0.84220366` bins per approximately one second, close to nominal `32/38 = 0.84210526`. All 32 bins are occupied; no backward or greater-than-quarter-cycle jump is recorded. About `23.62%` of diagnostic increments are zero, which is unsurprising at roughly one-second diagnostics with 1.19 seconds per bin. This supports an ordered latent progression consistent with the model's nominal cycle, rather than a constant state or random sequence of bins. The progression prior itself encourages this ordering, so it is not an independent measurement of physical phase accuracy.

The unconstrained variant has backward increments on `17.52%` of diagnostic pairs and greater-than-quarter-cycle jumps on `4.62%`, with much larger displacement variance. This is consistent with the nominal prior stabilizing phase selection in the reused normal recording. It does not show that unconstrained tracking has already hidden attacks.

Synchronized development mean resultant is `0.92296`, mean normalized entropy `0.43322`, maximum-bin mass `0.45328`, and the mean separated-competitor mass is `0.07347`. **53.12% of diagnostic states meet the predeclared descriptive ambiguity condition.** A high circular concentration can coexist with mass spread across adjacent bins. This percentage is neither phase error nor attack frequency. The model supports a distribution over coarse progression, not a uniquely known point phase at every observation. Mapped between-bin variance omits measurement noise and model misspecification; it is not a calibrated uncertainty interval.

### Scientific decision and next bounded action

The requested state/prediction/synchronization feasibility step is supported **at the level of a normal-development-tested empirical motion observer for this recording**. Its state has a documented relationship to recurring joint motion, prospective prediction has measurable content, the reference passes the declared kinematic check, and synchronization produces ordered progress with explicit ambiguity. Retain the term **motion observer**. These internal checks do not establish a validated physical digital twin, causal robot dynamics, live synchronization, independent phase accuracy or cybersecurity benefit.

Do not silently revise the period, bandwidth, diffusion, grid or weights to improve the observed numbers. Keep this version and all its limitations as evidence. The next bounded task should settle the final scientific comparison roster and implementation admission, retaining velocity, the ordinary fixed template and the stronger AR control alongside the exact paired `R` versus `R+C` observer scores. Any revised observer would require a separately declared development version and budget before fitting, and must retain this version's results. Resolve remaining recent-method admission and freeze the complete roster before calibration. No threshold, attack F1, final-normal alarm burden or final-test observation was examined in this scientific review.
