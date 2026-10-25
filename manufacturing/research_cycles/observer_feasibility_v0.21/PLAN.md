# Normal-only observation representation feasibility v0.21

19 October 2026. Manufacturing. All data in this study are explicitly synthetic. This is a finite normal-only mechanism admission test, not a cyberattack benchmark or a claim of a new estimation algorithm. Preserve v1.7, all old criteria and exposed outcomes.

## Question and mechanism

Can causal joint position/velocity consistency reduce current-state error and uncertainty in the protected-reference residual beyond ordinary smoothing and a constant-acceleration Kalman filter? The diagnosed v0.19 unknown-band entry/re-entry weakness cannot be repaired merely by relabeling unknown motion. This experiment changes observation estimation, with the nominal reference and alarm logic held fixed. Weighted local polynomial estimation and Kalman filtering are established methods; an empirical benefit does not establish algorithmic originality.

## Inputs, finite selection and calibration

Use already admitted synthetic task-separated normal records: K13 training, M13 development, L13 calibration, nine episodes per plant Q1/Q2/Q3. These are separate task episodes, not consecutive chronological partitions of one acquisition. Preserve time order and episode boundaries. Warmup 100 rows. Fit weight variances on K13 only, using third differences of position (noise variance factor20) and second differences of velocity (factor6), Gaussian MAD constant0.6744897501960817. This explicitly supersedes the v0.20 second-difference-only prototype in a new module; old files are unchanged. These are working independent-noise estimates, not certified measurement covariances. Nonfinite/zero scales fail.

Roster: raw observations; trailing mean with w={5,9}; uncoupled endpoint quadratic-position/linear-velocity polynomials w={5,9}; coupled endpoint quadratic-position/linear-velocity polynomials w={5,9}; ordinary steady-state constant-acceleration Kalman filter with continuous white-jerk covariance. Its training jerk-density estimate is the squared robust difference of K13 coupled-w9 acceleration, divided by dt. Select a multiplier from {0.01,0.1,1,10}. This larger KF grid protects against a deliberately weak control. No nonlinear robust weighting, attack-aware reset or alarm state extension is introduced.

Select one setting per family/plant by mean squared **one-step-ahead observed prediction error** on M13, standardized by the frozen base model's four channel scales. Ties choose the lower numeric setting. Predictor at t may use observations through t only; the t+1 observation is a normal development target. Raw/mean predict with current velocity and zero acceleration; polynomial/KF use their fitted acceleration. Save selected settings before opening L13. No hidden state, attack or old final outcome selects settings. L13 sets a separate global99th-percentile residual width for each selected family against the unchanged base ARX reference; it does not choose methods or settings.

## Prospective normal transfer, declared before generation

Two new analytic command families: an arctangent of sine and a sum of alternating Gaussian motion pulses. Six noise/task combinations on each of three previously modeled plants with fixed unseen parameter shifts (mass multipliers1.07/0.92, damping0.93/1.08, lag+0.006s), three noise seeds17/42/2026:54 episodes,1500 rows each,dt0.02. No attack or unauthorized command appears. Noise cases: independent Gaussian; Gaussian AR(1),rho0.65 with the same marginal scales; quantized encoder position (step0.0001rad) with velocity from its backward difference. The last case has correlated errors and an effective timing mismatch; treating q/v as independent can fail. It is a stress test, not a validated robot sensor model. No extra candidate is added after exposure.

At fixed parameters, compare estimated state with evaluator-only noiseless simulated state, and compare the fixed ARX reference with that state. Report scaled RMSE, maximum per-channel error, normal alarm occupancy and starts under the unchanged global interval state machine (delta0.1), residual-width coverage and uncertainty-band occupancy. State truth never enters the estimator, reference, fitting, selection or calibration. Scores and estimated states are saved before a separate evaluator joins truth. A double-substep check on the first fresh normal trajectory must have max state discrepancy<1e-4 native units; otherwise fail, preserve outputs and do not interpret transfer results.

## Decision, declared before outcomes

This is a feasibility gate, not a revised success claim for v0.19. Admit the coupled representation to later attack investigation only if its pooled standardized state RMSE is **strictly lower than each** of raw, mean, uncoupled and KF, and it is no worse than either uncoupled or KF within **each** noise regime. Also require no increase in pooled benign alarm points versus raw under the common fixed readout. The scientific purpose is to determine whether coupling contributes beyond matched ordinary estimation, without selecting a favorable noise model. No arbitrary industrial safety margin or significance claim is assigned to this finite grid. Failure rejects this candidate for further attack exposure in this cycle. Retain all families/strata, even if a simpler method wins. A pass would justify a separately specified attack study, not prove novelty or recovery superiority.

## Budget and provenance

One supervised local attempt:180s wall,120s CPU,1GiB sampled RSS,50MiB output. No neural training, paid resources or system installation. Bind sources, all consumed old model/normal records, configuration and interpreter before the attempt. Record commands/cwd, revision/dirty state, dependency versions, selected parameters, source/data hashes, timing, failures and output hashes. No automatic retry. Raw real datasets remain unopened.

Working directory `manufacturing/`; command after tests and freeze:

```sh
.venv-reproduction-v02/bin/python research_cycles/observer_feasibility_v0.21/run.py
```
