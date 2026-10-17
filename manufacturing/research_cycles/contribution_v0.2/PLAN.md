# Baseline investigation and contribution development v0.2

Started 17 October 2026 after the user's explicit request to pursue all five steps. The user also confirmed **no physical testbed access; use public datasets and clearly labelled simulation**. This is a new exploratory cycle. Earlier CASPER outcomes remain exposed and immutable. The intended contribution paper remains conditional on actual novelty and evidence; no pipeline stage may invent their completion.

## Execution scope

Use the academic-research-suite research-to-paper workflow with its experiment planning/validation guidance, inline. The user's instruction authorizes progression through the requested stages without repeated stage-permission questions. Existing explicit restrictions on paid compute, lengthy training, publishing and external messages remain. No outside model or fixed agent team is invoked.

1. Audit CASPER and its 2025 Edge/TinyML successor against manuscripts and pinned sources. Verify and retain licensing; identify exact branch/run uncertainty.
2. Reproduce isolated implementation defects with **synthetic arrays** and run the two published TFLite artifacts on synthetic inputs. This is code/model-artifact validation, not reproduction of paper scores or a robot benchmark. Never run an upstream best-test-F1 evaluation on benchmark attacks.
3. Acquire only the publicly listed successor's nominal `IMU_10Hz.csv` at provider version 2, if accessible within a 160 MB uncompressed size cap. Hash and preserve it read-only. Inspect metadata and a bounded initial nominal prefix only. Do not download/inspect anomaly observations in this cycle before a new final protocol.
4. If source identity, schema and clock checks pass, execute one bounded normal-only pilot of an independently coded, author-architecture-matched compact CNN: input 45, output 1, two 8-filter/kernel-3 valid Conv1D layers, pool 3, flatten/dense nine outputs, Adamax/MSE. Fit on 8,192 nominal targets and score 2,048 subsequent development targets, with independent window support. One epoch, batch 256, no shuffle, seed 17. This is a resource/functional pilot, not the published training protocol or an admitted final model. Fit the scaler only on training observations. No thresholds, attack metrics, checkpoint competition or final test.
5. Specify a mechanistic hypothesis around brief versus persistent deviations and the forecast/aggregation trade-off. Check close prior art first, including simple multiscale and sequential-change controls. A known detector with corrected evaluation is not automatically novel. Any synthetic experiment must disclose its generator and lack of physical validation.
6. Produce an evidence-backed contribution prospectus and LaTeX research notes. Write an original-contribution results section only if evidence establishes it; preserve explicit unfinished stages otherwise.

## Budgets and provenance

Each diagnostic/pilot worker: wall 300 s; CPU 180 s; monitored RSS 1 GiB; output 50 MiB. Use the existing unchanged supervisor. Preserve failures; source/runtime fixes receive new attempt directories. No automatic model/hyperparameter search. Stop on an unavailable RSS monitor rather than silently removing it. Network/source retrieval and isolated environment installation are separately logged setup actions.

Use a separate Python 3.12 environment, `.venv-reproduction-v02`, with TensorFlow 2.16.2, NumPy 1.26.4, pandas 2.2.3 and scikit-learn 1.5.2; freeze all actual transitive versions after installation. This is a new execution environment, not the authors' undocumented historical environment. Save commands, source/artifact hashes, interpreter/platform, Git revision/dirty state, timestamps, resource receipts and all failures. No GPU or edge-device speed claim follows from laptop execution.

Pinned successor: `hkayann/Real-time-Anomaly-Detection-in-Industrial-Robotic-Arms-via-TinyML`, revision `41b907749b7e5882319690a627a251e93fa99982`, root MIT grant. Original CASPER source remains at its separately recorded revision/license status. Reuse only the licensed successor snippets with their notice; do not transfer that grant to the original repository.

## Planned diagnostic claims

| ID | Test | Interpretation boundary |
|---|---|---|
| D1 | Execute successor cell 245's score-prefix with cell 238's saved 30-step history on synthetic data | Establishes whether the saved branch runs consistently with its hard-coded 45-row target offset; not the authors' actual run order |
| D2 | Execute cell 281's extracted anomaly-scoring function using perfect synthetic 45-step future forecasts | Demonstrates target alignment of that exact function; fake predictions are a software fixture, not model performance |
| D3 | Trace cell 283's rolling sums against the variables created in cell 281 | Tests stale-score dependency in a sequential saved-notebook path; does not establish which path produced a paper table |
| D4 | Compare notebook channel RMSE with embedded sum of absolute channel residuals on known synthetic vectors | Demonstrates differing score order, not the magnitude of real-world accuracy loss |
| D5 | Invoke both downloaded TFLite artifacts on deterministic synthetic input arrays | Establishes compatible runtime, shapes, finite outputs and repeatability only; no fitted scaler/run lineage inferred |

CASPER and successor threshold-oracle paths are audited statically. The source-level observation does not measure the performance penalty of fixing the protocol. Do not confuse these diagnostics with demonstrated algorithmic inferiority.
