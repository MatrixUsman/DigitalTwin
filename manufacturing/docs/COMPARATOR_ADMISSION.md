# Comparator decisions for the manufacturing study

**Current scope update, 17 October 2026:** the [ordinary-control study](CONTROL_STUDY_REPORT.md) and [empirical observer validation](OBSERVER_VALIDATION_REPORT.md) are complete within normal-only development. The [contribution decision](CONTRIBUTION_AND_EVIDENCE_SCOPE.md) now narrows the study to a single-acquisition score comparison. Its [eleven-variant roster](COMPARISON_ROSTER_DECISION.md) retains seven implemented variants and requires four unimplemented explanatory scores. ModernTCN remains a conditional secondary transfer; a recent-paper trio, physical twin and broad performance claim remain unsupported. Historical source decisions below are preserved.

Decision date: **17 October 2026, Asia/Karachi**. Owner: Haiqa Mushtaq. Applies to the selected **Group D normal-only, right-arm q/qdot study**, not water or grids. Prepared through the shared academic-research-suite source-verification workflow. This is an AI-assisted evidence audit, not a record of the researchers' comprehension or an executed comparison.

**The original three learning papers are not admitted as a common experimental trio.** Their dispositions are decided for this study. The current core is a transparent ordinary-control and same-observer score comparison; **ModernTCN remains a conditional modified author-code transfer** for a broader secondary comparison. A controller-input CASPER-inspired CNN remains optional and independently implemented if pursued. No recent paper baseline is execution-ready. The required C/K/L/Rv extensions and their precise roles are in the newer roster decision.

This deliberately separates two claims: all *our eventual reruns* must share the same authorized original-CASPER v3 bytes and protocol; the selected papers do **not** all have published experiments on that same task. The earlier requirement for a published common-data trio remains unsatisfied. We are not presenting a ported method as evidence that its paper evaluated CASPER.

## Original papers: final scope decisions

| Paper | Verified material and unresolved facts | Honest designation for this project |
|---|---|---|
| **CASPER, ACM ToIT 2024** | Corrected full VOR; author notebook at `bff03c9…`. External nine-axis IMU differs from our twelve controller channels. Test-label threshold optimization, missing loaded checkpoint, exact published-run bytes and original code-use permission remain unresolved. | **Separate external-IMU track, on hold.** A controller CNN is an **independent CASPER-inspired reimplementation with disclosed modifications**, not faithful reproduction. Do not copy the original notebook pending verified permission. [Evidence](literature/CASPER_ADMISSION_2026-10-17.md). |
| **TWINE, Internet of Things 2026** | **Full accepted manuscript newly obtained** from QUB; 33 pages, CC BY 4.0. MIT code at `841e119…`. Paper explicitly uses 63 features and supervised random 80/20 splitting. Model, metric and figure correspondence gaps remain. | **Background only for Group D.** A separately designed supervised track is possible but not admitted and must not consume our protected test attacks as training data. Access is resolved; compatibility is not. [Evidence](literature/TWINE_ADMISSION_2026-10-17.md). |
| **CatBoost on CASPER, IEEE Sensors Letters 2026** | Publication/repository connection verified; complete 55-file snapshot at `7f2a691…`. Inspected code uses supervised fitting, synthetic IMU targets, padded modality stacking and preprocessing before random splitting. Full manuscript, original run lineage and code-use grant remain missing. | **Background / critical study only; inspected implementation excluded from Group D.** A clean supervised classifier would be a separately specified modified/independent implementation, not a normal-only comparator. [Evidence](literature/CATBOOST_ADMISSION_2026-10-17.md). |

Two of the three original full manuscripts are available and have received an AI-assisted source audit. CatBoost remains an incomplete full-paper study. No result has been reproduced, and no paper is declared fabricated. Code defects or inconsistencies without exact run mapping are attributed to the inspected source paths, not automatically to every published result.

## Selected comparison design

| Scientific role | Selected method / implementation designation | Current readiness |
|---|---|---|
| Is simple speed amplitude enough? | **Maximum absolute standardized joint velocity**, independent ordinary control. Uses six velocity channels, a permitted subset of the common twelve-channel budget. | Implemented and synthetic-tested; prior subset pilot preserved. A new full-training reference is selected in the separate control study. |
| Is repetition alone enough? | **Frozen periodic-template control**, independent ordinary control. | Implemented, tested and full-training selected: 32-bin fixed-clock template with training-derived period and causal warmup phase initialization. |
| Is ordinary temporal prediction enough? | **Small causal AR/ridge predictor**, independent ordinary control. | Implemented, tested and full-training selected: channelwise AR(4), ridge 0.001, using the predeclared four-candidate normal-development procedure. |
| Does a recent competent nonlinear detector suffice? | **ModernTCN, ICLR 2024**, modified MIT author-code implementation transferred to original CASPER. | Full manuscript, source and license verified at `56a9a2c…`; design candidate selected. Adapter, dependency environment, exact configuration, tests and resource plan pending. It was published on SMD/MSL/SMAP/SWaT/PSM, **not CASPER**. |
| Does additional correction evidence contribute? | **Same observer R versus R+C**, our independent implementation/ablation; both retain nominal progression and identical states. | Implemented and normal-only validated: 254 tests, 7 internal checks and 48 saved-artifact checks. Empirical observer only; attack benefit unknown. Required C/K/L/Rv explanatory scores are design-only. |
| Optional directly related nonlinear family | **Controller-input CASPER-inspired CNN**, independent reimplementation. | Conditional design candidate. Fix changes to sensors, normalization, score support and calibration before implementation; original author code is not authorized for copying by this audit. |

The simple controls are necessary scientific tests, not recent papers and not a way to count three papers. ModernTCN is selected for its normal-only learning objective, available complete source and explicit permission, not a claimed headline ranking. No evidence yet establishes that it is the strongest method on these observations. The [replacement screen](literature/REPLACEMENT_COMPARATORS_2026-10-17.md) documents PINC, VARADE and related robotics methods, including inaccessible manuscripts and why none establishes the missing published trio. Additional close competitors may be needed after implementing the proposed mechanism and reassessing prior art.

## Non-negotiable transfer rules and execution gates

The existing [feature/split contract](ANNOTATION_FEATURE_SPLIT_CONTRACT.md), [evaluation protocol](EVALUATION_PROTOCOL.md), [metrics](METRIC_DEFINITIONS.md) and [final protection](FINAL_TEST_PROTECTION.md) remain unchanged. Selection of this design does not open calibration or either final slice.

**Score-interface gate identified during independent review:** ModernTCN reconstructs the current endpoint using a window that contains it, including its contribution to per-window normalization. This is an online, current-conditioned reconstruction score, **not a past-only forecast**. The frozen protocol says “Prediction uses past state.” Before execution, document whether that sentence scopes predictive/state-estimator methods and permits separately named reconstruction controls, or requires a versioned protocol amendment. Do not silently reinterpret it or change ModernTCN into a forecasting objective while retaining the original method label. Future-suffix invariance proves absence of future input, not past-only prediction. This reconciliation remains an explicit admission gate.

For ModernTCN, the audited implementation uses test features for SWaT validation, evaluates a test loader during training, combines training/test scores for threshold selection, and applies label-based point adjustment. Those paths are **not admitted**. The transfer must:

1. Receive only allowed q/qdot observations; use relative time for alignment/gaps, not absolute timestamps, indices or labels as features. Fit external scaling only on the defined training observations. Handle constant/nonfinite channels explicitly before admitting a run.
2. Use a trailing 100-observation window wholly within a valid segment. Score only its reconstructed **current endpoint**, using mean squared standardized-channel error. No interior-window prediction is treated as an online score; no overlap flattening or future suffix access. Preserve the common 1,528-observation warmup and entire fixed eligible support.
3. Use training-only reconstruction loss and a finite, declared normal-development checkpoint policy. Remove development's test loader entirely. Evaluation mode and frozen parameters/scaler must hold during replay; per-window normalization may use only available trailing context.
4. Record one explicit architecture/optimizer/epoch configuration and the project's declared seeds. The paper's default (one block, ten epochs) and SWaT script (three blocks, two epochs) differ; no uniquely matched published configuration is asserted. Resolve this before fitting, without attack outcomes.
5. Export raw aligned scores to our common calibration/evaluator. No oracle threshold, point adjustment, test-derived anomaly proportion or best-seed selection. Calibration follows model freeze; all variants/failures remain reportable.
6. Pass synthetic tests for causal endpoint alignment, future-suffix invariance, gap/split isolation, train-only fitting, label separation, closed calibration/final access and complete finite coverage. Pin/validate dependencies in a separate local environment; the current standard-library Python 3.15 pilot environment is not a validated PyTorch/TensorFlow environment. Specify a new finite resource-bounded pilot before real fitting.

The independent CASPER-inspired variant needs the same safeguards plus an explicit published-equation-to-new-code derivation and deviation ledger. Four 32-filter/kernel-5 convolution layers, pool-3 stages and a 755-step predictor are identifiable in the source family, but retaining those choices does not resolve controller-unit scoring, total support or computational feasibility. Do not substitute an unspecified CNN and call it a reproduction.

**Admission levels:** literature/role selection is complete for the original trio and the proposed transfer design; numerical configuration, adapters, tests and execution admission are not. The user's stronger finish condition—an entirely implementation-ready fair suite—is therefore **not yet met**. That gap is recorded rather than filled with incompatible supervised methods.

## Requested control and bounded runner: completed evidence verified

This coding milestone was completed in the preceding authorized task; it was not run again during this literature audit. [Implementation/report](PILOT_REPORT.md): streaming Welford training mean and population variance, immutable reference, maximum absolute standardized velocity, explicit failure for constant/nonfinite channels, and no development update of fitted statistics. The supervisor enforces **600 s wall, 300 s CPU, 1 GiB monitored RSS and 50 MiB outputs**; it records provenance and preserves partial failures. Sampled RSS is monitoring, not an instantaneous kernel memory ceiling.

The [software receipt](../experiments/SOFTWARE_TEST_REPORT_PILOT_V0.1.json) records **150 passing synthetic tests**, including numerical/reference isolation and supervisor failure cases. This audit rehashed all **22** source/configuration entries and found no differences; the completed run-manifest hash also matched. No software changes justified repeating tests or consuming another pilot attempt.

Concrete command, already executed once from `manufacturing/`:

```sh
.venv/bin/python scripts/run_bounded_pilot.py --execute --test-receipt local/software_validation/20261016T192407_763843Z/receipt.json
```

Its persistent attempt ledger prevents replay; do not remove it. The [recorded pilot](../experiments/PILOT_V0.1_SUMMARY.json) fitted 46,944 eligible normal observations and scored 18,472 development observations in 8.626 s wall / 8.571 s CPU, with 27.94 MiB peak sampled RSS and 1.93 MiB outputs. These are technical feasibility measurements, not detection accuracy, a trained twin or a paper result. Calibration and final observations were not parsed. Raw data was not reopened in this follow-up audit.

## Next bounded work

The ordinary controls and empirical observer are preserved. Next specify a separately versioned bounded C/K/L/Rv extension, then implement and validate it on permitted normal data. The [scope decision](CONTRIBUTION_AND_EVIDENCE_SCOPE.md) makes ModernTCN secondary/conditional: resolve its reconstruction interface, exact configuration and dependencies if a broader competitive claim is pursued. No neural training is required just to fill three paper slots. Freeze actual complete artifacts/commands before calibration. CatBoost full text remains unresolved; independent evidence needs its own admission. Historical control/runner records above are not executions from this review.
