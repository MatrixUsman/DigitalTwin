# Protection of the final CASPER evaluation

## Material Passport

- Project / owner: manufacturing / Haiqa Mushtaq.
- Origin: academic-research-suite, experiment-agent, bounded **plan** workflow.
- Date: 16 October 2026.
- Version: `final-test-protection-v0.1`.
- Verification status: **prospective design; no executable protection, model freeze or final evaluation established**.
- Scope: the normal-only right-arm study in the [question and threat model](RESEARCH_QUESTION_AND_THREAT_MODEL.md) and [annotation/feature/split contract](ANNOTATION_FEATURE_SPLIT_CONTRACT.md).

This document defines what must remain outside model development and what must be recorded before final replay. It does not authorize training, introduce an access-control system, certify a blind study or claim a result. The user's current request authorizes this design step. Later execution must fit its separately recorded scope and resource budget; paid compute, lengthy training and publication retain the existing approval requirements.

## What is protected, and what has already been inspected

The received original-CASPER-v3 `right_arm.csv` has SHA-256 `181662e25de09c1f4ed05e0877a65c40225752d6f54575ddb1cdf8a0cf29a334`. All ranges below count data rows from zero and exclude the ending row.

| Partition | Range | Use before final release |
|---|---|---|
| Training | `[0, 540002)` | Fit permitted transforms, references and parameters |
| Normal development | `[540002, 702002)` | Compare only the finite normal-only configuration choices and selection objective declared before the pilot |
| Normal calibration | `[702002, 864003)` | Determine each already selected model's alarm threshold; not rank models, change features or select a seed |
| Protected normal | `[864003, 1080004)` | No outcome-driven development; final normal alarm burden and coverage only |
| Protected intervention/recovery | `[1080004, 1762650)` | No outcome-driven development; final schedule-agreement and event reporting only |

The two protected slices are **one continuous final replay `[864003, 1762650)`**, with dynamic state initialized at its start and no reset at schedule transitions. The earlier normal slice is not a spare validation set or a source of threshold adjustment. All later schedule-zero recovery/inter-event observations remain protected too; being labelled zero does not make them training data.

The data is public, and the full original CSV already exists in a shared local directory. Previous audits inspected file identity, schema validity, row counts, flags, timestamps, gap locations and selected boundary records. The paper/code study also inspected author-reported results and preprocessing. These disclosures matter: this is a **prospectively protected evaluation after dataset/metadata and literature inspection**, not a wholly unseen dataset, blinded experiment or external replication. No model scores or our benchmark outcomes have been produced. A file-system permission boundary or independent custodian has not been implemented.

From this design onward, do not inspect protected joint-value plots, distributions, recurrence structure, feature correlations, prediction errors, scores, alarm behavior or model comparisons to make development choices. Do not use them indirectly through unsupervised fitting, full-trace normalization, task segmentation, clustering, threshold diagnostics or attack-specific synthetic generators. Prior metadata observations are disclosed; they are not permission to continue searching the protected values. An accidental access must be recorded with what became visible, to whom, and which later decisions could be affected.

## Two decision boundaries before final replay

**Model-selection freeze, before calibration:** specify the scientific contrasts and every method/ablation to be reported; permitted inputs; finite candidate configurations and normal-only selection objective; checkpoint/tie rules; fixed seeds; preprocessing; model histories and initialization; score direction; gap and missing-score handling; and the common reporting definitions. Select configurations using training/development only. Preserve the candidate table, including failed candidates and selection reasons. No model, seed or ablation is selected because of its calibration alarm behavior.

**Final-evaluation freeze, after calibration:** retain each selected fitted checkpoint/reference and preprocessing artifact, the exact calibration inputs/eligible endpoints, the declared threshold computation and its resulting threshold. Calibration runs only that computation for the already selected models. Its outputs do not permit a new search over features, score combinations, seeds, persistence rules, percentiles or preferred models. Code that cannot produce a valid threshold is a recorded failure, not a reason to select a more favorable unregistered variant.

The current data contract uses nearest-rank 99th-percentile calibration and strict `score > threshold`. The applicable versioned evaluation specification must retain one explicit rule, including ties, invalid scores and empty calibration. Fixing an implementation error requires a documented correction, synthetic verification and new artifact identities; it is not a license to use calibration as development. If choices are changed in response to calibration behavior, disclose the compromised separation and design a valid new calibration step before any final claim. Do not silently promote the protected normal block into its place.

The final freeze is **pending today**. A versioned plan/configuration is not a fitted-model freeze. In a machine-readable template, `model_selection_frozen_at`, `calibration_completed_at`, `final_freeze_at`, `campaign_started_at`, `first_outcome_revealed_at` and final artifact/result hashes remain `null` until the corresponding actions actually occur. An empty model/artifact/run list signifies unfinished prerequisites, not a valid zero-model campaign. A predeclared seed list is a planned setting, not proof that seeded artifacts exist. No person's approval or human-read attestation may be inferred from these documents.

## Required record before releasing final inputs

The operator records a single final-campaign manifest that resolves all of the following. A hash must refer to existing bytes, not an intended path.

1. **Question and analysis:** protocol version/hash, declared primary contrast, complete methods/ablations, metrics and reporting populations, missing-score/coverage rules, warmup and gap behavior, and all planned secondary analyses. The model-specific definition must distinguish causal state correction from forbidden parameter/threshold updates.
2. **Data:** raw-file hash, annotation and feature-contract hashes, split/mask identities and time-unit convention. Tests verify that detector inputs exclude schedule flags, absolute timestamps, row/event identifiers, future values and other prohibited channels. Evaluator coordinates may be retained separately for joining predictions to outcomes.
3. **Model selection:** exact finite search definition and normal-only objective, candidate outcomes, selected configurations/checkpoints, declared seeds and tie handling. If a matched ablation shares parameters, identify those bytes and the precise change. Otherwise identify separate fitting and calibration artifacts.
4. **Frozen artifacts:** fitted transforms, references/checkpoints, calibration receipt and threshold for every admitted model/seed, each hashed. Neither benchmark predictions nor test labels are used to create these artifacts.
5. **Executable provenance:** our code revision and dirty patch, upstream revisions/designations/licenses and any patches, evaluator revision, interpreter/dependency lock, hardware, commands, working directory, operator, resource limits and logs. A budget or permission record describes actual authorized scope; it is not fabricated by a template.
6. **Verification:** passing offline synthetic loader/alignment/leakage/metric tests and a bounded normal-only implementation pilot, with actual receipt hashes. Synthetic fixtures remain labelled synthetic. A metadata check is not a passing loader or metric test. Numerical failures, unequal coverage and unresolved scientific inputs cannot be hidden by declaring the checklist complete.

These prerequisites are not yet met. Exact model definitions, executable interfaces and fitted artifacts remain implementation work. No test-input release is recorded in this planning task. After calibration, do not refit on training plus development and reuse the old thresholds. Any such refit strategy would require a revised, predetermined protocol before calibration; it is not included in the current plan.

## Developer and evaluator responsibilities

Use a developer-facing API that supplies permitted observations and local stream-time increments only. Development functions receive explicit training/development ranges; calibration receives only its own range and frozen model artifacts. Runtime models must not receive a path that they can use to reopen the source CSV or obtain test labels. This is a required interface design, not an existing security sandbox.

An evaluator-controlled loader owns source row numbers, full timestamps, schedule flags and reporting boundaries. It runs the final stream, records aligned scores/decisions/unknowns, then joins them to annotations for scoring. Reset behavior follows stream breaks and the declared start, never labels. Predictions should be emitted before current observations update causal state. Fitted transforms, references, model parameters and thresholds remain unchanged throughout final replay.

Use narrow interfaces and synthetic tests that reject extra label/identifier fields. The evaluator records mismatched row counts, missing/nonfinite scores and artifact changes as failures. Hash checks and API separation help reveal mistakes; they do not stop a researcher with local file access from reading public data. Ideally another team member performs the release/report step, but a separate person is not guaranteed here and must not be claimed unless it happens. If one operator does both roles, disclose that fact.

## One declared campaign and a complete report

Run the frozen list of methods and seeds as one campaign. Report every declared method/seed, including technical failures, coverage failures and negative results. Do not inspect the first method's final curve to redesign the next one. Do not pick the best test seed, substitute a late ablation or decide which baseline to omit after seeing its performance.

The proposed bounded normal-only pilot uses seed **42**, with training/development access only. Final stochastic comparisons use **17, 42 and 2026**, paired between variants where applicable; deterministic controls run once. These choices are made before outcomes. Report every seed rather than a best seed or an outcome-selected ensemble. The campaign is one logical evaluation with a common frozen plan, not necessarily one process or simultaneous jobs. Its primary contrast is assessed jointly through the declared mean F1 difference, normal point-exceedance difference and normal episode-rate difference; it does not create an after-the-fact scalar winner or significance test.

Save and hash every declared run's score artifacts in ignored experiment storage **before joining final labels or releasing scientific outcomes**. Each registered run must reach a recorded terminal state. A failed run contributes its failure status, available artifacts and coverage record; missing failed-run scores must not prevent a complete failure report or justify silently removing that run. Prepare the joint report only after the campaign's complete status/artifact matrix is recorded. Until then, monitor technical completion/resource use rather than scientific outcomes. This delayed reveal is a planned procedure, not a confidentiality guarantee. If any scores, metrics or diagnostic plots become visible early, record the first reveal and treat subsequent decisions as post-reveal. Failures remain in the report instead of waiting for only favorable runs to finish.

The joint report includes the protected-normal and mixed slices, counts/coverage, all eight event outcomes and permitted delay definitions, plus the full registered model/seed list. Repeated seeds characterize computation on the same recording; they are not independent robots, acquisitions or attacks. Do not manufacture row-independent confidence intervals or generalization claims. The single recording and prior public-source exposure constrain what a confirmatory comparison can establish even when the procedure is followed.

## Access ledger, retries and changes after reveal

Keep an append-only **logical** final-access ledger in ignored experiment storage, with safe summary hashes/provenance in the campaign manifest. Git or a checksum alone does not enforce append-only storage. Each entry should record UTC time, actor/role, purpose, partition, data/artifact hashes, command/code/environment, scope of values/outcomes actually exposed, success/failure, report visibility and deviations. Preserve failed outputs and links to earlier attempts. Prior dataset/metadata audits are recorded in the work log; they are not entries in an experiment ledger that did not yet exist. Today there are **no final-evaluation access entries**, and the ledger implementation is pending.

| Situation | Permitted interpretation and response |
|---|---|
| Storage/process failure before scientific outcomes become visible | Record the attempt; retry only the same frozen scientific specification after identifying the technical cause and respecting the existing execution/resource authorization. Preserve artifacts and state that it is a retry, not another independent test. |
| Partial outcomes became visible before a failure | Record that reveal. Unchanged continuation/retry can complete the predeclared campaign; no scientific choices may respond to what was seen. Report the exposure and failure. |
| Bug found after outcomes were revealed | Preserve original outputs and identify the error/affected results. Validate the correction with synthetic fixtures, version the patch, and document any rerun. A corrected same-holdout analysis is a disclosed correction, not a newly untouched confirmatory test. Reassess interpretation if the fix changes the scientific comparison. |
| Features, threshold rule, architecture, labels, split boundaries or preferred variants changed in response to final outcomes | Label the revised work exploratory. Freeze the new proposal and obtain an independent suitable acquisition/dataset for a new confirmatory claim; reusing or reshuffling this holdout does not restore independence. |
| Exact repeat of an already revealed campaign | A reproducibility/determinism check on the same recording, not a new independent validation. Record its relationship to the original campaign. |

Technical retries are not automatic permission for longer runs or extra compute. Conversely, writing this plan introduces no new permission requirement for ordinary document work or authorized synthetic checks. A final result may motivate a useful next study; it must not silently become development evidence while retaining an untouched-test label.

## Current state and next action

Protected ranges and governance are now defined prospectively. No model-selection freeze, calibration result, executable loader/evaluator, final campaign or test-performance report exists. The next bounded action is to implement and test input separation, chronology and metrics with synthetic fixtures, then specify the finite normal-only pilot and concrete model configurations. Keep final values and outcomes outside that work.
