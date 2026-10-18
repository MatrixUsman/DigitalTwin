# Recent author-code forecasting comparisons

## Material Passport
Manufacturing; 18 October 2026; operator Codex; owner Haiqa Mushtaq; requested manuscript author Muhammad Usman. User explicitly requested running recent cited methods. Implement and run short compatibility pilots, then request approval for a concrete longer local study if needed. No paid compute, public release or attack/final-test access.

## Methods and correspondence

Execute the official ModernTCN, iTransformer and TimeMixer model classes, with unchanged author source in ignored `baselines/vendor/`. These are ICLR 2024 forecasting architectures transferred to the previously admitted nominal CASPER IMU prediction task. They are not digital-twin cyberattack-detector reproductions. The published benchmark numbers and optimal test thresholds are never used as our results.

Use the original authors' ETTh1 architectural settings as declared in `adapter.configuration`, with disclosed task adaptations: nine channels, 96 past observations and one future observation. ModernTCN uses one 64-wide stage/block, kernels 51/5, patch 8/stride 4, FFN ratio 1 and dropout .3; iTransformer uses two 256-wide layers, FFN 256 and eight heads; TimeMixer uses two layers, width 16/FFN 32, three average-downsampling levels and channel-independent moving-average decomposition. Disable future temporal covariates. Forecast from the past window only; symmetric convolutions are confined to that observed window. There is no target reconstruction or current-target input. Model-defined input-window normalization remains enabled; all outer scaling uses training only.

Model/seed CPU runs are sequential. Adam learning rates follow the selected author settings: .0001 for ModernTCN/iTransformer, .01 for TimeMixer. Batch size is 64, chronological and unshuffled. The common development rule saves the lowest finite standardized MSE with improvement >1e-6, patience 5, and at most 100 epochs. This is a fixed transferred configuration, not a paper-faithful benchmark or globally optimized model. Record actual stopping reason; a CPU-capped improving model is not converged.

## Data boundary and shared population

Load only the hashed `local/casper_convergence_v0.11/runs/pilot_001/prepared.npz` derived from the previously exposed nominal prefix. Its training-only scaler, causal width-20 median filtering, chronological raw split and source identity are inherited exactly. No raw data need be reopened. There are 8,192 eligible training targets and 2,048 development targets, the same target rows as E3. Older CNNs use histories 755 and 45; these three all use 96. Record that history difference rather than implying identical architectures/information windows. Same target population permits a normal-prediction comparison but does not establish online attack or recovery performance. No attack thresholds, test labels or original voraus-AD test signals are accessed.

## Bounded pilot and proposed larger run

Pilot: seed 17, two complete epochs per method, full eligible training/development populations. Bound each method to 120 s wall, 90 s CPU, 1 GiB sampled RSS and 50 MiB outputs. Purpose: source compatibility, finite gradients/scores, exact target alignment, immutable development evaluation, and measured cost. Save all pilot predictions/checkpoints and all failures. Do not use pilot outcome differences to change architectures or learning rates.

Full run, only after explicit approval: seeds 17, 42, 2026 start afresh; maximum 100 epochs/patience 5. Per-seed CPU admission 150 s; estimate the next epoch as 1.25 times its last CPU cost and reserve 2 s. Per-method 600 s wall, 480 s CPU, 1 GiB sampled RSS, 50 MiB outputs. Three methods give maximum 30 minutes wall/24 minutes CPU and 150 MiB output. Parent wall budget applies across methods. No automatic retry or favorable-seed selection. Freeze these rules before approval/execution; report shorter-than-needed training honestly.

Synthetic software tests must confirm past-only windows, output alignment, finite forward/backward updates, deterministic evaluation, no evaluation-state mutation and exact saved-state reload. Freeze upstream revisions/source hashes/licenses, adapter/config/runner, test receipt, interpreter/dependency lock, data/scaler/row identities and commands. Resource monitor and worker CPU limit enforce budgets. Report actual resources and checkpoint selection for every seed. Validate saved prediction arithmetic and row identity after each completed stage. Keep development numbers separate from final benchmark results.

MVT-Flow remains a separate offline, whole-execution study with a different dataset and objective. Its source discrepancies need an explicit released-code versus paper-aligned decision; it is not silently included in this forecast ranking. Foundational controls remain useful even though their original mathematics is older than three years. The recent-paper rule applies to published main comparator papers, not a prohibition on AR, persistence or CUSUM.
