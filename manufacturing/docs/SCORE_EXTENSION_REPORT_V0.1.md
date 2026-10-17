# Four-score extension: implementation and normal-only validation

## Material Passport

- Project/owner: manufacturing / Haiqa Mushtaq. Local date: **17 October 2026, Asia/Karachi**.
- Scope: user-authorized implementation/tests and one separately versioned bounded normal-only extension; **no fitting, calibration or final access**.
- Workflow: shared academic-research-suite experiment-agent guidance, scoped to local software validation and saved-artifact verification. Separate agents implemented core/runner and performed internal numerical/preflight/postrun review. This is not external peer review or independent empirical replication.
- Plan: [SCORE_EXTENSION_PLAN_V0.1.md](SCORE_EXTENSION_PLAN_V0.1.md), SHA-256 `a5754c9ddb4b18e89c08677b7c661e6993a6b67205418a3cd9df96393234b359`; [configuration](../configs/casper_right_arm_score_extension_v0.1.json), SHA-256 `57876f77ce2f447b127766246d91e0775a1e15de2996946b210adc4ed3fe0497`.
- Result: **one accepted replay**, unchanged model, complete finite scores and exact historical parity. This completes the four-score implementation/development milestone, not security-performance evaluation.

## What changed

Added the pure [score module](../src/mfg_twin/observer_scores.py), [development replay](../src/mfg_twin/score_extension.py), [bounded entry script](../scripts/run_score_extension.py), versioned configuration and two synthetic test modules. Original observer, loader, controls, supervisor, prior tests/configurations/plans, fitted artifacts and consumed attempts remain unchanged.

The new scores are correction-only **C**, classical posterior-to-prior KL surprise **K**, predictive mixture energy **L**, and six-channel prospective velocity residual **Rv**. All use the same existing synchronized proposal and full q/qdot state. R and RC are exported alongside them as exact historical controls. Singleton scores introduce no fitted scales or selection parameters. The original training-only R/C scales remain immutable.

The helper validates probability support, prepared observations, synchronized updates and finite/nonnegative arithmetic. L uses log-sum-exp; K uses log differences and the zero-posterior limit. Tolerances are declared in the frozen plan/configuration. No smoothing fixes invalid support. The original propose → score → commit sequence is retained. The helper cannot detect an already committed proposal on its own; owner/generation enforcement remains with the observer and runner.

## Synthetic validation and preflight

The full offline suite passed **295 tests**, zero failures/errors/skips, in 4.442 seconds: the preserved 254 tests plus **26 score tests and 15 runner/entry tests**. Its receipt binds **46 source/configuration files** and the same isolated Python interpreter. The test audit hook rejects raw-data/network access. Synthetic fixture fitting is not real CASPER fitting or a benchmark result.

Tests cover independent arithmetic and KL orientation, energy/mixture identities, tiny prior support and underflow/overflow, all six velocity channels, exact legacy score arithmetic, unchanged state trajectories, causality, invalid inputs, label independence, fixed support, provenance corruption, no-fit paths, resource failures, saved-array/formula corruption and exclusive attempts. The [test summary](../experiments/SOFTWARE_TEST_REPORT_SCORE_EXTENSION_V0.1.json) points to local receipt `local/software_validation/20261017T055132_395275Z/receipt.json`, SHA-256 `7329b62b0e2ed09632219cfe658248c3b8c3568c7fe20b9fcd2bc6c4cf31dd10`.

A separate **200-case synthetic numerical audit** compared C/K/L/Rv with 80-digit Decimal calculations using seed 20261017 and `rel_tol=1e-12`, `abs_tol=1e-14`. All cases passed. The exact script/source identity and receipt are under ignored `local/score_extension_review/independent_decimal_audit.py` and `independent_decimal_receipt.json`. This numerical audit does not simulate realistic physical attacks.

Preflight caught and corrected missing post-replay byte hashing and incomplete enforcement of the preserved-dependency inventory before any real attempt. Synthetic integration also exposed macOS temporary-path canonicalization and missing initial progress on tiny failing fixtures; these were corrected before the matching full receipt. The local managed shell blocked `/bin/ps`; approved local execution restored the required RSS monitoring rather than removing the limit. No real replay was retried.

## Actual execution and provenance

Commands executed from `/Users/matrixusman/CUI/DigitalTwin/manufacturing`:

```sh
.venv/bin/python scripts/run_synthetic_tests.py
.venv/bin/python scripts/run_score_extension.py --execute --test-receipt local/software_validation/20261017T055132_395275Z/receipt.json
```

Run: `experiments/runs/normal_score_extension_v0.1_20261017T055148_216862Z/`. UTC start/end **2026-10-17 05:51:48–05:52:22**, corresponding to approximately **10:51:48–10:52:22 Asia/Karachi**. Manifest SHA-256 `222c7dab492be668641d7f53772476e92a902f4ee257d5dd68ec8bb951897900`.

Environment: manufacturing-local Python **3.15.0**, standard library only; Apple M5 Pro, 24 GiB memory; deterministic seed `null`, one CPU worker/thread. Git HEAD `b207e0758c1dd90fbd09d3aa4de943a11d7f08cb` plus recorded dirty workspace, exact source/configuration snapshots and patch. No dependency/system package changed. No assistant-issued commit/push occurred.

| Population/identity check | Recorded result |
|---|---|
| Selected observations parsed | **162,000**, development [540002,702002) only |
| Warmup exclusions | **1,528**, state initialization only |
| Eligible scored endpoints | **160,472** per score, [541530,702002) |
| Score streams / total values | **6 / 962,832**, all finite |
| Historical R/RC and coordinates | **Exact byte parity** with the original observer run |
| Fitting / training observations parsed | **0 / 0** |
| CSV records traversed | **702,002**, including 540,002 positioning records whose features were not parsed |
| Whole-source identity checks | **2** byte hashes, 3,956,386,188 bytes total; raw bytes unchanged |
| Model/scales/dependencies | **72** bound inputs unchanged, including **66** historical protected files |
| Calibration/final observations, thresholds, attack metrics | **None** |

The nested population loader counters were captured before the final post-replay hash; the terminal diagnostic counters correctly report both byte scans. Hashing the whole raw file checks identity and is not observation parsing. Prior development arrays were read solely for exact compatibility, not to tune the new scores.

| Resource | Measured | Cap |
|---|---:|---:|
| Supervised worker wall time | **34.015 s** | 600 s |
| Worker CPU time | **33.784 s** | 300 s |
| Worker peak RSS (`getrusage`) | **42.61 MiB** | 1,024 MiB |
| All run outputs, including manifest | **16.30 MiB** | 50 MiB |

There were 136 RSS samples, maximum polling start gap 0.251136 seconds. Sampled peak was 39,534,592 bytes; terminal peak was 44,679,168 bytes. Both passed. RSS monitoring is sampled, not an instantaneous kernel ceiling. The persistent attempt record is consumed and retained; no repeat is authorized by this report.

## Score summaries and their limits

Each row below covers the same 160,472 normal-development endpoints. Scores have different meanings/scales; **their means are not performance rankings** and did not select a preferred method.

| Score | Minimum | Mean | Maximum |
|---|---:|---:|---:|
| R, scaled | 0.000001339 | 0.998484 | 26.678739 |
| RC, scaled | 0.049528 | 1.997631 | 33.463853 |
| C, raw JSD | 0.000091897 | 0.001854064 | 0.024737071 |
| K, raw KL | 0.000295471 | 0.006835573 | 0.094063922 |
| L, predictive energy | 0.000701173 | 0.546695554 | 13.683644436 |
| Rv, standardized velocity residual | 0.000000138 | 0.544908733 | 18.097849005 |

The original R and RC file hashes remain `aeac99c18828d9cd6686941cdde725d2c07038ae13ca2118c6301a64968e7dba` and `b150d02208d2bd71f05d2a5734a4f143dddd2b85a364d2d8548e733d82c69f5b`. Full-precision aggregates and all six output hashes are in the [safe summary](../experiments/SCORE_EXTENSION_V0.1_SUMMARY.json); row-level files remain ignored.

## Independent internal verification and decision

The runner's complete readback accepted lengths, ordered coordinates, finite values, hashes, unchanged inputs, exact prior parity, `RC=R+C/b`, the JS bound and `Rv<=2aR` within declared numerical tolerance. A separate saved-artifact audit passed **257 checks** covering every artifact/hash/size, test/source provenance, immutable model/scales, all scores/coordinates, scope counters, attempt ledger and resources. Receipt `local/score_extension_review/saved_artifact_audit.json`, SHA-256 `98e10078d5da25f4dfd3dc8d270b5177f573d126dfeb3ba04cab688ea4b38222`.

The reviewer opened saved artifacts only, without raw replay. This integrity audit is not a new acquisition, independent detector reproduction or attack evaluation. Per-endpoint posterior/component histories were not exported, so it does not independently reconstruct every real K/L value from those histories; their arithmetic is supported by tested source, high-precision synthetic cases and recorded execution. Rv's saved subset bound is not a full reconstruction from original velocities.

**The requested milestone is complete:** four scores implemented/tested, one accepted bounded normal replay, exact preservation of the existing observer's outputs and saved artifacts. All eleven core score/control variants have now been implemented and exercised on normal development across the preserved studies. The historical [roster decision](COMPARISON_ROSTER_DECISION.md) remains unchanged as a pre-extension snapshot; current readiness is recorded here and in the [extension registry](../experiments/SCORE_EXTENSION_ARTIFACTS_V0.1.json).

**Still unproved:** incremental attack-detection benefit, novelty, physical-twin fidelity, calibrated uncertainty and cross-acquisition generalization. Reused normal-development observations cannot answer those questions. No threshold or final result exists. Next prepare the complete executable-roster/threshold-calibration admission, with exact frozen artifact identities and tests for the calibration-only path. The current final-freeze record and both final slices remain unchanged and closed.
