# Recovery mechanism and physical simulation pilot v0.5

Manufacturing only. This exploratory cycle follows the exposed v0.4 measurement-replay results. It specifies and tests a simulated horizontal two-joint arm with protected command context. All observations generated here are **synthetic**. No CASPER data are opened and no real robot is connected.

- [Comparator decisions](COMPARATORS.md): independent Edge-architecture implementation in the recorded-IMU track; separate/background/reserve dispositions for CASPER, TWINE, CatBoost and ModernTCN.
- [Precise model, threat and evaluation plan](PLAN.md), [configuration](config.json), [prior-art and algebraic admission decision](PRIOR_ART.md).
- [Pre-execution identities](FREEZE.json), [primary-source artifact identities](SOURCE_RECEIPT.json).
- `plant.py`: equations, RK4, sensors and authorized/unauthorized command scenarios.
- `observer.py`: prospective following/reference states, AR/ARX, rolling/CUSUM scores, explicit uncertainty and dwell-time recovery.
- `worker.py`, `run.py`: bounded training/calibration, complete score sealing, joint evaluation and failure preservation.
- `test_pilot.py`, `verify.py`: synthetic physics/causality tests and separate replay/arithmetic checks.

The candidate is algebraically ordinary hysteresis on the maximum of two normalized errors. The pilot cannot establish originality of that rule. It tests the role of trusted context and recovery behavior, including comparison with the exact classical equivalent.

## Reproduce locally

Run from repository root `/Users/matrixusman/CUI/DigitalTwin`. Reuse the unchanged project Python3.12.15 / NumPy1.26.4 environment. Its dependency lock is [v0.2 requirements](../contribution_v0.2/requirements-macos-arm64.lock.txt); no TensorFlow model is used in this cycle. The supervisor may need permission to invoke `/bin/ps` on this machine. Never disable resource monitoring or replace an existing named attempt.

```sh
manufacturing/.venv-reproduction-v02/bin/python -m unittest discover -s manufacturing/research_cycles/recovery_v0.5 -p test_pilot.py -v
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/recovery_v0.5/run.py --attempt simulation_001
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/recovery_v0.5/verify.py --run simulation_001 --attempt verify_001
```

The named attempt commands are historical executable records, not invitations to overwrite results. `freeze.py` created the one-time freeze after the passing synthetic checks; it refuses to replace that record. A new explicitly authorized repeat uses a new attempt name and retains all earlier outcomes.

Ignored local storage: `manufacturing/local/recovery_v0.5/sources/`, `tests/`, `runs/simulation_001/`, `verification/`. Synthetic arrays, fit coefficients, calibration, per-episode scores, outcomes, full environment/provenance and logs are retained there. Git stores our implementation, protocol, safe summaries and hashes. `PACKAGE_MANIFEST.json` will bind completed reporting artifacts; it supplements rather than changes the pre-execution freeze.

## Test history

`tests_001`: 23/24 passed; one-step numerical convergence error with four RK4 substeps exceeded the original tolerance. `tests_002`: 24/24 passed after increasing the fixed integrator to eight substeps before any pilot observation was generated. Tolerance unchanged. Both logs and pre-correction source hashes are preserved. No experiment result motivated that correction.
