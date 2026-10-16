# Water project status

Project ID: `water`\
Owner: **Muhammad Usman**\
Updated: **2026-10-16 (Asia/Karachi)**\
Stage: **literature/data audit; implementation not started**

## Completed

- Existing water brief, candidate register, detailed paper/code audit, reproduction plan, and dataset-source search migrated into this project.
- CAROTS and its no-ensemble variant selected as conditional first comparisons. [Evidence](docs/LITERATURE_EVIDENCE.md)
- Official access requirements and alternative source listings checked. Owner reports a COMSATS Sahiwal student university email; exact account/access not verified. [Access checklist](docs/DATASET_ACCESS_CHECKLIST.md)
- Shared machine and skill setup remain documented at root; local folders define separate future storage.

## Not completed / blockers

- No SWaT/WADI files or approval received/verified; no provider request sent by the assistant. No dataset hashes, release freeze or row counts exist.
- No local full-text paper collection has been downloaded; public manuscripts were read online for the audit.
- No project environment, dependency lock, loader, test implementation, baseline checkout, model execution, or benchmark score exists.
- CAROTS test-based threshold and separate max-F1 reporting need a declared protocol change. Label alignment, raw-folder writes, preprocessing, and CPU/MPS portability need validation.
- Trust-gating novelty is unestablished; alarm gating in prior work must be distinguished from protecting model updates. Legitimate process-change evidence is unresolved.

## Next bounded task

Arrange the official SWaT/WADI request using the owner's university identity, with explicit authorization for any assistant submission. Keep source leads separate from granted access. On receipt, identify releases/terms and preserve original files before loading. While waiting, read the audited CAROTS paper and refine the static fidelity checklist; do not tune against attack test labels.

## Run and manuscript state

Training runs: **none**. Reproduced baselines: **none**. Benchmark results: **none**. Manuscript: **not drafted**. Working title and mechanism: **provisional**. Paid/lengthy runs and publishing remain approval-gated.

## Session handoff

Work from `water/`. Read `../AGENTS.md`, `AGENTS.md`, `PROJECT_BRIEF.md`, this file, and the evidence/reproduction documents before implementation. Record new decisions and source evidence here or in the relevant local document; do not overwrite sibling-project contexts.

## Persistent work history

Read [docs/WORK_LOG.md](docs/WORK_LOG.md) for the dated history and [the shared playbook](../docs/RESEARCH_PLAYBOOK.md) for reusable steps. After each substantive session, append actual work to the log and refresh this status; keep proposed steps separate from completed checks and experiments.
