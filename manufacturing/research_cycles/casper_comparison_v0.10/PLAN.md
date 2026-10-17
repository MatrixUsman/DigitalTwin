# CASPER-family common-input reproduction pilot

## Material Passport

Manufacturing / Haiqa Mushtaq; operator Codex under the user's request to address fair CASPER comparison and novelty. 17 October 2026. Academic-research-suite experiment workflow applied inline; no delegated agents. This plan precedes new fitting. It admits one bounded normal-only run, not a full attack benchmark or a novel detector. No new PDF is planned.

## Purpose and admission

Resolve an executable missing comparator: independently implement the original CASPER CNN architecture and its causal scoring pipeline, then fit it beside the compact Edge-2025 architecture and strong ordinary controls on identical external-IMU observations. The old joint-state simulation cannot prove superiority over an external-IMU detector. No original notebook code is copied or executed; its reuse grant and published checkpoint lineage remain unresolved. `core.py` and `io_utils.py` are our own previously tested v0.3 utilities, copied unchanged at creation.

Source: corrected CASPER VOR V1.1, 5 February 2025, DOI 10.1145/3670414, Figure 11 and Algorithm 1; local PDF SHA256 `323efce849d75e16833f166983a7387b6d8f86760ce889fe4918ff2f775be186`. The original journal article is August 2024. Figure 11 and the previous static source audit support four Conv1D layers, 32 filters, kernel 5, ReLU, pooling by three after each pair, flatten and nine-output prediction from 755 observations. Edge-2025 uses the already audited compact 45-observation, two-layer, eight-filter/kernel-three/pool-three configuration. Full paper experiments and evaluated checkpoints are not reproduced by matching an architecture.

## Data, filtering and matching

Use only the already received CASPER 1&2 provider-v2 nominal `IMU_10Hz.csv`, not a newly assumed original-paper release. Full file hashing checks identity; parse at most 12,007 numeric records. All selected observations are within previously exposed normal development. No fresh-test designation, attack file or label access.

Split raw rows first: training `[219,9185)`, development `[9185,12007)`. Fit median positive clock increment on training only. Reject either block if any interval is nonpositive or exceeds five times that increment. Do not silently bridge gaps. Apply a strictly trailing 20-observation per-channel median separately in each block, discarding its first nineteen incomplete outputs. Fit mean/population-standard-deviation scaling on filtered training only; zero/invalid scales fail. Complete history then gives **8,192 common training endpoints** and **2,048 common development endpoints**. Both CNNs and controls use exactly these endpoints, although the compact CNN needs only the latest 45 observations. Timestamp is not a feature and its unit remains unresolved.

All residuals compare a predicted next observation with that same causal filtered target. Retain both standardized-channel RMSE and inverse-scaled native-channel RMSE. A trailing sum of 755 residuals, restarting per block, gives 1,294 development score endpoints. Do not tune a threshold or use majority-window attack labels. Native-channel units are heterogeneous; neither score convention is silently declared universally preferable. The median itself delays/suppresses some changes, which remains an experimental factor for later evaluation.

## Training roster and bounded selection

Three deterministic controls: training mean, persistence and multivariate AR(4), ridge .001 on mean normal equations with unpenalized intercept. Six CNN fits: each architecture at seeds 17,42,2026. Input/prediction conventions, training data and scaler are common. CASPER architecture has 39,977 parameters; compact architecture has 1,369. Dense output kernels start at zero, with Keras default zero bias; this is an explicit implementation choice from the audited family, not an independently established published-checkpoint identity.

CNNs use Adamax .001, chronological minibatches of 64, no shuffle, maximum 30 epochs, normal-development patience five and minimum MSE improvement 1e-6. Batch size, prefix size and maximum epochs differ from the original paper/notebook; this is a resource pilot with modified protocol. Each fit has a **30-second CPU admission budget for complete epochs**. After its first complete epoch, do not begin another unless remaining budget exceeds 1.25 times the most recent complete epoch cost plus one second. Whole-run caps remain authoritative. The first epoch could exceed the per-fit admission budget; record it rather than erase it. Stop/selection uses only normal development. Save the earliest accepted best completed epoch. Record all curves, all seeds and every terminal failure. Do not select a winning seed or compare these losses to old differently filtered/subset results.

A budget or epoch cap is not convergence. This pilot establishes architecture execution, alignment, feasible cost and normal prediction behavior. A later full comparator needs adequate normal-only convergence, frozen calibration, defensible labels and compatible common-information final conditions.

## Execution and checks

Existing isolated Python 3.12/TensorFlow 2.16.2 environment, one CPU thread, no package change. Global bounds: 600 s wall, 300 s CPU, 1 GiB sampled RSS, 50 MiB output. Use existing supervisor, preserve launch/worker failures and exact logs. Test synthetic trailing-median causality/split isolation, gaps, constant/nonfinite rejection, raw endpoint lineage, 755-residual support, both architecture shapes/counts, causality of batched targets, save/load parity and CPU admission rule. Bind source/tests/configuration plus original study/PDF package hashes before raw access or fitting.

After the run, reload every saved model without refitting, independently recompute all saved predictions/metrics and aggregation, verify scaler independence and every selected epoch, and confirm prior packages unchanged. Output score arrays and checkpoints stay local and ignored. Save actual resource costs and an honest admission decision. No training result establishes attack superiority or originality.

Command from workspace root after tests/freezing:

```sh
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/casper_comparison_v0.10/run.py
```
