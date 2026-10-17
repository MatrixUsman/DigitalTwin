# Recovery under mismatch — v0.6

**Completed:** frozen 144-episode virtual experiment, thirteen methods, 1,872 outcomes. The candidate partly reduced legitimate-change alarm time and retained evidence, but missed its full primary target and failed under parameter extrapolation. The simpler fixed-return ablation is the stronger development lead. Every outcome is preserved.

- [Results and decisions](RESULTS.md), [all-method tables](TABLES.md), [machine-readable summary](SUMMARY.json).
- [Pre-execution plan](PLAN.md), [configuration](config.json), [freeze](FREEZE.json), [exposed-pilot diagnosis](DIAGNOSIS.json), [close prior art](PRIOR_ART.md).
- [Validation and limitations](VALIDATION.md), [comparison figure](../../output/recovery_v0.6/comparison.png), [paired motion/alarm figure](../../output/recovery_v0.6/examples.png).
- Implementation: [core](core.py), [worker](worker.py), [synthetic tests](test_core.py), [verification](verify.py). Physical equations are the immutable v0.5 `plant.py`; the supervisor and AP implementation are existing hash-bound project code.

Local evidence: `manufacturing/local/recovery_v0.6/runs/simulation_001/` contains launch, provenance, saved normal components, fit, threshold probes, before-generation seal, 144 fresh episodes, complete score seal, all outcomes, aggregate, resource report and logs. Local verification, numerical QA and presentation receipts remain outside Git. No raw CASPER access, model retraining, paid compute, contact or publication occurred.

Commands actually executed from `/Users/matrixusman/CUI/DigitalTwin`:

```sh
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/recovery_v0.6/freeze.py
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/recovery_v0.6/run.py --attempt simulation_001
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/recovery_v0.6/verify.py --run manufacturing/local/recovery_v0.6/runs/simulation_001 --output manufacturing/local/recovery_v0.6/verification.json
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/recovery_v0.6/numerical_audit.py
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/recovery_v0.6/config_access_audit.py
manufacturing/.venv-plots-v03/bin/python manufacturing/research_cycles/recovery_v0.6/present.py
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/recovery_v0.6/package.py
```

These are consumed commands, not instructions to overwrite/rerun them. The test script can run without observations; full reproduction requires the declared old synthetic input artifacts and matching dependencies. Future scientific changes require a new cycle. A verified package is not permission to publish it.
