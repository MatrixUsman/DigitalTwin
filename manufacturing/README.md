# Smart manufacturing research project

Owner: **Haiqa Mushtaq**. Project ID: `manufacturing`. Academic digital-twin cybersecurity research for manufacturing processes; titles and contributions remain provisional.

Start with [PROJECT_BRIEF.md](PROJECT_BRIEF.md), [STATUS.md](STATUS.md), and [AGENTS.md](AGENTS.md), together with the [shared rules](../AGENTS.md). This folder is independent of its siblings. A bounded pilot and a separate full-training normal-only velocity/template/AR study are complete; no attack benchmark result or reproduced paper baseline exists.

| Location | Purpose |
|---|---|
| [docs/PAPER_ROADMAP.md](docs/PAPER_ROADMAP.md) | Complete current roadmap: completed work, remaining tasks, evidence gates and submission lifecycle |
| [docs/WORK_LOG.md](docs/WORK_LOG.md) | Dated work history, checks, failures, decisions, and next steps |
| [docs/DATA_AND_BASELINE_STUDY.md](docs/DATA_AND_BASELINE_STUDY.md) | Start here: received materials, findings and a practical reading sequence |
| [docs/PAPER_CODE_TRACEABILITY.md](docs/PAPER_CODE_TRACEABILITY.md) | Paper-reading coverage and method-to-author-code connections for all three candidates |
| [docs/CONTRIBUTION_AND_EVIDENCE_SCOPE.md](docs/CONTRIBUTION_AND_EVIDENCE_SCOPE.md) | Current claim, close-prior-art overlap, falsification and single-acquisition limits |
| [docs/COMPARISON_ROSTER_DECISION.md](docs/COMPARISON_ROSTER_DECISION.md) | Eleven-variant core design; four additional scores still unimplemented |
| [docs/INDEPENDENT_EVIDENCE_PLAN.md](docs/INDEPENDENT_EVIDENCE_PLAN.md) | Separate fault/benign-source admission and requirements for broader cyber evidence |
| [docs/COMPARATOR_ADMISSION.md](docs/COMPARATOR_ADMISSION.md) | Current comparator designations, information-access compatibility and remaining implementation gates |
| [docs/RESEARCH_QUESTION_AND_THREAT_MODEL.md](docs/RESEARCH_QUESTION_AND_THREAT_MODEL.md) | Selected state-synchronization question, restricted command threat and falsification criteria |
| [docs/ANNOTATION_FEATURE_SPLIT_CONTRACT.md](docs/ANNOTATION_FEATURE_SPLIT_CONTRACT.md) | Exact right-arm schedule labels, permitted joint-state inputs and chronological partitions |
| [docs/EVALUATION_PROTOCOL.md](docs/EVALUATION_PROTOCOL.md) | Exact evaluation populations, threshold-only calibration, repeats, metrics and protected final campaign |
| [docs/METRIC_DEFINITIONS.md](docs/METRIC_DEFINITIONS.md) | Counts, AP ties, coverage, alarm episodes, event delay and synthetic acceptance examples |
| [docs/FINAL_TEST_PROTECTION.md](docs/FINAL_TEST_PROTECTION.md) | Prospective outcome protection and actual-artifact freeze requirements; not an enforced lock |
| [docs/SOFTWARE_VALIDATION.md](docs/SOFTWARE_VALIDATION.md) | Implemented loader/isolation/metric primitives, 83 synthetic tests, limitations and reproducible command |
| [docs/BOUNDED_PILOT_PLAN.md](docs/BOUNDED_PILOT_PLAN.md) | Historical specification for the single bounded velocity pilot |
| [docs/OBSERVER_VALIDATION_REPORT.md](docs/OBSERVER_VALIDATION_REPORT.md) | 254 tests; empirical observer and matched ablations; 7 normal checks and 48 artifact checks passed, with strong AR and ambiguity limitations |
| [docs/CONTROL_STUDY_REPORT.md](docs/CONTROL_STUDY_REPORT.md) | 205 tests; seven full-training normal-only candidates; selected velocity, 32-bin template and AR(4) artifacts |
| [docs/SIMPLE_CONTROLS_PLAN.md](docs/SIMPLE_CONTROLS_PLAN.md) | Fixed formulas, initialization, finite selection and resource limits |
| [docs/PILOT_REPORT.md](docs/PILOT_REPORT.md) | 150 synthetic tests and the completed real normal-only pilot, artifacts, resources and limits |
| [docs/ENVIRONMENT.md](docs/ENVIRONMENT.md) | Isolated standard-library test environment and actual interpreter |
| [docs/RESEARCH_BASICS_LESSON.md](docs/RESEARCH_BASICS_LESSON.md) | Step 0: twins, baselines, scores, thresholds, evaluation and leakage |
| [docs/YOUR_STEP_0_NOTES.md](docs/YOUR_STEP_0_NOTES.md) | Researcher's unanswered comprehension exercise |
| [docs/CASPER_DATASET_IDENTITY.md](docs/CASPER_DATASET_IDENTITY.md) | Actual received files, hashes, schemas and timing/label limits |
| [docs/DATASET_IDENTITY_REGISTER.md](docs/DATASET_IDENTITY_REGISTER.md) | Current consolidated release, six-file hash recheck, labels and exact clock inventory |
| [docs/BASELINE_DATASET_CORRESPONDENCE.md](docs/BASELINE_DATASET_CORRESPONDENCE.md) | What connects each paper to our files, and what remains unproved |
| [docs/CASPER_SENSOR_SCHEMA.md](docs/CASPER_SENSOR_SCHEMA.md) | Full nested-field validation, data dictionary and controller clock interpretation |
| [docs/CASPER_ANNOTATION_LINEAGE.md](docs/CASPER_ANNOTATION_LINEAGE.md) | Manual-label coordinate mapping and complete score history |
| [docs/BASELINE_CODE_STUDY.md](docs/BASELINE_CODE_STUDY.md) | Pinned source/result pack and paper-to-code reading notes |
| [docs/MANUSCRIPT_COLLECTION_AUDIT.md](docs/MANUSCRIPT_COLLECTION_AUDIT.md) | Collected paper/code artifacts and remaining full-text gaps |
| [docs/COMPARISON_PROTOCOL.md](docs/COMPARISON_PROTOCOL.md) | Proposed separate evaluation groups and pre-training gates |
| [docs/BASELINE_SELECTION_REPORT.md](docs/BASELINE_SELECTION_REPORT.md) | Current robotics recommendation, three-paper study set and unresolved admission criteria |
| [docs/BASELINE_SELECTION_CRITERIA.md](docs/BASELINE_SELECTION_CRITERIA.md) | Manufacturing-specific recency, shared-data, access and evaluation rules |
| [docs/LITERATURE_EVIDENCE.md](docs/LITERATURE_EVIDENCE.md) | Primary-source evidence and baseline eligibility |
| [docs/DATASET_ACCESS_CHECKLIST.md](docs/DATASET_ACCESS_CHECKLIST.md) | Access, releases, files, labels, and unresolved questions |
| [docs/REPRODUCTION_PLAN.md](docs/REPRODUCTION_PLAN.md) | Proposed evaluation, implementation and verification |
| [papers/](papers/README.md) | Reading notes and privately stored full texts |
| [datasets/](datasets/README.md) | Separate raw/processed data and release manifests |
| [baselines/](baselines/README.md) | Upstream-method provenance and future checkouts |
| [configs/](configs/README.md) | Defined data/evaluation policies; future executable method configurations |
| [src/](src/README.md) | Implemented loader, guarded development access, causal coordinator and metric primitives |
| [tests/](tests/README.md) | Executable synthetic correctness/isolation checks |
| [experiments/](experiments/README.md) | Synthetic software report and pending experiment/final-freeze records |
| [manuscript/](manuscript/README.md) | Future paper and contribution records |

Current selection: **normal-only right-arm motion monitoring using original CASPER**, comparing added correction evidence with residual-only and conventional scores in a single-acquisition case study. The restricted threat assumes truthful monitoring telemetry/time. Exact source, annotations, twelve joint-state features and chronological split metadata are specified; 254 synthetic tests pass, the earlier pilot/control studies are preserved, and a separately bounded observer validation completed. Its state/prediction/synchronization checks support an empirical motion observer with a matched correction-evidence ablation. Simple AR remains stronger at one-step forecasting. The scope decision is complete; measured contribution, four score extensions and final admission remain open.

The [current comparison decision](docs/COMPARATOR_ADMISSION.md) keeps CASPER's external-IMU reproduction separate and held; a CASPER-inspired controller CNN is an independent design candidate. TWINE/CatBoost are background for Group D, with no admitted supervised side track. CASPER's corrected paper and TWINE's accepted manuscript are available and AI-audited (**2/3**); CatBoost full text remains unavailable. ModernTCN 2024 is a conditional modified author-code transfer candidate, requiring an adapter and validation; it is not a published CASPER baseline or reproduced method. The pilot is an independent ordinary control; novelty is unverified.

Run future commands from `manufacturing/`; its local `.venv/`, fitted preprocessing, data, and results must not depend on sibling-project state. Dataset authorization is checked per user, not inferred from folder ownership. The [shared research skill](../.agents/skills/academic-research-suite/SKILL.md) remains at the workspace root; its generated state belongs here.

See the [portfolio roadmap](../docs/RESEARCH_ROADMAP.md) for sequential milestones. The essential normal-only controls are fitted and selected. The empirical observer and matched ablations are now tested on normal data. Next: specify and implement/test the bounded C/K/L/Rv extension, then freeze the executable comparison before calibration. Independently audit voraus-AD admission as a physical-anomaly track; no additional dataset is admitted. No attack result or validated physical twin exists.
