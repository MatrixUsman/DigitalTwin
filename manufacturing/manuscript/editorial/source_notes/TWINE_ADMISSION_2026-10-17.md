# TWINE: manuscript, code and comparator admission audit

Audit date: **17 October 2026 (Asia/Karachi)**. Project: manufacturing; owner: Haiqa Mushtaq. This is an AI-assisted source audit using the academic-research-suite verification workflow and PDF inspection. No researcher comprehension is inferred. No raw CASPER observations, model execution, training, Azure service, author contact or publication was involved.

**Decision:** retain TWINE as **background/architectural related work for the normal-only Group D comparison**. A separate supervised comparison remains a candidate, **not admitted for execution**. Obtaining the manuscript resolves the access gap; it does not resolve incompatible information access or the published-run provenance gaps.

## 1. New evidence and exact source identity

Mubashar Iqbal, Sabah Suhail, Simon Freudenthaler, Muhammad Fahim and Raimundas Matulevičius. *TWINE: ISO 23247-compliant digital twin and explainable AI framework for anomaly detection*. Internet of Things 38, article 101976. DOI [10.1016/j.iot.2026.101976](https://doi.org/10.1016/j.iot.2026.101976).

The [QUB record](https://pure.qub.ac.uk/en/publications/twine-iso-23247-compliant-digital-twin-and-explainable-ai-framewo/) identifies peer review, early online publication **26 May 2026**, and the July 2026 issue. The [MTU record](https://pure.mtu.ie/en/publications/twine-iso-23247-compliant-digital-twin-and-explainable-ai-framewo-2/) also identifies a peer-reviewed journal article. The [Crossref deposit](https://api.crossref.org/works/10.1016/j.iot.2026.101976) gives July 2026 publication and DOI-record creation on 21 May; its `published-online` field is absent. DOI creation is not a substitute for online publication. The paper meets our date window.

The complete accepted manuscript was successfully retrieved through the ordinary [QUB public file URL](https://pureadmin.qub.ac.uk/ws/files/689658736/TWINE.pdf). The portal's `/files/` route still returned HTTP 403; the web text-fetch tool failed on both file URLs. A subsequent ordinary standard-library HTTP request to the public URL returned HTTP 200 and a PDF. No authentication, paywall bypass, proxy or challenge-solving was used.

| Artifact | Identity / status |
|---|---|
| [Received manuscript](../../local/comparator_admission_20261017/twine/qub_public_pdf.pdf) | 33 PDF pages including institutional cover; 4,464,780 bytes; SHA-256 `02f446e7c62d22289209a2667c411322cce0c1a134e8a1b9ac9b333fe3ce5012` |
| Version and rights | QUB cover identifies a peer-reviewed accepted manuscript, copyright 2026 authors, **CC BY 4.0**; not asserted to be the publisher VOR |
| Receipt | [public_retrieval_receipt.json](../../local/comparator_admission_20261017/twine/public_retrieval_receipt.json), successful PDF request at `2026-10-16T19:32:56.291378+00:00` |
| Publisher page | [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S254266052600106X): metadata/snippets searchable; direct fetch HTTP 403. Full VOR not retrieved |
| Author code | [mubashar-iqbal/TWINE](https://github.com/mubashar-iqbal/TWINE/tree/841e1195acf90835c4c427e0fb48d10c08ed30d5), revision `841e1195acf90835c4c427e0fb48d10c08ed30d5`, commit timestamp `2026-05-22T10:12:45Z` |
| Code recheck | Fresh tree and license receipts match the existing [source pack manifest](../../baselines/SOURCE_PACK_MANIFEST.json); all nine local tracked-file sizes/SHA-256 values matched. No upstream code ran |

The manuscript includes an institutional cover generated at download and retains a blind-review placeholder in Appendix A. Its precise received bytes are preserved; the generated cover timestamp is not the article's publication date. QUB's landing-page size label differs from the received PDF size. The PDF signature, title, DOI, cover rights, page count and methods were checked rather than assuming identical versions from file names.

Scope of reading: main-text architecture, dataset, methods, algorithms, results, limitations and conclusion inspected; numerical result pages and SHAP figure visually checked. The 82-item bibliography was not independently validated in this task. This supersedes earlier **unavailable accepted manuscript** statements in the historical reading notes; it does not claim the publisher VOR was read.

## 2. Paper claims connected to the pinned implementation

Page references below use printed manuscript pages, followed by PDF page where helpful. Notebook cells are zero-based array indices, counting all cells. Pinned local files are in [source_snapshot](../../baselines/twine/artifacts/source_snapshot/).

| Experimental claim / operation | Manuscript anchor | Code/configuration anchor | Finding |
|---|---|---|---|
| CASPER controller dataset and targets | §2.2, printed p4 / PDF p5; reference 8 is CASPER DOI `10.1145/3670414` | README dataset link; `training.ipynb` cells 2–6 | Manuscript specifies **1,762,650 rows, 20 source columns, 63 expanded inputs**, normal 0/anomaly 1. Full notebook reads `/right_arm.csv`, expands vector columns and selects six scalars plus expanded coordinates. The previously inferred feature count is now explicitly supported by the manuscript. Exact release, archive version and source hashes remain unspecified |
| Operational anomalies | §2.2 | Target `Anomaly_State`, cell 6 | Manuscript identifies altered joint velocities above/below nominal 1.05 rad/s. A controller observation is assumed available; neither the code nor this paper establishes authenticated observations under full controller compromise |
| Supervised partition | §6, printed p16 / PDF p17 | `training.ipynb` cell 8 | Paper states 80/20 and 1,410,120/352,530 observations, fixed random state. Code uses randomized stratified split, seed 42. This matches the full-row path; the paper does not give exact saved split indices |
| Classifier | Algorithm 2, printed p17 / PDF p18 | Cells 9–10 | Binary supervised random forest; code has 100 trees, unrestricted depth, minimum split 2, leaf 1, seed 42, `n_jobs=-1`. Paper does not specify all these hyperparameters or dependencies. Code fits attack/anomaly labels, unlike Group D |
| Reported classification metrics | §6 equations 1–4 and Figure 4, printed pp17–18 | Cell 10 | Code computes support-weighted precision/recall/F1. Manuscript describes positive-anomaly equations, but its reported numbers match weighted arithmetic; detailed check below |
| SHAP explanation model and population | Algorithm 3, printed p19; Figure 5, p20 | Cells 15–18 | Paper describes explanations of the trained classifier and predicted-anomalous instances. Code replaces the 100-tree classifier with a separately fitted **50-tree, depth-10** forest, samples up to 1,000 test rows, and explains that sample without filtering predicted-positive rows. Figure 5's expanded temperatures/forces are compatible with the 63-feature path, not the five-feature schema. Exact figure-producing run remains unverified |
| Partial-dependence figures | Figure 6, printed p21 | Cells 19–21 | Code ranks top 12 features by mean absolute SHAP and computes PDP/ICE using the replacement forest and sampled test rows. Paper's action suggestions are not experimentally verified causal interventions or autonomous mitigation |
| Azure synchronized representation | §5; Algorithm 1; §6 | `digital_twin_azure.py` lines 54–91; `digital-twin-schema.json`; demo notebook cells 16/19 | Implemented update writes five measured scalars and the predicted flag to Azure. No physical transition model or prediction-residual equation appears in this path. The five-feature replay and 63-feature classifier cannot be interchanged without a documented interface change |
| Simulated data stream / generated instances | Algorithm 1, phase III, printed pp15–16 | Demo cells 13/16/19 | Paper describes generating instances using a variation threshold; collected demo instead subsamples every 100th recorded row, randomly splits and replays five shuffled test rows. No matching generator/configuration for the stated variation rule was located in the nine-file tree |
| Trained model availability | Appendix A, printed p25 / PDF p26 | Complete pinned repository tree | Appendix says code includes a trained model, but tree contains scripts/notebooks/schema and no fitted RF/checkpoint. All stored code-cell outputs are empty. README links the DOI; the manuscript retains a blind-review placeholder instead of its repository URL |
| Physical fidelity, adaptation and deployment | §7.3, printed pp23–24 | No online fitting/update rule in inspected classifier path | Authors explicitly limit the PoC to a single asset and simulated low-fidelity setting; physical constraints, cross-environment generalization and adaptive behavioral consistency are not validated. Framework-level continuous-learning discussion is not an executed adaptation experiment |

These matches establish a plausible method-to-code connection. They do not identify the exact code revision, dependency environment, fitted model or output files that generated the article's figures.

## 3. Numerical consistency audit of the authors' reported result

This is arithmetic on published counts, **not a model execution, benchmark result or reopening of protected observations**. PDF pp18–19 were rendered and visually checked. Figure 4 reports TN=277,440, FP=5,970, FN=6,524 and TP=62,596, totaling 352,530 test rows.

| Quantity | Arithmetic from Figure 4 | Manuscript / code interpretation |
|---|---:|---|
| Accuracy | 96.4559% | Figure title and conclusion round to 96.46%; §6 prose instead says 94.46% |
| Positive-anomaly precision | 91.2931% | Does not equal the reported 96.45% under equation 2 |
| Positive-anomaly recall | 90.5613% | Does not equal the reported 96.46% under equation 3 |
| Positive-anomaly F1 | 90.9257% | Does not equal the reported 96.45% under equation 4 |
| Support-weighted precision / recall / F1 | 96.4458% / 96.4559% / 96.4505% | Round to the manuscript's reported values and match cell 10's `average='weighted'` |

The arithmetic supports a **metric-labeling inconsistency**, with an additional prose accuracy discrepancy. It does not prove an invalid underlying classifier result or explain author intent. The acquired accepted manuscript may differ from the inaccessible VOR; any statement about the VOR must preserve that boundary. Saved calculation: [reported_confusion_matrix_arithmetic.json](../../local/comparator_admission_20261017/twine/reported_confusion_matrix_arithmetic.json). Do not copy these scores into our common-protocol table.

## 4. Code use, reproducibility and unresolved implementation details

The [pinned MIT license](https://github.com/mubashar-iqbal/TWINE/blob/841e1195acf90835c4c427e0fb48d10c08ed30d5/MIT-LICENSE.txt) is present and README explicitly attributes the copied source to `h1548782/seleniumforest` under that license. Freshly retrieved license bytes match SHA-256 `b60c044f81876f350bf5e309071bfc2057c444efd07d2b82790b786049d9d83f`. Code use therefore has an explicit stated license; preserve its existing copyright/permission notice and attribution when copying/modifying. This is evidence of the repository's stated terms, not an independent chain-of-title certification. Dataset and manuscript terms remain separate. No author permission request is required merely to study this openly licensed code.

The README recommends Python 3.7.9 and unpinned packages. No lock, runtime receipt, selected hyperparameter search, saved splits, raw-file hash, trained forest or source-result manifest is present in the inspected tree. Static checks also reconfirm:

- `predict_model` accepts a model argument but uses global `rf` (`anomaly_detection.py`, lines 42–56).
- Demo cell 19 produces five predictions; cell 23 compares them with 15 labels.
- Demo cell 29 calls an absent `create_shap_beeswarm_all`; a referenced dashboard alarm image is absent from the tree.
- `predictive_maintenance.py` fits another classifier for explanations rather than receiving the fitted model being explained.

These are static findings. No dependency installation or live reproduction was attempted, so they are not runtime failure measurements. Patches would require explicit recording, an isolated tested environment and a scoped run; Azure is not needed to assess the classifier alone.

## 5. Honest designation and admission rules

| Proposed use | Designation now | Reason / remaining gate |
|---|---|---|
| Main Group D: normal-only fitting; q/qdot/relative time; chronological replay | **Background only** | Published supervised RF needs anomaly labels and additional controller modalities. Our designated fit/development partitions contain only nominal labels. Restricting a binary RF to those observations is not a meaningful reproduction of TWINE and does not create an unsupervised detector |
| Original published full-feature supervised experiment | **Separate comparison track, on hold** | Full accepted manuscript and MIT code are available, but exact raw release/split/run/model provenance, metric interpretation and figure correspondence are unresolved. Original randomized attack-label fitting would also consume observations protected by our main protocol; do not run it against current Group D final data |
| Standalone RF using explicit permitted labels/features and a separately designed chronological supervised protocol | **Modified author-code implementation**, if actually implemented and executed | Must declare changed task/splits/features/metrics and keep it outside the normal-only ranking; would not reproduce the complete Azure/twin framework |
| New one-class model or normal-only predictor inspired by TWINE | **Independent implementation**, if built | Different objective and training information; do not retain the TWINE name as if its method were reproduced |
| Faithful reproduction | **Not established** | Requires matched source version, dataset identity, environment, model/figure mapping and all recorded deviations; none has run locally |

For the main study, seek methods whose learning objective and inputs genuinely fit Group D, together with necessary simple controls. Do not use additional labels, test-derived selection or wider sensor access merely to fill a three-paper quota.

## 6. Audit receipts and bounded next action

New receipts remain under ignored `local/comparator_admission_20261017/twine/`: public HTTP statuses/hashes; exact PDF and extracted text; rendered result/SHAP pages; source hash recheck; fresh pinned tree/license/commit; Crossref metadata; published-count arithmetic. Existing raw data, frozen protocols, source snapshots and pilot artifacts were unchanged.

Ordinary exact-title/DOI searches checked publisher, QUB, MTU, CHESS, author GitHub, and Tartu/arXiv/ETIS discovery routes. Search failures were treated as access gaps. The new QUB retrieval, rather than an inferred search match, is what closed accepted-manuscript access. No unlicensed mirror or external contact was used.

Inspection commands ran from `/Users/matrixusman/CUI/DigitalTwin`: `pdfinfo` on the received PDF; `pdftotext -layout` to the adjacent `.txt`; `pdftoppm -f 18 -l 19 -scale-to 1800 -png` and a separate page-21 render; Python standard-library JSON parsing, hashing and arithmetic. Exact receipt source URLs, times and hashes are preserved; no notebook cells were executed. Only this new audit and its ignored receipts were written by this subtask.

Next: the parent task should reconcile the literature register with this new access/result evidence and assemble main-method eligibility without admitting TWINE to Group D. If a supervised side study is later wanted, first define independent data protection and input/label access, obtain a justified manuscript/VOR and run correspondence, repair the known code paths with recorded patches, and specify a separate resource-bounded run. The current decision does not require author contact or paid access.
