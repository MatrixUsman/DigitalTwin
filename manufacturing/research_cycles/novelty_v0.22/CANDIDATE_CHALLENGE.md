# Adversarial review: bounded observation correction

24 October 2026. Independent AI-assisted design review by `mechanism_audit`, requested by the root. No experiment, new literature search or claim of novel mathematics is part of this review. The root's source review determines prior-art standing. The specific candidate is a protected command-driven nominal prediction plus a causal tanh observation adapter with a certified gain, and a trusted-context-only bounded score scale.

**Verdict: mathematically admissible as a narrow candidate; originality and scientific value unestablished.** The proposed lower bound is valid under the explicit paired-path assumptions below. The main risk is presenting an ordinary residual filter's DC sensitivity as new theory, or converting a conditional deterministic algebraic bound into an unsupported physical detection guarantee.

## Exact candidate and checked bound

Let the paired nominal and disturbed paths share the same protected reference b_t, trusted context c_t, fitted weights and initial adapter state. Use fixed, documented channel scaling. Define z_t=y_t−b_t and

\[
h_t=\tanh(W_hh_{t-1}+W_zz_{t-1}+W_cc_t+d),\quad
a_t=W_oh_t,\quad r_t=y_t-b_t-a_t.
\]

The infinity induced matrix norm is the maximum absolute row sum. Let `rho=||W_h||∞<1`, `beta=||W_z||∞`, `gamma=||W_o||∞`, and `gamma*beta/(1−rho)<=kappa<1`. Tanh is componentwise 1-Lipschitz. For a disturbance starting after identical history and bounded at every past tick by D,

\[
\|\Delta h_t\|_\infty\le\beta D\sum_{i=0}^{m-1}\rho^i,
\qquad
\|\Delta a_t\|_\infty\le\kappa(1-\rho^m)D\le\kappa D.
\]

Here m is the number of affected preceding observations consumed by the adapter. At a current constant displacement delta with `D=||delta||∞`,

\[
\|r_t^a-r_t^0\|_\infty\ge(1-\kappa)\|\delta\|_\infty,
\qquad
\|r_t^a\|_\infty\ge(1-\kappa)\|\delta\|_\infty-\|r_t^0\|_\infty.
\]

The proposed score `R_t=max_j |r_(t,j)|/s_(t,j)`, with `0<s_min<=s_(t,j)<=s_max`, therefore satisfies `R_t^a >= ((1−kappa)||delta||∞−||r_t^0||∞)/s_max` whenever the right side is positive. With strict alarm `R_t>tau`, a sufficient condition is `||delta||∞>(E+tau*s_max)/(1−kappa)` **only where** the nominal residual is in fact bounded by E. The scale bound must hold on the disturbed trace; a trusted-context-only scale makes it shared under this pairing. This is a score-level sufficient condition, not a probability guarantee or an estimate of actual detector delay.

The proof uses familiar contraction, induced norms and the reverse triangle inequality. It is not new merely because it is attached to a robot predictor. A leaky residual AR model already provides the same nonzero DC sensitivity; see `MECHANISM_AUDIT.md`.

## Exact invalidity cases and required repairs

| Invalid or overstated interpretation | Required condition or correction |
|---|---|
| The initial hidden states differ, or a resynchronization imports attacked measurements. | Add `gamma*rho^m*||Delta h_initial||∞` to the adaptation bound, or justify identical clean initialization. No implicit reset-to-observation can be omitted from the gain proof. |
| A previous displacement exceeded the current offset, or the disturbance is oscillatory/returning. | Use the actual history supremum: `||delta_t||∞−kappa*D_history`. The claimed constant-offset floor can disappear during recovery. No universal recovery guarantee follows. |
| The protected reference or trusted context contains measurement-derived phase, previous alarms, model outputs or untrusted executed commands. | Audit every information path. Those paths need their own gain terms; otherwise the common-b/common-c proof does not apply. |
| Weights, normalizers, scale parameters or thresholds update during evaluation. | Freeze them, or bound their changes explicitly. The current proof is not a theorem about online parameter adaptation. |
| A skip connection, residual block, direct observation input or layer normalization is added outside the stated tanh path. | Recompute the full map's certified gain. Per-layer clipping is not an automatic full-system certificate. |
| Matrix bounds are imposed only approximately or before the final optimizer update. | Verify the final matrices numerically with sufficient slack and retain the certificate. Training-time penalties alone do not establish hard row-sum bounds. |
| Scale is predicted by an observation-dependent hidden state, or has no enforceable upper bound. | This permits evidence attenuation through the denominator. Bound the complete scale path or retain the trusted-context-only design. |
| Delta is called the attack command magnitude. | The derivation concerns the difference between **observed trajectories**. Mapping actuator/command perturbations to that displacement needs a plant model and separate assumptions. |
| Observed nominal and disturbed trajectories have different sensor noise. | Include the noise difference in delta/history bounds, or state a common-noise coupling and the probability/noise assumptions used to bound nominal residual. Independent uncontrolled noise does not satisfy exact constant displacement. |
| E is the maximum residual on finite development data. | It is an empirical reference quantity, not a future deterministic bound. The resulting radius is a selection proxy only. Claims of population coverage require a justified separate method and assumptions. |
| A few nominal experiments or conformal marginal coverage are promoted to a bound for arbitrary attacked trajectories and stopping times. | State precisely which nominal event is controlled and its population, dependence and time scope. Ordinary marginal coverage is not uniform recovery or anytime attack detection. |
| A calibrated point threshold is called a bound on alarm starts, episode false alarms or physical harm. | Those are different denominators and objectives; measure/report each separately. |
| Scaled feature infinity norms are described as physical displacement. | Declare fixed per-channel units/scales and translate the bound. Position and velocity cannot be combined as a physical distance without justification. |

The hard score-scale upper bound can be too conservative to yield useful detection at practical deviations. That is a measurable feasibility issue. A valid but vacuous certificate is not a successful security contribution.

## Selection objective and leakage boundary

Minimizing `(E_dev+tau_dev*smax)/(1−kappa)` on normal development data is allowed as an explicitly empirical design criterion if all candidate families, selection rules and constraints are fixed first. It must not be described as minimizing the true guaranteed detection radius. Selection changes the distribution of the selected development maximum and threshold. Reserve final normal calibration and all fresh attack/evaluation conditions until the candidate is selected and sealed.

All methods must use the same admitted normal populations, protected command information, nominal reference fitting access, feature scaling, eligible timestamps and final calibration rule. Report how context-dependent scaling affects the score; global scaling cannot improve the radius by itself because threshold rescales inversely. Do not silently choose attack amplitude or an operating point from exposed failures to make the certificate look useful.

## Minimum comparison that could earn a contribution

1. **kappa=0:** command-only predictor, including its normally learned command-context correction if that is present in the candidate. Otherwise network capacity/context is confounded with synchronization.
2. **Constrained finite residual AR:** `a_t=sum_l A_l z_(t-l)+g(c_t)` with `sum_l ||A_l||∞<=kappa`; use the same nominal reference, trusted context, scale and gain budget. This directly realizes the same certificate.
3. **Ordinary KF/protected reference:** reasonably normal-selected process/measurement tuning and explicit observation influence. Describe whether it satisfies the same gain constraint or is an unconstrained tradeoff control.
4. **Unconstrained same tanh architecture:** isolates the constraint, with the same training access and budget. A larger unrelated neural baseline alone is insufficient.
5. **Released RAPT and protected-history diagnostic:** tests the motivating behavior, while preserving its exact scoring/gating as a distinct comparator. Same normal training/calibration is needed for the main ranking.
6. **Equal-cap saturation control:** constrain an otherwise ordinary correction to the same output-amplitude cap, without the proposed full-history gain restriction. Tanh already bounds hidden coordinates; an output cap can preserve large-offset evidence even without contraction. If clipping alone explains the benefit, the gain-constrained recurrent architecture has not earned its additional complexity. Match cap, trusted context, fit access and score scale.

To justify a nonlinear original-method contribution, it must show a prospectively specified benefit beyond the constrained linear control: for example, a smaller **measured** sustained-deviation miss region at matched benign-alarm operating points across held-out authorized tasks/plant changes, while retaining a valid useful certificate and acceptable delay/compute. It must not win only by reducing kappa, using a better command-only b_t, widening a threshold, exploiting extra trusted inputs, or omitting adverse transients. Match the certificate/gain budgets and disclose differing capacities. No specific numerical success threshold is selected by this review.

Kill the nonlinear claim if the constrained AR/reference control matches the tradeoff, the nominal mismatch term dominates the certificate, bounds are violated by hidden information paths, or gains vanish under legitimate command/plant changes. Preserve all failures. A useful engineering implementation may remain, but it does not automatically satisfy the user's original-method paper objective.

The existing virtual plant may not require a nonlinear correction at all: earlier RBF/ARX normal studies found weak or failed gains. Normal-only feasibility must therefore beat both an equal-capacity command-only model and constrained residual AR on an appropriate predictive/empirical-radius objective before spending a fresh attack test. Do not invent a harder nonlinear simulator specifically to create a favorable niche for the network after seeing these failures. Any additional plant/source must be justified independently by the intended operational population; broad claims need independent evidence.

## Prior-art and evidence limits

The root reports close overlap with upper-sensitivity/Lipschitz predictor guarantees, robust fault-detection filters and protected observers. This review did not freshly inspect those papers and cannot establish a first-of-kind distinction. A potentially defensible scope is **constraining useful synchronization to retain a score-level sustained-deviation floor**, but that remains a hypothesis awaiting exact equation-level prior-art comparison and the controls above.

The method requires trustworthy intent and sufficiently honest observations to define the relevant deviation. Existing public manufacturing metadata do not establish both authenticated command provenance and cyber-recovery truth. Synthetic paired trajectories can test the stated algebra/assumptions; separate real recordings can test normal-model adequacy or physical-fault detection within their labels. Neither supplies general real-world cybersecurity or recovery validation by implication.

No new code, experiment, model, test signal or manuscript was changed in this review. Its outcome is conditional design admissibility, not empirical success, originality or journal readiness.
