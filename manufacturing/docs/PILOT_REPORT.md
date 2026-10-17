# First bounded normal-only pilot: completed

## Material Passport

- Project / owner: manufacturing / Haiqa Mushtaq; operator: Codex assistant.
- Workflow: academic-research-suite, bounded experiment implementation, execution and artifact verification.
- Date: **17 October 2026, Asia/Karachi**; run timestamps below use UTC.
- Status: **150 synthetic tests passed; one real normal-only pilot completed and accepted**.
- Model designation: independently implemented ordinary velocity-deviation control. No digital-twin or paper-reproduction claim.
- Governing plan: [unchanged v0.1 specification](../configs/casper_right_arm_pilot_v0.1.json), SHA-256 `5df7c1e6f279aebe482099fe9dfeaeba1eb241df47ce9a93137fbfcbb95870dc`.

The user explicitly authorized both implementation/testing and execution of this bounded pilot. That later instruction supplied the execution authorization missing from the historical plan. Its original `proposed_not_executed` fields remain unchanged; this report and the actual run record describe the subsequent execution.

The resolved record preserves the original model-description block, including its historical `not_implemented` wording. Its separate implementation designation, code snapshots and completed run status record what actually executed; those copied planning labels are not current readiness claims.

## Outcome and what it means

The control fitted all **46,944 eligible training-prefix observations** and produced all **18,472 eligible development-prefix scores**. All six population variances were positive and finite. Saved scores were read back and checked for exact row order, completeness and finite values. The fitted reference's state hash was identical before and after development. There were no missing, duplicated or reordered score endpoints.

This demonstrates that the specified control and local pipeline can process these normal subsets within the declared budget. It does **not** establish attack detection, a useful twin, superiority, novelty, full-partition compatibility or a reproduced baseline. No threshold, alarms, attack metrics or final-normal alarm burden were computed. The pilot reference cannot be promoted into a full-training checkpoint by renaming it.

| Check | Actual outcome |
|---|---:|
| Real attempts / configurations | 1 / 1; deterministic, seed unused |
| Selected training observations parsed | 50,000: raw rows `[0,50000)` |
| Eligible observations fitted | 46,944 |
| Training warmup exclusions | 3,056; starts at rows 0 and 16,571 |
| Selected development observations parsed | 20,000: raw rows `[540002,560002)` |
| Eligible saved scores | 18,472 |
| Development warmup exclusions | 1,528; separate initialization at row 540,002 |
| Total CSV data records traversed | 610,002, including 540,002 positioning records in the development pass |
| Total selected observations parsed | 70,000 |
| Whole-source integrity scans | 2; 3,956,386,188 bytes hashed |
| Source / mask / end-of-stream checks | Completed for both prefixes |
| Reference changed during development | No |
| Calibration/final observations parsed | None |

The loader hashes the complete original file before each selected prefix. Those byte-level integrity scans include the bytes containing protected observations, but do not parse their features or compute their statistics. CSV positioning before development tokenizes records without interpreting their joint values, labels or timestamps. No record at or beyond row 560,002 was requested by the parser. Buffering and public local file access mean this is procedural protection, not OS isolation or a blinded experiment.

## Implemented control and execution boundaries

[velocity.py](../src/mfg_twin/velocity.py) computes per-channel streaming Welford means and population variances, then the maximum absolute standardized joint-velocity deviation. There is no epsilon, clipping, channel dropping, hyperparameter search or development refitting. Joint positions and relative time do not influence the score; labels, absolute timestamps, paths and row numbers never reach the control. The loader uses the declared timing and warmup policy for common eligibility.

[pilot.py](../src/mfg_twin/pilot.py) drains the two bounded loaders, checks exact support, records counts/timing, saves the immutable reference and aligned scores, and verifies saved artifacts. [supervisor.py](../src/mfg_twin/supervisor.py) supplies a wall watchdog, worker CPU limit, sampled RSS checks, bounded logs and aggregate artifact pre/post-write checks. The [entry script](../scripts/run_bounded_pilot.py) requires a passing receipt for the exact current source inventory and interpreter, snapshots code/configuration, verifies worker provenance, and creates exclusive persistent parent/worker attempt records. Another invocation cannot silently repeat this v0.1 attempt.

The worker is one Python computation process/thread using the standard library. The supervising process has a watchdog thread and launches short `ps` monitoring commands; these are supervision overhead, not additional model workers. A process-local audit hook rejects network operations, new worker subprocesses, raw writes and access to other raw members. This is reviewed cooperative software, not a general security sandbox.

Count-only progress records are saved at phase transitions and every 1,000 selected records. If termination prevents final diagnostics, the parent retains the last complete record and labels its counts partial. A forced termination cannot be presented as complete coverage.

## Measured resources

| Scope | Measurement | Declared bound / interpretation |
|---|---:|---|
| Supervised worker wall time | **8.625890 s** | 600 s |
| Entry including preparation/readback, before final receipt write | 8.705577 s | Separate scope from worker timing |
| Worker CPU time | **8.570764 s** | 300 s via `RLIMIT_CPU` |
| Worker peak RSS | **29,294,592 bytes (27.94 MiB)** | 1 GiB monitored abort threshold |
| RSS observations | 35; maximum poll-start gap 0.251148 s | Required interval at most 1 s |
| Run-directory outputs including `run.json` | **2,021,845 bytes (1.93 MiB)** | 50 MiB |
| Fit stage, including loading/hash | 1.517315 s | Prefix-only measurement |
| Fit accumulation/coordination, excluding loader advancement | 0.179989 s | Not a neural-training runtime |
| Development stage, including loading/output | 7.062468 s | Includes positioning and source hashing |
| Fit / development loader advancement | 1.337326 / 3.403956 s | Excludes time suspended at generator yields |
| Fit / development full-file hashing | 0.779421 / 0.673703 s | Included in loader times above |
| Score-function calls, accumulated | 0.048064 s | Excludes loading, output and most coordination |
| Score serialization/output | 3.593888 s | Includes conservative per-write budget checks |

Peak RSS from macOS `getrusage` agrees with the largest sampled `ps` value. `ps` uses 1,024-byte units; macOS `ru_maxrss` uses bytes. The memory limit is monitored rather than an instantaneous ceiling. These measurements describe this machine and this one invocation. They are not deployment latency, an attack-detection delay or an extrapolated full-dataset estimate. No throughput comparison or runtime superiority is claimed.

## Validation and corrections before the real attempt

The [new software report](../experiments/SOFTWARE_TEST_REPORT_PILOT_V0.1.json) records **150 passing tests**, zero failures/errors/skips/expected failures, and 22 source/configuration fingerprints. It extends the preserved [83-test foundation](../experiments/SOFTWARE_TEST_REPORT.json) with 23 velocity, 14 supervisor, 12 pilot-integration and 18 entry/admission tests. Fixtures are explicitly synthetic. Toy subprocesses contain invented workloads; the test harness's process-local raw/network guard does not propagate into children.

Tests cover Welford arithmetic, large offsets, constant channels, overflow/underflow, fixed reference state, label/development invariance, exact prefixes, invalid excluded suffixes, count-only loader statistics, saved-score corruption, source/receipt mismatches, duplicate worker admission, partial-progress recovery, timeout, CPU exhaustion, sampled-memory breach and output quotas.

Pre-run corrections were preserved in the work history:

- The managed sandbox denied `ps`; monitoring failed closed. The tests and pilot subsequently used approved local execution with monitoring enabled.
- A timeout race between supervisor and watchdog was fixed before the passing suite.
- A synthetic fixture initially generated a timestamp failure when its test expected a feature failure; the fixture was corrected. Entry tests also normalized macOS temporary-directory aliases.
- Independent internal review prompted exclusive worker admission, durable partial-progress records, actual worker runtime checks and stricter test-receipt admission. These were completed before the real attempt.

No real-data retry occurred. Internal review and passing tests do not prove the absence of every defect.

A separate post-run internal audit verified all 12 artifact hashes/sizes, the manifest's self-excluding inventory and total byte count, all 22 tested source/configuration fingerprints, attempt/PID correspondence, score coordinates/timestamps, reference identity and every declared resource bound. It read metadata and saved development outputs only; it did not reopen raw data or repeat the pilot. The pending final-freeze record and its referenced specifications remain unchanged.

## Reproducibility and saved artifacts

Working directory: `manufacturing/`. Environment: its isolated `.venv`, Python **3.15.0**, macOS arm64, standard library only; no third-party distributions installed. Exact hardware, interpreter, revision/dirty patch, commands, source/configuration snapshots and hashes are in the run artifacts. No package installation or system-wide change was made.

Executed commands:

```sh
.venv/bin/python scripts/run_synthetic_tests.py
.venv/bin/python scripts/run_bounded_pilot.py --execute --test-receipt local/software_validation/20261016T192407_763843Z/receipt.json
```

The second command is an execution record, not a request to repeat the consumed attempt. Any future real run needs a separately scoped/versioned plan and its own provenance.

- Run ID: `velocity_zmax_pilot_20261016T192422_101078Z`.
- UTC interval: `2026-10-16T19:24:22.098628+00:00` to `2026-10-16T19:24:30.804165+00:00`.
- [Safe aggregate summary](../experiments/PILOT_V0.1_SUMMARY.json).
- [Local complete run manifest](../experiments/runs/velocity_zmax_pilot_20261016T192422_101078Z/run.json), SHA-256 `94f0f5db16491b696742469aabbc3e57b69ce907efe20011143c6fd06f52d6a9`.
- [Local resolved configuration](../experiments/runs/velocity_zmax_pilot_20261016T192422_101078Z/resolved_config.json).
- [Local diagnostics](../experiments/runs/velocity_zmax_pilot_20261016T192422_101078Z/diagnostics.json).
- [Local test receipt](../local/software_validation/20261016T192407_763843Z/receipt.json).

Local run storage also contains `reference.json`, `development_scores.jsonl`, bounded logs/progress, worker-start record, source/specification snapshots and dirty patch. Reference artifact SHA-256: `6a84be2f750742dd51e19b6663eec6fe63f2818e6ed6c61f6c719d88121bcf77`; score artifact SHA-256: `b77c8d42d2e080c7d7b986f91fecd4349b1b7fd83f4457c98869f3d69935f861`. Raw data and numerical run artifacts remain ignored and local. No upload, publication, upstream execution, robot/cloud operation or assistant-issued commit/push occurred.

## Next bounded step

Specify the **full-training velocity control**, a **causal periodic-template control** and a **small causal predictor**, with finite normal-only development objectives, failure rules and measured resource budgets. Fit them only in a separately scoped execution stage. Use permitted normal training/development evidence to decide whether a meaningful nominal cycle/progression model is feasible before building the twin contrast.

Calibration and both final slices remain closed to model development. The [final freeze record](../experiments/FINAL_TEST_FREEZE_RECORD.json) is still pending. CASPER, TWINE and CatBoost remain learning papers with separate manuscript, input/supervision, code-use and published-run admission gaps. This pilot resolves none of those gaps.
