# Next study: demonstrate a method limitation before claiming an improvement

Proposed after v0.2 source diagnostics and the normal pilot, 17 October 2026. **Not executed, not a final freeze, and not evidence that the candidate is novel.** This records the next work in an order that prevents a new completed feasibility study from again being mistaken for the intended contribution paper.

## 1. Establish the corrected reference

Select a single documented Edge-2025 compact 45-input/one-output CNN branch. Write an explicit implementation contract for training chronology, scaler, initialization, stopping, score aggregation, warmup and endpoint indices. Resolve which quantities the paper actually specifies and label deviations. Retain an independent implementation where the original run is unavailable. Never attach the paper's headline score to our implementation.

For the LSTM, resolve reset-per-independent-window versus continuous streaming recurrence. Test each intended policy against the corresponding training semantics; do not compare a stream-state model to a window-state model without disclosure. The multi-output scoring defect is not automatically a defect in the one-output released artifact.

Before a larger fit, implement parameterized, bounded workers under a new version and synthetic tests for chronology, target offsets, source identity, finite scores, state initialization and frozen transforms. Record an exact finite normal-development selection procedure and every failed attempt. The v0.2 one-epoch pilot measures feasibility only. Do not extrapolate it into a claimed full-training runtime or an already selected checkpoint. Any lengthy run needs a concrete estimate and approval.

## 2. Demonstrate a method-level limitation on development evidence

The specific hypothesis is that conditioning a predictor on recent observations can make persistent execution deviations increasingly predictable, reducing the residual after the transition. It is **unproved** for a correctly trained CASPER-family model and can be false for some deviations.

Evaluate brief and persistent interventions across several predeclared magnitudes, retain the complete score time course, and compare early versus late intervention evidence. Distinguish:

- a true history-assimilation effect;
- insufficient training or a wrong scaler/state policy;
- aggregation-window delay;
- a deviation that is not observable in the permitted channels;
- a deviation that the training distribution legitimately includes.

Use persistence, AR/ARX, fixed-reference residuals and ordinary sequential/multiscale alarms to test these alternatives. Give every method the same context and normal calibration. If only a broken implementation fails, the result is a repair. If ordinary alarms solve the problem, they become controls and the proposed novel mechanism must be reconsidered.

## 3. Public data and simulation serve separate purposes

**Public observations:** the received nominal successor prefix can support preprocessing, prediction and false-alarm development. Before admitting additional files, establish acquisition grouping, time semantics and annotations. Provider-v2 packaging contains older and newer material; count actual acquisitions, not filenames or version labels. Additional physical disturbances may test motion sensitivity, but do not prove cyberattack recognition or trusted recovery. Original CASPER outcomes remain exposed exploratory evidence.

**New simulation:** use an explicitly documented simulated manipulator and sensor/command model, with separate plant and observer parameters. A first small mechanism fixture can use a planar two-link arm with inertial sensing and a finite-bandwidth servo. It must be called a synthetic mechanism test, not a validated UR3e twin. Do not generate attacks by simply adding a labelled offset to an arbitrary recorded channel and call the result physical motion.

The generator must expose: joint states and commands, link geometry, inertial observation map, sensor orientation, gravity/magnetic-field assumptions if used, controller lag, sample/arrival clocks, missing-data policy, random seeds and ground-truth intervention provenance. Test analytic special cases, numerical integration accuracy, rate limits and causal observation generation before interpreting detector results. No attack-capable code is deployed to a physical device.

Generate benign authorized speed/program changes and unauthorized command deviations separately. Trusted program markers are an explicit additional assumption. Supply them equally to context-aware controls; include a marker-removed ablation. Treat indistinguishable observations as an identifiability limit, not a detector implementation failure.

## 4. Protect prospective evaluation

Before any confirmatory simulation is generated or independent final observations inspected, commit the complete generator/configuration inventory, task/parameter groups, calibration population and run matrix to an immutable local manifest. Development and final groups must differ in meaningful predeclared plant/task/intervention conditions; merely changing noise seeds does not establish physical generalization.

Use seeds 17,42,2026 for stochastic model fitting, all reported; deterministic controls run once. Select models and recovery rules on permitted normal development or explicitly labelled exploratory intervention development, never on final attacks. Keep the normal-only learning track separate from any intervention-informed supervised track. Calibration fixes thresholds only. Define primary outcomes, sample/time units, all event misses/delays, normal alarms, uncertain coverage and false readmissions before final execution. Use an equal information budget and a jointly released final comparison.

Do not reuse the old CASPER calibration population/rank: those were specific to the completed v0.1 experiment. The new populations and exact numerical choices cannot be frozen until their identity and grouping are established.

## 5. Decide whether a contribution survives

Compare the full proposed equations and recovery conditions with the sources in [the prior-art addendum](../../docs/literature/RECOVERY_PRIOR_ART_ADDENDUM_2026-10-17.md). Generic set intersection, a separate reference, gating, uncertainty or a reset is insufficient novelty. The candidate must establish a precise difference, show why it changes a demonstrated failure, and survive matched controls and ablations.

Write a contribution-paper result only after those conditions are met. Otherwise preserve the diagnostic result and reject or revise the mechanism before spending the full budget. The next deliverables are a corrected comparator contract, a close-prior-art equation/assumption comparison, and a validated bounded simulation-development plan. Final results, title and journal selection remain open.
