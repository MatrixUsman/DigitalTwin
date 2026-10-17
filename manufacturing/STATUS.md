# Manufacturing status

## Current science — normal-only reference study v0.9, 17 October 2026

[Completed](research_cycles/commissioning_v0.9/RESULTS.md): 63 ordinary ARX/FIR candidate fits, fifteen archived normal checks, 81 fresh normal episodes and 576 role outcomes. Twenty-three synthetic tests and 10,293 verification checks passed. The first worker stopped on a reporting-key collision before fresh generation; the separately recorded fix reproduced every fit and selection unchanged. Completed run: 14.748 s wall, 14.296 s CPU, 113.97 MiB sampled RSS, 28.02 MiB outputs. No new attack experiment or raw dataset observation.

Clean-data selection chose ARX orders 8/16/32 for Q1/Q2/Q3. Q2 allowance fell 0.146910→0.071592 (51.27%) and all 108 normal probes can clear; its 93.32% feasible-point fraction misses the frozen 95% gate. Q3 allowance fell 0.191250→0.117495 (38.56%) but remains above tolerance 0.1. All normal prediction RMSEs improve against a matched-initialization ARX(4). These are ordinary identification gains; no new algorithm or attack benefit is established.

[Post-study noise diagnosis](research_cycles/commissioning_v0.9/NOISE_DIAGNOSTIC.json): for a hypothetical perfect reference under the declared independent Q3 Gaussian noise, the probability that a maximum allowance from 5,500 points leaves 95% population feasibility is about 2.19e-9. This is a conditional calculation, not a general impossibility result. Improving the reference alone does not fix the specific maximum-plus-discrepancy rule.

[Current versioned roadmap](docs/PAPER_ROADMAP_V0.9.md). The older roadmap retains its consumed frozen bytes.

**Next:** [define a noise-aware causal return decision](research_cycles/commissioning_v0.9/DECISION.md) that separates model bias, sensor noise and physical-deviation evidence. Compare with ordinary averaging, likelihood/equivalence tests and same-reference hysteresis before claiming novelty. Require a new frozen normal-feasibility check before fresh attacks. The current H/I/J check is exposed; full paper comparators and author approval remain unresolved. AFTER stays a proposed title, and existing manuscripts/results are preserved.

## Current title preview — 17 October 2026

The user rejected the question-style title and requested a memorable name. The assistant-proposed working title is **AFTER: Digital Twins for Cyberattack and Recovery Monitoring in Industrial Robots**. [Latest title preview and PDF](manuscript_recovery_v0.8r1/README.md). **The user has not finalized this name.** Only the title changes; the v0.8 scientific text, findings and readiness decision below are unchanged. [Title decision](docs/TITLE_DECISION.md) records the naming scope. Earlier titles remain historical evidence.

## Current handoff — commissioning and recovery v0.8, 17 October 2026

[The new frozen study](research_cycles/recovery_v0.8/RESULTS.md) completed **216 synthetic episodes, thirteen methods and 2,808 outcomes**. Fourteen pre-run tests and 9,610 post-run checks passed. All eleven scientific source/spec files and 1,078 prior/source/input bindings remain unchanged. The completed run took 229.196 s wall / 228.069 s CPU, with 167.25 MiB sampled RSS (217.41 MiB worker lifetime peak) and 118.32 MiB output. One process-monitor failure before worker startup is preserved; the unchanged worker completed after a scoped monitoring retry.

**Scientific decision:** reject the uncertainty-addition rule as the intended contribution. It reduced benign alarm observations from 621 to 309 versus nominal fixed return, but cleared within five seconds in only 36/108 detected-returned events. Its declared primary criterion failed. The same-entry-threshold control without the allowance achieved 140 benign alarms and 108/108 timely clearances, with the same 108 event overlaps and no premature clears. Q2/Q3 allowances exceed the return tolerance, making clearance impossible by construction. All 27 command-context misses remain in the results.

**Delivered:** [ten-page LaTeX/PDF manuscript](manuscript_recovery_v0.8/README.md), complete all-method/plant tables, mathematical explanation, primary-source/code audit and [publication decision](research_cycles/recovery_v0.8/REVIEW_AND_DECISION.md). The stronger ordinary control remains visible. The full recent-paper comparison set and original-method novelty are still incomplete. The draft is not journal-ready; author roles, Haiqa's affiliation, funding/conflicts and both-author approval remain unconfirmed. Public simulation is sufficient to continue; physical equipment is not required.

**Next bounded step:** commissioning-only diagnosis of reference error/model adequacy, with a normal-only clearance-feasibility gate before any new attack exposure. A proposed improvement must have a defensible distinction from close interval/recovery methods and share its fitted reference with ordinary controls. The v0.8 matrix is now exposed; outcome-informed changes need a separately frozen fresh test. See [normal-only admission diagnostic](research_cycles/recovery_v0.8/NORMAL_ADMISSION.json). The current monitor computations use only permitted inputs, but its broad dictionary interface does not enforce that boundary; the supplemental check is explicitly scoped to three restricted-input replays.

Earlier handoffs below are historical. Old experiments/PDFs, raw data and sibling projects are preserved. No publication, external contact, paid compute or assistant-issued Git mutation occurred.

## Historical manuscript edit — 17 October 2026

The [revised 14-page PDF](output/pdf/alarm-recovery-model-mismatch-revised.pdf) removes repeated draft notices and process commentary and tightens the prose throughout. [Editorial source and checks](manuscript_recovery_v0.7r1/README.md) preserve the findings, limitations, references and AI-assistance disclosure. All generated tables/figures and display equations are unchanged. Offline compilation and visual review passed; all 260 files in the original scientific package retain their hashes. No new experiment ran. The scientific findings and next research task below are unchanged.

## Historical handoff — fresh confirmation and manuscript v0.7, 17 October 2026

**Completed:** [the prospectively frozen virtual comparison](research_cycles/recovery_v0.7/RESULTS.md), 144 fresh episodes, 23 decisions and 3,312 outcomes; fourteen synthetic tests and 14,635 fresh-process checks passed. All source/configuration/input bindings, calibration and score seals remain intact. One successful run took 81.959 s wall / 81.472 s CPU, with 273.05 MiB measured peak memory. No raw observations, physical equipment or new neural training were used.

The selected fixed-return mechanism **failed its primary improvement criterion**: 2,778 benign alarm points versus 2,452 for fused hysteresis (13.30% more), with 90/90 overlaps, 72 fresh onsets and no premature clears. At the same entry threshold, removing dwell caused premature clearing in 44 events; removing reference entry left every alarm array unchanged. The all-method table retains stronger ordinary controls, subgroup results, all misses and recovery costs.

**Written and built:** [17-page LaTeX review manuscript](manuscript_recovery_v0.7/README.md), *When Should a Digital-Twin Alarm Clear? Recovery Evidence under Motion-Model Mismatch*, with result-generated tables/figures, claim/reference audit, declarations and a separate PDF at `output/pdf/alarm-recovery-model-mismatch.pdf`. Every page was rendered and inspected. Author order is Muhammad Usman, Haiqa Mushtaq; Muhammad Usman’s supplied COMSATS Sahiwal affiliation is recorded. Haiqa’s affiliation, individual roles, funding/conflicts and both-author approval remain unconfirmed. ISA Transactions is a conditional scope-fit target, not a submission or acceptance decision.

**Scientific gate:** a new original algorithm or overall improvement is not established. The intended original-contribution objective remains active; the manuscript records the completed evidence rather than relabeling failure as superiority. Next specify model-adequacy/recovery evidence against close interval/recovery prior art and test any redesign on newly frozen virtual conditions. v0.7 is exposed. Public fault recordings require separate admission and must not be renamed cyber evidence. No physical-lab requirement applies. Earlier studies, old PDFs, water and smart grids remain unchanged.

## Historical handoff — command uncertainty and recovery v0.6, 17 October 2026

**Completed:** [the frozen virtual experiment](research_cycles/recovery_v0.6/RESULTS.md): 144 new synthetic episodes, thirteen methods, 1,872 outcomes. Twenty-three synthetic tests, 8,332 fresh-process checks and twelve numerical-refinement trajectory comparisons passed. One successful supervised run took 63.578s wall / 63.114s CPU with 88.66MiB sampled RSS. All old scientific artifacts remain unchanged.

The envelope/fixed-return candidate reduced within-range benign alarms from 354 to 277 (21.75%) versus fused hysteresis, with 60/60 event overlaps, 48 fresh onsets and no premature clears. The predeclared 25% reduction requirement against both controls **failed**. Its false alarms rose to 66.60% beyond the modeled parameter range. The simpler nominal-entry/fixed-return ablation had 167 benign alarms (52.82% fewer than fused), the same event coverage and no premature clears, but did not improve outside-range benign alarms. Alarm episodes/hour and attack-interval F1 expose additional costs; [all methods and strata](research_cycles/recovery_v0.6/TABLES.md) remain visible.

**Decision:** retain the simple fixed-return ablation as a development lead and keep fused/ARX/following/rolling-mean controls. The sampled envelope is not justified as the final method. Next investigate trusted model-adequacy evidence under legitimate dynamics change, and resolve the distinction from interval-observer/recovery prior art before another design. This cycle is now exposed; any outcome-informed candidate needs newly frozen physical assumptions/conditions for confirmation. No original algorithm, faithful paper reproduction or real-robot validation has been established. The original-contribution destination remains active.

[Plan and code](research_cycles/recovery_v0.6/README.md), [comparison figure](output/recovery_v0.6/comparison.png), [validation](research_cycles/recovery_v0.6/VALIDATION.md). All work is fully virtual; the user needs no laboratory equipment. Earlier handoffs below are historical.

## Historical handoff — recovery simulation v0.5, 17 October 2026

**Entirely virtual:** the user confirmed that no physical laboratory work is feasible. The simulator and all existing pilot observations run in software. [Open the virtual lab guide and animated replay](simulation/README.md); Codex handles implementation and execution. This demonstration uses existing saved observations and does not create fresh experimental evidence.

**Completed:** [comparator role decisions](research_cycles/recovery_v0.5/COMPARATORS.md), [precise candidate/prior-art assessment](research_cycles/recovery_v0.5/PRIOR_ART.md), and [bounded physical simulation pilot](research_cycles/recovery_v0.5/RESULTS.md). Two simulated plants, three paired noise seeds, 18 training / 18 calibration / 48 evaluation episodes, eleven methods and 528 outcomes. All observations are synthetic; no CASPER or fresh physical recording was opened.

The protected-command following observer reaches 92.05% attack-command recall with 1.07% alarms on clean normal episodes; ordinary ARX reaches 91.72%. The recovery candidate gives the same 92.05% recall and 3.49% normal alarms. It clears after the declared simulated physical-return diagnostic in all 30 intervention episodes, whereas the following observer clears earlier. This is a real recovery/normal-alarm trade-off in the specified simulator. **The candidate is exactly fused-error dwell-time hysteresis**, verified algebraically and in every episode; do not claim original algorithmic novelty or general physical safety.

Validation: 26 passing synthetic tests; 53,004 passing fresh-process and reporting checks. Preserve one pre-run integration-test failure and one post-scoring JSON-export failure. All simulation scores were sealed; a separately frozen reporting job repaired only scalar serialization. Generation took 73.353 s supervised wall / 72.422 s CPU; export recovery 0.393 s / 0.379 s CPU. No scientific choice changed. Both attempts, source freezes, prior model/PDF identities and environments remain preserved.

**Next bounded scientific task:** diagnose authorized-change residuals in this exposed pilot, then specify a non-equivalent uncertainty/recovery mechanism against mode-conditioned calibration, ordinary hysteresis and close set-consistency work. The required problem is reducing legitimate-change alarms while retaining evidence until physical recovery under model mismatch. Freeze any new task/geometry/mismatch groups before generation; none was generated here. The original-contribution destination remains active. Recent paper roles are decided, but three faithful comparable paper reproductions are not established.

Everything below records prior stages; this v0.5 handoff supersedes their pending recovery-simulation task.

## Historical handoff — limitation experiment v0.4, 17 October 2026

**Completed:** [189 synthetic brief/persistent scenarios](research_cycles/limitation_v0.4/RESULTS.md), six saved predictors, four scoring rules and 4,536 jointly evaluated outcomes. No retraining or new raw/final observations. [Figures and package](research_cycles/limitation_v0.4/README.md) preserve all controls, seeds, misses, false alarms and costs.

Altered prediction histories reduce discrepancy for many holds/slow-playback cases, but CNN error does not consistently decline over time. Sensor offsets often amplify error. The broad hypothesis of universal persistent-deviation assimilation is not supported.

For 450-observation deviations, the CNN average point recall/F1 is **25.12%/0.2778** for point scoring, **53.33%/0.5127** for a 45-point mean, and **66.91%/0.2364** for CUSUM. CUSUM's long carryover offsets its coverage gain; 128/189 long seed-case outcomes remain alarmed throughout the next 512 observations. Rolling means miss all five-observation events. Same-percentile calibration does not ensure equal normal false-alarm rates. These are dependent synthetic scenarios on exposed normal development, not independently recorded attacks.

Validation: **22 synthetic tests** after one preserved float32 assertion correction; **26,374/26,374** fresh-process checks. One successful replay took **6.198s wall**, **4.799s CPU**, **453.77MiB sampled RSS**, and about 20.0MB of outputs, inside all caps. Original source/model/PDF identities remain unchanged.

**Next scientific step:** retain the 45-point mean as a strong ordinary control and test a mechanism that jointly handles sustained-change evidence, brief deviations and justified recovery. Specify a small dynamics-based simulation with permitted command context, plant/observer mismatch and legitimate changes; freeze separate task/plant groups before prospective outcomes. Resolve the exact difference from close prior art. This exploratory result does not establish algorithmic novelty. The user's original-contribution objective remains active.

The earlier handoffs below are historical records; the v0.4 result supersedes their pending limitation-experiment task.

**Current result:** the [compact CNN baseline pipeline](research_cycles/baseline_training_v0.3/README.md) is implemented, tested and executed. Three CNN seeds each completed 30 epochs on 65,536 normal training targets and scored 16,384 chronological development targets. The selected models, scaler, AR control, predictions and learning curves are saved and verified.

## Completed baseline training v0.3, 17 October 2026

| Item | Actual outcome |
|---|---|
| Trained models | CNN seeds 17,42,2026; epoch 30 selected for each; all retained |
| Controls | Training mean, persistence and fitted multivariate AR(4), same eligible endpoints |
| Normal-development MSE | CNN mean **0.105364**; persistence **0.124758**; AR(4) **0.071310** |
| Coverage | 65,536 training / 16,384 development; 100% eligible under the frozen gap rule |
| Validation | 25 synthetic tests; **410/410** fresh-process artifact checks; every saved CNN prediction reproduced exactly |
| Resources | 57.851 s supervised wall; 56.526 s worker CPU; 520.16 MiB sampled peak RSS; all caps passed |
| Outcomes preserved | All seeds, learning curves, controls and costs. No training failures/retries |
| Data access | Nominal prefix only; raw bytes unchanged; no calibration, attack or final-test access |

See the [complete result report](research_cycles/baseline_training_v0.3/RESULTS.md), [source/configuration freeze](research_cycles/baseline_training_v0.3/FREEZE.json) and [figure](output/baseline_training_v0.3/learning_curves.png). The implementation follows the compact published architecture with explicitly documented protocol choices. CNN curves were still improving at the 30-epoch cap. AR is the strongest normal predictor and stays in the next comparison.

**Next:** specify and execute an exploratory limitation experiment using these saved predictors and simple controls, examining brief versus persistent motion deviations. Declare any additional training budget before looking at intervention outcomes. The user's original-contribution objective and public-data/labelled-simulation route remain active; the earlier CASPER holdout stays exposed. Models and prior studies are preserved independently.

## Completed v0.2 source investigation — historical handoff

| Requested stage | Actual outcome |
|---|---|
| Investigate baseline limitations | [Dossier](docs/BASELINE_LIMITATION_DOSSIER_V0.2.md) connects manuscript/code claims to exact tests; original table/checkpoint/scaler lineage remains incomplete |
| Reproduce the limitation | Specific target/variable/score discrepancies and released-model state behavior reproduced. **No method-level cyber weakness demonstrated yet** |
| Design an improvement | [Constrained recovery candidate](docs/CONTRIBUTION_DESIGN_V0.2.md) specified; not implemented or admitted as novel. Close prior art overlaps its main ingredients |
| Test fairly | 18 synthetic tests and one normal-only pilot: 8,192 training targets, 2,048 finite aligned development scores, 3.8355 s supervised wall. No attack calibration/evaluation or full comparison |
| Write contribution paper | [Source-backed LaTeX notes](research_cycles/contribution_v0.2/research_notes.tex) written; contribution results, final title and venue remain pending. Notes have not been compiled to PDF |
| New data | One author-linked provider-v2 nominal `IMU_10Hz.csv` acquired and hashed; bounded prefix inspected. No successor disturbance observations acquired; no whole-release or independent-cyber admission |
| Evidence route | User confirms no physical testbed: use public datasets and clearly labelled simulation. No simulator has been implemented in this cycle |
| Validation | [237/237 saved-artifact checks](research_cycles/contribution_v0.2/EVIDENCE_MANIFEST.json) passed, including original frozen artifacts/PDF. Two failed diagnostic attempts and setup failures preserved |

**Historical next action at the v0.2 handoff:** resolve the close recovery prior art and exact baseline training/preprocessing/state policy; demonstrate an algorithmic limitation with corrected comparators under a separately specified exploratory protocol. The generic twin/recovery gate is not accepted as novelty. Full training needs a concrete bounded plan; lengthy runs retain approval requirements. The [results](research_cycles/contribution_v0.2/RESULTS.md) and work log preserve all outcomes. No sibling project changed scientifically.

## Completed v0.1 preliminary study — historical context

The following records describe the earlier experiment and its handoff. They do not negate the separate v0.2 data receipt, neural pilot or source-code execution above. Its frozen contracts, input identities and exposed-holdout status remain unchanged.

As of **17 October 2026**. Owner: **Haiqa Mushtaq**. Manufacturing remains active while water waits for iTrust. The [protected final campaign and joint analysis](docs/FINAL_CAMPAIGN_REPORT_V0.1.md) are complete: **eleven deterministic methods, 897,119 finite scores each, all eight event outcomes**, one accepted scoring attempt and one accepted delayed-label evaluation. No failures or retries. The saved-result arithmetic audit passed. The correction-score gain is small and absolute detection is poor; this single-acquisition study does not establish a general detector or novel digital twin. The holdout is now exposed.

| Item | Actual state |
|---|---|
| Stage | Preliminary campaign/report complete; original-contribution selection reopened; baseline limitation/reproduction planning is next |
| Recommended setting | Industrial robotic arms; original CASPER pick-and-place collection |
| Title / question | Intended contribution paper: not selected. “Correction Evidence in Robotic Motion Monitoring: A Controlled CASPER Study” names only the preserved preliminary report |
| Contribution / breadth decision | Original digital-twin security contribution remains the objective; no verified baseline failure or new mechanism yet. One acquisition/eight dependent intervals cannot establish broader generalization |
| Core comparison design | Eleven deterministic variants, one run each, actual fitted references/configurations frozen; all eleven calibrated. ModernTCN/independent alignment remain conditional on broader claims |
| Independent evidence | voraus-AD and NIST screened as separate physical-fault/benign routes; no new dataset received/admitted, no new cyber ground truth |
| Selected threat / inputs | Command/application speed manipulation with truthful monitoring telemetry/time assumed; twelve right-arm joint-position/velocity channels plus relative-time context |
| Annotation / splits | Recorded schedule flags, eight events; exact chronological blocks, common eligible support and continuous final replay defined |
| Calibration / metrics | All eleven thresholds stayed fixed at ascending rank 158,869 of 160,473, strict exceedance; P/R/F1/AP, normal burden, coverage, events/delays and recovery audited |
| Final-test protection | All scores sealed before labels; joint outcomes inspected after every method completed. Original freeze preserved; actual access/completion recorded separately. Holdout now exposed |
| Repeats | All eleven deterministic methods ran once, seed null. Policy seeds 17, 42, 2026 unused; no stochastic variability or independent replications |
| Learning set | CASPER 2024, TWINE 2026, CatBoost on CASPER 2026; source/admission notes under `baselines/` |
| Shared-data evidence | Our v3 bytes/hashes fixed; equivalent bytes behind every published run, common annotations/inputs and run correspondence remain unresolved |
| Public data access | Original CASPER v3 acquired publicly under provider CC BY-SA 4.0 terms; no institutional approval required |
| Local benchmark data | **Archive + five original members**, about 10.72 GB combined; fresh six-file hash matches, structural checks and PCAPNG header/timestamp audit complete |
| Manuscripts and code | CASPER corrected VOR V1.1 and TWINE accepted manuscript collected; CatBoost full text unresolved. Pinned source packs and audit receipts retained; no upstream code executed |
| Paper-to-code milestone | **2 of 3 original learning manuscripts available and AI-audited**; TWINE now has explicit section/code and reported-metric checks. Human comprehension unassessed; no reproduced run |
| Comparison designations | [Admission decision](docs/COMPARATOR_ADMISSION.md): CASPER external-IMU track held; CASPER-inspired independent CNN design candidate for Group D; TWINE/CatBoost background only for Group D, supervised track not admitted; ModernTCN 2024 is a conditional modified author-code transfer candidate, not a published CASPER result or ready baseline |
| Step 0 comprehension | Lesson and synthetic worked example prepared; researcher worksheet unanswered, understanding unassessed |
| First executable study | Deterministic velocity control fitted 46,944 eligible observations and saved 18,472 aligned finite development scores; reference unchanged; one attempt accepted |
| Other open routes | MIT synthetic machining/assembly; CMU TEP manipulations; no verified recent three-paper intersection |
| Environment / detector implementation / training | Manufacturing-local Python 3.15.0 venv, standard library only; seven ordinary controls fitted on full training and three selected on normal development. Empirical phase observer implemented and normal-development tested; no validated physical twin or reproduced paper baseline |
| Measured pilot resources | 8.626 s supervised wall, 8.571 s worker CPU, 27.94 MiB peak RSS, 1.93 MiB run outputs; all within declared limits |
| Full-training controls | 536,946 eligible training targets and 160,472 complete finite normal-development scores per candidate; selected velocity, 32-bin template, AR(4) ridge 0.001; all seven references unchanged |
| Control-study resources | 51.377 s wall, 51.270 s CPU, 147.48 MiB peak RSS, 17.53 MiB outputs; all within limits |
| Observer validation | 38-second recurrence and ordered phase progression; all 7 internal checks passed on 536,946 training / 160,472 development endpoints; same development reused after template selection |
| Observer limits | One-step MSE 0.338911 versus AR 0.002094; 53.12% descriptive phase ambiguity; uncertainty uncalibrated; diffusive free-running comparison is limited |
| Observer resources | 169.945 s wall, 169.649 s CPU, 330.19 MiB peak RSS, 14.05 MiB outputs; all caps met |
| Score extension | Six same-state outputs / 160,472 endpoints each; no fitting; exact previous R/RC/index parity; all 66 historical protected hashes unchanged |
| Score-extension resources | 34.015 s wall, 33.784 s CPU, 42.61 MiB peak RSS, 16.30 MiB outputs; all caps met |
| Frozen calibration resources | 52.247 s supervised wall, 52.043 s CPU, 49.67 MiB peak RSS, 18.26 MiB outputs; all limits satisfied |
| Protected scoring resources | 270.890 s wall, 270.520 s CPU, 143.19 MiB peak RSS, 102.317 MiB outputs; all frozen limits met |
| Joint evaluation resources | 44.778 s wall, 44.660 s CPU, 902.50 MiB peak RSS, 0.188 MiB outputs; all frozen limits met |
| Main result / novelty | O-RC F1 0.017292 versus O-R 0.016603; O-RC recall 0.8805%, 0.9941% normal point alarms and 185.98 episodes/hour. Small within-recording gain; no established novelty or general superiority |
| Ordinary controls | AR-4 F1 0.018846 with 437.09 normal episodes/hour; T-32 F1 0.074737 with 1.3997% normal point alarms. No method exceeded 4.0217% point recall |

## Important limits

- Original CASPER and CASPER 1 & 2 remain distinct provider listings. Only original v3 was acquired. `nicla_fixed.csv` is numerically equivalent to raw Nicla after six startup records under binary64 parsing; it provides no extra clock/labels. Its authoring history remains undocumented.
- The selected controller route changes the earlier external-IMU-first main-study proposal. It has a supported physical-state/time representation but a narrower threat: command changes with truthful telemetry. The collection does not prove an authenticated or independently protected monitor. Full controller/collector compromise, legitimate-change handling and fault/attack attribution remain outside demonstrated scope.
- Each arm has 1,762,650 rows and eight positive label runs. Full nested parsing validates 66 scalars per row including time/label, with no numeric/shape errors; 64 observables are possible before feature selection. IMU has 1,751,682 numeric rows without timestamps/labels. These are dataset facts, not detector results or independent runs.
- Matched author capture code and official UR documentation now support boot-relative seconds for controller timestamps. The original executing revision, wall-clock anchor and cross-device synchronization remain unproven. IMU labels are retrospective/manual; controller flags reflect a schedule rather than independently measured impact onset.
- Fresh boundary review preserves exact serialized times around all eight flag runs. The later matched source writes the same flag to both arms while changing only the right-arm speed; left-file flags are not per-arm physical-impact truth. `arms.pcap` is PCAPNG: 14,582,826 timestamped packet blocks, nanosecond resolution, two duplicate and 2,579 backward adjacent deltas in file order. Capture epoch times do not synchronize controller or IMU clocks; valid framing does not prove lossless capture.
- Static annotation lineage resolves a 916-row filtered-endpoint offset and 1,529-row complete CNN-score support. Derived class totals match the paper's confusion-matrix denominator; this is not reproduced predictions. Table 11 lists 750 fewer IMU rows than received and remains unresolved. The architecture figure agrees with four convolution layers in the code.
- CASPER's inspected threshold selection uses anomaly labels. TWINE uses random row splits and has inconsistent feature/model/demo paths. CatBoost's available script creates synthetic outlier labels, stacks incompatible sensor features as rows and scales before splitting. No such workflow is approved as our evaluation.
- Deeper paper/code reading also identifies unequal CASPER comparator training/output units and unresolved statistical-baseline records; TWINE's evaluated and SHAP-explained models differ; CatBoost author tables mislabel test accuracy as validation and mix timing units. These are documented source/provenance findings, not reproduced performance or blanket invalidation of the papers.
- CASPER observes external IMU; TWINE uses controller telemetry; supervised and normal-only training differ. Common collection does not automatically mean fair information access or a common detection task.
- Periodic alignment, task segmentation and prediction residuals already appear in close prior work. The specific synchronization/progression experiment is testable, but its novelty and benefit are unverified. Simple velocity and periodic-template controls are mandatory; no three-paper common-protocol ranking is admitted. ModernTCN requires a tested common-input adapter, clean selection rules, and explicit reconciliation of current-conditioned reconstruction with the frozen past-state prediction rule before execution.
- TWINE's accepted manuscript is now available; its VOR and CatBoost's full manuscript remain inaccessible. TWINE's reported P/R/F1 match support-weighted arithmetic rather than its positive-class equations; published-run and SHAP-model correspondence remain unresolved. Available code is not established as the exact code behind every published result. Original CASPER and CatBoost code licenses are unresolved; TWINE MIT license is verified. See the [dated TWINE audit](docs/literature/TWINE_ADMISSION_2026-10-17.md).
- Motion deviations and environmental faults do not by themselves establish malicious intent. Digital-twin labels/cloud state storage do not prove predictive physical fidelity or novelty. The CASPER+ programme already describes closely related research ideas.

## Next bounded action

Prepare the **baseline limitation and improvement-opportunity dossier** in the [corrected sequence](docs/ORIGINAL_CONTRIBUTION_DIRECTION_V0.1.md), starting with CASPER and its closest successor. Establish what is a verified code/protocol issue, what is an untested assumption, and what would require a reproduced failure. Select a common scientific task before choosing three experimental comparators. Any new method needs a close-prior-art argument and suitable fresh confirmatory evidence; source admission follows that question. Merely fixing splits/thresholds or renaming the existing observer does not establish a novel twin.

The following records describe the completed preliminary study, not the destination of the intended contribution paper.

Stages 12–15 of the [complete paper roadmap](docs/PAPER_ROADMAP.md) are complete for the frozen within-recording study. Preserve the [selection freeze](experiments/MODEL_SELECTION_FREEZE_V0.1.json), immutable [pre-execution freeze](experiments/FINAL_TEST_FREEZE_RECORD.json), [actual completion record](experiments/FINAL_CAMPAIGN_V0.1_RECORD.json), all scores/thresholds/manifests and consumed attempts. No scientific choices changed after freezing.

The [LaTeX manuscript and package](manuscript/README.md), [findings explanation](docs/FINDINGS_EXPLAINED_V0.1.md) and [post-exposure independent-evidence plan](docs/POST_EXPOSURE_INDEPENDENT_EVIDENCE_PLAN_V0.1.md) are preserved as preliminary records. Author understanding has not been attested. The [18-page PDF](output/pdf/correction-evidence-casper-study.pdf) is compiled and visually checked; see the [build report](manuscript/PDF_BUILD_REPORT.md). O-RC overlaps all eight events, but its sparse point recall and high normal episode rate prevent calling that reliable attack recognition. The primary pair tests correction evidence; both retain progression. Isolated per-method cost and latency quantiles are unavailable, so the report does not claim a measured compute advantage.

The original final holdout cannot become fresh confirmation through a rerun or reshuffle. Outcome-motivated changes are exploratory and must be declared as such. Prior plans/reports remain historical evidence; the completion record supersedes their readiness fields without rewriting frozen inputs. Researcher comprehension and source-specific independent-evidence admission remain separate; no new dataset, generalization claim or publication is admitted. The later writing/PDF entries below are historical milestones; their proposed next-source order is superseded by the baseline-first direction above.

## Evidence and persistent records

- [Complete final report](docs/FINAL_CAMPAIGN_REPORT_V0.1.md), [actual completion and hashes](experiments/FINAL_CAMPAIGN_V0.1_RECORD.json), [all-method summary](experiments/FINAL_CAMPAIGN_V0.1_SUMMARY.json), [metric CSV](experiments/FINAL_CAMPAIGN_V0.1_METRICS.csv), [88 event outcomes](experiments/FINAL_CAMPAIGN_V0.1_EVENTS.csv), [88 recovery outcomes](experiments/FINAL_CAMPAIGN_V0.1_RECOVERY.csv).

- [Freeze/calibration report](docs/CAMPAIGN_FREEZE_AND_CALIBRATION_REPORT_V0.1.md), [selection freeze](experiments/MODEL_SELECTION_FREEZE_V0.1.json), [actual final freeze](experiments/FINAL_TEST_FREEZE_RECORD.json), [safe summary](experiments/CAMPAIGN_CALIBRATION_V0.1_SUMMARY.json), [324-test report](experiments/SOFTWARE_TEST_REPORT_CAMPAIGN_V0.1.json).

- [Score-extension report](docs/SCORE_EXTENSION_REPORT_V0.1.md), [frozen plan](docs/SCORE_EXTENSION_PLAN_V0.1.md), [295-test report](experiments/SOFTWARE_TEST_REPORT_SCORE_EXTENSION_V0.1.json), [safe summary](experiments/SCORE_EXTENSION_V0.1_SUMMARY.json), [extension artifact registry](experiments/SCORE_EXTENSION_ARTIFACTS_V0.1.json).

- [Contribution and evidence scope](docs/CONTRIBUTION_AND_EVIDENCE_SCOPE.md), [eleven-variant comparison design](docs/COMPARISON_ROSTER_DECISION.md), [independent-evidence plan](docs/INDEPENDENT_EVIDENCE_PLAN.md).
- [Periodic alignment prior art](docs/literature/PERIODIC_ALIGNMENT_PRIOR_ART_2026-10-17.md), [innovation/synchronization prior art](docs/literature/INNOVATION_SYNCHRONIZATION_PRIOR_ART_2026-10-17.md), [independent-source screen](docs/literature/INDEPENDENT_EVIDENCE_SCREEN_2026-10-17.md). These are bounded primary-source audits, not exhaustive novelty proof or new baseline executions.

- [Observer validation report](docs/OBSERVER_VALIDATION_REPORT.md), [frozen plan](docs/OBSERVER_VALIDATION_PLAN.md), [scientific review](docs/OBSERVER_SCIENTIFIC_REVIEW.md), [254-test report](experiments/SOFTWARE_TEST_REPORT_OBSERVER_V0.1.json), [aggregate results](experiments/OBSERVER_V0.1_SUMMARY.json), [observer artifact registry](experiments/OBSERVER_ARTIFACTS_V0.1.json).

- [Control-study report](docs/CONTROL_STUDY_REPORT.md), [declared model plan](docs/SIMPLE_CONTROLS_PLAN.md), [205-test report](experiments/SOFTWARE_TEST_REPORT_CONTROLS_V0.1.json), [safe run summary](experiments/CONTROLS_V0.1_SUMMARY.json), [selected-control registry](experiments/SELECTED_CONTROLS_V0.1.json).

- [Pilot report](docs/PILOT_REPORT.md), [safe run summary](experiments/PILOT_V0.1_SUMMARY.json), [150-test report](experiments/SOFTWARE_TEST_REPORT_PILOT_V0.1.json), [historical 83-test foundation](docs/SOFTWARE_VALIDATION.md), [environment](docs/ENVIRONMENT.md), [historical pilot plan](docs/BOUNDED_PILOT_PLAN.md), [pilot JSON](configs/casper_right_arm_pilot_v0.1.json).
- [Evaluation protocol](docs/EVALUATION_PROTOCOL.md), [metric formulas](docs/METRIC_DEFINITIONS.md), [final-test protection](docs/FINAL_TEST_PROTECTION.md), [evaluation JSON](configs/casper_right_arm_evaluation_v0.1.json), [actual final freeze](experiments/FINAL_TEST_FREEZE_RECORD.json).
- [Evaluation design review and dispositions](docs/EVALUATION_PROTOCOL_REVIEW.md) is historical; subsequent model-specific tests and the complete final campaign are recorded in the joint report above.
- [Current comparator admission decision](docs/COMPARATOR_ADMISSION.md), [admission rules](docs/BASELINE_SELECTION_CRITERIA.md), [historical selection screen](docs/BASELINE_SELECTION_REPORT.md), [literature register](docs/LITERATURE_EVIDENCE.md).
- [Received-file identity](docs/CASPER_DATASET_IDENTITY.md), [receipt manifest](datasets/manifests/casper_v3_receipt.json), [manuscript/code collection](docs/MANUSCRIPT_COLLECTION_AUDIT.md), [proposed protocol](docs/COMPARISON_PROTOCOL.md).
- [Current release/hash/clock register](docs/DATASET_IDENTITY_REGISTER.md), [consolidated manifest](datasets/manifests/casper_v3_identity.json), [checksum file](datasets/manifests/casper_v3.sha256), [label/time review](docs/CASPER_LABEL_TIME_AUDIT.md), [paper-specific dataset correspondence](docs/BASELINE_DATASET_CORRESPONDENCE.md).
- [Selected question and threat model](docs/RESEARCH_QUESTION_AND_THREAT_MODEL.md), [annotation/features/splits](docs/ANNOTATION_FEATURE_SPLIT_CONTRACT.md), [contract JSON](configs/casper_right_arm_contract_v0.1.json), [design critique](docs/RQ_CONTRACT_REVIEW.md).
- [Complete sensor schema](docs/CASPER_SENSOR_SCHEMA.md), [annotation and score lineage](docs/CASPER_ANNOTATION_LINEAGE.md), [code study](docs/BASELINE_CODE_STUDY.md), [pinned source/result pack](baselines/SOURCE_PACK_MANIFEST.json).
- [Paper-to-code reading coverage](docs/PAPER_CODE_TRACEABILITY.md), [CASPER notes](baselines/casper/READING_NOTES.md), [TWINE notes](baselines/twine/READING_NOTES.md), [CatBoost notes](baselines/catboost/READING_NOTES.md).
- [Open data](docs/literature/OPEN_DATASET_SCREEN_2026-10-16.md), [comparator manuscripts/code](docs/literature/COMPARATOR_SCREEN_2026-10-16.md), [twin methods](docs/literature/TWIN_METHOD_SCREEN_2026-10-16.md).
- [Access/receipt checklist](docs/DATASET_ACCESS_CHECKLIST.md), [proposed reproduction plan](docs/REPRODUCTION_PLAN.md), [work log](docs/WORK_LOG.md).
- [Shared publication standards](../docs/PUBLICATION_STANDARDS.md) and [repeatable playbook](../docs/RESEARCH_PLAYBOOK.md) remain in force. No title, venue, authorship or publication outcome is finalized.

## Manuscript handoff — 17 October 2026

Intended author order confirmed by the user: **Muhammad Usman; Haiqa Mushtaq**. Affiliations, actual roles, funding/conflicts, corresponding author and both-author approval remain pending. The draft maps 65 marked claim groups to evidence and includes 13 verified/source-qualified references; all eleven methods and all event/recovery outcomes remain visible. Offline presentation checks passed; no raw observations opened, no new model run, no new data, no independent reproduction or submission. The next evidence candidate is voraus-AD for a separately scoped physical-anomaly study; NIST is a benign-condition route. Neither is received/admitted, and neither alone establishes cyber intent. See [internal review](manuscript/editorial/INTERNAL_REVIEW.md).

## PDF handoff — 17 October 2026

The requested [manuscript PDF](output/pdf/correction-evidence-casper-study.pdf) is built and all 18 pages inspected. Final compilation reports no warnings; references, glyphs, formulas, plots and tables render correctly. The [build/review receipts](manuscript/PDF_BUILD_REPORT.md) preserve exact identities and remaining limits. Only formatting changed; all numeric table/macro bytes and frozen experiment bindings remain unchanged. Author declarations/approval, venue fit and independent evidence remain pending. No dataset access or model execution occurred.
