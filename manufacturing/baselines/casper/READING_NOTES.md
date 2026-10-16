# CASPER: paper-to-code reading record

AI-assisted reading and static audit, 16 October 2026. Project: manufacturing / Haiqa Mushtaq. **No upstream code, model or preprocessing pipeline was executed. No benchmark results were reproduced. This record does not mark any researcher as having read the paper.**

CASPER is useful here as an externally sensed, non-twin anomaly detector and dataset-producing study. It predicts robot motion measurements from past measurements; the inspected implementation does not contain a process-state digital twin, online adaptation or a trusted update gate. Its concrete experimental task is detecting eight deliberately changed robot-speed intervals in a repetitive pick-and-place operation. That is narrower than identifying arbitrary cyberattacks or establishing the cause of an anomaly.

## Sources and reading scope

- [Corrected author-hosted version of record](https://ngcharithperera.gitlab.io/publications/pdfs/Kayan2024a.pdf), **CASPER: Context-Aware IoT Anomaly Detection System for Industrial Robotic Arms**, Kayan, Heartfield, Rana, Burnap and Perera; [DOI 10.1145/3670414](https://doi.org/10.1145/3670414), ACM Transactions on the Internet of Things 5(3), article 18, August 2024. The manuscript records acceptance on 13 May 2024. Its front matter identifies corrected VOR V1.1, 5 February 2025; the changes from the preceding version remain unspecified in our evidence.
- Local PDF: `artifacts/casper_corrected_vor_v1.1.pdf`; SHA-256 `323efce849d75e16833f166983a7387b6d8f86760ce889fe4918ff2f775be186`. Layout-preserving extraction: `artifacts/casper_corrected_vor_v1.1.txt`.
- [Author notebook at revision bff03c91d155bf3134f6d801d3a4f4af7ea78adb](https://github.com/hkayann/1D-CNN-Anomaly-Detection-via-CASPER/blob/bff03c91d155bf3134f6d801d3a4f4af7ea78adb/notebooks/casper.ipynb), local `artifacts/casper.ipynb`; SHA-256 `3f1beff113c904473cb554aa79edde7af31d777c4731eb93ba900e3aa4a5fea0`. **All cell numbers below are zero-based positions in its 178-cell JSON**, not execution counters.
- Read all main-text sections, abstract and conclusion, PDF pp. 1–30. Visually inspected Figures 1–12 and the key method/architecture/label tables and Algorithm 1. References pp. 30–36 contain 141 numbered entries; their presence was inventoried, not their individual accuracy verified. Historical incidents and related-work claims remain claims made by this paper.
- Fresh visual evidence is retained in ignored `artifacts/reading_renders/`, with hashes, page numbers and renderer details in `artifacts/reading_renders/RENDER_RECEIPT.json`. Previously inspected Table 11 and Algorithm 1 are in `artifacts/dataset_table11_page18.png` and `artifacts/algorithm1_page24.png`. Rendering is document inspection, not an experiment.

The [collection audit](../../docs/MANUSCRIPT_COLLECTION_AUDIT.md), [source manifest](../SOURCE_PACK_MANIFEST.json) and [dataset identity record](../../docs/CASPER_DATASET_IDENTITY.md) hold broader provenance. Public availability of a notebook does not resolve its code-use terms: the README displays an MIT badge, but its complete pinned repository tree has no license text. The separate successor TinyML repository is not the same source version.

## Read the argument before the architecture

| Paper location | What the section contributes | Connection to the inspected code and limits |
|---|---|---|
| §1, pp. 2–4 | Motivates independent physical sensing when controller/network observations might be manipulated. | Explains why the detector uses externally attached IMU measurements. No network IDS, attack attribution or autonomous response is implemented in the notebook. |
| §2, pp. 4–6; Table 1 | Historical incidents motivate cyber/physical monitoring. | Context, not experiments reproduced by this code. Incident narratives and their references require separate verification before reuse. |
| §3, pp. 6–9; Tables 2–3 | Reviews robot anomaly detection, sensor modalities and edge computing. | Establishes alternatives, not a common-dataset rerun of every cited method. §3.2 describes edge anomaly detection as future work. |
| §§4.1–4.2, pp. 9–10; Figure 1 | Distinguishes point, contextual and collective anomalies, then scores and thresholds. | The implemented CNN score is a sum of residual RMSEs, not a probability or a value necessarily bounded by one. |
| §4.3, pp. 10–11; Table 4, Figure 2 | Describes a phishing-to-controller-compromise scenario and altered robot speed. | Table 4 identifies CASPER's experimental mechanism as manual joint-velocity manipulation. The notebook cannot verify that phishing, firewall bypass or false telemetry delivery was executed. Preserve the distinction between the scenario and the measured physical intervention. |
| §5, pp. 11–13; Tables 5–6 | Separates sensor/edge, Raspberry Pi fog monitoring, and central ML computation. | The notebook provides central/offline analysis. BLE separation and encryption claims do not demonstrate resistance to compromise of the sensor, fog host or training history. |
| §6.1, pp. 13–15; Tables 7–8, Figure 3 | Describes two UR3e arms alternately moving a steel ball and the equipment/software. | No robot-control script, plant simulator or kinematic state model exists in the pinned detector tree. Controller CSVs are not the CNN's input. |
| §6.2, pp. 14–17; Figure 4, Table 9 | Compares sensor boards, noise and orientation representations. | Cells 31–32 compare Madgwick/Mahony quaternion correlations using the normal IMU data. These are not the three-board acquisition/power experiment, nor a quaternion-input detection model. |
| §6.3, pp. 17–18; Figure 5, Tables 10–11 | Describes the changed-speed schedule and IMU/controller/network recordings. | Cells 2–25 load, trim, filter and manually annotate IMU data. Paper schedule times do not supply missing IMU timestamps. |
| §§6.4.1–6.4.2, pp. 19–21; Figures 6–9, Tables 12–13 | Discusses noise removal, periodicity and feature correlations. | Cells 21, 27, 29, 31–32, 37, 39. The final detector still receives all nine raw-IMU channels after filtering/scaling; CCA/quaternion analysis is exploratory. |
| §§6.4.3–6.4.9, pp. 21–24; Figures 10–11, Algorithm 1 | Defines statistical, PLS, neural, tree and one-class comparators. | Notebook ranges below expose differences in training fraction, score units, output support and threshold selection. These cannot be treated as interchangeable evaluation records. |
| §6.4.10, pp. 24–26; Table 14 | Reports accuracy, recall, FPR, precision, F1 and inference latency. | Published results only. Thresholds in most notebook branches maximize F1 on evaluated anomaly labels; timing excludes parts of the alarm pipeline. No common independent calibration is established. |
| §6.5, pp. 26–27; Figure 12, Tables 15–16 | Demonstrates BLE collection, Node-RED, InfluxDB and Grafana monitoring/resource use. | Figure 12 shows telemetry monitoring. The detector snapshot does not contain exported Node-RED flows, Grafana configuration or measurement logs for the resource tables. |
| §6.6, pp. 27–29 | Discusses unsynchronized devices, manual label matching, idle intervals, correlation, tuning and missed point anomalies. | Supports retaining clock/annotation limitations. Its dismissal of training compromise is an assumption, not a poisoning experiment. |
| §7, pp. 29–30 | Concludes and proposes online learning, quaternion features, more interventions and edge detection. | These are future directions, not demonstrated components of this notebook. They also prevent a novelty claim based simply on adding online learning. |

The original README links an additional author project, [node-red-contrib-ble-sense](https://github.com/hkayann/node-red-contrib-ble-sense), and names its `niclaBLEIMUStruct` firmware folder. That is an explicit hardware-code lead outside this pinned detector tree; this reading did not audit that repository or establish its historical version. The generic sensor libraries referenced in §6.2 likewise are dependencies/leads, not complete experiment source packages.

## The measured problem and its trusted information

The equipment is physical, and the external sensor captures motion independent of the controller's reported values. The study assumes repetitive operation, an initially clean training period and an adversary controlling the controller-to-arm communication path. It does not establish what happens if an adversary tampers with the IMU, BLE receiver, fog computer or training data. Calling the sensing path out-of-band does not by itself prove those assets trustworthy.

Table 10 defines eight changed-speed intervals: increases of 10%, 35%, 65% and 100%, decreases of 50% and 5%, then a 20% increase and 25% decrease. These changes are relative to the stated default joint speed of 1.05 rad/s. The paper reports one approximately day-long repetitive task. It does not supply an independently labelled collection of legitimate new production modes against which safe adaptation can already be assessed.

Consequently, an alarm means a motion pattern differs from the learned reference under this experiment. It does not determine whether the change came from an attacker, wear, maintenance or a permitted command. Demonstrating a digital twin, cause attribution or protection against contaminated adaptation would require additional definitions and evidence.

## Data and CNN path, with exact code locations

| Stage | Notebook cells | What is actually specified |
|---|---|---|
| Receipt assumptions | 1–2 | Nine IMU columns, six skipped startup records; the notebook describes variable sampling and different device start/stop times. The received IMU file has no timestamp or label column. |
| Trimming/annotation | 8, 17, 20–25 | Drop 897 initial rows; apply trailing median width 20; manually mark eight intervals after inspecting GyroX; assign the first 1,072,450 filtered rows to the normal prefix and save separate normal/mixed/label arrays. |
| Exploratory processing | 27, 29, 31–32, 37, 39 | Correlation, CCA and quaternion comparisons; normal-data periodicity search uses rows 300,000–399,999. Cell 37 also studies the mixed segment. These operations are not a frozen validation-only search manifest. |
| Partition/scaler | 82 | Chronological 60/20/20 split of the normal prefix, then StandardScaler fitted on its training portion only. Windows are constructed within these partitions, but the earlier median operation has already crossed their eventual boundaries. |
| Predictor | 81–83 | Input 755 filtered rows × nine features, target the next nine values, stride one. Four Conv1D layers, each 32 filters/kernel five/ReLU, arranged as two convolutions then pool three, repeated, then flatten, Dense(9), reshape to 1×9. MSE, Adamax, maximum 100 epochs, batch 1,024, early stopping on validation loss with patience five. |
| Model selection/state | 81, 85–87 | Early stopping does not explicitly restore best weights. Cell 85 then replaces the fitted model by loading `../models/1DCNN.keras`; cell 86 plots the preceding training history. The pinned tree contains no such checkpoint or full tuning history, so these histories and evaluated weights are not conclusively linked. |
| Prediction/residual | 88–89 | Predict the mixed segment, inverse-transform predictions, then compute nine-channel RMSE against observations from mixed row 755 onward. The score combines errors in original feature scales, not standardized residuals. |
| Aggregate/target | 92, 95 | Sum 755 successive RMSEs. Assign a positive target when at least 378 of the corresponding 755 target labels are positive. This is majority-window evaluation. |
| Threshold/metrics | 97–99 | Search 1,000 thresholds using mixed-score extrema and choose the threshold maximizing F1 on the same mixed-segment labels. Produce metrics and a confusion matrix for that selection. This is not an admissible held-out protocol for our project. |

Figure 11(a) **does show four convolutions**, matching cell 82. The shorter §6.4.5 prose mentions a pair but does not establish a two-layer final network. Do not carry forward the earlier suspected architecture mismatch. Figure 11's displayed batch-size search candidates (32, 64) do not include the notebook's 1,024; the full configuration/version history remains unresolved.

The detailed [annotation and score-index study](../../docs/CASPER_ANNOTATION_LINEAGE.md) already derives the CNN's 1,529-original-row support, final-availability endpoint, 676,807 eligible scores and majority-label class totals. Those counts match Figure 11's denominator/class sums. They establish bookkeeping consistency, not replicated predictions or an exact match to the authors' input bytes/checkpoint. Inference runtime is not event-detection delay, and nominal 20 Hz does not justify exact seconds for this untimestamped IMU sequence.

## Other implemented methods and comparison consequences

Here, `n` is the upstream mixed-segment length, 678,316 under the received-file/static-lineage assumptions. Counts describe inspected code, not execution results.

| Method / paper section | Notebook cells | Training and scoring behavior |
|---|---|---|
| Always-positive null / §6.4.10 | 34–35 | Scores all `n` point labels. It is not evaluated on the CNN's reduced majority-window target array. |
| Periodic mean template / §6.4.3 | 36–69 | Builds 1,420 disjoint length-755 windows from 1,072,100 normal rows, aligns them to the first window and averages. Aligns mixed windows too, including replacement of shifted edge positions with reference-window values. Fits MinMaxScaler to the template; computes mean featurewise RMSE over 898 disjoint mixed windows; chooses best F1. Alignment transforms the values being compared, not only their displayed timestamps. |
| PLS / §6.4.4 | 70–77 | Uses the first 10% of the normal prefix, then its 60/20/20 split; flattens 755×9 inputs, predicts next nine values with `n_components=2`, then sums standardized residual RMSE over 755 steps and selects best F1. |
| CNN / §6.4.5 | 80–99 | Uses 60% of the full normal prefix for training; next-point predictions plus residual aggregation produce `n−1509` majority-window outputs. |
| LSTM / §6.4.6 | 100–117 | Same normal split and output support as CNN. Two eight-unit LSTM layers with normalization, dropout and dense output; residual aggregation and best-F1 search. Cell 105 loads a separate, unavailable checkpoint. |
| Dense AE / §6.4.9 | 118–133 | Standardized inputs but raw-unit reconstruction targets, sliding windows of 755, stride one. Encoder widths 64/32/16; decoder 16/32/64 then 755×9 ReLU output. Raw reconstruction RMSE and majority targets yield `n−754` outputs. Cell 124 loads a separate checkpoint. |
| LSTM AE / §6.4.9 | 134–148 | Same input/target scale distinction and `n−754` outputs. Sixteen-unit LSTM encoder/decoder with dropout, RMSprop and validation callbacks; separate checkpoint load, window RMSE, best-F1 selection. |
| CNN AE / §6.4.9 | 149–160 | Same raw reconstruction targets and `n−754` outputs. Convolutions/pooling/upsampling and dense reconstruction; Adamax, validation callbacks, separate checkpoint load and best-F1 selection. |
| XGBoost / §6.4.7 | 161–170 | First 10% of the normal prefix, then 60/20/20. Cell 162 uses stride-one 755×9 windows; cell 163 flattens them, predicts next nine values with 100 trees/max depth three/seed 42. Raw residual sum and majority targets yield `n−1509` outputs. |
| One-class SVM / §6.4.8 | 171–177 | First 10% of normal data, then 60/20/20. The defined window helper is not called: the RBF SVM uses individual standardized nine-feature rows. It makes `n` point decisions, not temporal-window decisions. |

These methods do not receive identical amounts of normal training data, and their target coverage differs. For example, the statistical template uses nearly the entire normal prefix, neural methods train on its first 60%, and PLS/XGBoost/SVM train on approximately its first 6%. Their published scores cannot establish a controlled ranking for our protocol merely because they use the same dataset name.

Table 14 itself reports the highest F1 for CNN-AE, and the lowest inference latency for XGBoost. CASPER's CNN is presented as a trade-off. Do not restate the paper as proving its CNN best on every metric.

## Discrepancies and qualifications to preserve

These are document/source findings, not a claim that the paper or all its results are false.

| Issue | Direct evidence | Consequence |
|---|---|---|
| Statistical baseline records disagree | Figure 10(c), p. 22: TN 398, FP 1, FN 106, TP 347, total 852. Arithmetic gives accuracy 87.44% and F1 86.64%. Its caption instead gives 84.6%/83.4%; Table 14 gives 95.76%/95.71%; cell 69 operates on 898 windows. | These figure/caption/table/source configurations are not reconciled. The arithmetic is a check of reported numbers, not a new model result. |
| PLS configuration/terminology | §6.4.4 describes reducing predictors to seven; cell 73 sets two PLS components on flattened nine-channel histories. | Resolve what the prose's predictor count corresponds to. Do not describe this as seven input channels versus two input channels. |
| XGBoost window description | §6.4.7 describes a window-length shift/input-target window construction; cells 162–163 build stride-one windows and next-point targets. | Faithful paper-method and available-code interpretations differ; freeze and disclose the chosen version. |
| Algorithm 1 length | Output declaration is `n−1509`; after aggregating residuals into `S`, line 14 iterates only through `|S|−W+1`, subtracting another window offset if `W=755`. Cell 97 thresholds every aggregated score. | Pseudocode is internally ambiguous/inconsistent with the declared length and available code; do not translate it literally without an explicit correction. |
| Dense-AE target mismatch | Cells 120/122 train against raw-unit targets; cell 125 evaluates against standardized `X_test_windows`, whereas cell 130 scores raw reconstruction error. | Its normal-test evaluation target is inconsistent with its stated training/scoring targets. The declared final ReLU also cannot output negative raw values, visible in Figure 6. This is a constraint of the declared architecture; the loaded checkpoint's architecture/provenance has not been verified. |
| Timing is not uniformly defined | CNN cell 88 divides elapsed batch prediction time by `number_of_batches×1024`, including a possibly incomplete final batch. Template cell 67 measures RMSE per disjoint window; AE branches time chunks or half-data inference; preprocessing/aggregation are outside several timers. | Use actual processed counts and a common hardware, batching, warmup and end-to-end scope in any later timing comparison. No speed claim transfers to our machine. |
| Incomplete selection record | Figure 11 mentions a final cross-validation chain; the notebook exposes a fixed chronological split and selected settings, not a complete fold/search log. Separate checkpoint loads break an automatic training-history-to-result association. | Do not invent folds, best-epoch rules, dependency locks or provenance for saved outputs. |
| Previously recorded data/annotation issues | Table 11 differs from the received numeric IMU count by 750; a final manual interval endpoint differs by six rows between prose and code; median filtering precedes partitioning; independent IMU timestamps are absent. | Retain the existing identity/lineage blockers. The matching Figure 11 totals do not resolve them. |
| Metric terminology/output errors | §6.4.3 repeats the FP description for FN. Cell 177 computes `f1` but prints the imported `f1_score` object. | Use independently checked metric definitions and explicit numerical outputs; do not infer that every stored metric was computed incorrectly. |

## What a fair follow-up must establish

The paper's own limitations include manual synchronization, a particular repetitive task, point anomalies potentially hidden by windowing, and future online/edge work. Additional limits of the available record are a single task/recording, no demonstrated independent calibration, incomplete code/model provenance, and no uncertainty estimates across independent runs or operating conditions. Detecting the smallest included speed change does not establish sensitivity to all subtle attacks or other robots.

Before executing a comparison, follow the [proposed common protocol](../../docs/COMPARISON_PROTOCOL.md): freeze exact input files and eligible channels; settle a defensible label version and availability-time convention; partition before fitting/selecting preprocessing; calibrate without held-out attacks; equalize information access; and state how point, reconstruction-window and residual-window outputs map to the same assessment unit. Resetting filtering, changing thresholds or changing target rules must be reported as a modified protocol.

The first human reading session can now use this checklist:

- [ ] Explain the trusted sensor path and the difference between a changed motion, an anomaly label and evidence of an actual cyberattack.
- [ ] Trace one raw IMU row through median filtering, a 755-row prediction window, residual aggregation and its target label, using the lineage record.
- [ ] Identify why Figure 11 matches four convolutional layers, and why its trained predictor is not itself a process digital twin.
- [ ] Explain why cell 97 cannot calibrate an operational detector and why a high published F1 is not our reproduced result.
- [ ] Compare the template, CNN, AE and SVM output units and normal-data access before selecting a shared protocol.
- [ ] Decide which unresolved source questions are necessary for faithful reproduction and which require a disclosed independent implementation.

Reading completion for a person should be recorded only after that person reviews the sources. No title, new mechanism, novelty claim or execution readiness is finalized by these notes.
