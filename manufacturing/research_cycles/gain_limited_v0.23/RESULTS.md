# Gain-limited correction: completed normal-only pilot

24 October 2026. The single frozen pilot completed all33methods, nine40epoch neural fits and ten linear fits on admitted synthetic normal operation. **The predeclared advancement gate failed.** No calibration, new simulation, attack evaluation or scientific retry followed. Independent saved-result review passed 1,643 main checks and 41 supplemental checks, with the same failed scientific decision; see `INDEPENDENT_RESULT_REVIEW.md`.

## Decision

The selected nonlinear candidate is `tanh_k0.25_r0.25`. Its cap-aware empirical radius is 3.695331727, versus 3.409818803 for the selected strongest simple control, `direct_reference`: **8.37% worse**, whereas the frozen criterion required at least5% improvement.

Its pooled normalized RMSE improves 11.06% against that direct reference (0.103372809 versus 0.116228148), but the same-budget constrained FIR `fir_k0.25` achieves 0.087016931. The candidate is 18.80% worse on RMSE than that linear control, so the second relevant requirement also fails. The same-budget radius comparison favors the candidate, but does not override these failures.

The selected candidate has no late-training underfit flag under the frozen epoch31→40 rule. The kappa.75/rho.25 candidate is flagged; this flag is recorded for every neural fit. Forty epochs and this diagnostic do not establish global optimization. The result rejects advancement of the configured candidate on these normal populations; it is not a universal impossibility result about every nonlinear predictor.

All six constrained neural candidates have worse cap-aware radius than the direct reference. Each is also strictly worse on **both** pooled RMSE and cap-aware radius than the saturated FIR control with the same declared amplitude-cap budget. At caps .25/.5/.75, the saturated controls' radius/RMSE pairs are3.416711/.082472,3.498161/.069022 and3.637458/.058067. The tanh certificates have negligible inward floating-point slack below the shared declared caps; this is a matched-cap-budget comparison, not a claim of byte-identical cap values. The independently checked cap-.25 saturated FIR alone also dominates all six candidates on these two quantities. All six candidate primary radii use the amplitude-cap bound because it is tighter here than the gain-only bound. These descriptive comparisons preserve the original two failed gate clauses.

The useful measured effect is a reduction in ordinary prediction error, accompanied by insufficient error reduction to compensate for the permitted observation correction in the sensitivity proxy. The familiar conditional inequality remains mathematically valid; it is not a new theorem or a demonstrated useful new cyberattack detector.

## Frozen gates

| Clause | Result |
|---|---|
| all_conditions_within_5pct | Pass |
| all_episodes_within_5pct | Pass |
| complete_roster | Pass |
| linear_solvers_converged | Pass |
| radius_5pct | Fail |
| rmse_2pct | Pass |
| same_budget_fir_radius_lower | Pass |
| same_budget_fir_rmse_not_higher | Fail |

All eight execution/source/test/resource clauses pass. Ten linear fits satisfy the projected-gradient convergence criterion; their complete iteration counts and optimality-residual diagnostics are retained. Resource completion does not turn the scientific gate into a pass.

## Complete method roster

Radius is the minimum of the valid gain and amplitude-cap proxies, evaluated with actual certified norms and the same exposed normal-development residual maximum/99th-percentile threshold. It is an empirical selection proxy, **not** an operational guarantee or an independently calibrated physical threshold. `—` means no corresponding finite certificate. RMSE uses the same4training-normalized channels and all9,900eligible M13 points.

| Method | Certified K | Cap C | Empirical radius | RMSE | Late-training flag |
|---|---:|---:|---:|---:|---|
| direct_reference | 0.000000 | 0.000000 | 3.409819 | 0.116228 | — |
| context_r0.25 | 0.000000 | 0.000000 | 3.417812 | 0.117194 | False |
| context_r0.75 | 0.000000 | 0.000000 | 3.418117 | 0.117146 | False |
| tanh_k0.25_r0.25 | 0.249999 | 0.250000 | 3.695332 | 0.103373 | False |
| tanh_k0.25_r0.75 | 0.249999 | 0.250000 | 3.786608 | 0.107018 | False |
| tanh_k0.5_r0.25 | 0.499999 | 0.500000 | 4.036798 | 0.092446 | False |
| tanh_k0.5_r0.75 | 0.499998 | 0.500000 | 4.189499 | 0.098459 | False |
| tanh_k0.75_r0.25 | 0.749998 | 0.749999 | 4.373291 | 0.083709 | True |
| tanh_k0.75_r0.75 | 0.749996 | 0.749999 | 4.606708 | 0.091073 | False |
| unconstrained_tanh | 6.379820 | 2.587064 | 6.432788 | 0.040475 | True |
| fir_k0.25 | 0.250000 | — | 3.731239 | 0.087017 | — |
| fir_k0.5 | 0.500000 | — | 4.410876 | 0.059988 | — |
| fir_k0.75 | 0.750000 | — | 6.461561 | 0.037311 | — |
| context_r0.25_fir_k0.25 | 0.250000 | — | 3.731781 | 0.087007 | — |
| context_r0.25_fir_k0.5 | 0.500000 | — | 4.416480 | 0.059971 | — |
| context_r0.25_fir_k0.75 | 0.750000 | — | 6.461540 | 0.037250 | — |
| context_r0.75_fir_k0.25 | 0.250000 | — | 3.731791 | 0.087007 | — |
| context_r0.75_fir_k0.5 | 0.500000 | — | 4.416945 | 0.059971 | — |
| context_r0.75_fir_k0.75 | 0.750000 | — | 6.461560 | 0.037249 | — |
| unconstrained_fir | 1.693799 | — | — | 0.026939 | — |
| saturated_fir_cap0.25 | 1.693799 | 0.250000 | 3.416711 | 0.082472 | — |
| saturated_fir_cap0.5 | 1.693799 | 0.500000 | 3.498161 | 0.069022 | — |
| saturated_fir_cap0.75 | 1.693799 | 0.750000 | 3.637458 | 0.058067 | — |
| leaky_k0.25_r0.25 | 0.250000 | — | 3.846252 | 0.088432 | — |
| leaky_k0.25_r0.75 | 0.250000 | — | 3.997862 | 0.091762 | — |
| leaky_k0.5_r0.25 | 0.500000 | — | 4.542231 | 0.061615 | — |
| leaky_k0.5_r0.75 | 0.500000 | — | 5.082658 | 0.069441 | — |
| leaky_k0.75_r0.25 | 0.750000 | — | 6.729156 | 0.037910 | — |
| leaky_k0.75_r0.75 | 0.750000 | — | 8.890483 | 0.052101 | — |
| kf_ratio0.01 | 1.000000 | — | — | 0.072175 | — |
| kf_ratio0.1 | 1.000000 | — | — | 0.043984 | — |
| kf_ratio1.0 | 1.000000 | — | — | 0.029287 | — |
| kf_ratio10.0 | 1.000000 | — | — | 0.025881 | — |

## Data, cost and limitations

- Fit: nine existing Q1 K13 normal/authorized-change episodes,9,900eligible observations. Development: nine M13 episodes,9,900eligible observations. Three noise seeds are not independent robots. All data were previously exposed development; L13 and physical-data/test signals remained closed.
- One common command-only FIR was fitted on the same training rows as the adapters/controls. Fixed training normalization, command context, clean zero initialization and scale1 were shared. Exact method and episode ordering, common normalized inputs/reference/context, model weights, development predictions/residuals and every epoch history are saved.
- Actual cost: 5.695969seconds wall; 4.809537CPU seconds; 292,421,632bytes sampled RSS; 23,689,059bytes before parent completion receipts. Caps120s wall/90CPU/1GiB/50MiB all held. The conservative79.33CPU estimate substantially overpredicted this small run: its short three-epoch timing included optimizer/setup overhead, which the extrapolation repeatedly charged, plus fixed allowance and50% margin. It is not a hardware-performance claim, consumed training budget or reason to extend the frozen schedule after outcomes.
- Sixteen synthetic tests passed before the independent release and41-input/source/runtime freeze. The reviewer separately reran those tests. A no-fit reload of all nine neural models then passed146checks and reproduced all388,800saved development correction values exactly; tensor and non-pickle NumPy weights agree. This reload reuses the implementation and is not the separate independent reviewer verification. That audit reconstructed all 33 predictors without importing pilot helpers, recomputed all metrics and gates, and verified all 41 frozen bindings and 88 sealed run outputs. Its nine NumPy neural replays differed from saved Torch corrections by at most 2.384185791015625e-7. See `REVIEWER_VERIFICATION.json` (1,643 checks) and `REVIEWER_DOMINANCE_V2.json` (41 supplemental checks); repeated checks are not independent research evidence units. These checks verify implementation and arithmetic, not benchmark superiority.
- No physically sourced tolerance was available, so no normalized value was invented as an operational safety threshold. A lower empirical radius alone would not establish physical detection, recovery, originality or journal readiness.
- The existing simple virtual plant may not justify nonlinear adaptation. Do not manufacture a harder simulator or choose a different primary objective after seeing this failure. No fresh attack campaign is admitted for this candidate by these results.

Working directory `/Users/matrixusman/CUI/DigitalTwin/manufacturing`:

```sh
python3 research_cycles/gain_limited_v0.23/freeze.py
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 .venv-analysis-v022/bin/python research_cycles/gain_limited_v0.23/run.py
```

Freeze SHA-256: `f5234ec8563babca1fa97305d5ca38c05390c14e3d6f0d1ba3b0b4a07886141b`. Results are under ignored `local/gain_limited_v0.23/normal_001/`. `FINAL_ADMISSION.json` combines the scientific and execution checks; `admission.json` contains worker scientific clauses only. The source protocol/config, input manifest, synthetic tests, runtime estimate and independent release are preserved in this study directory. Prior manuscripts and all older studies remain unchanged.
