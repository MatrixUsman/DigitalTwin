# Full-training simple controls: normal-only study

## Material Passport

- Project / owner: manufacturing / Haiqa Mushtaq; operator: Codex assistant.
- Date: 17 October 2026, Asia/Karachi.
- Workflow: academic-research-suite, bounded experiment implementation, synthetic validation and execution.
- Study: `manufacturing-casper-right-arm-controls-v0.1`.
- Result: **completed and accepted**, one declared attempt; no automatic retry.
- Meaning: three selected ordinary-control artifacts are fitted and ready to supply a later, separately admitted calibration step. No threshold, attack performance, paper reproduction or validated twin is reported.

The requested smaller pilot had already completed successfully. Its [report](PILOT_REPORT.md), 46,944 fitted / 18,472 scored observations, and attempt ledger were preserved. An independent saved-artifact recheck verified its twelve artifact hashes, exact score support, finite values, reference identity and resource limits without reopening raw data or repeating that fit. The new study below is a separately versioned full-training task authorized by the user's subsequent request.

## What was implemented and tested

The [predeclared plan](SIMPLE_CONTROLS_PLAN.md) and [configuration](../configs/casper_right_arm_controls_v0.1.json) specify every formula, input, training population, history, initialization, failure rule and finite selection policy. The existing velocity control is retained. New [ordinary-control models](../src/mfg_twin/controls.py) implement a training-only twelve-channel standardizer, fixed periodic templates and channelwise autoregressive ridge predictors. The [study coordinator](../src/mfg_twin/control_study.py) and [bounded entry point](../scripts/run_control_study.py) preserve all candidates, exact coverage, immutable fitted states and traceable selection.

**205 synthetic tests passed**, with zero failures, errors or skips. These include the preserved 150-test foundation, 39 model tests and 16 runner/selection tests. Checks cover independent ridge arithmetic, known periodic behavior, constant/nonfinite channels, phase and history resets, prediction before current-target assimilation, future-suffix invariance, immutable serialization, development changes leaving fitted parameters unchanged, label independence, protected access, saved-artifact corruption and resource/failure behavior. The full tested inventory contains **34** source/configuration files.

The [safe test summary](../experiments/SOFTWARE_TEST_REPORT_CONTROLS_V0.1.json) points to the detailed receipt. Exact command from `manufacturing/`: `.venv/bin/python scripts/run_synthetic_tests.py`. Receipt SHA-256: `ca56662de1daae37175871bfcaaf728e77367260b070702f82e13fad3073f87f`. Synthetic timing and numerical checks are software evidence, not CASPER benchmark results. An independent internal reviewer also checked eleven synthetic properties and the final plan/configuration/code interfaces before launch; this is not external peer review.

## Actual execution and coverage

Executed once from `manufacturing/`:

```sh
.venv/bin/python scripts/run_control_study.py --execute --test-receipt local/software_validation/20261016T195209_640436Z/receipt.json
```

Run ID: `normal_controls_v0.1_20261016T195243_137443Z`. UTC start `2026-10-16T19:52:43.134879+00:00`; completion `2026-10-16T19:53:34.760167+00:00`. The local project environment used Python 3.15.0, standard library only, Apple M5 Pro, 24 GiB RAM. No dependency installation occurred. All candidates are deterministic: seed is null, not an invented random seed.

| Check | Observed result |
|---|---:|
| Raw training rows parsed | 540,002 |
| Eligible training targets per candidate | **536,946** |
| Raw normal-development rows parsed | 162,000 |
| Eligible development scores per candidate | **160,472** |
| Candidates completed | **7 of 7** |
| Total finite aligned candidate scores | **1,123,304** |
| Training segment starts | Rows 0 and 16,571 |
| Development segment start | Row 540,002 |
| Training / development warmup exclusions | 3,056 / 1,528 |
| Fitted-reference hashes unchanged through development | **7 of 7** |
| Parsed calibration/final observations | **0** |

The loader parsed 702,002 selected observations in total and traversed 1,242,004 CSV data records, including positioning to the development start. It separately hashed the complete 1,978,193,094-byte source twice (3,956,386,188 hash bytes). Byte identity checks do not constitute protected-feature inspection. Both iterators completed source, ordering, gap and support checks. Raw files remained unchanged and read-only.

## Every candidate and the selected artifacts

The selection rule was fixed before fitting: retain the singleton velocity control; choose minimum normal-development prediction MSE within each predictor family, with exact ties following declared order. All models were fitted on the training partition only, and none was refitted on development. The standardizer was identical across template/AR candidates.

| Candidate | Normal-development objective | Decision |
|---|---:|---|
| Velocity maximum standardized deviation | 0.8519599183 mean score; **diagnostic only** | Retained singleton |
| Template, 32 bins | 0.3742228655 prediction MSE | **Selected template** |
| Template, 64 bins | 0.4172537230 prediction MSE | Preserved alternative |
| AR(1), ridge 0.001 | 0.0063150189 prediction MSE | Preserved alternative |
| AR(1), ridge 0.1 | 0.0145156338 prediction MSE | Preserved alternative |
| AR(4), ridge 0.001 | 0.0020935697 prediction MSE | **Selected AR** |
| AR(4), ridge 0.1 | 0.0177945162 prediction MSE | Preserved alternative |

The velocity score has different units from predictor MSE; it is not ranked against those values. Lower normal prediction error does not establish better attack detection. The training-only period estimator selected sampled lag 38, approximately 38 seconds, from 15,043 eligible first-segment observations (753 sampled points). Its full lag curve and alternatives are retained locally. This is the declared estimator's output, not independent validation of a unique physical cycle; coarse sampling, harmonics and ambiguous phase remain limitations.

The [selected-control registry](../experiments/SELECTED_CONTROLS_V0.1.json) binds all three model-file hashes, immutable state hashes, score-file hashes, source run and configuration. Full candidate artifacts are local and ignored. No candidate failure or unfavorable alternative was discarded. No CNN or imported paper method was run.

## Resource limits and provenance

| Resource | Measured | Limit |
|---|---:|---:|
| Supervised worker wall time | 51.376676 s | 600 s |
| Worker CPU time | 51.269773 s | 300 s |
| Peak worker RSS, getrusage | 154,648,576 bytes / 147.48 MiB | 1 GiB |
| Peak sampled RSS | 154,370,048 bytes | 1 GiB |
| All run outputs, including manifest | 18,376,800 bytes / 17.53 MiB | 50 MiB |

There were 204 RSS samples; the maximum interval between sampling starts was 0.252157 seconds. Sampling is not an instantaneous kernel ceiling. Post-run acceptance also checked the worker's CPU and peak-RSS record, rather than relying only on periodic samples. No cap was extended.

The [safe run summary](../experiments/CONTROLS_V0.1_SUMMARY.json) records source/configuration identities, environment, coverage, every objective and resource measurement. The [local run manifest](../experiments/runs/normal_controls_v0.1_20261016T195243_137443Z/run.json) has SHA-256 `a1ccb3c5d00ae2653765978cbc83ba2a6e65a54a621bf5ac216582c8c3ad65a6`. It lists 28 other artifact hashes/sizes, source and specification snapshots, the successful test receipt, dirty-workspace patch, exact commands, logs, progress, model/score artifacts and readback validation.

The configuration SHA-256 is `00e20b3ec3dab586c2ae14e5e8ab60c59648d91b154130fccfa7c95f92cb518a`. Execution recorded Git HEAD `6e9534c85434c76b652e4696043368ad846340df` plus the dirty state and actual source bytes; the HEAD alone is not the implementation identity. All 34 tested source/configuration fingerprints stayed unchanged during the run. The persistent parent and worker attempt records prevent replay of this version.

An independent post-run saved-artifact audit passed **28/28 checks**, including all 28 recorded artifact hashes/sizes, complete inventory, 34 tested/current/snapshot source identities, 1,123,304 finite aligned scores, reference immutability, selected configurations and resource bounds. It read saved outputs only; no raw observations were reopened and no model was rerun. [Audit receipt](../local/control_study_review/postrun_receipt.json).

## Readiness and remaining work

**The requested essential-control milestone is complete:** tested implementations and three selected full-training artifacts exist. These artifacts can supply later calibration after the complete model/ablation roster is fixed and the calibration path is implemented and tested. The [final-freeze record](../experiments/FINAL_TEST_FREEZE_RECORD.json) deliberately remains pending.

Next define and validate the candidate observer/twin and matched synchronization variants, using these ordinary controls as comparisons. Complete any admitted recent-method adapter and justify comparator strength before freezing the final roster. The ordinary template already retains nominal time progression; the proposed twin must explain and test what it adds. Success on one normal development block cannot establish attack sensitivity, novelty, broad manufacturing validity or physical twin fidelity.

No calibrated threshold, final-normal alarm burden, attack F1/AP, event/delay measure, paid computation, upstream-code execution, upload, publication or author contact occurred. The independent source/admission decisions for CASPER, TWINE, CatBoost and ModernTCN are unchanged.
