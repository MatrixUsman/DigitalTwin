# Water infrastructure research project

Owner: **Muhammad Usman**. Project ID: `water`. Academic digital-twin cybersecurity research for water treatment and distribution; titles and contributions remain provisional.

Start with [PROJECT_BRIEF.md](PROJECT_BRIEF.md), [STATUS.md](STATUS.md), and [AGENTS.md](AGENTS.md), together with the [shared rules](../AGENTS.md). This folder is independent of its siblings. We have not trained models or measured benchmark results; downloaded author artifacts are labelled separately.

For the beginner-friendly sequence, follow the **[detailed water research roadmap](docs/RESEARCH_ROADMAP.md)**. It includes numbered small tasks, responsibilities, dependencies, artifacts, completion checks and the first five work sessions.

Current priority: work through the **[detailed paper study guide](docs/PAPER_STUDY_GUIDE.md)**, starting with CAROTS, and record your own explanations/questions in [the reading record](papers/notes/READING_RECORD.md). The assistant has completed source reading and method/code mapping; your reading and understanding remain unconfirmed. Use [Step 0: the research basics](docs/RESEARCH_BASICS_LESSON.md) and [your basics note](papers/notes/research_basics.md) whenever needed. The [mechanism comparison](docs/MECHANISM_COMPARISON.md) connects the three methods to our provisional adaptation question.

The **[official dataset request](docs/DATASET_REQUEST_PREPARATION.md)** was submitted once after explicit user consent, and the website confirmed success. Email delivery, approval and dataset downloads remain pending or unverified. No duplicate request is needed while awaiting the response. Learning priorities and experimental admission remain separate, and no three-method numerical comparison is finalized.

The **[local baseline resource collection](baselines/README.md)** now contains their PDFs, available code, original figures/tables, bibliographies and study guides. [Dataset acquisition remains unresolved](baselines/DATASET_ACQUISITION_STATUS.md): public mirrors were found, but SWaT/WADI approval and release equivalence are not established.

**Stage 3 update:** the [dataset identity audit](docs/DATASET_IDENTITY_AUDIT.md) now records target revisions, label rules, timestamp unknowns, baseline compatibility and distinct hash sources. The user reconfirmed no files received; the [local inventory and candidate register](datasets/manifests/README.md) are prepared, while actual-file identification remains incomplete.

The subsequent **[verification audit](docs/BASELINE_VERIFICATION_REPORT.md)** found intact files and genuine paper records, alongside substantive code, citation and scientific inconsistencies. Read that verdict before treating any published result or guarantee as reliable. CAROTS remains the conditional first reproduction; the two twin methods remain on hold.

The deeper [CAROTS walkthrough](baselines/carots/METHOD_TO_CODE.md) also identifies CPA noise outside the forecast input and SOC pair-versus-anchor averaging differences. These static findings need a correction/deviation specification; no runtime or performance effects have been measured.

| Location | Purpose |
|---|---|
| [docs/WORK_LOG.md](docs/WORK_LOG.md) | Dated work history, checks, failures, decisions, and next steps |
| [docs/LITERATURE_EVIDENCE.md](docs/LITERATURE_EVIDENCE.md) | Primary-source evidence and baseline eligibility |
| [docs/DATASET_ACCESS_CHECKLIST.md](docs/DATASET_ACCESS_CHECKLIST.md) | Access, releases, files, labels, and unresolved questions |
| [docs/REPRODUCTION_PLAN.md](docs/REPRODUCTION_PLAN.md) | Proposed evaluation, implementation and verification |
| [docs/PAPER_STUDY_GUIDE.md](docs/PAPER_STUDY_GUIDE.md) | Three-paper explanation and links to each method/code walkthrough |
| [docs/MECHANISM_COMPARISON.md](docs/MECHANISM_COMPARISON.md) | Online updates, trust assumptions and contamination questions across methods |
| [papers/notes/READING_RECORD.md](papers/notes/READING_RECORD.md) | Researcher-attested reading and questions, separate from assistant study |
| [papers/](papers/README.md) | Reading notes and privately stored full texts |
| [datasets/](datasets/README.md) | Separate raw/processed data and release manifests |
| [baselines/](baselines/README.md) | Three paper/resource folders, pinned CAROTS source and provenance |
| [configs/](configs/README.md) | Future explicit dataset/protocol/method configurations |
| [src/](src/README.md) | Future project implementation |
| [tests/](tests/README.md) | Planned correctness and leakage checks |
| [experiments/](experiments/README.md) | Future run records and results |
| [manuscript/](manuscript/README.md) | Future paper and contribution records |

CAROTS and CAROTS-dagger are conditional first baselines. Source files are collected; see the audited evidence before installation or execution.

Run future commands from `water/`; its local `.venv/`, fitted preprocessing, data, and results must not depend on sibling-project state. Dataset authorization is checked per user, not inferred from folder ownership. The [shared research skill](../.agents/skills/academic-research-suite/SKILL.md) remains at the workspace root; its generated state belongs here.

See the [portfolio roadmap](../docs/RESEARCH_ROADMAP.md) for sequential milestones. Assistant source study is complete; researcher reading, reproduction specifications and authorized dataset receipt are next. No model execution has begun.
