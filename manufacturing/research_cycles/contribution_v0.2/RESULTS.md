# Baseline diagnostics and nominal pilot: actual results

17 October 2026. These results concern identified code paths, published model files and one small normal-data feasibility run. They do not reproduce the paper's benchmark tables, establish a new attack detector or invalidate the authors' results. [The dossier](../../docs/BASELINE_LIMITATION_DOSSIER_V0.2.md) gives exact source locations and interpretation limits.

## Software and released-artifact checks

**18 synthetic tests passed**: 13 source/alignment tests and five split/scaler isolation tests. Development changes cannot affect the fitted training reference in those tests. The fixtures are synthetic; the source-path tests additionally require the pinned public notebook. The original 324-test frozen experiment remains separate and was not rerun or modified.

| Check | Measured outcome | Meaning |
|---|---|---|
| Saved CNN branch uses history 30 but target offset 45 | 170 synthetic predictions versus 155 targets; `ValueError` | Inconsistent saved configuration, not known paper execution |
| Multi-output scoring uses input-origin targets | Perfect synthetic future forecasts receive 905.6075308874148 from the source function; correctly aligned RMSE is 0 | Specific target-alignment defect; not the released one-output LSTM branch |
| LSTM aggregation reads preceding row-score variables | Changing the new window scores leaves the saved aggregation unchanged | Stale dependency under that sequential execution; table lineage unknown |
| Notebook RMSE versus firmware absolute-error sum | Two synthetic residual vectors reverse ranking | Different score semantics, not a simple threshold rescaling |
| Released TFLite CNN/LSTM | Both load, input `[1,45,9]`, output `[1,1,9]`, finite outputs for seeds 17,42,2026 | Runtime compatibility only |
| Recurrent state | LSTM repeat-without-reset changes by 0.02729794, 0.02830003 and 0.02499928; reset equals fresh interpreter in all three fixtures | Requires an explicit state policy. This is known runtime behavior, not a novel algorithm or necessarily an upstream bug |

Threshold optimization on evaluated anomaly labels was audited **statically** and not executed. Its impact on real detection performance remains unknown.

## Real normal-only CNN pilot

One public author-linked nominal file from the combined CASPER-1-and-2 provider release v2 was acquired. The file SHA-256 is `1221df9be80c229969f3f21f820837e68ad28f4ccb3949bf4013f00d6d69d62c`; it is distinct from the original CASPER-v3 archive. Only an initial nominal prefix was parsed. No disturbance file was acquired, and no original final observations were reopened.

The independent CNN uses the compact published architectural family: history 45, two valid Conv1D layers with eight filters/kernel three/ReLU, max-pooling three, flatten, nine-output dense layer, Adamax learning rate 0.001 and MSE. It has 1,369 parameters. One epoch, batch 256, no shuffle, seed 17. This is a subset feasibility implementation, **not the paper's complete training protocol**.

All row intervals are zero-based, half-open, excluding the CSV header. Training observations `[219,8456)` produce 8,192 targets `[264,8456)`. Separate development observations `[8456,10549)` produce 2,048 targets `[8501,10549)`. Split before windows; all nine-channel means/standard deviations use training observations only. Fitted weights and scaler stayed unchanged during development. All 2,048 scores were finite and aligned. No threshold, attack metric or model-selection contest was run.

| Normal-development quantity | Measured value |
|---|---:|
| One-epoch CNN standardized MSE | 0.819239616394043 |
| Last-value persistence standardized MSE, same targets | 0.12468351423740387 |
| Zero prediction standardized MSE, same targets | 0.9077731370925903 |

Persistence performs much better on this prefix. A one-epoch feasibility run is not evidence that the converged published method is generally inferior. Retain these values; do not optimize a paper claim around them.

The first 11,000 nominal rows were separately profiled. Stored time increases without duplicate prefix timestamps, but native increments are not uniform. Clock units and acquisition-versus-arrival semantics remain unresolved; no physical jitter, duration or seconds-based detection-delay conclusion is drawn.

## Attempts and resources

Each worker has 300 s wall, 180 s CPU, 1 GiB monitored RSS and 50 MiB output caps. RSS is sampled, not an instantaneous hard ceiling. CPU is limited in the worker. Output counts below are supervisor observations before the parent's final receipt.

| Attempt | Outcome | Supervised wall | Sampled peak RSS | Outputs |
|---|---|---:|---:|---:|
| `diagnostics_001` | Failed: sandbox denied `/bin/ps`; worker stopped. Failure receipt backfilled from captured tool output because the initial launcher had not saved it | 0.005319 s | unavailable | 0 B |
| `diagnostics_002` | Failed: our initial repeat-equality assertion incorrectly assumed a stateless LSTM. Preserved log; revised the diagnostic to measure reset/continuous behavior | 106.001162 s | 420,659,200 B | 377 B |
| `diagnostics_003` | Completed corrected measurement diagnostic | 3.385369 s | 473,071,616 B | 9,600 B |
| `normal_pilot_001` | Completed normal-only pilot | 3.835523 s | 538,066,944 B | 78,746 B |

Successful diagnostic worker CPU was 2.191029 s; pilot worker CPU was 2.521551 s. These are laptop feasibility measurements, not edge-device latency. Initial TensorFlow import/setup affected the failed attempt; it is not a model inference benchmark.

Setup failures also remain visible: initial sandbox DNS resolution failures for source retrieval; one pip invocation before venv creation completed (`No module named pip`). The subsequent isolated installation succeeded and `pip check` passed. No system packages changed. A later documentation patch initially failed on an unmatched context and was reapplied; it did not modify scientific artifacts.

## Provenance and unfinished scientific work

Run JSON records preserve timestamps, exact commands/cwd, interpreter/platform, Git revision/dirty state, source identities, runtime versions, parameters and resource outcomes. [The evidence manifest](EVIDENCE_MANIFEST.json) binds these receipts, public source bytes, test logs and the saved artifacts. Its creation is a post-run readback, not a retroactive preregistration. Python 3.12.15, TensorFlow 2.16.2 and NumPy 1.26.4 ran on macOS arm64; the complete dependency lock is retained. A separately labelled post-run host query records Apple M5 Pro, 18 logical CPUs and 24 GiB RAM. Initial sandbox hardware queries were denied; both the denial and authorized read-only retry are preserved. The workers use one TensorFlow intra/inter-op thread, not all host cores.

The [candidate improvement](../../docs/CONTRIBUTION_DESIGN_V0.2.md) remains unimplemented and unadmitted as novel. Close prior art already covers key ingredients. Full paper reproduction, method-level cyber limitation, prospective independent evaluation and a contribution paper remain unfinished. The existing CASPER holdout stays exposed; a renamed split or new noise seed cannot make it fresh physical evidence.
