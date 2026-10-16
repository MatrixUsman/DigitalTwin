# Proposed smart-grid reproduction plan

Updated **2026-10-16**. **Proposal only: no baseline, environment, loader, tests, simulation or training has been implemented or run.** The full smart-grid audit follows water and manufacturing; this document does not authorize that next phase.

## 1. Establish a reproducible target

Choose AC distribution, transmission or DC microgrid before selecting a principal comparator. G1/G2 in [the literature register](LITERATURE_EVIDENCE.md) are promising reading leads, not execution recommendations. Require full manuscript, matched implementation or enough detail for an explicitly labelled reimplementation, permitted data/case access, and a compatible evaluation protocol.

The first executable control, when authorized, should be a small conventional electrical-state consistency/residual detector appropriate to the chosen setting, with a fixed normal-data calibration rule. This is a transparent engineering control, not a recent-paper reproduction or a novel contribution. Exact estimator, required measurements, observability conditions and equations must be specified first. Do not assume residual tests detect all stealthy false-data injection attacks.

No recent paper is yet sufficiently verified to name as the first faithful reproduction. Prioritize artifact feasibility during the future audit, then select one recent method on the same electrical setting and information budget.

## 2. Freeze the question and evaluation

- Define the detector's measurements and independently trusted topology/status inputs. State whether topology is known, uncertain or adversarial, and distinguish a topology update from a physical network change.
- Predeclare benign cases (normal load variation and authorized switching), physical faults/sensor faults, and malicious measurement or status manipulation. Do not label every fault an attack.
- Split complete independent runs/scenarios into development and held-out groups before windowing; preserve time within each run. Fit transforms, models and calibration only on designated development data. If source chronology is missing, choose a non-temporal classification protocol and limit claims accordingly.
- Never tune thresholds, parameters, checkpoints or model selection on held-out test attacks. A normal-validation false-alarm budget or fixed documented rule is a candidate calibration approach; choose its value before final evaluation.
- Compare every method using the same data/case release, sensor access, scenario families, temporal alignment and labels. Report unadjusted detection metrics, false alarms on benign changes, missed attacks, and detection delay only where timestamps support it. Report state-estimation error only where independent reference truth exists; simulator truth is not real-world ground truth.
- Predeclare how abstentions, unobservable states, solver failures and missing packets count. Keep per-scenario and aggregate metrics, with independent runs/scenarios as the unit of uncertainty rather than overlapping windows.

Only after a baseline is understood should the project investigate an additional topology-consistency component. Compare against the fixed control and remove the proposed component to establish what it contributes. No novelty or superiority claim follows from a smoke test.

## 3. Minimal future structure and environment

The project reserves `baselines/`, `datasets/`, `papers/`, `configs/`, `experiments/`, `src/`, `tests/`, `manuscript/`, and `docs/`. The root skill installation is shared tooling, not shared project evidence or experimental state.

When implementation is approved, propose a project-local `.venv/` and pinned dependencies for metadata/loading, numerical evaluation and tests; do not install now. Candidate modules are `src/grid_research/data.py`, `splits.py`, `metrics.py`, `provenance.py` and a simulator adapter only if needed. These are proposed names, not files currently implemented. Separate upstream environments when dependencies differ. GridSTAGE would additionally require verified MATLAB/PST access; a Python environment alone does not provide those dependencies.

## 4. Proposed tests, not executed tests

| Test | Meaningful invariant |
|---|---|
| Loading/schema | Original bytes unchanged; expected units, labels, timestamps, sensor identity and bus/branch mapping preserved |
| Topology/state mapping | Measurement ordering matches the selected topology revision; inconsistent units/reference frames fail visibly |
| Split isolation | No raw interval, window, scenario instance or derived duplicate crosses development/test boundaries |
| Calibration independence | Altering held-out labels cannot change thresholds, model selection, preprocessing or fitted parameters |
| Metrics | Known synthetic cases verify counts, missing/undefined cases, event matching and delay alignment |
| Simulation boundary | Synthetic fixtures identified; oracle state/attack schedule unavailable to detector input unless explicitly allowed |
| Provenance | Run/config/source hashes and required dependency, command, revision and seed fields recorded |

Synthetic fixtures must run without benchmark data or network access. Their passing status would establish software invariants, not benchmark performance.

## 5. Later execution gates

1. Complete the scheduled grid audit and choose a feasible task/data pairing.
2. Obtain authorization for minimal implementation and isolated environments; implement loaders/evaluator and the above tests.
3. Propose a bounded local pilot with a fixed configuration, time limit and explicit stop criteria. Do not assume hardware suitability or runtime from paper claims.
4. Use measured pilot resource use to budget the baseline; obtain approval before lengthy or paid runs.
5. Freeze configurations, evaluate held-out scenarios once, and retain failures and all predeclared variants.
6. Assess a contribution only after reproduction/control evidence; write methods from actual logs and results from recorded measurements.

Every later experiment must record seeds, data/case/split hashes, simulator/dependency versions, code revisions and patches, commands, hardware/device, timestamps, configuration, preprocessing/calibration rules, scores/metric definitions and logs. Classify the work as faithful reproduction, author-code evaluation under a changed protocol, or independent reimplementation. No experimental record exists yet.
