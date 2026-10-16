# Smart manufacturing research project

Owner: **Haiqa Mushtaq**. Project ID: `manufacturing`. Academic digital-twin cybersecurity research for manufacturing processes; titles and contributions remain provisional.

Start with [PROJECT_BRIEF.md](PROJECT_BRIEF.md), [STATUS.md](STATUS.md), and [AGENTS.md](AGENTS.md), together with the [shared rules](../AGENTS.md). This folder is independent of its siblings. No trained models or benchmark results exist.

| Location | Purpose |
|---|---|
| [docs/WORK_LOG.md](docs/WORK_LOG.md) | Dated work history, checks, failures, decisions, and next steps |
| [docs/DATA_AND_BASELINE_STUDY.md](docs/DATA_AND_BASELINE_STUDY.md) | Start here: received materials, findings and a practical reading sequence |
| [docs/PAPER_CODE_TRACEABILITY.md](docs/PAPER_CODE_TRACEABILITY.md) | Paper-reading coverage and method-to-author-code connections for all three candidates |
| [docs/RESEARCH_QUESTION_AND_THREAT_MODEL.md](docs/RESEARCH_QUESTION_AND_THREAT_MODEL.md) | Selected state-synchronization question, restricted command threat and falsification criteria |
| [docs/ANNOTATION_FEATURE_SPLIT_CONTRACT.md](docs/ANNOTATION_FEATURE_SPLIT_CONTRACT.md) | Exact right-arm schedule labels, permitted joint-state inputs and chronological partitions |
| [docs/EVALUATION_PROTOCOL.md](docs/EVALUATION_PROTOCOL.md) | Exact evaluation populations, threshold-only calibration, repeats, metrics and protected final campaign |
| [docs/METRIC_DEFINITIONS.md](docs/METRIC_DEFINITIONS.md) | Counts, AP ties, coverage, alarm episodes, event delay and synthetic acceptance examples |
| [docs/FINAL_TEST_PROTECTION.md](docs/FINAL_TEST_PROTECTION.md) | Prospective outcome protection and actual-artifact freeze requirements; not an enforced lock |
| [docs/SOFTWARE_VALIDATION.md](docs/SOFTWARE_VALIDATION.md) | Implemented loader/isolation/metric primitives, 83 synthetic tests, limitations and reproducible command |
| [docs/BOUNDED_PILOT_PLAN.md](docs/BOUNDED_PILOT_PLAN.md) | Proposed simple velocity-control feasibility pilot; no training executed |
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

Current selection: **normal-only right-arm motion monitoring using original CASPER**, testing whether state synchronization can conceal changed-speed evidence. The restricted threat assumes truthful monitoring telemetry/time. Exact source, annotations, twelve joint-state features and chronological split metadata are specified; foundational synthetic checks pass, while model configurations, model-specific tests and pilot execution admission remain open. **CASPER (2024), TWINE (2026) and CatBoost on CASPER (2026)** remain learning papers with unequal inputs/supervision, not a single admitted ranking. CASPER's full paper is collected; TWINE/CatBoost full-text gaps persist. External-IMU reproduction remains a separate track. No model has run and novelty is unverified.

Run future commands from `manufacturing/`; its local `.venv/`, fitted preprocessing, data, and results must not depend on sibling-project state. Dataset authorization is checked per user, not inferred from folder ownership. The [shared research skill](../.agents/skills/academic-research-suite/SKILL.md) remains at the workspace root; its generated state belongs here.

See the [portfolio roadmap](../docs/RESEARCH_ROADMAP.md) for sequential milestones. Current work has reached synthetic software validation and pilot specification; no model execution has begun.
