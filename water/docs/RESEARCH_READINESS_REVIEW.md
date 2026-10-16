# ARS fact-check: research readiness

Date: **2026-10-16**. Workflow: installed ARS-Codex 3.23.1, `deep-research` **fact-check**, using the source-verification role. Scope: three specific claims from the project audit. This AI-assisted check used public primary sources and static code inspection; it did not execute models or validate published performance. It is not an exhaustive literature search or a formal novelty assessment.

## 1. CAROTS can be our first baseline without using held-out attack labels

**Verdict: conditional; the default evaluation must change.** At revision `63a41f45a2ae680d5cdbb2d5739e7a11264867cb`, the configuration defaults to `best_f1`; threshold selection searches the test precision–recall curve using test labels. Separately, the predictor reports maximum F1 from that curve. Replacing only the threshold selector would leave test-optimized F1 reporting intact. [Configuration](https://github.com/kimanki/CAROTS/blob/63a41f45a2ae680d5cdbb2d5739e7a11264867cb/config.py), [threshold implementation](https://github.com/kimanki/CAROTS/blob/63a41f45a2ae680d5cdbb2d5739e7a11264867cb/threshold.py), [predictor](https://github.com/kimanki/CAROTS/blob/63a41f45a2ae680d5cdbb2d5739e7a11264867cb/models/carots/predictor.py).

Do **not** extend this finding to say default checkpoint selection uses attack labels. The inspected CAROTS and CUTS+ trainers select checkpoints by validation loss and discard anomaly labels during validation. [CAROTS trainer](https://github.com/kimanki/CAROTS/blob/63a41f45a2ae680d5cdbb2d5739e7a11264867cb/models/carots/trainer_carots.py), [base trainer](https://github.com/kimanki/CAROTS/blob/63a41f45a2ae680d5cdbb2d5739e7a11264867cb/trainer.py), [CUTS+ trainer](https://github.com/kimanki/CAROTS/blob/63a41f45a2ae680d5cdbb2d5739e7a11264867cb/models/carots/trainer_cuts_plus.py).

A separate configuration hazard exists: `TRAIN_RATIO >= 1` makes the SWaT/WADI loader use test data as validation. This leaks test measurements into model selection even when labels are discarded. That branch must be prohibited and cached splits checked. [Loader](https://github.com/kimanki/CAROTS/blob/63a41f45a2ae680d5cdbb2d5739e7a11264867cb/datasets/build.py).

The first-baseline recommendation remains our judgment, supported by proceedings publication, both-dataset experiments, and available author code. It does not establish execution readiness or superiority. Later clean calibration and fixed-threshold reporting will constitute an explicitly **modified evaluation protocol**. [Proceedings](https://proceedings.mlr.press/v267/kim25aa.html), [manuscript](https://arxiv.org/html/2506.03964v1).

## 2. The proposed trust gate is already known to be novel—or already duplicated

**Verdict: neither conclusion is established.** Sayghe et al. describe an alarm gate in Equation 13, EWMA threshold updates from windows designated certified-normal, and drift-triggered twin/ML updates using recent normal data. These are specific overlaps with the broad project concept. [Publisher methods](https://www.nature.com/articles/s41598-026-53863-z).

However, an alarm gate is not automatically an update-admission gate. Equation 5 separately assimilates measurements through an EKF. The accessible prose does not establish how normal-window certification rejects contaminated adaptation data. It therefore supports withholding a broad novelty claim, without proving equivalence to every possible guarded-update mechanism. This check did not validate implementation or effectiveness; the algorithm image was inaccessible. [Ensemble fusion, adaptive thresholding, and drift-detection subsections](https://www.nature.com/articles/s41598-026-53863-z).

The detailed ensemble evidence now explicitly distinguishes alarm decisions, state assimilation, parameter learning, and threshold adaptation.

## 3. Shared SWaT/WADI names establish common releases and data access

**Verdict: not established.** The SWaT provider documents normal v0/v1 with different startup handling, while WADI A2 removes unstable periods and supplies revised labels and attack dates. Those changes can affect preprocessing, chronology, and evaluation. Dataset names alone do not identify comparable files. [SWaT provider description](https://www.sutd.edu.sg/itrust/itrust-labs/datasets/dataset-characteristics/swat/), [WADI provider description](https://www.sutd.edu.sg/itrust/itrust-labs/datasets/dataset-characteristics/wadi/).

The follow-up workspace inventory found no candidate benchmark data or archives outside the installed skill tree. Its bundled examples/test fixtures are third-party skill assets, not research dataset access. External storage remains uninspected because no location was supplied. Exact releases, files, authorization, and hashes remain unresolved; the [dataset checklist](DATASET_ACCESS_CHECKLIST.md) still applies.

## Limits and next decision

Source authority was assessed against each claim: author code for implemented evaluation logic, publisher text for described methods, and provider documentation for release changes. These sources do not independently verify experimental effectiveness. No general venue-integrity review was performed; unavailable evidence was not labelled fabricated.

The next research milestone remains data access/release verification, followed by the already proposed loader, split, calibration, and metric checks. The [reproduction plan](REPRODUCTION_PLAN.md) is still a proposal. No baseline, training, manuscript results, or novelty claim was produced by installing or using the skill.
