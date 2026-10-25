# Finite normal-only feasibility pilot

24 October 2026. Proposed, not executed. Manufacturing only. Root requested implementation and independent review before a single scientific pilot. The theorem itself is familiar prior art; this stage tests practical value of constrained nonlinear correction against strong ordinary controls. It does not establish originality, cyberattack detection, physical recovery or journal readiness. Preserve v1.7, sealed v0.22 and every earlier failure.

## Common data and information

Only the existing exposed Q1 K13 normal-development population is admitted for fitting: three conditions (normal, authorized_offset, authorized_slow), three noise seeds, nine episodes of 1,200 rows. The corresponding nine M13 episodes are development. They are different synthetic tasks, not chronological slices or independent robots. Read only `measurements`, `commands` and `valid`; no simulator state, paired truth or attack labels. All conditions are authorized nominal operation. L13 is excluded entirely, including calibration; no original physical data or test signals are opened.

K13 rows 100:1200 fit separate command/observation means and population standard deviations with floor 1e-6. All subsequent models use these frozen scales. Fit a common command-only FIR with 16 preceding-command lags and ridge 0.001, plus an unpenalized intercept, to all eligible K13 targets. Prediction at t uses commands t−1 through t−16; it has no measured initial state, phase, alarm or adaptation path. Use zero-padded normalized commands only before the earliest lag; all scoring begins at row100. No reference hyperparameter selection occurs. This is a fitted command-response model, not a physical twin validation.

Every expected validity flag must be true and every permitted observation/command must be finite with exact1,200×4 shape. Reject an episode with any gap or invalid flag; do not interpolate, continue state across an unknown gap, drop rows or change the roster silently. These generated normal populations are expected complete, so a violation blocks this pilot rather than changing its scientific meaning.

Trusted context is the four normalized command channels at t−1 and their first difference, eight features. Candidate and controls share this context and base reference. Define z=y−b in fixed training-normalized units. Score scale is fixed at one for this feasibility stage; no learned variance or scale choice is allowed.

## Finite roster

- Six width8 causal tanh adapters: kappa in {.25,.5,.75}, rho in {.25,.75}, seed17. Use z_(t−1), the trusted context and a hidden state starting at zero each episode. Enforce actual row-sum limits `||Wh||∞<=rho`, `||Wz||∞<=1−rho`, `||Wo||∞<=kappa` after initialization and every optimizer step, with 1e-6 numerical slack. This guarantees complete history gain at most kappa and absolute observation-adapter amplitude at most kappa; both actual norms and budgets are reported.
- Two same-width command-only tanh adapters (one per rho), Wz fixed zero, same epochs/optimizer/context and base reference. These isolate command-only nonlinear capacity. Their output weights are unrestricted: imposing a small observation-adapter amplitude cap on a trusted command-only predictor would unnecessarily weaken this control. They have observation gain zero; their context-dependent output is common under paired paths and is not charged as an observation-dependent amplitude cap.
- One same-width unconstrained tanh diagnostic with the same initialization/40-epoch optimizer budget; do not call it RAPT or a published-method reproduction. Report a certificate only if its actual norms support one.
- Direct common FIR reference (zero correction).
- Constrained residual FIR, five preceding residual lags plus trusted context and intercept, for every kappa. Solve the convex ridge objective by projected-gradient iterations with exact per-output l1-ball projection over all residual lags. This uses the exact history-infinity norm (maximum row absolute sum across all lags); it is less restrictive than summing per-lag matrix norms. Report convergence residual; an unresolved control solver blocks advancement.
- Additive command-only-tanh plus constrained FIR: both command-only rho variants × all three kappas, fitted on K13 with the same residual/context access. The FIR predicts residual remaining **after** the frozen context-only correction, using the preceding residuals relative to that corrected reference. This prevents nonlinear command modeling plus a simple residual filter from being omitted as an explanation.
- Leaky filters for all six kappa/rho pairs: `a_t=rho*a_(t−1)+(1−rho)*kappa*z_(t−1)`. Same clean initialization and no labels/reset trigger.
- Unconstrained residual FIR with trusted context/intercept, plus saturated versions at observation-dependent amplitude caps {.25,.5,.75}. For cap controls clip only the residual-dependent correction; leave the command-only part outside the cap, since it cancels under paired-path comparison. The nonlinear adapter’s cap is also included when calculating its best supported radius.
- Four ordinary steady-state scalar Kalman filters for the four residual channels, random-walk process/measurement ratio {.01,.1,1,10}. Score against the prior estimate before update, initialize state to zero and reset only at episode start. These ordinary adaptive baselines have complete history gain one, so no finite gain-only plateau radius follows. Report predictive errors and uncertainty honestly; do not deliberately make them rigid.

All fitted linear/context terms, predicted streams, loss histories, settings and outcomes are retained. No preferred variant is chosen from attack outcomes.

## Training and causal evaluation

Neural fits use deterministic CPU float32, one thread, 40 full-batch Adam steps/epochs at learning rate .01 and weight decay 1e-4. Training windows are 96 rows: 48 causal burn-in rows and up to 48 scored targets. Windows stay inside episodes, have disjoint scored targets covering eligible rows, and do not cross populations. Their hidden state starts at zero at the window start; the burn-in reduces, but does not eliminate, the mismatch with full-episode deployment state. Report this approximation. Save every epoch's training and development **window** MSE, but select no epoch: retain final fixed-epoch weights. The final comparative metrics use full-episode states. Flag unresolved optimization if training window loss improves more than1% from epoch31 to40; a flagged failure concerns this configured budget, not an optimized method's general inability. K13 trains; M13 selects only among the finite fits.

Full-episode prediction starts hidden state at zero once and scores before consuming the target observation. All eligible M13 points are retained. No future input, measurement-derived context, label-dependent reset or online fitting is allowed. The same complete gain and amplitude analysis must include additive context paths; context-only paths cancel only because both compared streams share trusted commands.

## Frozen normal admission rule

For every method calculate global `Edev=max_(eligible t,j)|r_t,j|`, threshold `tau_dev` as the exact sorted rank `ceil(.99*N)−1` of `max_j|r_t,j|`, pooled normalized RMSE, each episode RMSE and condition-stratified RMSE. Edev and threshold both use exposed normal development and are **empirical design quantities**, not future uniform bounds or independent calibration.

Use actual certified history gain K and actual certified observation-dependent amplitude cap C where available, retaining budget values separately. The primary radius is the minimum of valid gain radius `(Edev+tau_dev)/(1−K)` and cap radius `Edev+tau_dev+2*C`. If neither certificate is available, radius is null/unbounded and the method remains a predictive-error diagnostic. For context-only methods K=0,C=0. An additive context-only correction does not enlarge C. For candidate tanh, a context-only trajectory with the same network can be nonzero; the safe total tanh-output bound C=||Wo||∞ remains valid for the complete bounded output and yields the 2C paired contrast. Both proxies are reported; selecting only the favorable formula for our candidate is forbidden.

Select the candidate by smallest primary radius, then pooled RMSE, then stable method ID. Select **one** strongest certified simple comparator (direct reference, constrained/additive FIR, leaky, saturated linear, command-only same-width controls and unconstrained FIR whenever its actual K<1) by the identical rule. Ordinary KF remains in the roster but its K=1 and absence of a finite cap exclude it from a finite-radius selection. The unconstrained neural diagnostic is excluded from the simple comparator pool but reported. Advance only if all of the following hold:

1. Candidate radius is at least 5% lower than this same selected simple comparator.
2. Candidate pooled RMSE is at least 2% lower than that comparator.
3. No individual M13 episode RMSE is more than 5% worse than that comparator, and no condition-pooled RMSE is worse by more than 5%.
4. The same candidate also beats the best same-budget-kappa constrained/additive FIR on radius and has no worse pooled RMSE. This verifies the advantage is not solely a different gain budget.
5. Every normal input/source identity, causal/norm check and linear solver convergence check passes; resource caps hold and all declared fits complete.

No physically sourced operational tolerance is available. Radius below an invented normalized .1 is therefore not an admission requirement or a claimed safety threshold. Even a pilot pass leaves operational nonvacuity, originality and fresh attack protocol admission unresolved. A failure ends this candidate's advancement; no post-result criterion changes or larger neural matrix.

## Cost and execution gate

The entire real-normal pilot, including common-reference fitting and every control, is capped at120 seconds wall,90 CPU seconds,1GiB sampled RSS and50MiB output. No paid compute, GPU or concurrent substantial run. Before GO, a separately labelled synthetic arithmetic/runtime fixture with identical tensor shapes estimates the full fit cost. It must not read K13/M13 values. Record measured time and conservative extrapolation; if expected total approaches the cap, narrow the protocol prospectively before any normal-data fit and repeat independent review.

The synthetic fixture completed in2.027s wall/0.989CPU with no research arrays. Three epochs on all207×96 windows cost0.373152CPU; batched inference of18separate episodes cost0.009558CPU. Nine neural fits plus measured reference/linear costs and an8CPU-second fixed allowance estimate52.886953CPU for40epochs, or79.3304295CPU after a50% margin. The60epoch estimate with margin is112.9141095CPU and is not admitted. Root chose40epochs before any normal-array access, superseding the initial12epoch draft saved in the synthetic timing receipt. These estimates are not guarantees; the monitor's hard cap remains decisive.

The complete roster has33methods: six candidate tanh, two command-only tanh, one unconstrained tanh, direct reference, three constrained FIR, six context-plus-FIR, unconstrained FIR, three saturated FIR, six leaky and four KF controls. Neural weights are saved both as tensors and non-pickle NumPy arrays; common normalized input/reference/context, ordered metadata and all development corrections/residuals support independent replay.

Proposed commands from `/Users/matrixusman/CUI/DigitalTwin/manufacturing`:

```sh
python3 research_cycles/gain_limited_v0.23/admit_data.py
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 .venv-analysis-v022/bin/python -m unittest discover -s research_cycles/gain_limited_v0.23 -p 'test_*.py' -v
python3 research_cycles/gain_limited_v0.23/freeze.py
# ROOT + INDEPENDENT REVIEW GO required before this one monitored scientific run:
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 .venv-analysis-v022/bin/python research_cycles/gain_limited_v0.23/run.py
```

Use the existing same-project `.venv-analysis-v022` bridge and frozen old package locations. This is not a fresh portable environment installation. New outputs belong only to ignored `local/gain_limited_v0.23/`; old data, environments, checkpoints, source and manuscripts are unchanged.

Root and independent reviewer GO are required after source, synthetic tests, runtime estimate and protocol review, before the scientific freeze/run. A failed or capped scientific run is preserved and not silently retried. No fresh attacks are authorized by this normal-only pilot.
