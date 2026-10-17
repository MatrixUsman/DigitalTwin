# Frozen virtual recovery study v0.7

Completed under the user's request to test mechanisms/components, run fresh frozen conditions and write the paper, entirely virtually. Start with [results](RESULTS.md), [complete tables](TABLES.md), [pre-generation plan](PLAN.md) and [source/comparator decisions](SOURCES_AND_ADMISSION.md).

The sole experiment is `manufacturing/local/recovery_v0.7/runs/confirmation_001/` (ignored local storage). All 144 episodes × 23 methods = 3,312 outcomes are accounted for. Fourteen synthetic tests and 14,635 verification checks passed. Main hypothesis failed; no scientific redesign followed outcome inspection.

Commands, from repository root, used the existing isolated environment:

```sh
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/recovery_v0.7/v7_test.py
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/recovery_v0.7/v7_freeze.py
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/recovery_v0.7/v7_run.py
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/recovery_v0.7/v7_verify.py --run manufacturing/local/recovery_v0.7/runs/confirmation_001 --output manufacturing/local/recovery_v0.7/verification.json
manufacturing/.venv-plots-v03/bin/python manufacturing/research_cycles/recovery_v0.7/present.py
manufacturing/.venv-reproduction-v02/bin/python manufacturing/manuscript_recovery_v0.7/build_pdf.py
```

Do not recreate or overwrite the consumed freeze. Replays must preserve the original attempt and use a new output directory. A new scientific choice requires a new cycle and fresh evidence. The bounded supervisor may need process inspection permission for `/bin/ps`; this run was authorized and completed. Model weights, transformations and old calibration are hash-bound. Earlier environments and raw observations were not changed.

`present.py` is post-exposure reporting, outside the scientific freeze. It generates plots, tables, all-outcome CSV, exact entry-ablation equality checks and a source-identity receipt from saved artifacts only. The first plotting invocation used a temporary font cache; no package was installed. Set a project-local `MPLCONFIGDIR` for future plotting.

The separate [manuscript directory](../../manuscript_recovery_v0.7/README.md) contains source, generated figures/tables, traceability, declarations, review and PDF build records. Public release is not authorized; third-party paper/data permissions are unchanged. Scope is explicitly synthetic and depends on protected approved commands plus truthful sensing.
