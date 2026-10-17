# Empirical motion-observer validation — completed v0.1

## Material Passport

- Project/owner: manufacturing / Haiqa Mushtaq; operator: Codex assistant; 17 October 2026, Asia/Karachi.
- Scope: the user's authorized design, implementation and bounded normal-only validation of a stateful motion observer and matched correction-evidence ablation.
- Evidence: one completed real-data attempt, 254 passing synthetic tests, an internal scientific review and 48/48 independent saved-artifact checks. The reviewers are agents in the same assistant team, not external or blinded peer reviewers.
- Workflow: shared academic-research-suite, scoped experiment design/execution/verification. No paid service, third-party model call, package installation, publishing, calibration or final evaluation.
- Frozen declaration: [plan](OBSERVER_VALIDATION_PLAN.md), [configuration](../configs/casper_right_arm_observer_v0.1.json). Current aggregate evidence: [run summary](../experiments/OBSERVER_V0.1_SUMMARY.json), [fitted-artifact registry](../experiments/OBSERVER_ARTIFACTS_V0.1.json).

## Decision

The model has an explicit state, a physically interpretable empirical reference, prospective joint prediction and measurement-driven synchronization. All seven predeclared internal checks passed on the permitted normal data. We can proceed with the narrower designation **empirical phase-based motion observer** for this recording.

This is not a validated physical digital twin, a reproduced paper baseline, an established novel method or evidence of attack-detection improvement. The strongest limitation is visible in the ordinary controls: the observer's one-step standardized MSE is **0.338911**, compared with **0.002094** for the selected AR(4), about **162 times higher**. We retain that result. Useful synchronization and recurrence do not establish predictive superiority.

The existing template values and period were fitted on training, and its 32-bin configuration was selected on the same normal-development partition used here. These are development findings with disclosed reuse, not independent confirmation. No result selected a new configuration, changed a check or triggered a retry.

## What was built

The observer maintains 32 phase weights: its current uncertainty about where the arm lies within a nominal cycle. Each phase bin maps to six joint positions and six joint velocities. The fitted period is approximately **38 seconds**; the grid spacing is approximately **1.1875 seconds**. The nominal transition advances the distribution with actual elapsed time and a fixed 0.02/s uniform-mixing rate. Both interpolation and mixing broaden the distribution in the absence of measurements.

At each observation it predicts from the previous state, computes the prediction residual, forms a tentative measurement correction, emits the score, then commits the corrected state. Current measurements cannot change their own prospective prediction. At a gap or partition boundary, the phase distribution resets and all variants receive the same 1,528-observation warmup. Labels and attack boundaries do not reach the model.

The reference, transformation, period, bandwidth and score scales stay fixed during development. State synchronization changes phase weights; it does not adapt those fitted parameters. The RBF pseudo-likelihood bandwidth was fitted only on eligible training data as mean nearest-bin standardized MSE: **0.3309050380943476**. It is not an estimated, calibrated physical noise variance.

The principal pair uses the very same observer proposal and committed trajectory:

- **Residual only:** `R / 0.3394252231379215`.
- **Residual plus correction evidence:** `R / 0.3394252231379215 + C / 0.0018556470655418222`.

Here `R` is the prospective 12-channel standardized MSE, and `C` is the natural-log Jensen–Shannon divergence between prior and tentative posterior phase weights. Both denominators are training means, fitted on 536,946 eligible endpoints. The comparison removes the correction-evidence term only; the residual-only variant still uses nominal progression to predict. Correction evidence measures synchronization effort, not independently verified maliciousness or signed speed error. Whether adding it helps detection is **unmeasured**.

Two additional variants share the same mapping and warmup: unconstrained following uses likelihood-only correction after warmup; free-running stops assimilating measurements after warmup. The selected AR(4), persistence and training-mean predictors provide ordinary forecasting comparisons. Implementations: [observer core](../src/mfg_twin/observer.py), [study coordinator](../src/mfg_twin/observer_study.py), [bounded entry point](../scripts/run_observer_study.py).

## Normal-data results

All errors below are mean squared errors after the same training-only channel standardization. They are prediction diagnostics, not attack F1 scores. Every one-step method used the same **160,472** eligible development endpoints.

| Predictor/update policy | One-step MSE | Nominal 1-second MSE | Nominal 5-second MSE |
|---|---:|---:|---:|
| Synchronized observer | 0.338911 | 0.427053 | 0.529248 |
| Unconstrained following | 0.471257 | 0.602360 | 0.802438 |
| Free-running observer | 0.997809 | 1.022183 | 1.022573 |
| Persistence | 0.006335 | 0.964283 | 2.149228 |
| Fixed training mean | 0.998754 | 1.023089 | 1.023547 |
| Selected AR(4), ridge 0.001 | **0.002094** | Not implemented | Not implemented |

Longer-horizon forecasts were fixed at the origin and propagated without intervening measurements. All methods within a horizon share exactly the same matched targets. Of 8,024 issued diagnostic origins, **8,023** one-second targets and **8,019** five-second targets matched; one and five respectively were censored at the partition end. Actual mean horizons were **1.009890** and **5.009877** seconds; maxima were about 1.05 and 5.05 seconds, within the predeclared 0.075-second tolerance. Floating accumulated-time comparisons near equality can select the next 20 Hz observation. No post-result rematching occurred. AR time-horizon forecasts are unavailable because no irregular-time recursive rollout was admitted; this is not evidence that AR would perform poorly at those horizons.

The earlier deterministic fixed-template control reported 0.374223 one-step MSE. That is contextual evidence from the prior control study, not a newly rerun matched observer policy. It remains relevant: the new free-running distribution approaches uniform weights (mean normalized entropy **0.999233**, resultant **0.003557**) under the declared mixing and interpolation. Its poor error therefore partly reflects that transition rule. Beating this free-running variant does not prove that every fixed reference fails or that synchronization always improves prediction.

### Recurrence and nominal progression

| Lag | Training MSE | Development MSE |
|---|---:|---:|
| 19 s, `0.5T` | 2.207377 | 2.261469 |
| 34.2 s, `0.9T` | 2.058596 | 2.092043 |
| 38 s, `T` | **0.000645** | **0.000606** |
| 41.8 s, `1.1T` | 2.059477 | 2.096600 |

All four lags used common paired populations: **26,765** training origins and **7,982** development origins. The 83/42 unmatched origins lacked an eligible past endpoint near a segment's start; they do not reduce primary score coverage. Native history was retained at the source rate. The nominal-period discrepancy was lower than every predeclared alternative in both partitions, supporting this recording's repetitive-motion reference.

Across **8,023** adjacent development diagnostic pairs, synchronized MAP phase advanced by a mean **0.842204 bins per approximately one second**, against nominal progression of approximately **0.842105 bins**. The mean deviation was 0.0000984 bins. No backward or greater-than-quarter-cycle jumps were observed at these sampled origins. Phase was unchanged in **23.62%** of comparisons; this is compatible with a 1.1875-second bin observed about once per second. Every bin was visited. These are ordered model-state progression diagnostics, not ground-truth phase accuracy, measured physical speed or a guarantee that no jump occurred between diagnostic samples.

### Kinematic correspondence

The circular central derivative of reference joint positions agrees substantially better with reference velocity than a training-mean-velocity predictor: aggregate standardized discrepancy **0.005429 versus 0.252794**. The comparison is internal to the fitted reference and does not validate robot forces, commands or closed-loop mechanics.

| Joint | Reference derivative/velocity MSE, `(rad/s)^2` | Error divided by mean-velocity baseline error |
|---|---:|---:|
| 1 | 0.000527226 | 0.009322 |
| 2 | 0.000105976 | 0.018781 |
| 3 | 0.000141830 | 0.029735 |
| 4 | 0.000550662 | 0.018890 |
| 5 | 0.000001392 | 0.036979 |
| 6 | 0.000084141 | 0.036534 |

A separate recorded-signal diagnostic compares backward position differences divided by actual elapsed time with the current recorded velocity, without angle unwrapping. On all eligible development targets, standardized discrepancy was **0.003362**, versus **0.998641** for the training-mean velocity. This supports the local position/velocity correspondence assumed here; sensor truthfulness still comes from the threat-model assumption, not this arithmetic check.

### Ambiguity and uncertainty

Across **8,024** sampled development states, the synchronized observer's mean normalized phase entropy was **0.433220**, circular resultant **0.922955**, maximum bin mass **0.453282**, and greatest competing-bin mass outside MAP±1 **0.073472**. The predeclared descriptive ambiguity flag—entropy above 0.5 or resultant below 0.5—occurred in **53.12%** of these states. High circular concentration and uncertainty across several neighboring bins can coexist.

The full posterior remains in the model. All twelve mapped physical-unit phase-mixture variances and bin occupancies are retained in the aggregate summary, along with every channel's prediction error and all auxiliary variants. These quantities describe this estimator's uncertainty; there is no calibrated confidence interval or independent phase label. An empirical average across incompatible phases may not lie on a feasible physical trajectory. The coarse competing-bin summary is not a full modal decomposition.

## Checks, execution and provenance

All **seven** declared internal checks passed: recurrence on training, recurrence on development, prediction below the training mean at one step/one second/five seconds, synchronization benefit at at least one declared horizon, and aggregate reference kinematic correspondence. These deliberately limited engineering checks are not significance tests, broad robustness validation, independent replication or a superiority certificate.

The [254-test receipt summary](../experiments/SOFTWARE_TEST_REPORT_OBSERVER_V0.1.json) covers 40 source/configuration files. It includes synthetic checks for training/development isolation, label independence, stable phase calculations, current-observation-independent prediction, shared principal state, gaps, time matching, kinematic arithmetic, exact coverage, tamper rejection and consumed-attempt protection. Test fixtures were synthetic and raw access was blocked. The [scientific review](OBSERVER_SCIENTIFIC_REVIEW.md) records the design review, primary-source terminology grounding and dispositions.

Executed once from `manufacturing/`:

```sh
.venv/bin/python scripts/run_synthetic_tests.py
.venv/bin/python scripts/run_observer_study.py --execute --test-receipt local/software_validation/20261016T201237_129872Z/receipt.json
```

The managed environment required approved local execution for process monitoring. No system packages changed. Environment: local Python **3.15.0**, standard library only, macOS arm64, Apple M5 Pro; deterministic, seed `null`. The run records hardware, exact interpreter/commands, dependency inventory, revision `6e9534c85434c76b652e4696043368ad846340df`, dirty state, source snapshots and patch. A revision alone would not describe this uncommitted implementation.

| Resource | Measured | Declared cap |
|---|---:|---:|
| Supervised wall time | 169.945 s | 600 s |
| Worker CPU time | 169.649 s | 300 s |
| Worker-reported peak RSS | 330.19 MiB | 1 GiB |
| Outputs, including final manifest | 14.05 MiB | 50 MiB |

The supervisor took 675 RSS samples; maximum sampling gap was 0.2522 seconds. Monitoring is not a guaranteed instantaneous memory ceiling; terminal worker peak RSS was also checked. All limits passed.

The loader parsed **702,002 permitted observations**: 540,002 training and 162,000 development, including warmups. It traversed **1,242,004** CSV records for positioning and performed two whole-source byte-identity hashes totalling **3,956,386,188 bytes**. Byte hashing did not parse protected observations. Calibration and both final slices remained closed. Raw data, the earlier pilot/control run manifests, their selected references, frozen data/evaluation documents and the pending final-test freeze record remain unchanged.

Run storage: `experiments/runs/normal_observer_v0.1_20261016T201310_830939Z/`, UTC **2026-10-16 20:13:10–20:16:01** (17 October locally). It retains 18 artifacts plus `run.json`, four finite score arrays of 160,472 values each, aligned coordinates, fitted model, all diagnostics, source/configuration snapshots, logs and resource evidence. Row-level artifacts remain ignored and local.

Key identities:

| Record | SHA-256 |
|---|---|
| Frozen observer plan | `32826aa937d2c5126f1813a98b727e5e8769781fd4e7b59909912986e32017f0` |
| Observer configuration | `0d28264c8621aa9e772d72ad1ef5cd87734eef5f2c583982c5381b14ab8a7277` |
| Successful synthetic receipt | `e0e2666d5dbfedb81976783ea67e3e31857d5f4f2e83e8cae739de315311b209` |
| Run manifest | `7e28d3955f244058f3ce4767ed90b8f9362b727f69bd7c11d5f5328a4fe53fc0` |
| Fitted observer artifact | `28a9376bc93945adc783f7cd11354393fab070d0306081372891df7292977767` |
| Independent saved-artifact audit | `2ed0f969eead66a0dcc68aa79869aadab7d95aa6fc3ce1148e609424005f1fbb` |

The independent saved-artifact audit passed **48/48** grouped checks, including all artifact bytes/hashes, the 40-source binding, exact score/index coverage, pinned references, positive training-only scales, diagnostic accounting, independently recomputed acceptance criteria, resource caps and preserved earlier records. Its receipt is in `local/observer_review/saved_audit_normal_observer_v0.1_20261016T201310_830939Z.json`; script/command/log hashes are in `saved_audit_execution.json`. It did **not** independently reconstruct per-row JS from exported posteriors, because full posterior histories were not saved. It checked inferred correction bounds and aggregate agreement; shared-state identity is supported by the single-proposal implementation, synthetic tests and run assertions.

## What is complete and what follows

This milestone is complete within the supported observer scope: the state, nominal dynamics, prospective prediction, synchronization, matched score ablation, normal-only checks and limitations are concrete and executable. All fitted parameters remained unchanged during development, and artifacts are available for later calibration consideration. The principal security hypothesis remains open.

Use the refined working question: **Does retaining measurement-correction evidence improve an empirical motion observer's detection of recorded right-arm speed changes, compared with the same observer's residual alone under the same normal-only calibration?** The original threat, data and evaluation contracts remain unchanged. Treat the earlier digital-twin title as provisional; do not promote it on the strength of these checks alone.

Next complete the contribution/prior-art argument and admit a strong, compatible recent-method comparison, retaining the ordinary AR, velocity and fixed-template controls. Decide the full observer/control/ablation roster before any calibration. Any refinement of phase resolution, interpolation or diffusion needs a new declared development version and must preserve v0.1, including its weak one-step performance. Then implement/admit threshold-only calibration and freeze the final campaign. No threshold, attack result, publication claim or final-run approval is implied by this milestone.
