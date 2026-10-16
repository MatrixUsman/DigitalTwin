# Evaluation-definition review

Date: 16 October 2026. Scope: the selected CASPER right-arm study's evaluation documents and metadata. Status: **internal design review; no implementation, model or benchmark validated**.

The parent used the academic-research-suite experiment-planning workflow, with three separate shared-context agent tasks: metric specification, final-test governance and read-only evaluation audit. The read-only reviewer then examined the integrated documents and JSON. This is an internal multi-agent review, not external peer review, researcher comprehension assessment or a blind independent replication.

## Findings and dispositions

| Finding | Disposition |
|---|---|
| Exact support needed after partition/gap warmup | Independently recomputed training 536,946; development 160,472; calibration 160,473; held-out normal 214,473; mixed 682,646; final 897,119. All eight events remain intact. |
| Calibration rank and ties can differ across library defaults | Explicit one-based rank 158,869 at `m=160473`, strict `>`, no interpolation/jitter. Maximum calibration exceedances 1,604, with no future false-alarm guarantee. |
| Missing predictions can favor a method if dropped | Full finite score coverage required at fixed eligible endpoints; failures and diagnostics retained, no primary partial-support comparison. |
| Normal holdout can be mistaken for spare validation | Both final slices protected from model selection, unsupervised feature inspection and recalibration. |
| AP and undefined F1 may be implemented incorrectly | Tie-grouped noninterpolated AP; direct count-based F1 and metric-specific denominator rules; synthetic acceptance examples specified. |
| Event overlap does not establish a fresh alarm | Separate overlap, pre-existing alarm, known negative-to-positive onset and censoring; no label-boundary resets. |
| Repeated seeds can be mistaken for independent acquisitions | Three fixed stochastic seeds, deterministic controls once, full run matrix, descriptive paired outcomes; no independent-row/event/seed significance claims. |
| Protection document initially said output saving was only “where feasible” | Revised to require saved/hashed score artifacts before label join/reveal, with terminal failure records so incomplete runs neither vanish nor prevent a complete failure report. |
| Metric draft mentioned frozen persistence/cooldown despite direct threshold decisions | Revised to exclude separate post-threshold filtering. Predeclared causal score aggregation may be part of a method, but every alarm remains `score > threshold`. |
| Public shared CSV precludes a credible blindness claim | Disclosed previous metadata/source-result inspection; protection is procedural and prospective, with evaluator interfaces still planned. |
| A completed plan might be confused with completed artifact freeze | Pending record uses null timestamps/artifacts and empty run lists; actual model selection, calibration and final replay remain unexecuted. |

The audit reviewer confirmed both draft ambiguities resolved. The linked [protocol](EVALUATION_PROTOCOL.md), [metrics](METRIC_DEFINITIONS.md), [protection procedure](FINAL_TEST_PROTECTION.md), [policy](../configs/casper_right_arm_evaluation_v0.1.json) and [pending record](../experiments/FINAL_TEST_FREEZE_RECORD.json) are the resulting definitions. Review did not read raw joint observations or create detector scores.

## Validation boundary

The ignored `local/evaluation_protocol_review/` folder contains the metadata builder, integration validator and receipt. The validator checks referenced hashes, split/support arithmetic, pending statuses, policy consistency, local links and small explicitly synthetic arithmetic examples. It uses prior immutable data-contract evidence rather than rehashing/reprocessing raw data. The work log records the actual command and outcome. These checks do not establish that an unimplemented loader, metric library, model, evaluator access boundary or final campaign works.

Remaining gates: exact model formulas, train-only transforms, causal initialization/history, finite normal-only development objective/search/tie rules, isolated dependencies, executable synthetic tests, bounded pilot and actual artifact freeze. One acquisition, uncertain physical onset, truthful-telemetry assumptions, incomplete comparator manuscripts and unverified novelty remain scientific limitations.
