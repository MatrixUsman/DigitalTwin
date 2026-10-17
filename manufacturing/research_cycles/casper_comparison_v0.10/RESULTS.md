# CASPER-family comparison pilot: measured results

17 October 2026. **Completed normal-only architectural pilot. No attack superiority or new detector established.**

The missing original CASPER-style predictor is now implemented independently and executed alongside the compact Edge-2025 architecture and ordinary controls. All nine outcomes use the same nine IMU channels, training-only scaler, causal filtering and 2,048 development targets. The experiment provides usable saved references and a verified alignment pipeline. It does not establish full-paper reproduction or adequate CNN convergence.

## Complete normal-development outcomes

Lower MSE indicates better next-observation prediction within this specific filtered prefix. These are development results, not held-out attack performance. Native-unit MSE combines heterogeneous sensor units and has a different weighting from standardized MSE.

| Method / seed | Standardized MSE | Native-unit MSE | Completed / selected epoch | Stop |
|---|---:|---:|---:|---|
| mean | 1.073987 | 258.138210 | — | Closed-form control |
| persistence | 0.019432 | 2.942017 | — | Closed-form control |
| ar4 | 0.006074 | 0.542004 | — | Closed-form control |
| casper_cnn_seed17 | 0.034652 | 3.226219 | 3 / 3 | CPU admission cap |
| casper_cnn_seed42 | 0.041666 | 4.355938 | 3 / 2 | CPU admission cap |
| casper_cnn_seed2026 | 0.032397 | 2.738312 | 3 / 3 | CPU admission cap |
| edge_cnn_seed17 | 0.087276 | 18.201428 | 30 / 30 | Epoch cap |
| edge_cnn_seed42 | 0.080812 | 15.870631 | 30 / 30 | Epoch cap |
| edge_cnn_seed2026 | 0.079634 | 14.272769 | 30 / 30 | Epoch cap |

AR(4) has the lowest error in this pilot. This supports keeping it as a strong control. It does not establish its attack-detection advantage. The CASPER-style fits stop after three epochs under the resource policy; two select the last available epoch, and seed42 selects epoch2. All compact models select epoch30 and are still improving. The larger architecture has 39,977 parameters and the compact architecture 1,369. No seed is discarded or declared the preferred final model.

## What was actually run

- Raw normal file: author-linked CASPER1&2 provider-v2 `nominal/IMU_10Hz.csv`, SHA256 `1221df9be80c229969f3f21f820837e68ad28f4ccb3949bf4013f00d6d69d62c`. It is not established as the original CASPER paper-run release.
- Parsed at most12,007 numeric rows, all inside previously exposed normal development. Split raw rows `[219,9185)` and `[9185,12007)` before causal trailing20-observation medians; training-only population scaling. No attack file or final-test label was opened.
- Training targets8,192, development targets2,048. Same complete755-history support for every method; compact/ordinary controls may use shorter histories within that support. Both standardized and native-channel RMSE retained. Rolling755-residual sums have1,294 common endpoints.
- Adamax.001, chronological minibatches64, at most30epochs, normal-development patience5, minimum improvement1e-6; per-fit30-second CPU admission policy. Prefix, batch, stopping and evaluation differ from the original publication. Full details were [frozen before fitting](PLAN.md).

## Execution and verification

Successful attempt `pilot_002`: **100.647s supervised wall, 98.871s worker CPU, 563.80MiB sampled RSS**, 564.55MiB worker lifetime peak, 2.53MiB supervised output. The worker's internal wall timer starts after library import and is not the total supervised duration. All whole-run limits passed. RSS sampling is not an instantaneous hard memory ceiling.

The first launch stopped before worker startup because the sandbox blocked `/bin/ps`. Its receipt and empty log remain in `pilot_001`. A separately recorded monitoring retry changed only the launcher output directory and process-monitor permission; the frozen scientific worker/configuration were unchanged. This is one completed scientific pilot and one preserved startup failure.

**14 synthetic tests** passed before freezing. A fresh process then passed **2,411 integrity/numerical checks**: exact CNN checkpoint reload/prediction parity, independent control calculations and rolling-sum arithmetic, selected-epoch accounting, all nine score populations, resource receipts and preservation of11 earlier scientific sources,1,521 input bindings,301 v0.9 package files and24 manuscript package files. The verifier opens derived saved observations, not raw or attack files. These checks validate software/artifact consistency, not physical fidelity, novelty or benchmark superiority.

## Evidence and next action

[Scientific and comparator decision](DECISION.md) separates the IMU comparison from the command-aware recovery problem and specifies the uncertainty-control requirement. [Source review](SOURCE_REVIEW.md) preserves what was and was not verified. Original checkpoint/release/label provenance and full convergence remain necessary before a CASPER superiority claim. Existing failed recovery results and the consolidated PDF remain unchanged.

The immediate next executable experiment is a separately bounded normal-only convergence study. The original-contribution objective additionally requires an operation distinguishable from existing uncertainty/recovery methods and a successful fresh, common-information evaluation. A smaller prediction error or a new name cannot substitute for those results.

Commands executed from the workspace root:

```sh
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/casper_comparison_v0.10/freeze.py
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/casper_comparison_v0.10/run.py
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/casper_comparison_v0.10/run_monitor_retry.py
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/casper_comparison_v0.10/verify.py
```

The run launchers enforce unique output directories. Do not rerun a consumed pilot or edit its freeze to disguise a retry. No public upload, external contact, paid compute or new PDF.
