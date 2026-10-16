# Workspace decisions

## 2026-10-16 — Three independent projects

The user requested separate water, manufacturing and smart-grid research projects, with shared root instructions and skills. The owner mapping was explicitly confirmed:

- Muhammad Usman → `water/`.
- Haiqa Mushtaq → `manufacturing/`.
- Muhammad Usman Sanghla → `smart_grids/`.

Folder ownership is not an authorship assignment. Each project retains its own question, baselines, datasets, evaluation, environments, runs and manuscript. The default future work order is water → manufacturing → smart grids, one milestone at a time.

## Migration record

The former single-water root `PROJECT_BRIEF.md` and `AGENTS.md` were moved into `water/`, then adapted to reference shared instructions. Root versions now describe the portfolio. Water-specific documents moved from `docs/` to `water/docs/`: literature evidence/candidates, dataset checklist and source searches, reproduction plan, readiness review, and all four detailed literature records. Their local Markdown links were rebased.

`docs/WORKSPACE_AUDIT.md` and `docs/RESEARCH_SKILL_SETUP.md` remain shared at root. The installed `.agents/skills/academic-research-suite/` package remains in place and was not reinstalled or edited. A temporary pre-migration documentation backup was created during the move; the migrated project files are the durable working context.

Manufacturing and grid source registers start as **initial screening**, not completed reproduction audits. No water baseline was silently adopted for another sector. New folder READMEs describe planned contents, not implemented models or acquired data.

The ignore policy was extended to nested project datasets, full-text downloads, environments, vendor checkouts and experiment outputs. No Git repository or remote was created. No datasets or full papers were downloaded during restructuring, no packages installed, no models run, and no messages or access requests sent.

## Setup validation

Checked the confirmed owner mapping, required project documents and storage directories. All 58 project Markdown files passed the local-link check; the original external source links in all nine migrated water evidence files were preserved. An isolated temporary Git repository verified 28 paths that must be ignored and 21 documentation/configuration paths that must remain trackable. Raw data, processed data, paper downloads, vendor checkouts, local state and run directories are empty. The installed skill's router and manifest hashes are unchanged. These are workspace checks, not benchmark results.
