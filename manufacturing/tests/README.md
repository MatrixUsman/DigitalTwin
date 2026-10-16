# Synthetic software tests — Smart manufacturing

The initial loader/metric suite now has **83 passing synthetic tests**, recorded in [SOFTWARE_VALIDATION.md](../docs/SOFTWARE_VALIDATION.md) and the [test report](../experiments/SOFTWARE_TEST_REPORT.json). No benchmark execution exists. Implemented cases cover:

- Read-only loading, header handling, schema and feature/label/timestamp alignment.
- Chronological splits and window isolation across partitions, episodes and gaps.
- Blocked calibration/final source access, feature/label separation and isolated synthetic calibration; actual training-only fitted-transform validation remains for future models.
- Known-value metric cases, denominators, event boundaries and detection latency.
- Causal replay: changing future samples cannot alter earlier decisions.
- Run/configuration/dataset provenance and repeatability where supported.

The suite implements [the metric specification's synthetic cases](../docs/METRIC_DEFINITIONS.md): strict threshold equality, nearest-rank quantiles, tied AP, undefined denominators, eight-event support, fresh onset versus overlap, censoring and native-time exposure. It rejects missing/nonfinite/duplicate/misaligned scores and checks continuity across reporting boundaries. Decimal precision/rounding/trap regressions preserve exposure/delay. Model-specific history/fit behavior still needs tests before admission. Earlier metadata checks in `local/evaluation_protocol_review/` are distinct from this executable suite.

Fixtures are explicitly synthetic functions in the test modules, generated in memory or temporary directories; no real observations are copied into the repository. From manufacturing, run `.venv/bin/python scripts/run_synthetic_tests.py`. The runner records a source snapshot, log and receipt, blocks raw paths/network through a process-local audit hook, and needs no third-party packages. Synthetic checks never establish benchmark performance. Add domain-specific physical-consistency checks only where their assumptions are justified.
