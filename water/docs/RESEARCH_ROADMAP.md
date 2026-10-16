# Water research roadmap: from first reading to a defensible paper

## Material Passport

- Origin skill: **academic-research-suite / ARS-Codex 3.23.1**, `experiment-agent` planning guidance, with the paper-planning readiness guidance consulted for the writing stages.
- Origin date: **2026-10-16, Asia/Karachi**. Version: **water_roadmap_v1**.
- Verification status: **UNVERIFIED experimental plan**. Planning and document checks do not validate a model or a scientific claim.
- Owner: **Muhammad Usman**. Project directory: `water/`. This document is a proposed working checklist, not an approved experiment configuration or a completed ARS research-to-paper pipeline.
- Source of decisions: the user's confirmed water/SWaT/WADI scope and the existing project audit. The final question, architecture, contribution, paper venue and authorship remain open.

## Start here

Our first research milestone is **an authorized, identifiable dataset pair and a baseline pipeline we can explain and reproduce**. The first scientific milestone is a fair comparison that can support or reject the adaptation hypothesis. A polished title comes later.

Use this file for the order of work. Use [REPRODUCTION_PLAN.md](REPRODUCTION_PLAN.md) for technical protocol details, [LITERATURE_EVIDENCE.md](LITERATURE_EVIDENCE.md) for source evidence, [DATASET_ACCESS_CHECKLIST.md](DATASET_ACCESS_CHECKLIST.md) for access/releases, and [WORK_LOG.md](WORK_LOG.md) for what actually happened. [STATUS.md](../STATUS.md) is the short handoff.

**Priority update, 2026-10-16:** the user wants to select three recent papers on the shared dataset pair for learning first. Start with [BASELINE_SELECTION_CRITERIA.md](BASELINE_SELECTION_CRITERIA.md) and Stage 2; access preparation may proceed in parallel. This changes the next work package, not the data/evaluation prerequisites for later experiments.

**Selection outcome:** the [expanded search report and reading sequence](BASELINE_SELECTION_REPORT.md) retain CAROTS, IT-DT and the ensemble for initial study. Start the researcher-owned CAROTS explanation next. No human-reading, implementation or experimental-admission checkbox is complete merely because the assistant performed this source audit.

**Acquisition update, 2026-10-16:** the [three baseline packs](../baselines/README.md) now contain local full texts, figures/tables/references and available pinned CAROTS author artifacts. The user confirms no iTrust approval; [mirror provenance and release matching](../baselines/DATASET_ACQUISITION_STATUS.md) remain unresolved. The immediate next action is learning from these packs, not training.

**Verification update:** read the [audit verdict](BASELINE_VERIFICATION_REPORT.md) before using those packs. Files passed integrity checks, while source code, figures, formulas and references contain material issues. The twin papers remain critical-reading material, not trusted numerical comparators. Researcher reading and runtime verification are still incomplete.

**Deep-study and request update, 2026-10-16:** the assistant completed the [paper study guide](PAPER_STUDY_GUIDE.md), three method-to-code walkthroughs and [mechanism comparison](MECHANISM_COMPARISON.md). Researcher reading/understanding remains unconfirmed in [the reading record](../papers/notes/READING_RECORD.md). The [official SWaT/WADI request](DATASET_REQUEST_PREPARATION.md) was submitted once with explicit consent and website confirmation. Email delivery, approval and downloads remain unverified. These updates supersede the earlier preparation-only status; they do not complete the human-reading or experimental stages.

Checkboxes are task status, not promises. Tick an item only after its output exists and its check passes; cite the evidence in the work log. **U** = researcher action/decision; **A** = assistant work within the authorized task; **B** = both. The next session should address a small set of IDs, not run this entire document automatically. All proposed file paths below resolve from `water/`; a path in backticks may not exist yet.

### Current position

- [x] Water sector and project owner agreed; separate project folder and instructions exist.
- [x] Initial paper/code/source audit and proposed common protocol recorded.
- [x] Private workspace repository and shared work-log procedure established.
- [x] This detailed roadmap written; that does not complete its future steps.
- [x] Three baseline resource packs collected, hashed and inspected; missing public code/results recorded.
- [x] Assistant source study, method-to-code guides, protocol-gap audit and cross-paper mechanism comparison prepared.
- [x] Official SWaT/WADI form submitted once with explicit user consent; safe website receipt summary recorded.
- [ ] Authorized SWaT and WADI files received and identified.
- [ ] Human reading of core papers recorded by the researcher; no reading is assumed on your behalf.
- [ ] Environment, loaders, evaluator, baseline and meaningful software tests implemented.
- [ ] Experiments, measured results, validated contribution and manuscript completed.

The earlier 2026-10-16 inventory found empty storage. The subsequent acquisition task populated `baselines/<method>/artifacts/` and `baselines/carots/vendor/author_code/`. Raw/processed dataset storage and experiment runs remain empty. Uninspected external storage remains unknown.

### The order and the dependencies

| Stage | Outcome | Depends on |
|---|---|---|
| 0 | Understand the task and key terms | Existing brief |
| 1 | Request/verify dataset permission | Accurate researcher identity |
| 2 | Read and audit core papers | Can proceed while access is pending |
| 3 | Identify received datasets | Access and acquisition authorization |
| 4 | Choose a feasible question and comparison set | Literature plus data capabilities |
| 5 | Freeze development/test boundaries and evaluation | Exact releases and comparison requirements |
| 6 | Build isolated software foundation | Authorized implementation and inspected dependencies |
| 7 | Validate loaders, splits and evaluator | Stages 3, 5 and 6 |
| 8 | Make CAROTS run on development data | Passing software checks and upstream audit |
| 9 | Implement and validate a fixed twin | A documented model and available inputs |
| 10 | Develop a narrowly specified adaptation hypothesis | Development evidence and prior-art analysis |
| 11 | Freeze all comparisons and run final evaluation | All selection complete; run approval where required |
| 12 | Analyse evidence and write the paper | Traceable results; source notes can start earlier |
| 13 | Review, submit and respond | Author-approved manuscript and publication permission |

**Important sequencing rule:** baseline reproduction has two parts. First establish implementation fidelity and development-data behavior. Reserve final held-out attack scoring until the proposed method, controls and analysis are frozen. Do not inspect baseline test failures and then design a method around them while calling those same attacks an untouched final test.

No calendar deadline is promised. Access, paper availability, learning time and measured runtime determine progress. A stage may finish with an honest feasibility failure or a revised question; it need not produce a positive result.

## 0. Learn enough to explain what we are doing

**Output:** a short researcher-owned note in `papers/notes/research_basics.md`. **Done when:** you can explain the data flow and distinguish the roles below in your own words.

**Learning session, 16 October 2026:** the assistant prepared [the Step 0 lesson](RESEARCH_BASICS_LESSON.md), with a synthetic tank calculation, detection flow, comparison roles, split example, leakage cases and comprehension prompts. [Your note scaffold](../papers/notes/research_basics.md) awaits your own explanation. Teaching material is available; the checkboxes below remain open because preparation does not establish researcher understanding or provider-specific channel verification.

- [ ] **W0.01 · U:** Read [the brief](../PROJECT_BRIEF.md) and state the candidate question in one sentence. Mark any wording you do not understand.
- [ ] **W0.02 · B:** Draw a simple offline flow: recorded measurements → expected behavior → anomaly score → threshold → alarm → evaluation.
- [ ] **W0.03 · B:** Identify sensors, actuators, controller commands and process state using provider documentation; do not assume a recorded command is trustworthy.
- [ ] **W0.04 · B:** Explain what the proposed twin would estimate or predict and which observations keep it synchronized. An ordinary classifier is not automatically a twin.
- [ ] **W0.05 · B:** Distinguish an anomaly, a physical fault, a documented cyberattack and a legitimate operating change. Write what labels we would need for each.
- [ ] **W0.06 · U:** Explain why a baseline is an existing method used for comparison, while an ablation removes one component to test its contribution.
- [ ] **W0.07 · B:** Work through a tiny **synthetic** example of training, validation, calibration and final testing. These sets have different jobs.
- [ ] **W0.08 · B:** Explain why changing a threshold after seeing test attacks is leakage, even if the model weights stay unchanged.
- [ ] **W0.09 · U:** Keep a list of unresolved terms; learn the terms needed for the current step rather than postponing all research for a large course.

Quick vocabulary: a **score** measures suspiciousness; a **threshold** converts it into an alarm; a **release** identifies a particular dataset version; a **seed** controls a source of randomness; a **checkpoint** stores model state; an **event** is a documented attack interval; a **false alarm** occurs during eligible normal operation. A **reimplementation** is our code based on a method description, not the original author's code.

## 1. Establish the legitimate dataset-access route

**Output:** updated access checklist plus private request/access record in `local/`. **Done when:** the requester and each data user are covered by the relevant permission and an authorized acquisition source is identified. Local receipt and release verification belong to Stage 3. Submission alone does not complete this stage.

**Current status, 16 October 2026:** the [official request](DATASET_REQUEST_PREPARATION.md) was submitted once after the university email was supplied and the user explicitly accepted terms/privacy consent. Website success was observed; a private record and safe summary exist. The user's earlier-request status remains unknown, but the current authorized submission is confirmed. Do not submit another request merely because approval is pending. Email delivery, provider approval and dataset receipt are separate unresolved steps; Stage 1 is not complete.

- [ ] **W1.01 · U:** Confirm privately that your own COMSATS Sahiwal student email works and you can receive messages. Do not put the address or login credentials in the repository.
- [x] **W1.02 · B:** Open the [official request form](https://www.sutd.edu.sg/itrust/request-for-datasets/) and inspect the current [terms](https://www.sutd.edu.sg/itrust/itrust-labs/datasets/terms-of-usage/). Current form/terms were checked; subsequent user agreement is recorded in the [request summary](DATASET_REQUEST_PREPARATION.md).
- [x] **W1.03 · B:** Enter the supplied identity/institution/email, category, region and date; select SWaT and WADI. Fields were read back, and explicit terms/privacy consent was received before checking the consent boxes. Personal values remain private; this does not establish inbox delivery or provider acceptance.
- [x] **W1.04 · U/A:** Obtain explicit user authorization and submit the reviewed form. The assistant clicked Submit once; website success was observed. No second submission is needed now.
- [x] **W1.05 · B:** Record request date, requested datasets and receipt observation privately; retain the [safe status summary](DATASET_REQUEST_PREPARATION.md). No request identifier or download link was displayed.
- [ ] **W1.06 · U:** Monitor inbox/spam for the provider's response. Record approval, denial, missing information or no response accurately; do not equate silence with approval.
- [ ] **W1.07 · B:** If follow-up is necessary, prepare accurate questions about access/releases. Sending an inquiry is a separate authorized action; do not invent a supervisor or affiliation.
- [ ] **W1.08 · B:** Check who may use the files and which storage/compute locations are permitted. A private GitHub repository does not permit uploading restricted datasets.
- [ ] **W1.09 · A:** Determine which release includes the required normal recordings, attack recordings, schemas and corrected attack intervals; retain unresolved provider naming/date discrepancies.
- [ ] **W1.10 · A:** Recheck free disk against archive, extraction, processed-data and run-output needs using actual advertised/received sizes. Historical free-space numbers are not a capacity guarantee.
- [ ] **W1.11 · B:** If access fails, keep reading/code inspection moving. Reconsider feasibility with the user; do not silently replace WADI, use an unverified mirror, or pretend a reduced sample is the agreed benchmark.

The form and terms were re-opened on 2026-10-16: it requests a university/organization email; the terms prohibit recipient redistribution, require attribution and require notification after publication. Student-email ownership is not proof of acceptance. Read the actual terms rather than relying only on this summary.

## 2. Build a small, traceable paper collection and actually read it

**Output:** bibliographic records, versioned source notes, a paper-to-code checklist and an updated evidence table. **Done when:** the selected method can be explained and its unresolved reproduction details are explicit. No arbitrary paper count is required.

**Assistant study completed:** [the Stage 2 guide](PAPER_STUDY_GUIDE.md) links the detailed [CAROTS](../baselines/carots/METHOD_TO_CODE.md), [IT-DT](../baselines/it_dt/METHOD_TO_CODE.md) and [ensemble](../baselines/dt_ensemble/METHOD_TO_CODE.md) walkthroughs. Only CAROTS has matched author functions to trace. The other guides identify conceptual implementation contracts and missing details. Human tasks remain open until the researcher supplies their own reading scope and explanations in [READING_RECORD.md](../papers/notes/READING_RECORD.md).

- [x] **W2.01 · A:** Inspect CAROTS proceedings, full manuscript and author repository; retain pinned revision. Evidence: [CAROTS pack](../baselines/carots/README.md).
- [x] **W2.02 · A:** Obtain the three open full texts. Per the user's folder request, files are stored under ignored `baselines/<method>/artifacts/papers/`; no earlier-chat attachment was assumed to transfer.
- [x] **W2.03 · A:** Record title/authors/dates/identifier/version in each pack and source URLs, acquisition times and hashes in the [resource manifest](../baselines/RESOURCE_MANIFEST.json).
- [x] **W2.04 · A:** Create primary-metadata `CITATION.bib` in each baseline folder, replacing the proposed single `papers/references.bib` location for these three papers. Author bibliographies remain separate, not fully verified citation records.
- [ ] **W2.05 · U:** First reading pass: abstract, main diagram, introduction, conclusion and limitations. Write the problem, inputs, output and claimed contribution in your own words.
- [ ] **W2.06 · U:** Second pass: dataset section, preprocessing, method, loss/objective, evaluation and ablations. Mark equations and experimental choices you cannot explain yet.
- [ ] **W2.07 · B:** Third pass for the first implementation: map each algorithm step to a code file/function or mark it unresolved. Assistant mapping with paper/source anchors exists in [CAROTS METHOD_TO_CODE.md](../baselines/carots/METHOD_TO_CODE.md); researcher review/explanation remains pending.
- [x] **W2.08 · A:** Separate authors' reported results from our observations in each pack's `PUBLISHED_RESULTS.md`. No measured-results table exists here.
- [x] **W2.09 · A:** Audit file names, downsampling, exclusions, windows, validation, thresholds, checkpoints, fusion, metrics and test-label use against the available paper/code. Each [method guide](PAPER_STUDY_GUIDE.md) contains the audit and unresolved fields. This completes an assistant source/protocol-gap audit, not validation of absent data or execution.
- [ ] **W2.10 · B:** Read IT-DT next as the provisional model-based twin candidate. The assistant's [study](../baselines/it_dt/METHOD_TO_CODE.md) records identification, filtering, residual and calibration gaps; researcher reading/explanation remains pending. No verified author code means a future implementation would be ours.
- [ ] **W2.11 · B:** Read the ensemble for state assimilation, alarm gating, model-update admission and threshold adaptation. The assistant's [study](../baselines/dt_ensemble/METHOD_TO_CODE.md) separates those operations and documents algorithm order; researcher reading/explanation remains pending.
- [ ] **W2.12 · A:** Continue CDT/DPDGAD full-text/code verification only as needed for comparator selection; record inaccessible material without filling gaps by guesswork.
- [ ] **W2.13 · A:** Create a dated search log for closest adaptive/gated twin methods, including queries, searched sources, reasons for inclusion/exclusion and unresolved leads. Refresh it before final novelty claims.
- [x] **W2.14 · A — comparison artifact:** Created [MECHANISM_COMPARISON.md](MECHANISM_COMPARISON.md): online changes, clean-data admission, trusted information, contamination evidence and limits. This checks only assistant artifact preparation; joint interpretation and researcher understanding remain pending.
- [ ] **W2.15 · U:** Record actual sections read and questions in [the reading record](../papers/notes/READING_RECORD.md). AI extraction or assistant review must not become a human-read declaration.
- [ ] **W2.16 · B:** Keep background/older work and unreviewed preprints separate from recent main comparisons. Preserve the agreed main-paper window, 2023-10-16 through 2026-10-16, unless explicitly revised later.

The initial roadmap drew on the existing [audit](LITERATURE_EVIDENCE.md); the subsequent [deep-study pass](PAPER_STUDY_GUIDE.md) read the collected full methods and mapped the pinned CAROTS code. It found CPA noise outside the subsequent forecast input and SOC pair-versus-anchor averaging differences; runtime effects have not been measured. Preserve source files and record proposed corrections separately. The first non-twin baseline remains CAROTS full plus CAROTS-dagger, conditionally; no variant is selected because it is easier to beat.

## 3. Receive, identify and preserve the exact dataset files

**Requires:** Stage 1 and an authorized acquisition task. **Output:** release manifests and a data-dictionary report. **Done when:** every required file, annotation and transformation rule has a traceable identity; test contents have not been used to design a model.

- [ ] **W3.01 · A:** Create ignored release-specific raw directories and verify the ignore rule before saving data. Keep private download links in `local/` only.
- [ ] **W3.02 · A:** Download normal, attack, metadata and attack-interval files from the authorized source; record acquisition dates and original names.
- [ ] **W3.03 · A:** Verify archive integrity before extraction; retain original archives unchanged. Check that expected files are present and not empty Git LFS pointers or HTML error pages.
- [ ] **W3.04 · A:** Compute SHA-256 and byte sizes of originals; create `datasets/manifests/<dataset>_<release>.json` with safe metadata only.
- [ ] **W3.05 · A:** Resolve corrected versus uncorrected releases and known startup removals. Avoid dropping startup samples twice; do not silently rename a release to resolve contradictory provider dates.
- [ ] **W3.06 · A:** Inspect sheet/header structure, text encoding, timestamp format, timezone status, units and label syntax. Preserve original row IDs for alignment.
- [ ] **W3.07 · A:** Classify features as sensors, actuators and metadata. Keep labels, timestamps and row IDs outside learned feature arrays.
- [ ] **W3.08 · A:** Record observed row counts, date ranges, duplicates, timestamp reversals, gaps, missing markers and sampling cadence. Mark unknown units/timezones as unknown.
- [ ] **W3.09 · A:** Map release-documented labels explicitly to internal normal `0` / attack `1`; reject unexpected labels. Reconcile file labels with the official interval table under a recorded policy.
- [ ] **W3.10 · B:** Restrict attack-file inspection to necessary structural/annotation integrity work. Log any access; do not explore attack traces or detector failures for feature/model design.
- [ ] **W3.11 · A:** Put conversions and caches under `datasets/processed/`, keyed by raw hashes and configuration. Rehash originals after loader checks to confirm no writes.
- [ ] **W3.12 · B:** Freeze the chosen SWaT and WADI release identities for comparisons. If only one dataset is available, label work partial and keep the shared-pair claim blocked.

## 4. Narrow the question to what our evidence can answer

**Output:** `docs/QUESTION_AND_THREAT_MODEL.md` and a comparison decision record. **Done when:** the researcher has chosen a feasible scope, not when we have invented a new-sounding title.

- [ ] **W4.01 · B:** Restate the candidate question and identify what observation would support it and what would contradict it.
- [ ] **W4.02 · B:** Specify an offline chronological replay study, the two plants and the detector's available observations. Do not describe it as live deployment.
- [ ] **W4.03 · B:** State which sensors/actuators an attacker may manipulate, when and for how long. State what, if anything, remains trustworthy.
- [ ] **W4.04 · B:** Specify what changes in the twin: state estimate, model parameters, residual reference distribution or threshold. Choose one initial adaptation target; a moving state estimate alone is not learned-model adaptation.
- [ ] **W4.05 · B:** Identify real legitimate-change annotations, or a separately validated process simulator and its assumptions. Standard attack detection recordings alone do not establish this evidence.
- [ ] **W4.06 · B:** If legitimate-change evidence is absent, narrow the claim to documented attack detection plus explicitly synthetic measurement/adaptation stress tests. A sensor offset must not be called a hydraulic operating change.
- [ ] **W4.07 · B:** Specify independent variables: fixed/ungated/gated update policy, corruption timing/severity and available trusted inputs. Specify measured outcomes and controlled settings.
- [ ] **W4.08 · B:** List confounds: extra model capacity, extra information, different thresholds, different features, different warmup, different compute and different release preprocessing.
- [ ] **W4.09 · B:** Admit CAROTS variants as non-twin controls if their execution prerequisites pass. Select a fixed twin only when equations/code, inputs and identification assumptions are adequate.
- [ ] **W4.10 · B:** Compare the proposed question with manufacturing/grid scopes before asserting separate contributions; do not merely reuse the same mechanism under three titles.
- [ ] **W4.11 · U:** Choose the study scope and record open scientific decisions. Keep the working title provisional; no novelty or superiority statement is approved by completing a checklist.

Proposed outcome measures: event recall, missed events, detection delay, point precision/recall/F1, average precision, false-alarm behavior and resource use. Adaptation-specific measures are defined in Stage 10. The practical improvement needed to justify added complexity remains an author decision before final tests; there is no invented target accuracy.

## 5. Freeze the evaluation and protect the final test

**Output:** versioned protocol/configuration, deviation ledger and test-access record. **Done when:** another person can determine every partition, score timestamp, threshold and metric denominator without seeing model performance.

- [ ] **W5.01 · A:** Map each received normal recording into fit, model-selection, threshold-calibration and held-out-normal partitions by chronological boundaries. Treat the existing 60/15/15/10 proposal as provisional until metadata supports it.
- [ ] **W5.02 · A:** Reserve the official attack recordings for final scoring; record any prior inspection, including exposure before a redesign. A familiar public benchmark is not a globally unseen dataset.
- [ ] **W5.03 · B:** Define separate development and final stress-test scenarios/seeds if synthetic adaptation tests are needed; do not tune and report on the same perturbations.
- [ ] **W5.04 · A:** Define boundaries, gaps, warmup, lookback, target horizon and reset behavior before constructing windows. Never let a window cross partitions or missing time.
- [ ] **W5.05 · A:** Fit feature eligibility, scalers and imputation only on fit data. Specify causal missing-data handling and separate continuous-sensor aggregation from actuator/status aggregation.
- [ ] **W5.06 · B:** Confirm the proposed common five-second grid against actual cadence and timing needs. Decide how short attacks and incomplete bins are represented before looking at scores.
- [ ] **W5.07 · A:** Use endpoint-available scores and documented interval-overlap/OR labels on the chosen grid; never median attack labels or assign a future-computed score to an earlier time.
- [ ] **W5.08 · A:** Define one common eligibility mask from data availability and the maximum predeclared method support. Record discarded coverage; never drop hard examples based on prediction error.
- [ ] **W5.09 · B:** Decide the normal-only hyperparameter/checkpoint objectives and equal search budgets. No attack-F1 selection is allowed without separately designated development attacks; none currently exist.
- [ ] **W5.10 · B:** Choose the calibration rule and strict comparison semantics. The proposed 99.5th normal-score percentile is a starting proposal, not a guaranteed real false-alarm budget.
- [ ] **W5.11 · A:** Specify alarm episodes, boundary/gap resets, hysteresis/cooldown if any, and observed false alarms per eligible normal hour; also report normal point exceedance and alarm duration.
- [ ] **W5.12 · A:** Define primary event recall, exact attack endpoints, overlapping-event policy and zero-opportunity events. Report misses and coverage; no hidden grace period or point adjustment.
- [ ] **W5.13 · A:** Define detection delay from event start to an eligible new alarm, including aggregation latency. Persistent alarms, misses and post-event detections need separate handling.
- [ ] **W5.14 · A:** Name point/ranking metrics precisely: FPR is FP/(FP+TN); average precision differs from trapezoidal PR area. Specify undefined/empty-class outcomes and counts.
- [ ] **W5.15 · B:** Predeclare seeds, repeat counts, deterministic settings and uncertainty summaries. The existing seeds 0/1/2 are a proposal; three runs do not establish broad statistical certainty.
- [ ] **W5.16 · B:** Choose an appropriate uncertainty unit: attack event, independent run or time block where justified. Do not treat overlapping windows or millions of rows as independent experimental replications.
- [ ] **W5.17 · A:** Record all departures from each original paper in `docs/PROTOCOL_DEVIATIONS.md`, including split sizes, labels, thresholds and hardware adaptations.
- [ ] **W5.18 · B:** Freeze protocol version 1 before final tests. Record revisions made during development; any revision after final-test exposure requires an explicit exploratory/confirmation disposition.

**Final-test policy:** keep test labels outside all fitting, selection, gating and calibration interfaces. Also prevent unlabeled test measurements from influencing offline model selection. If final test performance has already informed a redesign, a rerun on the same files is not fresh confirmation: disclose exploration and obtain genuinely independent confirmation evidence, or limit the claim. Changing seeds does not undo test exposure.

## 6. Prepare the smallest useful software environment

**Requires:** a later implementation instruction. **Output:** an isolated harness, explicit dependencies and import/configuration checks. **Done when:** we can identify the interpreter and reproduce the software setup without changing another project.

- [ ] **W6.01 · A:** Recheck available Python, architecture, RAM and free disk. Use the historical machine audit as a lead, not live evidence.
- [ ] **W6.02 · A:** Inspect dependency constraints before selecting versions. The existing Python 3.11 harness proposal is subject to compatibility; avoid the system/base environment.
- [ ] **W6.03 · A:** Create `.venv/` from within `water/` after authorization. Record the exact command and interpreter path.
- [ ] **W6.04 · A:** Add only required packages; resolve macOS/ARM dependencies and make a platform-specific version lock. Use a separate method environment if requirements conflict.
- [ ] **W6.05 · A:** Add `pyproject.toml` and a small `src/water_twin/` package. Start with data, split, preprocessing, calibration, metric and run-record modules; no application UI is needed.
- [ ] **W6.06 · A:** Separate dataset, protocol and method configs. Keep credentials/private paths outside tracked config; validate required fields before a run.
- [ ] **W6.07 · A:** Establish a run ID and manifest containing command, working directory, seeds, dependencies, hardware, code revisions/patches and data/config hashes.
- [ ] **W6.08 · A:** Store runtime outputs in ignored `experiments/runs/<run_id>/`; record safe summaries in documents. Do not upload raw records in logs or error reports.
- [ ] **W6.09 · A:** Write tiny hand-authored fixtures under `tests/fixtures/synthetic/`; mark them synthetic in metadata. Make tests run without private data or network access.
- [ ] **W6.10 · A:** Record actual setup commands and their outcomes. A proposed command in this roadmap is not an executable script or a passed test.

Proposed environment command, **not run here**, from `water/`: `/opt/homebrew/bin/python3.11 -m venv .venv`. Recheck that interpreter before use. Actual model entry commands cannot be finalized until the adapter exists; do not launch upstream dataset scripts blindly.

## 7. Make the data and evaluation code trustworthy before model training

**Output:** executable tests with recorded outcomes plus a local data-integrity report. **Done when:** the required invariants pass, with no benchmark-performance claim from software tests.

At this stage, checkpoint-independence and causal-scoring tests exercise the harness and synthetic test adapters. They do not establish the correctness of a model that is not integrated yet. Repeat the relevant checks against each real adapter in Stages 8–10 before final evaluation.

- [ ] **W7.01 · A:** Implement read-only loaders for the actual formats; test headers/sheets, whitespace, numeric parsing, missing markers and unknown labels.
- [ ] **W7.02 · A:** Test timestamp parsing with ambiguous day/month examples, duplicates, regressions and gaps. Fail clearly or apply the declared policy; never silently repair time.
- [ ] **W7.03 · A:** Track row IDs through trimming, aggregation and windows. Test a first-row label mismatch explicitly.
- [ ] **W7.04 · A:** Use a one-sample synthetic attack to verify that common-bin OR labels preserve it. Test exact bin and event endpoints.
- [ ] **W7.05 · A:** Assert disjoint ordered fit/selection/calibration/test IDs and reject windows crossing a partition or gap.
- [ ] **W7.06 · A:** Modify synthetic held-out values/labels and confirm offline fitted preprocessing, chosen checkpoint and initial threshold do not change.
- [ ] **W7.07 · A:** Test tied calibration scores, quantile method and `score > threshold`. Verify training/calibration interfaces cannot accept test-label arrays.
- [ ] **W7.08 · A:** Check a known confusion matrix: synthetic truth `[0,0,1,1]` and prediction `[0,1,1,0]` give TP=FP=FN=TN=1. Test no alarms, all-normal, all-attack, masks and empty input too.
- [ ] **W7.09 · A:** Test missed events, existing alarms at attack onset, new alarms, overlap policy, short zero-opportunity events and reset after a gap.
- [ ] **W7.10 · A:** Confirm delay uses timestamps and includes bin latency. Verify missing time does not inflate normal exposure.
- [ ] **W7.11 · A:** Check ranking metrics against a named library on known synthetic scores; do not implement maximum-test-F1 as reported operational F1.
- [ ] **W7.12 · A:** Test prefix causality: later observations cannot change earlier outputs; prediction occurs before adaptation.
- [ ] **W7.13 · A:** Make absent dataset/split/config/revision metadata mark a run incomplete; verify raw hashes remain unchanged after opt-in local integration tests.
- [ ] **W7.14 · B:** Review the test report, known limitations and data dictionary. Fix failures before baseline training; repeat tests only when changes or unresolved concerns justify it.

## 8. Reproduce CAROTS on development data first

**Output:** pinned adapter/patches, fidelity checklist, development report and measured resource estimate. **Done when:** the method runs under the declared protocol and deviations are documented. This is not yet a final benchmark table.

- [x] **W8.01 · A:** Obtain pinned author source with license and source URL. The requested pack uses a selective CAROTS snapshot under `baselines/carots/vendor/author_code/`, not a full Git clone; 57 code/support files and 16 separate water artifacts are identified in the manifest. This does not complete environment or execution checks.
- [ ] **W8.02 · A:** Inspect imports, shell scripts, device assumptions, downloads and output paths before executing anything. Never let upstream conversion caches write into raw storage.
- [ ] **W8.03 · A:** Map the causal-discovery, contrastive-learning, forecasting and scoring stages to the paper; identify every checkpoint and dependency between stages.
- [ ] **W8.04 · A:** Verify the suspected first-row alignment, gap and factor-five aggregation issues with fixtures/integration checks; distinguish confirmed bugs from audit concerns.
- [ ] **W8.05 · A:** Reject `TRAIN_RATIO >= 1` test-as-validation behavior; verify cached splits cannot reintroduce it.
- [ ] **W8.06 · A:** Replace the test-label threshold selector **and** separate maximum-F1 reporting path with our frozen calibration/evaluator. Keep original algorithms and protocol deviations traceable.
- [ ] **W8.07 · A:** Establish a CPU correctness path before optional device acceleration. Audit CUDA-only operations and test any MPS change; do not assume Apple GPU compatibility.
- [ ] **W8.08 · B:** Prepare a concrete pilot config: normal-data subset, exact stages, seed, epoch/iteration limits, threads, outputs, memory cap and hard timeout. A one-epoch stage does not imply the entire multi-stage method completed.
- [ ] **W8.09 · B:** Obtain a scoped pilot instruction before execution. The current proposal is one seed and a CPU ceiling of 10 wall-clock minutes; it is not permission or an estimated completion time.
- [ ] **W8.10 · A:** Execute the authorized pilot with progress/resource logging. Record timeout, crash, nonfinite score, label mismatch or raw-write attempt; do not silently retry or call incomplete training successful.
- [ ] **W8.11 · A:** Inspect development loss, score finiteness, deterministic alignment and checkpoint selection. Use normal development/synthetic checks, not held-out attack outcomes.
- [ ] **W8.12 · A:** Measure training/inference time and memory; estimate full-run resources with uncertainty. Recheck disk for checkpoints and scores.
- [ ] **W8.13 · B:** Choose a feasible full development run budget, then obtain approval for lengthy/paid work. If local CPU is impractical, prepare options; do not rent compute or upload data automatically.
- [ ] **W8.14 · A:** Run and retain both CAROTS full and no-ensemble variants as predeclared; share intermediate computation only when algorithmically valid and recorded.
- [ ] **W8.15 · B:** Write `docs/BASELINE_DEVELOPMENT_REPORT.md`: what was reproduced, what changed, which checks passed, unresolved limitations and measured costs. Label it author code under a modified protocol.
- [ ] **W8.16 · A:** Run the relevant Stage 7 leakage, checkpoint-selection, timestamp/score alignment and causality checks against the integrated CAROTS adapter, not only the synthetic harness. Record any failure before final evaluation.

**If blocked:** missing dependencies/code or unacceptable runtime triggers a documented feasibility decision. Do not replace CAROTS with a homemade imitation while calling it a faithful reproduction. Adding an easier control does not remove the need for a justified recent comparator.

## 9. Establish a fixed digital-twin reference

**Output:** a documented fixed-twin implementation and development validation. **Done when:** the predicted state/measurement, identification procedure, residual and decision rule can be traced to equations and inputs.

Here, **fixed** means the specified model parameters, residual reference and initial decision rule are not learned from the evaluation stream. State estimates may still evolve under the specified filter. List exactly which quantities are frozen, how state is initialized/reset at recording boundaries and gaps, and how suspect/missing observations affect state assimilation; frozen parameters alone do not prevent state contamination.

- [ ] **W9.01 · B:** Decide whether IT-DT is sufficiently specified to reimplement, whether verified author artifacts resolve another candidate, or whether scope must change. Record why.
- [ ] **W9.02 · A:** For a manuscript-based implementation, extract the equations, state/input/output definitions, identification assumptions, dimensions and all missing choices into `docs/TWIN_SPECIFICATION.md`.
- [ ] **W9.03 · B:** Choose model order, process/measurement-noise treatment, residual reference, monitoring window and stability constraints using fit/selection data only; record deviations rather than attributing our choices to the paper.
- [ ] **W9.04 · A:** Build synthetic systems with known behavior to check matrix dimensions, residual computation, covariance conditioning and numerical stability.
- [ ] **W9.05 · A:** Test score causality and pre-update versus post-update residuals; a filter must not silently remove an attack's evidence before scoring.
- [ ] **W9.06 · A:** Fit separate models for SWaT and WADI; record feature mappings and physical metadata. This is not training on SWaT and transferring a model to WADI.
- [ ] **W9.07 · A:** Assess normal-development predictions, residual behavior and model mismatch. Describe violated distribution assumptions rather than assuming them true.
- [ ] **W9.08 · B:** Compare against a simple sanity control where useful, and explain what the twin adds. A simple control is not automatically a recent published comparator.
- [ ] **W9.09 · A:** Apply the same test-independent calibration, score grid and coverage policy; document any extra physical information given to the twin.
- [ ] **W9.10 · B:** Write the fixed-twin development report and finalize its reproduction/reimplementation label. Keep final attack-test evaluation closed.
- [ ] **W9.11 · A:** Repeat the applicable Stage 7 isolation, calibration, state-reset, score-alignment and prefix-causality checks against the integrated fixed-twin adapter.

## 10. Design the smallest defensible adaptation experiment

**Output:** a chosen mechanism specification and predeclared experiment matrix, not a claimed improvement. **Done when:** all variants, information permissions, tuning budgets and evidence limitations are fixed before final evaluation.

- [ ] **W10.01 · B:** Use development evidence to state one failure mode worth investigating; do not manufacture a weakness solely to favor our proposal.
- [ ] **W10.02 · B:** Revisit closest prior art. Write what is already known and the specific unresolved assumption, keeping novelty provisional.
- [ ] **W10.03 · U:** Choose the protected update target and candidate mechanism. The reference/adaptive pair is a proposal, not a compulsory architecture.
- [ ] **W10.04 · B:** Specify exactly what the gate sees at time t and which evidence is independent of potentially corrupted measurements. Record unidentifiable cases.
- [ ] **W10.05 · A:** Write time-ordered pseudocode: predict → score/alarm → assess update admission → update eligible state. Define whether state assimilation itself is gated and how it differs from parameter/calibration updates.
- [ ] **W10.06 · B:** Define adaptation rate, warmup, quarantine, freeze, rollback and resumption rules only if the chosen mechanism uses them. Prevent future labels or future observations from certifying a window.
- [ ] **W10.07 · A:** Specify candidate controls: fixed twin; ungated adaptive twin; guarded twin; guarded twin without the reference component; and the frozen CAROTS variants.
- [ ] **W10.08 · B:** Hold capacity, features, calibration access and tuning budgets comparable. Add a control for extra model capacity if a second model could explain gains.
- [ ] **W10.09 · A:** Create a scenario register separating original benchmark recordings, verified legitimate-change evidence, synthetic measurement shifts and synthetic contamination. Record source/seed/timing/severity and whether physics has been validated.
- [ ] **W10.10 · A:** Keep synthetic modifications in derived storage and preserve original raw data. Avoid choosing perturbations after seeing which ones favor the gate.
- [ ] **W10.11 · B:** Predeclare stress-test development and final scenario sets, corruption budgets, duration ranges, clean adaptation periods and recovery periods.
- [ ] **W10.12 · B:** Define contaminated-update acceptance as accepted corrupted eligible updates divided by corrupted eligible update opportunities; also report rejected clean updates and update volume so “never adapt” is not mistaken for success.
- [ ] **W10.13 · B:** Define recovery operationally: which metric returns to which development-chosen bound for how long, from which start time. Treat failure to recover by recording end as censored/unrecovered, not zero recovery time.
- [ ] **W10.14 · A:** Test label independence, score-before-update, frozen reference parameters, causal buffering and exact rollback/reset behavior with synthetic fixtures against the actual adaptive adapters. Repeat applicable Stage 7 invariants; harness-only checks are insufficient.
- [ ] **W10.15 · B:** Tune only on permitted development evidence and record all trials, including failed variants. Do not select a final architecture using held-out test attacks.
- [ ] **W10.16 · U:** Decide whether the evidence supports continuing with the candidate question, narrowing it, or reporting a careful negative study. Do not force the original title to survive contradictory evidence.

The main hypothesis is a trade-off: adapt usefully to supported changes while limiting contaminated learning. A gate that rejects everything may preserve an old model yet fail the adaptation objective; a gate that accepts everything may reduce alarms by learning attacks. Both behaviors need explicit controls and measurements.

## 11. Freeze, execute and audit the final comparisons

**Output:** immutable run records and a complete result set for both datasets. **Done when:** every planned comparison has a result or an explained failure and the analysis can be regenerated.

- [ ] **W11.01 · B:** Review all open protocol/specification decisions and resolve them before scoring final attacks. Save a dated freeze record, configs, code revisions/patches and test-access history.
- [ ] **W11.02 · A:** Build the run matrix: dataset × method/variant × seed, plus separately identified stress scenarios. Separate deterministic repeats from stochastic training repeats.
- [ ] **W11.03 · B:** Set time, memory, disk, failure and restart budgets from pilot observations. Get explicit approval for lengthy or paid runs and any new external data transfer.
- [ ] **W11.04 · A:** Recheck required correctness tests after final code changes, resolve dependency locks and verify raw/split hashes. Record dirty state or make an authorized local revision; do not rely on an unrecorded working tree.
- [ ] **W11.05 · A:** Train only on permitted partitions, choose checkpoints on designated development data, and calibrate on designated normal calibration data. Persist these choices before test scoring.
- [ ] **W11.06 · A:** Schedule substantial runs sequentially on the shared machine. Log command, working directory, progress, hardware, seeds, versions, start/end times and resource use.
- [ ] **W11.07 · A:** Generate causal test scores without access to attack labels in the detector/gate. Keep outputs and sensitive logs local.
- [ ] **W11.08 · A:** Join scores to labels only in the final evaluator; verify timestamp alignment and the common mask. Log test unsealing and scoring.
- [ ] **W11.09 · A:** Report every predeclared variant/seed, failures and excluded coverage with reasons. Do not retain only the best run or the more favorable dataset.
- [ ] **W11.10 · B:** Inspect final failures to understand limitations. Any resulting redesign belongs to a disclosed new exploratory iteration; it cannot reuse this test as untouched confirmation.
- [ ] **W11.11 · A:** Regenerate tables from stored outputs/configs, not manual spreadsheet edits. Confirm denominators, alarm episodes and event delays match the frozen definitions.
- [ ] **W11.12 · B:** Classify each result as original benchmark, synthetic stress test, development diagnostic or published reference. Keep the tables distinct.

## 12. Interpret the evidence and write a paper you can defend

**Output:** a traceable draft with limitations and no unsupported results. **Done when:** the researcher understands each contribution claim and can point to its evidence.

- [ ] **W12.01 · B:** Prepare per-dataset tables with all planned variants and seed summaries. Include false alarms, missed events, delay and cost alongside detection metrics.
- [ ] **W12.02 · B:** Explain uncertainty without treating correlated samples as independent. If too few independent events/regimes exist for a strong inferential claim, report descriptive evidence and the limitation.
- [ ] **W12.03 · B:** Inspect ablations: determine whether any gain comes from the gate, reference, extra capacity, information or calibration. Preserve negative/ambiguous results.
- [ ] **W12.04 · B:** Check the trade-off against the predeclared practical criterion; do not move the success criterion to whichever metric improved.
- [ ] **W12.05 · A:** Create publication figures from scripts with units, sample/event denominators and legends. Export standalone plots; do not draw scientific curves from invented values.
- [ ] **W12.06 · B:** Build `manuscript/CLAIM_EVIDENCE.md`: each claim links to a source passage or run/config/result. Mark inference and untested assumptions separately.
- [ ] **W12.07 · U:** Decide the supported contribution in your own words. It may be a limited improvement, a failure analysis or a reproducibility finding; publication is not guaranteed.
- [ ] **W12.08 · B:** Choose a paper outline appropriate to the actual contribution: introduction, related work, system/threat model, method, evaluation, results, discussion/limitations and conclusion.
- [ ] **W12.09 · B:** Write methods from actual implementation, and results from retained outputs. Start background/reading notes earlier; do not fill a results section before experiments.
- [ ] **W12.10 · B:** Explain common-protocol deviations and any independent reimplementation, not just architecture details. Include data, code and environment availability accurately.
- [ ] **W12.11 · B:** Discuss dataset realism, legitimate-change evidence, trusted-input assumptions, test exposure, system count, resource limits and failure cases.
- [ ] **W12.12 · A:** Check every citation against its supporting passage, version and bibliographic record. Use quotations sparingly and follow the eventual venue's actual style.
- [ ] **W12.13 · U:** Review and rewrite the reasoning you cannot explain; confirm actual authorship contributions/order and any required AI-use disclosure.
- [ ] **W12.14 · B:** Finalize the title and abstract only when they accurately describe the scope, method and measured evidence. Do not claim live deployment or physical mitigation from offline replay.

## 13. Review, select a venue and handle submission properly

**Output:** an author-approved submission package and a clear record of decisions. **Done when:** the requested submission/revision milestone is completed; acceptance is outside our control.

- [ ] **W13.01 · B:** Shortlist venues after contribution type and quality are clear. Check current official scope, article type, review model, deadlines, page limits and fees; do not assume a prestigious title fits.
- [ ] **W13.02 · U:** Choose the venue and any publication budget. No payment, submission or external contact follows automatically from this roadmap.
- [ ] **W13.03 · B:** Use the research skill's relevant review/citation guidance against the actual draft and chosen criteria. An AI review is not completed journal peer review.
- [ ] **W13.04 · B:** Resolve correctness and evidence problems; preserve an issue/revision record and justify any acknowledged limitation.
- [ ] **W13.05 · A:** Check template, figure readability, references, supplementary material, anonymity if required, author details and required declarations.
- [ ] **W13.06 · B:** Inspect every proposed public artifact for restricted data, private paths, credentials, data-bearing logs and third-party licensing obligations. The private workspace is not a publication-ready artifact by default.
- [ ] **W13.07 · U:** Review the final package and explicitly authorize submission/publication. Archive the exact submitted files and checksums locally.
- [ ] **W13.08 · B:** If reviews arrive, map each request to evidence, proposed response and required work. Obtain decisions for disputed changes; do not fabricate experiments to satisfy a reviewer.
- [ ] **W13.09 · B:** Treat additional experiments as logged protocol extensions, with test-exposure limitations and compute approval where required. Update methods/results consistently.
- [ ] **W13.10 · U:** After publication, meet the applicable provider attribution/notification obligations and any approved artifact-release commitments. External notifications still require authorization.

## First five sessions, without waiting for everything to be solved

These are bounded work packages, not five days or automatic authorizations.

| Session | Work | Concrete stopping point |
|---|---|---|
| A | W0.01–W0.08 and W1.01–W1.05 | Researcher understands the task; access request is submitted by the researcher or an accurately recorded pending draft exists |
| B | W2.01–W2.09 | CAROTS source notes and first paper-to-code checklist; unclear equations/protocol choices listed |
| C | W2.10–W2.16 and W4.01–W4.06 | Twin/prior-art reading notes; specific plan for legitimate-change evidence or a narrowed claim |
| D | W3 if files arrive; otherwise finish W2/code audit | Verified release inventory, or an explicit unresolved access status; no invented data properties |
| E | W4–W5 decisions, then scoped W6–W7 implementation only when requested | A concrete evaluation specification and next software task; no automatic training |

**Our immediate next action:** use the [completed assistant study guide](PAPER_STUDY_GUIDE.md) and [CAROTS code map](../baselines/carots/METHOD_TO_CODE.md) to develop a researcher-owned explanation, then prepare a bounded correction/deviation specification covering augmentation/loss semantics, data alignment, calibration and checkpoint selection. Record reading in [READING_RECORD.md](../papers/notes/READING_RECORD.md). The official dataset request is submitted; await the provider response and verify authorized receipt separately. The resource-acquisition history in WATER-007 and later study artifacts do not complete researcher reading or model execution. Both twin candidates remain on numerical hold.

## Decisions we will ask for when the evidence is ready

| Decision | Why it belongs to the researcher | When |
|---|---|---|
| Submit access form / contact provider | Uses identity, consent and external communication | Stage 1 |
| Final question, trusted inputs and update target | Determines what the study claims | Stages 4 and 10 |
| Full-run budget / paid compute | Commits time or money | After measured pilots |
| Contribution, authorship and venue | Academic responsibility and publication scope | Stages 12–13 |
| Publishing or submitting artifacts | Releases research and may trigger data/license obligations | Stage 13 |

Routine source reading, document updates and authorized local implementation do not need repeated approval. Preserve earlier authorization within its actual scope. The earlier GitHub instruction covered one initial push; this roadmap session does not automatically push new files.

## End every work session this way

1. Record the completed task IDs, artifacts, exact commands where relevant, observed checks, failures and decisions in [WORK_LOG.md](WORK_LOG.md).
2. Tick only supported completed items here and update [STATUS.md](../STATUS.md), including the exact next bounded task and remaining blockers.
3. Add a reusable lesson to the [shared playbook](../../docs/RESEARCH_PLAYBOOK.md) when warranted; do not copy water's datasets or completion status into the other projects.
4. Keep a reproducible local revision/patch record for experiments. Push, upload, send or publish only within the user's authorization.

### Skill use and limits

Applied the installed [skill router](../../.agents/skills/academic-research-suite/SKILL.md), [experiment planning workflow](../../.agents/skills/academic-research-suite/ars/experiment-agent/WORKFLOW.md), [code experiment-plan template](../../.agents/skills/academic-research-suite/ars/experiment-agent/templates/code_experiment_plan.md), and [paper-planning readiness guidance](../../.agents/skills/academic-research-suite/ars/academic-paper/references/plan_mode_protocol.md). Existing project decisions prepopulate the question/design discussion; unresolved choices remain proposals for the researcher. No chapter negotiation, author contribution decision, result-validation mode, or full pipeline was claimed as executed.

The plan covers objective/hypothesis, setup, inputs, expected outputs, pilot monitoring, metrics, controls and analysis. Exact executable commands, resource limits and success criteria must be completed for each later run. The installed package remains unchanged, and no model/runtime switch, cross-provider service, paid automation or external manuscript upload was used.
