# Water project status

Project ID: `water`\
Owner: **Muhammad Usman**\
Updated: **2026-10-16 (Asia/Karachi)**\
Stage: **Stage 2 assistant paper/code study completed; official dataset request submitted, approval pending; model implementation not started**

## Completed

- Submitted the [official SWaT/WADI request](docs/DATASET_REQUEST_PREPARATION.md) once after the user supplied the university email and explicitly agreed to the terms/privacy consent. Website success was observed and a safe receipt summary recorded; exact personal information remains private. Email delivery, provider approval and downloads are not verified. No duplicate submission is needed while the response is pending.
- Completed the assistant's [detailed study of the three papers](docs/PAPER_STUDY_GUIDE.md), with method-to-code guides for [CAROTS](baselines/carots/METHOD_TO_CODE.md), [IT-DT](baselines/it_dt/METHOD_TO_CODE.md) and [the ensemble](baselines/dt_ensemble/METHOD_TO_CODE.md), plus a [mechanism comparison](docs/MECHANISM_COMPARISON.md). Actual author functions are mapped only for CAROTS; the twin guides identify missing implementation details. The [reading record](papers/notes/READING_RECORD.md) keeps researcher reading/understanding unconfirmed.
- Prepared the [Step 0 research-basics lesson](docs/RESEARCH_BASICS_LESSON.md): a synthetic water-tank example, score/threshold/alarm flow, baselines versus ablations, data roles, leakage and adaptation. The [researcher note scaffold](papers/notes/research_basics.md) is unanswered; no mastery or human reading is inferred.
- Existing water brief, candidate register, detailed paper/code audit, reproduction plan, and dataset-source search migrated into this project.
- CAROTS and its no-ensemble variant selected as conditional first comparisons. [Evidence](docs/LITERATURE_EVIDENCE.md)
- Official access requirements and alternative source listings checked. The supplied COMSATS Sahiwal university email was entered in the authorized request; inbox receipt and dataset access remain unverified. [Access checklist](docs/DATASET_ACCESS_CHECKLIST.md)
- Shared machine and skill setup remain documented at root; local folders define separate future storage.
- [Detailed water roadmap](docs/RESEARCH_ROADMAP.md) created using the research skill's planning guidance, with numbered tasks through submission. Final-test scoring now explicitly follows development of all compared methods; no experiment stage is complete.
- [Baseline-selection criteria](docs/BASELINE_SELECTION_CRITERIA.md) documented under the user's latest literature-first direction. CAROTS, IT-DT and the ensemble are a provisional learning set; no three-method experimental shortlist is approved. Three additional leads were screened with unresolved/exclusion reasons recorded.
- Expanded search and [three-paper study selection](docs/BASELINE_SELECTION_REPORT.md) completed. Retained CAROTS → IT-DT → ensemble for complementary learning roles after checking additional twin, contamination and robustness candidates. RoCA is priority contamination prior art; ISTFAD is the priority inaccessible twin follow-up. [Search, exclusions and new evidence](docs/literature/EXPANDED_SEARCH_2026-10-16.md)
- The earlier in-memory paper audit is now followed by a [local three-paper collection](baselines/README.md): 110 public source objects and 79 reading derivatives, with hashes. Separate CAROTS, IT-DT and ensemble folders contain PDFs, original figures/tables/bibliographies, citations, protocol notes and missing-resource records.
- CAROTS has a selective 57-file author-code snapshot pinned to `63a41f45a2ae680d5cdbb2d5739e7a11264867cb`, plus 16 upstream SWaT/WADI CUTS+ graph/checkpoint/log artifacts. These checkpoints are not final CAROTS detector weights. No author code or checkpoint was executed/deserialized.
- Dataset mirrors were rechecked and their metadata saved. SWaT/WADI filenames matching CAROTS were found; provider permission and exact-release equivalence remain unverified. [Acquisition status](baselines/DATASET_ACQUISITION_STATUS.md)
- [Baseline verification](docs/BASELINE_VERIFICATION_REPORT.md) checked all 189 original collection files, complete PDF parsing/rendering, extracted tables, guide transcriptions, reference inventories and static CAROTS code. Authentic source records were established; material source problems were found. Per-paper reports retain exact evidence and unresolved checks. No blanket scientific validation is claimed.

## Not completed / blockers

- The official request has website submission confirmation, but no iTrust approval or raw SWaT/WADI files have been received or verified. No measured local dataset hashes, release freeze or row counts exist. Mirror metadata and application submission are not dataset receipt records.
- No matched public executable code, fitted models or full experimental outputs were verified for IT-DT or the ensemble. Those collections are complete only for the public resources located in this bounded search.
- No scientific project environment, dependency lock, benchmark loader/evaluator, research tests, model execution or reproduced score exists. Resource-download/extraction utilities exist; the CAROTS source snapshot is not an installed or validated implementation.
- CAROTS test-based threshold and separate max-F1 reporting need a declared protocol change. Label alignment, raw-folder writes, preprocessing, and CPU/MPS portability need validation.
- CAROTS published gradient clipping is 1.0 versus code default 0.5; resolve the intended configuration before a pilot. The repository's 51/49-channel issue is a user report requiring schema checks, not a reproduced failure here.
- CAROTS's ratio-calibration path has a missing validation-score input and attribute-name error; inference loader configuration and fresh-versus-cached causal checkpoint selection require repair/validation. Syntax checks passed, but no runtime compatibility is established.
- Deeper CAROTS source reading found that CPA injects noise outside the subsequent forecast's input slice, and the SOC loss averages eligible pairs globally rather than averaging within each anchor first. These are paper/code discrepancies with static evidence in [the walkthrough](baselines/carots/METHOD_TO_CODE.md); their runtime or performance effects have not been measured. Any correction needs an explicit deviation record.
- IT-DT's alarm plot disagrees with its displayed threshold, and its window-selection label provenance is unclear. The ensemble has incorrect reference identifiers, chi-square scaling and robustness-radius/norm problems, plus unresolved FPR and dataset protocol questions. Keep both numerical baselines on hold; do not import their performance or guarantee claims as established facts.
- Trust-gating novelty is unestablished; alarm gating in prior work must be distinguished from protecting model updates. Legitimate process-change evidence is unresolved.

## Next bounded task

Use the [paper study guide](docs/PAPER_STUDY_GUIDE.md) to explain CAROTS from normal windows to an alarm and record actual reading/questions in [the researcher record](papers/notes/READING_RECORD.md). Prepare a bounded CAROTS correction/deviation specification covering augmentation/loss semantics, calibration, alignment, checkpoints and device support before implementation. Keep the [Step 0 comprehension prompts](docs/RESEARCH_BASICS_LESSON.md) available as needed. Independently await the provider's response to the [submitted request](docs/DATASET_REQUEST_PREPARATION.md); no inbox access or background monitoring is implied. Download and hash originals only through an established authorized route. The [verification verdict](docs/BASELINE_VERIFICATION_REPORT.md) remains in force; three experimental baselines are **not** admitted. Keep final attack outcomes closed throughout development.

## Run and manuscript state

Training runs: **none**. Reproduced baselines: **none**. Benchmark results: **none**. Manuscript: **not drafted**. Working title and mechanism: **provisional**. Paid/lengthy runs and publishing remain approval-gated.

## Session handoff

Work from `water/`. Read `../AGENTS.md`, `AGENTS.md`, `PROJECT_BRIEF.md`, this file, and the evidence/reproduction documents before implementation. Record new decisions and source evidence here or in the relevant local document; do not overwrite sibling-project contexts.

## Persistent work history

Read [docs/WORK_LOG.md](docs/WORK_LOG.md) for the dated history and [the shared playbook](../docs/RESEARCH_PLAYBOOK.md) for reusable steps. After each substantive session, append actual work to the log and refresh this status; keep proposed steps separate from completed checks and experiments.

## Confirmed portfolio preferences

The [shared publication, writing and title standards](../docs/PUBLICATION_STANDARDS.md) now apply here. They guide future research and presentation; no title, venue, authorship or experimental claim was finalized. The current technical stage and next research task are unchanged.
