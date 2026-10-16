# Reading the ensemble method: from equations to an implementation contract

Prepared **16 October 2026** for the water project. This guide explains what the authors specify, how the pieces connect, and what an implementation would still require. **There is no verified runnable author implementation for this paper.** The function names below are manuscript pseudocode, not functions found in a repository. No model was implemented or executed for this guide.

Read alongside the [version-of-record PDF](artifacts/papers/Ensemble_ScientificReports_VOR.pdf), [PMC XML](artifacts/pmc/PMC13402577.1.xml), [verification report](VERIFICATION_REPORT.md) and [experimental audit](EXPERIMENTS.md). Page numbers below refer to the 17-page VOR, not the accepted manuscript. The existing verification report controls how confidently we can use its claims; this explanatory guide does not remove the experimental hold.

## What the system is trying to do

The proposed detector asks two questions about the same plant observations. First, do they look unusual to learned models? Second, do they disagree with a process model driven by the recorded controls? It combines those answers before issuing an alarm. A sensor value might be statistically unusual during a legitimate operating change yet compatible with the process model; conversely, a carefully manipulated reading could resemble learned normal behavior while disagreeing with that model.

That is the authors' intended reasoning, not a demonstrated guarantee that these two cases can always be distinguished. The twin depends on correct dynamics, suitable uncertainty estimates and sufficiently trustworthy inputs. A coordinated attack that preserves the available consistency checks can remain ambiguous. The paper itself acknowledges limits for attacks respecting both physical and temporal normality.

**Figure 1**, VOR p. 10, XML `Fig1`, connects the physical plant to a twin and three learned detectors, then to fusion and response. Its dashed feedback paths include safe control, twin updates and learned-weight adaptation. The diagram is an architecture description; it does not establish an implemented closed-loop deployment or identify executable components.

## Process state, observations and the residual

Methods `Sec5`–`Sec7`, VOR pp. 4–5, Equations 1–7 distinguish plant state `x`, control input `u`, observed measurements `y`, noise and an additive measurement anomaly. Equation 2 supplies a linear discrete-time form; Equation 4 describes prediction through first-principles functions `f_hat` and `g_hat`. The authors name MATLAB/Simulink for SWaT/WADI and the Downs–Vogel model for Tennessee Eastman. Actual process files, fitted matrices, hydraulic parameters, actuator handling and identification procedure are absent.

The estimator is an **Extended Kalman Filter (EKF)**, not an unscented Kalman filter. It carries an estimated state and covariance forward. Before using the new observation to correct that estimate, there is a prediction of what the observation should be. Equation 6 defines the innovation as the observed value minus this prediction. Equation 5 then corrects the estimated state with a gain-weighted innovation. An updated state is not itself a newly learned process model: the distinction matters when discussing contamination.

Equation 7 converts the innovation into a covariance-weighted score, divided by the monitored-channel count. A larger score is intended to indicate a less plausible observation under the model. Its accompanying chi-square distribution statement has a scaling error documented in the [verification report](VERIFICATION_REPORT.md); it must not be copied as a valid calibration rule. The nonlinear prediction description also needs Jacobians and covariance-prediction rules to become a complete EKF; Equation 5 alone does not supply them.

The text adds linear-temporal-logic checks to residual processing (`Sec7`), but does not specify a numerical mapping from each violated property into residual components or score increments. A finite deadline is also not established by the displayed “always eventually” formula. These checks are requirements to resolve, not executable constraints we can reconstruct faithfully from the page.

## The three learned branches

Methods `Sec8`, VOR p. 5, Equations 8–10 and **Table 1**, p. 9 (`Tab1`), provide partial specifications:

| Branch | Information the manuscript supplies | What remains unspecified |
|---|---|---|
| LSTM autoencoder | Normal-sequence reconstruction; Euclidean reconstruction-error score; hidden sizes 128/64/32, latent size 16, sequence length 50, dropout .2, Adam learning rate .001 | Decoder topology, exact training loss/reduction, window stride, hidden-state resets, score alignment and conversion to `[0,1]` |
| Attention transformer | Scaled dot-product attention; four layers, eight heads, model width 256, feed-forward width 1024, AdamW learning rate .0001, 4,000 warmup steps | Input tokens/embedding, temporal versus sensor axes, prediction or reconstruction target, final anomaly-score definition, masking and attention-to-explanation procedure |
| Isolation Forest | Path-length-based anomaly score; 100 estimators, sample size 256, contamination .01 | Whether input is a point, flattened window or summary; fitting subset, implementation/version and alignment with the other outputs |

An attention equation is not a complete transformer detector. Similarly, listing hyperparameters does not identify the executable model that produced a table. All three branch scores are called normalized scores `D_i,k` in Equation 11; only the Isolation Forest expression naturally has the displayed bounded range. The other score transformations need their own fitted parameters and training/calibration provenance.

## Calibration, fusion and the alarm gate

Methods `Sec9`, VOR pp. 5–6, Equations 11–14 first combine the three learned scores using nonnegative weights summing to one. The paper reports SWaT weights `.35/.35/.30`, WADI `.40/.30/.30`, and Tennessee Eastman `.30/.40/.30`. These are author-reported settings, not weights fitted here.

The current manuscript says weight selection uses **normal-only validation**, correcting an earlier manuscript's F1-tuning wording. Its proxies are score variability over one-hour windows, calibration to a nominal .01 false-positive rate, and Spearman association with the twin residual score. However, the proxy coefficients, constraints, search bounds, treatment of near-zero means and precise optimization objective are missing. The intended interpretation of weak correlation as independent information is not a demonstrated independence result.

Equation 12 mixes the learned ensemble score and twin score with another coefficient `alpha`. The paper reuses `alpha` for different purposes, including a nominal false-alarm level and normalization; an implementation would need distinct configuration names. It also reuses `S_k` for innovation covariance and the scalar joint score. Those roles must not become the same program variable. The twin score is not inherently bounded like the learned scores, so their relative scaling needs specification before the fusion coefficient is meaningful.

Equation 13 alarms only when the joint score exceeds its threshold **and** either the twin score exceeds a twin threshold or the learned score exceeds a stricter learned-only threshold. Thus the gate has a learned-only override; it is not simply “no physical violation, no alarm.” Values and calibration procedures for those two additional thresholds and the fusion coefficient are not supplied. Table 1 gives an initial joint threshold of .68, followed by adaptation.

## What is allowed to change, and what protects it?

These operations must be considered separately. Calling all of them “trust gating” would hide the actual information flow.

| Operation | Manuscript condition | Protection that is not established |
|---|---|---|
| Measurement acquisition/replacement | TLS/X.509 transport; detected sensor failure triggers imputation from past observations using GraphSAGE and increases covariance | No rule establishes that an authenticated endpoint, control record or plausible observation is uncompromised. Failure detection is not a specified attack-admission test. |
| Current-state correction | Equation 5 assimilates each observed measurement; Algorithm 1 performs synchronization before the alarm gate | No explicit suspicious-measurement rejection, gain clipping bound or gate protecting state correction is supplied. “Bounded EKF” is not operationally defined. |
| Input normalization | EWMA with coefficient .1 adapts to drift/bias (`Sec12`) | No explicit accepted-sample condition, history rule or ordering relative to training-fitted min–max scaling is supplied. |
| Alarm decision | Equation 13 applies joint/twin/strict-ML thresholds | This controls the reported alarm, not automatically eligibility for estimator or learning updates. |
| Joint-threshold adaptation | Text says EWMA over **certified-normal windows** | The certificate/admission rule, EWMA coefficient for this threshold, buffer contents and handling of delayed or wrong decisions are missing. The .1 normalization coefficient must not silently be reused here. |
| Process/learned-model adaptation | GMM residual-likelihood drop triggers updates using recent normal data; a seven-day buffer and constraint-preserving updates are described | Parameter subset, optimizer state, certification of buffer entries, rollback and contamination checks are not specified. |
| Ensemble-weight updates | Algorithm 1 names OBAL with normal-only proxies following drift detection | Exact OBAL objective/update law and relationship to initial Bayesian weight selection are absent. “ML weights” can refer to network parameters or fusion weights in the prose; this needs resolution. |

The required trusted information is therefore unresolved. Transport authentication protects a communication channel under its assumptions; it does not prove the truth of a sensor reading. The paper does not identify an independently trusted control channel, unaffected sensor subset or external mode-change authority sufficient to certify new training observations. That is directly relevant to our research question.

## Algorithm 1: order matters

The [algorithm image](artifacts/pmc/41598_2026_53863_Figa_HTML.jpg), VOR p. 8, XML `Figa`, is the closest available orchestration specification:

1. Lines 1–8 initialize state/covariance/failure buffer, acquire measurements and controls, conditionally impute sensor failures, then normalize measurements.
2. Line 9 calls the manuscript's `DigitalTwinSync`; its arguments show the acquired/replaced `y_k`, whereas the learned models in lines 10–11 consume normalized `y_tilde_k`. The diagram's common-stream description does not settle these units or transformations.
3. Lines 13–14 compute the learned vote and joint score.
4. Lines 15–16 detect drift and update weights. Line 18 adapts the threshold. **Only line 19 evaluates the alarm gate.**
5. Lines 20–22 classify an alarm, request smoothing-based certification and send an alert. The stated outputs include confidence and explanation, but their complete computation is not specified.

This order does not implement an explicit score-then-admit-then-update protocol. It might use only previously certified history, but the pseudocode does not say so; its `S_history` membership and timing are unknown. A repair must be disclosed rather than attributed to the authors. Equation 6 requires a pre-correction prediction; the internals of `DigitalTwinSync` must retain it even though the call returns updated state and residual together.

Figure 1 includes response coordination and consensus; Algorithm 1 does not show a consensus call or safe-control branch. The text also mentions process-parameter updates that the algorithm represents only through weight updating. Smoothing appears after an alarm in the algorithm, whereas the robustness discussion describes a smoothed detector during inference. These are unresolved interface/order differences, not permission to invent missing steps. Its claimed robustness certificate has mathematical errors already documented separately.

## Conceptual implementation contract — no author functions available

The following table defines questions an eventual implementation must answer. It is **not** a mapping to existing source files and is not authorization to build a substitute.

| Component / paper anchor | Inputs → outputs; retained state | Missing executable evidence |
|---|---|---|
| Preparation / `Sec12`, `Figa` lines 3–8 | Measurements, controls, failure history → repaired/normalized inputs; fitted scales and EWMA history | Loader, channel units, imputer, failure predicate and fitting/admission rules |
| Prediction/correction / `Equ4`–`Equ6` | Previous state/covariance and control, then measurement → prediction, innovation, corrected state/covariance | Process functions, matrices/Jacobians, noise covariance, initialization and bound implementation |
| Twin scoring / `Equ7`, `Sec7` | Innovation/covariance and property checks → twin score; calibration state | Corrected distribution/scaling, numerical stability policy and property-to-score mapping |
| Learned branches / `Equ8`–`Equ10`, `Tab1` | Aligned windows → three scores and attention; models and score transforms | Complete architectures, losses, fits, saved weights and alignment |
| Fusion/gating / `Equ11`–`Equ14` | Four scores and thresholds → score/alarm; weights and thresholds | Calibration objective, selected parameters and exact comparison/coverage rules |
| Adaptation / `Equ16`, `Sec12`, `Figa` lines 15–18 | Residual history and accepted windows → drift decision/updates; GMM and seven-day buffer | GMM refresh schedule, admission certificate, update targets, ordering and rollback |
| Classification/certification / `Sec10`, `Equ17` | Alarm residual, attention and control history → attack type/confidence | Classifier training labels/data, smoothing sample count, probability bounds and valid theorem/application |
| Distributed response / `Sec11`, `Fig1` | Local detections and node messages → agreed response | Consensus implementation, threat assumptions, timing traces and safe-control integration |

The last two rows extend beyond our initial offline detection task. Byzantine agreement does not by itself establish that an agreed detector output is true. A future narrow reimplementation should explicitly name excluded components rather than claim reproduction of this entire architecture.

## Protocol audit before any numerical comparison

| Item | Published description | Required resolution |
|---|---|---|
| Releases/filenames | Dataset names and counts in `Sec14`/Table 2, pp. 8–9 | No exact provider files, revisions or hashes; no authorized local files yet |
| Cadence/downsampling | 10 Hz; 50 samples described as five seconds | Resampling/downsampling unspecified; duration/count conflict unresolved |
| Exclusions/inputs | SWaT 51, WADI 123 channels | Channel lists, startup removal, missing-channel handling, episode boundaries and label revisions absent |
| Windows | Length 50 | Stride, target timestamp, warm-up coverage and crossing of gaps/splits absent |
| Validation | SWaT day 8 normal-only; WADI day 12; TE hours 33–36 | SWaT conflicts with the provider's seven-normal/four-attack-day description; timestamps/filtering absent |
| Thresholds | Initial .68, adaptive EWMA, nominal .01 calibration | Gate thresholds, fusion scaling and normal-certification implementation missing |
| Checkpoints/tuning | Early stopping; 500 TPE trials; 48-hour budget | Monitoring/stopping/selection rule and saved configurations absent; Gaussian-process narrative conflicts with TPE wording |
| Fusion | Dataset-specific branch weights; normal proxies | Full search objective, selected mixing coefficient and online weight-update rule absent |
| Metrics | Tables 3–6 and Figure 3; ten runs; bootstrap intervals | Point adjustment/coverage unspecified; FPR issue unresolved; scores/confusion counts/interval construction unavailable |
| Test-label access | Text says test attacks used only for evaluation | Cannot verify unreleased implementation; normal-only test-window selection for added perturbations in Table 7 is a separate constructed evaluation, not deployable adaptation information |

Table 7's added perturbations must stay separate from unchanged SWaT/WADI attack evaluation. Keeping values within sensor ranges does not establish physically achievable plant operation. Published latency is also distinct from attack-detection delay and the acquisition time needed to form a window.

## Why read this paper now?

It is close prior art because it already combines a twin, alarm gating, normal-data calibration, drift detection and online updates. Therefore, merely proposing “an adaptive twin with a gate” would not establish novelty. Our narrower question concerns **which observations may change which state, on what evidence, and what happens when that evidence is wrong**.

The bounded code-status audit on this date checked the publisher, exact-paper searches and 16 public repositories on the identified author's account; no matched implementation was verified. See [the evidence record](VERIFICATION_REPORT.md#code-and-experimental-readiness). Nearby repositories describe other papers. No new external search was needed for this same-date reading pass; no additional repository or code availability is claimed.

A useful researcher-owned reading outcome is an explanation of Equation 13 and a trace of one observation through all six update categories above. Then list what evidence would be needed to keep that observation out of adaptation without consulting its true test label. These are learning and design questions, not proof that our eventual method is novel or superior. The current paper remains on hold as a numerical or mathematical foundation until its material issues are resolved.
