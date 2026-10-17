# Candidate improvement and fair-evidence design

17 October 2026. **Research hypothesis and executable-study design work, not established novelty or a final model freeze.** The [baseline dossier](BASELINE_LIMITATION_DOSSIER_V0.2.md) demonstrates source/artifact issues and identifies method assumptions. It does not yet show an attack-detection weakness of a faithfully reproduced CASPER-family predictor. No publication title is chosen.

## Candidate question

**Can a motion twin recover synchronization after uncertain observations without accepting an unauthorized change in execution progress as its new reference?**

This is a candidate about state synchronization and recovery with fixed model parameters. It is distinct from changing model weights or learning a new normal distribution. The baseline connection is that an external-IMU predictor conditions on recent observations and an aggregation window; a score may fall once its history describes the changed motion. That possible failure must be demonstrated rather than inferred from our old observer or from source-code bugs. Correct timing, target alignment, residual formula and recurrent-state policy first.

Three questions govern admission:

1. Does a correctly implemented, normal-calibrated baseline lose sensitivity during persistent command deviations, and is that effect explained by its observation history rather than model capacity or poor calibration?
2. Can an explicit nominal-state constraint preserve evidence while allowing legitimate timing variation, with the same inputs and false-alarm budget as the controls?
3. When synchronization becomes ambiguous, can a declared recovery rule restore a useful reference without silently clearing unresolved deviations? What information makes recovery identifiable?

The user has no testbed access. Development therefore uses public observations plus explicitly labelled simulation. Original CASPER is exposed exploratory material. The newly obtained successor nominal file is development material; no successor anomaly file has been downloaded or inspected. Physical-disturbance recordings cannot be relabelled as independently recorded cyberattacks.

## Specific mechanism to investigate

This is an **independent design candidate**, not a modification of a published checkpoint. It should initially be called a constrained motion observer. Calling it a twin requires validating correspondence between its state and the modeled plant/task.

Let `z=(m, φ, v)` represent task mode, execution phase and phase velocity. A frozen nominal observation map `h_m(φ)` predicts the monitored channels. A declared transition model `F(z, u, Δt)` advances phase using permitted commands/context `u`, rate bounds and acceleration bounds. Keep a *set* `S` of plausible nominal states rather than interpreting an unvalidated single phase estimate as ground truth.

Before observation `y_t`, form:

```
S_t^- = { F(z, u_t, Δt_t) : z in S_(t-1), permitted transition bounds }
g_t   = min[z in S_t^-] d_R(y_t, h(z)) - ε
S_t   = { z in S_t^- : d_R(y_t, h(z)) <= ε }
```

Here `R` and observation tolerance `ε` are fixed using permitted nominal development data or an explicitly validated sensor-noise specification. The distance, bounds and map must be specified numerically before any final experiment. A discrete grid is a computational approximation, not a continuous reachability proof. Empty-set, grid-resolution and model-mismatch behavior need tests.

The proposed addition to an ordinary feasible-state observer is an explicit **quarantine and recovery rule**:

- Emit the discrepancy before incorporating the observation. If no nominal state explains it, retain the inconsistency; do not silently reset the trusted reference to the nearest observed phase.
- Maintain a separate candidate state that may follow new observations, without promoting it to the nominal reference.
- Re-admit it only when a predeclared window is compatible with a permitted state path and a justified synchronization anchor. An anchor can be an authenticated program/cycle marker in simulation, or a separately validated observable landmark. A detector's own “normal” prediction is not an independent trusted anchor.
- If the propagated nominal set becomes too broad to support a decision, output **uncertain**. Count this loss of coverage; never convert it into a correct normal decision or omit it from the denominator.

This mechanism is not novel merely because it uses sets, gates, dual states, phase or abstention. Those ingredients have established precedents. The potential contribution would have to reside in a specific recoverability condition and its validated detection/coverage trade-off beyond the closest constrained observers. That argument is not complete. If an existing set-membership monitor plus a standard reset rule is equivalent, reject the novelty claim and retain the implementation only as a control.

## Threat and information boundary

Initial synthetic threat: unauthorized changes to a robot's execution command or execution speed while an independently protected monitoring channel supplies truthful observations. Model parameters, reference trajectory and calibration remain fixed. Benign program changes are explicitly authorized in the simulated command context; every comparator receives the same context if the proposed method uses it.

Do not infer authorization from a motion trace alone. Identical sensor histories under a fault, a malicious command and an authorized change cannot establish three different intentions without additional information. Do not claim protection against fully forged telemetry, compromised trusted context, attacks invisible to the sensor, live mitigation or physical safety. Clock values must be identified as acquisition or arrival times before using them as `Δt`.

## Prior-art and feasibility decisions

| Route | Decision now |
|---|---|
| Correct notebook alignment, reset TFLite variables, unify norms | **Implement as baseline repairs.** Measured code/artifact evidence exists; not a standalone novel twin. |
| Add multiscale residual windows or CUSUM | **Mandatory ordinary controls.** The successor already recognizes adaptive-window opportunities; sequential evidence is established background. |
| Add phase alignment or a posterior/prior discrepancy | **Not admitted as novelty.** Existing project prior-art audits already establish substantial overlap. |
| Add task recognition or external-IMU/controller disagreement | **Close-prior-art hold.** CASPER+ already proposes these directions; exact recent implementations and assumptions need review. |
| Constrained recovery with explicit uncertainty and protected state lineage | **Candidate only.** Requires comparison against set-membership observers, robust filtering, timed/path constraints, change detection and reset/reinitialization methods. No original theorem or experimentally validated gain yet. |

The candidate's feasibility is conditional: task/phase correspondence, legitimate-change annotations, trusted anchors and identifiable timing are absent or unresolved in the current public recordings. Public-data replay alone cannot establish those assumptions. A simulation can test them under explicit conditions; it must not be presented as a validated UR3e digital twin unless its kinematics, dynamics, sensing and discrepancies are validated against that asset.

## Fair comparison protocol to prepare before full experiments

1. **Reference correctness first.** Pin one architecture/configuration per comparator; use explicit target indices, fixed score formulas and named recurrent-state policies. Separate original author artifacts, modified author code and independent reimplementations. Never compare our corrected method against a knowingly broken baseline and attribute the difference to novelty.
2. **Compare by role.** Include the corrected CASPER-family CNN and a correctly specified recurrent predictor; persistence/AR or ARX; nominal periodic and causal alignment controls; fixed-reference and ordinary constrained observers; standard multiscale/CUSUM alarms; and an admitted recent general detector such as a clearly labelled ModernTCN transfer if its access contract fits. Two related family models are not three independent recent baseline papers. TWINE's supervised track stays separate.
3. **Use separate evidence tracks.** Original CASPER: exposed exploratory diagnosis only. Successor nominal/physical disturbances: ordinary motion/fault sensitivity, after release/annotation/run admission. New simulation: explicit command manipulations and authorized changes, with imperfect models, clock/measurement disturbances and held-out parameter/task combinations. Do not pool their scores or rename faults as cyberattacks.
4. **Preserve future evidence.** Specify training/development, normal calibration and whole held-out acquisition/scenario groups before opening final outcomes. Split before windows, retain gaps and warmups, and forbid cross-boundary targets. A new file is not automatically an independent recording; establish lineage. Simulation seeds alone are not new physical robots.
5. **Use equal information.** Same native channels/context, timestamps, observation history rules, model-selection labels and calibration population within each track. If our observer uses an authenticated marker, supply it to the relevant controls and report a context-removed ablation. An oracle-state diagnostic is labelled an oracle and excluded from the main ranking.
6. **Freeze finite choices.** Nominal development chooses architecture, phase resolution, transition bounds and recovery window from a declared finite policy. Normal calibration sets thresholds only. Use policy seeds 17,42,2026 for stochastic fitting; deterministic methods once. Do not select variants or percentiles using test interventions.
7. **Assess all costs and outcomes.** Unadjusted point metrics, event misses and delays, normal alarms/episodes, uncertain coverage, recovery time and false readmissions; resource measurements by method with actual units. If time provenance is unresolved, report sample delays and alarms per fixed observation count instead of invented seconds/hours. Include long sustained alarms and all misses.
8. **Falsify the proposed mechanism.** Compare the same observer with automatic reset, quarantine without an anchor, anchored recovery, and fixed/free-running reference. If ordinary controls explain the gain, if unknown coverage absorbs the difficult cases, or if recovery needs privileged labels/context, reject the proposed contribution. A failed candidate is not repaired through test-driven tuning and then presented as confirmatory.

## Additional novelty check

The subsequent [recovery prior-art check](literature/RECOVERY_PRIOR_ART_ADDENDUM_2026-10-17.md) found an older set-intersection attack detector and a 2026 institutional record describing twin-based, consistency-gated recovery. The latter's full text and exact publication date remain unresolved, but it is sufficiently close to prevent admitting the generic mechanism as novel. The equations above are a design candidate/control, not a new contribution. Establish a specific difference from these sources before further model development.

## Current completion state

Baseline source limitations are connected to tests, and selected implementation defects have been reproduced. A normal-only CNN pilot succeeded. The constrained-recovery mechanism is specified at mathematical/design level, **not implemented or admitted as novel**. Full baseline training, attack evaluation, validated simulation, complete close-prior-art comparison, contribution results, final title and venue selection remain unfinished.

The next scientific decision is whether the constrained-recovery rule differs meaningfully from close prior art and has an observable/testable advantage under feasible public/synthetic evidence. If it does not, select a different mechanism before spending the full training budget. The user's original-contribution objective remains active; the source audit and preliminary report do not replace it.
