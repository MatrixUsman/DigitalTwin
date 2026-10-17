# Noise-aware return control: implementation and normal feasibility

17 October 2026. Prepared before generating the study signals. Scope: the user's resume instruction continues the manufacturing recovery-mechanism work. This is a small, local, normal-only diagnostic; the consumed v0.11 training authorization is not reused.

## Material passport

- Project: manufacturing; owner: Haiqa Mushtaq; operator: Codex.
- Type: implemented standard statistical control and explicitly synthetic residual experiment.
- Inputs: generated residuals only. No CASPER observations, saved CNN predictions, attack recordings, protected tests or robot simulator are loaded.
- Outcome: test whether a mathematically explicit treatment of noise can certify ordinary within-tolerance return under its stated assumptions. No novel detector or attack-performance claim is tested.
- Skill: academic-research-suite, bounded experiment/validation guidance, applied inline under project rules.

## Formula and assumptions

For each of four dimensionless channels, `e_t = delta_t + b_t + epsilon_t`, with `|b_t| <= B`, `|delta_t - delta_(t-1)| <= L`, and a known stationary zero-mean Gaussian AR(1) noise process of marginal standard deviation sigma and nonnegative correlation rho < 1. Independent noise is rho=0. Across-channel independence is unnecessary for the union bound. This specification does not cover arbitrary heavy-tailed, nonstationary or feedback-dependent measurement noise.

For a registered trailing window m, define

`V_m = sigma^2 * (m + 2 * sum((m-k)*rho^k, k=1..m-1)) / m^2`.

This is the exact variance of a stationary Gaussian AR(1) window mean. Use the Gaussian/sub-Gaussian tail and triangle inequality:

`U_t(m) = |mean(e_(t-m+1):e_t)| + B + sqrt(2 * V_m * log(2*d*K/alpha_t)) + L*(m-1)/2`,

where `alpha_t = 6*alpha/(pi^2*t^2)`, d=4, K=3, alpha=0.05. The global sample clock never restarts after an alarm or missing observations. Only a new independent trace starts at one. The error contract is per trace, not a 95% guarantee for all 36 traces combined. All three windows share the error allocation; overlap does not require independence for this union bound. On the simultaneous coverage event, every channel's current absolute physical deviation is bounded for every registered window/time. Declare a return certificate when `min_m U_t(m) <= tolerance` in every channel. Different channels may select different windows because all bounds are simultaneous. This is standard multiple-comparison accounting, not a new algorithm.

The drift term follows `|delta_t - mean(delta_window)| <= L*(m-1)/2`. Dropping it changes the target from current deviation to a window average. Dropping temporal correlation can understate uncertainty. Do not treat ordinary conditional mean-zero martingale formulas as valid for raw correlated AR(1) noise.

All uncertainty inputs are **known generator parameters** in this diagnostic. They are oracle-informed assumptions, not estimates obtained from commissioning data. No operational guarantee, dynamics-aware contribution or robust robot performance follows.

## Frozen design

- 36 traces: 4 noise settings × 3 within-tolerance deviation profiles × seeds 17,42,2026. Each has 1,200 samples, four channels; common reporting support is samples 201–1,200 (1,000 endpoints).
- Noise settings: (sigma,rho)=(0.03,0),(0.06,0),(0.03,0.8),(0.06,0.95); channel sigma multipliers [1,0.8,1.1,0.9]. AR(1) initialization is drawn from its stationary marginal, not set to zero.
- Deviation profiles: zero; 0.02*sin(0.004*t+channel phase); 0.02*sin(0.04*t+channel phase). These remain within tolerance 0.1. L=2*amplitude*abs(sin(frequency/2)), derived before execution. Bias=0.01*cos(0.003*t+channel phase), B=0.01. The phases are 0,0.4,0.8,1.2 radians. These are residual-level scenarios, not physical robot trajectories or authorized-change recordings.
- Registered valid controls: instantaneous m=1, fixed m=41, fixed m=201, and simultaneous multiwindow envelope. Two deliberately misspecified controls assume rho=0 for m=41/201; label them invalid under correlated noise, regardless of observed outcomes. They illustrate a tempting but unjustified shortcut.
- All six variants receive identical residuals and the same nominal parameter contract; the misspecified controls explicitly discard its rho. No tuning, fitting, threshold search or model selection follows the outcomes. All 216 method/trace outcomes are retained.
- Primary normal-feasibility diagnostic: at least 95% of common endpoints certified on **every** trace by the simultaneous envelope. Report a pass/fail per condition and overall; do not lower this criterion after results. Passing would admit only this conditional residual control, not the entire recovery mechanism.
- Report certificate count/fraction, channel-bound coverage violations, any-violation trace indicator, first certificate on common support, score time, resource use and failures. With every trace within tolerance, these are not attack recall, false alarm rates, or recovery delays. Samples and seeds are not independent robot acquisitions. No significance tests or population confidence interval from these 36 constructed traces.

## Implementation and verification

Pure causal functions receive residuals, validity flags, a fixed parameter contract and global start time. Invalid/gapped measurements invalidate each affected window; they never reset the error clock. Nonfinite valid observations fail closed. Tests cover independent covariance arithmetic, current-versus-average drift, future isolation, gaps, budget allocation, malformed inputs, no mutation and exact independent-noise equivalence. Synthetic software tests are separate from the generated feasibility traces.

Freeze sources/configuration, passing test receipt, dependency versions and prior-package identities before one run. Use the existing tested supervisor: 120 seconds wall, 60 seconds CPU, 512 MiB sampled RSS, 20 MiB output. No paid compute, neural training, package installation, external contact or publication. Preserve any failure; no automatic retry. RSS is sampled, not an instantaneous memory ceiling.

Commands from the workspace root, in order:

```sh
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/return_bound_v0.12/freeze.py --test-attempt test_002
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/return_bound_v0.12/run.py
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/return_bound_v0.12/verify.py
```

The verifier recomputes bounds independently from saved residuals and a covariance sum, checks truth only for evaluation, checks every saved outcome and hash, and verifies old packages unchanged. No claims about CASPER superiority or publication readiness are admitted. Closest prior-art gaps remain in [PRIOR_ART.md](PRIOR_ART.md).
