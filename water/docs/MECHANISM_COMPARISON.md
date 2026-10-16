# What changes online, and what could become contaminated?

Prepared **16 October 2026** from the three detailed studies: [CAROTS](../baselines/carots/METHOD_TO_CODE.md), [IT-DT](../baselines/it_dt/METHOD_TO_CODE.md), [ensemble](../baselines/dt_ensemble/METHOD_TO_CODE.md). These are source-based comparisons, not measured findings. Our title and mechanism remain provisional.

## Method roles and update semantics

| Question | CAROTS | IT-DT | Digital-twin ensemble |
|---|---|---|---|
| What produces an expectation? | Learned causal forecaster and representation of normal windows | Identified state-space model with steady-state Kalman filtering | Process-model twin with EKF, plus three learned detectors |
| What is scored? | Embedding-to-centroid distance plus forecasting error; dagger retains only the embedding score but still uses causal discovery for augmentation | Gaussian KL divergence of a recent innovation window against a fixed normal reference | Learned ensemble score fused with a covariance-weighted twin residual score |
| Is a physical process state followed explicitly? | Not a physical state-estimation twin in the audited implementation | A latent state estimate is corrected each sample; its coordinates are not automatically physical quantities | State/covariance are synchronized, but complete process files and EKF details are missing |
| What changes during online evaluation? | Input windows and scores; learned graph/forecaster/encoder are fixed in the described path | State estimate and recent residual buffer | State, input normalization, threshold and stated model/weight adaptation; exact targets/order are incomplete |
| Does recent evidence redefine the normal reference? | No online reference learning specified; centroid/score scaling derived from training | No; model, normal innovation covariance and threshold are fixed | Text describes updates from certified-normal history, but the admission implementation is absent |
| Who declares observations clean enough to learn from? | Training is assumed normal; synthetic positives rely on the learned graph | Offline fitting/calibration assumed clean; no online parameter/reference acceptance decision | Claimed certified-normal windows/recent normal data; certification criteria and mistake handling unresolved |
| Is there an alarm gate? | Scalar score threshold; no separate physics/update gate established | KL threshold | Joint-score threshold plus either a twin threshold or stricter ML threshold |
| Does that gate protect state assimilation? | Not applicable to this non-twin estimator role | No rejection rule; state correction is unconditional | No explicit rejection rule; synchronization precedes alarm gating |
| Are trusted signals independent of the measured process? | Not established by the learned graph | Control inputs are called known, but exact channels and integrity assumptions are unspecified | TLS/authentication is described; it does not establish that endpoint readings or commands are truthful |
| Are contamination/adaptation benefits demonstrated in our workspace? | No | No | No |
| What implementation evidence exists? | Pinned author source; static divergences and execution prerequisites remain | Equations/pseudocode only; no matched author implementation verified | Equations/pseudocode only; no matched author implementation verified |

## Four operations to keep separate

1. **Measurement admission and state estimation:** how a new reading changes the estimate of the current process. A corrupted correction can influence later predictions even with frozen parameters.
2. **Parameter adaptation:** how process coefficients or neural-network weights learn a new relationship. Admitting contaminated samples can change future expected behaviour.
3. **Reference/threshold calibration:** how the definition of normal residuals or tolerated discrepancy changes. Raising tolerance can suppress alarms without improving the process model.
4. **Alarm reporting:** whether a score becomes an alert. Suppressing an alarm does not prove that the same observation is safe for any of the other three operations.

Input normalization, imputation and fusion weights can also alter future scores. They belong in the adaptation inventory rather than being treated as harmless preprocessing. Source studies above identify which methods specify these operations and where the details are absent.

IT-DT illustrates why order alone needs careful interpretation: its current innovation is computed before correction, even though correction is listed before the KL decision. Reordering an otherwise identical unconditional update can be algebraically equivalent; rejecting that update changes the estimator. For the ensemble, the unknown contents of the update history prevent deciding whether the current suspicious sample is admitted. We must not turn that uncertainty into a claim that it definitely learns every attack.

## Evidence required before a trust-gating contribution

The candidate question concerns adaptation under legitimate change and measurement corruption. The three readings do not establish a complete experimental answer to it. Before implementation, specify:

- **Protected quantity:** choose one initial update target and explain why it can become contaminated. Do not silently change state, parameters and thresholds together.
- **Available evidence:** identify authenticated/independent information if any, and state what an attacker may forge. A small score or model agreement is evidence under assumptions, not ground truth.
- **Timing:** define score, decision, history admission and update order, including startup, missing readings and episode resets. No future samples or hidden labels enter the method.
- **Failure behaviour:** describe what happens when a suspicious observation is accepted, a legitimate change is rejected, evidence is insufficient, or normal operation resumes.
- **Comparison controls:** retain a fixed version, an ungated adaptive version, the gated version and relevant non-twin/closest-prior-art controls with the same information access and calibration rules.
- **Evaluation evidence:** obtain justified legitimate-change scenarios as well as attacks. Measurement perturbations are separately labelled stress tests, not automatically physically valid changes.

These are proposed research requirements, not a finalized architecture or a verified novelty claim. No score/ranking table is included because methods have not been rerun under consistent authorized releases and evaluation rules.
