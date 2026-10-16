# Manufacturing baseline source pack and reading guide

Audit date: **16 October 2026**. Owner: Haiqa Mushtaq. Status: **collected and statically inspected; no model or notebook executed**. The shared academic-research-suite's bounded source-verification workflow guided this task. This is an assistant's source study, not an attestation that a researcher has read or understood the papers.

We have enough material to study how the three candidates process data and produce an output. We do **not** have three comparable, runnable reproductions. Start with CASPER's physical experiment and prediction task; then study TWINE's controller classifier and state representation; finally use CatBoost's source to understand why target construction and splitting matter as much as the algorithm.

## What is local

The [source-pack manifest](../baselines/SOURCE_PACK_MANIFEST.json) records immutable repository revisions, source URLs, receipt times, sizes, SHA-256 hashes, Git blob hashes, file types and structural checks. Original bytes are read-only under each ignored `baselines/<method>/artifacts/source_snapshot/` directory. Existing manuscript/code snapshots were preserved. This is a selective source snapshot, not an installed environment or executable project checkout.

| Candidate | Pinned revision | Collected source/configuration/documentation | Other research material |
|---|---|---|---|
| [CASPER](https://github.com/hkayann/1D-CNN-Anomaly-Detection-via-CASPER/tree/bff03c91d155bf3134f6d801d3a4f4af7ea78adb) | `bff03c91d155bf3134f6d801d3a4f4af7ea78adb` | README, ignore file, primary 178-cell notebook | Corrected full paper is in the [manuscript collection](MANUSCRIPT_COLLECTION_AUDIT.md); notebook contains stored author outputs. Complete tree contains only an autosave notebook and two OS metadata files beyond these selected sources. |
| [TWINE](https://github.com/mubashar-iqbal/TWINE/tree/841e1195acf90835c4c427e0fb48d10c08ed30d5) | `841e1195acf90835c4c427e0fb48d10c08ed30d5` | All nine tracked blobs: two notebooks, three Python files, twin JSON schema, README, ignore file and MIT license | Full-text access is tracked separately in the manuscript audit. A linked demonstration video was not collected; source study does not require a cloud deployment. |
| [CatBoost on CASPER](https://github.com/Priyanshu-byte-coder/CatBoost_Anomaly_Detection_implementation/tree/7f2a691f94f548e6b7c744ee0eeee287489a8639) | `7f2a691f94f548e6b7c744ee0eeee287489a8639` | Three Python files, README, requirements and ignore file | Author-reported result artifacts: 20 CSV tables, 14 TeX tables and 15 PNG figures. They are **unreplicated author artifacts**, not our results. |

The source/configuration/documentation subset is **18 files / 2,333,596 bytes**. The additional CatBoost tables and figures are **49 files / 4,143,670 bytes**. Three complete GitHub tree receipts are also retained. The original CASPER dataset is already received separately; see [the dataset identity audit](CASPER_DATASET_IDENTITY.md). Do not duplicate dataset files inside each baseline folder.

Licenses need separate treatment. TWINE includes an MIT license and acknowledges inherited `seleniumforest` code. CASPER's README shows an MIT badge, but the complete pinned tree has **no license text**; a badge does not supply the missing terms or establish the successor repository's license applies retroactively. CatBoost has no license file in the complete pinned tree. Public availability permits this evidence inspection but is not a verified reuse or redistribution license. Both code-use questions remain unresolved.

## CASPER: trace one prediction into one alarm

Read the [corrected paper](../baselines/casper/artifacts/casper_corrected_vor_v1.1.pdf) alongside the [pinned notebook](../baselines/casper/artifacts/source_snapshot/notebooks/casper.ipynb). Notebook cell numbers below are **zero-based**. The notebook includes several methods; the first controlled learning target is its 1D-CNN predictor.

| Stage | Source location | Meaning and question to resolve |
|---|---|---|
| Acquisition interpretation | Cells 1–25; paper §§6.3–6.4 | `nicla.csv` supplies nine external IMU channels. Controller labels help retrospectively annotate IMU motion. Skip six malformed startup records, discard 897 initial numeric rows, and apply a 20-row trailing median. These transformations create different row-coordinate systems. |
| Annotations | Cells 23–25 | Eight manually chosen intervals define anomalies on the filtered IMU series. The normal prefix ends at filtered row 1,072,450. This is retrospective annotation, not timestamps delivered by the IMU. Preserve the six-sample disagreement between the final interval's source code and explanatory text until resolved. |
| Training information | Cells 79, 81–83 | Sequential 60/20/20 partitions of the declared normal prefix; StandardScaler fitted on the training partition. Seeds differ by library: Python 12345, NumPy 42, TensorFlow 1234. These are observed author settings, not a configuration we have executed. |
| Prediction model | Cells 81–82 | Input shape `(batch, 755, 9)`; predict the next nine-channel observation with output `(batch, 1, 9)`. Four Conv1D layers, two pooling layers, flatten and dense output appear in this code. Resolve the paper's prose/architecture description before claiming exact equation-to-code fidelity. |
| Optimization | Cells 81–83 | MSE objective, Adamax, maximum 100 epochs, validation-loss early stopping with patience five, batch size 1024. There is no explicit `restore_best_weights=True` in the shown callback; do not assume the returned in-memory weights are the best validation checkpoint. |
| Model actually evaluated | Cell 85 | A later `load_model('../models/1DCNN.keras')` replaces the freshly trained object. No `models/` files exist in the pinned tree. The loaded checkpoint's origin is unresolved; training history cannot establish the provenance of predictions from that replacement. |
| Residual and score | Cells 88–95 | Inverse-transform predictions, compare to observed nine-channel vectors using per-row RMSE, then sum 755 consecutive residuals. Predictor history, median filter and score aggregation all contribute to support and warm-up. Majority labels over the score window are different from endpoint labels and event onset. |
| Threshold and reported metrics | Cells 97–99 | Search 1,000 thresholds against the evaluated anomaly labels and retain maximum F1. This is an oracle selection path, ineligible for our held-out results. A normal-calibrated threshold would be a disclosed protocol modification. |

The code's error is first computed in the original nine-channel numerical scales. Accelerometer, gyroscope and magnetometer channels have different meanings; the cross-channel RMSE is not a physical distance in one unit. That is a property of the inspected score definition, not proof that it cannot detect the recorded deviations.

The notebook also contains PLS, LSTM prediction, LSTM/CNN autoencoders, XGBoost and one-class SVM sections. Their presence does not make them separate recent papers. We have inventoried their source, but this study does not certify every branch's equations, preprocessing or evaluation. Establish one traceable path before expanding the reproduction scope.

Missing execution resources include an environment lock, documented dependency versions, saved derivative arrays (`outputs/nicla_*.npy`), the referenced model checkpoint and its training provenance, and a resolved time/annotation contract. The arrays can be derived only after their lineage is specified; they should not be treated as original raw data. The README links a successor TinyML repository and a Node-RED collection package, but neither establishes the original publication's exact acquisition revision or checkpoint.

## TWINE: distinguish training, explanation and twin synchronization

Read [training.ipynb](../baselines/twine/artifacts/source_snapshot/scripts/training.ipynb) first. Then inspect [the simulation notebook](../baselines/twine/artifacts/source_snapshot/simulation_robotic_arm.ipynb), [anomaly_detection.py](../baselines/twine/artifacts/source_snapshot/scripts/anomaly_detection.py), [digital_twin_azure.py](../baselines/twine/artifacts/source_snapshot/scripts/digital_twin_azure.py), and [the twin schema](../baselines/twine/artifacts/source_snapshot/model/digital-twin-schema.json).

| Path | Direct source evidence | Consequence for study/reproduction |
|---|---|---|
| Full-feature training | Training cells 2–6 expand list-valued columns; select six named scalars plus expanded vectors; target is `Anomaly_State`. Cells 8–10 use a stratified random 80/20 split and RF with 100 trees, unrestricted depth and seed 42. | The detector receives controller information and attack labels for fitting. This is different information access from CASPER's normal-only external-IMU predictor. The random-row split is not our chronological replay protocol. |
| Explanation | Training cell 15 replaces `rf_model` with 50 trees and depth 10 before SHAP analysis. `predictive_maintenance.py` lines 8–17 independently fits another 100-tree model. | The explanation and reported prediction paths need an explicit model/version match. SHAP describes a fitted classifier's output, not proof of physical attack causation. |
| Demo data | Simulation cell 16 selects five scalars, retains every 100th row, randomly splits 80/20, and resets indices. | This is a separate feature/subsampling path from full-feature training. A reset index is not a restored timestamp or chronological replay. |
| Twin state | `digital_twin_azure.py` lines 54–91 write the five measurements and predicted anomaly state into Azure; JSON schema contains those six properties. | The inspected twin is an observed-state and classifier-output representation. This code does not establish a predictive process model or a corruption-resistant update rule. |
| Prediction helper | `anomaly_detection.py` lines 42–52 accepts a model parameter but predicts through the module-global `rf`. | A caller can pass a different model without it being used. Preserve this as a static implementation defect; no runtime failure was induced here. |
| Demo metrics | Simulation cell 19 generates five predictions; cell 23 compares them with fifteen labels. | The requested metric inputs have inconsistent lengths if those cells run as shown. This is distinct from the full-feature notebook's evaluation path. |
| Incomplete demo resources | Last simulation cell calls `pm.create_shap_beeswarm_all`, absent from the supplied module. The dashboard loads `./Data/alarm.jpg`, absent from the complete tree. | This snapshot does not support an unmodified end-to-end demo. Missing UI resources do not by themselves invalidate the separately fitted RF. |

The README recommends Python 3.7.9 and unpinned installation commands. It does not provide a locked environment; the tree contains no requirements file. The code also imports packages beyond that short README list. Do not infer that the old interpreter plus current package versions will work. No Azure login, credential lookup, schema upload or service call was performed. The full paper's exact correspondence to these separate code paths remains subject to the [manuscript audit](MANUSCRIPT_COLLECTION_AUDIT.md).

## CatBoost: inspect the target before the classifier

Start with [final_multi_run.py](../baselines/catboost/artifacts/source_snapshot/final_multi_run.py). The repository title and README discuss self-supervised fault detection; the linked paper emphasizes CatBoost. Matched authorship and an article link are useful provenance, but they do not establish that this revision generated every published table.

| Stage | Source lines | What the source actually does |
|---|---|---|
| Input | 59–89 | Reads raw `nicla.csv` with six startup lines skipped and `right_arm.csv`; concatenates CSV chunks back into memory. It does not load a pre-aligned multimodal time series. |
| Controller branch | 122–184 | Randomly samples up to 100,000 rows, expands list fields, uses `Anomaly State` labels. Broad parsing exceptions insert zeros; ragged feature vectors are padded. A valid dataset loader should instead expose schema failures and document any repairs. |
| IMU branch | 186–206 | Randomly samples up to 100,000 IMU rows and creates positive labels from the largest five percent of acceleration norms. These are synthetic outlier labels, not the original attack schedule. |
| Combining modalities | 471–484 | Pads the nine IMU features to the controller width, then stacks IMU and controller observations as rows and concatenates their labels. This is not time-aligned sensor fusion; corresponding columns can have different physical meanings. |
| Scaling and splits | 492–501 | Fits StandardScaler to the full combined matrix before random stratified 60/20/20 splitting. Both the target definition and this preprocessing violate the proposed common evaluation contract. |
| Label use in the “SSL” branch | 264–300 | Combines reconstruction MSE with cross-entropy on `batch_y`: `0.6 * reconstruction + 0.4 * classification`. The inspected training objective is not label-free merely because the class/README says self-supervised. |
| CatBoost control | 554–565 | 200 iterations, depth six, learning rate 0.1 and per-run seed. `train_and_evaluate_ml_model` fits on training rows and separately predicts validation/test rows. The earlier combined-data construction still controls the scientific meaning of these scores. |
| Metrics | 414–428 | Reports **support-weighted** F1/precision/recall, and ROC AUC where available. These are not automatically positive-attack F1 or precision–recall AUC. On exceptions, AUC becomes zero instead of an explicit missing status. |
| Invocation | 26–28, 592–600 | Ten predefined seeds; a top-level loop starts all experiments. There is no `if __name__ == '__main__'` guard. Importing this module can start training; inspect it as text only. |

The collected [requirements.txt](../baselines/catboost/artifacts/source_snapshot/requirements.txt) contains lower version bounds, not a lock. `testing_imbalancing_methods/final.py` is a separate single-run branch that also trains at top level and saves preprocessed arrays near its end. `imbalance_comparison.py` expects those arrays and imports `imblearn`, which is absent from the supplied requirements. These auxiliary scripts were syntax-checked and their entry/data dependencies inspected; their full numerical behavior has not been audited.

The author result folders contain per-run summaries, aggregate tables and plotted comparisons. Their file names and reported values do not independently verify source revision, original-file hashes, fit/test membership, uncertainty assumptions, or physical attack labels. “Different random seeds” over one recording does not establish independent physical experiments. Keep these artifacts in the baseline source pack, separate from our future `experiments/` outputs.

## What to learn next and what must wait

1. **Understand the observation.** Compare nine external IMU channels with the controller's scalar/vector fields. Identify which information each method receives and which signals an attacker could corrupt. Use the [dataset identity audit](CASPER_DATASET_IDENTITY.md), not a guessed unified row index.
2. **Trace CASPER's score without training.** Explain the sequence: past IMU observations → next-observation prediction → residual → aggregated score → calibrated alarm. Mark the row coordinate and eligible history at each stage. The [Step 0 lesson](RESEARCH_BASICS_LESSON.md) supplies a small synthetic example.
3. **Explain why TWINE is a different task.** Identify controller inputs, supervised labels, RF predictions, explanations and cloud properties separately. Determine the twin contribution from supported paper/code evidence before designing our own.
4. **Explain why the CatBoost script is not yet an admissible comparison.** The problem is not the choice of CatBoost; it is the data/label contract, scale fitting, chronology and reported metric definitions. A clean controller-only CatBoost control would be an independent implementation unless exact paper correspondence is established.
5. **Freeze the scientific contract before execution.** Resolve annotation/time correspondence and code-use terms; choose the permitted input/training-label group; freeze features, chronological partitions, preprocessing, score alignment, calibration and metrics under [the proposed protocol](COMPARISON_PROTOCOL.md). Retain unresolved papers on hold rather than converting source availability into admission.

No final baseline selection, training command, performance table or novelty claim follows from this collection. We can read and reason about the materials now. Environment construction and any later pilot should start from a reviewed, bounded configuration after the outstanding gates are resolved.

## Receipt and checks

Collection commands, from `/Users/matrixusman/CUI/DigitalTwin`:

```text
python3 manufacturing/local/source_pack_collection/collect_source_pack.py
python3 manufacturing/local/source_pack_collection/collect_reported_artifacts.py
```

Both collectors are retained in ignored local storage; their hashes and actual UTC times appear in the manifest. They perform public HTTP reads, local writes and structural validation only. Source trees were complete (`truncated=false`). Every collected artifact matches its pinned Git blob and SHA-256 receipt. JSON/notebooks parse, the six Python source files pass AST parsing, CSV result tables parse, and PNG signatures/chunk CRCs validate. Existing selected source snapshots and their new equivalents were compared by bytes. No Git LFS pointer or HTML error body was accepted as a source file.

Notebook stored outputs were preserved without execution. Figure file integrity does not verify its statistical content or paper correspondence. No datasets, fitted model objects, cloud secrets or new experiment outputs were taken from these repositories. Raw CASPER files were neither modified nor copied into the code pack. The parent task maintains the project status and work log.
