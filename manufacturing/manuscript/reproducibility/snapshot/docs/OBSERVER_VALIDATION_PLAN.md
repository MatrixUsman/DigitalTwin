# Normal-only empirical motion-observer validation, v0.1

## Material Passport

- Project/owner: manufacturing / Haiqa Mushtaq.
- Declared: 17 October 2026, Asia/Karachi, before this observer's real fitting or validation.
- Authorization: the user explicitly requested design and normal-only validation of the observer, prospective prediction, synchronization, ambiguity and matched ablations.
- Status at declaration: specification, not a result. The later `OBSERVER_VALIDATION_REPORT.md` records execution and decisions. Preserve this plan unchanged once execution starts.
- Skill: the shared ARS experiment-agent workflow, scoped to local design, implementation, synthetic checks and one bounded study. No external model calls or automated manuscript pipeline.
- Inputs: frozen right-arm data/evaluation contracts and the immutable selected 32-bin template and AR(4) artifacts in `experiments/SELECTED_CONTROLS_V0.1.json`.

## Question and naming

Can a causal observer synchronize to an empirical joint-motion cycle while retaining the discrepancy between nominal phase progression and measurement-driven correction? This normal-only study checks whether its representation and predictions are useful enough to investigate that question later. It cannot establish attack detection or whether correction evidence improves detection.

Call the implementation an **empirical phase-based motion observer**. The phase bins map to measured joint positions and velocities, but phase has no independent ground truth. Neither authenticated commands nor robot dynamics are supplied. Passing internal checks is not sufficient for a validated physical digital-twin claim. This decision refines the conditional terminology in the historical question document without changing its frozen data/evaluation contract.

The period and reference values were fitted on training in the ordinary-control study; the 32-bin template configuration was selected on normal development. The new use of that same development partition is explicitly **developmental reuse**, not independent validation, a new holdout, or a preregistration of the entire research project. No configuration will be changed after this run to make its checks pass.

## State, observation correspondence and nominal progression

The immutable reference has period `T` seconds, `B=32` bins and a 12-channel standardized mean `m[k]` for each bin. Its existing training-only standardizer maps six joint positions and six joint velocities into and out of physical units. There is no new template fit or development refit.

The dynamic state is a categorical weight vector `p[k]` over cycle phase plus the number of observations since reset. It expresses uncertainty over where the recorded motion lies on the empirical cycle. Retain the complete distribution; a circular mean is not a unique physical-state estimate when phases are ambiguous.

For actual relative elapsed time `dt`, nominal progression shifts the distribution forward by `B*dt/T` bins using a circular linear interpolation of adjacent bins, then mixes in uniform weight with `epsilon=1-exp(-0.02*dt)`. This fixed numerical transition expresses periodic progression and modest phase diffusion. It is not an identified mechanical state-transition equation. Repeated fractional shifts add numerical diffusion; a single long-horizon shift need not equal many short shifts.

Every segment starts from a uniform phase distribution. All variants receive the same 1,528-observation warmup. Only the frozen gap rule or partition boundary resets state. Attack labels/boundaries never initialize, reset or identify phases. The model receives `Observation(q,qdot,dt)` only; labels, row identifiers and absolute timestamps stay with the evaluator.

## Prediction and correction

1. Propagate the previous posterior using `dt` to obtain prior weights `p_minus`.
2. Predict the current standardized 12-channel observation as `sum_k p_minus[k]*m[k]`. This prediction uses no current measurement.
3. Form the prospective residual `R=mean_j (z[j]-prediction[j])^2`.
4. Compute each bin's mean squared standardized distance `D[k]` to the current measurement. Define a normalized radial-basis pseudo-likelihood proportional to `exp(-D[k]/(2*tau))`, with stable log normalization. This is not a calibrated Gaussian noise model.
5. The bandwidth is `tau=max(mean_training min_k D[k], 1e-8)`, fitted once on all and only 536,946 eligible training endpoints. No development selection or bandwidth sweep occurs.
6. Tentatively reweight the prior by that pseudo-likelihood. Compute correction evidence `C=JensenShannon(p_minus,p_plus)` using natural logarithms, before committing the tentative state. It lies between zero and `log(2)`, subject to numerical tolerance.
7. Emit the score, then commit `p_plus`. Proposal creation must not mutate state. A stale proposal or one from another observer must fail.

`C` quantifies synchronization effort relative to nominal progression. It is unsigned; it does not independently identify a speed increase, slowdown, attack or physical phase error. A low residual after correction must never be substituted for the prospective residual.

## Matched and auxiliary comparisons

The principal score pair shares **one observer trajectory**, not separately fitted trackers:

- Without correction evidence: `S_R=R/a`.
- With correction evidence: `S_RC=R/a+C/b`.

`a` and `b` are the arithmetic means of `R` and `C` over the eligible training replay after bandwidth fitting. Both must be finite and strictly positive or the study fails. Weights are fixed at one, without development or attack optimization. Save the scales and distributions: a very small `b` can amplify tiny corrections. The pair's state and predictions are identical by construction and synthetic tests must verify this. No normal-only objective can select the better attack detector.

Auxiliary state-update variants use the same template, bandwidth, inputs, initial state and warmup:

- **Unconstrained following:** forecast using the last posterior and nominal progression, then update from the likelihood alone, ignoring the nominal prior. This allows measurement-driven phase jumps; it is not a constant uniform-prior forecast.
- **Free-running:** synchronize during the common warmup, then propagate without further measurement correction. Its correction evidence is zero by definition.

Replay the already selected AR(4), a one-step persistence predictor and a zero-standardized-mean predictor as ordinary forecasting comparisons. Do not refit or select any of them. Prior control-study values may be contextual; direct comparisons require identical endpoints, inputs and forecast horizon.

## Normal-only validation and predeclared diagnostics

All primary one-step scores cover exactly the frozen 160,472 development endpoints, with no masks chosen from observed values. Training replay uses 536,946 eligible endpoints. Every variant must produce finite output. Diagnostic subsampling is every 20 eligible endpoints and never changes primary score coverage.

**Recurrence.** On both training and development, compare the standardized motion at diagnostic endpoints with past observations at lags `0.5T`, `0.9T`, `T`, `1.1T`. Use native timestamps with an absolute matching tolerance of 0.075 seconds and a common paired denominator for all four lags. Do not cross gaps or partitions. Retain counts, timing error and each lag's MSE. The nominal-cycle check passes only if the `T` MSE is strictly lower than all three alternatives in each partition. Failure limits the periodic interpretation; it does not authorize selecting a new period.

**Prospective prediction.** Report all-endpoint one-step standardized MSE and per-channel errors. At every 20th eligible development origin, freeze forecasts for 1 and 5 seconds ahead from the post-origin state; propagate once by the declared horizon with no intervening measurements. The evaluator matches the first eligible future endpoint at or after the target within 0.075 seconds. Save matched counts, timing errors and boundary/gap exclusions. Origins without eligible future endpoints are reported, not imputed. Compare observer variants with persistence and the fixed training mean at the same origins/targets. AR's primary comparison is the native one-step endpoint task; a time-horizon AR comparison is unavailable unless an explicit causal time-to-step rule is implemented and declared before execution.

The internal prediction check requires finite full primary support and MSE below the training-mean forecast at every declared horizon. The synchronization-benefit check requires lower MSE than free-running at at least one declared horizon; report every horizon even when a check fails. These are diagnostic engineering criteria, not statistical significance or proof of cybersecurity benefit. A simple AR beating the observer is retained evidence, not grounds for excluding AR.

**Ambiguity and uncertainty.** Record normalized phase entropy, circular resultant, maximum bin mass, separated phase modes and mapped joint-state variance at diagnostic endpoints. A separated competitor is the maximum-mass bin outside the circular MAP-neighborhood `{MAP-1, MAP, MAP+1}`; report its bin, mass and circular distance. It is a coarse competing-bin diagnostic, not a complete modal decomposition. Record the posterior mapped variance for all twelve channels in physical units. Define ambiguity descriptively by normalized entropy above 0.5 or resultant below 0.5; report frequencies without treating these cutoffs as alarm thresholds. Report distributions and differences across variants, including confidently wrong predictions if present. Posterior weights and mapped variances are uncalibrated algorithmic uncertainty, not confidence/credible coverage. Similar states at distinct phases cannot be resolved without additional information; there is no measured phase-accuracy target.

**Inferred progression, descriptive.** At consecutive diagnostic origins within the same segment, record the shortest signed circular MAP-bin displacement in `[-B/2,B/2)`, elapsed seconds, and displacement minus `B*elapsed/T`. Report unchanged, backward and large-jump (`abs(displacement)>B/4`) fractions, resetting the comparison at gaps and partition boundaries. This is a quantized model-state diagnostic, not phase accuracy or physical speed: roughly one-second diagnostic spacing is smaller than a 1.19-second phase bin, and a MAP may switch between competing modes. No extra hard gate is based on these fractions.

**Kinematic correspondence.** In original joint units compare the circular central finite difference of the reference position curve with its separately fitted velocity curve. Compare squared discrepancy against the training-mean-velocity reference, report all six joint ratios and the standardized aggregate. The template consistency check requires aggregate improvement over that reference. Also compare causal finite differences of recorded positions with recorded velocities on permitted development observations, using `(q_t-q_previous)/dt` against `qdot_t` without angle unwrapping, reporting per-joint error and its limits. The previous observation must belong to the same continuous segment; an eligible target may use its permitted warmup predecessor. This checks correspondence, not validation of forces, commands, a continuous feasible robot trajectory or closed-loop dynamics. Averaging incompatible phases may produce a vector that is not on a valid motion trajectory.

## Software, execution and failure handling

Use the manufacturing Python standard-library environment. Synthetic tests must cover phase wrapping/mass, actual elapsed time, ambiguity, stable emissions, physical-unit mapping, immutable fitted references, current-measurement-independent prediction, tentative-versus-committed state, identical principal-pair states, fixed support, horizon alignment/censoring, gap isolation, training-only fitting and failure preservation. Synthetic fixtures and timing probes are explicitly synthetic, never CASPER results.

One declared worker attempt, CPU only: 600 seconds wall time, 300 seconds worker CPU, 1 GiB monitored RSS (poll at most one second; no instantaneous ceiling promised), 50 MiB total outputs, one computational thread, no network/subprocesses in the worker. The parent applies the tested supervisor; a terminal worker resource check also rejects excessive measured peak RSS/CPU. No automatic retry, expanded budget, installation or configuration change follows a failure.

Fit/load only the frozen training and development slices; the whole source may be hashed for byte identity but protected observations may not be parsed. Retain the old pilot/control attempt records and references unchanged. Calibration, both final slices, thresholds, attack metrics, attacks-as-phase-labels and publication are excluded.

Save the tested source inventory, source snapshots, exact command/cwd, interpreter/dependencies, hardware, seed (`null`, deterministic), configuration/documentation/data/reference hashes, dirty revision/patch, start/end times, resource samples, logs, diagnostics, training-fitted bandwidth/scales, all variant score arrays, paired row coordinates, readback/hash checks and failures. Keep row-level artifacts local and ignored. The aggregate report must distinguish successful software execution, individual scientific-check outcomes, and the final naming/next-step decision.
