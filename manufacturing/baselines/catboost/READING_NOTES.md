# CatBoost on CASPER: source reading and result provenance

Audit date: **16 October 2026**. Project: manufacturing; owner: Haiqa Mushtaq. **The full manuscript remains unavailable.** This note studies the official abstract, publisher-deposited metadata, institutional/author records, pinned implementation and author-reported result files. It does not claim a full-paper reading, a faithful reproduction, a model run or researcher understanding.

The paper and author repository are genuine identifiable records. Its headline accuracy/F1 can now be traced numerically to the repository's ten-run summaries. That correspondence is useful, but the input/label construction, evaluation protocol and missing run provenance still prevent admitting this implementation to our benchmark.

## Identity and available evidence

**Paper:** Priyanshu Doshi, Neal Daftary, Hetavi Jani and Anuja Nair, *CatBoost-Driven Anomaly Detection in Industrial Robotic Arms Using CASPER Dataset*, IEEE Sensors Letters **10(2), 1–4**, February 2026 issue. [DOI](https://doi.org/10.1109/LSENS.2026.3656499). The [publisher-deposited Crossref record](artifacts/crossref.json) supports title, authors, journal, issue and DOI. Its record-creation timestamp of 21 January 2026 is **not** independently verified as the first-online publication date.

The [official APSCON record](https://epapers2.org/apscon2026/ESR/paper_details.php?paper_id=6394) lists a Sensors Letters route and poster acceptance. Treat that presentation as the same work, not a second independent baseline. [Nirma University's announcement](https://cse.nirmauni.ac.in/students/achievements/) independently identifies the title, four authors and DOI. Its promotional venue-ranking language is not used as methodological evidence here.

The [first author's GitHub profile](https://github.com/Priyanshu-byte-coder) explicitly connects the IEEE article and implementation repository. The [pinned repository](https://github.com/Priyanshu-byte-coder/CatBoost_Anomaly_Detection_implementation/tree/7f2a691f94f548e6b7c744ee0eeee287489a8639) is revision `7f2a691f94f548e6b7c744ee0eeee287489a8639`; all its tracked files are available in [the local source snapshot](artifacts/source_snapshot/README.md). Receipts and hashes are in [SOURCE_PACK_MANIFEST.json](../SOURCE_PACK_MANIFEST.json). No license file was found in that complete tree; reuse terms remain unresolved.

New lawful full-text follow-up checked the university announcement and the author's portfolio. Both lead to IEEE rather than a manuscript download. The portfolio's public JavaScript was inspected **as text**, not executed; its research link is the same IEEE document. IEEE still presents a robot-verification page to the web tool. No verification challenge, account restriction or paywall was bypassed. The official abstract, university page and public portfolio receipts are retained in ignored [local audit storage](../../local/catboost_result_audit/public_source_receipts.json). Missing text remains an access limitation, not evidence of nonexistence.

## What the abstract claims, and what we can actually connect

The official abstract describes a robotic-arm fault/anomaly task, a nominal 200,000-observation subset, six compared approaches and CatBoost's reported accuracy **97.20%** with F1 **0.9718**. It does not establish a process-state twin or attack attribution. Those numbers are author claims, not our measurements. [Official abstract](https://epapers2.org/apscon2026/ESR/paper_details.php?paper_id=6394).

| Abstract/record item | Available source connection | Verdict |
|---|---|---|
| CASPER data | Main loader reads `data/nicla.csv` and `data/right_arm.csv`. README/reference metadata also mention the successor CASPER 1 & 2 listing. | Filenames match the original collection, but published-run hashes/releases remain unknown. |
| 200,000 observations | Two preprocessing functions each sample at most 100,000 rows before concatenation. | Consistent with the intended combined size when both branches retain 100,000 rows. No saved row IDs or arrays establish the exact paper sample. |
| Stratified subset | Sampling inside each branch uses random `.sample(...)`; a later stratification helper immediately returns when length is at most 100,000. Train/validation/test splits are stratified. | The initial selected rows are not stratified by that helper on the normal 100,000-row path. Distinguish initial sampling from the subsequent stratified split. |
| CBC and five alternatives | The script contains CatBoost, SVM, LR, NB, QDA and an encoder/decoder/classifier called SSL. | Model names map, but input access, target semantics and metric choices must also map. |
| Accuracy 97.20%, F1 0.9718 | These equal the rounded **mean testing accuracy** and **mean support-weighted F1** in the ten-run author file. | Numerical correspondence verified; published execution lineage still unverified. |
| Regularization and imbalance-aware learning | Main CatBoost call sets 200 iterations, depth six, learning rate 0.1 and a seed. Separate auxiliary scripts test class weights and resampling. | No evidence establishes which auxiliary treatment, if any, belongs to the paper's headline run. Do not silently combine settings from different branches. |

The abstract expands CASPER as “collaborative arm sensing for predictive error recognition,” whereas the original CASPER paper is titled *Context-Aware IoT Anomaly Detection System for Industrial Robotic Arms*. This is a naming discrepancy to resolve. It does not establish a different dataset because the source filenames and original-paper citation still connect to the CASPER collection.

## The actual computational path

All line references below are to the immutable [final_multi_run.py](artifacts/source_snapshot/final_multi_run.py). Reading it as text is essential: its top-level loop starts ten experiments, including neural-network training, if imported or executed.

1. **Load and sample:** lines 59–89 load the IMU/controller CSVs. Lines 122–184 sample controller rows and expand vector-valued fields; the source label is `Anomaly State`. Lines 186–206 sample the IMU and assign positive labels to acceleration norms exceeding their sample's 95th percentile. The IMU labels are synthetic outlier targets, not the recorded attack schedule.
2. **Combine different observations:** lines 471–484 pad IMU vectors and stack them below controller rows. This is not synchronized sensor fusion. A feature position can represent a different physical quantity depending on the row's modality, and the two branches have different label definitions.
3. **Scale, then randomly split:** lines 492–501 fit StandardScaler before the split, exposing all selected rows to the fitted transform. The intended 60/20/20 split would be 120,000/40,000/40,000 rows if 200,000 survive preprocessing. Actual split row IDs and saved run arrays are absent. Chronology and attack episodes are not preserved by random sampling/splitting.
4. **Fit:** lines 554–565 construct CatBoost with fixed visible parameters; lines 386–432 fit the classical estimators on `X_train` and separately evaluate validation/test partitions. The SVM path uses at most 20,000 training rows, whereas the other classical estimators receive all available training rows. The code does not show an explicit CatBoost hyperparameter-search or checkpoint-selection procedure for the headline run.
5. **Score:** lines 414–428 compute support-weighted F1, precision and recall; AUC is ROC AUC from predicted class probabilities. No per-attack recall, chronological alarm episode, detection delay or false alarms per hour is computed in this path. AUC failures become zero rather than an explicit missing result.
6. **Repeat and aggregate:** lines 26–28 define ten seeds; lines 435–476 resample and split under each seed; lines 592–600 run the experiments. Lines 622–652 compute the means, population standard deviations and Student-t intervals. These are repeated randomized analyses of the same source collection, not ten independent physical plant runs.

The SSL-labelled branch is not label-free: lines 264–300 combine reconstruction MSE and cross-entropy using `batch_y`, with weights 0.6 and 0.4. The name therefore cannot justify placing that code in a normal-only unsupervised comparison. A clean controller-only CatBoost reference would remain useful to consider, but implementing it under our valid data/split contract would be an **independent implementation**, not an established faithful reproduction of this paper.

## Where the headline numbers come from

The following values were recomputed **only from the authors' stored run-level metrics**, not from raw sensor measurements or model predictions. [Author run file](artifacts/source_snapshot/output2/multi_run_raw_results.csv), [author detailed summary](artifacts/source_snapshot/output2/statistical_summary_detailed.csv), and [our arithmetic audit](../../local/catboost_result_audit/author_table_audit.json).

| CatBoost quantity in author file | Arithmetic result | Interpretation |
|---|---:|---|
| Mean `testing_accuracy` | 0.9719525 | 97.19525%, which rounds to the abstract's 97.20% |
| Mean `validation_accuracy` | 0.972455 | 97.2455%; different from the preceding quantity |
| Mean `f1_score` | 0.9718004327472999 | Rounds to 0.9718; source defines this as support-weighted F1 |
| Maximum single-run `testing_accuracy` | 0.972675 | The headline is not this best-run value |
| Mean ROC AUC | 0.9940723051650129 | Consistent with the author's rounded 0.9941; not PR AUC |
| Mean `recall` | 0.9719525 | Support-weighted recall; equals accuracy under the source's single-label classification definition |

The author file has **60 rows: six algorithms × ten run IDs**, with seeds `[42, 123, 456, 789, 1011, 1213, 1415, 1617, 1819, 2021]` for every algorithm. “Raw results” in that filename means raw **run summaries**. It contains no per-observation scores, true labels, sampling indices, preprocessing fit records, model hashes or logs.

The arithmetic of [output2/statistical_summary_detailed.csv](artifacts/source_snapshot/output2/statistical_summary_detailed.csv) is consistent with the stored run metrics: all **48 means**, **48 population standard deviations**, and **96 confidence-interval endpoints** passed the audit. That supports internal aggregation consistency. It does not validate the underlying observations, random-split design, target construction or exact published run.

## Three result-provenance issues that matter

### 1. A “validation” heading contains test values

For every algorithm, `Val Acc` in [multi_run_average_comparison.csv](artifacts/source_snapshot/multi_run_analysis_output/multi_run_average_comparison.csv) equals the mean of raw `testing_accuracy`, not `validation_accuracy`. Likewise, `Val Accuracy` in [CBC_all_runs_transposed.csv](artifacts/source_snapshot/multi_run_analysis_output/CBC_all_runs_transposed.csv) matches the ten test values. The same heading propagates into [the TeX table](artifacts/source_snapshot/latex_tables/comprehensive_metrics_fixed.tex).

The [validation_accuracy_comparison.png](artifacts/source_snapshot/multi_run_analysis_output/validation_accuracy_comparison.png) was visually inspected: its y-axis says validation accuracy, while its six printed values match the rounded test means. This is a direct inconsistency **within the repository artifacts**. Without the full paper, do not assert that its table uses the same erroneous heading. Preserve the original artifact and explain the mapping instead of silently relabelling its contents.

This refines the earlier manuscript-audit observation that the collected table was labelled validation accuracy. The label is indeed present, but tracing its values now identifies a mismatch with the author's raw column names. Neither label should be uncritically copied into our own result table.

### 2. The standard-deviation convention changes across folders

The main script calls `np.std(values)` without `ddof`, matching the population SD stored under `output2/`. The later transposed tables under `multi_run_analysis_output/` numerically match **sample SD**, using denominator `n−1`. All **42 transposed sample-SD entries** and **420 rounded per-run values** were checked against the raw file.

For CatBoost test accuracy, population SD is **0.0004965443**, while sample SD is **0.0005234037**. Both round to 0.0005 at four decimals; apparent agreement after rounding hides the change of definition. CatBoost precision makes it visible: population SD **0.0005254052** rounds to 0.0005, while sample SD **0.0005538258** rounds to 0.0006.

The stored intervals match `mean ± t(0.975, 9) × sample_SD / sqrt(10)`, consistent with `stats.sem` and `stats.t.ppf` in the source. Checking that arithmetic does not establish independent observations or justify a plant-level generalization claim. The three collected Python files do not contain a generator for the later `multi_run_analysis_output/` and `latex_tables/` outputs, so their transformation provenance is incomplete even where numeric correspondence is strong.

### 3. Timing columns mix units and execution records

`evaluate_pytorch_model` at lines 347–384 averages forward-pass elapsed time **per minibatch**. The main batch size is 256. `train_and_evaluate_ml_model` at lines 409–412 instead divides prediction time by the number of rows, giving **seconds per observation**. A shared `inference_time` heading does not make these comparable. Batch boundaries, device synchronization, preprocessing costs and source hardware also need a consistent measurement contract.

[complete_results.csv](artifacts/source_snapshot/output2/complete_results.csv) and raw run 0 share all compared predictive metrics, but their training and inference timings differ for all six algorithms. For CatBoost, the training times are approximately **3.860 s** and **4.103 s**, respectively. This could reflect separate executions; without logs we cannot establish their relationship. Do not assemble a table by taking accuracy from one artifact family and runtime from another while implying a single verified experiment.

## What the auxiliary imbalance results establish

[imbalance_comparison_results.csv](artifacts/source_snapshot/testing_imbalancing_methods/results/imbalance_comparison_results.csv) stores 12 model/treatment rows, not ten repeats of every treatment. Its baseline rows report 120,000 training observations, with 105,166 normal and 14,834 positive labels. That is evidence of the counts **reported in that auxiliary artifact**, not a validation of all main-run splits or authentic attack labels.

Its baseline CatBoost predictive values match the main run-0 values; its timing differs again. The class-weight/resampling variants therefore need their own provenance rather than being assumed to explain the headline mean. Several SSL validation-accuracy cells are literal zero; the companion code passes zero as a placeholder when saving those entries. They must not be interpreted as measured 0% validation performance. Full auxiliary-method numerical validation is outside this note's coverage.

## What we can responsibly learn and what remains missing

We can learn the supervised tree-ensemble workflow, the distinction between validation and test records, how weighted metrics differ from attack-class metrics, and why normalization/label/split choices must precede numerical comparisons. The source is useful precisely because it exposes those choices and several failure modes.

Before treating this as a numerical baseline we still need the full manuscript; exact release/file/split hashes and selected row IDs; authentic label semantics; an admissible chronological evaluation; explicit metric conventions; the published configuration and dependency versions; result-generator/run logs and code-use terms. Our source audit supplies none of those missing experimental records by inference.

The next bounded action is to keep this candidate on **critical-learning / reproduction hold**, finish the available-paper study, and decide whether a clean CatBoost control belongs in the common supervised-controller track. Do not tune a new implementation against these published scores or held-out attack outcomes. Readiness and the common protocol remain governed by [the comparison plan](../../docs/COMPARISON_PROTOCOL.md).

## Audit command and coverage

From `/Users/matrixusman/CUI/DigitalTwin`:

```text
python3 manufacturing/local/catboost_result_audit/audit_author_tables.py
```

This standard-library audit reads preserved author CSV summaries, computes aggregates, verifies correspondence and writes ignored audit metadata with input/script hashes, Python version and UTC time. It never imports the author scripts, opens raw CASPER observations, fits a model or selects a threshold. The Student-t quantile was independently computed by integrating the t(9) density through a cosine-power recurrence and bisection; interval differences were below `3.5e-11`. Author artifacts remain unchanged.

Search follow-up used exact title/identifier plus institution/author routes; irrelevant search hits were discarded. No new full paper was found. One reported figure was visually checked; this is not a visual or scientific audit of all 15 figures. Static source evidence, arithmetic checks, publication identity and manuscript availability remain separate statuses. No experimental result or human reading completion is claimed.
