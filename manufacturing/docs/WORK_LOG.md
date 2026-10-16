# Manufacturing work log

Owner: **Haiqa Mushtaq**. Follow the [shared playbook](../../docs/RESEARCH_PLAYBOOK.md) and its entry template. [STATUS.md](../STATUS.md) contains the current handoff; this log preserves the sequence of actual work. Shared setup history is in the [root log](../../docs/WORK_LOG.md).

### 2026-10-16 — MFG-001 — Initial project history

Record type: **retrospective summary** from the linked project documents, written when persistent work logging was introduced. It is not a newly executed audit or a reconstructed command transcript.

- Created the independent manufacturing brief, instructions, storage structure, initial literature register, dataset checklist and reproduction proposal. The process/sequence direction remains provisional.
- Evidence: [brief](../PROJECT_BRIEF.md), [literature register](LITERATURE_EVIDENCE.md), [dataset checklist](DATASET_ACCESS_CHECKLIST.md), and [reproduction proposal](REPRODUCTION_PLAN.md).
- Blockers: no selected process, verified common attack dataset/release, executable main baseline or environment. Initial framework/testbed leads still need full protocol and code audits.
- Next bounded action when this project is active: apply the shared literature/data-feasibility procedure to manufacturing sources; verify attack labels, chronology, production phases and licensing before choosing a baseline.
- Checks/outcomes: source-screening findings and unknowns are recorded in the linked evidence documents. Shared folder/link/ignore validation is recorded in [workspace decisions](../../docs/WORKSPACE_DECISIONS.md); no new scientific validation is claimed by this entry.
- Historical commands: not reconstructed. Future entries must capture exact commands and working directories when needed for reproducibility.
- Run state: **none**. No dataset download, model reproduction, training or benchmark result exists in this project at initialization of this log.
- Reusable lesson: follow the shared checklist while making sector-specific data and baseline decisions. Do not inherit another project's completed status or results.

### 2026-10-16 — MFG-002 — Session logging enabled

Record type: contemporaneous. Added this log and navigation from the project README/status under the user's shared-workflow request. No project research state or scientific evidence was changed. After each substantive task, append actual actions, artifacts, checks, failures, decisions and the next step here; update status and add proven reusable lessons to the shared playbook. Run state: **none**. Next action remains the bounded task recorded above and in status.

### 2026-10-16 — MFG-003 — Shared publication and presentation preferences

Record type: contemporaneous. Under the user's explicit instruction covering all three projects, linked the [shared publication standards](../../docs/PUBLICATION_STANDARDS.md) from this project's brief/status. Leading-journal ambitions, natural precise prose, distinctive evidence-supported titles and accurate professional-use records now persist as shared instructions. Titles and contributions remain provisional; no authorship assignment, venue choice or immigration eligibility determination was made. See [SHARED-006](../../docs/WORK_LOG.md) for the common record. Research stage, data access and experimental state are unchanged. No implementation, training, external messages or push occurred. Next action remains this project's recorded research task.

### 2026-10-16 — MFG-004 — Manufacturing baseline and open-data feasibility audit

Record type: contemporaneous. Scope/authorization: the user explicitly switched from water while waiting for data and requested recent manufacturing baselines sharing accessible, non-water data, using the skill and project instructions. Applied bounded literature/source verification from the pinned academic-research-suite; no automated full research-to-paper pipeline. Read shared/project instructions, briefs, status, logs, publication rules and playbook first.

Actions completed:

- Parallel primary-source searches covered explicit manufacturing twins, recent comparable detectors and public provider data. Checked publisher/DOI and institutional records, available author manuscripts, linked author code and provider metadata. Detailed queries, failed retrievals and source locators are retained in the three screens below.
- Identified **original CASPER robotic-arm pick-and-place data** as the preferred accessible anchor. Provider v3/date/license/file inventory and an unauthenticated archive response were checked without reading its body. Original CC BY-SA 4.0 and newer collection MIT metadata remain separate. No received-byte hashes invented.
- Connected **CASPER 2024, TWINE 2026 and CatBoost 2026** to author repositories. Pinned revisions and inspected selected notebook/script paths without running code. The CatBoost author-code search initially failed, then succeeded through the first author's portfolio/ORCID and explicit IEEE link; the final records include this correction.
- Preserved blockers: unavailable full TWINE/CatBoost manuscripts, exact publication-run mapping, differing supervision/input trust, release ambiguity, code licenses and label/evaluation defects. CATBOOST's synthetic labels are source-code behavior, not measured benchmark ground truth. No claim that the inspected script necessarily produced published results.
- Screened MIT machining/assembly synthetic data and CMU TEP manipulations as public alternatives. Recorded why ICS-Flow is water-adjacent, fault/operational corpora do not establish cyberattacks, and FactoryIO/LOTL are distinct datasets. Did not manufacture a third same-protocol comparator.
- Created manufacturing admission rules and a synthesis/selection report, three baseline source-note folders, and refreshed the brief, status, access checklist, literature register and reproduction proposal. Shared root context now records manufacturing as active; water/grid files and the installed skill were not edited.

Evidence/artifacts:

- [Selection report](BASELINE_SELECTION_REPORT.md) and [admission criteria](BASELINE_SELECTION_CRITERIA.md).
- [Provider/access screen](literature/OPEN_DATASET_SCREEN_2026-10-16.md), [comparator manuscript/code screen](literature/COMPARATOR_SCREEN_2026-10-16.md), [twin-method screen](literature/TWIN_METHOD_SCREEN_2026-10-16.md).
- [Baseline note index](../baselines/README.md), [receipt checklist](DATASET_ACCESS_CHECKLIST.md), [reproduction proposal](REPRODUCTION_PLAN.md).

Commands/working directory: `/Users/matrixusman/CUI/DigitalTwin`. Local read-only checks used `git status --short`, `rg --files manufacturing`, selected `cat`/`rg`/`sed` reads, and `git diff HEAD --check`. Source retrieval used web search/open plus standard-library `urllib.request` for the exact provider/DOI/GitHub endpoints in the detailed screens; source bodies were parsed as text/JSON, never executed. The comparator screen records the exact temporary PDF extraction command and hashes. Some sandbox DNS/HTTP routes failed; authorized public reads resolved selected gaps. No system packages were changed.

Validation: local Markdown targets checked with Python `pathlib` and Markdown-link extraction; the final pass covered **28 documents and 152 local targets**, with zero missing paths. Raw/processed/vendor/run directories each contained zero files. `git diff HEAD --check` passed across staged and unstaged documentation changes; `git diff HEAD --name-only -- water smart_grids .agents .codex` returned no changes. An independent read-only review of the synthesis/admission criteria found no actionable contradictions with the source screens. These are document/provenance checks, not model tests or scientific results.

Reproducible final local-link/inventory check (no network or data reads):

```sh
python3 - <<'PY'
from pathlib import Path
import re
files = list(Path('manufacturing').rglob('*.md')) + [Path(p) for p in ('README.md', 'PROJECT_BRIEF.md', 'docs/RESEARCH_PLAYBOOK.md', 'docs/WORK_LOG.md')]
missing = []
for file in files:
    for target in re.findall(r'\]\(([^)]+)\)', file.read_text()):
        target = target.strip('<>').split('#', 1)[0]
        if not target or re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:', target):
            continue
        if not (file.parent / target).exists():
            missing.append((str(file), target))
assert not missing, missing
for name in ('datasets/raw', 'datasets/processed', 'baselines/vendor', 'experiments/runs'):
    path = Path('manufacturing') / name
    assert not any(p.is_file() for p in path.rglob('*'))
print('Local links valid; raw/processed/vendor/run inventories empty.')
PY
git diff HEAD --check
```

Decision: industrial robotics is the preferred next feasibility route, with CASPER first to study and conditionally reproduce. The three-paper critical-learning set is **not** execution-ready or an established fair numerical comparison. Keep the title, mechanism and novelty provisional; CASPER+ already describes related research directions.

Reusable lesson: the [shared playbook](../../docs/RESEARCH_PLAYBOOK.md) now records bounded public endpoint checks, exact collection/loader matching, label provenance and the separation of learning versus experimental admission. Run state: **none**. No benchmark data bodies acquired, model/attack/simulator execution, Azure setup, package installation, author contact, paid service, publication, commit or push performed by the assistant. Next action: bounded original-CASPER acquisition/identity planning and missing manuscript/run reconciliation, before any environment or training.

### 2026-10-16 — MFG-005 — Step 0 beginner lesson and comprehension worksheet

Record type: contemporaneous. User asked to learn twins, baselines, scores, thresholds and data leakage. Prepared a manufacturing-specific lesson using the research skill's source-verification discipline and the shared teaching procedure. Verified NIST twin/manufacturing context and primary security-ML/scikit-learn evaluation guidance. No broad literature rescreen or experiment pipeline was launched.

Artifacts: [RESEARCH_BASICS_LESSON.md](RESEARCH_BASICS_LESSON.md), [YOUR_STEP_0_NOTES.md](YOUR_STEP_0_NOTES.md). The robot-angle and six-point label examples are explicitly **synthetic**. They teach state/model/calibration distinctions, anomaly versus attack, fair information access, score versus probability, independent threshold calibration, confusion-matrix denominators, event versus point evaluation and chronology/window leakage. The worksheet remains unanswered; no researcher reading or understanding is attested.

Checks: a separate read-only reviewer checked arithmetic and terminology. Corrected wording to distinguish labels needed for evaluation from labels available to an operating detector, and to say detectors compute scores from permitted observations. A standard-library arithmetic check verified TP/FP/FN/TN at thresholds 1.5, 3 and 5 as `(3,2,0,1)`, `(2,1,1,2)` and `(1,0,2,3)`. This is classroom arithmetic, not a benchmark or model experiment. Sources are linked in the lesson; older methodological background is not counted as a recent baseline.

Working directory: repository root. No environment/packages/models created. Next learning action: researcher explains the four worksheet prompts; give feedback only on their actual response. Shared playbook records reusable clarifications without copying learning completion to another project.

### 2026-10-16 — MFG-006 — Original CASPER receipt, manuscript follow-up and comparison protocol

Record type: contemporaneous. The user expanded the task to explicitly authorize original-CASPER collection/identification, missing-manuscript resolution and a fair comparison protocol before training, while retaining Step 0. This superseded earlier source-screen-only scope; no further download permission was needed. Read existing rules/audits, checked storage/ignore coverage, and used separate bounded dataset and manuscript workers. The parent prepared/reviewed the protocol and integrated project status.

Completed:

- Original author Kaggle **v3** archive (2,824,019,108 bytes) and five unchanged members (7,899,312,074 bytes) preserved under ignored `datasets/raw/casper/v3/`. Version/license were checked before/after the latest-endpoint download; all members passed CRC and received SHA-256 hashes. Originals are read-only. About 10.72 GB total archive+member storage; no paid compute.
- Full streaming CSV structural/native-clock/label audit and numeric correspondence check. Each arm: 1,762,650 rows, eight positive runs, asynchronous native clocks. Original Nicla: 1,751,682 numeric rows after six startup records, no time/label fields. Fixed Nicla contains the same numeric sequence under binary64 parsing; it is not an aligned or labelled dataset. PCAP received/integrity-checked, not decoded or replayed.
- CASPER corrected VOR V1.1 (36 pages) collected and matched to prior SHA-256; targeted methods reading plus selected notebook/author-source snapshots. One full paper collected, **TWINE/CatBoost full texts still unresolved** after lawful publisher/institutional/author routes. Two TWINE institutional PDF endpoints returned 403; IEEE presented robot verification; no bypass, purchase or author contact. Available source-code findings remain distinct from proven published-run correspondence.
- [COMPARISON_PROTOCOL.md](COMPARISON_PROTOCOL.md) prepared: normal-only external-IMU and supervised controller groups kept separate; proposed chronological 50/15/15/20 normal partition; train-only fitting; normal calibration at a declared empirical 99th percentile; no test-based tuning; explicit coverage, endpoint/event semantics and combined-history purging. Exact annotation/feature/split manifests and Group B admission remain blocked by unresolved evidence. This is not an execution-ready protocol or permission to train.
- Refreshed current brief/instructions/status, data/paper/baseline indexes, access checklist and reproduction proposal. Earlier selection-session no-download statements retained as historical scope with a current-stage pointer. Root context and shared playbook updated; water/grid files and installed skills left unchanged.

Evidence: [identity report](CASPER_DATASET_IDENTITY.md), [receipt manifest](../datasets/manifests/casper_v3_receipt.json), [manuscript collection/mapping audit](MANUSCRIPT_COLLECTION_AUDIT.md), [manuscript manifest](../papers/MANUSCRIPT_MANIFEST.json), [protocol](COMPARISON_PROTOCOL.md), [audit utilities](../scripts/README.md). Detailed source metadata, CSV profiles, clock/annotation intervals and original-source artifacts are ignored/local; tracked notes contain provenance/aggregate facts, not raw observations.

Executed dataset commands, from `/Users/matrixusman/CUI/DigitalTwin`:

```sh
python3 manufacturing/scripts/acquire_casper_v3.py
python3 manufacturing/scripts/profile_casper_v3.py
python3 manufacturing/scripts/inspect_casper_alignment.py
```

The profiler was refined for the fixed file's header and rerun; final outputs are identified in the receipt. Public network access required approved sandbox execution. No system packages changed. Manuscript retrieval/extraction/render commands and source failures are in its audit; local collection script is retained under ignored `papers/downloads/`. No detector/code snapshot or checkpoint was executed.

Validation: dataset worker checked complete decompression/CRC, all hashes, read-only modes, final utility/profile provenance and ignore rules. Manuscript worker checked 14 successful source/derived artifact hashes and ignore coverage, notebook JSON and rendered PDF pages. Parent independently parsed the receipt/manuscript JSON and three audit utilities, matched member sizes, confirmed read-only/ignore status, and checked local links. The pre-log pass covered **33 documents and 205 local links**, with no missing targets. `git diff HEAD --check` passed; `git ls-files manufacturing/datasets/raw manufacturing/baselines/casper/artifacts manufacturing/baselines/twine/artifacts manufacturing/baselines/catboost/artifacts` returned no tracked payload files. No training tests or model scores were generated.

A separate read-only review found four protocol wording/support issues; fixed current-measurement availability, supervised training/validation label access, unknown-gap alarm contiguity, and combined filter/model/aggregation history. No supported primary event/delay claim is made while clock/annotation provenance remains unresolved.

Final post-log check: **34 Markdown documents and 218 local links passed**, receipt/manuscript JSON and three script syntax checks passed, processed-data and run directories remained empty, and `git diff HEAD --check` passed. No water/grid/skill changes appeared in the scoped diff.

Run state: **data acquisition/identity and document checks only**, plus separately labelled synthetic teaching arithmetic. No training, fitted transforms, benchmark scores, cloud/simulator setup, packet replay, installs, external messages, uploads, publication, commit or push by the assistant.

Next bounded technical action: reconcile the paper's retrospective IMU annotation with frozen bytes and document uncertainty/clock limitations; select an admissible information-access group and freeze annotation/feature/split manifests before implementation. Obtain lawful missing full texts or keep affected methods on hold. No novelty or superiority conclusion follows from receipt or code inspection.

### 2026-10-16 — MFG-007 — Collected source/result pack and deeper dataset study

Record type: contemporaneous. User requested “download datasets and stuff and study them properly,” continuing manufacturing. Read root/project rules, current briefs/status/log and the installed research skill's bounded source-verification guidance; used the PDF skill for targeted manuscript inspection. Original CASPER was already fully received, so it was not downloaded again. Delegated independent controller-schema, manuscript and source-pack work; parent traced annotation/score indices, reviewed findings and integrated a beginner reading guide.

Actually completed:

- Collected **67 pinned repository artifacts / 6,477,266 bytes**, plus three complete repository-tree receipts. The pack contains 18 source/config/doc files and 49 author-reported tables/figures (34 tables, 15 figures). All tracked TWINE/CatBoost blobs are represented; CASPER omits only an autosave notebook and OS metadata. Existing originals remained unchanged. Artifact URLs, revisions, SHA-256 and Git blob identities are in [SOURCE_PACK_MANIFEST.json](../baselines/SOURCE_PACK_MANIFEST.json). Author outputs remain explicitly **unreplicated** in ignored baseline storage.
- Fully parsed both controller files: **3,525,300 rows / 232,669,800 scalar values**, including nested vectors. No missing/invalid/nonfinite values or shape errors found; both hashes match the original receipt. Sixty-six scalar values per row include time and label; 64 potential observables are not an approved feature set. New [sensor study](CASPER_SENSOR_SCHEMA.md) and [separate schema manifest](../datasets/manifests/casper_controller_schema_audit.json) preserve the historical receipt.
- Matched a pinned later author capture source's complete CSV header/order to received fields. Official UR definitions and capture mapping support controller seconds since startup. Exact original executing revision/configuration, wall-clock anchors, cross-device synchronization and IMU timing remain unresolved. Capture labels are scheduled application flags, not independently measured physical-onset times.
- Statically extracted the upstream eight manual IMU slices and traced all index spaces in [annotation lineage](CASPER_ANNOTATION_LINEAGE.md). Filtered endpoints map by +916 numeric rows; complete CNN score support spans 1,529 raw observations. Derived 676,807 score positions and positive/negative targets 341,608/335,199 match Figure 11 class totals. This is bookkeeping consistency, **not reproduced model predictions**. No labels or processed training arrays were created.
- Visually confirmed Figure 11's four convolution layers agree with code, narrowing the earlier prose/architecture concern. Table 11 lists 750 fewer IMU points than received; the discrepancy remains explicit. Notebook final-end prose differs from its slice by six samples. No boundary was chosen to improve a detector.
- Extended lawful full-text searches through institutional/author-linked sources. TWINE/CatBoost full manuscripts remain unavailable; the ordinary browser route reported no browser available. No request to authors, payment or access-control bypass. [Manuscript audit](MANUSCRIPT_COLLECTION_AUDIT.md) and manifest record checks and two additional CASPER page renders.
- Wrote the [data and baseline study guide](DATA_AND_BASELINE_STUDY.md) and [paper-to-code study](BASELINE_CODE_STUDY.md); refreshed status, brief, indexes, checklist, protocol pointers and shared reusable procedure. The original broad phase/changeover question is not established as testable from this corpus alone. Three learning papers remain distinct from three admitted comparative methods.

New code-study details: CASPER README has an MIT badge without matching license text; checkpoint and test-label threshold issues remain. TWINE has distinct training/explanation/demo models/features and missing demo functions/assets. CatBoost's “SSL” uses labelled cross-entropy, reports weighted metrics, and launches ten experiments on import. These source observations are not proof that every paper result used that exact path. No upstream file was imported or executed.

Executed commands from `/Users/matrixusman/CUI/DigitalTwin`:

```sh
python3 manufacturing/scripts/audit_casper_controller_schema.py
python3 manufacturing/scripts/audit_casper_annotation_lineage.py
python3 manufacturing/local/source_pack_collection/collect_source_pack.py
python3 manufacturing/local/source_pack_collection/collect_reported_artifacts.py
python3 manufacturing/local/study_pack_validation/validate.py
```

The annotation audit was hardened after an independent read-only review to require valid finite nine-field IMU records before applying exact warmup arithmetic, then rerun. It reads existing metadata and notebook source, not sensor values. Its local result hash is `4ddbb14e3dd0704807fa63dae6ded64d95e993bb99f797522777d7fec6bd3dfa`; the result contains the script/source/profile/receipt hashes, environment and timestamps. Complete support was checked using a **synthetic index-set union**, not a dataset/model performance test. Source collectors and validation utility remain in ignored local storage, with their hashes recorded. No dependency installation occurred.

Validation: workers checked raw byte identity, source-field mapping, complete nested schema, all collected Git blob/SHA-256 identities, read-only/ignore coverage, CSV/PNG integrity, and manuscript/render provenance. Parent independently verified **89 artifact hashes**, all 67 source-pack blob identities and ignore/read-only status, six upstream Python syntax trees, four JSON/notebook structures, five audit script syntax trees, and original receipt/profile linkage. Initial documentation validation covered **31 Markdown files / 277 local links**, with no failures. No raw/source payload is tracked; processed-data/run storage remains empty. Independent review found annotation/score arithmetic and qualifications correct. No changes appeared under water, smart_grids or installed skills. `git diff HEAD --check` passed. Observed workspace HEAD during integration: `48795ac18a8846df383bb44074b5821e6999b63a`; workspace already had changes at task start and automatic workspace snapshots can advance this revision.

Run state: **data/source audit and synthetic index bookkeeping only**. No training, installed model environment, benchmark scores, learned parameters, cloud deployment, packet replay, external messages, paid service, upload, publication, or assistant-issued commit/push. Researcher reading/comprehension remains unassessed.

Next bounded action: study CASPER with the new guide, then propose a versioned external-IMU annotation/feature/split contract that states onset uncertainty, warmup, exclusions and permitted claims. No frozen benchmark manifest or permission for long training is implied. Keep inaccessible full texts and code-use/published-run provenance issues open.

Final post-log validation at `2026-10-16T17:51:33Z`: the same 89 artifact hashes, source/syntax/receipt checks and empty derivative/run checks passed; all **287 local links across 31 Markdown files** resolved, with zero validation failures.

### 2026-10-16 — MFG-008 — Read available papers and connect methods to pinned code

Record type: contemporaneous. User requested “Collect and read papers; connect their methods to author code.” Active scope remained manufacturing. Reused the existing dataset, manuscript and 67-file source pack instead of redownloading. Read current project/shared context and used the academic research skill's bounded source-verification workflow, with PDF inspection for CASPER. Three scoped workers studied CASPER, TWINE and CatBoost; parent independently reviewed key source cells, one figure and selected author-summary arithmetic, reconciled current documentation and checked artifacts.

Deliverables: [paper-to-code coverage map](PAPER_CODE_TRACEABILITY.md), [CASPER reading record](../baselines/casper/READING_NOTES.md), [TWINE reading record](../baselines/twine/READING_NOTES.md), and [CatBoost reading/result-provenance record](../baselines/catboost/READING_NOTES.md). Updated project status, paper/baseline indexes and current code/manuscript audit pointers. Earlier architecture wording was corrected to reflect the already visually verified four-convolution match. Shared playbook gained a reusable result-column/unit tracing procedure; sibling projects and installed skills stayed untouched.

Actual coverage and findings:

- **CASPER:** main text §§1–7, PDF pp. 1–30, read; Figures 1–12 visually inspected and notebook detector branches mapped by zero-based cell. References inventoried, not individually verified. Eleven additional page renders and a receipt remain ignored under `baselines/casper/artifacts/reading_renders/`. Hardware/system/threat assumptions are distinguished from the offline detector code and future online/edge work. Training fractions and output units differ between comparator branches. Figure 10's confusion counts, its caption, Table 14 and code denominator do not reconcile; PLS terminology/configuration, XGBoost windows and Dense-AE targets need clarification. These findings do not invalidate all paper results. CNN architecture and static class-total correspondences remain supported.
- **TWINE:** available institutional abstract/records plus both complete notebooks, all three modules and twin schema studied. Confirmed 63-feature training, weighted metrics, 100-tree evaluation versus 50-tree/depth-10 SHAP, and a separate five-feature shuffled/subsampled Azure demonstration. New MTU institutional and Tartu publication-list checks found no full manuscript; publisher returned 403. No blind repeat of the failed institutional PDF endpoints. Full-paper reading remains incomplete.
- **CatBoost:** official abstract, publisher metadata, university/author records, main code and saved author tables studied. Headline numbers round to ten-run mean test accuracy/weighted F1; derived “validation” columns instead match test values. Population versus sample SD differs across artifact families; neural timing is per batch while classical timing is per observation. Some auxiliary validation zeros are placeholders. An arithmetic audit checked **48 means, 48 population SDs, 96 interval endpoints, 42 sample SDs, 420 rounded run cells and six mean-table mappings** (660 checks). These are author-summary consistency checks, not our detector results or a verification of the underlying experimental design. New primary institutional/portfolio checks yielded no accessible full paper.

Public source collection added four small, read-only page/asset captures for CatBoost's identity/abstract links; no new full manuscript, dataset, model checkpoint or dependency was acquired. A public portfolio JavaScript asset was read only as text. Source URLs, times and hashes are in ignored `local/catboost_result_audit/public_source_receipts.json`; received bytes and prior manifests were preserved. The parent also opened ACM (403), the QUB institutional record and official APSCON abstract. Inaccessible sources remain explicitly unresolved, not fabricated/nonexistent.

Commands from `/Users/matrixusman/CUI/DigitalTwin`:

```sh
python3 manufacturing/local/catboost_result_audit/audit_author_tables.py
python3 manufacturing/local/paper_code_validation/validate.py
```

CASPER render commands/page scales and source hashes are recorded in `baselines/casper/artifacts/reading_renders/RENDER_RECEIPT.json`. Author arithmetic audit hash: `f1e52ccc72361e3ef9d69256bf6ef635226d0b013ec0a6881661a481589d8a01`; render receipt hash: `c3494d014c8c6d73c60482d287d16564ae16f140e9b93e8889302d9a7b78e591`. Both retain exact input/source provenance. A separate parent validation script preserves the earlier MFG-007 validation utility/hash and output.

Initial parent validation passed **115 artifact hash checks**, all pinned pack identities/read-only/ignore checks, three independently recomputed CatBoost author means, two Figure 10 arithmetic checks, 11 new render hashes, JSON/notebook structure, six upstream Python syntax trees, five dataset-audit script syntax trees and prior receipt/lineage links. It covered **35 Markdown files / 336 local links** before final integration/log links. An independent read-only review tightened “static source data flow” and “F1 in inspected code” wording so the map cannot imply runtime or unseen-paper verification. Raw/processed/run state and Git exclusion checks passed; no benchmark was run.

Run state: **paper/source reading, document rendering and arithmetic of author-reported summaries only**. No upstream import/execution, model fitting, test threshold selection, data modifications, installed environment, cloud/robot execution, messages to authors, paid service, upload, publication or assistant-issued commit/push. Human reading/comprehension remains unassessed. Full-paper coverage is **one of three**; all three have source-study records, none has a reproduced run.

Next bounded action remains the external-IMU annotation/feature/split contract with declared timing uncertainty and normal-only calibration. Obtain lawful TWINE/CatBoost full manuscripts when available, or retain those comparison claims on hold. Do not tune toward published headline scores or turn source-level corrections into an unreported faithful-reproduction claim.

Final post-integration validation at `2026-10-16T18:03:04Z`: **115 artifact hash checks and 347 local links across 35 Markdown files passed**, together with the recorded syntax, source-identity, arithmetic and raw/run-state checks. Zero validation failures; no water, smart-grid or skill changes in the scoped diff.
