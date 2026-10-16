# Bounded normal-only feasibility pilot

Historical specification, preserved below. A later explicit user instruction authorized implementation and one execution. See the [completed pilot report](PILOT_REPORT.md) and [actual run summary](../experiments/PILOT_V0.1_SUMMARY.json). The model, ranges and limits were not changed; planning-state fields in the original JSON remain historical. The one v0.1 attempt is consumed and must not be automatically repeated.

## Material Passport

- Project / owner: manufacturing / Haiqa Mushtaq.
- Origin: academic-research-suite, experiment-agent, **plan** workflow.
- Date / version: 16 October 2026 / `casper-right-arm-pilot-v0.1`.
- Status: **proposed, not executed**. This document specifies a future pilot; it does not authorize or record fitting, calibration or a final experiment.
- Inputs: the unchanged [data contract](ANNOTATION_FEATURE_SPLIT_CONTRACT.md), [evaluation protocol](EVALUATION_PROTOCOL.md), [selected question](RESEARCH_QUESTION_AND_THREAT_MODEL.md) and [pilot configuration](../configs/casper_right_arm_pilot_v0.1.json).

The first pilot should establish that a small normal-only control can fit and produce complete, aligned finite scores within a bounded local budget. It cannot answer the research question or establish attack sensitivity. Its model is an ordinary joint-velocity deviation detector; it has no predictive physical state, synchronization or digital-twin claim.

## Fixed scope and chronology

Use only original CASPER v3 `right_arm.csv`, whose recorded SHA-256 is `181662e25de09c1f4ed05e0877a65c40225752d6f54575ddb1cdf8a0cf29a334`. These are **prefix subsets of existing partitions**, not replacement split definitions. All ranges are zero-based data rows with an excluded upper bound.

| Purpose | Permitted raw range | Raw rows | Eligible endpoints used |
|---|---|---:|---|
| Fit this pilot's reference | `[0,50000)` inside training | 50,000 | `[1528,16571)` and `[18099,50000)`: 46,944 |
| Check this pilot's scores | `[540002,560002)` inside development | 20,000 | `[541530,560002)`: 18,472 |

Retain the contract's 1,528-observation warmup and gap rule `delta_t <= 0 or delta_t > 0.075 seconds`. The known training restart at row 16,571 therefore remains exercised. Initialize development separately; never carry training history across the partition boundary. This row-independent control needs no dynamic warmup of its own, but it respects the common mask rather than claiming extra coverage. A discrepancy in expected validity, timing or support stops the pilot; it does not create an easier mask.

The loader may validate the twelve allowlisted joint-state channels and timing. The scoring interface receives only the six joint velocities, in the existing joint order. Joint positions are unused by this control. Timestamp differences determine continuity only; timestamps, row coordinates and labels never enter its score. Row coordinates remain output-alignment metadata. The model and its fitting loop receive no `Anomaly State` column.

A sequential CSV reader may have to traverse the prefix before the development start. Such traversal is permitted for record positioning, without fitting, retaining or reporting skipped feature values. It must stop before row 560,002, without consuming an extra record; it must never reach calibration `[702002,864003)` or either protected final slice `[864003,1762650)`. For source-integrity verification only, hashing may traverse the complete original byte stream without parsing or inspecting protected feature values. Record that I/O separately from selected observation parsing. An implementation that cannot enforce the parsing limits is not admitted. No alternate dataset member, attack script, cloud connection or robot execution is part of this pilot.

## One transparent control, with no search

For each of the six velocity channels, fit its arithmetic mean `mu_j` and population standard deviation `sigma_j` from the **46,944 eligible fitting rows only**. Use a streaming Welford accumulator in source order:

```text
n = n + 1
delta = x - mu
mu = mu + delta / n
M2 = M2 + delta * (x - mu)
variance = M2 / n
sigma = sqrt(variance)
```

There is one independent accumulator per channel; `n` must match for all six. Use Python floating-point values and record the actual interpreter/platform. Do not round values, standardize per file, fit on development, clip inputs, remove channels or recalculate statistics during scoring. A nonfinite accumulator or `variance <= 0` in any channel stops with a named diagnostic. There is no unrecorded epsilon floor or fallback: a constant channel would require a separately documented future specification change before another pilot.

The fixed score is:

```text
score(x_t) = max_j(abs((qdot_t[j] - mu_j) / sigma_j))
```

Higher values indicate greater deviation from the fitted marginal reference. Emit one finite score for every eligible development endpoint; fail if a required score is missing, duplicated, misaligned or nonfinite. The current observation defines the score, but does not update the fitted reference. There is no future window, state correction, label input, score smoothing, adaptive calibration or alarm decision.

This is a **single deterministic configuration**: no optimization epochs, hyperparameter grid, model ranking, checkpoint selection or repeated seeds. Seed 42 is reserved by the wider protocol for future stochastic pilots and is unused here. An AR predictor, periodic template and the proposed twin remain later model specifications. The subset reference produced here is a pilot artifact and cannot become a final comparator checkpoint by renaming it; a full-training fit requires its own declared stage and provenance.

## Technical acceptance and reporting

The objective is a pass/fail feasibility check, not minimization of normal scores. Accept only if all of these conditions hold:

1. Source/contract/config identity and isolated-environment provenance are recorded; read boundaries and feature/label separation are verified.
2. The declared 46,944 fitting endpoints are used exactly once, with no undeclared gap or invalid input, and all six positive finite variances are obtained.
3. Exactly 18,472 development endpoints each receive one aligned finite score under the common mask, without fitting or state leakage from development.
4. Reference and score artifacts are saved with hashes, their parameters remain unchanged during development, and the run terminates inside the proposed limits.

Record rows traversed, observations parsed, eligible rows fitted/scored, structural exclusions, failures, elapsed wall time, process CPU time, measured peak RSS and output bytes. Separate fit, development traversal/loading and scoring timings when the runner supports them. Report end-to-end throughput using the rows actually processed, with the exact numerator and timed scope. A short-prefix measurement is not a full-dataset runtime estimate, deployment latency or benchmark result.

**Do not compute a threshold, alarms, attack F1/AP, event recall, detection delay or final normal false-alarm metrics in this pilot.** Calibration remains unused. Synthetic metric test results from software validation are distinct from every real-data artifact. No hypothesis test, confidence interval, speed-change detection conclusion or comparison with author-reported results is supported here.

Keep any actual fit/score data local under a new ignored `experiments/runs/<unique-run-id>/` directory. Proposed artifacts are `run.json`, `resolved_config.json`, `reference.json`, `development_scores.jsonl`, `diagnostics.json` and a log. These names are planned, not existing evidence. On failure, retain the partial artifact/error, stage and coverage; do not replace it with a successful-run-only report.

## Proposed resource bounds and execution gate

The [historical workspace audit](../../docs/WORKSPACE_AUDIT.md) recorded an Apple M5 Pro, 24 GB unified memory and no CUDA device. This plan makes no fresh hardware or runtime measurement. Use CPU only, one worker process, one computation thread, no GPU/MPS, network, paid service or concurrent experiment. The proposed implementation uses the Python standard library in the manufacturing-local isolated environment.

| Bound | Proposed future limit | Required behavior |
|---|---:|---|
| Worker wall time | 600 seconds | Supervisor terminates worker at the deadline and preserves failure evidence |
| Worker process CPU time | 300 seconds | Enforce a process CPU limit; do not silently extend it |
| Resident memory | 1 GiB monitored abort threshold | Sample at most one second apart and terminate on excess; this is not a guaranteed instantaneous memory ceiling |
| Run outputs | 50 MiB | Check before/after writes and stop before exceeding the allocation; no raw copy |
| Selected input ranges | 50,000 training + 20,000 development raw rows | No automatic subset expansion; positioning traversal is separately counted |
| Runs/configurations | One deterministic attempt | Record failure; a retry needs a documented diagnosis and an explicit bounded scope |

These limits are chosen safeguards, **not measured requirements or a claim the run will finish**. The supervising runner must be implemented and tested before execution; no enforcement is present merely because this document or JSON declares a limit. If the platform cannot enforce a bound, revise the plan transparently before running instead of silently omitting it.

The pilot entry command is **not implemented and not specified as runnable**. Working directory would be the manufacturing project root. Actual interpreter, code revision/dirty state, dependencies, exact command, operator, timestamps and artifact hashes remain unset until a real run is prepared. The existing synthetic loader/metric tests do not implement this control or its supervisor.

Before execution:

1. Finish synthetic loader, split-isolation and metric tests, including negative access tests. Record their actual report and code revision.
2. Implement this single control and a bounded runner separately, with synthetic tests for Welford statistics, zero variance, unchanged fitted state and abort behavior.
3. Verify read-only source identity through the existing manifest/integrity procedure without examining protected final feature distributions. Validate policy/config hashes and restrict selected observations to the two prefixes above.
4. Resolve actual environment/interpreter, output location, complete run manifest and exact command. Review memory/timeout enforcement and available local disk space.
5. Proceed only under a subsequent task that authorizes the bounded real-data fit. This current milestone authorizes software tests and pilot specification, not training. Paid compute, lengthy runs and publishing retain their separate approval requirements.

If feasibility succeeds, define the full-training control and the next finite normal-only predictor/template configurations. Do not open calibration to compare these pilot choices; calibration follows the later model/configuration freeze. Both final slices stay protected throughout development.

## Three learning papers remain separate

This ordinary control is our independent implementation when eventually written; it is not a reproduction of any of the learning papers. Their [admission rules](BASELINE_SELECTION_CRITERIA.md) and [paper/code traceability](PAPER_CODE_TRACEABILITY.md) still apply:

- **CASPER:** the paper/code use external IMU inputs; a right-arm controller port changes the experiment. Inspected anomaly-label threshold selection cannot be used here, and original code-use terms remain unresolved.
- **TWINE:** full manuscript access and exact published-run correspondence remain unresolved; inspected supervised/random-row workflows do not enter this normal-only chronological group unchanged.
- **CatBoost on CASPER:** full manuscript and code-use provenance remain unresolved; inspected synthetic-target, modality-stacking and pre-split scaling choices do not define an admitted comparator for this study.

Passing loader/metric tests or this future pilot resolves none of those literature-admission gaps. The study remains one repetitive acquisition under the stated truthful-telemetry assumption, without established novelty, attack attribution or independent-plant generalization.
