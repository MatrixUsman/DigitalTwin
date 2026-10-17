# Compact CNN baseline training study v0.3

## Material Passport

- Project: manufacturing; owner Haiqa Mushtaq; operator Codex under the user's instruction to implement and execute the next step.
- Date: 17 October 2026, Asia/Karachi.
- Workflow: academic-research-suite experiment execution and artifact validation, applied inline. The user's instruction authorizes implementation and this bounded run; repeated stage confirmation is unnecessary.
- Purpose: produce tested fitted baseline artifacts, convergence curves and aligned normal-development control comparisons.
- Status when written: planned before reading the expanded nominal prefix or fitting. The execution freeze will bind these bytes, source/configuration, environment and passing tests.

## Reference and declared deviations

Reference: Kayan et al., *Real-Time Anomaly Detection for Industrial Robotic Arms Using Edge Computing*, DOI `10.1109/JIOT.2025.3569780`; author manuscript SHA-256 `a7f8a647ad277fdcacb0e361b3ce95107bfb849a8111ac314d7841bf31d75fd9`. The saved MIT notebook revision is `41b907749b7e5882319690a627a251e93fa99982`, notebook SHA-256 `46bf5121bf6c2a4420d41f3914b23e0ccebc424891265c56f24386fb67ab07a0`. No upstream code is copied into this implementation.

The paper describes nine-channel IMU prediction, two convolutions and max-pooling; Table IX includes the compact 45→1, eight-filter/kernel-three/pool-three configuration. Notebook cell 238 uses batch 1024, no shuffle, MSE/Adamax and zero-initialized output weights; its saved history is 30 and maximum epochs ten/patience three. The manuscript instead describes five-epoch patience and a 60/20/20 split. Exact checkpoint/scaler/table correspondence is unresolved. Our implementation fixes history 45 and endpoint alignment, uses a bounded chronological prefix, max 30 epochs, patience five, restores the best eligible checkpoint, and reports three fixed seeds. It is an **independent implementation of the published architectural family under a declared normal-only protocol**. Raw-channel RMSE is retained as secondary evidence; balanced standardized-channel MSE selects checkpoints, avoiding implicit dominance by differently scaled sensor units. No authors' attack score is attributed to this run.

## Data and isolation contract

Only the already acquired provider-v2 nominal `IMU_10Hz.csv`, expected SHA in `config.json`, can be opened. Numeric row intervals exclude the CSV header and are half-open:

| Population | Raw rows | Potential targets after 45-observation warmup |
|---|---|---|
| Training | `[219,65800)` | `[264,65800)`: 65,536 |
| Normal development | `[65800,82229)` | `[65845,82229)`: 16,384 |

The previous pilot's small development block now lies within the expanded training block. This reuse is disclosed exploratory normal-data development; the new development block is subsequent and separate. No calibration/final population is selected or opened here. Do not parse rows at or beyond 82,229. Hashing the complete nominal file checks identity without parsing later observations.

Parse schema strictly; no silent bad-line skipping, sorting, interpolation or imputation. Fail on nonfinite measurements or constant training channels. Fit population means/standard deviations on the designated training observations only, then freeze them. Timestamp values never enter model features. Fit the median positive timestamp increment on training timestamps only. A nonpositive transition or increment exceeding five times that median marks a segment boundary. No prediction window or target may cross a boundary or a split. Report every excluded target and reason; require at least 95% of potential targets in each population before fitting. All methods use identical eligible endpoint arrays. Clock units remain unresolved; use sample/observation units, not invented elapsed seconds.

## Models, selection and scores

CNN: history 45, nine channels, Conv1D(8,3,ReLU,valid) twice, MaxPool(3), flatten, Dense(9, zero kernel/default zero bias), reshape(1,9), Adamax learning rate 0.001, MSE. Seed 17/42/2026; all runs retained, no best-seed selection. One CPU thread per TensorFlow intra/inter-op pool. Train in chronological batches of 1024, no shuffle. Maximum 30 epochs; stop after five epochs without a development MSE improvement greater than `1e-6`. Select the earliest accepted best epoch among completed epochs 1–30. Epoch zero is diagnostic only. Save that model's weights; optimizer state is intentionally excluded, so the artifact is for inference and is not a resumable training checkpoint.

Learning curves are **post-epoch full-population training and development MSE**, not averages of a framework's cumulative batch-metric averages. Score one future observation after each history; standardized channel RMSE is primary, inverse-scaled native channel RMSE secondary. No aggregation window or alarm threshold is selected. Save indices, all scores, predictions and per-channel errors locally.

Controls, fixed in advance and fitted only on training: zero in standardized space (training mean), last-value persistence, and multivariate AR(4) with an intercept and ridge 0.001 on `X'X/n` (intercept unpenalized). Every control uses the same CNN-eligible endpoints. No AR order/ridge search; this is a strong ordinary control, not an invented paper baseline. Report each model/seed, arithmetic mean and standard deviation across CNN seeds, and all losses even if controls are stronger. Seeds characterize optimization variation on this recording.

## Tests, execution and verification

Synthetic tests precede a freeze and actual data access. Cover chronology, future/target alignment, gap boundaries, training-only transformations, nonfinite/constant rejection, batching, score arithmetic, AR recovery on a known synthetic process, early-stop/tie behavior, model shape/parameter count and save/load inference parity. Tests contain no benchmark observations.

One supervised attempt runs the roster sequentially. Caps: 600 s wall, 300 s CPU, 1 GiB sampled RSS, 50 MiB outputs. The earlier 3.8355 s one-epoch pilot includes startup and does not isolate epoch cost; we use caps and per-epoch measurements rather than assert a precise duration. No paid resources, background service, lengthy uncapped run or automated hyperparameter sweep. The existing unchanged supervisor enforces the caps; failures remain in named immutable attempt directories. Sampled RSS is not an instantaneous hard ceiling. If infrastructure fails, diagnose and preserve the attempt before a separately named retry within the authorized implementation task.

Required outputs: pre-execution source/config/test freeze, append-only epoch log, all three selected CNN artifacts, scaler and AR coefficients, aligned score/prediction arrays, source/runtime provenance, per-method fitting/scoring cost, supervisor result and independent saved-artifact arithmetic/parity review. An external verification worker may reload models and recompute saved development predictions using stored standardized histories only; it never refits or changes selected checkpoints. Plots derive solely from recorded learning curves and aggregate losses.

Command from workspace root after tests/freeze:

```sh
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/baseline_training_v0.3/run_study.py --attempt training_001
```

The completed study advances a trained reference for subsequent limitation experiments. Its successful deliverable is a valid fitted baseline and complete evidence, regardless of which predictor has the lowest normal-development loss. Previous frozen experiments and v0.2 receipts stay unchanged.
