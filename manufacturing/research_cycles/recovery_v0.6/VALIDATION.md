# Validation record

Material: manufacturing v0.6; owner Haiqa Mushtaq; operator Codex; all data synthetic. Source: [frozen protocol](PLAN.md), saved run, normal calibration and complete joint outcomes. **Status: arithmetic/decision replay VERIFIED; scientific interpretation ANALYZED; physical fidelity externally unvalidated.** Skill used: [academic-research-suite](../../../.agents/skills/academic-research-suite/SKILL.md), bounded experiment validation performed inline. This is not an independent external review or a second end-to-end simulation run.

Pre-execution checks: 23 tests passed. Freeze binds 12 source/specification files and 575 existing input/source/receipt identities. The test receipt includes the exact command and source hashes. Fresh-process verification passed 8,332 explicit checks, including minimal stateful thresholds, source/score hashes, fresh noise identities, all 1,872 decisions/outcomes and independent TP/FP/FN arithmetic. Verification uses the same declared decision/metric implementation for replay; those checks cannot rule out every shared scientific error. The synthetic tests independently enumerate threshold candidates and assert analytically constructed alarm/recovery cases.

The post-run numerical audit compares eight versus sixteen RK4 substeps for the twelve complete normal/authorized-offset task/plant trajectories. Its receipt is `local/recovery_v0.6/numerical_audit.json`. This is numerical QA selected after the run, not a fresh performance experiment or permission to change the frozen physics. No source, saved observation or threshold is changed by it.

## Statistical interpretation: 11/11 patterns checked

| Pattern | Assessment |
|---|---|
| Simpson's paradox / aggregation | Primary and extrapolation strata kept separate. Within-range candidate improvement reverses on both high-plant task cells: A/low 130 vs 188 benign points; A/high 70 vs 0; B/low 7 vs 129; B/high 70 vs 37 (candidate vs fused). No uniform-effect claim. |
| Ecological fallacy | No inference from aggregate points to robots, factories or individual real incidents. |
| Berkson/selection bias | Designed conditions selected after v0.5 diagnosis; not representative samples. No model/episode dropped. |
| Collider bias | No covariate adjustment or outcome-conditioned population used for the primary comparison. Recovery delay necessarily conditions on detection/return; report all misses and no-return cases alongside it. |
| Base-rate neglect | Primary attacks occupy 9,660/86,400 targets (11.18%); stress 4,830/43,200 (11.18%). These are designed prevalences, not deployment estimates. Benign-only alarms, F1, AP and event results are all shown. |
| Regression to mean | v0.5 diagnosis is exploratory. New tasks/parameters/noise are prospectively frozen, with all matched controls run. Improvements are compared within v0.6, not old versus new thresholds. |
| Survivorship bias | All 144 episodes, 13 methods, 1,872 outcomes and the single terminal success retained. Persistence/AR misses and CUSUM non-clearing remain visible. No seed chosen. |
| Look-elsewhere effect | Full roster and conjunctive primary criterion declared before fresh generation. Failed primary criterion reported. No significance testing or selective p-values. |
| Forking paths | Local source/configuration freeze and before-generation calibration seal preserved. Not external preregistration. Earlier exploratory v0.1–v0.5 paths remain recorded. Selecting a different final method from this result is a new exploratory step. |
| Correlation versus causation | Alarm differences are paired algorithmic comparisons in a fixed simulator. v0.5 residual/jump association is a diagnosis, not proof of a real-system causal failure or published-baseline weakness. |
| Reverse causality | Commands and detector scores are causal in replay, with score-before-measurement-correction checks. Labels and true state enter only delayed evaluation. No inferred causal claim from observational real data. |

## Presentation and scientific caveats

Plots and tables are generated from the saved aggregate. Figures show all thirteen methods and both strata; example trajectories are explicitly synthetic. The first rendering displayed warmup alarm strips without qualification and emitted font-cache warnings; preserved under `local/recovery_v0.6/presentation_draft_001`. The final rendering marks warmup and excludes its alarm strips, with project-local font cache configuration. No numerical table values changed. The presentation is not an additional experiment.

Recovery uses a fixed nominal reference with known noise scales. It has no certified probability or physical-safety interpretation. Sampled bounds do not inherit interval-observer guarantees. Rerun agreement verifies artifact consistency, not robot realism. Exact code-use/run correspondence for the paper comparators and recent close-prior-art full text remain separate unresolved research gates.

Implementation-access clarification: the frozen worker passes the full configuration dictionary to numerical functions, so the plan's statement that detectors never “receive” scenario metadata is too strong as an interface-isolation claim. The functions use only the declared physical/score settings, and true state/label arrays are not passed to scoring. A separate post-run `config_access_audit.py` replays every score/decision with a restricted key mapping and checks the first sixteen propagated observer/bank states of every episode. Its receipt records 4,176 passing checks, exact agreement and allowed keys. This is output-dependency evidence, not an OS/capability boundary. The original plan/source remain unchanged; the qualification corrects interpretation without altering any outcome.
