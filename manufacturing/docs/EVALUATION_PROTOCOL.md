# Evaluation plan for the CASPER right-arm study

## Material Passport

- Project / owner: manufacturing / Haiqa Mushtaq.
- Origin: academic-research-suite, experiment-agent, **plan** workflow.
- Date / version: 16 October 2026 / `casper-right-arm-evaluation-v0.1`.
- Status: **evaluation rules defined and metadata reviewed; implementation, fitting, calibration and final evaluation not executed**.
- Scope: selected normal-only Group D. This supplements the unchanged [data contract](ANNOTATION_FEATURE_SPLIT_CONTRACT.md); it does not merge the earlier external-IMU or supervised tracks.

The question is whether retaining a nominal cycle-progression reference during state synchronization improves detection of the recorded right-arm speed changes. This is a paired algorithm comparison on one existing acquisition, not a randomized plant experiment. The [question and threat model](RESEARCH_QUESTION_AND_THREAT_MODEL.md) restricts the security interpretation to command-path manipulation with truthful joint telemetry and time assumed. Scheduled changes do not prove malicious intent or independently measured physical onset.

Read this entry point with the [metric definitions](METRIC_DEFINITIONS.md), [final-test protection procedure](FINAL_TEST_PROTECTION.md), [evaluation configuration](../configs/casper_right_arm_evaluation_v0.1.json) and [pending freeze record](../experiments/FINAL_TEST_FREEZE_RECORD.json). The configuration contains planning metadata, not a runnable detector. The metric document is authoritative for metric formulas; the protection document is authoritative for outcome access. These later rules resolve previously open evaluation details for Group D only. Any disagreement must be resolved and versioned before execution.

## 1. Exact chronology and permitted use

Source: original CASPER v3, `right_arm.csv`, 1,762,650 data rows, SHA-256 `181662e25de09c1f4ed05e0877a65c40225752d6f54575ddb1cdf8a0cf29a334`. Rows below are zero-based, exclude the CSV header, and use an excluded upper bound. CSV record number is row + 2. Raw bytes remain unchanged.

| Partition | Rows `[start, end)` | Raw rows | Eligible endpoints | Permitted purpose |
|---|---|---:|---:|---|
| Training | `[0, 540002)` | 540,002 | 536,946 | Fit transforms, nominal references and model parameters |
| Normal development | `[540002, 702002)` | 162,000 | 160,472 | Choose configurations/checkpoints using a predeclared normal-only objective |
| Normal calibration | `[702002, 864003)` | 162,001 | 160,473 | Compute each frozen detector's threshold only |
| Protected normal | `[864003, 1080004)` | 216,001 | 214,473 | Final normal alarm burden and coverage |
| Protected mixed | `[1080004, 1762650)` | 682,646 | 682,646 | Final schedule agreement and all eight event outcomes |

The first four ranges are cumulative 50%, 65%, 80%, 100% boundaries of the initial 1,080,004-row schedule-zero prefix, rounded down. They are not random row splits or independent acquisitions. The last two ranges form **one continuous final replay** `[864003, 1762650)`, with 898,647 raw rows and 897,119 eligible endpoints. The mixed slice contains 345,602 schedule-positive and 337,044 schedule-zero rows. Later zero rows remain final recovery/inter-event observations; they cannot become calibration data.

Split before all filtering, window construction or fitted preprocessing. Fit scalers, nominal trajectories, residual normalization and other learned transforms on training only. Use development only to select among a finite declared set, without fitting transforms to it. No model-selection objective may use final labels, final distributions or alarm performance. Method-specific normal prediction/state-validation objectives and configuration grids still need definition before the pilot. There is no meaningful attack F1 to optimize on a normal-only development block; low normal residual alone does not establish attack sensitivity.

## 2. Causal state, gaps and common score support

Inputs remain six actual joint positions, six actual joint velocities, and relative elapsed time for propagation/gap handling. Labels, absolute timestamps, row/event IDs, safety status, other modalities and future samples are excluded from detector features. The evaluator retains coordinates separately to align outputs.

Initialize state separately at training, development, calibration and final-replay starts. Break continuity on nonpositive time increments, increments above 0.075 seconds, or invalid permitted observations. Never impute across a gap. The audited 0.1-second gap restarts training at row 16,571. It is the only observed right-arm break under this rule. A future loader must confirm the evidence; an unexpected discrepancy blocks admission instead of silently redefining the mask.

Every stream segment has a common warmup of 1,528 preceding observations. This yields training support `[1528,16571)` and `[18099,540002)`, development `[541530,702002)`, calibration `[703530,864003)`, and final `[865531,1762650)`. A recurrent state may use all preceding observations within its segment; this warmup is not a bound on total state memory. Final state continues across row 1,080,004 and every label transition. There are no event-driven resets or fresh warmups inside the mixed slice.

The common support remains conditional on model histories being feasible. If a model needs more initialization, revise the common policy before calibration and final outcomes; do not trim its difficult rows afterward. Require one finite, correctly aligned score at **every** structurally eligible endpoint. Unexpected missing/nonfinite scores, duplicate endpoints or abstentions fail that run's comparative admission. Keep failure and coverage records; neither dropping rows nor taking a favorable common intersection is allowed. These stricter admission rules resolve the older contract's general coverage language.

Prediction uses past state; score the current observation before correcting state with it. The dynamic state may evolve under the declared correction rule. Fitted references, parameters, residual distributions and thresholds remain fixed throughout calibration and final replay. No online adaptation is part of this study.

## 3. Calibration after model selection

Before calibration, freeze the finite model/ablation roster, all selected configurations/checkpoints, score definition and direction, initialization, feature transformations, seed policy and selection/tie rules. The primary matched contrast is progression-aware versus progression-omitted synchronization. Mandatory simple velocity and nominal-template controls remain; an ordinary causal predictor and any CNN port need explicit implementation specifications. The three learning papers are not an admitted unchanged three-way comparison.

For each selected model/seed, use all 160,473 finite eligible normal-calibration scores. Sort ascending, take one-based rank `ceil(99*m/100)`, and alarm only when `score > threshold`. At the current `m`, rank is **158,869**. There can be at most 1,604 strictly greater calibration scores; ties may reduce that number. This is an empirical operating point, not a guarantee of future 1% false alarms.

Calibration determines this one number per frozen artifact. It cannot rank models, select seeds, fit a residual covariance, choose fusion weights, change persistence, retune the percentile or select a second operating point. Equal scores are non-alarms; no interpolation or jitter. Invalid/incomplete calibration blocks evaluation. No refitting on training plus development after calibration is included. Save exact thresholds, dtype, input/score hashes and exceedance counts without turning those values into a new development search.

## 4. Outcomes and repeats fixed before testing

The following are a joint comparison, with no post-hoc composite winner:

- **Mixed-slice point performance:** positive-class unadjusted precision, recall and F1, with TP/FP/FN/TN and fixed support. No point adjustment, window-majority labels or test-selected thresholds.
- **Protected-normal burden:** alarm-positive fraction and observed alarm episodes per eligible hour, with actual native-time exposure, counts, censoring and coverage.
- **Coverage:** raw versus structurally eligible versus finite-scored counts; complete eligible coverage is required for admission.
- **Supporting outcomes:** tie-grouped noninterpolated average precision; all eight event overlap/fresh-onset outcomes and schedule-relative delays; mixed zero/recovery alarm burden; measured computational cost.

The [metric specification](METRIC_DEFINITIONS.md) fixes formulas, undefined cases, exposure and synthetic acceptance examples. A sustained pre-existing alarm can overlap a scheduled event without a fresh onset. Do not report its zero overlap delay as a newly triggered detection. All eight intervals stay in the denominator, and detected-only delay summaries must show misses. Processing time is distinct from detection delay and transport latency.

Final stochastic seeds are **17, 42, 2026**, paired across matched variants. Deterministic controls run once. A proposed implementation pilot uses seed 42 on training/development only. Record every declared run, failure and per-seed outcome; no seed ranking, pooling of rows across seeds, post-hoc ensemble or successful-run-only average. For complete defined values report unweighted mean, median and min/max, alongside paired differences. If any replicate's metric is undefined, its aggregate is undefined with counts/reasons. A failed run cannot disappear from the declared matrix.

Report `progression-aware minus progression-omitted` differences jointly for F1, normal point exceedance and normal episodes/hour, with coverage. Different desirable signs reflect a trade-off; state it explicitly. No minimum-effect or superiority claim is established by this specification. Seeds measure computational variability on one acquisition, not independent robots. No independent-row, event or seed significance tests/confidence intervals are planned.

## 5. Protect both final slices and freeze before release

Prior metadata/schema/label/time audits and author results have been inspected. Our model outcomes have not. The public CSV is already locally accessible, so protection is **procedural**, with planned developer/evaluator interfaces; no OS lock, blinding or independent custodian exists. From this plan onward, final feature plots/statistics, segmentation, scores and outcomes cannot guide development, even without using attack labels.

After model selection and threshold calibration, record actual hashes for code, environment, fitted transforms/references/checkpoints, thresholds, split/mask and evaluator tests. Only then can the separately scoped final campaign proceed. The [freeze record](../experiments/FINAL_TEST_FREEZE_RECORD.json) leaves absent artifacts and timestamps null; an empty roster is not a completed freeze.

Generate and hash all declared score artifacts before label joining and report release. Each registered run must reach a recorded terminal state; failed runs retain their failure/coverage artifacts rather than blocking a complete failure report or disappearing from the campaign. Run all frozen methods/seeds as one logical campaign, sequentially if necessary. Do not use early results to redesign later methods. Record accidental/partial outcome exposure and technical retries. Scientific changes after outcome inspection become exploratory; reusing or reshuffling this recording cannot create a fresh confirmatory test. Corrected analyses retain the original records and disclose the correction.

## 6. Next implementation gates

1. Implement a narrow read-only loader and separate evaluator annotation access; validate exact ranges, shared support and feature allowlist without exposing final values to development.
2. Implement the documented metric rules with offline **synthetic** tests for ties, undefined denominators, missing scores, gap/boundary episodes, eight-event support and causal score alignment. Specification arithmetic checks are not these implementation tests.
3. Specify model-specific formulas, normal-only objectives, finite search/tie rules, causal initialization and resource limits. Resolve upstream code-use and faithful-versus-modified designations.
4. Prepare an isolated environment and concrete bounded normal-only pilot plan; record commands and measured feasibility when actually executed. No training command, runtime estimate or completed run is invented here.
5. Freeze selected artifacts, calibrate once, complete the final-freeze record, and only then run the declared final campaign within its authorized scope. Approval remains required for lengthy/paid runs and publication.

One repetitive task, one acquisition, scheduled labels, trusted-telemetry assumptions and incomplete comparator manuscripts remain material limitations. A well-specified evaluation can reveal failure of the proposed mechanism; it cannot guarantee a publishable advantage or physical twin fidelity.
