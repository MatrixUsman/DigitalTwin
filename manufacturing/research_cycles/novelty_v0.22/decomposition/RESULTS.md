# RAPT score decomposition: completed exploratory diagnostic

24 October 2026. All 36 exposed Q1 episodes were replayed once with the original selected model and unchanged scoring inputs. This is arithmetic decomposition of existing findings, not a new detector, fresh confirmation or causal identification.

## Main finding

The simple statement that a persistent offset always makes its own position-prediction error shrink is unsupported. In L19 persistent-offset episodes, q1 prediction-error log magnitude rises while v1 prediction-error log magnitude falls. In S19 persistent-offset episodes, q1 error shrinks strongly, while its predicted variance also shrinks and therefore partly opposes the score reduction. Different channels and tasks behave differently.

Across the three seed realizations, L19 persistent q1 changes are +1.9838 in mean log squared error and +0.0736 from the negative log-variance term, giving +2.0574 in mean log score. Its v1 terms are −3.2055 and −0.1430, giving −3.3484. For S19 persistent q1, terms are −3.4826 and +0.2897, giving −3.1929. These figures describe first-to-last quarter changes in per-channel geometric score behavior; they do not add to the detector’s max-over-gates risk or identify why the model made those predictions.

The dominant numerical contribution to these particular declining channels is the squared-error term, rather than variance inflation alone. S19 v2 is different: both falling error and rising variance contribute. No blanket variance or recurrent-memory explanation is established. The protected versus observed-history intervention has not been executed.

## Execution and verification

- One inference attempt completed: 4.823758 seconds wall, 3.889797 CPU, 410,664,960 bytes sampled RSS and 7,933,849 output bytes before the supervisor receipt. All declared caps held.
- Complete population: 36 episodes, 129,600 rows and 126,000 eligible rows; one fitted Q1/seed17 epoch14 model. No new trajectory, training, calibration or original physical-data/test observation.
- All 518,400 saved per-channel score values equal the v0.21 replay values exactly. Thus this added visibility into means/variances did not change the detector result.
- Six synthetic tests passed before freeze; 295 frozen source/input/runtime identities are retained. Separate verification without model inference or core summary helpers passed 5,480 checks. Maximum per-element log-identity roundoff was 1.26e-07. These counts are arithmetic checks, not independent experiments.
- Saved inference arrays include normalized-unit means, log variances, squared errors before variance division, original standardized scores, defined-row and eligible-row masks. The first row is undefined/padded and excluded.
- The environment required a documented project-local bridge because the original forecast interpreter symlink points to a removed Homebrew Cellar location. The old environment remained unchanged. A sandboxed synthetic test aborted on OpenMP shared memory before input/model access; its failed receipt/log are preserved. Shared-memory-enabled tests passed. The scientific inference run had no failed attempt or retry.

## Complete task/condition/channel table

Each row averages the last-quarter minus first-quarter mean-log changes across three noise-seed episodes. The first term measures squared-error change; the second is **minus** log-variance change; their sum is log-score change up to float32 rounding. No zero squared errors/scores were excluded in these summaries. Brief-offset quarter windows have only three points for L19 and two for S19, so they are highly local diagnostics. Normal/authorized-change quarters span the full eligible benign episode and are not identical-phase controls for intervention quarters. Complete denominators are retained in `STRATA.json` and each episode summary.

| Task | Condition | Channel | Δ log squared error | −Δ log variance | Δ log score |
|---|---|---|---:|---:|---:|
| L19 | normal | q1 | -0.0889 | -0.0021 | -0.0910 |
| L19 | normal | q2 | +0.0449 | -0.0072 | +0.0377 |
| L19 | normal | v1 | +0.2087 | -0.0021 | +0.2067 |
| L19 | normal | v2 | -0.0164 | +0.0077 | -0.0087 |
| L19 | authorized_changes | q1 | -0.2386 | -0.0042 | -0.2427 |
| L19 | authorized_changes | q2 | +0.0216 | -0.0090 | +0.0127 |
| L19 | authorized_changes | v1 | +0.2504 | +0.0024 | +0.2529 |
| L19 | authorized_changes | v2 | -0.0606 | +0.0199 | -0.0406 |
| L19 | brief_offset | q1 | -1.2254 | -0.1588 | -1.3842 |
| L19 | brief_offset | q2 | -1.2031 | -0.1165 | -1.3197 |
| L19 | brief_offset | v1 | +1.6744 | -0.0387 | +1.6358 |
| L19 | brief_offset | v2 | -0.2663 | -0.0248 | -0.2911 |
| L19 | persistent_offset | q1 | +1.9838 | +0.0736 | +2.0574 |
| L19 | persistent_offset | q2 | -1.1050 | +0.0568 | -1.0482 |
| L19 | persistent_offset | v1 | -3.2055 | -0.1430 | -3.3484 |
| L19 | persistent_offset | v2 | +1.0476 | +0.1174 | +1.1651 |
| L19 | hold | q1 | -1.1919 | -0.0158 | -1.2077 |
| L19 | hold | q2 | +0.3247 | -0.0295 | +0.2953 |
| L19 | hold | v1 | -0.3414 | +0.0048 | -0.3365 |
| L19 | hold | v2 | +0.2604 | +0.0142 | +0.2746 |
| L19 | slow | q1 | +0.8703 | +0.1604 | +1.0307 |
| L19 | slow | q2 | -0.3069 | -0.1422 | -0.4491 |
| L19 | slow | v1 | +2.5302 | -0.1794 | +2.3509 |
| L19 | slow | v2 | -0.1340 | -0.0006 | -0.1346 |
| S19 | normal | q1 | +0.1582 | +0.0075 | +0.1657 |
| S19 | normal | q2 | -0.0020 | +0.0083 | +0.0063 |
| S19 | normal | v1 | +0.0463 | -0.0035 | +0.0429 |
| S19 | normal | v2 | -0.1388 | -0.0133 | -0.1521 |
| S19 | authorized_changes | q1 | -0.0615 | +0.0080 | -0.0534 |
| S19 | authorized_changes | q2 | +0.1335 | -0.0007 | +0.1328 |
| S19 | authorized_changes | v1 | -0.2265 | +0.0138 | -0.2127 |
| S19 | authorized_changes | v2 | -0.0782 | -0.0118 | -0.0900 |
| S19 | brief_offset | q1 | -0.8778 | -0.0348 | -0.9126 |
| S19 | brief_offset | q2 | -0.6586 | +0.1296 | -0.5290 |
| S19 | brief_offset | v1 | +2.7523 | -0.3923 | +2.3599 |
| S19 | brief_offset | v2 | -0.3167 | +0.1099 | -0.2068 |
| S19 | persistent_offset | q1 | -3.4826 | +0.2897 | -3.1929 |
| S19 | persistent_offset | q2 | +0.0278 | -0.0094 | +0.0184 |
| S19 | persistent_offset | v1 | +0.0213 | +0.1797 | +0.2010 |
| S19 | persistent_offset | v2 | -2.2149 | -0.6445 | -2.8594 |
| S19 | hold | q1 | +1.5555 | +0.0133 | +1.5688 |
| S19 | hold | q2 | +0.6430 | +0.0117 | +0.6547 |
| S19 | hold | v1 | +2.3198 | -0.0131 | +2.3068 |
| S19 | hold | v2 | -0.1453 | -0.0198 | -0.1651 |
| S19 | slow | q1 | +0.5472 | -0.1108 | +0.4364 |
| S19 | slow | q2 | -0.4408 | -0.0404 | -0.4812 |
| S19 | slow | v1 | +5.8701 | +0.2214 | +6.0915 |
| S19 | slow | v2 | -1.9333 | -0.2783 | -2.2116 |

## Interpretation and next boundary

The observation-dependent mean and scale remain distinct candidate contributors, but their causal roles cannot be inferred from arithmetic score decomposition alone. The present computation cannot determine whether changes reflect immediate prior observations, recurrent memory, command/phase structure, model mismatch or task transfer. It also does not compare the proposed bounded-adaptation candidate with a simple reference/AR/KF control. The original failed candidate criteria and journal hold remain unchanged.

No attack truth/counterfactual/state member was opened by this worker. Schedule boundaries were taken from the already frozen v0.19 configuration. All cases and channels are retained. The unchanged original calibration/thresholds are inherited in the freeze, but no new threshold or preferred mode was chosen.

From `/Users/matrixusman/CUI/DigitalTwin/manufacturing`:

```sh
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 .venv-analysis-v022/bin/python research_cycles/novelty_v0.22/decomposition/run.py
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 .venv-analysis-v022/bin/python research_cycles/novelty_v0.22/decomposition/verify.py
```

Artifacts: `PROTOCOL.md`, `FREEZE.json`, `TEST_RECEIPT.json`, `RUNTIME_BRIDGE.json`, `VERIFICATION.json`, `STRATA.json` and ignored `local/novelty_v0.22/decomposition_001/` containing access/provenance, summaries, every saved array, unchanged-score parity and resource receipts. The bridge is a compatibility repair, not a fresh portable dependency installation.
