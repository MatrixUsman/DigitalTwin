# CAROTS experiments: original protocol and our pending reproduction

Status **16 October 2026:** static acquisition/audit only. No environment, training, model inference or benchmark scoring was performed.

## Original description

The [published manuscript](artifacts/papers/CAROTS_ICML2025.pdf), Section 5 and appendices, describes normal training data with 20% reserved for validation, training-based standardization, factor-five SWaT/WADI downsampling and length-ten windows. A window is anomalous when it contains an anomalous retained point. Defaults include batch size 256, 30 epochs, three seeds, an LSTM encoder and NVIDIA A40 training. Checkpoint selection uses lowest validation loss. The paper reports AUROC, AUPRC and best F1 and excludes point-adjusted F1.

The pinned scripts configure SWaT with learning rate `0.0003`, weight decay `0.001`, and WADI with learning rate `0.001`, weight decay `0.0`; both set downsampling to five. These are upstream configuration evidence, not settings approved for our runs. Read [SWaT.sh](vendor/author_code/scripts/SWaT.sh), [WADI.sh](vendor/author_code/scripts/WADI.sh) and [config.py](vendor/author_code/config.py).

## Changes and checks required before a run

| Area | Finding and required action |
|---|---|
| Thresholds and reported F1 | `threshold.py` optimizes against test labels. `predictor.py` independently reports the maximum F1 from the test PR curve. Replace both paths with frozen development-only calibration and reporting. Changing one setting is insufficient. |
| Validation | Default checkpoint selection uses normal validation loss. Preserve that separation and prohibit the test-as-validation loader branch. Determine and record all hyperparameter-selection data. |
| Metrics | Main metrics must be unadjusted. The code can also output point-adjusted metrics, despite the paper's exclusion; keep metric names explicit. Its trapezoidal PR-AUC is not interchangeable with average precision. |
| Data | Resolve [release, label, resampling and alignment questions](DATASETS.md), then test chronology and score coverage on synthetic fixtures before private data. |
| Configurations | Paper gradient clipping is `1.0`; code default is `0.5`. Resolve and record paper/code differences rather than silently assuming equivalence. Audit full resolved configurations before execution. |
| Device and dependencies | CUDA calls are hard-coded in training paths. No validated environment lock or CPU/MPS port is available. Local compatibility and runtime remain unmeasured. |
| Reused artifacts | The downloaded CUTS+ graph/checkpoint provenance lacks complete training/split metadata. Preserve for study; decide whether reuse is valid only after checking it against our common protocol. No checkpoint was loaded. |
| Variants | Predeclare both CAROTS and CAROTS-dagger. The inspected predictor combines scores; a contrastive-only evaluation path needs explicit validation. Do not select a preferred variant using final attack outcomes. |

Our intended classification is **author-code execution with declared protocol changes**, if implementation proceeds. That does not promise numerical replication of the authors' best-F1 scores. Preserve the current source snapshot, record future patches, and keep our runs under `water/experiments/runs/`, apart from author artifacts.

## Next bounded steps

1. Learn the pipeline and record unresolved questions; no installation is needed for reading.
2. Confirm authorized files and freeze a common data/evaluation protocol for all admitted methods.
3. Prepare an isolated environment and small adapters; test loading, splits, alignment, calibration independence and metrics using explicitly synthetic fixtures.
4. Propose a bounded resource pilot with recorded configuration before lengthy training. Do not execute the upstream shell scripts during acquisition.
5. Freeze all baseline and proposed-method development before opening final held-out attack results. Record seeds, dependencies, commands, revisions, hashes, logs and deviations for every reported experiment.

See the [reproduction plan](../../docs/REPRODUCTION_PLAN.md) and [roadmap](../../docs/RESEARCH_ROADMAP.md) for the complete sequence. No task above is marked completed by possession of source files.
