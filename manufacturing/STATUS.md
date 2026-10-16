# Manufacturing status

As of **16 October 2026**. Owner: **Haiqa Mushtaq**. Manufacturing is active while water waits for iTrust. The user authorized teaching, acquisition/identity and paper audits, research/evaluation definitions, then loader/isolation/metric implementation with synthetic tests and a bounded pilot specification.

| Item | Actual state |
|---|---|
| Stage | Loader/isolation/metric primitives implemented; 83 synthetic tests pass; bounded pilot specified but model/runner/fitting and comparator admission remain pending |
| Recommended setting | Industrial robotic arms; original CASPER pick-and-place collection |
| Title / question | State synchronization versus preservation of nominal cycle-progression evidence; title and twin/novelty claims remain provisional |
| Selected threat / inputs | Command/application speed manipulation with truthful monitoring telemetry/time assumed; twelve right-arm joint-position/velocity channels plus relative-time context |
| Annotation / splits | Recorded schedule flags, eight events; exact chronological blocks, common eligible support and continuous final replay defined |
| Calibration / metrics | Threshold-only nearest-rank 99% with strict exceedance; unadjusted counts/P/R/F1, normal burden, AP, event/delay, coverage and cost rules specified |
| Final-test protection | Both final slices protected; development wrapper blocks calibration/final opens. Public raw bytes remain accessible; no OS enforcement or completed artifact freeze |
| Repeats | Final stochastic seeds 17, 42, 2026; deterministic controls once; all failures retained, no best-seed selection |
| Learning set | CASPER 2024, TWINE 2026, CatBoost on CASPER 2026; source/admission notes under `baselines/` |
| Shared-data evidence | Our v3 bytes/hashes fixed; equivalent bytes behind every published run, common annotations/inputs and run correspondence remain unresolved |
| Public data access | Original CASPER v3 acquired publicly under provider CC BY-SA 4.0 terms; no institutional approval required |
| Local benchmark data | **Archive + five original members**, about 10.72 GB combined; fresh six-file hash matches, structural checks and PCAPNG header/timestamp audit complete |
| Manuscripts and code | CASPER corrected VOR V1.1 collected; TWINE and CatBoost full-text access unresolved. Pinned pack: 67 source/doc/config/author-result artifacts plus three tree receipts; no upstream code executed |
| Paper-to-code milestone | CASPER main text studied with figure/cell mappings; TWINE and CatBoost abstract/record/code studies have separate reading notes. Full-paper reading remains **1 of 3**, with no reproduced run |
| Step 0 comprehension | Lesson and synthetic worked example prepared; researcher worksheet unanswered, understanding unassessed |
| First executable study | Proposed deterministic velocity-deviation pilot: 46,944 eligible fit-prefix rows and 18,472 development-prefix scores; model/supervisor not implemented or run |
| Other open routes | MIT synthetic machining/assembly; CMU TEP manipulations; no verified recent three-paper intersection |
| Environment / detector implementation / training | Manufacturing-local Python 3.15.0 venv; stdlib loader/contract/replay/metrics and 83 synthetic tests. No detector model or training |
| Benchmark results / novelty evidence | None |

## Important limits

- Original CASPER and CASPER 1 & 2 remain distinct provider listings. Only original v3 was acquired. `nicla_fixed.csv` is numerically equivalent to raw Nicla after six startup records under binary64 parsing; it provides no extra clock/labels. Its authoring history remains undocumented.
- The selected controller route changes the earlier external-IMU-first main-study proposal. It has a supported physical-state/time representation but a narrower threat: command changes with truthful telemetry. The collection does not prove an authenticated or independently protected monitor. Full controller/collector compromise, legitimate-change handling and fault/attack attribution remain outside demonstrated scope.
- Each arm has 1,762,650 rows and eight positive label runs. Full nested parsing validates 66 scalars per row including time/label, with no numeric/shape errors; 64 observables are possible before feature selection. IMU has 1,751,682 numeric rows without timestamps/labels. These are dataset facts, not detector results or independent runs.
- Matched author capture code and official UR documentation now support boot-relative seconds for controller timestamps. The original executing revision, wall-clock anchor and cross-device synchronization remain unproven. IMU labels are retrospective/manual; controller flags reflect a schedule rather than independently measured impact onset.
- Fresh boundary review preserves exact serialized times around all eight flag runs. The later matched source writes the same flag to both arms while changing only the right-arm speed; left-file flags are not per-arm physical-impact truth. `arms.pcap` is PCAPNG: 14,582,826 timestamped packet blocks, nanosecond resolution, two duplicate and 2,579 backward adjacent deltas in file order. Capture epoch times do not synchronize controller or IMU clocks; valid framing does not prove lossless capture.
- Static annotation lineage resolves a 916-row filtered-endpoint offset and 1,529-row complete CNN-score support. Derived class totals match the paper's confusion-matrix denominator; this is not reproduced predictions. Table 11 lists 750 fewer IMU rows than received and remains unresolved. The architecture figure agrees with four convolution layers in the code.
- CASPER's inspected threshold selection uses anomaly labels. TWINE uses random row splits and has inconsistent feature/model/demo paths. CatBoost's available script creates synthetic outlier labels, stacks incompatible sensor features as rows and scales before splitting. No such workflow is approved as our evaluation.
- Deeper paper/code reading also identifies unequal CASPER comparator training/output units and unresolved statistical-baseline records; TWINE's evaluated and SHAP-explained models differ; CatBoost author tables mislabel test accuracy as validation and mix timing units. These are documented source/provenance findings, not reproduced performance or blanket invalidation of the papers.
- CASPER observes external IMU; TWINE uses controller telemetry; supervised and normal-only training differ. Common collection does not automatically mean fair information access or a common detection task.
- Periodic alignment, task segmentation and prediction residuals already appear in close prior work. The specific synchronization/progression experiment is testable, but its novelty and benefit are unverified. Simple velocity and periodic-template controls are mandatory; three admitted recent common-protocol baselines remain unresolved.
- TWINE and CatBoost full manuscripts remain inaccessible in this audit. Available code is not established as the exact code behind every published result. Original CASPER and CatBoost code licenses are unresolved; TWINE MIT license is verified.
- Motion deviations and environmental faults do not by themselves establish malicious intent. Digital-twin labels/cloud state storage do not prove predictive physical fidelity or novelty. The CASPER+ programme already describes closely related research ideas.

## Next bounded action

The [software validation report](docs/SOFTWARE_VALIDATION.md) completes this bounded implementation milestone: 83 synthetic tests passed, including chronology/isolation, coverage and exact time metrics. No real CASPER observations were opened. The [pilot plan](docs/BOUNDED_PILOT_PLAN.md) and [configuration](configs/casper_right_arm_pilot_v0.1.json) specify one deterministic velocity control and proposed resource bounds. Next: implement and synthetically test that control and its bounded supervisor, resolve the concrete run command/provenance, then undertake a separately scoped normal-only pilot. Calibration/final access stays closed; the [freeze record](experiments/FINAL_TEST_FREEZE_RECORD.json) remains pending. CASPER, TWINE and CatBoost still require separate fair-comparator admission. **No real-data fitting, calibrated threshold, final result or Azure/Factory I/O deployment exists.**

The three-paper list is for critical study; final comparative admission remains pending. If a clean shared-data comparison requires independent implementations or different features, record those changes before execution. No change has been made to water or grid research status.

## Evidence and persistent records

- [Software validation](docs/SOFTWARE_VALIDATION.md), [actual test report](experiments/SOFTWARE_TEST_REPORT.json), [environment](docs/ENVIRONMENT.md), [bounded pilot](docs/BOUNDED_PILOT_PLAN.md), [pilot JSON](configs/casper_right_arm_pilot_v0.1.json).
- [Evaluation protocol](docs/EVALUATION_PROTOCOL.md), [metric formulas](docs/METRIC_DEFINITIONS.md), [final-test protection](docs/FINAL_TEST_PROTECTION.md), [evaluation JSON](configs/casper_right_arm_evaluation_v0.1.json), [pending freeze record](experiments/FINAL_TEST_FREEZE_RECORD.json).
- [Evaluation design review and dispositions](docs/EVALUATION_PROTOCOL_REVIEW.md); metadata/arithmetic checks passed, executable validation remains pending.
- [Admission rules](docs/BASELINE_SELECTION_CRITERIA.md), [selection decision](docs/BASELINE_SELECTION_REPORT.md), [literature register](docs/LITERATURE_EVIDENCE.md).
- [Received-file identity](docs/CASPER_DATASET_IDENTITY.md), [receipt manifest](datasets/manifests/casper_v3_receipt.json), [manuscript/code collection](docs/MANUSCRIPT_COLLECTION_AUDIT.md), [proposed protocol](docs/COMPARISON_PROTOCOL.md).
- [Current release/hash/clock register](docs/DATASET_IDENTITY_REGISTER.md), [consolidated manifest](datasets/manifests/casper_v3_identity.json), [checksum file](datasets/manifests/casper_v3.sha256), [label/time review](docs/CASPER_LABEL_TIME_AUDIT.md), [paper-specific dataset correspondence](docs/BASELINE_DATASET_CORRESPONDENCE.md).
- [Selected question and threat model](docs/RESEARCH_QUESTION_AND_THREAT_MODEL.md), [annotation/features/splits](docs/ANNOTATION_FEATURE_SPLIT_CONTRACT.md), [contract JSON](configs/casper_right_arm_contract_v0.1.json), [design critique](docs/RQ_CONTRACT_REVIEW.md).
- [Complete sensor schema](docs/CASPER_SENSOR_SCHEMA.md), [annotation and score lineage](docs/CASPER_ANNOTATION_LINEAGE.md), [code study](docs/BASELINE_CODE_STUDY.md), [pinned source/result pack](baselines/SOURCE_PACK_MANIFEST.json).
- [Paper-to-code reading coverage](docs/PAPER_CODE_TRACEABILITY.md), [CASPER notes](baselines/casper/READING_NOTES.md), [TWINE notes](baselines/twine/READING_NOTES.md), [CatBoost notes](baselines/catboost/READING_NOTES.md).
- [Open data](docs/literature/OPEN_DATASET_SCREEN_2026-10-16.md), [comparator manuscripts/code](docs/literature/COMPARATOR_SCREEN_2026-10-16.md), [twin methods](docs/literature/TWIN_METHOD_SCREEN_2026-10-16.md).
- [Access/receipt checklist](docs/DATASET_ACCESS_CHECKLIST.md), [proposed reproduction plan](docs/REPRODUCTION_PLAN.md), [work log](docs/WORK_LOG.md).
- [Shared publication standards](../docs/PUBLICATION_STANDARDS.md) and [repeatable playbook](../docs/RESEARCH_PLAYBOOK.md) remain in force. No title, venue, authorship or publication outcome is finalized.
