# Water project status

Project ID: `water`\
Owner: **Muhammad Usman**\
Updated: **2026-10-16 (Asia/Karachi)**\
Stage: **three-paper resource collection and data-access audit; model implementation not started**

## Completed

- Existing water brief, candidate register, detailed paper/code audit, reproduction plan, and dataset-source search migrated into this project.
- CAROTS and its no-ensemble variant selected as conditional first comparisons. [Evidence](docs/LITERATURE_EVIDENCE.md)
- Official access requirements and alternative source listings checked. Owner reports a COMSATS Sahiwal student university email; exact account/access not verified. [Access checklist](docs/DATASET_ACCESS_CHECKLIST.md)
- Shared machine and skill setup remain documented at root; local folders define separate future storage.
- [Detailed water roadmap](docs/RESEARCH_ROADMAP.md) created using the research skill's planning guidance, with numbered tasks through submission. Final-test scoring now explicitly follows development of all compared methods; no experiment stage is complete.
- [Baseline-selection criteria](docs/BASELINE_SELECTION_CRITERIA.md) documented under the user's latest literature-first direction. CAROTS, IT-DT and the ensemble are a provisional learning set; no three-method experimental shortlist is approved. Three additional leads were screened with unresolved/exclusion reasons recorded.
- Expanded search and [three-paper study selection](docs/BASELINE_SELECTION_REPORT.md) completed. Retained CAROTS → IT-DT → ensemble for complementary learning roles after checking additional twin, contamination and robustness candidates. RoCA is priority contamination prior art; ISTFAD is the priority inaccessible twin follow-up. [Search, exclusions and new evidence](docs/literature/EXPANDED_SEARCH_2026-10-16.md)
- The earlier in-memory paper audit is now followed by a [local three-paper collection](baselines/README.md): 110 public source objects and 79 reading derivatives, with hashes. Separate CAROTS, IT-DT and ensemble folders contain PDFs, original figures/tables/bibliographies, citations, protocol notes and missing-resource records.
- CAROTS has a selective 57-file author-code snapshot pinned to `63a41f45a2ae680d5cdbb2d5739e7a11264867cb`, plus 16 upstream SWaT/WADI CUTS+ graph/checkpoint/log artifacts. These checkpoints are not final CAROTS detector weights. No author code or checkpoint was executed/deserialized.
- Dataset mirrors were rechecked and their metadata saved. SWaT/WADI filenames matching CAROTS were found; provider permission and exact-release equivalence remain unverified. [Acquisition status](baselines/DATASET_ACQUISITION_STATUS.md)

## Not completed / blockers

- The user confirms no iTrust approval has been received. No raw SWaT/WADI files are present; no provider request was sent by the assistant. No measured local dataset hashes, release freeze or row counts exist. Mirror metadata is not a receipt record.
- No matched public executable code, fitted models or full experimental outputs were verified for IT-DT or the ensemble. Those collections are complete only for the public resources located in this bounded search.
- No scientific project environment, dependency lock, benchmark loader/evaluator, research tests, model execution or reproduced score exists. Resource-download/extraction utilities exist; the CAROTS source snapshot is not an installed or validated implementation.
- CAROTS test-based threshold and separate max-F1 reporting need a declared protocol change. Label alignment, raw-folder writes, preprocessing, and CPU/MPS portability need validation.
- CAROTS published gradient clipping is 1.0 versus code default 0.5; resolve the intended configuration before a pilot. The repository's 51/49-channel issue is a user report requiring schema checks, not a reproduced failure here.
- Trust-gating novelty is unestablished; alarm gating in prior work must be distinguished from protecting model updates. Legitimate process-change evidence is unresolved.

## Next bounded task

Begin the [local CAROTS reading pack](baselines/carots/README.md) and [structured reading sequence](docs/BASELINE_SELECTION_REPORT.md): researcher-owned explanation of the model and both variants, followed by a proposed reproduction/deviation specification. Then study IT-DT and the ensemble. Resolve authorized dataset receipt independently; do not treat mirrors as matched releases. Three experimental baselines are **not** admitted. Keep final attack outcomes closed throughout baseline and proposed-method development.

## Run and manuscript state

Training runs: **none**. Reproduced baselines: **none**. Benchmark results: **none**. Manuscript: **not drafted**. Working title and mechanism: **provisional**. Paid/lengthy runs and publishing remain approval-gated.

## Session handoff

Work from `water/`. Read `../AGENTS.md`, `AGENTS.md`, `PROJECT_BRIEF.md`, this file, and the evidence/reproduction documents before implementation. Record new decisions and source evidence here or in the relevant local document; do not overwrite sibling-project contexts.

## Persistent work history

Read [docs/WORK_LOG.md](docs/WORK_LOG.md) for the dated history and [the shared playbook](../docs/RESEARCH_PLAYBOOK.md) for reusable steps. After each substantive session, append actual work to the log and refresh this status; keep proposed steps separate from completed checks and experiments.

## Confirmed portfolio preferences

The [shared publication, writing and title standards](../docs/PUBLICATION_STANDARDS.md) now apply here. They guide future research and presentation; no title, venue, authorship or experimental claim was finalized. The current technical stage and next research task are unchanged.
