# Manufacturing paper roadmap: evidence, experiments and submission

## Material Passport

- Project / owner: manufacturing / Haiqa Mushtaq; project ownership is not a final authorship decision.
- Updated: **17 October 2026, Asia/Karachi**.
- Origin: academic-research-suite planning guidance, current project records and two internal read-only status/dependency reviews.
- Version: `manufacturing-paper-roadmap-v0.1`.
- Status: **current lifecycle plan, grounded in completed artifacts; future work remains unexecuted**.

This is the main lifecycle roadmap for this paper. Use [STATUS.md](../STATUS.md) for the short current handoff and [WORK_LOG.md](WORK_LOG.md) for what actually happened. Earlier reproduction proposals remain useful historical/source notes; they do not override the selected right-arm study or the current software status. The frozen data/evaluation specifications retain their original bytes and planning-date readiness fields.

## Where we actually are

We have an audited dataset, selected feasibility question, defined evaluation protocol, **254 passing synthetic tests**, preserved pilot/control studies and a completed **normal-only empirical motion-observer validation**. Seven candidates each fitted 536,946 eligible targets and scored 160,472 development endpoints; velocity, a 32-bin template and AR(4) ridge 0.001 were selected. We have **not reproduced a paper baseline, calibrated a threshold or measured attack-detection performance**. See the [observer report](OBSERVER_VALIDATION_REPORT.md): all seven internal checks and 48 saved-artifact checks passed, while ordinary AR remains substantially stronger at one-step prediction. The physical-twin claim remains unsupported.

Working title: **“Correction Evidence in Robotic Motion Monitoring: A CASPER Case Study.”** It remains provisional and follows the [scope decision](CONTRIBUTION_AND_EVIDENCE_SCOPE.md). The question is:

> Does retaining measurement-correction evidence improve the empirical motion observer’s detection of recorded right-arm speed changes compared with its residual alone under the same normal-only calibration?

In everyday terms: compare the monitor's prediction error with the additional evidence in how a measurement changes its estimated phase. Both variants already use expected progression. Because measured velocity can retain speed mismatch after position alignment, do not assume synchronization hides the interventions. Conventional surprise/energy and velocity scores must test these alternative explanations.

The scope is one right-arm pick-and-place recording, with truthful telemetry/time assumed and command-path speed manipulation as the restricted threat. It does not cover a fully compromised controller, forged telemetry, legitimate changeovers, fault/attack attribution or live robot protection. See the [question and threat model](RESEARCH_QUESTION_AND_THREAT_MODEL.md).

| Stage | Current status | Evidence or unfinished part |
|---|---|---|
| 0. Workspace and records | Completed within setup scope | Independent project, instructions, local storage, logs and publication standards |
| 1. Researcher understanding | Partial | Lesson exists; researcher worksheet unanswered |
| 2. Literature and comparator admission | Decisions recorded; implementation gates remain | Two original learning manuscripts available/AI-audited; [explicit designations](COMPARATOR_ADMISSION.md); no admitted three-paper ranking |
| 3. Data identity and suitability | Completed audit, with scientific limitations | Original CASPER v3 received; hashes/schema/labels/clocks recorded |
| 4. Research question and threat model | Selected for feasibility | Novelty and twin usefulness unproved |
| 5. Evaluation rules | Defined | Actual model/checkpoint/threshold freeze not completed |
| 6. Loader and metric foundation | Implemented and tested | Expanded 254-test suite; loader exercised on complete training/development as well as the earlier pilot prefixes |
| 7. First control and bounded runner | Implemented and tested | Welford velocity control, supervision, access/provenance and failure checks |
| 8. Real-data feasibility pilot | Completed, one accepted attempt | 46,944 fitted / 18,472 scored; immutable reference; 8.626 s supervised wall, 27.94 MiB peak RSS |
| 9. Full normal-only controls | Completed for essential controls | Seven candidates; selected velocity, 32-bin template and AR(4) ridge 0.001; CNN deferred |
| 10. Observer and matched ablations | Completed within empirical-observer scope | 7/7 normal checks; prospective prediction/synchronization and uncertainty evaluated; physical-twin claim unsupported |
| 11. Contribution and evidence scope | Design decision complete; empirical contribution unproved | Narrow single-acquisition score audit; prior-art overlap, eleven-variant design and independent-source needs recorded |
| 12. Model-selection freeze | Partial; execution roster pending | Seven implemented variants; four required C/K/L/Rv extensions and actual complete run matrix pending |
| 13. Calibration and final-release preparation | Not done | No thresholds; final runner, ledger and actual freeze incomplete |
| 14. Protected final campaign | Not run | No final scores or outcomes |
| 15. Analysis and interpretation | Normal-only feasibility interpreted; final analysis pending | Observer limitations and strong simple predictors recorded; no attack outcomes |
| 16. Manuscript and reproducibility package | Not completed | Existing notes are source material, not a finished paper |
| 17. Venue review and submission | Not started | No selected journal, approved submission or acceptance |
| 18. Peer review and publication | Future, outcome uncertain | Depends on submission and editorial decisions |

There is no meaningful “percentage of paper completed” yet: an unresolved contribution or unsuitable comparison can change the remaining work substantially. No calendar completion or journal acceptance is promised.

## 0–1. Preserve the workspace and make the researchers able to explain the work

**Already done:** project separation, owner mapping, instructions, raw-data ignore rules, evidence records, beginner lesson and a local standard-library environment. No authorship order is inferred from folder ownership.

**Remaining checklist:**

- [ ] Read [the concepts lesson](RESEARCH_BASICS_LESSON.md) and answer [the worksheet](YOUR_STEP_0_NOTES.md) in the researcher's own words.
- [ ] Explain the difference between a twin, predictor, anomaly score, threshold, baseline and ablation.
- [ ] Explain why calibration is separate from model selection and final testing.
- [ ] Explain the exact threat restriction: a suspicious speed change does not prove malicious intent.
- [ ] Walk through one synthetic precision/recall/delay example and explain each denominator.
- [ ] Read CASPER's physical setup and model sections, then explain the input-to-score-to-alarm path without relying on generated prose.
- [ ] Start an actual contribution record: who reads, designs, codes, checks data, analyzes and writes. Agree authorship later from real contributions.

**Completion evidence:** researcher-authored notes and a reviewed explanation. Assistant-generated notes or an available PDF do not attest to human understanding.

## 2. Finish the literature audit and admit fair comparators

**Already done:** source collection and static method/code study; a pinned pack of source/configuration/author-result artifacts; detailed [paper-to-code traceability](PAPER_CODE_TRACEABILITY.md); [current comparator designations](COMPARATOR_ADMISSION.md). CASPER's corrected paper and TWINE's newly obtained accepted manuscript are available and AI-audited (**2/3 original learning papers**); researcher comprehension remains unassessed. Author graphs and tables are literature artifacts, not our reproduced results.

| Learning paper | What is available | What prevents current experimental admission |
|---|---|---|
| CASPER | Corrected full paper and author code studied | Separate external-IMU track held for code-use, threshold and run-correspondence gaps; an independently implemented CASPER-inspired controller CNN is a Group D design candidate, not a faithful reproduction |
| TWINE | Accepted manuscript obtained; section/code and reported-metric audit complete within stated coverage | Background only for Group D; supervised/random-row task and wider inputs are incompatible. Separate supervised track remains unadmitted; model/result correspondence remains unresolved |
| CatBoost on CASPER | Publication/abstract evidence, code and reported-output audit | Background only for Group D; full manuscript/provenance unresolved and target/modalities/preprocessing unsuitable for direct reuse. Separate supervised track unadmitted |

ModernTCN 2024 is a **conditional modified author-code transfer candidate** for a normal-only comparison after a causal/common-input adapter and tests. This is not evidence that its paper evaluated CASPER, nor an execution-ready or reproduced baseline. Follow the [admission decision](COMPARATOR_ADMISSION.md) for the justified comparison set and remaining gates.

**Remaining checklist:**

- [x] Obtain and audit TWINE's lawful institutional accepted manuscript; preserve the acquired version and result/code discrepancies.
- [ ] Resolve CatBoost's remaining manuscript gap if its separate study role warrants further work. Contact requires separately authorized outreach; absence of access is not evidence of a fake paper.
- [ ] Finish exact paper-section ↔ code-function ↔ configuration ↔ dataset/run correspondence.
- [ ] Resolve licenses/code-use terms and distinguish public availability from permission to reuse or redistribute.
- [ ] Search specifically for close work on task-phase synchronization, progression residuals, periodic-template alignment, prediction and anomaly preservation.
- [ ] Keep the current publication window **2023-10-16–2026-10-16** unless explicitly revising the search plan. Record any later literature update separately; older work can remain relevant background.
- [ ] For every proposed comparator, record release, features, labels, supervision, chronology, preprocessing, calibration, code revision and implementation designation.
- [x] Record honest designations for the original three learning papers, separating Group D from original-input and supervised tracks.
- [ ] Complete adapter/model validation and execution admission for selected independent or transfer comparators; do not convert design eligibility into completed reproduction.
- [ ] Extend the better-matched recent-method search where needed; do not fill three slots with scientifically unequal methods.

**Completion evidence:** an admission matrix with justified decisions and runnable/specifiable methods. Three downloaded papers are not three reproduced baselines, and three is not a scientific upper limit. Missing manuscripts do not block our independent simple-control pilot; they do block claims of reproducing those methods.

## 3–4. Keep the data identity, question and assumptions explicit

**Already done:** original CASPER v3 archive and five members received; six-file integrity checks; nested schema, labels, clocks, gap and annotation audits; selected right-arm source hash; twelve permitted q/qdot channels and relative time; exact eight recorded positive intervals. See the [identity register](DATASET_IDENTITY_REGISTER.md) and [data contract](ANNOTATION_FEATURE_SPLIT_CONTRACT.md).

Earlier audits did read raw records for identity/schema/annotation work. The later loader/metric implementation milestone used synthetic observations only. Do not describe the dataset as wholly unseen.

**Remaining checklist:**

- [x] Exercise the new loader on the authorized bounded normal prefixes during the pilot and verify exact support, without changing raw bytes.
- [ ] Preserve the clean-commissioning and truthful-monitor assumptions as assumptions, not discovered security properties.
- [ ] Keep recorded schedule flags separate from physical-onset or malicious-intent ground truth.
- [ ] Decide whether the available normal data support a meaningful nominal trajectory/progression model.
- [ ] Revisit the question before final testing if the normal-only feasibility evidence contradicts that representation.

**Completion evidence:** successful bounded real-data loading plus a documented scientific scope. Byte integrity alone does not validate the threat model or establish broad manufacturing generalization.

## 5–6. Preserve evaluation rules and build on the tested foundation

**Defined partitions:**

| Partition | Raw rows | Eligible endpoints | Use |
|---|---:|---:|---|
| Training | 540,002 | 536,946 | Fit permitted references/transforms/parameters |
| Normal development | 162,000 | 160,472 | Select finite declared configurations |
| Normal calibration | 162,001 | 160,473 | Set each frozen model's threshold only |
| Protected normal | 216,001 | 214,473 | Final normal alarm burden |
| Protected mixed | 682,646 | 682,646 | Final recorded interventions and recovery |

Final normal and mixed are one continuous replay. Warmup is 1,528 preceding observations; gaps and invalid inputs break continuity. Labels do not reset state. The [evaluation protocol](EVALUATION_PROTOCOL.md) and [metric definitions](METRIC_DEFINITIONS.md) fix exact row ranges, ties, missingness and event conventions.

**Implemented:** read-only loader; manifest-bound training/development wrapper; observation/evaluator separation; causal score/update coordinator; calibration/count/AP/episode/event/time primitives. The historical foundation passed 83 tests; the current observer/control/runner suite passes **254 tests**, with 40 source/configuration fingerprints verified. See the [observer report](OBSERVER_VALIDATION_REPORT.md) and [current test receipt summary](../experiments/SOFTWARE_TEST_REPORT_OBSERVER_V0.1.json).

**Remaining checklist:**

- [x] Add fitting, future-information and immutable-reference tests for velocity/template/AR; future models require their own tests.
- [x] Test the bounded supervisor and synthetic failure/abort records; the real pilot completed successfully.
- [ ] Implement production calibration/final admission, exact score artifacts and protected label-join/release path.
- [ ] Implement complete seed/run report assembly and actual resource instrumentation.
- [ ] Validate these additions before using them for claims. Do not treat existing synthetic tests as production evaluator admission.

The current wrapper intentionally blocks calibration and final observations. Public raw files remain accessible locally; this is procedural/interface protection, not an OS lock or blinded study.

## 7. First control and bounded supervisor — completed

The [pilot specification](BOUNDED_PILOT_PLAN.md) was implemented without changing its formula, subsets or limits. The [pilot report](PILOT_REPORT.md) records the implementation, 150 passing synthetic tests and actual execution.

- [x] Implement six-channel velocity mean and population variance using the declared streaming Welford calculation.
- [x] Implement the fixed maximum absolute standardized-deviation score.
- [x] Reject zero/nonfinite variance; do not introduce an unrecorded epsilon or discard a channel.
- [x] Test known synthetic statistics, constant channels, nonfinite inputs, complete score support and unchanged fitted parameters.
- [x] Ensure only eligible training-prefix observations fit the reference; development observations cannot update it.
- [x] Implement timeout, CPU, monitored-memory and output-size limits with explicit terminal failure records.
- [x] Test the supervisor on harmless synthetic workers that finish, fail or exceed a bound.
- [x] Resolve the exact interpreter, command, configuration hashes, output paths and run manifest.

**Completion evidence:** executable, tested control and runner with a concrete command. This stage is software work; it does not require an attack score or a claim that the method is a twin.

The 17 October literature follow-up verified the existing 150-test receipt and source identities without repeating tests or training. The completed stage does not need another pilot attempt.

## 8. Bounded normal-only feasibility pilot — completed

- [x] Verify raw source identity without inspecting protected feature distributions.
- [x] Fit on raw training prefix `[0,50000)`: **46,944 eligible observations**.
- [x] Score raw development prefix `[540002,560002)`: **18,472 eligible observations**.
- [x] Record source traversal separately from selected observations; do not borrow history across the development boundary.
- [x] Record all finite scores, coverage, reference hashes, timing, CPU, memory, output size and terminal status locally.
- [x] Enforce 600 seconds wall, 300 seconds CPU, 1 GiB monitored RSS, 50 MiB outputs and one deterministic attempt. Actual supervised wall 8.626 seconds, CPU 8.571 seconds, peak RSS 27.94 MiB, run outputs 1.93 MiB.
- [x] Do not calculate a threshold, attack F1/AP, final normal false alarms or event detection in this pilot.
Failure preservation and termination behavior were tested synthetically; the one real attempt succeeded. Any future retry or changed rule requires a separate declared scope. No attempt was repeated.

**Pass condition:** exact permitted fitting/scoring support, finite outputs, immutable reference and recorded completion within the declared limits. **What it proves:** machinery and resource feasibility. **What it does not prove:** attack detection, novelty or superiority. A subset-fit pilot artifact cannot be renamed a full-training final checkpoint.

## 9. Implement and validate the simple comparison methods — completed

- [x] Specify and fit the full-training velocity control.
- [x] Implement a frozen nominal periodic template with causal warmup alignment and fixed clock progression.
- [x] Implement channelwise autoregressive ridge prediction with past-only histories.
- [x] Define inputs, formulas, training-only transforms, history, initialization, score direction and failures in the [plan](SIMPLE_CONTROLS_PLAN.md).
- [x] Predeclare one velocity, two template and four AR configurations, normal-development MSE selection and deterministic ties.
- [x] Pass synthetic numerical, causal, leakage and saved-artifact tests.
- [x] Fit all seven using 536,946 eligible training targets and score all 160,472 normal-development endpoints without changing fitted references.
- [x] Retain every candidate and select velocity, template32 and AR(4)/ridge0.001 without development refitting.
- [x] Save [selected artifacts and hashes](../experiments/SELECTED_CONTROLS_V0.1.json) and measure resources: 51.377 s wall, 147.48 MiB peak RSS, 17.53 MiB output.

**Completion evidence:** [control-study report](CONTROL_STUDY_REPORT.md), 205 passing tests and an independent 28-check post-run audit. The compact CNN is optional and deferred; no recent paper method was reproduced. Selected controls are ready to supply later calibration, but the complete twin/ablation roster and calibration runner are not ready. Normal prediction loss does not establish attack sensitivity.

## 10. Specify and validate the observer and ablations — completed in narrow scope

- [x] Define the physical quantity/state represented and its connection to measured joint motion.
- [x] Learn the nominal motion reference/progression from training only; do not use event boundaries to create task phases.
- [x] Specify causal initialization, state propagation, prospective observation prediction and synchronization.
- [x] Separate prediction before correction from the correction proposed by the current measurement.
- [x] Keep expected progression separate from merely adopting measured speed as authorized speed.
- [x] Define the detection score and any permitted causal score aggregation before calibration.
- [x] Test normal-only recurrence, phase ambiguity, prediction usefulness and state uncertainty against simple controls.
- [x] Implement the matched correction-evidence versus residual-only score comparison with identical state trajectories; nominal progression remains in both predictors.
- [x] Specify scientifically justified additional ablations: unconstrained following and fixed/free-running reference, with failure/normal drift reported.
- [x] Test actual model causality and score-before-update behavior; infrastructure call order alone is insufficient.

**Go/no-go:** if meaningful asset-state correspondence, prediction and synchronization cannot be established, describe the model as an observer/predictor or revise the question before final testing. A twin label or an added phase variable is not evidence of novelty.

**Completion evidence:** [observer report](OBSERVER_VALIDATION_REPORT.md), [artifact registry](../experiments/OBSERVER_ARTIFACTS_V0.1.json), 254 passing tests, 7/7 declared internal checks and 48/48 saved-artifact checks. The state is an empirical phase distribution; ambiguity and strong AR performance limit the claim. This meets the stated observer/revised-question branch of the milestone; it does not establish a physical twin or security benefit.

## 11. Resolve contribution and evidence breadth — scope decision complete

The [contribution decision](CONTRIBUTION_AND_EVIDENCE_SCOPE.md), [comparison design](COMPARISON_ROSTER_DECISION.md), three primary-source audits and [independent-evidence plan](INDEPENDENT_EVIDENCE_PLAN.md) now document this decision. No security result or publication readiness follows.

- [x] Compare phase/alignment/segmentation/prediction/surprise prior art claim by claim. These components and the tracking/detection trade-off are established; no new-twin/estimator claim.
- [x] Correct the matched contrast: R versus R+C isolates added correction-discrepancy scoring. Both retain nominal progression and identical states; map the historical wording in a future versioned execution manifest.
- [x] Decide the narrow core comparison roles: eleven variants, seven implemented and four C/K/L/Rv design-only. Classical controls remain essential; original learning trio is not a fair admitted ranking. Full implementation admission remains Stage 12.
- [x] Limit claims to one repetitive acquisition/eight dependent intervals. No robot/task/fault/changeover generalization or intent attribution.
- [x] Screen independent sources: prioritize voraus-AD as separate physical-fault/variable-execution evidence and NIST as benign-condition evidence. No additional source admitted.
- [ ] Freeze an independent-evidence design before looking at its outcomes. Multiple windows, eight intervals and three seeds are not independent robot replications.
- [x] Choose a narrow single-recording score-comparison case study; broader cybersecurity claims remain withheld. Leading-journal ambitions do not turn limited evidence into a general result.

**Go/no-go:** do not spend a large training budget on an indistinct mechanism or unsupported claim. If simple controls explain the task or prior art already establishes the proposed contribution, narrow/revise the question. Negative findings may be useful; neither a negative nor positive finding guarantees publication.

**Complete here:** scope revision, close-prior-art comparison, scientific roster design and independent-source investigation. **Still pending:** measured contribution, four score implementations, independent dataset/protocol admission and final execution readiness. The uncompleted independent-evidence freeze is a future source-specific gate, not a claim that metadata screening supplies new observations.

## 12. Freeze the selected model comparison before calibration

- [x] Select scientific roles and designations in the [core roster](COMPARISON_ROSTER_DECISION.md); seven implemented and four design-only variants.
- [ ] Specify, implement/test and normal-validate the new C/K/L/Rv scores under a versioned bounded extension; preserve v0.1 and the consumed attempts.
- [ ] Admit the complete executable roster, exact artifact identities and explicit historical-to-current contrast-name mapping.
- [ ] Record each finite search, normal-only selection objective, candidate table and selected configuration.
- [ ] Fit selected full-training artifacts and record their transforms, references/checkpoints and initialization.
- [ ] Fix stochastic seeds **17, 42, 2026**, paired where applicable; deterministic controls run once.
- [ ] Fix all score definitions, common support, failure policies, reporting populations and primary paired contrast.
- [ ] Freeze exact code/environment/configuration identities, commands and resource budgets.
- [ ] Verify that no calibration or final behavior selected a model, seed, feature or persistence rule.

**Completion evidence:** a nonempty frozen roster/run matrix and real artifact hashes. Empty lists/nulls in the current [freeze record](../experiments/FINAL_TEST_FREEZE_RECORD.json) mean this is unfinished.

## 13. Calibrate thresholds and complete final-evaluation readiness

- [ ] Implement/test a calibration-only path that accepts frozen artifacts and the correct normal partition.
- [ ] For every model/seed, produce complete scores on the same **160,473** eligible calibration endpoints.
- [ ] Set the threshold at ascending one-based rank **158,869**, using strict `score > threshold`; no interpolation or test-selected alternative.
- [ ] Save the exact threshold, score dtype, score/count/hash receipt and fitted-artifact identities.
- [ ] Do not rank models on calibration behavior or refit after calibration under this protocol.
- [ ] Implement/test final-source admission, complete output alignment, access ledger, terminal failure handling, and label joining only after all campaign outputs are saved/hashed.
- [ ] Fill the actual final-freeze record with completed prerequisites; keep approvals, timestamps and hashes factual.

**Completion evidence:** valid thresholds for every admitted artifact and a verified final runner. The empirical 99th-percentile rule is not a guarantee of a future 1% false-positive rate.

## 14. Execute the protected final campaign once as declared

- [ ] Replay protected normal and mixed slices continuously, with no label-driven resets.
- [ ] Hold model parameters, nominal references, residual normalization and thresholds fixed; only the declared dynamic state may evolve.
- [ ] Run every declared method/seed under the frozen scope. Sequential execution is acceptable; inspecting one result to redesign later methods is not.
- [ ] Save/hash aligned scores and terminal failure records before joining labels or releasing scientific outcomes.
- [ ] Account for every registered run, including failures; do not discard bad seeds or shrink support.
- [ ] Record accidental early exposure, technical retries and any deviations.

**Completion evidence:** a complete campaign artifact/status matrix and the full report. Lengthy/paid runs and publication retain explicit approval requirements; this roadmap does not launch them.

## 15. Analyze the evidence, including failures and trade-offs

- [ ] Verify unadjusted TP/FP/FN/TN, precision/recall/F1 and tied-score average precision on the mixed population.
- [ ] Report protected-normal point exceedance, observed episodes/hour, native-time exposure and coverage together.
- [ ] Show all eight interval outcomes, misses, pre-existing alarms, fresh onsets and schedule-relative delay; keep recovery behavior visible.
- [ ] Compare R versus R+C (additional correction evidence) and all mandatory controls without a new composite winner or a better-looking threshold.
- [ ] Report every seed and descriptive paired summaries. Do not turn correlated rows, intervals or seeds into independent-plant significance claims.
- [ ] Separate parsing, fitting, calibration and processing costs; do not present them as live deployment latency.
- [ ] Inspect final plots/failure cases only after release, as analysis; do not use them to tune the claimed final model.
- [ ] Record whether the hypothesis is supported, contradicted, or only partly supported, and under which assumptions.

If the twin adds little beyond velocity/template controls, say so. If detection improves while normal alarms increase, report the trade-off. Outcome-informed redesign is exploratory; reusing or reshuffling this holdout does not create fresh confirmation. Bug corrections retain the original outputs and correction history.

## 16. Write the manuscript and reproducibility package from the evidence

Writing notes can proceed throughout the project. A results section and contribution claims require actual results.

- [ ] Draft the problem, why synchronization matters, and the restricted threat model from verified sources.
- [ ] Organize related work by scientific role and distinguish close prior art from peripheral architecture papers.
- [ ] Document dataset release, annotations, assumptions, split/support rules and permissions.
- [ ] Write the exact method, equations/pseudocode, state flow and ablation logic.
- [ ] Describe selection/calibration/final separation and all implementation deviations.
- [ ] Generate tables/figures directly from frozen result artifacts; retain the generating scripts and source hashes.
- [ ] Explain negative results, uncertainty, single-acquisition limits and unsupported generalizations.
- [ ] Write the abstract and conclusion after the evidence is settled.
- [ ] Develop title candidates that describe the demonstrated contribution; check collisions and retain “digital twin” only if justified.
- [ ] Make the authors explain/revise the manuscript in their own precise voice; avoid filler without concealing required AI-assistance disclosure.
- [ ] Prepare code/config/environment/command documentation and an authorized data-access recipe. Review permissions before distributing data, PDFs, author figures or model artifacts.
- [ ] Confirm actual contributions, author order, funding/conflicts and availability/disclosure statements.

**Completion evidence:** an internally reviewed manuscript whose claims, tables and figures trace to primary sources or actual runs, plus a reproducibility package that does not redistribute restricted material.

## 17–18. Choose a venue, submit, revise and preserve the scholarly record

- [ ] Choose a justified target and alternatives based on the finished contribution and evidence. Check current official scope, article type, relevant published work, reporting/code/data policies, fees and AI-use rules; no journal is selected here.
- [ ] Conduct a technical review for leakage, unfair comparisons, unsupported novelty, inconsistent units/metrics, citation errors and claim inflation.
- [ ] Verify every reference against primary metadata and supporting text; inspect figure/table permissions and publication obligations.
- [ ] Format for the selected venue and complete its actual checklist and declarations.
- [ ] Have all authors approve the final text, contribution statement and submission package.
- [ ] Obtain explicit approval before external submission/public posting or paid publishing actions; do not infer it from this roadmap.
- [ ] Record the submitted version and receipt. Submission is not acceptance or publication.
- [ ] If reviews arrive, create a point-by-point response with traceable revisions; mark new post-reveal experiments correctly and seek fresh evidence when needed.
- [ ] If rejected, assess the scientific reasons and venue fit honestly before revision/resubmission.
- [ ] If accepted, check proofs, archive permitted versions, preserve DOI/version/contribution records and fulfill applicable dataset acknowledgments/notifications.

Acceptance and publication timing are editorial outcomes, not milestones we can guarantee. Maintain factual records of later citations/use; do not manufacture impact or endorsements.

## What we do next, and what can run in parallel

**Immediate sequence:** retain controls/observer v0.1 → specify the bounded C/K/L/Rv extension → implement/test and normal-validate it → admit the complete executable roster → implement/admit threshold-only calibration → complete final freeze → execute the protected campaign only within its separately scoped plan. No large neural run is needed to fill a quota. Any observer refinement preserves v0.1 and declares a new development version before execution.

**Parallel work:** researcher learning, missing-source follow-up, contribution records and source-specific independent-evidence admission. ModernTCN/causal alignment become necessary if broader competitive claims are revived; they remain conditional now.

**Keep closed:** calibration for model selection, both final slices for exploratory development, invented results, heavy training without a concrete measured plan, and submission/publication without approval.

The supported nominal representation is an empirical observer. The next experiment must test the narrowly defined scoring question against its ordinary alternatives; an empirical contribution remains unproved. Additional faults or benign variation would extend evidence in separate tracks, not establish cross-robot cybersecurity by themselves.
