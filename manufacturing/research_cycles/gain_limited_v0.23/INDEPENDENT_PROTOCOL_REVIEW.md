# Independent normal-pilot protocol review

24 October 2026. Manufacturing only. Reviewer: the separate `recovery_theory` AI agent, with shared research context. This is not blinded human peer review. Review scope is the finite normal-only `gain_limited_v0.23` pilot, not publication approval or a new scientific theorem. No scientific training, fresh test observation, or implementation modification was performed by this reviewer.

## Initial preliminary disposition (superseded by final release below)

**Preliminary mathematical/protocol review: acceptable in principle, NOT YET RELEASED TO RUN.** The complete implementation, synthetic guard tests, cost estimate and frozen file identities must be inspected before release. The root owns the scientific GO decision. This preliminary status will be superseded below only after the additional evidence is reviewed.

The reviewed draft uses only nine exposed Q1/K13 nominal episodes for fitting and nine exposed Q1/M13 nominal episodes for development, with L13 and attacks excluded. The fixed common reference, training-only normalization, causal trusted context and unit score scale are appropriate for this narrow feasibility question. Development maxima and thresholds are empirical selection quantities. They do not certify future residual bounds or false-alarm probabilities.

## Mathematical contract

For identical trusted command histories, reference, parameters and initial state, the proposed tanh model has

\[
\|\Delta a_t\|_\infty\le\|W_o\|_\infty\|W_z\|_\infty\sum_{s<t}\|W_h\|_\infty^{t-1-s}\|\delta_s\|_\infty.
\]

The certified history gain is the **actual** upper bound

\[
K=\|W_o\|_\infty\|W_z\|_\infty/(1-\|W_h\|_\infty),
\]

provided the actual recurrent norm is strictly below one. A numerical projection tolerance must not be silently omitted when evaluating this quantity. Stable state dynamics alone do not establish `K<1`. Every observation-dependent input, skip path, initializer, normalization change and scale path must be included. In this pilot, fixed train-only normalization, fixed unit scale, zero initialization and command-only context can meet that requirement; code inspection remains necessary.

The total tanh output also satisfies the paired contrast bound `||Delta a||_infinity <= 2 C`, where `C=||Wo||_infinity`, including when its command-conditioned hidden trajectory is nonzero. A shared output bias would cancel. For a linear temporal FIR, the maximum output-row absolute sum over **all** residual lags is the exact history infinity gain. Summing individual lag-matrix norms is sufficient but unnecessarily conservative. A command-only additive correction cancels under the paired comparison and contributes no observation gain or paired amplitude term.

For a constant observed displacement `D`, with earlier displacement no larger, nominal residual bounded by `E` on the evaluated interval and unit score threshold `tau`, the two sufficient radii are

\[
D_{gain}=(E+\tau)/(1-K)\quad(K<1),\qquad
D_{cap}=E+\tau+2C.
\]

Where both are valid, the smaller is valid. Crucially, a clipped linear predictor can have a finite cap radius even when its history gain is at least one. The current draft correctly applies this bound to both neural and linear controls, rather than crediting only the neural method. If one certificate is unavailable, it is omitted, not numerically assigned a favorable value. Strict exceedance requires `D` strictly larger than the selected radius. Arbitrary histories need the full fading-memory term; a larger earlier transient invalidates the simplified plateau assertion until its contribution is accounted for.

These statements are standard norm, reverse-triangle and bounded-output arguments. They do not establish originality. They concern measured normalized trajectories under common trusted intent, not attack input amplitude, unobserved physical state, physical recovery, or detection of every possible cyberattack. A legitimate unrecorded offset can be indistinguishable from an unauthorized one.

The stored-weight norm calculation certifies the corresponding real-arithmetic network. The implementation evaluates in float32; its rounding has not been enclosed with verified arithmetic. Finite synthetic perturbation checks with numerical tolerance are useful implementation checks, not a universal floating-point guarantee for arbitrarily small perturbations. Keep this distinction explicit in any manuscript claim.

## Controls and selection

The strengthened draft includes direct command-only prediction, command-only tanh, constrained FIR, command-only-tanh plus constrained FIR, leaky filters, clipped unconstrained linear correction, ordinary random-walk KF and an unconstrained same-width neural diagnostic. This addresses the key risks that an apparent gain comes only from protected-command access, nonlinear command fitting, saturation or an unnecessarily weak linear comparator.

The common reference and unit scale should remain identical across methods. Command-only tanh has observation gain zero regardless of its output norm and should not be handicapped by an unnecessary observation-gain output cap. For additive controls, use the actual observed-dependent FIR branch for `K` and any cap; do not charge the shared command branch. The same-budget FIR comparison is useful in addition to the best overall comparator.

The fixed radius-first selection rule and the 5% radius improvement, 2% pooled RMSE improvement, maximum 5% episode/condition RMSE regression, and same-budget FIR conditions form a concrete, falsifiable **normal feasibility** gate. The same selected comparator must be used for all primary comparisons. Report every method, both radius components and actual/budget norms. Missing or failed linear solver convergence must block advancement, rather than silently removing a difficult comparator. The percentages are prospective pilot design choices, not clinically/operationally established effect sizes or statistical significance thresholds.

No sourced physical tolerance has been established. The review rejected assigning an arbitrary normalized `D=0.1` a physical meaning. A pilot pass therefore cannot resolve operational nonvacuity or authorize fresh attacks automatically. Conversely, a fixed-budget failure would reject advancement of the configured pilot; it would not prove that every sufficiently trained nonlinear model is inferior.

## Outstanding pre-run checks

1. Inspect complete source for the lag direction, score-before-update, train-only transforms, context construction, observation paths, per-episode initialization, invalid-row handling and control fairness.
2. Verify actual norm projection/certificates, complete output caps, causal prefix invariance, reset behavior, scalar/multichannel perturbation checks and the linear solver convergence calculation.
3. Freeze the fixed training schedule, final-epoch checkpoint rule, all training histories and a prospective underfit flag. The initial draft used 12 epochs; a synthetic-only cost estimate subsequently supports the root's prospective increase to 40 epochs, before any admitted normal signal loading. The revised underfit flag compares epochs 31 and 40, with greater than 1% training-window loss improvement flagged. Truncated training windows introduce a state approximation; the 48-row burn-in substantially reduces it under contractivity but does not remove the need to report it. An underfit flag must narrow interpretation without changing the pass/fail threshold after results.
4. Put every gate, including the condition-level and same-budget comparisons, in the machine-readable configuration. Fix exact score rank, warmup, finite-value and invalid-row policies before reading the permitted normal values.
5. Inspect the identically shaped, explicitly synthetic runtime estimate and conservative total cost estimate. The full scientific run includes reference and control fits and is capped at 120 seconds wall, 90 CPU seconds, 1 GiB sampled RSS and 50 MiB output. Preserve a failure rather than silently retrying.
6. Bind reviewed protocol/config/source/tests and all admitted normal inputs before root GO. After execution, independently recompute saved-weight certificates, metrics, gates and selection without importing the implementation's helpers.

## Prior-art and evidence boundary

The v0.22 decision remains provisional. The parent source review identified close lower-bound antecedents, including contractive residual mappings and Lipschitz anomaly models; the final 2026 recurrent-equilibrium-network equations remain incompletely accessed. There is no theorem-led originality claim to release. Successful normal feasibility would support only further investigation of a complete method and its tradeoff, not a new journal contribution, fresh held-out performance or manuscript submission readiness.

Reviewed local evidence at this preliminary stage: `PROTOCOL.md`, `config.json`, `RUN_CONTEXT.md`, and `../novelty_v0.22/DECISION.md`. Changes prompted during review are recorded prospectively in direct coordination with the implementation agent and root. Implementation and post-run evidence are pending.

## Source review and runtime follow-up

Before scientific execution, the reviewer also inspected `models23.py`, `data23.py`, `admit_data.py`, `test_models23.py`, `pilot23.py`, `worker.py`, `run.py`, `freeze.py`, `runtime.py` and `runtime_worker.py`. The dataflow uses only permitted normal observations, protected commands and validity flags; reference, transforms and fitted weights use K13. Development is used for the declared finite model selection and recorded window losses, not gradient updates or epoch selection. The command-only controls retain unrestricted output weights. Additive FIRs operate on residuals after the frozen command-only nonlinear correction. The unconstrained FIR is included in the simple pool whenever its actual gain makes a finite radius available. The final arrays provide enough information for independent saved-output validation.

The synthetic receipt at `local/gain_limited_v0.23/synthetic_runtime_001/runtime.json` reports a 200-parameter neural model, batch shape `207 x 96 x 4`, 0.373152 CPU seconds for three training epochs, 0.009558 CPU seconds for batched full-episode inference on 18 synthetic episodes, and 0.003744 CPU seconds for four synthetic linear fits. Recalculation agrees with the declared 40-epoch full-roster estimate: 52.886953 CPU seconds before the 50% margin and 79.3304295 after it. The corresponding 60-epoch estimate is 112.9141095 CPU seconds and exceeds the cap. These are cost estimates from independent random tensors, not actual normal-data runtimes or assurance that all normal linear solves converge.

The fixture completed once in 2.02700125 seconds wall, with 290,930,688 bytes sampled peak RSS and 6,953 bytes output. Its worker CPU receipt is 0.989289 seconds. Source changes since the fixture require final identity review; increasing only the fixed iteration count is the declared prospective extrapolation.

Still pending at this follow-up: final protocol alignment with 40 epochs and epoch31-to40 flag; explicit finite-value rejection for fitted weights, histories, certificates and output streams; synthetic admission-rule boundary checks; passing final test receipt and release bindings. No normal scientific run is released by this intermediate note.

## Final pre-run disposition

**ADMITTED for the single specified normal-only feasibility pilot, subject to root GO and the mandatory source/input freeze.** This supersedes the preliminary non-release above. It is not a scientific pass, a novelty finding, an independent final evaluation, or journal approval.

The final source resolves the pending items: 40 fixed epochs and the epoch31-to40 optimization flag; finite-value rejection of weights, losses, certificates and prediction/residual populations; unrestricted output weights for command-only controls; actual-gain eligibility for the ordinary unconstrained FIR; and explicit 33-method, same-budget, per-condition, per-episode and solver gates. The final external admission combines those scientific clauses with supervisor completion, resource limits, unchanged frozen inputs, passing software tests and complete method count. `FINAL_ADMISSION.json`, rather than a worker-only scientific flag, is authoritative after execution.

The reviewer independently reran the 16 synthetic tests with the following command from the manufacturing directory; all passed, exit code 0:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv-analysis-v022/bin/python -m unittest discover -s research_cycles/gain_limited_v0.23 -p 'test_*.py' -v
```

The test body's reported duration was 0.049 seconds; shell/tool elapsed time was 0.759753458 seconds. These tests use synthetic arrays and fake selection records; they do not fit or inspect the admitted normal population. The review also checked the existing passing test receipt and final source hashes. The prospective 40-epoch choice remains supported by the synthetic cost extrapolation, with hard supervision decisive.

Exact reviewed bindings and release disposition are recorded in `REVIEW_RELEASE.json`. The reviewer writes that receipt under the root's explicit expanded scope. No implementation was changed by this reviewer. Preserve this pre-run review and its release unchanged after the freeze; subsequent saved-output findings belong to a separate independent audit.
