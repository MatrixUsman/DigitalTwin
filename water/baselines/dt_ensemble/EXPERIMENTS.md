# Ensemble experimental specification audit

**No baseline experiment has been run.** Paper assets, extracted tables and graphics are collected for study. They are not executable evidence, checkpoints or our measurements. Refer to [resource provenance](../RESOURCE_MANIFEST.json), [dataset gaps](DATASETS.md), and the [reproduction proposal](../../docs/REPRODUCTION_PLAN.md).

## Authors' described pipeline

| Component | Published specification | Missing or unresolved |
|---|---|---|
| Physical twin | First-principles MATLAB/Simulink process model plus EKF | Process-model files, plant parameters, fitted matrices, inputs and initialization |
| Learned detectors | LSTM autoencoder, attention transformer and Isolation Forest | Matched source code, exact executable configurations and trained models |
| Fusion | Weighted ML score combined with twin residual; Equation 13 gates alarm output | Complete score normalization and calibration implementation |
| Weight selection | Normal-only stability, calibration and residual-consistency proxies; Bayesian search | Full objective specification, search artifacts and exact development intervals |
| Adaptation | EWMA threshold on certified-normal windows; residual drift triggers parameter/ML updates; seven-day recent-data buffer described | Operational certification/admission rule, replay ordering, optimizer state and contamination handling |
| Preparation | Training-statistic min–max scaling, 50-sample windows; EWMA normalization and imputation also described | Precise ordering and causal implementation; sampling and release compatibility |
| Tuning | Table 1 describes 500 Optuna TPE trials and a 48-hour budget on one A100 | Narrative also refers to a Gaussian-process surrogate; released search configuration absent |
| Compute | DGX with eight A100 GPUs reported; Python 3.9.7, TensorFlow 2.11.0, PyTorch 1.13.0, MATLAB R2023a | Environment lock, source revision, execution scripts and logs; local Apple CPU/MPS compatibility untested |

Table 1 gives seeds `42, 123, 456, 789, 2021, 2022, 2023, 2024, 2025, 8675309`; batch 64 for training and batch 1 for inference. These are **published configuration statements**, not versions installed or seeds executed here. Details are in the [VOR PDF](artifacts/papers/Ensemble_ScientificReports_VOR.pdf), Methods/Results and Tables 1–7.

## Questions that block faithful reproduction

1. What raw files and timestamps produce the paper's splits and its normal-only SWaT day 8? How was the stated 10 Hz stream obtained?
2. Which information certifies an incoming window as normal without labels? Does that certificate control threshold updates, parameter learning, state correction, or all three?
3. Where are the exact plant models, calibration objectives, hyperparameters, update configurations and detector implementations?
4. Are reported scores point-adjusted? What score-to-label alignment, coverage, warm-up and event-delay definitions were used?
5. What generated the added adversarial perturbations, latency measurements, uncertainty intervals and ablations? Original output files/models are explicitly withheld in Data availability.

The alarm gate (Equation 13), EKF state update (Equation 5), residual/threshold adaptation and model-parameter updates are different operations. Their interaction is important prior art for our proposed question, but the narrative does not demonstrate that updates resist contaminated observations.

**Additional reporting question from the collected Table 3:** every displayed FPR equals `100% − precision` (for example, 97.6% precision and 2.4% FPR). Standard FPR is `FP/(FP+TN)`, whereas `1 − precision` is `FP/(TP+FP)`. This numerical pattern calls for a denominator check; the table alone does not prove how the authors computed those values. Do not treat them as verified standard false-positive rates. [Source table XML](artifacts/extracted/tables_03.xml)

## Proposed clean comparison, if feasible and separately implemented

- Freeze common authorized SWaT/WADI releases and chronological partitions before method development. Record every method-specific exception and preserve immutable raw data.
- Select all thresholds, hyperparameters, model states and preferred variants using only predeclared development evidence. Never use held-out attack labels to certify windows, tune weights or choose an update rule.
- Make causal replay ordering explicit. Score each observation before allowing it to update learned/calibrated state; separately document measurement assimilation required by the estimator. Any departure from the article's algorithm is a disclosed change.
- Report unadjusted point metrics, false alarms on independent normal data, event recall, misses, delay and computational cost with explicit denominators and time units. Keep the paper's added attack scenarios separate from unchanged benchmark evaluation.
- Validate data loading, chronological isolation, preprocessing state, score alignment and metrics on labelled synthetic fixtures before any benchmark run. Preserve seeds, hashes, revisions, dependency versions, commands and logs.
- Missing author software would make our work an **independent reimplementation**, with its uncertainty and assumptions recorded. No package installation or implementation is implied by this collection. Approval is required before paid compute or lengthy training; first prepare an authorized bounded pilot.

The paper's compute scale and proprietary MATLAB components may make a faithful local reproduction impractical. Reassess feasibility before committing resources. Neither its published deployment-oriented discussion nor collecting its figures establishes our live-deployment or safety evidence.
