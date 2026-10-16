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
