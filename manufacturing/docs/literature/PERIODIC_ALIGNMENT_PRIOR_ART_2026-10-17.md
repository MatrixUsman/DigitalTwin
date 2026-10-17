# Periodic alignment, progression and motion prediction: close-prior-art audit

Date: **17 October 2026, Asia/Karachi**. Project: manufacturing / Haiqa Mushtaq. Operator: Codex research agent. This is a bounded primary-source review for the contribution decision, using the shared academic-research-suite deep-research/source-verification guidance. It is neither an exhaustive novelty search nor a completed experimental baseline admission. No human-reading attestation is implied. No raw observations, calibration or final-test samples were opened; no model was trained or upstream code executed.

## Finding for the contribution decision

**A periodic phase variable, a distribution over progression, prediction followed by correction, and phase-dependent anomaly scoring are established ideas.** The sources below directly establish these precedents. Our defensible next question concerns the incremental security-monitoring value of a particular correction-evidence statistic under equal observations, state evolution, calibration and score support. Its usefulness and novelty remain unproven.

The current implementation is a 32-bin empirical phase filter with an RBF pseudo-likelihood, prospective standardized residual, and Jensen–Shannon correction score. Its [normal-only validation](../OBSERVER_VALIDATION_REPORT.md) supports limited internal correspondence and synchronization. It does not show that alignment conceals any of the protected interventions, that the added statistic detects them, or that this mechanism generalizes to other acquisitions.

The recent-paper eligibility window remains **2023-10-16–2026-10-16**. Earlier work below is indispensable methodological prior art; it is not relabelled as a recent baseline. If a foundational algorithm is implemented as a control, record it as an explicitly justified methodological supplement. None of these records adds another dataset to the admitted study.

## Recent sources within the window

### P1. CASPER — existing aligned-template and prediction precedents

**Kayan et al., “CASPER: Context-Aware IoT Anomaly Detection System for Industrial Robotic Arms.”** Peer-reviewed *ACM Transactions on Internet of Things* 5(3), article 18, August 2024; DOI [10.1145/3670414](https://doi.org/10.1145/3670414). The inspected [author-hosted corrected version of record](https://iotgarage.net/publications/pdfs/Kayan2024a.pdf) explicitly identifies V1.1, **5 February 2025**. Direct DOI opening failed in this session; the complete author-hosted manuscript and existing publisher-metadata receipt support identity.

Manuscript §§6.4.2–6.4.5 and Algorithm 1 already estimate periodicity, align normal windows, construct a mean periodic reference and score mismatch. CNN/LSTM methods forecast the next IMU observation from preceding windows, then aggregate residuals. The original experiment uses external IMU, not our controller q/qdot inputs. Its temporal alignment and threshold/search procedures are not automatically our causal protocol.

The pinned [author notebook](https://github.com/hkayann/1D-CNN-Anomaly-Detection-via-CASPER/tree/bff03c91d155bf3134f6d801d3a4f4af7ea78adb) has unresolved code-use terms: an MIT badge is present but matching license text is absent in the previously audited tree. The [admission audit](CASPER_ADMISSION_2026-10-17.md) remains authoritative. A q/qdot port is an independent adaptation, not a faithful published-result reproduction.

### P2. Edge robotic-arm monitoring — segmentation and prediction already coexist

**Kayan et al., “Real-Time Anomaly Detection for Industrial Robotic Arms Using Edge Computing.”** Peer-reviewed *IEEE Internet of Things Journal* 12(15), 29696–29712; DOI [10.1109/JIOT.2025.3569780](https://doi.org/10.1109/JIOT.2025.3569780). Publisher-deposited metadata gives issue date **1 August 2025**; [Cardiff](https://orca.cardiff.ac.uk/id/eprint/178905/) records acceptance **6 May 2025**. Exact first-online day remains unverified; DOI creation on 14 May is not substituted for publication.

The [author manuscript](https://iotgarage.net/publications/pdfs/Kayan2025a.pdf), §§V.D–E and VI, combines idle/activity segmentation, task heuristics, CNN/LSTM next-observation prediction and residual aggregation. It describes 26 hours and three tasks, with external disturbances and IMU inputs. Idle detection can misclassify weak movement; anomaly timestamps were not recorded precisely. These are author-described limitations, not results from our study.

Its linked [TinyML repository](https://github.com/hkayann/Real-time-Anomaly-Detection-in-Industrial-Robotic-Arms-via-TinyML) contains an MIT license; it is separate from original CASPER code. Exact paper-run/code correspondence and controller-input compatibility remain unresolved. This is relevant prior art and a possible separate future track, not an admitted equal-information comparator. Generic task recognition or combining segmentation with residuals cannot be our novelty claim.

### P3. ClaSS — recent online segmentation, with a material input/task mismatch

**Ermshaus, Schäfer and Leser, “Raising the ClaSS of Streaming Time Series Segmentation.”** Peer-reviewed *PVLDB* 17(8), 1953–1966, 2024; DOI [10.14778/3659437.3659450](https://doi.org/10.14778/3659437.3659450). Publisher-deposited dates: print **April 2024**, online **31 May 2024**. [arXiv:2310.20431](https://arxiv.org/abs/2310.20431) first submitted **31 October 2023**.

The [proceedings manuscript](https://www.vldb.org/pvldb/vol17/p1953-ermshaus.pdf), §§2–3 and 6, evaluates candidate splits within a trailing window using self-supervised classification and significance testing. It reports change points after supporting evidence arrives, so detection time and estimated boundary time differ. It does not supply robot task semantics, prospective motion predictions or an attack detector. The paper explicitly limits ClaSS to **univariate** time series.

The [author repository](https://github.com/ermshaua/classification-score-stream/tree/704b3deb3dac9cc65c5666968b76886e42343e2f), pinned here at `704b3deb3dac9cc65c5666968b76886e42343e2f`, has a verified BSD-3-Clause license. Twelve-channel fusion and conversion to endpoint attack scores would be new methodological choices. Retain as segmentation background; do not force it into our detector ranking merely to fill a recent-method slot.

## Foundational sources outside the recent-baseline window

### P4. Bayesian Interaction Primitives — joint phase/state inference and uncertainty

**Campbell and Ben Amor, “Bayesian Interaction Primitives: A SLAM Approach to Human-Robot Interaction.”** Peer-reviewed CoRL 2017, PMLR 78, 379–387, **13–15 November 2017**; stable identifier [PMLR campbell17a](https://proceedings.mlr.press/v78/campbell17a.html). No DOI verified.

The [proceedings manuscript](https://proceedings.mlr.press/v78/campbell17a/campbell17a.pdf), §3, uses an EKF state containing phase, phase velocity and trajectory basis weights. It predicts this state, incorporates current observations through an innovation, and propagates covariance. Phase velocity addresses ambiguity when motion is temporarily static. Future trajectory inference and uncertainty therefore precede our design. Its human–robot interaction task is different from cybersecurity monitoring.

The matched author/lab [IntPrim library](https://github.com/ir-lab/intprim/tree/8994b158c3f1306be7f9d6304b370d70e2c257fb) is pinned at `8994b158c3f1306be7f9d6304b370d70e2c257fb`; MIT text and README were retrieved. README identifies Python 2.7-era testing and numerical dependencies. No installation or compatibility check ran. A periodic, fixed-reference CASPER observer is an adaptation: the published method also conditions trajectory weights and uses demonstrations with identifiable beginnings/endings.

### P5. Periodic Interaction Primitives — directly relevant periodic q/velocity correspondence

**Clark et al., “Predictive Modeling of Periodic Behavior for Human-Robot Symbiotic Walking.”** Peer-reviewed ICRA 2020, 7599–7605; DOI [10.1109/ICRA40945.2020.9196676](https://doi.org/10.1109/ICRA40945.2020.9196676). Publisher-deposited publication month **May 2020**; [arXiv v1](https://arxiv.org/abs/2005.13139) **27 May 2020**. [Institutional record](https://experts.azregents.edu/en/publications/predictive-modeling-of-periodic-behavior-for-human-robot-symbioti/) corroborates venue and DOI.

The [full manuscript](https://arxiv.org/pdf/2005.13139v1), §III, encodes periodic motion with von Mises basis functions. Training gait cycles are aligned using angular position, velocity and derived acceleration. A position/velocity lookup estimates phase from current observations; Kalman conditioning updates trajectory weights and uncertainty, then predicts future states. Current-observation-conditioned reconstruction must not be reported as a prospective prediction of that same observation.

IntPrim lists this work among uses of the library; a paper-specific reproducible release was not verified. Gait/prosthesis variables, segmentation, demonstrations and control outputs differ from CASPER. A fixed-template q/qdot phase-lookup control is nevertheless a close conceptual comparator, explicitly our adaptation. Neither periodic state inference nor adding uncertainty is a new contribution by itself.

### P6. Progress-dependent HMM anomaly detection — distributional phase and contextual scores

**Park, Erickson, Bhattacharjee and Kemp, “Multimodal Execution Monitoring for Anomaly Detection During Robot Manipulation.”** Peer-reviewed ICRA, **May 2016**, 407–414; DOI [10.1109/ICRA.2016.7487160](https://doi.org/10.1109/ICRA.2016.7487160), verified with IEEE-deposited metadata and [author record](https://pidipidi.github.io/publication/icra_2016_ad/).

The [author manuscript](https://pidipidi.github.io/pdf/ICRA16_2378_FI.pdf), §§III–IV, trains a left-to-right Gaussian-emission HMM on successful demonstrations. Execution progress is a hidden-state probability distribution. The alarm compares observation log-likelihood with a progress-dependent mean-minus-scaled-standard-deviation threshold; KL divergence selects the nearest normal progress cluster. Thus probabilistic progress, its uncertainty and divergence-based contextual monitoring already exist.

The paper describes prefix-recursive online detection; its general forward/backward equation also appears, so any port must enforce endpoint filtering without future smoothing. Experiments concern PR2 manipulation and multimodal task trials, not CASPER cyberattacks. GHMM is named; a matched author experiment repository/license was not verified. Cyclic continuous operation and our permitted features would require an explicit adaptation. The 2019 *Autonomous Robots* extension is a verified related record, not separately audited here.

### P7. Online time warping — adaptive alignment and path-speed information

**Dixon, “An On-Line Time Warping Algorithm for Tracking Musical Performances.”** IJCAI 2005 proceedings short/poster paper, 1727–1728; [official two-page paper](https://www.ijcai.org/Proceedings/05/Papers/post-0005.pdf). Conference publication is verified; detailed historical review procedure and DOI were not verified. Treat as foundational background.

It incrementally aligns a live sequence against a stored reference with dynamic-programming accumulated distance, bounded search and permitted path increments. The recurrence is `D(i,j)=d(i,j)+min[D(i−1,j),D(i,j−1),D(i−1,j−1)]`. The alignment-path slope already represents relative tempo. Only observed live samples enter the online path; the paper separately evaluates an offline method that can use the future.

The data are musical performances, not robots. No exact author implementation/license was verified in this pass. A circular multivariate q/qdot port needs explicit wraparound, elapsed-time, path constraints and initialization. It is an independent control, not a reproduction of the audio experiment. Alignment cost and deviation from nominal path speed should be retained separately; an offline full-test warp is ineligible.

### P8. Forward-plotting DTW — monotone online motion alignment, just outside cutoff

**Randall, Harvey and Williams, “Online alignment of human motion using forward plotting-dynamic time warping.”** Peer-reviewed *Computer Animation and Virtual Worlds* 34(3–4), e2166; DOI [10.1002/cav.2166](https://doi.org/10.1002/cav.2166). [Author institution](https://www.open-access.bcu.ac.uk/14487/) records acceptance **1 May 2023**, online publication **16 May 2023**: outside our baseline window.

The full published manuscript available there, §3 Algorithms 1–3, compares monotone local frame matching and two prediction-assisted alignment variants. Method A searches forward from the previous matched reference frame using the current target frame. B/C extrapolate a short future from already received frames; they do not consume actual future observations. Motion orientation/geodesic distance and finite human-motion sequences differ from our joint telemetry and endless cycle.

No author code/license was located in the inspected record/manuscript. The manuscript is CC BY-NC-ND; this is not a software license. A causal monotone matcher is relevant as an explicitly adapted control; matching the current observation is not a forecast of it. The work also shows that online monotonicity and prospective short-window alignment are not unexplored.

## Exact mechanism and competing explanations

This section is our analysis of the implemented estimator, not a claim that any reviewed paper implemented our exact score.

For standardized observation `z_t`, template bin `m_k`, predicted phase weights `p^-_t(k)` and bandwidth `τ`, the current filter uses:

```text
d_t(k) = mean_j (z_t,j − m_k,j)^2
L_t(k) = exp(−d_t(k)/(2τ))
p^+_t(k) = p^-_t(k)L_t(k) / sum_l p^-_t(l)L_t(l)
yhat_t = sum_k p^-_t(k)m_k
R_t = mean_j (z_t,j − yhat_t,j)^2
C_t = JS(p^-_t, p^+_t)
S_t = R_t / training_mean(R) + C_t / training_mean(C)
```

The reference, bandwidth and score scales are fixed during scoring. This is state assimilation, not online parameter learning. RBF weights are a pseudo-likelihood; their normalization across phase does not establish calibrated physical observation probabilities. The current matched pair changes only the final `C` term. Both still contain nominal progression and correction in their state evolution.

Three checks are essential before a mechanistic contribution claim:

1. **Correction is not automatically abnormality.** If all phase-bin likelihoods are equally poor, normalization can leave the posterior equal to the prior, giving `C=0` despite poor fit. Conversely, an informative normal observation can legitimately change phase belief. JSD is bounded, unsigned and depends on bandwidth/prior uncertainty. It is neither an authenticated speed estimate nor evidence of malicious intent.
2. **Ordinary likelihood may already retain the same information.** A natural same-filter control is `−log sum_k p^-_t(k)exp(−d_t(k)/(2τ))`, computed stably before state commit. This is a fixed-bandwidth kernel evidence score, not an automatically calibrated Gaussian likelihood. Its comparison with `R`, `C` and `R+C` tests whether the addition improves over an ordinary predictive fit statistic rather than only a deliberately incomplete score. It is proposed, not implemented or run.
3. **Position alignment does not generally remove velocity evidence.** For a time-warped reference `q(t)=q_0(φ(t))`, the chain rule gives `qdot(t)=q'_0(φ(t))φdot(t)`. Retiming position can reduce positional residual while speed still changes velocity amplitude. Our model observes both q and qdot. A phase-conditioned velocity/progression control is therefore necessary before attributing a benefit to synchronization effort. For the parent's narrower same-filter score audit, this can be `Rv`: the prospective residual restricted to the six standardized velocity channels, with the same full-input state evolution. This isolates score content without changing its state estimator. Do not presume that CASPER interventions are hidden by the present observer. A q-only diagnostic would require a separately declared feature ablation and cannot silently replace the common-input task.

## Comparison implications for the parent study decision

These are recommended roles, not implementation admission or an instruction to run experiments now.

| Comparison role | Minimal defensible option | What it resolves | Status / boundary |
|---|---|---|---|
| Ordinary prediction | Keep selected AR(4), velocity-deviation and fixed-template controls | Whether an ordinary predictor or direct speed-sensitive signal suffices | Existing artifacts; none is a paper reproduction |
| Matched evidence isolation | Existing synchronized `R` versus `R+C`, plus `C` alone | Added term versus shared state/update trajectory | Pair implemented; C-only needs declared score/artifact path; thresholds must be calibrated separately at the same normal-only operating rule |
| Ordinary same-filter fit | Predictive kernel evidence / negative log-evidence using the existing prior and emission distances | Whether ordinary observation surprise already explains any benefit | New transparent control; no new learned representation required; declare and test before fitting/calibration |
| Direct velocity evidence | Same-filter prospective residual on velocity channels only, `Rv` | Whether direct speed-sensitive mismatch explains the same-filter score result | Proposed minimal control for the narrow score audit; same full q/qdot state and fixed denominators |
| Independent temporal alignment | Circular monotone alignment with an explicit progression-speed score | Whether a phase estimator outperforms established alignment/progression alternatives | Required only if claiming alignment/progression superiority, which the revised study declines; any future adaptation must resolve uncertainty, circular differences and initialization without attack-boundary segmentation |
| State-update policy | Existing unconstrained following/free-running policies, interpreted with the fixed-template control | Influence of synchronization policy rather than score composition | Diffusive free-running near-uniform collapse prevents treating it as the sole fixed-reference competitor |
| Modern learned detector | A recent method admitted under the exact input and chronology rules | Whether a stronger generic learned representation changes a broad detector comparison | Conditional for broader detector-superiority claims; a narrow same-filter score audit need not invent a three-paper ranking. ClaSS is not a substitute |

A full BIP/PIP/HMM port is scientifically justified only if its role adds evidence beyond the simpler temporal control and its adaptation can be specified fairly. The first requirement is to represent the prior-art mechanism, not to collect the greatest number of models. The parent's selected scope is a single-acquisition same-filter score audit: it explicitly declines estimator/alignment superiority, a new twin, and broad detection superiority. Under that narrowed scope, Rv is the minimal direct-velocity control and an independent alignment implementation is conditional rather than a gate. Classical KL surprise is also required by the companion synchronization review. Do not rank published numbers from heterogeneous modalities, task labels, boundary access and ROC/oracle threshold protocols.

## Search and verification record

Scope: bounded web search and primary citation chaining from the existing [prior-art screen](RQ_PRIOR_ART_SCREEN_2026-10-16.md), completed 2026-10-17 locally (retrieval receipts carry UTC 2026-10-16). Eight principal sources were retained for specific mechanism coverage. No claim of exhaustive coverage, exact-algorithm novelty, retraction clearance, code reproducibility or independent peer review follows.

Literal discovery queries included:

```text
"Probabilistic Phase Estimation" "Bayesian Interaction Primitives"
"robot" "anomaly detection" "phase" "HMM" Park
"ClaSS" "Streaming Time Series Segmentation" 2024
"Online Time Warping" Dixon 2005 synchronization
Campbell Amor Bayesian Interaction Primitives phase estimation 2017
"Multimodal Anomaly Detection for Assistive Robots" Park 2017 pdf
"Online alignment of human motion" "Randall" pdf
"Raising the ClaSS" github license
"Multimodal execution monitoring" "2016" "pdf"
site:github.com Bayesian interaction primitives intprim license
"Multimodal anomaly detection" "9733" pdf
"An On-Line Time Warping Algorithm" site:ijcai.org
site:pidipidi.github.io "Multimodal anomaly detection for assistive robots" pdf
"Predictive Modeling of Periodic Behavior" Clark Campbell periodic phase
"Multimodal execution monitoring" "7487160" site:ieeexplore.ieee.org
"3659437.3659450" date
"9196676" site:ieeexplore.ieee.org
"3569780" "2025" date
```

The numerical/date searches returned irrelevant and secondary items; those were not promoted to evidence. Publisher-deposited Crossref records resolved four exact identifiers/dates. A DOI creation timestamp is not a publication timestamp. Web requests for GitHub API/raw URLs failed; a default shell fetch then failed DNS. Approved read-only public fetching retrieved metadata, license text, README files and six open manuscripts without executing them. No dataset, private material or author contact was involved.

Local receipts under ignored `local/contribution_review/periodic/`:

- `retrieval.json`: author repository commit IDs, source URLs, README/license byte counts and SHA-256 hashes.
- `metadata_receipt.json`: exact Crossref identifiers, dates, publisher/type and original response hashes.
- `manuscript_receipt.json`: six primary PDF URLs, redirected URLs, sizes and SHA-256 hashes. CASPER and the edge paper were inspected through their author-hosted full manuscripts; CASPER's previously stored corrected VOR remains unchanged.

| Saved manuscript | SHA-256 |
|---|---|
| `bip2017.pdf` | `9070941ea2b0c22c485817b2fb11144aa811e5c937eda99f79911123d5bb71d0` |
| `pip2020.pdf` | `df6b38924528e57d2cc26c9193b7e7e7988dd375c29be1028bd3b19f38643873` |
| `hmm2016.pdf` | `d0d892fcf05087bb4d76374e360429ae07ef9db80ba1918e1b6cf186c8ce6aba` |
| `oltw2005.pdf` | `98756e93b873627fec226ed35fb822c9ad3e332b83058c9c2d5889c629d049e8` |
| `class2024.pdf` | `7dff948ad56fd66f6dab07e8eba69ce77066e6974209211db0ec7195ff534327` |
| `fpdtw2023.pdf` | `ba6cf314aa079f3f7f007d48917ca2c6c312bb80938c72ea39daa2e0b6caa549` |

Primary texts were inspected at the named method/limitation sections. Exact code experiments were not audited beyond the explicitly stated repository/license observations and preserved CASPER audit. The parent study must integrate this record with synchronization/security prior art and the independent-recording feasibility screen before freezing claims or comparisons.
