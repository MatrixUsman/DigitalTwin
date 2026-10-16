# Three papers to study before implementation

Decision date: **16 October 2026 (Asia/Karachi)**. Project: water / Muhammad Usman. This decision applies the [predefined criteria](BASELINE_SELECTION_CRITERIA.md), [shared publication standards](../../docs/PUBLICATION_STANDARDS.md) and the [expanded search record](literature/EXPANDED_SEARCH_2026-10-16.md). It recommends a learning set; it does not finalize the research mechanism or admit three numerical baselines.

## Recommendation

**Study CAROTS → Information-Theoretic Digital Twins → the digital-twin/deep-learning ensemble.** The expanded search supports retaining these three for their complementary roles. It did not establish three recent, peer-reviewed, reproducible twin comparators satisfying all our requirements. Do not describe the set as three globally best models, three ready implementations, or three peer-reviewed papers: IT-DT is a verified preprint only.

| Study order and exact paper | What we need to learn | Evidence-based decision |
|---|---|---|
| **1. CAROTS:** Kim et al. (2025), *Causality-Aware Contrastive Learning for Robust Multivariate Time-Series Anomaly Detection*. ICML/PMLR 267:30591–30608. [Proceedings](https://proceedings.mlr.press/v267/kim25aa.html), [published PDF](https://raw.githubusercontent.com/mlresearch/v267/main/assets/kim25aa/kim25aa.pdf), [author code](https://github.com/kimanki/CAROTS) | How normal causal relationships, synthetic perturbations, contrastive learning and score combination form a competitive non-twin detector. What its fixed-relationship assumption means under operational change | **First conditional practical reproduction candidate.** Both datasets verified in the published manuscript. Author code is inspectable; normal-validation checkpoint selection makes it a clearer starting point than several alternatives. Threshold/reporting, alignment, configuration and device issues remain. Full and no-ensemble variants count as **one paper** |
| **2. IT-DT:** Kreso et al. (2026), *Information-Theoretic Digital Twins for Stealthy Attack Detection in Industrial Control Systems: A Closed-Form KL Divergence Approach*. **2 March 2026 preprint**, `arXiv:2603.01621v1`. [Record](https://arxiv.org/abs/2603.01621), [full manuscript](https://arxiv.org/html/2603.01621v1), [PDF](https://arxiv.org/pdf/2603.01621v1) | The explicit chain from a learned state-space model to Kalman innovations, residual-distribution comparison and a fixed normal-calibrated decision rule | **Model-based learning anchor, reproduction hold.** §V-A/Table I reports both datasets; §§III–IV expose the estimator and score. No peer-reviewed version or matched author code verified. Release/preprocessing and window-selection provenance remain unresolved. Later manuscript-based implementation must be labelled ours |
| **3. Ensemble:** Sayghe, Alahmadi and Gharawi (2026), *A digital twin and deep-learning ensemble for cyber attack detection in industrial control systems at the IoT edge*. *Scientific Reports*, 16, 23318, DOI `10.1038/s41598-026-53863-z`; published **22 May 2026**, version of record **27 July 2026**. [Publisher/full text](https://www.nature.com/articles/s41598-026-53863-z) | How physics residuals, ML scores, alarm gating and adaptive updates interact; what evidence is used to call a window safe for updating | **Closest adaptive/hybrid critical-reading anchor, reproduction hold.** Both datasets reported. The publisher describes normal-window threshold updates and drift-triggered updates, making it important prior art. Normal certification, SWaT day split/cadence, physical-model artifacts and public code remain unresolved. Reading priority is not endorsement of its results |

The distinction between a twin's evolving state, fixed or learned parameters, residual reference and alarm threshold is central. Protecting one does not automatically protect the others. In particular, an alarm gate is not necessarily a gate controlling which measurements can update a model.

## Applying the ten rules

Legend: **supported** means observed primary evidence; **conditional/unknown** means a requirement remains open; **hold** prevents experimental admission. Publication and dataset claims are authors' reports, not replication.

| Criterion | CAROTS | IT-DT | Ensemble |
|---|---|---|---|
| Recent publication | Supported: ICML July 2025; preprint June 2025 | Date supported; preprint March 2026 | Supported: May/July 2026 |
| Manuscript evaluates both datasets | Supported in published paper | Supported in author manuscript | Supported in publisher text |
| Identical authorized releases for our reruns | **Unknown**; code expects SWaT Normal v1/Attack v0 and WADI A2 | **Unknown** | **Unknown** |
| Comparable task/information | Normal-data detector; synthetic augmentation declared | Nominal identification described; exact controls/features unresolved | Normal-data detection described; additional physical artifacts unresolved |
| Useful scientific role | Learned non-twin control | Explicit estimator/residual control | Close gated/adaptive prior art |
| Reproducible implementation route | Author code exists; modifications/tests needed | No matched code verified; specification incomplete | No matched runnable code verified; specification incomplete |
| Test-independent selection | Default checkpoint: normal validation; threshold and metric paths need changes | Calibration described; F1-based window-selection labels unclear | Normal-only selection claimed; split/certification unresolved |
| Common causal scores and metrics | Plausible after alignment/reporting repair | Plausible from algorithm, not demonstrated | Plausible in equations, not demonstrated |
| Peer review | ICML proceedings | **Not verified** | Published journal article |
| Local execution feasibility | CUDA assumptions; CPU/MPS untested | CPU-oriented description, actual runtime untested | Described hardware/MATLAB artifacts not reproduced locally |

No candidate passes every execution gate. Access to SWaT/WADI is still unconfirmed, so there are no common-file hashes or benchmark results. We will never turn a code download or paper table into evidence of dataset permission or successful reproduction.

## Why the search did not simply pick newer papers

- **CCM-TAD (ICML 2026)** has author code and both datasets, but the inspected revision uses test F1 for checkpoint/Optuna decisions and adds timing/alignment issues. It requires a larger protocol change than CAROTS. Its recency does not make it a cleaner first reproduction.
- **Causal Digital Twins** remains a direct-twin reserve; code restrictions, release/selection gaps and the earlier metric-definition concern persist. **DPDGAD** still lacks a fully accessible protocol and verified usable code.
- **ISTFAD** is a new September 2026 twin lead with both datasets in publisher excerpts. It is the priority inaccessible-paper follow-up; full-text and implementation gaps prevent promotion now.
- **SCDT** is relevant to operating contexts and ambiguous observations, but its LLM can determine the final anomaly decision; code, cost and information access need resolution.
- **RoCA** is the priority new contamination paper to read. Its [author manuscript](https://arxiv.org/html/2503.18385v1) evaluates both datasets, but the inspected code has overlapping training/validation windows and test-wide imputation. Its claimed TNNLS version still needs complete primary-source verification. It informs the problem without replacing CAROTS as the first practical candidate.
- Recent contamination-aware and physics/shift work must inform our novelty review even if it does not fill one of the three initial learning roles. The expanded record records these alternatives and exclusions. An older relevant method also remains prior art when it falls outside the main-baseline date window.

These are reasons about suitability for the next milestone, not claims about whose algorithm performs best. Published headline scores were not pooled or ranked.

## Concrete reading sequence

Each reading produces a short evidence card in the researcher's own words. No human-reading completion is implied by this assistant's source audit.

1. **CAROTS:** read abstract, Figure 1, §5.1/Table 1, method and experimental appendices. Draw the input → augmentation → encoder → scores → decision path. Explain the full versus no-ensemble variants. Then trace loader, trainer, predictor and threshold code. Output: a one-page explanation, common-release questions and a proposed deviation list. Resolve paper/code gradient clipping before any run; do not choose it using test attacks.
2. **IT-DT:** read §§III–IV/Algorithm 1, then §V and limitations. Define state, actuator input, observation, innovation, reference distribution and threshold. Mark which quantities are fixed and which update. Output: equation-to-operation map and a list of missing identification/calibration details. Keep unknowns explicit rather than silently inventing an implementation.
3. **Ensemble:** read the system/twin model, fusion/gating, adaptive thresholding, drift update, experiment setup and availability sections. Make four rows: state update, parameter update, residual/reference update, threshold update; record the evidence permitting each. Output: comparison to our provisional question and the unresolved normal-certification/split/code questions.
4. **Cross-paper decision:** record what each method can test, its trusted inputs, its release requirements and why the planned evaluation would depart from upstream. Check the new contamination/context/shift prior art before drafting a novelty claim. Decide the implementation set only after these evidence gaps and dataset feasibility are addressed.

The next practical work is structured CAROTS reading and its reproduction specification, with official dataset-access work in parallel. No substantial implementation, installation, external contact or training was started by this selection task. Three learning papers are an initial curriculum, not a ceiling on the baselines a strong eventual submission may require.
