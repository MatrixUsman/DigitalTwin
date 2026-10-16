# IT-DT: understanding the method and its missing implementation

Prepared **16 October 2026** for the water project. Source: Kreso et al., [arXiv:2603.01621v1](https://arxiv.org/abs/2603.01621v1), [local six-page PDF](artifacts/papers/IT_DT_arxiv_2603.01621v1.pdf) and [original TeX](artifacts/source/arxiv_v1/Manuscript.tex). **This is an explanatory specification, not author code or a tested implementation.** The paper is a verified preprint; numerical baseline admission remains on hold under the [verification report](VERIFICATION_REPORT.md).

The method predicts measurements using an estimated process state, measures prediction errors, and asks whether recent errors have a different joint distribution from the normal reference. Its useful teaching distinction is between a changing estimate of the current process and a changing definition of normal behavior.

## Reading prerequisites and notation

First understand vectors/matrix multiplication, a time-series index, mean/covariance, Gaussian distributions, and training versus calibration versus testing. Covariance describes how two quantities vary together; a residual is an observed value minus its prediction. A Kalman filter combines prediction with measurement correction. These concepts explain the pipeline without requiring us to accept its experimental claims.

| Symbol | Meaning in this paper | Important boundary |
|---|---|---|
| `u_t`, length `m` | Control input at time `t` | Actual columns and trusted-input assumptions are unspecified. A logged actuator value is not automatically an authenticated command. |
| `y_t`, length `p` | Observed measurement vector | This is what the detector receives, potentially corrupted. |
| `x_t`, length `n` | Unobserved system state | Identified latent coordinates need not correspond directly to individual tank levels. |
| `A`, `B`, `C` | State transition, control effect, measurement mapping | Dimensions are `n×n`, `n×m`, `p×n`; fitted offline in the stated method. |
| `Q`, `R` | Process-noise and measurement-noise covariance | These describe assumed uncertainty, not known attack statistics. |
| `K`, dimension `n×p` | Steady-state Kalman gain | Sets how strongly the measurement corrects the state. |
| `r_t`, length `p` | Innovation, or prediction residual | Computed from the prediction before incorporating the current observation. |
| `Σ`, dimension `p×p` | Normal innovation covariance | Distinct from both noise covariance `R` and state uncertainty `P`. |
| `W`, `d_t`, `τ*` | Residual-window length, score, alarm threshold | `W=60` means samples; seconds require the missing sampling specification. |

Notation follows Section III-A, Eqs. 1–5, PDF p. 3; TeX lines 131–170. [Versioned source section](https://arxiv.org/html/2603.01621v1#S3.SS1)

## From normal recordings to a fixed model

The plant model is `x_(t+1)=A x_t+B u_t+w_t` and `y_t=C x_t+v_t+a_t`. The attack vector `a_t` expresses additive measurement corruption in the formulation; the detector does not receive its true value. Neither equation supplies an explicit actuator-attack model. A benchmark containing broader attack types therefore needs a clear account of what the model observes and assumes trustworthy. [Section III-A, Eqs. 1–2, p. 3; TeX 133–143](https://arxiv.org/html/2603.01621v1#S3.E1)

The paper says N4SID identifies the state-space matrices and noise covariances from normal recordings, with state orders 12 for SWaT and 25 for WADI chosen from Hankel-matrix singular values. Conceptually, subspace identification uses aligned histories of controls and observations to estimate a compact dynamic representation. Singular values help assess how many state dimensions to retain; they do not identify physically meaningful states automatically. The manuscript does not give the library, block lengths, numerical cutoff or fitted matrices. [Section III-A, p. 3; TeX 143–150](https://arxiv.org/html/2603.01621v1#S3.SS1)

Before implementing this stage we would need the exact files, ordered control/output columns, time alignment, units, missing-value treatment and chronological fitting interval. Many identification routines expose additional choices, including a direct-feedthrough matrix `D`; the paper's measurement equation has no `D u_t` term. Introducing one silently would change the specified model. The initial state, estimator covariance and steady-state gain calculation also remain unresolved. See [DATASETS.md](DATASETS.md).

The Gaussian reference is `P_0=N(0,Σ)`, with `Σ=C P_pred Cᵀ+R` in the manuscript. `P_pred` denotes uncertainty in the predicted state; it is not the state vector itself. The description leaves unclear whether the final reference covariance is taken directly from that theoretical expression, estimated from training residuals, or reconciled between them. A zero mean is an assumption; centering data or residuals is an additional implementation choice requiring documentation. [Section III-A, p. 3; TeX 170](https://arxiv.org/html/2603.01621v1#S3.SS1)

## What happens when one measurement arrives

Suppose the previous corrected estimate is available and the next control/measurement pair is correctly aligned:

1. **Predict the current state:** `x_pred=A x_previous+B u_previous`. This moves the model forward before looking at the new measurement. [Eq. 3, p. 3; TeX 154–156](https://arxiv.org/html/2603.01621v1#S3.E3)
2. **Predict the measurement and form the innovation:** `y_pred=C x_pred`, then `r=y-y_pred`. An unexpected observation produces a residual, but a residual alone does not prove an attack; noise and model error also contribute. [Eq. 4, p. 3; TeX 158–162](https://arxiv.org/html/2603.01621v1#S3.E4)
3. **Correct the state:** `x_corrected=x_pred+K r`. The paper applies this correction unconditionally, including when the incoming observation may be malicious. [Eq. 5, p. 3; TeX 164–168](https://arxiv.org/html/2603.01621v1#S3.E5)
4. **Append the innovation to the trailing buffer.** Keep the most recent `W` residual vectors. Algorithm 1 produces no KL score until the buffer is full. Startup positions therefore need an explicit unscored mask, not invented zero anomaly scores. [Algorithm 1, p. 4; TeX 244–257](https://arxiv.org/html/2603.01621v1#S4)
5. **Estimate the recent residual distribution, score it and compare with the threshold.** The score belongs to the window ending at the current timestamp. No future observation is needed by the written algorithm.

These steps are a conceptual trace, not callable functions. There is no verified author file/function implementing any step in this collection.

## Why a window distribution is scored

The paper fits a Gaussian to the trailing residual window. It specifies maximum-likelihood estimation; under the usual Gaussian MLE, this means a sample mean and covariance with denominator `W`, not the unbiased denominator `W−1`. That denominator follows mathematically from the stated estimator, but remains unconfirmed in author code. [Section IV-A, pp. 3–4; TeX 195–203](https://arxiv.org/html/2603.01621v1#S4.SS1)

Write the regularized window covariance as `S_t=Σhat_t+εI`, using a separate symbol here to make the regularization visible. The paper uses `ε=10^-4`. Adding a positive diagonal prevents singularity when the empirical covariance has insufficient rank. With 127 dimensions and 60 centered samples, its unregularized rank cannot exceed 59. Regularization addresses matrix conditioning; it does not make a non-Gaussian distribution Gaussian. Its magnitude depends on measurement scaling, which is not specified.

The KL direction is **recent window → normal reference**:

`d_t = ½ [ trace(Σ⁻¹ S_t) − p + μhat_tᵀ Σ⁻¹ μhat_t + logdet(Σ) − logdet(S_t) ]`.

This is Eq. 6 with the covariance regularization made explicit. Reversing the distributions changes the score. The mean term measures displacement relative to normal uncertainty; the trace and determinant terms together compare spread and correlation structure. Consequently, two windows with similar per-channel means may receive different scores if their cross-channel relationships change. With identical Gaussian parameters the formula gives zero. In finite windows, estimation noise and regularization generally prevent exact equality. [Section IV-B, Eq. 6, p. 4; TeX 225–230](https://arxiv.org/html/2603.01621v1#S4.E6)

A future implementation would normally use stable matrix solves and log determinants rather than naively computing determinants/inverses. Those are proposed numerical choices, not recovered author procedures. The claimed quadratic per-step cost cannot be assumed without specifying how the changing covariance determinant is updated. See verification finding IT-05. A score based on these moments cannot promise detection of every attack, including manipulations that preserve the monitored residual moments.

## Calibration and the decision rule

Section IV-C takes a threshold from attack-free validation scores at the empirical 99th percentile, targeting `α=.01`; Algorithm 1 alarms when `d_t>τ*`. Eq. 7 defines the inverse empirical cumulative distribution. For `M` sorted scores, its mathematical order-statistic interpretation is the score at one-based rank `ceil(.99M)`; an interpolating software percentile default may differ. Ties and the strict comparison must be preserved. [Eq. 7 and Algorithm 1, p. 4; TeX 234–255](https://arxiv.org/html/2603.01621v1#S4.E7)

This target describes calibration behavior; it is not a demonstrated 1% false-alarm guarantee on future dependent or shifted data. Calibration must replay the same model, preprocessing, windows, warm-up and reset policy used at evaluation.

Window selection remains unresolved. The manuscript selects 60 from `{30,60,120,240}` and presents validation F1 across ten chronological folds, but describes threshold validation as attack-free. Nonzero attack-class F1 requires attack examples; different development/calibration sets may have existed, but their provenance is absent. We must not fill that gap by searching held-out attacks for the best window. [Section IV-A/Figure 2 and IV-C, p. 4; verification IT-03](VERIFICATION_REPORT.md)

## Conceptual implementation contract

**No matched author source file or function is available for any row.** This table specifies the information an eventual independent implementation would require; it does not create modules, invent repository paths, or approve a runnable configuration.

| Stage and paper anchor | Required inputs → outputs | Retained state and unresolved choices |
|---|---|---|
| Dataset preparation; III-A | Authorized raw recordings plus timestamps/schema → aligned `u`, `y`, episode boundaries | Release, columns, offsets, scaling, gaps, channel exclusions and train/calibration intervals unknown. Labels must stay outside the detector. |
| Identification; III-A | Normal fitting sequences plus model-order rule → `A,B,C,Q,R` | Retain fitted transformations/configuration. Library, block size, deterministic settings and identification details missing. |
| Estimator/reference setup; III-A | Fitted model/noise plus initialization → `K`, `Σ`, initial state | Steady-state solution, initial covariance/state, reference estimation, positivity checks and resets unresolved. |
| Predict/innovate/correct; Eqs. 3–5 | Previous state, previous control, current observation → prediction, residual, corrected state | Retain corrected state. Define timestamp alignment, missing readings, episodes and whether previous control is actually available. |
| Window estimate; IV-A | Trailing residuals and `W,ε` → mean, regularized covariance, coverage mask | Retain buffer or equivalent sufficient statistics. Estimator convention is implied; numerical/update implementation is absent. |
| KL score; Eq. 6 | Window moments plus fixed reference → one scalar score | Retain stable reference factorization if used. Numerical tolerances and determinant updates require decisions. |
| Threshold calibration; Eq. 7 | Eligible normal calibration scores → fixed `τ*` | Retain partition/score provenance and quantile rule. Independence from fitting/window selection remains unresolved. |
| Alarm/evaluation; Algorithm 1, Section V | Timestamped eligible scores plus fixed threshold → alarms; labels enter only separate final scoring | Record warm-up exclusions, event matching, missed events, delay and false-alarm denominators. Published aggregation details are incomplete. |

## What changes online—and what a gate would change

The **current state estimate** changes each step. The **residual buffer** changes as new errors arrive. In contrast, the written method does not refit `A,B,C,Q,R`, update the normal reference `Σ`, or recalibrate `τ*` online. A changing window describes recent evidence; it does not itself redefine that evidence as normal. [Algorithm 1 and conclusion, pp. 4, 6; TeX 244–258, 390](https://arxiv.org/html/2603.01621v1#S4)

Algorithm 1 corrects the state before producing the KL alarm, but its current residual was already calculated from the prior prediction. Therefore, the same observation is not used twice to erase its own current innovation. It can influence **subsequent** predictions through the corrected state. Computing the score before committing an otherwise identical unconditional correction would preserve the mathematical sequence of states and scores, assuming no other dependencies; this is an ordering observation, not an implemented patch.

A gate that rejects or downweights that correction changes the estimator and future residual distribution. A gate that instead protects parameter updates, reference calibration or threshold updates governs a different operation—one absent from the paper's online algorithm. These alternatives must not be treated as equivalent or labelled faithful reproduction. Removing suspicious residuals from the detection window also changes the evidence being scored; excluding data from an accepted learning history is a separate decision. Any eventual gate would require contemporaneously available evidence, explicit uncertainty handling and recalibration for its changed residual process. No true test label can decide an update.

## What to learn before proposing a reimplementation

This paper offers a compact way to learn state estimation, residual diagnostics and distribution-based alarms. It does not supply a calibrated hydraulic simulator or validate every identified coordinate as a physical state. It also does not establish that our provisional adaptation mechanism is new.

The [verification hold](VERIFICATION_REPORT.md) remains: the plotted alarm/threshold discrepancy, conditional F1 arithmetic question, ambiguous calibration, statistical-endpoint mismatch, missing code and unidentified releases prevent dependable numerical comparison. Related repositories must not be substituted merely because they involve the same author or water systems. The bounded code check on 16 October inspected the arXiv record/full text, exact-title/identifier searches, 39 public repository names/descriptions and selected author READMEs; no matched implementation was established. This stage reuses that recorded search rather than repeating it.

An implementation derived from equations would be **our independent reimplementation**. Using a new calibration/split policy would additionally be a **modified-protocol evaluation**. Recovering author code later would still require version/configuration matching and issue resolution before a faithful reproduction claim.

Researcher reading questions:

1. Which quantities are observed, estimated, fitted offline and changed online?
2. Why must the innovation use the predicted state rather than the already-corrected state?
3. What does covariance add beyond separate channel thresholds, and which attacks remain indistinguishable?
4. Why are `W` samples, a 99th percentile and a 1% future false-alarm rate different concepts?
5. Which exact operation would our proposed gate protect, and how would that alter calibration?
6. Which missing choices must be resolved before two implementations can be compared fairly?

Source coverage: the full local v1 manuscript and TeX were read, with close mapping of Section III, Section IV, Algorithm 1 and the Section V–VI claims. This is an AI-assisted source explanation; it does not mark any researcher as having read or understood the paper. No detector code, models or scientific tests were executed for this document, and no experimental result was generated. Local link targets, source HTML anchors and whitespace were checked.
