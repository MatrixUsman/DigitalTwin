# Smart manufacturing research project

Owner: **Haiqa Mushtaq**. Project ID: `manufacturing`. Academic digital-twin cybersecurity research for manufacturing processes; titles and contributions remain provisional.

Start with [PROJECT_BRIEF.md](PROJECT_BRIEF.md), [STATUS.md](STATUS.md), and [AGENTS.md](AGENTS.md), together with the [shared rules](../AGENTS.md). This folder is independent of its siblings. No trained models or benchmark results exist.

| Location | Purpose |
|---|---|
| [docs/WORK_LOG.md](docs/WORK_LOG.md) | Dated work history, checks, failures, decisions, and next steps |
| [docs/BASELINE_SELECTION_REPORT.md](docs/BASELINE_SELECTION_REPORT.md) | Current robotics recommendation, three-paper study set and unresolved admission criteria |
| [docs/BASELINE_SELECTION_CRITERIA.md](docs/BASELINE_SELECTION_CRITERIA.md) | Manufacturing-specific recency, shared-data, access and evaluation rules |
| [docs/LITERATURE_EVIDENCE.md](docs/LITERATURE_EVIDENCE.md) | Primary-source evidence and baseline eligibility |
| [docs/DATASET_ACCESS_CHECKLIST.md](docs/DATASET_ACCESS_CHECKLIST.md) | Access, releases, files, labels, and unresolved questions |
| [docs/REPRODUCTION_PLAN.md](docs/REPRODUCTION_PLAN.md) | Proposed evaluation, implementation and verification |
| [papers/](papers/README.md) | Reading notes and privately stored full texts |
| [datasets/](datasets/README.md) | Separate raw/processed data and release manifests |
| [baselines/](baselines/README.md) | Upstream-method provenance and future checkouts |
| [configs/](configs/README.md) | Future explicit dataset/protocol/method configurations |
| [src/](src/README.md) | Future project implementation |
| [tests/](tests/README.md) | Planned correctness and leakage checks |
| [experiments/](experiments/README.md) | Future run records and results |
| [manuscript/](manuscript/README.md) | Future paper and contribution records |

Current recommendation: **industrial robotic arms using original CASPER pick-and-place data**. Its public download route was verified without institutional approval. **CASPER (2024), TWINE (2026) and CatBoost on CASPER (2026)** are the critical-learning shortlist, with matched author code and explicit limitations. None is execution-ready; exact shared release, input/label comparability, missing manuscript access and code/protocol issues remain. No raw data was downloaded. Start with the selection report above.

Run future commands from `manufacturing/`; its local `.venv/`, fitted preprocessing, data, and results must not depend on sibling-project state. Dataset authorization is checked per user, not inferred from folder ownership. The [shared research skill](../.agents/skills/academic-research-suite/SKILL.md) remains at the workspace root; its generated state belongs here.

See the [portfolio roadmap](../docs/RESEARCH_ROADMAP.md) for sequential milestones. Current work is planning and source audit, not model execution.
