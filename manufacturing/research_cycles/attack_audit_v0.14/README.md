# Saved-model attack and recovery audit v0.14

Completed on 17 October 2026 at the user's request. **The candidate failed its declared improvement criterion; algorithmic novelty remains unestablished.** This package preserves that outcome and the useful protected/following-reference comparison.

- [Results, all methods and figures](RESULTS.md)
- [Contribution decision and next investigation](CONTRIBUTION_DECISION.md)
- [Closest-prior-art and comparator audit](NOVELTY_AUDIT.md)
- [Frozen plan](PLAN.md) and [configuration](config.json)
- [Pre-execution identities](FREEZE.json), [saved-result verification](VERIFICATION.json), [presentation identities](PRESENTATION.json)

## Scope

189 synthetic episodes × 17 controls/ablations = 3,213 method outcomes; 81 benign episodes and 108 attack episodes. All episodes contain 1,200 samples at 50 Hz, with 100 initialization samples and 1,100 scored endpoints. Seeds are 17, 42 and 2026. Fresh task/noise parameterizations use the existing three virtual plants; they are not independent robot acquisitions.

The saved v0.13 base, linear and RBF fits and their normal thresholds are unchanged. New simple controls were calibrated on the same old normal population. There was no retraining, raw CASPER access, paid compute or public-data download. Trusted command context and honest noisy state measurements are assumptions. Nothing here tests a fully compromised sensing/command channel.

One supervised attempt completed in 27.515 seconds wall time and 26.656 seconds worker CPU, with 90.17 MiB sampled peak RSS and 83.44 MiB outputs. All 25 pre-execution synthetic tests and 30,448 saved-result checks passed. The verification replays inference and separately checks metric arithmetic; it is not an independent scientific replication.

## Executed commands

Working directory: `/Users/matrixusman/CUI/DigitalTwin`.

```sh
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/attack_audit_v0.14/freeze.py
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/attack_audit_v0.14/run.py
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/attack_audit_v0.14/verify.py
manufacturing/.venv-plots-v03/bin/python manufacturing/research_cycles/attack_audit_v0.14/present.py
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/attack_audit_v0.14/package.py
```

The scientific freeze, experiment and verification are consumed, no-overwrite operations. Do not remove their guards or alter frozen code to rerun them. A fresh independent reproduction needs its own versioned location and an explicit distinction from new confirmatory evidence. Presentation was run twice for typography/axis cleanup, without changing scientific choices or numbers.

## Local evidence

Full score/truth arrays, calibration, provenance, environment, exact run command, timestamps, resource logs and every method/event outcome are in `manufacturing/local/attack_audit_v0.14/runs/audit_001/`. Synthetic test receipts are under that cycle's `local/.../tests/`. The package manifest binds source, previous evidence, outputs and snapshots of mutable project handoffs.

`summary.csv` contains every method's pooled/plant metrics; `strata.csv` adds all task/condition groups; `events.csv` retains all 108 events for each method. `DESCRIPTIVE_DIAGNOSTICS.json` is explicitly post-study and does not redefine the primary metric. Raw data and local evidence remain out of Git. This is a local evidence package, not an uploaded or independently portable release.
