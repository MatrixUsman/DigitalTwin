# Model freeze and normal calibration — completed

## Material Passport

Manufacturing / Haiqa Mushtaq; 17 October 2026; academic-research-suite bounded experiment execution and internal validation. Version v0.1. **Executed: actual model freeze, one normal-only calibration, saved-artifact audit, populated final freeze and metadata-only production admission. Final scoring and label evaluation were not executed.** This is calibration/software evidence, not an attack benchmark or independent replication.

## What is frozen

The [selection record](../experiments/MODEL_SELECTION_FREEZE_V0.1.json) was written at `2026-10-17T06:12:20.955125+00:00`, before calibration started at `2026-10-17T06:12:27.592958+00:00`. It binds **52 tested source/configuration files**, **133 saved inputs**, all original candidate outcomes, four existing fitted references, eleven method/ablation definitions and the complete declared run matrix. Full filenames, hashes, original study receipts, transformations, initialization, normal-only selection objective/tie rules and commands are recorded there and in the [campaign configuration](../configs/casper_right_arm_campaign_v0.1.json).

All eleven methods are deterministic: one run each, `seed: null`. Seeds **17, 42, 2026** remain the declared policy for stochastic methods; none is admitted here. No extra fitting, selected checkpoint change, post-calibration refit, percentile search or score combination was performed. The main contrast is **O-RC minus O-R**: both use nominal progression and the same state; the added correction-score term is the only difference. This is the explicit mapping for obsolete progression-omitted terminology in the historical evaluation policy.

The original seven ordinary candidates remain recorded: velocity singleton, template bins 32/64, and AR order 1/4 × ridge .001/.1. Template 32 and AR(4) ridge .001 were selected by normal-development prediction MSE in their earlier study. Observer period/template/scaler, fixed mixing, training-derived temperature and residual/JS means remain unchanged. Four explanatory scores were prescribed before calibration. The original three literature papers are still not three faithful or fair reproduced baselines.

## Actual calibration

One accepted attempt parsed **162,001** observations from `[702002,864003)`, used 1,528 for initialization and saved **160,473 eligible scores per method** at `[703530,864003)`. All scores are finite and aligned; files use explicit little-endian binary64. Detector inputs contain q, qdot and relative dt only. The separate coordinate stream contains all raw calibration rows, including warmup. No labels were interpreted.

For every method, the threshold is ascending one-based rank **158,869**, and alarms require **strictly greater** scores. Every threshold had one exact tie and 1,604 strict exceedances in calibration. These facts only verify the specified quantile. They do not rank methods, measure attack detection or guarantee a future 1% false-alarm rate. Score scales differ; threshold magnitudes cannot be compared as performance.

| Method | Fitted-artifact SHA-256 prefix | Threshold |
|---|---|---|
| O-R | 28a9376bc939… | `13.985559778490424` |
| O-RC | 28a9376bc939… | `16.463814217165016` |
| O-C | 28a9376bc939… | `0.015377372026598208` |
| O-K | 28a9376bc939… | `0.05635036542503125` |
| O-L | 28a9376bc939… | `7.215389156567541` |
| O-Rv | 28a9376bc939… | `9.30218041641827` |
| O-Follow | 28a9376bc939… | `14.83928194200882` |
| O-Free | 28a9376bc939… | `23.009252694772172` |
| V-Z | 6ab61aac8025… | `6.570120518167795` |
| T-32 | f46cd8248eb0… | `4.9056682511855545` |
| AR-4 | f18d2191e41f… | `0.03677493527896336` |

Every observer row shares the same saved observer model file; its mode/score formula supplies the declared ablation. Full artifact hashes and exact thresholds are in the [final freeze](../experiments/FINAL_TEST_FREEZE_RECORD.json) and [safe summary](../experiments/CAMPAIGN_CALIBRATION_V0.1_SUMMARY.json).

Run: `experiments/runs/campaign_v0.1_calibrate_2026-10-17T061227.592687_0000`. Manifest SHA-256: `495642cc7db6060f19a42afaa0c9f988cacc7523d5e73cc3acf9c2c7ae803553`. Completed at `2026-10-17T06:13:20.608899+00:00`.

| Resource | Measured | Frozen cap |
|---|---:|---:|
| Supervised worker wall time | 52.246722 s | 600 s |
| Worker CPU | 52.043006 s | 300 s |
| Worker peak RSS | 52,084,736 bytes (49.67 MiB) | 1 GiB |
| Outputs, including manifest | 19,142,875 bytes (18.26 MiB) | 50 MiB |

These are shared whole-roster measurements, not isolated per-method inference costs. One CPU worker; Python 3.15.0 standard library in the existing local venv; no installations/network/GPU/paid compute. Whole-file pre/post SHA-256 scans covered 3,956,386,188 bytes without interpreting observations; CSV positioning traversed 864,003 records but interpreted only the calibration block. No final record was requested. Buffering/byte hashing is disclosed; this is not OS-level isolation.

## Tests and verification

- **324 synthetic tests passed** in 5.888506 seconds, with zero failures/errors/skips. The 29 added cases exercise all-score alignment, exact old-API parity, immutable fitted references, label invariance including poisoned label strings, partition/mask separation, strict quantiles and ties, failed admission, incomplete/nonfinite/reordered/tampered outputs, delayed joining and failure/attempt retention. Existing supervisor, loader and metric tests remain included. [Receipt summary](../experiments/SOFTWARE_TEST_REPORT_CAMPAIGN_V0.1.json).
- The independent arithmetic readback script `local/campaign_v0.1/review/audit_calibration.py` reconstructed every threshold from saved scores, checked every raw coordinate, rehashed all artifacts and frozen inputs, verified source/support counters and limits, and confirmed no final attempt exists. **162,268 assertions include 162,001 per-row checks; they are not that many independent experiments.** No model was rerun and no raw source was reopened by this audit.
- `--check-final` passed. A further production preflight ran with an audit hook that rejects any raw-dataset open. It accepted the actual freeze and rejected seven synthetic metadata corruptions: missing run, changed seed, threshold, fitted reference, mask, budget and calibration hash. These injected records were never written over the actual freeze.
- Final score/evaluation integration has been exercised with explicitly synthetic recordings only. Saved real calibration scores and source checks establish normal replay; final-size runtime, final labels, detector outcomes and scientific conclusions remain unobserved.

The first focused test command omitted `PYTHONPATH=src` and failed import; the corrected synthetic command passed. Initial default-sandbox freeze collection failed at read-only `sysctl` before creating a freeze or any data-access attempt. The unchanged command succeeded with approved local hardware access. Both are recorded technical setup failures, not failed calibrations. There was **one real calibration attempt, successful**, and no automatic retry.

## Final pipeline ready; final observations still closed

The actual [final freeze](../experiments/FINAL_TEST_FREEZE_RECORD.json) was populated at `2026-10-17T06:13:50.712014+00:00`; SHA-256 `1fd7767bdcd4e5203de7180f9e78cb6d82e35c2d7e2b5564821634fedf295a1d`. Its eleven rows have valid calibration and `final_status: not_started`. Final-start/outcome timestamps remain null because those events have not happened. Actual execution state will be retained in external attempt/access/run records; the freeze itself is the immutable pre-execution specification.

Final scoring and evaluation are separate explicit commands. Scoring initializes once at row 864003, preserves continuity across normal/mixed and label boundaries, and requires 897,119 finite endpoints per method. All eleven streams, coordinates, hashes and a successful supervisor manifest must exist before the separate evaluator can interpret timestamps/labels. The evaluator checks exact joins and frozen annotation events, reports every method, all eight event outcomes with misses, normal and recovery burden, coverage, AP and the paired O-RC minus O-R differences. Scores/coordinates allow episode details to be reconstructed; compact JSON reports retain required counts, censoring and delays.

Access events and failures are logically append-only in `local/campaign_v0.1/`; they are not tamper-proof storage or an independent custodian. No `score-final.attempt.json` or `evaluate-final.attempt.json` exists. Synthetic label joining is not final exposure. Prior public metadata/label inspection remains disclosed in the selection record.

## Commands and handoff

Working directory: manufacturing project root. Completed commands:

```text
.venv/bin/python scripts/run_synthetic_tests.py
.venv/bin/python scripts/run_campaign.py --freeze --test-receipt local/software_validation/20261017T061203_982829Z/receipt.json
.venv/bin/python scripts/run_campaign.py --calibrate
.venv/bin/python local/campaign_v0.1/review/audit_calibration.py
.venv/bin/python scripts/run_campaign.py --prepare-final --calibration-run experiments/runs/campaign_v0.1_calibrate_2026-10-17T061227.592687_0000
.venv/bin/python scripts/run_campaign.py --check-final
.venv/bin/python local/campaign_v0.1/review/audit_final_preflight.py
```

Do not repeat freeze/calibration: their records and attempt are consumed. The next separately authorized task is final scoring followed by delayed evaluation, using the commands already fixed in the selection/final records. Future caps are 900 s wall / 600 s CPU / 1 GiB / 256 MiB for scoring, and 1,800 s / 1,200 s / 1 GiB / 256 MiB for metrics. Output caps account for about 75.3 MiB of final score arrays alone. These are abort ceilings, not measured final runtimes or an execution request in this task. Current calibration's 52.25-second roster replay supports local feasibility but cannot guarantee those final runs finish.

The empirical observer, weak one-step forecast relative to AR, reused development data and one-acquisition/eight-dependent-interval limits are unchanged. No novelty, superiority, validated physical twin, generalization, attack benchmark or publication claim follows from calibration. No scientific choices may be changed in response to its thresholds or later final outcomes.
