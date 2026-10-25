# Representation study: scientific admission and prior-art decision

19 October 2026, manufacturing. This is a bounded AI-assisted mechanism review using the shared academic-research-suite deep-research workflow and its assumption-challenger guidance. It is not a human-read attestation, a systematic literature review, a novel-method certificate or experimental evidence. The reviewer created only this document. Root-owned plans and executed receipts determine what actually runs.

## Decision

Admit **normal-only state-representation feasibility**, with a fixed existing reference and explicit standard filtering controls. Do not yet admit a new attack campaign or an originality claim for the causal position/velocity estimator. The point of this stage is to determine whether better measurement interpretation can reduce the uncertainty that caused delayed entry and re-entry, before changing another alarm rule.

Keep v1.7 and the failed v0.19 requirements unchanged. The proposed study is a prerequisite for a different mechanism, not a replacement pass criterion for the earlier detector. A favorable estimation result alone cannot establish cyberattack-detection advantage or journal readiness.

The specific hypothesis is: **a causal estimator that enforces the relationship between joint position and velocity can reduce instantaneous actual-state error, with less motion lag than a trailing average, under the declared sensing conditions.** This is falsifiable, computationally small and mechanistically connected to the diagnosed error. Weighted polynomial estimation and sensor fusion are established; the hypothesis does not assert new mathematics. A future contribution would need evidence that a specific representation change benefits the admitted security monitor beyond equally informed ordinary filtering.

## What the completed study establishes

The [v0.19 independent review](../context_recovery_v0.19/INDEPENDENT_REVIEW.md) finds that 678 of 679 candidate outside-tolerance inactive observations lie in the declared uncertainty band. None violates the entry rule. There are no alarm falling edges while outside tolerance. The errors comprise late initial entry and missed or delayed re-entry, including 321 points after a previous sustained return. The first-return definition did not imply permanent convergence.

This separates an implementation defect from insufficient distinguishing information. Flipping the retained state in the uncertain band does not increase information; it changes the false-alarm/miss tradeoff. Applying an ordinary filter may improve information quality under appropriate assumptions, but a new state name, dwell length or hysteresis variant is not a distinctive contribution.

## Primary sources checked for methodological overlap

These are methodological background and the relevant recent comparator. Older estimation papers are kept separate from the recent principal-baseline window. A full system was not reproduced in this review.

| Source and evidence inspected | What limits our claim |
|---|---|
| Gualandi and Papadopoulos, *From Passive Monitoring to Active Defence: Resilient Control of Manipulators Under Cyberattacks*, [full author manuscript, arXiv:2603.13003v1](https://arxiv.org/html/2603.13003v1), 13 March 2026, §§I-A, II–III; [author institution PDF](https://www.es.mdu.se/pdf_publications/7340.pdf). The existing audit links ICRA 2026 DOI 10.1109/ICRA57385.2026.11697152; this review inspected the preprint rather than establishing byte identity with the conference version. | The paper already discusses integrator-related persistent-bias invisibility and compares a Kalman estimate with a measurement-free actuation prediction. It also periodically resynchronizes that prediction. Thus protected/reference-versus-innovation monitoring is not a broad untouched idea. Its active defence and sensor-injection threat model differ from our command-deviation/recovery task; no weakness is inferred merely from this difference. |
| *RAPT: Model-Predictive Out-of-Distribution Detection and Failure Diagnosis for Sim-to-Real Humanoid Deployment*, [arXiv:2602.01515v2](https://arxiv.org/html/2602.01515v2), 21 July 2026, §§3.2–3.4 and 6; [author code](https://github.com/csiro-robotics/RAPT), pinned revision recorded in [v0.20 admission](../baseline_admission_v0.20/ADMISSION.md). Preprint status; peer review not established. | Current-conditioned recurrent reconstruction is the general formulation; the velocity task uses previous-state/action forward prediction. Its calibrated nominal-surprise gates do not establish a physical-return guarantee. Intent-relative features would be a disclosed transfer modification. Released standardized-error scoring and local gate differ from manuscript equations; preserve this distinction rather than quietly fixing the baseline. |
| Rijnen, Saccon and Nijmeijer, *Motion Signals With Velocity Jumps: Velocity Estimation Employing Only Quantized Position Data*, IEEE Robotics and Automation Letters 3(3), 1498–1505, 2018, DOI [10.1109/LRA.2018.2800097](https://doi.org/10.1109/LRA.2018.2800097); [institution-hosted published PDF](https://pure.tue.nl/ws/portalfiles/portal/122955148/08276257.pdf), §§II–V inspected. PDF records acceptance 14 January and online publication 31 January 2018. Background, outside recent baseline window. | Causal polynomial estimation, delay/smoothing tradeoffs and jump-aware window adaptation are established. The paper derives position/velocity estimates from encoder data and shows why a window spanning an abrupt change can overshoot. An endpoint estimate or a jump/reset rule would not be new merely because it is inserted before our monitor. |
| Kang and Xiong, *Legged Robot Estimation—A Decoupled Approach via Moving Horizon Estimation and Invariant Filters*, [author-hosted 2025 workshop manuscript](https://www.leggedai.com/publication/2025rss2/14_Legged_Robot_Estimation_A_D.pdf), kinematic/MHE formulation inspected. Full archival peer-review status unverified. | Combining kinematic observations and physical constraints over a causal window is established methodological overlap. It is not a compatible manufacturing-security benchmark and does not demonstrate a failure of our candidate. |

Searches included causal joint position/velocity polynomial estimation, encoder-derived correlated noise, Kalman filtering, protected actuation prediction and robotic attack observers. Search absence is not novelty evidence. A retrieved 2025 polynomial tracking publisher page was inaccessible on open and was not used to establish detailed claims. The closer 2018 primary manuscript supplies the relevant established filtering counterexample.

## Exact candidate and information contract

Retain the finite support already proposed in [v0.20](../contribution_v0.20/MECHANISM_REVIEW.md): `w ∈ {5,9}`, at `dt = 0.02 s`. Those windows cover 0.08 or 0.16 s between first and last samples. For each joint, set `τ_i = t_i − t` and fit `[a,b,c]` by

\[
 \sum_i \frac{(q_i-a-\tau_i b-\tau_i^2c/2)^2}{\sigma_q^2}
 +\frac{(v_i-b-\tau_i c)^2}{\sigma_v^2}.
\]

Output the endpoint `[a,b]`, not the center or mean of the history. Maintain only the causal observation buffer. No attack labels, simulator truth, future measurement, online fitting, accepted-normal history, alarm-triggered reset or executed corrupted command enters the estimate. Training supplies weight estimates; normal development chooses the window. A one-step prediction target can be used retrospectively for normal development, while the deployed endpoint uses only information available at its timestamp.

The ordinary polynomial reproduction property gives a useful software constraint: exact quadratic position/linear velocity and a constant position displacement are preserved on noiseless fixtures. It does not ensure preservation of brief impulses, abrupt changes or correlated noise. Measure those limitations; do not infer them away from a passing polynomial fixture.

The estimator operates on **actual observations before subtraction of the fixed command reference**. A learned ARX position/velocity reference need not itself be kinematically consistent. Enforcing the derivative relationship directly on its residuals without the reference defect can manufacture an apparent violation. Preserve the reference output for every method. If expressing the estimator in residual coordinates, include the reference itself, which gives the same observation projection; do not use a different residual model silently.

The existing v0.20 implementation uses second-difference noise scales for all channels under a locally affine working assumption. Its design review suggested third differences for position under a quadratic assumption. These are different estimators. Root must freeze one implemented, documented rule for v0.21 and test it; this review does not change the sealed v0.20 code. Neither estimate is automatically a physical measurement-noise covariance under motion curvature or temporal correlation.

## Important falsification: velocity may contain no new measurement information

This algebra is an explanatory derivation, not a new theorem. If a velocity channel is constructed from the same encoder samples, `v = Dq`, the stacked data are `z = Gq`, where `G = [I; D]`. If encoder noise has covariance `Σ`, stacked noise has covariance `GΣGᵀ`. It is generally correlated and singular: its rank cannot exceed the number of original encoder observations. Duplicating those observations in derivative form does not create an independent sensor.

Consequently a diagonal position/velocity weighting must not be described as independent evidence in this case. It can regularize motion, but it can also double-count a noise source. A covariance-aware estimator or position-only polynomial fit is an essential explanation if encoder-derived velocity is the relevant acquisition model. Do not assume that CASPER, RAPT or a future public recording provides independently measured velocity without provider/schema evidence.

For a small simulation stage, declare and report sensing families separately:

1. Independent position/velocity noise: a favorable but explicitly limited information assumption.
2. Correlated temporally structured noise: tests the diagonal working covariance.
3. Encoder-derived velocity: derive it causally from quantized/noisy position with a frozen differentiation convention. Record the difference between an interval-average finite difference and instantaneous velocity; do not count this discretization as sensor corruption.

The root may first execute a declared subset as a bounded pilot. Unexecuted families remain pending; do not claim the broader sensing audit is complete. Adding covariance estimation or adaptive window switching after this stage would be a separately versioned method, not an undisclosed repair.

## Matched controls and finite selection

| Control | What it isolates |
|---|---|
| Raw observations | Whether estimation helps at all. |
| Trailing mean, same finite windows | Ordinary averaging and its lag. |
| Uncoupled endpoint polynomial fits, same windows/orders | Endpoint smoothing without the q/v derivative constraint. Its parameter count differs; this is not an identical-capacity ablation. |
| Constant-acceleration Kalman filter | Established recursive q/v fusion with the same observations and training-derived measurement scale. |
| Position-only endpoint polynomial when velocity is derived | Whether a nominally redundant channel adds genuine information or only a duplicated weighting. |

The KF state is `[q,v,a]`; use the standard constant-acceleration transition and position/velocity measurement matrix. Select its process-noise parameter on the same normal development objective from a small frozen grid. An untuned near-rigid KF is not a meaningful comparator. Apply the same readiness/support intersection to every method, and report full-row coverage separately. No attack-boundary reset is permitted.

For a later RAPT comparison, transform training, development, calibration and evaluation consistently and retrain each transformed model. Filtering only final inputs of a raw-trained network confounds representation with distribution shift. Keep architecture, seed roster, optimization access and budgets matched. Raw RAPT, coupled RAPT, uncoupled RAPT and KF RAPT separate a useful application extension from generic smoothing. A plain fixed-reference score on the same state estimate determines whether the recurrent model adds value. That neural campaign is not authorized or completed by this review.

## Prospectively justified objective for the immediate bounded stage

Use a **state-estimation feasibility objective**, because no validated physical cost of missed recrossings versus false alarms is available to justify a new alarm tradeoff. Do not weaken v0.19's zero-increase outside-inactivity constraint retrospectively.

For an eligible normal synthetic episode `e`, evaluate the known simulated state `x_t` only in the evaluator and define

\[
 L_{e,m} = \frac1{4|I_e|}\sum_{t\in I_e}\sum_{j=1}^4
 \left[(\hat x_{t,m,j}-x_{t,j})/s_j\right]^2,
\]

where `s_j` is the already frozen training-only channel scale and `I_e` is the common eligible timestamp set. Also report joint-position RMSE in radians, joint-velocity RMSE in radians/second and the 99th percentile of the standardized infinity-norm error. Report prospective one-step prediction separately from endpoint estimation. Do not pool unlike physical units without the fixed scaling.

Suggested finite advancement rule, to be adopted or replaced **before generation** in the root protocol:

- Select each method's finite configuration on designated normal development only, minimizing equal-condition-weighted `L`; fixed tie ordering favors the smaller window/process complexity.
- On frozen new normal conditions, coupled estimation must reduce equal-condition-weighted `L` relative to raw observations and the normally selected uncoupled/KF controls. It must also avoid worsening the pooled 99th-percentile standardized endpoint error relative to those controls. List every comparison, not only the favorable opponent.
- Report each task × plant × sensing-family cell, mean/median absolute and relative paired differences, and signs across cells. Average repeated noise seeds within a cell first; seeds and timestamps are not independent plants. Numerical equality is not a scientific win.
- If ordinary KF or uncoupled filtering matches or wins, classify the result as ordinary estimation benefit and reject a claim that the coupling is necessary. If coupled improves only under independent-channel noise, retain that narrow dependence explicitly.

The zero-direction comparisons above are an exploratory **advancement gate**, not a claim of practically important benefit. No 10% or 20% clinical/industrial relevance threshold is invented. Before an attack-level claim, specify an application-supported cost budget and a minimum worthwhile effect, retain all prior failed criteria, and freeze genuinely fresh conditions. A small positive estimation difference cannot by itself satisfy the user's publication objective.

The grid is a finite simulator study. Paired intervals from resampled cells, if reported, describe that explicit resampling scheme; they are not population uncertainty over real robots. Do not run significance tests over millions of time samples as if they were independent experiments.

## What this changes and what remains open

This stage directly tests information quality underlying ambiguous alarm states, while holding the learned reference and alarm semantics fixed. That is a measurable change from trying another persistence rule. It is still a standard estimation candidate and may fail against standard controls.

An original contribution remains unestablished. Possible future evidence is a demonstrated, specifically delimited weakness of a released nominal-surprise monitor under a declared protected-intent task, with a representation change whose benefit survives equal-information controls and model mismatch. That requires actual comparator execution, compatible task interpretation and a closer baseline-specific distinction. RAPT cannot be criticized for lacking a recovery guarantee it never claimed. A fresh attack grid should be consumed only after these prerequisites, not merely because another filter can be implemented.

No new data were loaded, no model was trained, no final evaluation was run, no manuscript was revised and no package was published by this reviewer. The existing studies and their failures remain the governing evidence. Parent should record this source/decision review in the durable project work log alongside actual root execution receipts.
