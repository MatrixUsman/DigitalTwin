# Mechanism review for the bounded v0.20 investigation

19 October 2026. Manufacturing only. This is an AI-assisted design and primary-source review, prepared before any v0.20 attack experiment. It does not alter the sealed v0.19 experiment or manuscript v1.7. The user has explicitly requested a defensible original improvement, a compatible comparator and fresh evaluation; this note identifies an executable hypothesis and its originality limits rather than declaring those objectives accomplished.

## Decision

Investigate **causal joint-position/velocity fusion before anomaly scoring**, using a short, physically coupled endpoint estimate. Its role is to reject measurement noise without averaging away the current motion departure. Compare it with the released RAPT monitor and ordinary filters under the same information and calibration contract. Retain a command-driven reference if the outcome is physical departure from authorized motion; a one-step predictor and an intent-conformity monitor answer different questions.

The proposed estimator below is a weighted local polynomial estimator, equivalently a small constrained least-squares state estimator. **Its estimator mathematics is established, not a new algorithm.** Coupling it to RAPT would be an application extension that must earn a concrete empirical advantage and survive matched filtering controls. A new name, a different platform, or an unreported combination is not sufficient originality. This bounded search did not establish a unique algorithmic contribution.

Do not add a second recovery state machine now. Test the observation/state representation first, with fixed scoring and readout. A finite two-window choice is sufficient to determine whether this direction addresses the diagnosed problem. If an ordinary Kalman filter or uncoupled endpoint smoother obtains the same benefit, attribute it to estimation or filtering and do not claim that the proposed coupling is necessary.

## What the exposed experiment actually diagnoses

The [v0.19 independent review](../context_recovery_v0.19/INDEPENDENT_REVIEW.md) records 679 outside-tolerance inactive points for the contextual two-sided envelope. Of these, 678 satisfy `L <= 0.1 < U`; zero violate its declared entry rule. There are no falling edges while physically outside tolerance. Of the 679 points, 299 precede initial detection and 380 follow detection; 321 occur after the first ten-point physical return, including subsequent recrossings. Thus the immediate failure is insufficient evidence for entry/re-entry near the boundary, not an implementation defect in clearing.

The earlier [v0.18 replay](../review_extension_v0.18/RESULTS.md) identifies noisy threshold entry followed by dwell amplification. A wider uncertainty allowance rejects noise but also enlarges the ambiguous band, producing the observed latency/support cost. Changing how an inactive alarm behaves in that band alone cannot create additional information. It must be reported as a changed false-alarm/miss tradeoff.

These are post-exposure design observations. The exposed v0.19 cases may be development diagnostics, never reused as fresh confirmation.

## RAPT: a precise comparator and a conditional limitation

[RAPT v2](https://arxiv.org/html/2602.01515v2), dated 21 July 2026, describes current-conditioned recurrent reconstruction; a previous-state/action forward variant is used for velocity tracking (§3.2). Detection uses calibrated local/global deviation gates and an optional range gate (§§3.3–3.4). It explicitly acknowledges calibration/sensitivity tradeoffs (§6). The main text does not establish a physical-return guarantee.

The inspected [author code](https://github.com/csiro-robotics/RAPT), local revision `d745668ffdb0e26877b1de4c9b2126af7bda5b03`, continually updates its hidden state and previous observation in `rapt/detector.py:RaptDetector.step`. Forward input is the previous observation and action. The released scoring function is squared error divided by predicted variance; its local calibration formula also differs from the manuscript equation. Preserve those source distinctions in execution rather than silently repairing them.

**Reader-inferred hypothesis, not demonstrated RAPT failure:** conditioning on recent actual motion may reduce predictive surprise during a sustained departure, even when the motion remains displaced from an authorized trajectory. This must be tested using the real implementation. It cannot be inferred from architecture alone. A protected command reference changes the monitored quantity and must be an explicit, equally informed comparison component.

The source version/status and full paper-to-code audit belong to the parallel comparator admission record. RAPT remains a preprint unless a proceedings/publisher record verifies peer review.

### Why conditional prediction is not necessarily intent conformity

The following elementary linear example is our explanatory derivation, not an originality claim or a theorem about the nonlinear RAPT network. Suppose a nominal reference follows

\[
 x^0_t=A x^0_{t-1}+B u_{t-1},\qquad y_t=x^0_t+d_t+\epsilon_t.
\]

A one-step observation-conditioned predictor has innovation

\[
 y_t-(Ay_{t-1}+Bu_{t-1})
 =d_t-Ad_{t-1}+\epsilon_t-A\epsilon_{t-1}.
\]

For a constant displacement `d` in a unit-eigenvalue direction, the deterministic innovation vanishes although `d` is nonzero. A fixed authorized-motion residual is instead `y_t-x^0_t=d+epsilon_t`. With stable dynamics the innovation need not vanish; a recurrent network may also retain relevant context. Consequently this example motivates a failure test, not a blanket criticism of all predictors. Conditional likelihood, authorized-motion deviation and physical recovery must be evaluated as different quantities.

## Candidate A: causal kinematic endpoint fusion

Permitted inputs are the timestamped, truthful joint positions and velocities already admitted to the monitor. No simulator state, executed corrupted command, future observation, attack label or counterfactual physical state is allowed. The approved command copy may drive the existing protected reference but does not enter this kinematic estimator.

For each joint, let the last `w` observations be `(q_i,v_i)` at times `t_i <= t`, and define `tau_i=t_i-t`. Fit the endpoint position, velocity and constant acceleration by

\[
 \hat\beta_t=\arg\min_{\beta=(a,b,c)}\sum_{i=t-w+1}^{t}
 \left[\frac{(q_i-a-\tau_i b-\tfrac12\tau_i^2c)^2}{\sigma_q^2}
 +\frac{(v_i-b-\tau_i c)^2}{\sigma_v^2}\right],
 \quad \hat x_t=(\hat a_t,\hat b_t).
\]

This fits observations at the **current endpoint**, not the center or average of the window. With fixed timestamps and weights its map is precomputable: `beta=(H.T W H)^(-1) H.T W z`; use a numerically stable least-squares factorization rather than an unchecked matrix inverse. Its state is the finite causal buffer; there is no accepted-normal history or online parameter update that could absorb an attack. Estimation of actual motion is distinct from changing the nominal model.

Freeze only `w in {5,9}` at 50 Hz (80 or 160 ms of history), quadratic order, no robust reweighting, no special attack/recovery reset and no extrapolation horizon. Increasing the candidate grid after seeing attack outcomes invalidates this finite selection. A simpler linear fit may be an explanatory control but must not become an unregistered third choice.

### Calibration and selection

Estimate the observation weight ratio using training measurements only. A transparent provisional estimate under locally quadratic motion and independent white noise is

\[
 \hat\sigma_q=\operatorname{MAD}(\Delta^3q)/(0.67449\sqrt{20}),\qquad
 \hat\sigma_v=\operatorname{MAD}(\Delta^2v)/(0.67449\sqrt6).
\]

These estimates use the squared binomial-coefficient sums 20 and 6. Nonzero jerk, correlation and quantization violate the simplification; record empirical diagnostics and a fixed positive floor based on the declared measurement units. Do not substitute simulator-known noise parameters for an estimated quantity in only the proposed method. If correlated-noise weighting is added, it becomes a separate design requiring a new protocol; the first bounded test should expose the limitation.

Select `w` on normal development by a declared causal prospective-prediction loss and a predeclared tie rule, not attack performance. One eligible choice is weighted error between the polynomial's one-step-ahead `[q,v]` prediction and the subsequent normal observation; the future observation is used only as a development target, never online. The estimator then emits its **current endpoint** at deployment. Fit input normalization and model parameters on the training split, choose the window on development, and set decision thresholds on a separate normal calibration split. Do not use calibration to pick the window.

### Exact invariance worth testing, not a novel theorem

On noiseless motion with quadratic position and matching linear velocity, the estimate reproduces the current state exactly when the design has full rank. Adding a constant position offset adds the same offset to `a`; adding a constant velocity with its consistent position ramp adds that velocity to `b`. Therefore the estimator does not, by construction, force persistent physical departure toward the command reference. By contrast, a trailing mean is delayed on a ramp. These ordinary polynomial-reproduction properties motivate the candidate; tests must cover them.

At abrupt jerk or a very short impulse, the local motion assumption can fail and the endpoint fit can overshoot. Honest correlated position/velocity noise can also reduce the benefit. Neither the weighted fit nor its normal calibration provides a physical safety bound.

## Placement: project observations, not an inconsistent reference residual

**Preferred first implementation:** project raw measured `[q,v]` at every split, then use the same transformation for RAPT training, development, calibration and replay. Normalize after projection. Approved commands remain unchanged. Preserve both raw and projected observations in development/output records. A current projected target uses observations only through the current timestamp; a forward predictor uses only the preceding projected input and approved command, with explicit alignment.

For the protected-reference control, form `e_t=(xhat_t-r_t)/scale` after estimating actual state, where `r_t` is the unchanged command-driven reference. Use the same physical tolerance/readout for raw, projected, uncoupled and Kalman variants so filtering benefit cannot be confused with changing the alarm semantics. Keep an original statistical-threshold operating point as a separately named comparison if required; do not pool physical-tolerance and statistical-threshold results as if they calibrate the same quantity.

**Do not impose `d(r_q)/dt=r_v` directly on residuals of a generic learned ARX reference.** Its predicted positions and velocities need not satisfy that identity. If residual projection is used, the complete known reference must be included:

\[
 r^q_i+q^{ref}_i=a+\tau_i b+\tfrac12\tau_i^2c,\qquad
 r^v_i+v^{ref}_i=b+\tau_i c.
\]

This is simply observation projection written through residuals. In discrete propagation, the reference defect

\[
 \kappa_t=q^{ref}_t-q^{ref}_{t-1}
 -\tfrac{\Delta t}{2}(v^{ref}_{t-1}+v^{ref}_t)
\]

must be subtracted in residual-position transport. Omitting it makes learned-reference inconsistency look like a physical violation. A test with deliberately inconsistent synthetic reference channels should detect that error.

## Optional Candidate B: protected-reference representation for RAPT

Only if the root protocol explicitly admits a second scientific candidate, train the same released RAPT architecture on **raw protected-reference residuals plus approved command features**, and compare with the same representation after kinematic fusion. This tests intent anchoring separately from smoothing. It changes the feature representation; it is not a faithful reproduction of the original humanoid experiments. Both training and inference must use the same frozen reference and scaling. The reference may not reset to attacked observations.

This is a standard residual-modeling extension, not a novel algorithm. Its important falsification control is RAPT with the same protected residual representation **without** kinematic fusion. Without that control, a gain might be entirely due to revealing authorized-motion error to the detector. A favorable result could motivate an application contribution framed around a demonstrated baseline limitation; it would still need a close-prior-art argument and independent evidence. Do not launch this merely to rescue an unfavorable Candidate A result.

## Minimum explanatory roster

| Variant | Fixed question |
|---|---|
| Released RAPT, permitted common observations/commands | What does the recent nominal-only monitor achieve under our disclosed transfer protocol? |
| RAPT with coupled endpoint fusion | Does the explicit q/v relation help, with architecture, seeds and budget held fixed? |
| RAPT with uncoupled endpoint fits | Is benefit due to ordinary endpoint smoothing instead of kinematic coupling? |
| RAPT with a constant-acceleration Kalman filter | Does established recursive sensor fusion already obtain the benefit? |
| Raw and fused protected-reference physical-tolerance point rules | Does the neural detector add value beyond motion estimation and a direct readout? |
| Existing mean, three-of-five and CUSUM controls | Does ordinary temporal aggregation explain the improvement/cost? |
| Raw protected-residual RAPT, if Candidate B admitted | Is protected intent anchoring the effective component? |

The KF state for each joint is `[q,v,a]`, with `F=[[1,dt,dt²/2],[0,1,dt],[0,0,1]]`, `H=[[1,0,0],[0,1,0]]`, training-derived `R`, and a fixed, normally selected acceleration/jerk process-noise scale. No attack-triggered covariance inflation or state reset. This is an ordinary reference control. Its tuning budget must be comparable to the endpoint estimator; an intentionally rigid KF would not be a fair control.

The uncoupled control fits endpoint polynomials to position and velocity independently over the same window with the same causal support. It removes only the cross-channel derivative constraint. Report the different coefficient count; do not describe this as an identical-capacity ablation. The fitted RAPT weights must be retrained for each input transformation; filtering only final inputs of a raw-trained model confounds preprocessing with distribution shift.

## What would qualify as an earned result

Before attack generation, freeze the exact model/representation roster, normal-only selection rules, operating points, seeds and new conditions. A suitable primary comparison tests the coupled estimator against **the strongest normally admitted ordinary filtering control**, not only raw RAPT. Declare the benefit and tolerable costs prospectively. Detection, fresh entry, post-onset outside-tolerance inactive support, alarm occupancy/starts, physical recrossings and cost must all be visible.

The old zero-outside-inactivity condition and failed v0.19 result remain intact. A new operational tradeoff may be chosen prospectively, but it cannot turn that failure into success or be relaxed after exposure. Selection of the strongest control must also avoid final attacks: use a predeclared rule or report all comparisons without selecting a flattering opponent.

Fresh conditions should include different motion shapes and plant response, plus correlated sensor noise, quantization and timing assumptions where admitted. Changing only RNG seeds does not provide a new physical system. Joint-position/velocity redundancy is informative only if timestamps, units and measurement errors support it; velocity derived from the same encoder may have strongly correlated error. Simulation with independent noise in all four channels must not stand in for that validation.

A coupled-estimator win would support a narrow claim of useful kinematic regularization for the disclosed monitor/task. It would not establish new estimation mathematics, general cyberattack attribution, physical safety, or superiority on the authors' humanoid benchmark. If KF or uncoupled filtering matches the benefit, report ordinary estimation as the explanation and retain the original-contribution goal as unresolved.

## Focused prior-art record

| Primary source inspected | Scope/status and implication |
|---|---|
| [RAPT v2](https://arxiv.org/html/2602.01515v2), §§3.2–3.4 and 6; [author repository](https://github.com/csiro-robotics/RAPT) | 2026 preprint and released code. Bounded equation/code reading above; no faithful humanoid reproduction or complete supplement audit by this reviewer. It supports the proposed comparator and conditional representation hypothesis, not a proven weakness. |
| Kang and Xiong, [*Legged Robot Estimation—A Decoupled Approach via Moving Horizon Estimation and Invariant Filters*](https://www.leggedai.com/publication/2025rss2/14_Legged_Robot_Estimation_A_D.pdf), §§II–III | Author-hosted 2025 workshop-style abstract, not verified as a full peer-reviewed proceedings article. It explicitly uses kinematic measurements and physical constraints in receding-window state estimation; equations include encoder position/velocity noise and constrained estimation. Its role is methodological overlap, not a compatible cyberattack benchmark. |
| [*Observer based attack detection and security control for UAVs against attacks on desired trajectory*](https://www.sciencedirect.com/science/article/pii/S0016003224003417), Journal of the Franklin Institute, July 2024 publisher abstract | Unknown-input and attack-estimation observers combine state-estimation and tracking errors. Full equations were not inspected; no method weakness assessed. Combining observation consistency with authorized-trajectory deviation is not a broad untouched idea. |
| [*An Observer-Based Approach to Mitigation of Integrity Cyberattacks*](https://www.sciencedirect.com/science/article/pii/S2405896324003550), IFAC-PapersOnLine 58(4), 520–525 (2024), DOI 10.1016/j.ifacol.2024.07.271 | Publisher abstract verifies observer/controller residual feedback and a networked-robot demonstration. Full implementation and compatibility remain unverified; no weakness inferred. |
| [*From Passive Monitoring to Active Defence: Resilient Control of Manipulators Under Cyberattacks*](https://ieeexplore.ieee.org/abstract/document/11697152), ICRA 2026, DOI 10.1109/ICRA57385.2026.11697152 | Publisher abstract describes a measurement-free actuation-projected predictor, Kalman/chi-square monitoring and control attenuation. Full manuscript/code uninspected. It blocks a broad claim that a measurement-independent robotic reference is new. |
| [Existing recovery prior-art audit](../../docs/literature/RECOVERY_IMPROVEMENT_PRIOR_ART_2026-10-19.md) | Previously inspected Kaisar, dynamic residual thresholds, interval/conformal methods and observer agreement already limit broad protected-reference, uncertainty and recovery novelty claims. This note does not modify its frozen bytes. |

Targeted queries included robot cyberattack detection with position/velocity consistency, moving-horizon residual monitoring, causal polynomial state estimation, RAPT kinematic consistency, and persistent-deviation conditional prediction. Search absence is not evidence that a particular combination is new. Older polynomial filtering and Kalman estimation remain necessary background even though principal detector candidates must satisfy the project's recent-paper window. A Savitzky–Golay DOI retrieval returned HTTP 403; it is not represented here as a newly inspected full manuscript.

## Handoff

The root can implement Candidate A and its controls after reconciling the RAPT admission report. The root should select one explicit readout/representation contract before freezing; this design review does not authorize silently mixing Candidate A, Candidate B and protected-reference scores. No training, new final generation, paper edit, dataset read, contact or publication was performed by this reviewer. Only this document was created. No evidence currently establishes algorithmic originality; the next bounded experiment can establish or refute a specific empirical benefit.
