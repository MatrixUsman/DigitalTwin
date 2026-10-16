# Manufacturing paper roadmap: evidence, experiments and submission

## Material Passport

- Project / owner: manufacturing / Haiqa Mushtaq; project ownership is not a final authorship decision.
- Updated: **17 October 2026, Asia/Karachi**.
- Origin: academic-research-suite planning guidance, current project records and two internal read-only status/dependency reviews.
- Version: `manufacturing-paper-roadmap-v0.1`.
- Status: **current lifecycle plan, grounded in completed artifacts; future work remains unexecuted**.

This is the main lifecycle roadmap for this paper. Use [STATUS.md](../STATUS.md) for the short current handoff and [WORK_LOG.md](WORK_LOG.md) for what actually happened. Earlier reproduction proposals remain useful historical/source notes; they do not override the selected right-arm study or the current software status. The frozen data/evaluation specifications retain their original bytes and planning-date readiness fields.

## Where we actually are

We have a received and audited dataset, a selected feasibility question, a defined evaluation protocol, working research infrastructure and **83 passing synthetic software tests**. We have **not fitted a real-data model, reproduced a baseline, calibrated a CASPER threshold or measured attack-detection performance**. Most work that would establish the paper's scientific contribution is still ahead.

Working title: **“Digital Twins for Robotic Motion Integrity: The Role of State Synchronization.”** It remains provisional. The question is:

> Does retaining a nominal cycle-progression reference during state synchronization improve a motion twin's detection of CASPER's recorded right-arm speed changes under normal-only calibration?

In everyday terms: the monitor must follow the robot's motion, but following an unexpected speed change too readily might make that deviation disappear from its alarms. We want to test that possibility and whether retaining expected progression helps. It is a hypothesis, not a demonstrated failure or improvement.

The scope is one right-arm pick-and-place recording, with truthful telemetry/time assumed and command-path speed manipulation as the restricted threat. It does not cover a fully compromised controller, forged telemetry, legitimate changeovers, fault/attack attribution or live robot protection. See the [question and threat model](RESEARCH_QUESTION_AND_THREAT_MODEL.md).

| Stage | Current status | Evidence or unfinished part |
|---|---|---|
| 0. Workspace and records | Completed within setup scope | Independent project, instructions, local storage, logs and publication standards |
| 1. Researcher understanding | Partial | Lesson exists; researcher worksheet unanswered |
| 2. Literature and comparator admission | Partial / blocked in places | One full paper out of three; no admitted three-method ranking |
| 3. Data identity and suitability | Completed audit, with scientific limitations | Original CASPER v3 received; hashes/schema/labels/clocks recorded |
| 4. Research question and threat model | Selected for feasibility | Novelty and twin usefulness unproved |
| 5. Evaluation rules | Defined | Actual model/checkpoint/threshold freeze not completed |
| 6. Loader and metric foundation | Implemented, synthetic-tested | 83 tests pass; new loader has not been exercised on real observations |
| 7. First control and bounded runner | Not implemented | Exact pilot specification exists |
| 8. Real-data feasibility pilot | Not run | No fitted reference, scores, timing or memory measurements |
| 9. Full normal-only controls | Not implemented/fitted | Velocity, template and causal predictor specifications needed |
| 10. Twin and matched ablations | Not implemented/validated | State, progression, prediction and synchronization must be justified |
| 11. Contribution and evidence scope | Unresolved | Close prior art, appropriate comparators and independent-evidence needs |
| 12. Model-selection freeze | Not done | Roster/configurations/checkpoints/seeds remain pending |
| 13. Calibration and final-release preparation | Not done | No thresholds; final runner, ledger and actual freeze incomplete |
| 14. Protected final campaign | Not run | No final scores or outcomes |
| 15. Analysis and interpretation | Not started | Requires complete declared results and failure records |
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

**Already done:** source collection and static method/code study; a pinned pack of source/configuration/author-result artifacts; detailed [paper-to-code traceability](PAPER_CODE_TRACEABILITY.md). Author graphs and tables are literature artifacts, not our reproduced results.

| Learning paper | What is available | What prevents current experimental admission |
|---|---|---|
| CASPER | Corrected full paper and author code studied | Original external-IMU inputs differ from our controller inputs; inspected threshold selection uses anomaly labels; code-use and exact published-run correspondence remain unresolved |
| TWINE | Publication/abstract evidence and pinned code | Full manuscript unresolved; supervised/random-row workflow and differing model paths do not match our normal-only study |
| CatBoost on CASPER | Publication/abstract evidence, code and reported-output audit | Full manuscript/code provenance unresolved; inspected target construction, modality stacking and scaling cannot be adopted as our common protocol |

**Remaining checklist:**

- [ ] Seek lawful full manuscripts through publisher, institutional repository or author versions. Contact requires separately authorized outreach; absence of access is not evidence of a fake paper.
- [ ] Finish exact paper-section ↔ code-function ↔ configuration ↔ dataset/run correspondence.
- [ ] Resolve licenses/code-use terms and distinguish public availability from permission to reuse or redistribute.
- [ ] Search specifically for close work on task-phase synchronization, progression residuals, periodic-template alignment, prediction and anomaly preservation.
- [ ] Keep the current publication window **2023-10-16–2026-10-16** unless explicitly revising the search plan. Record any later literature update separately; older work can remain relevant background.
- [ ] For every proposed comparator, record release, features, labels, supervision, chronology, preprocessing, calibration, code revision and implementation designation.
- [ ] Decide: admitted under the common protocol, disclosed modified implementation, independent reimplementation, separate reproduction track, or background only.
- [ ] Find better-matched recent alternatives if necessary; do not fill three slots with scientifically unequal methods.

**Completion evidence:** an admission matrix with justified decisions and runnable/specifiable methods. Three downloaded papers are not three reproduced baselines, and three is not a scientific upper limit. Missing manuscripts do not block our independent simple-control pilot; they do block claims of reproducing those methods.

## 3–4. Keep the data identity, question and assumptions explicit

**Already done:** original CASPER v3 archive and five members received; six-file integrity checks; nested schema, labels, clocks, gap and annotation audits; selected right-arm source hash; twelve permitted q/qdot channels and relative time; exact eight recorded positive intervals. See the [identity register](DATASET_IDENTITY_REGISTER.md) and [data contract](ANNOTATION_FEATURE_SPLIT_CONTRACT.md).

Earlier audits did read raw records for identity/schema/annotation work. The later loader/metric implementation milestone used synthetic observations only. Do not describe the dataset as wholly unseen.

**Remaining checklist:**

- [ ] Exercise the new loader on the authorized bounded normal prefixes during the pilot and verify exact support, without changing raw bytes.
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

**Implemented:** read-only loader; manifest-bound training/development wrapper; observation/evaluator separation; causal score/update coordinator; calibration/count/AP/episode/event/time primitives. **83 synthetic tests passed**, and the recorded 13 source/config fingerprints still match at this roadmap audit. See [software validation](SOFTWARE_VALIDATION.md) and the [actual receipt summary](../experiments/SOFTWARE_TEST_REPORT.json).

**Remaining checklist:**

- [ ] Add model-specific fitting, future-information and immutable-reference tests when each model is implemented.
- [ ] Test the bounded supervisor and actual failure/abort records.
- [ ] Implement production calibration/final admission, exact score artifacts and protected label-join/release path.
- [ ] Implement complete seed/run report assembly and actual resource instrumentation.
- [ ] Validate these additions before using them for claims. Do not treat existing synthetic tests as production evaluator admission.

The current wrapper intentionally blocks calibration and final observations. Public raw files remain accessible locally; this is procedural/interface protection, not an OS lock or blinded study.

## 7. Implement the first control and bounded supervisor — immediate next task

The [pilot specification](BOUNDED_PILOT_PLAN.md) is complete as a plan. The control and supervisor are absent.

- [ ] Implement six-channel velocity mean and population variance using the declared streaming Welford calculation.
- [ ] Implement the fixed maximum absolute standardized-deviation score.
- [ ] Reject zero/nonfinite variance; do not introduce an unrecorded epsilon or discard a channel.
- [ ] Test known synthetic statistics, constant channels, nonfinite inputs, complete score support and unchanged fitted parameters.
- [ ] Ensure only eligible training-prefix observations fit the reference; development observations cannot update it.
- [ ] Implement timeout, CPU, monitored-memory and output-size limits with explicit terminal failure records.
- [ ] Test the supervisor on harmless synthetic workers that finish, fail or exceed a bound.
- [ ] Resolve the exact interpreter, command, configuration hashes, output paths and run manifest.

**Completion evidence:** executable, tested control and runner with a concrete command. This stage is software work; it does not require an attack score or a claim that the method is a twin.

## 8. Run the bounded normal-only feasibility pilot

- [ ] Verify raw source identity without inspecting protected feature distributions.
- [ ] Fit on raw training prefix `[0,50000)`: **46,944 eligible observations**.
- [ ] Score raw development prefix `[540002,560002)`: **18,472 eligible observations**.
- [ ] Record source traversal separately from selected observations; do not borrow history across the development boundary.
- [ ] Record all finite scores, coverage, reference hashes, timing, CPU, memory, output size and terminal status locally.
- [ ] Respect proposed limits: 600 seconds wall, 300 seconds CPU, 1 GiB monitored RSS, 50 MiB outputs, one deterministic attempt. These are unmeasured proposed limits until the supervisor exists and a run occurs.
- [ ] Do not calculate a threshold, attack F1/AP, final normal false alarms or event detection in this pilot.
- [ ] Preserve failure; diagnose with permitted normal data and version any changed rule before another bounded attempt.

**Pass condition:** exact permitted fitting/scoring support, finite outputs, immutable reference and recorded completion within the declared limits. **What it proves:** machinery and resource feasibility. **What it does not prove:** attack detection, novelty or superiority. A subset-fit pilot artifact cannot be renamed a full-training final checkpoint.

## 9. Implement and validate the simple comparison methods

- [ ] Specify a full-training version of the velocity control.
- [ ] Specify a nominal periodic-trajectory/template control with causal alignment.
- [ ] Specify an ordinary causal predictor, initially a small autoregressive model where feasible.
- [ ] Add a compact CNN only if it has a justified comparison role and an acceptable implementation/source designation.
- [ ] For every method, define inputs, formula, train-only transforms, history, initialization, score orientation and numerical failures.
- [ ] Predeclare a finite configuration set, normal-only development objective and deterministic tie-breaking. Development has no attack F1 target.
- [ ] Fit/select using training/development only; assess predictive/state behavior and computational feasibility there.
- [ ] Record all candidate configurations and failures, including simpler methods that work well.

**Completion evidence:** verified, complete-score controls with normal-only selected artifacts. Their final attack performance remains unknown until the common final campaign. Simple controls are essential because the recorded intervention directly changes speed.

## 10. Specify and validate the candidate twin and ablations

- [ ] Define the physical quantity/state represented and its connection to measured joint motion.
- [ ] Learn the nominal motion reference/progression from training only; do not use event boundaries to create task phases.
- [ ] Specify causal initialization, state propagation, prospective observation prediction and synchronization.
- [ ] Separate prediction before correction from the correction proposed by the current measurement.
- [ ] Keep expected progression separate from merely adopting measured speed as authorized speed.
- [ ] Define the detection score and any permitted causal score aggregation before calibration.
- [ ] Test normal-only recurrence, phase ambiguity, prediction usefulness and state uncertainty against simple controls.
- [ ] Implement the matched progression-aware versus progression-omitted comparison with all other conditions held comparable.
- [ ] Specify scientifically justified additional ablations: unconstrained following and fixed/free-running reference, with failure/normal drift reported.
- [ ] Test actual model causality and score-before-update behavior; infrastructure call order alone is insufficient.

**Go/no-go:** if meaningful asset-state correspondence, prediction and synchronization cannot be established, describe the model as an observer/predictor or revise the question before final testing. A twin label or an added phase variable is not evidence of novelty.

## 11. Resolve contribution, comparator strength and evidence breadth before final exposure

This work runs alongside Stages 7–10 rather than waiting for final results.

- [ ] Build a claim-by-claim comparison with the closest existing methods: what is already known, what differs here, and which experiment could refute the proposed benefit.
- [ ] Confirm that the matched ablation isolates progression evidence rather than changing inputs, capacity and tuning budget at the same time.
- [ ] Decide whether the final comparison set is strong and fairly admitted; keep unchanged paper reproductions separate from modified methods.
- [ ] Decide which claims one repetitive recording can support and what broader claims would require.
- [ ] Assess suitable independent acquisitions/tasks/robots or another compatible dataset/testbed if broader evidence is needed. No additional source is currently admitted; verify access, labels, clocks and comparability first.
- [ ] Freeze an independent-evidence design before looking at its outcomes. Multiple windows, eight intervals and three seeds are not independent robot replications.
- [ ] Record a reasoned choice: a narrow single-recording feasibility claim, or a larger validated study. Leading-journal ambitions do not turn limited evidence into a general result.

**Go/no-go:** do not spend a large training budget on an indistinct mechanism or unsupported claim. If simple controls explain the task or prior art already establishes the proposed contribution, narrow/revise the question. Negative findings may be useful; neither a negative nor positive finding guarantees publication.

## 12. Freeze the selected model comparison before calibration

- [ ] Finalize the full method/control/ablation roster and implementation designations.
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
- [ ] Compare the progression-aware/omitted pair and all mandatory controls without a new composite winner or a better-looking threshold.
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

**Immediate sequence:** implement the velocity control → test its fitting/numerical behavior → implement/test the bounded supervisor → prepare the concrete pilot command/manifest → run the separately scoped normal-only pilot → review feasibility before expanding models.

**Parallel work:** researcher learning, missing-manuscript/source follow-up, comparator admission, close-prior-art analysis, contribution records and independent-evidence planning. These need not wait for the pilot.

**Keep closed:** calibration for model selection, both final slices for exploratory development, invented results, heavy training without a concrete measured plan, and submission/publication without approval.

The next scientific decision after the pilot is whether normal-only data support a useful nominal state/progression representation and whether a strong comparison can test a distinct contribution. Completing code is necessary, but that decision determines what paper we can honestly write.
