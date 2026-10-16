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
- [Detailed water roadmap](docs/RESEARCH_ROADMAP.md) created using the research skill's planning guidance, with numbered tasks through submission. Final-test scoring now explicitly follows development of all compared methods; no experiment stage is complete.
- [Baseline-selection criteria](docs/BASELINE_SELECTION_CRITERIA.md) documented under the user's latest literature-first direction. CAROTS, IT-DT and the ensemble are a provisional learning set; no three-method experimental shortlist is approved. Three additional leads were screened with unresolved/exclusion reasons recorded.
- Expanded search and [three-paper study selection](docs/BASELINE_SELECTION_REPORT.md) completed. Retained CAROTS → IT-DT → ensemble for complementary learning roles after checking additional twin, contamination and robustness candidates. RoCA is priority contamination prior art; ISTFAD is the priority inaccessible twin follow-up. [Search, exclusions and new evidence](docs/literature/EXPANDED_SEARCH_2026-10-16.md)
- Published CAROTS and CCM-TAD PDFs were retrieved and inspected in memory, with hashes recorded; their repositories were pinned for static audit. CAROTS paper/code clipping discrepancy was verified. No paper files were saved in the local collection and no code was run.

## Not completed / blockers

- No SWaT/WADI files or approval received/verified; no provider request sent by the assistant. No dataset hashes, release freeze or row counts exist.
- No local full-text paper collection has been downloaded; public manuscripts were read online for the audit.
- No project environment, dependency lock, loader, test implementation, baseline checkout, model execution, or benchmark score exists.
- CAROTS test-based threshold and separate max-F1 reporting need a declared protocol change. Label alignment, raw-folder writes, preprocessing, and CPU/MPS portability need validation.
- CAROTS published gradient clipping is 1.0 versus code default 0.5; resolve the intended configuration before a pilot. The repository's 51/49-channel issue is a user report requiring schema checks, not a reproduced failure here.
- Trust-gating novelty is unestablished; alarm gating in prior work must be distinguished from protecting model updates. Legitimate process-change evidence is unresolved.

## Next bounded task

Begin the [structured CAROTS reading sequence](docs/BASELINE_SELECTION_REPORT.md): researcher-owned explanation of the model and both variants, followed by a proposed reproduction/deviation specification. Then study IT-DT and the ensemble, with RoCA/context/shift work included before any novelty claim. The learning selection is complete for this bounded search; three experimental baselines are **not** admitted. Dataset-access preparation can proceed independently using roadmap W1, with explicit authorization for assistant submission. Keep final attack outcomes closed throughout baseline and proposed-method development.

## Run and manuscript state

Training runs: **none**. Reproduced baselines: **none**. Benchmark results: **none**. Manuscript: **not drafted**. Working title and mechanism: **provisional**. Paid/lengthy runs and publishing remain approval-gated.

## Session handoff

Work from `water/`. Read `../AGENTS.md`, `AGENTS.md`, `PROJECT_BRIEF.md`, this file, and the evidence/reproduction documents before implementation. Record new decisions and source evidence here or in the relevant local document; do not overwrite sibling-project contexts.

## Persistent work history

Read [docs/WORK_LOG.md](docs/WORK_LOG.md) for the dated history and [the shared playbook](../docs/RESEARCH_PLAYBOOK.md) for reusable steps. After each substantive session, append actual work to the log and refresh this status; keep proposed steps separate from completed checks and experiments.

## Confirmed portfolio preferences

The [shared publication, writing and title standards](../docs/PUBLICATION_STANDARDS.md) now apply here. They guide future research and presentation; no title, venue, authorship or experimental claim was finalized. The current technical stage and next research task are unchanged.
