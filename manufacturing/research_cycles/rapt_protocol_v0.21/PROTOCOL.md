# RAPT normal-only training and preprocessing protocol

19 October 2026; manufacturing only. This is the next bounded step after the completed v0.20 source admission and one-epoch timing pilot. Preserve all earlier scientific runs and sealed manuscripts. No attack/final observations, public G1 signals or new simulation conditions enter this stage.

## Immediate admitted run

Train the complete released RAPT forward-dynamics architecture for **100 epochs on Q1, seed17, raw inputs only**, with normal-development checkpoint selection. Use the unchanged author `train_rapt`, `RaptModel`, Gaussian NLL objective and `score_sequence` at commit `d745668ffdb0e26877b1de4c9b2126af7bda5b03`. The upstream code is BSD-3-Clause; the paper remains a 2026 preprint. Read the v0.20 `METHOD_MAP.md` for released/manuscript score and gate differences.

Bound this single run at **120 seconds wall,90 seconds CPU,1 GiB sampled memory,25 MiB output**. One thread; batch32 instead of the paper/library batch256. Retain a terminal failure; no automatic retry or shortened replacement is permitted. The command is executable after `FREEZE.json` and the synthetic-test receipt exist:

```sh
# cwd: manufacturing/
.venv-forecast-v016/bin/python research_cycles/rapt_protocol_v0.21/run.py
```

The parent task will coordinate execution sequentially with its other bounded CPU work. Preparing this protocol does not authorize the future36-fit matrix below.

## Exact normal data populations

All files are already admitted **synthetic normal** data under `local/residual_twin_v0.13/runs/pilot_001/`. The machine-readable `INPUT_MANIFEST.json` enumerates every exact filename, SHA256, episode seed, condition and role. For each plantQ1,Q2,Q3:

| Role | Exact filename pattern | Episodes | Eligible rows |
|---|---|---:|---:|
| Fit | `normal_K13_{plant}_{17,42,2026}_{normal,authorized_offset,authorized_slow}.npz` |9|9,900|
| Checkpoint/normal development | `normal_M13_{plant}_{17,42,2026}_{normal,authorized_offset,authorized_slow}.npz` |9|9,900|
| Threshold calibration, after checkpoint seal | `normal_L13_{plant}_{17,42,2026}_{normal,authorized_offset,authorized_slow}.npz` |9|9,900|

These are **task-separated normal populations**, not consecutive blocks from one real acquisition. Within each1,200-row episode, chronology is retained and rows0–99 are excluded from fitted transformations/training targets and reported scores. Independent windows are constructed only after assignment to a role. No window spans episodes or roles. Training and development each yield189 complete50-transition windows: target rows101–1150 per episode (9,450 fitted/evaluated targets); the remaining49 transitions per episode are not silently called training targets. During scoring, the recurrent state is initialized at episode row0, runs continuously through the prefix, and reports rows100–1199. Calibration uses all9,900 eligible scores with the same state policy. Episode seeds describe repeated noisy simulations, not independent physical acquisitions.

The existing100-row startup policy is retained. Statistics use only K13 rows100–1199. The loader exposes `measurements`, `commands`, `valid` only; it must reject nonfinite or missing command context. No simulator truth, attack arrays, model references or residuals enter fitting, selection or calibration. Verify all81 data hashes before execution, although the immediate run opens onlyQ1's27 normal files.

## Feature and action timing contract

Observation channels are `[q1,q2,v1,v2]`, in radians and radians/second. Action features are the protected planned `[q1,q2,v1,v2]` at the same timestamp, in native units. They are desired position/velocity supplied to the fixed low-level controller, **not torque commands** or authenticated features from a physical dataset. In the source simulator `v7_core.physical`, `command[t]` drives the transition from state`t` to`t+1`; therefore the RAPT input `[observation[t],command[t]]` and target`observation[t+1]` have the correct causal alignment. The supplied approved command must remain unchanged by measurement preprocessing. The corrupted executed command is forbidden.

At deployment, score row`t` with the prediction from row`t−1`, then retain observed state and command for the next transition. Weights, normalizer and thresholds stay fixed. Updating GRU hidden state is inference-state estimation, not parameter adaptation. Reset only at a declared episode boundary; never at an intervention label.

## Fitting, checkpoint selection and calibration

Architecture: width256;4residual encoder/decoder blocks each;GRU256;latent192;Gaussian mean/logvariance head with logvariance clamp±6. Optimizer:AdamW,learningrate.001,weightdecay.01,OneCycleLR over100epochs,noise.01,clip1,batch32. All stochastic final fits, if later admitted, use seeds17,42,2026. Fit a separate model for each plant.

The author loop evaluates M13 normal-development NLL every epoch, completes100epochs, then restores the first minimum-development-NLL checkpoint. Save the entire train/development curves and selected epoch. This does not use attack labels or calibration. The last epoch and a best-development checkpoint are not interchangeable; do not state that the final-epoch checkpoint was selected when it was not.

Seal selected weights, fitted K13 statistics, configuration, history and selection metadata **before opening L13 calibration**. The normalizer maps observations to training mean/std; std floor1e−6 is the upstream rule. Raw planned command features remain unstandardized as in the author forward-dynamics loader.

The released score is `ell_i=(target_i−mu_i)^2/exp(logvar_i)`, although its function is named `nll_per_dim`. The training loss additionally includes half the logvariance. Calibrate the released gates on L13 eligible rows only: local`max_i+2(max_i−median_i)`; global`max_t mean_i ell_ti+3 std_t mean_i ell_ti`; optional range`min−range,max+range`. Implement only this warmup-population adapter; retain all original score/gate arithmetic. Do not run the upstream default calibrator on warmup rows. Emit separately named model-only and hybrid scores without selecting between them. A later paper-formula gate branch must be separately registered, not substituted after results.

## Learning-adequacy evidence and decision

The100-epoch run can establish that the configured training is executable and show whether the normal-development curve is still improving. It cannot certify global optimization, detector usefulness or sufficient training for every plant/seed. Record first/last/best losses; selected epoch; first20 versus last20 minima; absolute relative improvement using denominator`max(abs(first20minimum),1e−8)`; and a flag for a best checkpoint after epoch90. Report curves and flags rather than relabeling a fixed epoch count as convergence. A late optimum or material late improvement means training adequacy is unresolved. No learning-rate/epoch extension follows automatically from this run.

## Future finite preprocessing matrix — proposed, not authorized for execution here

After the root's separate normal-only estimator study selects one coupled window, one matched uncoupled window, and one ordinary constant-acceleration Kalman setting, freeze **four preprocessing families ×3plants ×3seeds=36fits**: raw, coupled endpoint, uncoupled endpoint, CA-KF. Windows are5or9; KF search is the root's declared finite noise grid. No new grid or preferred seed may be chosen from attacks. Prefer one family-selected setting shared over the three plants unless the normal-only protocol prospectively justifies separate settings.

For each family, transform each episode causally, then fit that family's observation statistics on K13 only, and train/calibrate/evaluate consistently. Transform inputs and targets consistently if preserving the complete author data interface. Because projected targets can have less measurement noise, **do not rank preprocessing families by their own transformed-target RAPT NLL/RMSE**. Select the estimators by a shared raw next-observation prediction target on M13. Separately retain raw-target predictive diagnostics if filtered-input/raw-target training is later implemented; that variant modifies the author window adapter and is not the same comparison.

Required software checks include prefix invariance, episode reset, constant-offset preservation, quadratic trajectory consistency, no command/label access, training-only variance estimation, unchanged selected transforms under calibration perturbation, valid masks and strict threshold alignment. The ordinary CA-KF and uncoupled estimator are necessary because the proposed endpoint estimator is standard weighted least squares. This study does not claim new estimator mathematics.

## Resource estimate and scope

The measured one-epoch call took.803s including setup; internal epoch.4s. A conservative extrapolation is80.3s training per fit before development/calibration, with ample single-run uncertainty. The120s single-fit bound resolves that feasibility directly. Nine raw plant/seed fits would be roughly12minutes at that conservative extrapolation; all36fits roughly48minutes before validation and calibration. Thus the full matrix is substantial training and needs a concrete aggregate run decision/approval; the current single-run authorization does not silently expand to it. No paid compute, public upload or physical setup is needed for the admitted run.

This extends a complete detector component under a new data protocol. It is not a full reproduction of the G1 paper, evidence of a cyberattack advantage, or a novelty finding. No old exposed final test is revisited.
