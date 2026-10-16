# Start here: our manufacturing data and papers

Study record: 16 October 2026. Owner: Haiqa Mushtaq. We have enough material to study the original robotic-arm experiment seriously. We do **not** yet have three methods ready for a fair benchmark. No model has been trained and no published result has been reproduced.

For the subsequent collect/read/connect milestone, use the [paper-to-code map and individual reading notes](PAPER_CODE_TRACEABILITY.md). They expand the main-text study and distinguish what the paper says, what the code does, and which published-result links remain unresolved.

## What is on this computer

The original [CASPER provider collection](https://www.kaggle.com/datasets/hkayan/industrial-robotic-arm-anomaly-detection), version 3, is already received. It contains an approximately 24-hour physical pick-and-place recording with planned changes to joint velocity. The unchanged archive plus extracted files occupy about **10.72 GB**. The dataset's provider license is CC BY-SA 4.0. Exact source/version, bytes and hashes are in the [receipt](../datasets/manifests/casper_v3_receipt.json) and [identity report](CASPER_DATASET_IDENTITY.md).

All paths in this table are relative to `manufacturing/`. Payloads are local and excluded from Git.

| Material | Local location | What to use it for |
|---|---|---|
| Original archive | `datasets/raw/casper/v3/original_casper_v3.zip` | Preserve the received release; do not edit or repeatedly download it. |
| Two controller recordings | `datasets/raw/casper/v3/original/dataset/left_arm.csv` and `right_arm.csv` | Learn joint, tool, status, native-time and scheduled anomaly fields. They are two devices in one setup, not automatically two independent experiments. |
| External motion sensor | `datasets/raw/casper/v3/original/dataset/nicla.csv` | CASPER's detector observes nine accelerometer/gyroscope/magnetometer channels. There are no embedded labels or timestamps. |
| Alternate IMU serialization | `datasets/raw/casper/v3/original/nicla_fixed.csv` | Adds channel headers and changes numeric text. Our full comparison found the same numeric sequence after startup removal; it is not a new labelled or synchronized dataset. |
| Network capture | `datasets/raw/casper/v3/original/dataset/arms.pcap` | Preserved and integrity-checked. Packet contents have not been decoded or replayed; the studied CASPER IMU detector does not require them. |
| Corrected CASPER manuscript | `baselines/casper/artifacts/casper_corrected_vor_v1.1.pdf` | Read the experiment, label construction, architecture and evaluation directly. |
| Pinned author source/docs | Each method's `baselines/<method>/artifacts/source_snapshot/` | Read matched source revisions without running them. The [source-pack manifest](../baselines/SOURCE_PACK_MANIFEST.json) gives every included path and hash. |
| Author-reported graphs/tables | Listed separately in the same source-pack manifest | Study what authors report. These files are **unreplicated author artifacts**, never our experimental outputs. |

The newer “CASPER 1 & 2” listing is a separate collection. It has not been silently substituted or added to this experiment. Water datasets and smart-grid materials remain in their independent projects.

## What these recordings tell us

Each controller CSV has **1,762,650 rows** and twenty top-level fields. Several fields contain lists, so one CSV cell is not necessarily one measurement. Full nested parsing of both files validates the field shapes and yields 66 scalar values per row including time and label; there are **64 possible observables** before scientific feature selection. This is not a decision to give a model every field. The [sensor schema study](CASPER_SENSOR_SCHEMA.md) separates established field mappings from uncertain acquisition provenance.

Each controller has eight positive label runs. The raw IMU has **1,751,682 numeric rows**, after six startup records, and does not carry those labels. The code reconstructs IMU labels by manually locating changes in a plotted sensor channel. Our [annotation study](CASPER_ANNOTATION_LINEAGE.md) explains every coordinate change and what remains uncertain.

This distinction matters: a scheduled command change, a measurable physical effect, and a malicious action are different events. A classifier trained against a schedule flag learns to predict that annotation. It has not necessarily learned to identify an attacker or distinguish an authorized change with the same physical effect.

The files also do not provide verified production-cycle identifiers, a catalogue of authorized changeovers, or independent attack-versus-fault examples. Consequently, the current broad working question about legitimate production changes and malicious sequences is **not yet demonstrated to be testable with this corpus alone**. Use CASPER first for a clearly limited motion-deviation study; broader claims need further evidence or a separately justified dataset.

## What each paper contributes to our learning

| Paper | Method to understand | Material/readiness |
|---|---|---|
| **CASPER, 2024** | Learn normal IMU motion; predict the next observation; measure prediction error; aggregate errors; threshold the score. | Full corrected paper, author notebook and supporting materials available. Conditional first method to reproduce after annotation, code terms and protocol are settled. |
| **TWINE, 2026** | Learn how controller classification, explanations and a cloud twin representation are connected. Check what the twin actually predicts or estimates. | Author source is available under MIT. The institutional record identifies a full accepted manuscript, but retrieval remains unsuccessful. Code alone cannot establish every paper claim. |
| **CatBoost on CASPER, 2026** | Learn supervised classification and examine whether data preparation preserves a meaningful task. | Author script and reported results available; complete manuscript not obtained. Available code has synthetic IMU labels, incompatible modality stacking and pre-split scaling. These issues block direct execution as our benchmark. |

See the [code study](BASELINE_CODE_STUDY.md) for functions/cells, dependencies, missing assets and licenses, and the [manuscript audit](MANUSCRIPT_COLLECTION_AUDIT.md) for primary-source identities and access failures. The absence of an accessible manuscript is an access limitation, not evidence that a paper is fake.

## Follow one observation through CASPER

Read this as a description of the upstream method, not a run we performed:

1. The robot moves. Its external sensor produces nine measurements.
2. Startup records and an initial idle section are removed. A trailing median reduces short-term fluctuation.
3. A neural model uses 755 filtered observations to predict the next nine measurements.
4. When the next observation arrives, the method calculates a prediction error. This error is an anomaly **score**, not yet an alarm and not proof of an attack.
5. It sums 755 successive errors, then compares the sum with a threshold.
6. Evaluation compares the decisions with retrospectively assigned labels, using the paper's specified window-label convention.

The complete upstream score depends on **1,529 raw numeric observations**, including filtering and aggregation. This explains why a 755-step neural input alone does not describe the method's full history or detection latency. The IMU lacks observed time, so we cannot honestly call that history a verified number of seconds.

Our static deductions give the same total and positive/negative label counts as the paper's Figure 11 confusion matrix. Visual inspection also confirms that its four-convolution architecture matches the notebook. These resolve useful consistency questions. Table 11 still lists 750 fewer IMU rows than received; checkpoint identity, exact published bytes and predictive performance remain unverified.

## Why we cannot press “run all” yet

CASPER uses normal-only learning with external IMU observations. TWINE's inspected classifier uses labelled controller observations. The CatBoost script mixes data/labels in ways that require redesign before a clean comparison. Different channels and different access to attack labels can explain performance differences independently of model quality.

The [comparison protocol](COMPARISON_PROTOCOL.md) therefore separates a normal-only IMU group from a supervised controller group. A third method must join the same information-access group, or be described as a different experiment. Moving an algorithm onto new features or a new learning objective is a declared reimplementation, not an unchanged reproduction.

The upstream CASPER code selects a threshold using evaluated attack labels. We will instead freeze the configuration on permitted development data and calibrate the operating threshold on a separate normal block. Raw files remain unchanged; any future transformed arrays receive their own source/operation manifests. Reported author scores remain separate from our future runs.

## Study order and the next technical step

1. Read the [Step 0 lesson](RESEARCH_BASICS_LESSON.md). Be able to explain prediction, score, threshold, label and leakage in your own words. The worksheet remains unanswered; no understanding is assumed.
2. Use this guide and the sensor schema to explain what each file measures, which data a detector can see, and what its target label means.
3. Read CASPER §6.3–6.4 alongside the annotation study and pinned notebook cells. Start with data preparation, then the CNN, then scoring and threshold selection. Do not execute all cells.
4. Use the code study to examine TWINE and CatBoost as critical comparisons. Keep their missing manuscript and published-run correspondence questions visible.
5. **Next bounded technical milestone:** propose a versioned external-IMU annotation/feature/split contract, with uncertainty, warmup and exclusions recorded. Establish which event and delay claims are supportable before training. If annotation timing remains unresolved, explicitly limit the evaluation or obtain further evidence; do not invent timestamps.

After that contract passes review, we can create an isolated environment and small loader/split/metric checks. A bounded pilot would follow those checks under its own recorded configuration. None of those execution steps has happened in this study.
