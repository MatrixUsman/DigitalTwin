# Loader, split isolation and metric implementation

Historical **83-test foundation milestone** below, preserved as executed. The subsequent [pilot report](PILOT_REPORT.md) records the expanded **150-test suite**, control/supervisor implementation and one completed real normal-only pilot. Earlier statements about absent models/readiness apply to this document's original milestone; current handoff is [STATUS.md](../STATUS.md).

## Material Passport

- Project / owner: manufacturing / Haiqa Mushtaq.
- Origin: academic-research-suite, bounded implementation and validation guidance; user-authorized software work.
- Date / version: 16 October 2026 / implementation v0.1.
- Status: **83 explicitly synthetic software tests passed; no real-data fitting, calibration, final evaluation or baseline reproduction**.
- Authority: unchanged [data contract](ANNOTATION_FEATURE_SPLIT_CONTRACT.md), [evaluation rules](EVALUATION_PROTOCOL.md) and [metric definitions](METRIC_DEFINITIONS.md).

The first implementation now exists. It is a small standard-library Python package with separate detector observations and evaluator metadata. The tested cases establish behavior on invented inputs and the existing metadata contracts. They do not establish compatibility with every real record, attack sensitivity, physical twin fidelity or experimental comparator admission.

## Implemented boundaries

| Module | Implemented behavior |
|---|---|
| [data.py](../src/mfg_twin/data.py) | Read-only CSV parsing against the original 20-column schema; six q and six qdot values; native Decimal timestamps; strict labels; half-open partitions; explicit invalid-feature/gap/warmup handling; causal feature-only windows |
| [contract.py](../src/mfg_twin/contract.py) | Hash-bound data/evaluation metadata, source size/SHA verification on one opened file, bounded training/development prefixes, frozen support/reset validation, and rejection of calibration/final access before opening the source |
| [replay.py](../src/mfg_twin/replay.py) | Detector receives only immutable q/qdot/relative-time observations; score before state update; explicit resets; no score during warmup; rejection of omitted/reordered inputs or nonfinite scores |
| [metrics.py](../src/mfg_twin/metrics.py) | Strict nearest-rank calibration, complete-domain/mask admission, unadjusted counts/P/R/F1, tied-score AP, coverage, alarm episodes/censoring/exposure, declared event outcomes and schedule-relative delay |

Only real stream partitions are represented as loader streams. The final normal and mixed reporting slices do not create separately initialized streams. Metadata can describe their bounds without exposing their observations. The current production wrapper admits **only training and development**; a future calibration/final runner must implement artifact-freeze admission separately. Passing a hand-built synthetic `Study` in tests does not authenticate a production source. Real use starts from `load_study`, which checks the registered metadata hashes.

The low-level CSV parser and pure metric functions are reusable primitives, not security sandboxes. A person with local file access can bypass them. Caller-owned streams must begin at the header, and iterators must be fully consumed to establish requested length. CSV positioning may tokenize earlier records, and ordinary buffering may read ahead in bytes. Before parsing a production prefix, the wrapper hashes the complete source for integrity; this technical byte read does not parse protected feature values or compute their statistics. None of those production reads happened in this milestone.

All dataset labels, original row coordinates, native absolute timestamps and source paths stay outside the detector observation type. The replay coordinator enforces call order, but cannot prove that a future model's internal predictor is causal. Model-specific state/fit tests remain mandatory. Generic `evaluate` requires an independently supplied domain, eligibility mask and complete event list; it does not authenticate their dataset origin. No final-release runner exists yet.

## Executed checks and recorded correction

The final suite contains **9 contract tests, 28 loader tests, 9 integration tests and 37 metric tests**, with zero failures, errors or skips. See the [machine-readable software report](../experiments/SOFTWARE_TEST_REPORT.json). Test fixtures are generated in memory or temporary files and explicitly named **synthetic**; none comes from CASPER observations.

Coverage includes malformed/short CSVs, invalid vector shapes and nonfinite values, label/feature separation, exact warmup, timestamp/gap resets, no history crossing partitions, no requested record beyond a partition end, future-suffix invariance, strict threshold equality, tied AP, undefined denominators, missing/duplicate/misaligned output rejection, episode continuity across reporting boundaries, all-eight-event denominators and censoring. An integrated artificial stream exercises loader → causal coordinator → calibration/metrics; its invented scores are not benchmark results. A Python audit hook blocks raw-dataset file opens and network operations during the suite. It is a process-local check, not an OS sandbox; no blocked attempts occurred in the final run.

The initial integrated run passed 80 tests. A separate shared-context internal reviewer then found an uncovered issue: ambient Decimal precision could round exposure and delay, even though the timestamp inputs were unchanged. The implementation now uses exact rational arithmetic for native-time differences/sums and context-independent Decimal construction. Three additional regressions cover hostile precision/rounding/traps, a nonterminating episode rate, and eight intervals overlapped by one pre-existing alarm with no fresh onsets. The final 83-test run passed. Both receipts are retained locally; the earlier pass did not establish correctness for the newly discovered case.

The loader reviewer also prompted successful-wrapper tests, invalid-observation rejection inside warmup, and separation of reporting slices from continuous replay. These reviews are internal software checks, not external peer review or a proof that no defects remain.

## Re-running the software checks

From the manufacturing project root:

```sh
.venv/bin/python scripts/run_synthetic_tests.py
```

The command discovers offline `unittest` tests and saves an ignored `local/software_validation/<UTC-run-id>/` receipt, test output, source snapshot and tracked dirty patch. It records exact source/config hashes, interpreter, platform, dependencies, command, revision/dirty state, duration and failures. Synthetic tests are deterministic; no fitting seed is used. The runner fails if checked source files change during testing. The current package has no third-party dependencies or network setup. See [ENVIRONMENT.md](ENVIRONMENT.md) for the actual environment and recreation command.

The earlier frozen evaluation JSON contains historical planning readiness fields. Its bytes remain unchanged; current implementation status is this report and [STATUS.md](../STATUS.md). The [final-freeze record](../experiments/FINAL_TEST_FREEZE_RECORD.json) remains pending. A successful software receipt is one prerequisite, not a complete model/configuration/artifact freeze.

## Remaining work and pilot

The [bounded pilot plan](BOUNDED_PILOT_PLAN.md) specifies one ordinary velocity-deviation control using 46,944 eligible training-prefix rows and 18,472 development-prefix rows. Its reference formula, zero-variance failure rule, single configuration and proposed resource bounds are explicit. The control and supervising runner are **not implemented or executed**. No threshold or final partition is used in that pilot.

Still pending: control/observer model implementations, actual fitted-transform isolation tests, resource supervision, production calibration/final admission, immutable run artifacts, seed-summary/report assembly, runtime/memory instrumentation and baseline reproduction. CASPER, TWINE and CatBoost retain their separate manuscript, information-access, protocol and code-use admission gaps. These software tests do not admit them as fair comparators.
