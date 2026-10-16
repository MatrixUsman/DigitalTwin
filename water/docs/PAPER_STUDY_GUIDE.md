# Stage 2: study the three methods and trace their implementations

Prepared **16 October 2026**. This is an assistant-prepared source study, not a manuscript, researcher reading attestation or empirical reproduction. The existing public collection was reused; no duplicate paper downloads were needed. The [verification report](BASELINE_VERIFICATION_REPORT.md) remains in force.

The useful outcome is to explain a complete path from recordings to a score and alarm, identify where each decision is implemented, and distinguish missing specifications from choices we would make ourselves. Do not begin by memorizing reported F1 values or treating every architecture box as implemented software.

## What is available to study

| Paper/version and role | Full text | Detailed method-to-code study | Implementation status |
|---|---|---|---|
| CAROTS, ICML 2025/PMLR 267; non-twin comparison | [Proceedings PDF](../baselines/carots/artifacts/papers/CAROTS_ICML2025.pdf) | [CAROTS walkthrough](../baselines/carots/METHOD_TO_CODE.md) | Selective author-code snapshot pinned to `63a41f45a2ae680d5cdbb2d5739e7a11264867cb`; actual files/functions can be traced, but code is not validated by execution |
| IT-DT, arXiv `2603.01621v1`, 2 March 2026; model-based twin learning | [Versioned PDF](../baselines/it_dt/artifacts/papers/IT_DT_arxiv_2603.01621v1.pdf) | [IT-DT equations and implementation requirements](../baselines/it_dt/METHOD_TO_CODE.md) | Verified preprint; no matched executable author code. Required interfaces are conceptual, not invented repository functions |
| Digital-twin/deep-learning ensemble, Scientific Reports, 22 May 2026; closest adaptive/hybrid learning paper | [Version-of-record PDF](../baselines/dt_ensemble/artifacts/papers/Ensemble_ScientificReports_VOR.pdf) | [Ensemble equations, algorithm and missing implementation](../baselines/dt_ensemble/METHOD_TO_CODE.md) | Published article; no matched executable author code. Pseudocode names do not establish implementations |

Primary records: [CAROTS proceedings](https://proceedings.mlr.press/v267/kim25aa.html), [IT-DT arXiv v1](https://arxiv.org/abs/2603.01621v1), [ensemble publisher](https://www.nature.com/articles/s41598-026-53863-z). Publication identity is separate from evidence that a method is correct or reproducible. The recent-paper window is unchanged. Older methodological references and a preprint are not silently promoted to peer-reviewed recent baselines.

All three packs contain their own dataset/protocol notes, reported-results guide, references and verification findings. The [collection manifest](../baselines/RESOURCE_MANIFEST.json) identifies source versions and hashes. Neither the GitHub code license nor paper availability grants dataset permission.

## CAROTS: learn a representation of normal relationships

The paper's core idea is to exploit relationships among measured channels. A causal-discovery/forecasting component learns a graph and predicts observations. Two augmentation procedures then construct training examples: one intended to preserve those learned relationships, and another intended to disturb them. Contrastive learning trains a representation that separates those groups while retaining some diversity within normal behaviour. A representation is a learned numerical description of a window; it need not be a physical process state.

At inference, CAROTS combines distance from a reference embedding with the causal forecaster's prediction error. Its dagger variant retains the embedding score and omits the forecasting-error score; it still uses causal discovery for training augmentation. These are separate score components; the similarity-filter threshold used during representation learning is also distinct from the final alarm threshold.

Follow this learning order in the [detailed code map](../baselines/carots/METHOD_TO_CODE.md):

1. Read Figure 1 and the method sections. Explain what a window, channel, graph, augmentor, encoder and score mean without discussing results.
2. Follow a dataset-specific script through `main.py`, configuration handling and `datasets/build.py`. Identify every operation affecting time, channels or labels.
3. Trace the causal forecaster, positive augmentor, negative augmentor, encoder/projector and loss in that order. Follow their actual tensor dimensions rather than assuming the diagram supplies them.
4. Trace the training loop and checkpoint selection; then read `scorer_carots.py`, `predictor.py`, `threshold.py` and metric reporting as separate stages.
5. Explain what is trained once, what remains fixed during scoring, and what needs data-independent or development-only correction before reproduction.

Synthetic negative augmentations are training constructions; they are not automatically physically realizable cyberattacks. A learned forecasting graph is also not established physical causality merely because the model calls it causal. These limitations matter when deciding whether its machinery could help a future twin.

The new walkthrough found a consequential paper/code mismatch: the positive augmentor changes the value at `INPUT_STEP`, while its subsequent forecast uses only the earlier slice `:INPUT_STEP`. The perturbation therefore does not enter that forecast as the paper describes. The parent independently checked the indexed assignments and the paper's Eq. 3. This is a static source finding, not a measured performance effect. Preserve the original and specify any correction as a deviation; do not silently repair it and call the resulting score a faithful reproduction.

**Reading output:** draw the two score paths and name the file/function where each stage occurs. Explain the full/dagger difference and identify which threshold is used for contrastive training versus final alarms. See the detailed walkthrough for additional loss/schedule differences and source anchors.

## IT-DT: compare recent prediction errors with normal errors

This method begins with a state-space model identified from normal recordings. A Kalman filter predicts an observation, computes its innovation residual, and corrects the internal state estimate. A trailing window of residuals is summarized by a Gaussian mean and covariance. The KL-divergence score compares that recent distribution with a fixed normal Gaussian reference; a calibrated threshold converts the score into an alarm.

The important distinction is that a changing state estimate does not mean the model is learning a new definition of normal. In the written algorithm, the identified matrices, normal reference and alarm threshold remain fixed online. The recent residual window changes because it describes current evidence.

Read Sections III–IV and Algorithm 1 before the performance tables. In the [detailed guide](../baselines/it_dt/METHOD_TO_CODE.md), explain the roles of controls, measured outputs, latent state, predicted state, innovation, covariance and threshold. Then follow one observation through the equations. The required source code is unavailable, so the guide maps each stage to inputs, outputs, retained state and unresolved implementation choices rather than claiming real author functions exist.

The algorithm corrects the state before completing its alarm calculation, but the current innovation is formed before that correction. Therefore, it does not erase its own current residual by definition. A malicious measurement can still affect later predictions through the updated state. Rejecting that correction, changing model parameters, and changing the normal residual reference would be three different modifications.

**Reading output:** annotate what is observed, fitted offline, updated every sample and used only for final evaluation. Identify the missing control-channel mapping, identification settings, initialization, preprocessing and calibration partitions. The plotted alarm discrepancy and other [audit findings](../baselines/it_dt/VERIFICATION_REPORT.md) remain unresolved; an independent implementation is not currently an approved numerical comparator.

## Ensemble: several detectors, a twin, and several different update rules

The paper combines an LSTM autoencoder, an attention transformer and an Isolation Forest with a process-model twin. The estimator described in the manuscript is an **Extended Kalman Filter (EKF)**. The learned branch scores are fused, combined with the twin's residual score and passed through an alarm gate. The text also describes drift detection, threshold adaptation and model/weight updates.

Begin with the method equations, Figure 1 and Algorithm 1. The [detailed guide](../baselines/dt_ensemble/METHOD_TO_CODE.md) maps their source locations and explains the limits of each specification. Hyperparameter lists and a diagram do not supply complete architectures, process models or an executable calibration/update policy.

Its alarm gate is not automatically an update-admission gate. Algorithm 1 performs synchronization first, updates weights after a drift decision, and adapts the threshold before applying the alarm gate. The text says learning/calibration uses certified-normal history, but the certification and history membership rules are not operationally specified. It is possible that only previously accepted history was intended; the available manuscript does not resolve that interpretation.

**Reading output:** explain the alarm rule and separately list which observations influence state estimation, normalization, model parameters, fusion weights and the alarm threshold. For each, identify the admission rule or mark it missing. Do not inherit its mathematical robustness or performance claims without resolving the [verification findings](../baselines/dt_ensemble/VERIFICATION_REPORT.md).

## What the three readings mean for our question

The [mechanism comparison](MECHANISM_COMPARISON.md) records the cross-paper synthesis. CAROTS supplies a learned non-twin control with real code. IT-DT supplies a compact mathematical example of state estimation and fixed-reference detection. The ensemble supplies close prior art for combining detection with online changes, but not an executable trusted-update policy.

Consequently, our next design decision is not a network name or title. It is **which quantity a proposed gate would protect, which evidence it could use at that moment, and how its mistakes would be evaluated**. The literature establishes that these distinctions need examination; it does not establish novelty or show that our eventual gate improves anything.

Maintain three separate records for every stage:

- **Paper specification:** the equation, algorithm step or protocol the authors describe.
- **Implementation observation:** an actual pinned file/function, or an explicit statement that none is verified.
- **Our proposed choice:** a correction, missing detail we would resolve, or an extension; never attribute it to the author by implication.

A faithful algorithm implementation can still use a modified evaluation protocol. An author-code run with our clean calibration rules is not reproduction of an upstream optimal-test-F1 result. Independently coding a method from equations is a reimplementation. None of these labels can be assigned from reading alone as an accomplished experiment.

## What is complete and what still belongs to the researcher

Assistant source study and code mapping have been prepared. All three original full texts were already collected; no public executable author implementation was verified for either twin paper. The pinned CAROTS snapshot remains untouched and unexecuted. New discrepancy checks do not supply runtime evidence.

Record your own reading scope and questions in [the reading record](../papers/notes/READING_RECORD.md). No section is marked human-read on your behalf. A useful first discussion is: **explain CAROTS from normal windows to an alarm, then identify which part of that path is actually causal modelling and which part is ordinary learned scoring.** Do not attempt to learn every architecture simultaneously.

Next implementation preparation should be a documented CAROTS correction/deviation specification, including augmentation/loss semantics, data alignment, calibration, checkpoint selection and device compatibility. Dataset access, exact releases and software validation still precede training. IT-DT and the ensemble remain on numerical hold; finding stronger reproducible twin comparators is still necessary before final experimental admission.

During this study the official SWaT/WADI request was submitted after the user's supplied email and explicit consent. Website confirmation is recorded [separately](DATASET_REQUEST_PREPARATION.md). Approval and downloads are pending; this does not change the reading or reproduction evidence above.
