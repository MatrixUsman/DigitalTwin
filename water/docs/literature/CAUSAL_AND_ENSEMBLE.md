# Causal and ensemble digital-twin evidence audit

Audit date: 2026-10-16. These identities match the titles and authors subsequently supplied in the conversation notes. Notes remain leads; statements below come from the linked sources. No experiments were run and no reported performance was reproduced. Search failure establishes only that an artifact was not found in this audit.

## Causal Digital Twins (CDT)

**Causal Digital Twins for cyber–physical security in water systems: A framework for robust anomaly detection** — Mohammadhossein Homaei, Mehran Tarif, Pablo García Rodríguez, Andrés Caro, Mar Ávila. *Machine Learning with Applications* 23 (March 2026), 100824; [DOI 10.1016/j.mlwa.2025.100824](https://doi.org/10.1016/j.mlwa.2025.100824). The [publisher search-index record](https://www.sciencedirect.com/science/article/pii/S2666827025002075) confirms title/issue/identifier, but direct retrieval returned HTTP 403.

The [author-uploaded published manuscript](https://www.researchgate.net/publication/398808814_Causal_Digital_Twins_for_cyber-physical_security_in_water_systems_A_framework_for_robust_anomaly_detection), uploaded by Homaei, supplies received 2025-11-10, revised 2025-12-05, accepted 2025-12-16, online 2025-12-17. Treat as a published journal article; individual review reports were not available. The [arXiv record](https://arxiv.org/abs/2510.09616) separately displays submission 2025-09-16 and revision 2025-11-14, under a different title ending “in Industrial Control Systems.” Its identifier is 2510.09616; preserve the displayed date without inferring it from the identifier. The preprint is not proof of peer review.

| Field | Evidence / unresolved item |
|---|---|
| Datasets | SWaT, WADI, HAI; exact release filenames/hashes unverified. |
| Preparation | Temporal lag augmentation; normalization, missing-value handling and dropped columns not located. |
| Split | SWaT days 1–5 training, 6–7 validation, 8–11 testing. Published §5.1 specifies ten runs on this same split. WADI boundaries unverified. |
| Calibration / metrics | Anomaly threshold exists; selection rule and point adjustment unverified. Published §4.4 defines FPR as `1 − precision`. |
| Availability | §5.1 asserts code availability; Data Availability instead restricts data/code to requests. No verified author implementation or software license. |
| Limitations | Hidden confounding, stable causal structure assumption, slow drift and scaling limitations. |

Protocol references: [published manuscript §§4.4, 5.1, 5.6, Data Availability](https://www.researchgate.net/publication/398808814_Causal_Digital_Twins_for_cyber-physical_security_in_water_systems_A_framework_for_robust_anomaly_detection); [preprint §§4–6](https://arxiv.org/html/2510.09616v2). Published and preprint versions differ; freeze one version before implementation.

**Audit interpretation:** `1 − precision = FP/(TP+FP)` is a false discovery proportion, whereas standard false-positive rate is `FP/(FP+TN)`. These denominators answer different questions. The published false-alarm claim therefore cannot be accepted as standard FPR. This is an evaluation-definition concern, not evidence that every detection result is invalid. Threshold provenance, WADI splits and preprocessing must be resolved before a faithful reproduction.

Author/repository checks:

- [Homaei's public repositories](https://github.com/Homaei?tab=repositories) were inspected; no linked CDT implementation was identified.
- [kbacsa-tudelft/scm-dnn](https://github.com/kbacsa-tudelft/scm-dnn) describes a benchmark harness implementing CDT among several methods. It is third-party implementation evidence, not the paper authors' released experimental code; no equivalence, revision cutoff or license audit was completed.
- [tomtlp/causal-digital-twin-swat](https://github.com/tomtlp/causal-digital-twin-swat) describes a restricted SWaT reproduction effort. It does not establish author-code availability or WADI support. Neither repository was cloned or executed.

**Eligibility:** date and both-dataset scope pass provisionally; reproduction readiness does not. Keep as a candidate comparator, with the metric concern explicitly recorded. Not recommended as the first reproduction.

## Digital-twin/deep-learning ensemble

**A digital twin and deep-learning ensemble for cyber attack detection in industrial control systems at the IoT edge** — Ali Sayghe, Mohammad D. Alahmadi, Abdulrahman A. Gharawi. *Scientific Reports* 16, 23318. [Publisher/full text; DOI 10.1038/s41598-026-53863-z](https://www.nature.com/articles/s41598-026-53863-z).

| Field | Publisher evidence / unresolved item |
|---|---|
| Dates | Received 2025-10-13; accepted 2026-05-14; published 2026-05-22; version of record 2026-07-27. |
| Datasets | SWaT, WADI, Tennessee Eastman; exact releases unverified. |
| Preparation | Training-statistic min–max scaling; 50-sample windows; also describes adaptive EWMA normalization and imputation. |
| Splits | Train/validation/test: SWaT days 1–7/8/9–11; WADI 1–11/12/13–16. Calls validation normal-only. |
| Calibration | Normal-only proxy optimization and 1% false-alarm target; adaptive thresholds on certified-normal windows. Point adjustment unverified. |
| Mechanism | EKF/physics residual gates an LSTM/transformer/Isolation-Forest ensemble; drift triggers updates. |
| Code / limits | Code promised upon publication; results/models withheld. Physics-model artifacts, certification rule and license unverified; zero-day detection not guaranteed. |

Publication and version-of-record dates differ. Peer-reviewed journal status is supported by the [journal's editorial policies](https://www.nature.com/srep/journal-policies/editorial-policies); article-specific review reports were not inspected.

**Audit interpretation:** reconcile the SWaT day-8 normal claim and the stated 10 Hz sampling with the selected official release before using these splits. iTrust describes SWaT A1 as seven normal days followed by four attack days; release selection cannot be inferred from the paper's dataset name. [Official dataset catalog](https://itrust.sutd.edu.sg/itrust-labs_datasets/). Document the relationship between fixed min–max and adaptive preprocessing. A physics gate plus normal-window adaptation is direct prior-art overlap with the provisional project concept; it does not establish novelty or settle whether the same trust decision is used.

**ARS fact-check clarification (2026-10-16):** Equation 13 gates the **alarm decision**. The adaptive-threshold subsection separately describes EWMA updates from certified-normal windows and drift-triggered changes to twin parameters and ML weights using recent normal data. Equation 5 performs EKF measurement assimilation. These distinct operations do not establish that the alarm gate controls admission into model learning, or that the normal-window certification resists contamination. The accessible prose leaves that certification rule unresolved. Thus this is specific prior-art overlap, not evidence that every proposed update-admission mechanism duplicates the paper or lacks novelty. [Publisher methods, “Ensemble fusion and adaptive thresholding” and “Adaptive threshold and drift detection”](https://www.nature.com/articles/s41598-026-53863-z). No implementation or effectiveness was independently validated.

Repository checks: [asayghe1](https://github.com/asayghe1) has a [SCADA DT repository](https://github.com/asayghe1/Digital-Twin-Driven-Intrusion-Detection-for-Industrial-SCADA-A-Cyber-Physical-Case-Study) whose README identifies a different, 2025 Sensors paper; its inspected listing contains only README.md. [physics-informed-cps-security](https://github.com/asayghe1/physics-informed-cps-security) identifies another paper with different coauthors. Neither proves that this ensemble's promised implementation was released. No matching author repository was verified by the exact-title/DOI search; no author was contacted.

**Eligibility:** dates and claimed SWaT/WADI evaluation fit, but release/protocol ambiguity and missing matched artifacts block a faithful comparison. Do not choose it first. An implementation from the narrative alone must be called our reimplementation, with assumptions listed.

## Additional background: Digital Twin Degradation

**Digital Twin Degradation: Detecting Cyber Physical Attacks via Temporal Inconsistencies** — Konstantinos E. Kampourakis, Vasileios Gkioulos, Sokratis Katsikas. [arXiv:2608.16159v1](https://arxiv.org/abs/2608.16159), submitted 2026-08-17; [DOI 10.48550/arXiv.2608.16159](https://doi.org/10.48550/arXiv.2608.16159). No primary publisher/proceedings acceptance was verified; classify as a preprint, peer review unverified.

The [full manuscript §5](https://arxiv.org/html/2608.16159v1) evaluates SWaT, HAI and BATADAL, not WADI. Normal data are split chronologically 80/20 for training versus validation/calibration, with windows confined to each subset. Training-feature medians impute missing residual features; validation scores calibrate CUSUM. Evaluation uses event detection, alarm-onset frequency, delay and a composite reliability measure. Exact dataset releases, raw scaling, repository and software license remain unverified; no matching author code link was located. §5 discusses calibration and also fixed CUSUM settings, which require reconciliation. Controlled degradation with unchanged reference measurements limits interpretation as a real adversarial deployment.

**Eligibility:** relevant recent background only. It does not meet the both-SWaT-and-WADI main-comparator criterion. Adding WADI ourselves would be an extension, not a reproduced published WADI result.

## Next evidence needed

1. Obtain authorized exact dataset manifests and timestamps before reconciling any paper's day numbering.
2. Obtain matched author code, license, immutable revision and original model/configuration artifacts; any author outreach requires user authorization.
3. Resolve the recorded metric, threshold, preprocessing and split ambiguities in writing before claiming faithfulness.
4. Freeze common evaluation rules separately from paper-specific reproduction rules; never silently change a paper's protocol or calibrate on test attacks.

These are audit findings, not allegations of misconduct or validated counter-results. No citation or reported score in this file establishes the proposed project's novelty, superiority or deployment readiness.
