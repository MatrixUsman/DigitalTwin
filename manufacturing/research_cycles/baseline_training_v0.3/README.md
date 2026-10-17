# Trained manufacturing baseline pipeline

**Completed 17 October 2026.** Three compact CNN models (seeds 17,42,2026), a fitted AR(4) control, persistence and training-mean controls have been run on the same chronological normal-development targets. The pipeline passed 25 synthetic tests and 410 saved-artifact checks. Start with [the result report](RESULTS.md) and [learning curves](../../output/baseline_training_v0.3/learning_curves.png).

## Contents

- [PLAN.md](PLAN.md), [config.json](config.json), [FREEZE.json](FREEZE.json): model, data, selection, budget and pre-execution identities.
- [core.py](core.py): train-only scaling, timestamp boundaries, endpoint/batch construction, scores, early stopping and AR.
- [model.py](model.py): independently implemented compact architecture and inference-weight loading.
- [worker.py](worker.py), [run_study.py](run_study.py): sequential bounded training and resource supervision.
- [Synthetic tests](test_core.py), [loader tests](test_io.py), [model tests](test_model.py), [test/freeze runner](test_and_freeze.py).
- [Fresh-process verifier](verify_run.py): inference parity, independent metric/selection arithmetic and preserved-history checks.
- [Report/plot generator](report_results.py), [machine-readable results](RESULTS.json).
- [Post-execution package manifest](PACKAGE_MANIFEST.json): binds the delivered source, reports, figures and local evidence receipts. It supplements the pre-execution freeze and does not replace it.

## Completed commands

Working directory: `/Users/matrixusman/CUI/DigitalTwin`.

```sh
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/baseline_training_v0.3/test_and_freeze.py --attempt tests_001
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/baseline_training_v0.3/run_study.py --attempt training_001
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/baseline_training_v0.3/verify_run.py --run training_001 --attempt verify_001
manufacturing/.venv-plots-v03/bin/python manufacturing/research_cycles/baseline_training_v0.3/report_results.py
```

Consumed test/fitting/verification attempt names cannot be overwritten. Keep this study's sources and freeze unchanged; use a separately versioned plan for new data, models or training choices. The plotting command can regenerate presentation artifacts from the preserved result files; it does not fit models.

Training uses the unchanged [Python 3.12 dependency lock](../contribution_v0.2/requirements-macos-arm64.lock.txt). Plotting uses a separate [platform lock](requirements-plot-macos-arm64.lock.txt); no system packages changed. A clean machine needs those environments and the exact authorized nominal file before it can reproduce the data-dependent run. Synthetic tests work without benchmark data or network access.

## Saved model use

Fitted files are local under `manufacturing/local/baseline_training_v0.3/runs/training_001/`:

- `cnn_seed17_weights.npz`, `cnn_seed42_weights.npz`, `cnn_seed2026_weights.npz`: all three selected inference checkpoints.
- `prepared_development.npz`: fixed training mean/scale, standardized development histories and endpoint coordinates; these derived observations stay local.
- `ar_coefficients.npz`: AR(4) parameters.
- `*_scores.npz`: aligned predictions, standardized/native scores and original row coordinates.
- `learning_curves.csv`, `*_record.json`, `summary.json`, `population.json`, `provenance.json`, `launch.json`, `data_access.json`, `supervisor.json`.

Load an inference checkpoint with `model.load_weights_artifact(config, weight_path)`. Input shape is `(batch,45,9)` in the recorded feature order and training standardization; output `(batch,1,9)` predicts the next observation. Use the saved mean/scale, preserve gap boundaries, and score each actual target at its declared coordinate. No fitted threshold is included. Do not resume optimization from these inference-only weights as though an optimizer state had been saved.

## Interpretation and next use

The average CNN normal-development MSE is 0.105364; persistence is 0.124758 and AR(4) is 0.071310. All checkpoints were selected using normal data. The CNNs reached the fixed 30-epoch cap while still improving, which is visible in the curves. These artifacts are ready for a separately specified exploratory limitation study; any added training budget is a new declared choice. Retain AR and persistence as controls. All previous experiments and the exposed-holdout record remain unchanged.
