# Manufacturing status

As of **16 October 2026**. Owner: **Haiqa Mushtaq**. Manufacturing is active while water waits for iTrust. The user authorized Step 0 teaching, original-CASPER acquisition/identification, manuscript collection and a fair protocol before training.

| Item | Actual state |
|---|---|
| Stage | Exact local release, six-file hashes and label/clock inventory consolidated; source/result pack collected; one full paper available; comparison protocol remains proposed |
| Recommended setting | Industrial robotic arms; original CASPER pick-and-place collection |
| Title / question | Provisional; broad process/sequence question not validated against these data |
| Learning set | CASPER 2024, TWINE 2026, CatBoost on CASPER 2026; source/admission notes under `baselines/` |
| Shared-data evidence | Our v3 bytes/hashes fixed; equivalent bytes behind every published run, common annotations/inputs and run correspondence remain unresolved |
| Public data access | Original CASPER v3 acquired publicly under provider CC BY-SA 4.0 terms; no institutional approval required |
| Local benchmark data | **Archive + five original members**, about 10.72 GB combined; fresh six-file hash matches, structural checks and PCAPNG header/timestamp audit complete |
| Manuscripts and code | CASPER corrected VOR V1.1 collected; TWINE and CatBoost full-text access unresolved. Pinned pack: 67 source/doc/config/author-result artifacts plus three tree receipts; no upstream code executed |
| Paper-to-code milestone | CASPER main text studied with figure/cell mappings; TWINE and CatBoost abstract/record/code studies have separate reading notes. Full-paper reading remains **1 of 3**, with no reproduced run |
| Step 0 comprehension | Lesson and synthetic worked example prepared; researcher worksheet unanswered, understanding unassessed |
| First reproduction | CASPER conditional on code-use terms, label alignment and corrected calibration; none execution-ready |
| Other open routes | MIT synthetic machining/assembly; CMU TEP manipulations; no verified recent three-paper intersection |
| Environment / detector implementation / training | None; six standard-library receipt/schema/index/capture-header audit utilities only |
| Benchmark results / novelty evidence | None |

## Important limits

- Original CASPER and CASPER 1 & 2 remain distinct provider listings. Only original v3 was acquired. `nicla_fixed.csv` is numerically equivalent to raw Nicla after six startup records under binary64 parsing; it provides no extra clock/labels. Its authoring history remains undocumented.
- Each arm has 1,762,650 rows and eight positive label runs. Full nested parsing validates 66 scalars per row including time/label, with no numeric/shape errors; 64 observables are possible before feature selection. IMU has 1,751,682 numeric rows without timestamps/labels. These are dataset facts, not detector results or independent runs.
- Matched author capture code and official UR documentation now support boot-relative seconds for controller timestamps. The original executing revision, wall-clock anchor and cross-device synchronization remain unproven. IMU labels are retrospective/manual; controller flags reflect a schedule rather than independently measured impact onset.
- Fresh boundary review preserves exact serialized times around all eight flag runs. The later matched source writes the same flag to both arms while changing only the right-arm speed; left-file flags are not per-arm physical-impact truth. `arms.pcap` is PCAPNG: 14,582,826 timestamped packet blocks, nanosecond resolution, two duplicate and 2,579 backward adjacent deltas in file order. Capture epoch times do not synchronize controller or IMU clocks; valid framing does not prove lossless capture.
- Static annotation lineage resolves a 916-row filtered-endpoint offset and 1,529-row complete CNN-score support. Derived class totals match the paper's confusion-matrix denominator; this is not reproduced predictions. Table 11 lists 750 fewer IMU rows than received and remains unresolved. The architecture figure agrees with four convolution layers in the code.
- CASPER's inspected threshold selection uses anomaly labels. TWINE uses random row splits and has inconsistent feature/model/demo paths. CatBoost's available script creates synthetic outlier labels, stacks incompatible sensor features as rows and scales before splitting. No such workflow is approved as our evaluation.
- Deeper paper/code reading also identifies unequal CASPER comparator training/output units and unresolved statistical-baseline records; TWINE's evaluated and SHAP-explained models differ; CatBoost author tables mislabel test accuracy as validation and mix timing units. These are documented source/provenance findings, not reproduced performance or blanket invalidation of the papers.
- CASPER observes external IMU; TWINE uses controller telemetry; supervised and normal-only training differ. Common collection does not automatically mean fair information access or a common detection task.
- TWINE and CatBoost full manuscripts remain inaccessible in this audit. Available code is not established as the exact code behind every published result. Original CASPER and CatBoost code licenses are unresolved; TWINE MIT license is verified.
- Motion deviations and environmental faults do not by themselves establish malicious intent. Digital-twin labels/cloud state storage do not prove predictive physical fidelity or novelty. The CASPER+ programme already describes closely related research ideas.

## Next bounded action

The requested identification step is complete for our received bytes; the [identity register](docs/DATASET_IDENTITY_REGISTER.md) distinguishes observed data facts from unresolved scientific-use gates. Next technical milestone: propose a versioned external-IMU annotation/feature/split contract, explicitly retaining onset uncertainty, supported evaluation units and warmup/exclusions. Freeze it only after the [protocol](docs/COMPARISON_PROTOCOL.md) gates pass. The [paper-to-code map](docs/PAPER_CODE_TRACEABILITY.md), [study guide](docs/DATA_AND_BASELINE_STUDY.md), [Step 0 lesson](docs/RESEARCH_BASICS_LESSON.md) and [worksheet](docs/YOUR_STEP_0_NOTES.md) support learning; comprehension remains unassessed. Keep missing manuscripts and unavailable published-run provenance on hold. **Do not start training or an Azure/Factory I/O deployment.**

The three-paper list is for critical study; final comparative admission remains pending. If a clean shared-data comparison requires independent implementations or different features, record those changes before execution. No change has been made to water or grid research status.

## Evidence and persistent records

- [Admission rules](docs/BASELINE_SELECTION_CRITERIA.md), [selection decision](docs/BASELINE_SELECTION_REPORT.md), [literature register](docs/LITERATURE_EVIDENCE.md).
- [Received-file identity](docs/CASPER_DATASET_IDENTITY.md), [receipt manifest](datasets/manifests/casper_v3_receipt.json), [manuscript/code collection](docs/MANUSCRIPT_COLLECTION_AUDIT.md), [proposed protocol](docs/COMPARISON_PROTOCOL.md).
- [Current release/hash/clock register](docs/DATASET_IDENTITY_REGISTER.md), [consolidated manifest](datasets/manifests/casper_v3_identity.json), [checksum file](datasets/manifests/casper_v3.sha256), [label/time review](docs/CASPER_LABEL_TIME_AUDIT.md), [paper-specific dataset correspondence](docs/BASELINE_DATASET_CORRESPONDENCE.md).
- [Complete sensor schema](docs/CASPER_SENSOR_SCHEMA.md), [annotation and score lineage](docs/CASPER_ANNOTATION_LINEAGE.md), [code study](docs/BASELINE_CODE_STUDY.md), [pinned source/result pack](baselines/SOURCE_PACK_MANIFEST.json).
- [Paper-to-code reading coverage](docs/PAPER_CODE_TRACEABILITY.md), [CASPER notes](baselines/casper/READING_NOTES.md), [TWINE notes](baselines/twine/READING_NOTES.md), [CatBoost notes](baselines/catboost/READING_NOTES.md).
- [Open data](docs/literature/OPEN_DATASET_SCREEN_2026-10-16.md), [comparator manuscripts/code](docs/literature/COMPARATOR_SCREEN_2026-10-16.md), [twin methods](docs/literature/TWIN_METHOD_SCREEN_2026-10-16.md).
- [Access/receipt checklist](docs/DATASET_ACCESS_CHECKLIST.md), [proposed reproduction plan](docs/REPRODUCTION_PLAN.md), [work log](docs/WORK_LOG.md).
- [Shared publication standards](../docs/PUBLICATION_STANDARDS.md) and [repeatable playbook](../docs/RESEARCH_PLAYBOOK.md) remain in force. No title, venue, authorship or publication outcome is finalized.
