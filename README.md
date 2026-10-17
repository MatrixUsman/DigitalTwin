# Three independent digital-twin cybersecurity research projects

Start here. This workspace supports three separate academic papers. The owners and sectors below were confirmed on **16 October 2026**. Project ownership is an organizational responsibility, not a final authorship or author-order decision.

| Owner | Project | Current position |
|---|---|---|
| **Muhammad Usman** | [Water infrastructure](water/README.md) | Existing literature audit preserved; SWaT/WADI access and releases unresolved; CAROTS is the conditional first baseline |
| **Haiqa Mushtaq** | [Smart manufacturing](manufacturing/README.md) | Right-arm state-synchronization question and exact data contract defined; no training, novelty or final baseline admission |
| **Usman Zahoor** | [Smart Grids](smart_grids/README.md) | Initial scoping and source screening; no selected dataset pair or approved baseline |

No project has reproduced a model or generated benchmark results. Working titles and research questions remain provisional.

All three follow the [shared publication, writing and title standards](docs/PUBLICATION_STANDARDS.md): aim for leading journals through rigorous distinct research, use natural academic prose, and choose strong titles supported by the eventual contribution. These preferences are persistent project instructions, not claims of acceptance or results.

Private repository: [MatrixUsman/DigitalTwin](https://github.com/MatrixUsman/DigitalTwin), branch `main`. It stores project documents and future eligible source/configuration files. Datasets, access records, environments, run outputs and the reinstallable third-party skill package remain excluded by `.gitignore`. To restore the skill on another machine, follow its [pinned installation record](docs/RESEARCH_SKILL_SETUP.md), adapting the local destination path. Git does not preserve empty directories; recreate the documented local storage directories when needed.

```text
DigitalTwin/
  README.md                    # start here and choose a project
  PROJECT_BRIEF.md             # portfolio decisions and independence
  AGENTS.md                    # shared research rules
  .gitignore                   # protects data/outputs in all projects
  .agents/skills/               # shared, pinned ARS-Codex installation
  docs/                        # shared roadmap, decisions, machine/skill records
  water/                       # Muhammad Usman
  manufacturing/               # Haiqa Mushtaq
  smart_grids/                 # Muhammad Usman Sanghla
```

Each topic has its own `PROJECT_BRIEF.md`, `AGENTS.md`, `STATUS.md`, and folders for `docs/`, `papers/`, `datasets/`, `baselines/`, `configs/`, `src/`, `tests/`, `experiments/`, and `manuscript/`. Their README files explain what belongs there. These are research scaffolds; no model implementation or downloaded dataset is implied.

## How to work here

1. Choose a project explicitly: for example, “Work in `water/`: continue the dataset-access audit.”
2. Read root `AGENTS.md`, then that project's `AGENTS.md`, `PROJECT_BRIEF.md`, and `STATUS.md`.
3. Keep project data, fitted transforms, checkpoints, environments, configurations, logs, and manuscript claims inside that project. Run commands from its directory and record the working directory.
4. Follow the [repeatable research playbook](docs/RESEARCH_PLAYBOOK.md). Read the project's `docs/WORK_LOG.md` to see what has already been done.
5. End a work session by appending actual work and checks to that log and updating `STATUS.md`. Add reusable lessons to the playbook so the next project can follow them.

The [shared work log](docs/WORK_LOG.md) records workspace-wide changes. Project logs retain their own detailed history: [water](water/docs/WORK_LOG.md), [manufacturing](manufacturing/docs/WORK_LOG.md), and [smart grids](smart_grids/docs/WORK_LOG.md).

Planned order: **water → manufacturing → smart grids**, one bounded milestone at a time. The user has now selected **manufacturing while water awaits access**. Its public-data and baseline screen is in the [selection report](manufacturing/docs/BASELINE_SELECTION_REPORT.md); shared-release/protocol admission remains pending. First finish each sector's feasibility, datasets, and baseline decisions; then implement and run each project separately. See the [shared roadmap](docs/RESEARCH_ROADMAP.md).

The installed [research skill](.agents/skills/academic-research-suite/SKILL.md) stays at the root. Its source material is shared; generated research notes and state belong to the active project. [Installation provenance](docs/RESEARCH_SKILL_SETUP.md) and the [original machine audit](docs/WORKSPACE_AUDIT.md) are shared references.
