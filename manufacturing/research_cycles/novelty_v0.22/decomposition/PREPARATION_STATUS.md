# Preparation status

24 October 2026. Source/protocol prepared; no checkpoint inference or decomposition run has occurred.

The documented synthetic-test command failed before Python startup with exit 127:

```text
zsh:1: no such file or directory: .venv-forecast-v016/bin/python
```

Inspection found that `.venv-forecast-v016/bin/python3.12` points to the historical Homebrew Cellar `python@3.12/3.12.15` location, while the installed current Cellar directory is `3.12.15_1`. The stable `/opt/homebrew/opt/python@3.12/bin/python3.12` and `.venv-reproduction-v02/bin/python` both report Python 3.12.15. Forecast site-packages, including torch/numpy, still exist. The reproduction environment has numpy but no torch.

No old environment, package or symlink was changed. Parent was notified to choose a provenance-preserving runtime route. Six synthetic tests must pass under the admitted runtime before a source/input freeze is written. The scientific output directory does not exist yet. A root GO remains required before the single bounded inference attempt.

Root subsequently authorized the exact `.venv-analysis-v022` runtime bridge documented in `PROTOCOL.md`. Read-only import smoke passed for Python 3.12.15, NumPy 1.26.4 and PyTorch 2.5.1. The first test process under the sandbox then aborted with OpenMP error 179, “Can't open SHM”; it loaded no benchmark/checkpoint. Its receipt/log remain in `TEST_ATTEMPT_001.json` and `synthetic_tests_attempt_001.log`. Monitor/shared-memory-enabled execution with one-thread environment settings passed all six synthetic tests without a scientific-source change. Runtime identity/package inventory is in `RUNTIME_BRIDGE.json`. Root authorized one monitored inference attempt after the final freeze; execution outcome will be recorded separately, not inferred from preparation.
