# Review extension v0.18

Executed exploratory **saved-synthetic replay**, 19 October 2026. No model training, new simulation or original real dataset access. The new matched base dual no-dwell comparison shows that the earlier no-dwell benefit does not require RBF: 1,198 versus 1,195 benign points. More alarm starts accompany shorter occupancy. See [RESULTS.md](RESULTS.md).

The original 17-method audit, v1.6 and original failed 10% criterion remain unchanged. New analyses are exposed-data development, not fresh confirmation or demonstrated novelty.

- [PLAN.md](PLAN.md): pre-execution comparison, diagnostics and budgets.
- [FREEZE.json](FREEZE.json): 400 source/input bindings, including old saved scores/truth/models.
- [REPAIR_FREEZE.json](REPAIR_FREEZE.json): first scientific-empty attempt preserved after sandbox denied the RSS monitor; identical worker run again with monitoring enabled.
- [VERIFICATION.json](VERIFICATION.json): 112,847 read-back checks and completed artifact hashes.
- [REPORTING.json](REPORTING.json): main manuscript tables and strata in machine-readable form.
- [BOUNDARY_DIAGNOSTIC.json](BOUNDARY_DIAGNOSTIC.json): explicitly post-replay timing-window diagnostic.
- `runs/replay_001/`: preserved infrastructure failure.
- `runs/replay_002/`: completed predictions/alarm arrays, 3,402 episode outcomes, summaries, diagnostics, environment, logs and supervisor receipts.

## Commands

Working directory: `manufacturing/`. Existing isolated interpreter: `.venv-reproduction-v02/bin/python`. Dependencies are recorded in successful `provenance.json`; no system packages changed.

```sh
.venv-reproduction-v02/bin/python research_cycles/review_extension_v0.18/test_replay.py
.venv-reproduction-v02/bin/python research_cycles/review_extension_v0.18/present.py
```

The 12 tests use explicitly synthetic fixtures and no observations. Presentation only reads existing exposed artifacts. `verify.py` preserves its initial verification and refuses to overwrite it; consult the existing receipt.

For an explicitly requested independent replay with the same source files and saved input bundle available, use a new attempt name:

```sh
.venv-reproduction-v02/bin/python research_cycles/review_extension_v0.18/reproduce.py --attempt reviewer_replay_001
```

This command is provided, not run. It uses the same 300 s wall / 180 s CPU / 1 GiB sampled memory / 100 MiB output bounds and refuses an existing directory. It may require process-monitor permission on macOS. The completed worker costs were approximately 1.63 s wall and 1.30 s CPU. A recorded scientific reproduction uses saved simulator outputs, not newly generated data. None of these materials has been published or externally uploaded.

`OUTPUT_SEAL.json` was written while the worker log still streamed; its scientific output hashes verify, and `VERIFICATION.json` binds the completed log. This packaging timing caveat is preserved rather than rewriting the historical run.
