# Novelty investigation: selected research hypothesis

24 October 2026. Manufacturing only. This is a completed research/design investigation with a **provisional candidate**, not an established original method, successful experiment or submission-ready contribution. The current v1.7 manuscript and every earlier failed criterion remain unchanged.

## Recommendation

Investigate **a motion-monitoring twin that limits how much observation-based synchronization can erase evidence of sustained departure from authorized motion**. Constrain the complete correction path and the score's uncertainty normalization, rather than merely adding another alarm window or retraining a predictor on reference-subtracted inputs.

The proposed contribution, if earned, would be an implementable normal-only learning method with a sufficient, explicitly scoped lower bound on sustained-deviation evidence, together with a useful measured tradeoff against ordinary constrained linear filters. The reverse-triangle/contraction proof is established mathematics. The contribution cannot be the bound alone, a new method name, or changing a sensor-fault paper's application label to cybersecurity.

**Current novelty standing:** plausible narrow research hypothesis, substantial prior-art overlap, final-version comparison unresolved, no measured improvement. This is the strongest of the examined directions because it addresses a specified failure mode and has a falsifiable design property. It is not endorsed merely because a search did not find an identical title.

## What changed in our understanding

1. The exposed RAPT result is a measured task-transfer limitation, not a demonstrated causal failure of recurrence. The [completed no-fit decomposition](decomposition/RESULTS.md) exactly reproduces all 518,400 original per-channel score values over all 36 exposed episodes. It rejects a uniform absorption account: L19 persistent-offset position-channel error grows while velocity-channel error falls; S19 position error falls while shrinking variance partly opposes its score decline. Different channels and tasks behave differently. Arithmetic decomposition does not identify recurrence, immediate conditioning, phase, calibration or task transfer as the cause. No checkpoint, input, threshold or detector outcome changed.
2. Subtracting a protected reference and feeding the residual into a GRU does not in itself prevent absorption. An invertible coordinate transformation can leave all prediction errors and scores exactly unchanged. `MECHANISM_AUDIT.md` gives the counterexample; seven scalar checks passed, explicitly not benchmark results.
3. Protected predictors, trusted anchors, observer disagreement, uncertainty allowances, sensitivity-constrained models and guarded recovery already exist. These are essential comparison material, not ingredients we can claim to have invented.
4. A concrete potential distinction appears in the inspected Ghanipoor **2025 v1**: a necessary sensitivity condition from an upper energy-gain bound is different from a sufficient lower response bound. The paper itself identifies a sufficient sensitivity construction as future work. Its **2026 final journal version is not equation-verified**, so this is a version-specific lead rather than an established current literature gap. See `ROOT_SOURCE_REVIEW.md`, `THEORY_REVIEW.md` and `FINAL_VERSION_CHECK.md`.

## Exact proposed mechanism

All channels are transformed by a fixed, training-only scale. Let `u` be the protected authorized command history and `c_t` its causal context. A normally fitted, frozen reference gives `b_t=B(u_≤t)`. It may contain learned command-only dynamics; it may not take measurement-derived phase, alarms or untrusted executed commands through an undocumented path.

Let `z_t=y_t−b_t`. A small causal adapter uses past measurements:

\[
h_t=\tanh(W_hh_{t-1}+W_zz_{t-1}+W_cc_t+d),\quad
a_t=W_oh_t,\quad \mu_t=b_t+a_t.
\]

Enforce actual induced infinity norms, not just a soft penalty:

\[
\|W_h\|_\infty\le\rho<1,\quad
\|W_z\|_\infty\le\beta,\quad
\|W_o\|_\infty\le\gamma,\quad
\gamma\beta/(1-\rho)\le\kappa<1.
\]

The score is `R_t=max_j |y_t,j−mu_t,j|/s_t,j`, with strictly positive, bounded `s_t,j` derived only from protected command context and frozen normal-data fits. A changing observation-conditioned variance must not silently absorb the preserved discrepancy. This is a proposed score contract, **not** an unchanged RAPT implementation.

Tanh and row-sum bounds give an explicit fading-memory inequality between two streams sharing commands, weights, initialization and reference:

\[
\|\Delta a_t\|_\infty\le
\gamma\beta\sum_{s<t}\rho^{t-1-s}\|\delta_s\|_\infty.
\]

If the observed stream acquires a constant displacement of magnitude `D`, with no earlier larger displacement, the adapter cannot cancel more than `κD`. Thus

\[
\|r_t^a\|_\infty\ge(1-\kappa)D-\|r_t^0\|_\infty.
\]

Where the nominal residual really is bounded by `E` and `s_t,j≤s_max`, a sufficient condition for strict alarm `R_t>τ` is

\[
D>(E+\tau s_{\max})/(1-\kappa).
\]

This is a **conditional algebraic result**, not a new experimental finding, physical safety guarantee or population false-alarm guarantee. A finite development maximum is not a bound on every future nominal residual. For arbitrary time-varying motion, use the full history inequality; the plateau simplification is invalid after a larger transient until its tail is accounted for. Delta is observed-trajectory displacement, not attack-command amplitude. Noise, plant dynamics and the conversion to physical units need separate treatment. No permanent-recovery claim follows.

## Why a learned version might be useful—and why it might fail

An uncorrected reference preserves all displacement but can have substantial nominal prediction error. A predictor that closely follows observations can predict a displaced trajectory well and produce little residual. The candidate permits limited correction while retaining a quantified response. Its useful hypothesis is that a small nonlinear correction captures repeatable nominal mismatch more efficiently than a linear correction **at the same certified gain budget**.

This is an empirical hypothesis, not an explanation already established for RAPT. An ordinary leaky residual filter has the same basic property:

\[
a_t=\rho a_{t-1}+(1-\rho)\kappa z_{t-1}.
\]

The direct reference (`κ=0`) has the strongest sensitivity floor. If nonlinear learning does not sufficiently reduce normal error/false alarms relative to these controls, there is no worthwhile nonlinear contribution. Tanh saturation and scale capping can also explain apparent wins; test them separately. Legitimate unrecorded offsets that are observationally identical to unauthorized offsets cannot be separated by architecture alone.

## Candidate screening decisions

| Direction | Decision and reason |
|---|---|
| Residual-input RAPT | Reject as a novelty mechanism by itself: coordinate change does not restrict evidence cancellation. Could be an ordinary preprocessing control. |
| More dwell/hysteresis or a new return threshold | Reject as the original-method route: established machinery and repeated local tradeoffs; failed criteria remain failed. |
| KF or position/velocity coupling | Ordinary controls; the tested coupling already failed against KF. |
| Periodically reset protected twin | Existing resilient-manipulator and trusted-authentication methods overlap strongly. Any reset must be included in sensitivity analysis. |
| Active watermarking/probing | Different scope requiring control authority; manufacturing-specific DynaMark is close prior art. Not selected. |
| Coupled counterfactual uncertainty | Secondary lead; joint parameter/noise assumptions and set-membership equivalences unresolved. Not selected for immediate implementation. |
| Anytime-valid return testing | Useful inference discipline, but not a distinct new method by itself; mean evidence does not certify current physical return. |
| Gain-limited observation correction with bounded trusted scale | Select for further mathematical/code admission only. It has a precise contract, strong controls and explicit rejection conditions; originality/value remain unestablished. |

## Minimum fair comparison

| Role | Required implementation/interpretation |
|---|---|
| Command-only reference | `κ=0`, same command model, context capacity and scale. Isolates whether observation correction earns its cost. |
| Constrained residual AR/FIR | Same inputs and gain budget; require `sum_l ||A_l||∞≤κ`. Strong direct competitor, not a token ablation. |
| Saturated/clipped linear correction | Same amplitude cap as tanh where meaningful. Separates saturation from certified incremental gain. |
| Ordinary KF/protected reference | Reasonable normal-only tuning, same measurements and protected commands; report any different gain properties. |
| Covariance-aware periodically reset predictor | Admit Gualandi's joint covariance and reset mechanism explicitly, or document a task/threat adaptation and its limitations. An ordinary KF alone does not reproduce or test that whole mechanism. |
| Unconstrained same small network | Same capacity/training population. Isolates the effect of the hard gain constraint. |
| Scale ablations | Same mean with fixed, command-only and observation-conditioned scale; only preregistered variants, all outcomes retained. |
| RAPT author code | Complete detector-core transfer with matched normal populations; retain source/paper differences. Separate original gates from any disclosed common-calibration score adaptation. |
| Closest recent recurrent/robust observer | Final REN/H-minus equation and license admission first. A generic neural network is not their reproduction. |

Every main comparison must match authorized information, normal training/development/calibration, score support and evaluation populations. Adding a protected command only to our candidate creates an information advantage, not algorithmic superiority. An openly published equation does not automatically grant permission to copy an unlicensed implementation.

## Bounded next-stage design

This section is a proposal, **not a launched training or final attack campaign**.

1. **Source gate:** resolve final REN article equations and compatible robust-observer scope; record any inaccessible theorem rather than claim a solved gap. Admit a comparator only with an explicit implementation/license contract.
2. **Mechanism evidence:** the frozen no-fit mean/variance decomposition of all 36 exposed Q1 cases is complete, with exact original-score parity. It supports a narrower, channel-dependent explanation rather than universal mean absorption or variance inflation. If causal diagnosis is necessary, a separately specified observed/protected-history intervention can follow; the intervention must change the actual conditioning path rather than only rename coordinates. No such intervention is executed here. Neither diagnostic is confirmation or a basis for tuning against a final test.
3. **Software gate:** implement one tiny constrained tanh adapter and constrained linear control, with exact weight certificates, causal-prefix tests, reset/initialization checks, and scalar/multichannel counterexamples. The ordinary bound should be checked for arbitrary input histories and explicit recovery failures. Software checks establish implementation only.
4. **Normal feasibility pilot proposal:** one CPU thread; hidden width8; `κ∈{0.25,0.5,0.75}`, `ρ∈{0.25,0.75}`, one pilot seed17; six finite candidate fits plus constrained AR and direct-reference controls. Use one common, explicit normal fit/development contract. Old exposed populations are development, not fresh confirmation. Hard proposed caps for the **entire pilot including common-reference fitting and controls**:120 seconds wall,90 CPU-seconds,1GiB peak RSS,50MiB total outputs. These are budget caps, not measured runtime estimates; a concrete pilot runner/admission must estimate cost before any longer study. No automatic extension if the cap is hit.
5. **Selection rule:** preserve all configurations. Use normal development only; a predeclared empirical radius proxy `(E_dev+τ_dev*s_max)/(1−κ)` and per-task normal errors can screen whether useful sensitivity survives. Fix the definitions and compare with the best equally selected linear control before running. Reserve independent final normal calibration. This proxy is selection-optimistic and must never be labelled a deterministic deployment certificate.
6. **Stop condition:** do not advance a nonlinear candidate if a constrained linear/reference control matches its normal tradeoff, the bound is vacuous at the operational tolerance, the actual code violates the gain contract, or the close-method distinction collapses. Do not replace a failure with a new success criterion.
7. **Fresh confirmation only after admission:** freeze held-out task/plant/sensing conditions, primary comparator, meaningful numerical effect and noninferiority costs before generating attack outcomes. Require fewer missed sustained-deviation points at a matched benign operating point, or fewer benign alarms at fixed required sustained sensitivity, with delay and return behavior explicitly bounded. Choose one primary direction before exposure; do not select whichever wins. Retain normal changes, brief deviations, onset overshoots, oscillations, recrossings, dropout/noise and mismatch cases. Random seeds/windows are not independent robots.

The outcome of a successful pilot would be feasibility, not novelty. A successful fresh synthetic campaign would still not establish independent real-world cybersecurity generalization.

## Evidence and publication boundary

Original CASPER evidence is exposed. Original voraus-AD remains a possible separate physical-fault/normal-model track after feature/split admission; it cannot be relabelled as cyberattack/recovery evidence. FactoryNet has only partial metadata admission and possible source overlap. The current protected-intent/paired-return assumptions are clearest in the explicitly synthetic simulator, not yet demonstrated on an independent real cyber-recovery dataset.

Keep the original selected paper title, v1.7 PDF, author actions and journal hold. Do not write the proposed method into the manuscript as an achieved result. A future original paper requires exact prior-art distinction, successful measured benefit beyond the strongest simple controls, suitable independent evidence and human author review.

## Review provenance

The root performed source investigation and candidate synthesis. Three parallel AI agents separately reviewed close robotic-security prior art, mathematical/statistical alternatives, and local code/identifiability. The mechanism agent then challenged the precise proposed parameterization. The agents shared session context and received focused follow-ups; this is separate AI execution, not blinded human peer review. `CANDIDATE_CHALLENGE.md` records the objections. Main dispositions: retain the linear/saturation controls; constrain scale as well as mean; restrict the plateau theorem; separate empirical calibration from physical guarantees; keep final-version novelty unresolved. No external model provider was used.
