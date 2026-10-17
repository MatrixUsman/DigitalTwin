# Implemented model candidate and normal-motion pilot

Start with [the proposed model](MODEL_PROPOSAL.md): plain-language explanation, diagram, equations, state, training, threat assumptions and validation matrix. Then read [the measured results](RESULTS.md) and [reporting clarifications](REPORTING_NOTES.md).

- `model.py`: deterministic RBF/linear correction, causal return evidence and alarm machine.
- `test_model.py`: 18 synthetic tests; no benchmark claims.
- `PLAN.md`, `config.json`, `FREEZE.json`: unchanged pre-run scientific specification and identities.
- `freeze.py`, `run.py`, `worker.py`: one versioned, bounded normal-only experiment.
- `verify.py`, `VERIFICATION.json`: 4,080 saved-artifact checks, including reference replay and independent arithmetic.
- `present.py`, `RESULTS.md`, `metrics.csv`, PNG/SVG figure: reports from saved results.
- `PRIOR_ART.md`, `REPORTING_NOTES.md`: established overlap and corrected source/probe interpretation.
- `MODEL_PROPOSAL.md`: a research candidate, not a claim of original architecture or publication readiness.

Local fits, calibration arrays, synthetic observations, logs and provenance are under `manufacturing/local/residual_twin_v0.13/runs/pilot_001/`. Historical baseline artifacts and simulator sources remain unchanged. No raw CASPER observations or new attack outcomes were accessed. The run succeeded technically, but its predeclared all-plant scientific improvement criterion failed.

The source-generation, supervision and validation guidance in academic-research-suite was applied inline under the user's explicit model-building request. No full-team or external peer-review certificate is claimed. The teacher's broader requests are tracked in [the revision action map](../../docs/TEACHER_REVIEW_ACTIONS_V0.13.md).
