# CASPER comparison protocol — before training

**Current routing, 17 October 2026:** [comparator admission](COMPARATOR_ADMISSION.md) now records the original papers' dispositions and an explicitly transferred ModernTCN candidate. The frozen Group D feature/evaluation contracts remain unchanged. The ordinary velocity control has completed [one bounded pilot](PILOT_REPORT.md); this earlier comparison-plan snapshot is not a statement that no fitting has ever occurred.

## Material Passport

- Origin skill: academic-research-suite, experiment-agent planning guidance; project rules take precedence.
- Origin date: 2026-10-16.
- Version label: `manufacturing_casper_protocol_v0.2` — selected right-arm track added; earlier IMU/supervised proposals retained separately.
- Verification status: **PROPOSED / NOT EXECUTED**. This is an engineering comparison contract, not a registered study, experiment result or validated statistical design.
- Scope: offline evaluation of robotic-motion deviation detection using original CASPER. No training, cloud deployment or attack execution authorized by this document.

## What is settled and what is still blocked

The user authorized collection, exact identification, manuscript follow-up and a fair protocol before training. The rules below are fixed for this planning stage without looking at detector performance. Exact partitions/features/event annotations must be recorded in a machine-readable manifest before execution. If the data cannot support them, change the plan transparently **before** inspecting final model scores; do not fill missing labels or independent runs by assumption.

Use [CASPER_DATASET_IDENTITY.md](CASPER_DATASET_IDENTITY.md) for received-byte evidence and [MANUSCRIPT_COLLECTION_AUDIT.md](MANUSCRIPT_COLLECTION_AUDIT.md) for current paper/code coverage. Those documents, not an earlier access-only record, govern the latest receipt status. Dataset identity does not establish trustworthy time alignment or attack ground truth.

**Current selection:** the user subsequently requested a feasible question/threat model and exact annotation/features/splits. The [decision](RESEARCH_QUESTION_AND_THREAT_MODEL.md) selects **Group D** below; its [versioned contract](ANNOTATION_FEATURE_SPLIT_CONTRACT.md) supplies exact ranges and supersedes generic split/primary-metric proposals in this document **for Group D only**. It does not silently alter or complete Group A/B. Read [the latest identity register](DATASET_IDENTITY_REGISTER.md) for six-file integrity and clock evidence. No final architecture, score implementation or run is approved merely by this specification.

The later [sensor-schema audit](CASPER_SENSOR_SCHEMA.md) validates all nested controller fields and supports boot-relative seconds through a matched capture source and official definitions; original execution provenance and cross-device timing remain unresolved. The [annotation lineage study](CASPER_ANNOTATION_LINEAGE.md) derives **1,529 raw observations of support** for the inspected CASPER CNN score (median + prediction + residual aggregation). This is an audit of upstream behavior, not a newly frozen window choice or a reason to claim seconds for untimestamped IMU data.

Scientific target: detect documented changes to robot motion under an explicit observation/trust model. A correct alarm does not prove malicious intent when an identical change could be authorized. No claim of general APT detection, attack attribution, unseen-robot generalization or live protection follows from these recordings.

**Later Group D evaluation supplement:** [EVALUATION_PROTOCOL.md](EVALUATION_PROTOCOL.md), [metric definitions](METRIC_DEFINITIONS.md) and [final protection](FINAL_TEST_PROTECTION.md) now fix support, calibration, repeats and reporting. They resolve Group D evaluation details, including complete-score admission, and preserve the reviewed data-contract bytes. No change to Group A/B is implied; their earlier generic proposals do not override the selected track.

## 1. Comparison groups: do not pool unequal information

| Group | Permitted observations/training | Candidates and claim |
|---|---|---|
| **A: external-sensor, normal-only detection** | Original IMU signals available by decision time; prediction formed before the measurement it predicts, then compared with that measurement. Model/configuration development uses designated normal data. Attack labels remain evaluator-only. | CASPER 1D-CNN is the conditional first method. A later twin or simple predictor can join only with the same channels/history and normal-only access. This group tests motion deviations detectable from an external sensor. |
| **B: controller-telemetry, supervised classification** | Same allowlisted controller features and labelled development episodes for every method; disjoint final episodes. Normal calibration reserved separately. | TWINE's random forest and a declared independent CatBoost implementation are candidates after full specifications and splits are resolved. Neither is a normal-only comparator as originally described. This group tests classification with controller telemetry and attack-labelled training. |
| **C: added context/sensor fusion, future work only** | Explicit additional trusted commands, phase estimates or external references with availability times documented. | Separate information-access experiment, with controls receiving the same extra evidence. Not authorized implementation and not a current novelty claim. |
| **D: right-arm controller telemetry, normal-only — selected main feasibility track** | Six actual joint positions, six actual joint velocities and relative elapsed time for propagation/gap handling; no labels or absolute-time/index features. Reference/model fitting and selection use designated initial scheduled-normal partitions. | Command-path speed manipulation with truthful monitoring telemetry/time assumed. Simple velocity/template/AR controls and a candidate synchronized motion twin; controller-input CNN would be a modified implementation. No claim of resistance to telemetry forgery or faithful three-paper reproduction. |

**There is no approved single three-way ranking of the published implementations.** Same CASPER filenames do not equal same input information, labels or supervision. An algorithm ported to different channels or a different learning objective is a modified method/reimplementation. Do not present a random-forest regressor as a faithful reproduction of TWINE's classifier merely to place it in Group A.

Group D uses the recorded right-arm schedule flags, not copied IMU/manual labels. The primary fitting/development/calibration prefix ends at row 864003; held-out normal begins there, followed continuously by all changed-speed/recovery records. See the contract for exact half-open boundaries, gap reset and warmup policy. Event labels never trigger state resets. Point-level schedule agreement and held-out-normal burden/coverage are reported together; eight long event hit counts alone cannot establish benefit. Model-specific normal-only initialization, transforms and score definitions remain to be specified before any execution.

## 2. Source and label contract

Use original CASPER provider v3 and retain its CC BY-SA 4.0 record, canonical source, archive/member checksums and unchanged originals. Do not silently merge the newer CASPER 1 & 2 listing or substitute `nicla_fixed.csv`. Record every local derivative's input hashes and transformation. The receipt audit found every parsed numeric row of `nicla_fixed.csv` equal to original Nicla after its six startup records; this is measured numeric equivalence, not byte identity, time alignment or label restoration. Use the original file as the reference and preserve that documented relationship. Provider generation history remains unknown.

The original paper describes scheduled controller-velocity changes. Its external IMU lacks a shared aligned clock/rate; the inspected notebook drops initial rows and manually labels eight intervals using signal plots. Nominal 20 Hz is not proof of exactly 20 samples per second. Therefore:

1. Identify original time fields, their units and resets, actual gaps and sampling behavior. Do not generate wall-clock time from `row_index / 20` and describe it as observed time.
2. Treat `Anomaly State` as a candidate target only after reconciling values, transitions and provider/paper semantics. Remove it and all direct derivatives from model inputs.
3. Keep a separate, versioned annotation record: source event, controller start/end, mapping to IMU indices, uncertainty and rationale. Manual upstream indices may be retained as **retrospective paper-derived annotations**, not as independently verified physical timestamps.
4. Mapping must be chosen without detector scores. An annotation procedure informed by observed motion is not independent of that signal; disclose the circularity risk and annotation uncertainty. Merely hiding the labels from the model does not cure an invalid target.
5. Do not generate cyberattack labels from an acceleration percentile, join modalities without time correspondence, pad features and stack them as equivalent rows, or silently relabel faults as attacks.

If exact IMU timing cannot be established, report index/window-level evaluation under a stated annotation convention only; **seconds-based delay and precise cross-modal claims remain unavailable**. Do not infer malicious intent from velocity magnitude alone. If the available annotation cannot support a meaningful holdout, block that comparison rather than invent events.

## 3. Partition before filtering/windowing

### Group A proposed partition rule

Identify the first documented contiguous clean operating span before the manipulated-motion segment, using source chronology and reconciled annotations, not score plots. Partition its ordered time/sample range into **50% training, 15% development, 15% normal calibration, 20% held-out normal evaluation**. These are proposed fractions chosen before training, not the original paper's split and not measured file boundaries.

Assign whole documented cycles/runs where available; snap boundaries forward to the next complete cycle and record actual counts. If cycle identifiers cannot be recovered independently, use contiguous chronological blocks, purge boundary context and explicitly limit independence/generalization claims. Repeated measurements, replays and duplicates must not cross partitions. A separate robot or independent collection would support a stronger claim than adjacent periods from one run.

The manipulated-motion recording remains held out. Recovery/startup/unknown intervals must be represented explicitly and reported as exclusions, never quietly added to normal calibration. Report all excluded duration/rows and all events affected by exclusions. Do not choose which attacks count after examining detector outputs.

Each partition starts with fresh state. Build trailing windows and causal preprocessing **within** that partition. Exclude initial warmup from point scoring, count it in coverage, and record every affected event. Derive the **effective combined raw-input history** of each full pipeline, including consecutive filters, prediction windows and residual aggregation; use the maximum combined history across compared methods for boundary purging. Taking only the largest individual window can be too short. The manifest must specify exact rows and support intervals. No centered smoothing or interpolation from future values in a claimed online replay.

### Group B gate

The corpus must support distinct chronological development and final attack episodes, sufficient normal context, and a separate normal calibration block. Every supervised method receives the same training labels and feature set. Group attack episodes and any duplicated trajectories together; never split a single event's neighboring rows across train/test.

**No Group B split is frozen yet.** The receipt/annotation audit must first identify admissible episodes and time boundaries. Record the exact episode assignment and intended known-pattern versus unseen-pattern claim before fitting any method. If chronology and episode coverage do not permit a valid labelled-development split, Group B stays exploratory or is dropped; random stratified rows are not a substitute. This unresolved gate prevents declaring the full three-paper comparison ready.

## 4. Allowed inputs and preprocessing

Maintain a per-group feature allowlist with source columns, units, transformations, trust assumptions and availability time. Exclude target labels, filenames encoding the target, anomaly-indicator derivatives, future summaries and signals produced only after the alarm time. Validate vector parsing and physical meaning before flattening controller fields.

Fit scaling, imputation parameters and feature selection on the designated training partition only. Apply them unchanged to development/calibration/test. Causal forward filling, if selected, must have a maximum gap and must not cross partitions/resets. Missing/invalid input produces an explicit unscored/uncertain state, not an invented normal observation. Specify whether out-of-range values are retained or clipped before testing.

Audit original rolling-median, period/window estimation and alignment paths before copying them. Derive any period/window choice only from allowed training/development observations. The CASPER notebook can load a pretrained checkpoint after a training cell; **do not accept that checkpoint without its training-data and model-selection provenance**. No untrusted pickle/model deserialization is part of this audit.

## 5. Model selection and alarm calibration

For Group A, select configurations and checkpoints using normal-development prediction loss or another predeclared normal-only objective. Do not use attack F1, test losses or test visualization to select settings. A finite candidate grid and selection/tie rules must be saved before a pilot; no hidden search over final attack outcomes. For Group B, attack labels may be used only in its recorded training and validation partitions, equally across methods; final-test labels remain evaluator-only, and alarm calibration uses its separate normal block.

After model selection, freeze the model and compute scores on the independent normal calibration block. Proposed initial operating rule:

```text
Score orientation: larger = more anomalous.
Calibration target: 1% normal point exceedance (research operating point).
Threshold: nearest-rank empirical 99th percentile of eligible normal-calibration scores.
Alarm: score > threshold; equality does not alarm.
```

Document finite-sample rank, ties, exclusions and score orientation. This controls only empirical calibration exceedance under this rule; it does not guarantee 1% future false alarms, independent samples or acceptable industrial alarm burden. Report actual held-out-normal behavior. Each method gets its own calibrated threshold under the same budget, not the same numeric threshold on incompatible score scales.

Primary point evaluation uses raw threshold decisions, with no smoothing chosen after test inspection. For reporting alarm episodes, merge only adjacent eligible positive decisions within one continuous recording/partition. An unscored sample, declared acquisition gap, clock reset or recording/partition boundary breaks contiguity and is separately marked unknown; never bridge it as if normal or continuously alarming. Define the acquisition-gap tolerance from verified sampling metadata before scoring. Do not invent extra persistence or cooldown rules after seeing results. Additional operating points, if needed, must be declared before final scoring and reported together without selecting a favorable one afterwards.

Future adaptive methods must score before updating, expose only causal information and use no true test labels. State updates, parameter learning, residual calibration and threshold adaptation must each have their own declared policy. No adaptive method is currently implemented or selected.

## 6. Score alignment and metrics

Associate every score with the last observation actually used and an explicit support interval. Use the same target convention within a group; endpoint labels are the proposed main point target. The upstream majority-window label convention is a separate reproduction diagnostic and must not be silently mixed into main results. No point adjustment that retroactively marks an entire attack as detected.

Report score coverage for each method, plus a predeclared common eligible interval for point-wise comparison. Unscored points remain visible. An event with no eligible alarm is a miss in an event analysis rather than being silently removed; events wholly outside the valid dataset scope must be separately enumerated with reasons.

Primary comparison, where annotations support it: **event recall at the independently calibrated operating point**, accompanied by observed false alarm episodes per verified operating hour and missed-event count. If event/timing labels remain uncertain, this primary analysis is **blocked**, not silently replaced by a different headline metric.

Supporting outputs: unadjusted point precision/recall/F1, average precision with score orientation specified, normal point exceedance, coverage, per-event detections and first-alarm delay. Delay in seconds requires verified time correspondence; otherwise use labelled sample/window units and acknowledge the limitation. Report delay for detected events together with all misses. No invented timing resolution, significance or confidence interval based on treating correlated rows as independent experiments.

State zero-denominator behavior before evaluation: undefined precision/recall/event rates are `NA` with their counts, not arbitrary favorable values. False-alarm episode rates need valid normal-duration denominators; sample counts alone do not establish hours. Runtime measurement, when later authorized, must separate preprocessing, model inference and end-to-end detection delay.

## 7. Reproducibility and readiness gates

Use seed **42** for a future bounded feasibility pilot only; a pilot is not a benchmark or evidence of superiority. A later repeated-run study needs predeclared seeds and independent event/run uncertainty, not only repeated initialization on one trace. No environment or training command is created by this protocol; pin dependencies and estimate resources after admission.

Before a pilot, require: receipt hashes; target/clock provenance; feature and split manifests; paper-to-implementation designation; permitted code reuse or an independent implementation; exact configurations/checkpoint rules; calibration specification; tests of schema, chronology, windows, metrics and hidden-label isolation; run command/budget; environment and hardware record. No held-out score may influence these choices.

Future tests should use clearly labelled synthetic fixtures: a clock reset; a missing vector field; non-binary/unknown labels; duplicate run; window crossing a split; a scaler mistakenly fitted on test; a single event with delayed alarm; no-positive/no-alarm cases. These are proposed software checks, not implemented tests or benchmark results.

Success for this stage means an explicit, reviewable plan with unsupported comparisons blocked. It does not mean model accuracy, validated twins, publication readiness or all three papers admitted. Preserve changed-protocol and independent-implementation labels. Paid compute, lengthy training and publishing still require explicit approval.
