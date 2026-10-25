# Independent saved-artifact audit

24 October 2026. Manufacturing only. Reviewer: separate `recovery_theory` AI agent with shared context, not blinded human peer review. The pre-run review and release remain unchanged. This audit imports no pilot/helper module, performs no training or optimization, and opens no original normal, calibration or test signal arrays. It reads the saved normalized inputs, weights, predictions, metadata and receipts of `local/gain_limited_v0.23/normal_001`.

**The execution is valid and the predeclared scientific advancement gate fails.** The independently selected nonlinear candidate is `tanh_k0.25_r0.25`; its radius is worse than the direct reference, and its RMSE is worse than the same-budget constrained FIR. This configured candidate does not advance. No fresh attack or final calibration was run or admitted.

## What was independently checked

`reviewer_verify23.py` passed **1,643 checks**, covering all 41 frozen bindings, all 88 sealed outputs, the 33-method roster and nine fit/nine development episodes. Every method has 9,900 eligible development rows. All 1,425,600 saved development residual scalars, including warmup, have the exact saved observation-minus-reference-minus-correction identity.

The audit reconstructed the common command-only reference and causal command context from saved normalized inputs; checked training normalization and the reference's ridge normal equations without refitting; recomputed every final neural/FIR gain and cap from non-pickle weights; verified all 40 epoch records and each constrained epoch's reported norms; and independently replayed all 33 predictors. Nine neural models were implemented separately in NumPy from the equations. Their largest difference from the saved float32 Torch corrections was **2.384185791015625e-7**, below the declared comparison tolerance. No detector implementation or report helper was imported. The ten linear fits satisfy independently calculated convex stationarity checks; the largest projected-gradient residual was **9.945628575388112e-8**, below the frozen 1e-7 tolerance. The independent projection used bisection rather than the implementation's sorting algorithm.

Every threshold rank, empirical maximum, radius component, pooled/episode/condition RMSE, finite-roster selection and scientific/execution clause was recomputed. RMSE sums use Python `math.fsum`, separate from the implementation's NumPy mean reduction. The normal-only access record has the expected 18 paths and only `measurements`, `commands` and `valid` members. This checks the saved access declaration and code path; it is not an operating-system data-access audit.

## Reproduced outcome

| Method | Empirical primary radius | Normalized pooled RMSE | Role |
|---|---:|---:|---|
| Direct reference | 3.409818803 | 0.116228148 | Best simple comparator under frozen radius-first selection |
| Tanh, kappa .25, rho .25 | 3.695331727 | 0.103372809 | Selected candidate |
| Constrained FIR, kappa .25 | 3.731238652 | 0.087016931 | Best same-budget FIR |
| Saturated FIR, cap .25 | 3.416710767 | 0.082471783 | Prespecified ordinary control; descriptive comparison below |

The selected candidate's radius is **8.3733% worse** than the direct reference, so the required 5% reduction fails. Its RMSE is **11.0604% lower** than the direct reference, satisfying the required 2% improvement; all episode and condition noninferiority checks pass. Its radius is slightly lower than the same-budget FIR's, but its RMSE is higher, so the required same-budget RMSE condition fails. The complete roster and all linear-convergence checks pass. The final decision is false with exactly these two failed scientific clauses; no criterion was changed after execution.

The selected candidate's predeclared underfit flag is false: its training-window loss improves **0.39868%** from epochs31 to40, below the 1% flag. Two of nine neural fits are flagged: `tanh_k0.75_r0.25` (1.13640%) and `unconstrained_tanh` (23.66912%). A false flag is not a proof of a global optimum. The conclusion concerns this fixed model/training/data configuration, not every possible nonlinear architecture or training schedule.

## Separate post-gate descriptive check

The root requested an additional comparison after the frozen gate had already failed. `reviewer_dominance23_v2.py` separately passed **41 checks**, recomputing the saturated cap-.25 control and all six candidate metrics from saved residuals and actual weights. The ordinary saturated FIR has a **strictly lower primary radius and pooled RMSE than every one of the six neural candidates**. This is a descriptive finding on exposed synthetic development, not a new selection criterion, statistical superiority claim or causal explanation.

All six candidates' primary radius is supplied by their amplitude-cap bound, which is tighter here than their gain-only bound. For the selected candidate, the cap radius is 3.695331727 versus gain-only radius 4.260439805. The saturated FIR's unconstrained history gain is 1.693798917; it has no finite gain-only plateau radius, but its .25 amplitude cap supplies radius 3.416710767. Thus saturation already supplies the more informative sufficient bound in this observed range, and the constrained nonlinear models have not demonstrated added practical value on the declared quantities. This does not establish that a gain restriction is useless under every operating condition.

The original supplemental receipt `REVIEWER_DOMINANCE.json` is preserved. Its field `verified_gate_unchanged:false` was an ambiguous metadata label intended to record the failed primary gate. The V2 script/receipt explicitly correct that field to `verified_gate_unchanged:true` and `verified_primary_gate_passed:false`; all numerical findings and the 41 checks are unchanged. Use **REVIEWER_DOMINANCE_V2.json** for current citation. Report **1,643 main checks plus 41 supplemental checks** separately: some quantities are deliberately recomputed in both, and repeated supplemental execution does not add evidence units.

## Execution and reproducibility

One scientific attempt completed in **5.695969375 seconds wall** and **4.809537 process CPU seconds**. The supervisor observed **292,421,632 bytes peak sampled RSS** over 23 samples; the worker reports lifetime peak RSS 292,405,248 bytes. The audit measured **23,690,990 bytes** in the run directory after final metadata. All are within the frozen limits. Sampled RSS is not an instantaneous memory proof. The conservative synthetic timing estimate was prospective; its overestimate is not grounds to extend this failed run.

Commands, from the manufacturing directory:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv-analysis-v022/bin/python research_cycles/gain_limited_v0.23/reviewer_verify23.py
PYTHONDONTWRITEBYTECODE=1 .venv-analysis-v022/bin/python research_cycles/gain_limited_v0.23/reviewer_dominance23_v2.py
```

Each verification receipt uses exclusive creation and should not be overwritten by a rerun. Exact identities:

| Artifact | SHA-256 |
|---|---|
| `reviewer_verify23.py` | `5b5c5c5b4227c2a68ee046e499f8f58e0e1fe2651ef19815b511b48be5383e0a` |
| `REVIEWER_VERIFICATION.json` | `3541c6e87e858cfffaf2b9902af7f4f2851b8124a53be68adeed4a20ad32c602` |
| `reviewer_dominance23_v2.py` | `c99e9aa01732d598b89754ad817d058493d7689af6878e77865a709184b8fb3e` |
| `REVIEWER_DOMINANCE_V2.json` | `1ccd7062c6810f2521a9c939bc726a0c2f989f63f689b6b0d442ecb61c4f3f01` |

## Interpretation limits

The arithmetic/code audit passes; the scientific gate fails. The normal development population is exposed and synthetic, and seeds are not independent robots. The empirical radius is not a future deterministic residual envelope, a physical tolerance, or a measured attack-detection result. Stored-weight norm calculations concern the corresponding real-arithmetic network; numerical replay is not a machine-arithmetic proof. The study neither establishes novelty nor supports journal submission of this candidate as a successful original method. Preserve the failure and the earlier journal hold; manuscript claims must reflect these limits.
