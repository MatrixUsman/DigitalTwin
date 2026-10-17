# Collect, read and connect papers to author code

**Current follow-up, 17 October 2026:** [admission decisions](COMPARATOR_ADMISSION.md) and [TWINE full-manuscript audit](literature/TWINE_ADMISSION_2026-10-17.md) supersede the access/readiness statements in this historical study. Two of the original three full manuscripts are now available and AI-audited; CatBoost remains inaccessible. TWINE/CatBoost are background only for Group D; CASPER requires a separate IMU track or an independent controller-input adaptation. ModernTCN is an explicitly transferred candidate. One ordinary control pilot exists, but zero paper baselines have been reproduced. The coverage table and detailed findings below describe the earlier 16 October study.

Manufacturing / Haiqa Mushtaq. Updated 16 October 2026. This is a source-study milestone, not a reproduction report. The study uses the shared academic research skill's bounded verification workflow. No researcher is marked as having read or understood a paper on the assistant's behalf.

## Completion and evidence levels

| Candidate | Paper material | Implementation material | Current conclusion |
|---|---|---|---|
| **CASPER** — ACM ToIT, August 2024, [10.1145/3670414](https://doi.org/10.1145/3670414) | Corrected VOR V1.1 available locally; main text studied, key figures inspected. | Pinned author notebook and README, stored author outputs, original dataset receipt. | Substantial paper-to-code mapping; exact checkpoint, published-run provenance and clean evaluation remain unresolved. |
| **TWINE** — Internet of Things, online May 2026, [10.1016/j.iot.2026.101976](https://doi.org/10.1016/j.iot.2026.101976) | Publisher/institutional abstract and limited public text; full accepted manuscript listed but not retrieved. | Complete pinned repository snapshot, including training, explanations and Azure demonstration. | Partial paper-to-code mapping. Static source data flow is mapped; full-paper experiment correspondence is not. |
| **CatBoost on CASPER** — IEEE Sensors Letters, February 2026 issue, [10.1109/LSENS.2026.3656499](https://doi.org/10.1109/LSENS.2026.3656499) | Official abstract and publication records; full manuscript not retrieved. | Complete pinned repository snapshot, including scripts and author-reported run tables/figures. | Partial paper-to-code and reported-result mapping; target construction, chronology and provenance prevent numerical admission. |

**One full paper is available out of three.** Available main code paths for all three were read statically. Zero models have been executed or reproduced. Remaining manuscript gaps are not silently marked complete.

Detailed records:

- [CASPER reading notes](../baselines/casper/READING_NOTES.md)
- [TWINE reading notes](../baselines/twine/READING_NOTES.md)
- [CatBoost reading notes](../baselines/catboost/READING_NOTES.md)
- [Collected manuscript receipts and access failures](MANUSCRIPT_COLLECTION_AUDIT.md)
- [Pinned source/configuration/author-result manifest](../baselines/SOURCE_PACK_MANIFEST.json)

## The method-to-code connection

An author's repository establishes that an implementation is available. To reproduce a result, we also need the exact data and labels, transformations, selected model/checkpoint, permitted tuning information and evaluation target. Matching a model name or a single headline number does not establish this chain.

| Question | CASPER | TWINE | CatBoost on CASPER |
|---|---|---|---|
| What does the model observe? | Nine external IMU channels. | Training notebook: 63 controller features, derived from six scalars and 57 vector coordinates. Demo: a different five-scalar subset. | Public script combines sampled controller observations with padded IMU rows. This is not synchronized sensor fusion. |
| What is learned? | Predict the next IMU observation from a 755-step filtered history. | Classify the supplied anomaly target with a random forest. | Classify a mixture of controller flags and acceleration-derived synthetic IMU labels; includes a CatBoost control and other learners. |
| What labels are available in training? | The prediction target is the next normal observation. Attack labels enter later evaluation/threshold selection upstream. | Attack/anomaly class labels are used in supervised fitting. | Labels are used in classifiers and in the branch called “SSL,” which includes classification loss. |
| How does an alarm arise? | Prediction error in original channel scales → sum of 755 residuals → threshold. | Random-forest class prediction; Azure stores observed properties and that predicted state. | Classifier output against the script's mixed target definition. |
| What does F1 in the inspected code mean? | Binary anomaly evaluation on majority-labelled aggregation windows. | Main training notebook reports support-weighted F1 over random test rows. | Script reports support-weighted F1. Abstract headlines match means of author test-run records; a derived table's validation label is misleading. |
| Which state is a digital twin? | CASPER is the non-twin detector reference; its temporal predictor alone is not a demonstrated synchronized physical twin. | Inspected cloud schema stores current measurements and classifier output. Full-paper physical/model fidelity remains unverified. | No digital-twin component established in the inspected classifier workflow. |
| What prevents a common ranking? | Manual IMU annotations, missing sensor time, checkpoint provenance, and test-label threshold selection. | Different observations/supervision, random row splitting, differing model/feature paths, missing full paper. | Synthetic labels, incompatible row stacking, scaling before splitting, missing full paper and exact run provenance. |

These are observations about the named source paths, not a finding that every paper result is false. Detailed notes identify exact cells, functions, figures and unresolved links.

## Findings from the deeper reading

**CASPER:** the complete paper includes hardware/sensor design, communications and resource measurements beyond its detector notebook. A mapping of the CNN does not reproduce that wider system. Further comparison of the paper's statistical baseline figure, its caption and Table 14 finds different reported values; related code also uses a different evaluation denominator. Preserve each source and its evaluation unit rather than choosing a preferred number. The detailed reading note separates these issues from the CNN architecture/denominator checks that do agree.

**TWINE:** the 100-tree model's evaluation precedes a replacement 50-tree, depth-10 model used for SHAP. Explaining a separately fitted model is not automatically an explanation of the model whose accuracy was reported. The five-feature Azure demonstration is a third path, with a different feature set and shuffled/subsampled rows. The full paper is needed to identify which path supports each claimed experiment.

**CatBoost:** the official abstract's accuracy and F1 round to the means of ten **author-reported test-run records**. A derived `Val Acc` column contains test accuracy instead of the separate validation-accuracy values. Different summary families use population versus sample standard deviation. The script also reports neural inference time per batch and classical-model inference time per observation under a common label. These are artifact arithmetic and code-unit findings, not training results from this project. Recomputed means cannot prove the underlying experiments or make the target construction appropriate.

The source study therefore improves traceability while keeping numerical admission on hold. Missing run provenance is not filled by agreement between a saved CSV and a paper abstract.

## Reading the code in an order that explains the paper

CASPER is the best starting point in the current collection because its complete manuscript and original recording are available. Start with the physical setup and assumptions, then the data, then the predictor and evaluation. Its “context” is partly captured through temporal motion history; do not infer that the dataset supplies production-phase or authorized-changeover labels.

For the primary CNN path, read notebook cells **1–25 → 79–85 → 88–99** alongside paper §6.3–6.4, Figure 11 and Algorithm 1. Cell numbers are zero-based and belong to revision `bff03c91d155bf3134f6d801d3a4f4af7ea78adb`. The [annotation study](CASPER_ANNOTATION_LINEAGE.md) explains the filtered/raw coordinate difference and complete score support. The architecture figure matches four convolution layers in code, but a later checkpoint load replaces the trained object. That unresolved replacement matters more than the already-resolved layer-count concern.

For TWINE, use the abstract to identify the claimed relationship between supervised detection, SHAP explanations and a twin. Read `scripts/training.ipynb`, then the explanation code, then `scripts/digital_twin_azure.py` and `model/digital-twin-schema.json`. Keep the 63-feature training path separate from `simulation_robotic_arm.ipynb`'s five-feature demonstration. The name “simulation” and periodic cloud updates do not establish chronological real-time validation.

For CatBoost, start with the input and target construction in `final_multi_run.py`, before looking at its CatBoost parameters or reported scores. Follow that target through splitting, scaling, training, metric calculation and saved CSVs. Read it as text: importing the module starts experiments. Use the detailed reading note to distinguish the official abstract, raw author result tables, derived tables, and what their labels actually mean.

All of these source files are already available in each method's ignored `artifacts/source_snapshot/` directory. Do not rerun download or setup instructions merely to read them.

## What is settled, and what the next stage needs

The collection identifies real papers and matched author repositories, preserves exact available bytes/revisions, explains the inspected methods and records substantive protocol problems. CASPER's figure/code architecture and annotation-denominator consistency have supporting evidence. Those checks do not establish exact experimental equivalence or predictive performance.

**Historical reproduction proposal:** this paper-reading pass recommended a normal-only external-IMU comparison with CASPER as a conditional reference. The later [question decision](RESEARCH_QUESTION_AND_THREAT_MODEL.md) selected a right-arm controller study as the main feasibility track. External-IMU reproduction remains separate and still needs its own annotation/time/feature contract and corrected calibration, disclosed as a departure from upstream best-test-F1 selection. A supervised controller experiment is another separate group; none silently shares a leaderboard. Use [PAPER_ROADMAP.md](PAPER_ROADMAP.md) for the current sequence.

Full TWINE/CatBoost manuscripts and exact published-run correspondence remain open. Do not infer unseen equations, tables, split rules or limitations from abstracts or code. No author contact, purchase, access-control bypass, cloud deployment, dependency installation or training is implied by this study.

The earlier IMU/supervised proposals in [COMPARISON_PROTOCOL.md](COMPARISON_PROTOCOL.md) retain their unresolved decisions. The selected Group D now has exact [data/evaluation definitions](EVALUATION_PROTOCOL.md) and [synthetic-tested software](SOFTWARE_VALIDATION.md), while real models and final admission remain pending. The [data study guide](DATA_AND_BASELINE_STUDY.md) remains a reading entry point; this document records paper-reading and implementation-mapping coverage, not experimental completion.
