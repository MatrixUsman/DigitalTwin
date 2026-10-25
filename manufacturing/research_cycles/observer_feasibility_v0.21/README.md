# Normal-only observation representation study

Start with [RESULTS.md](RESULTS.md), then the [independent review](INDEPENDENT_REVIEW.md). The [prospective plan](PLAN.md) and140-file [freeze](FREEZE.json) precede the new normal conditions. All observations are synthetic. This study leaves manuscript v1.7 and its original failed criterion unchanged.

**Outcome:** the coupled estimator fails its advancement rule; ordinary Kalman filtering estimates state more accurately in all three sensing regimes. No new attack campaign was run for this candidate.

Implementation: `observers.py`; six synthetic fixture tests: `test_observers.py`. Fitting and evaluation are in `worker.py`, with restricted estimator inputs and a saved selection before calibration. `run.py` is the original supervisor; `resume_monitor.py` is the separately recorded infrastructure-only recovery after the sandbox denied memory monitoring. Do not rerun these consumed output paths or silently overwrite their records.

Read-only verification and report regeneration from the existing local run, cwd `manufacturing/`:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv-reproduction-v02/bin/python research_cycles/observer_feasibility_v0.21/verify21.py
python3 research_cycles/observer_feasibility_v0.21/report.py
```

These commands use the existing project environment and recorded synthetic artifacts. They are not a standalone fresh-environment replication. `PACKAGE_MANIFEST.json` identifies completed sources, reports and local run artifacts; the existing freezes identify consumed historical sources/normal data. No real data, vendor code or fitted state from another project enters this study. A new experiment requires a separately versioned protocol, not reuse of its now-exposed conditions as confirmation.
