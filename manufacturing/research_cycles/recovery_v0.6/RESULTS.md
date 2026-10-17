# Command uncertainty and recovery: completed v0.6 experiment

**17 October 2026.** We implemented a sampled command-model envelope with a separate fixed-return rule, froze new conditions, and evaluated every declared method. The primary candidate reduced benign alarm time and retained alarm evidence through physical return within the modeled mismatch range. It **did not meet the full predeclared success criterion**, and the envelope performed poorly outside that range. A simpler ablation is the more useful lead for further investigation.

All observations are synthetic. This is prospective evidence on newly frozen simulation conditions within a shared plant family, not a new robot acquisition, a paper-baseline reproduction, a safety guarantee or an established original algorithm. [The frozen plan](PLAN.md) and [prior-art assessment](PRIOR_ART.md) separate those claims.

## What was built and executed

The entry score measures distance outside the componentwise range of three command-driven physical models. The recovery rule requires ten consecutive observations close to the nominal command-reference state, with a fixed sensor-noise margin. The recovery tolerance does not expand with the entry envelope. State correction, prediction, entry and clearing have separate code paths; true state and attack schedules are not used in detector calculations; see the configuration-access qualification in [validation](VALIDATION.md).

Thirteen methods received common observations and the same normal-only calibration population. Persistence and AR are explicit command-information ablations; ARX, observers and envelope methods have protected command context. We reused the immutable v0.5 training-only AR/scaler artifacts, fitted only two training-normal mode normalizers, and calibrated each complete alarm process to at most 162 alarmed targets among 16,200 normal targets. This includes retained-alarm duration. Actual counts were 153–162. The procedure differs from v0.5's point-score percentile; its old percentages are not a directly comparable control.

The code, 144-condition roster and success criteria were frozen before new generation. Thresholds and normal artifacts were sealed before fresh observations. All 144 episodes and thirteen methods were saved and hashed before joint evaluation: **1,872 method/episode outcomes, 129,600 eligible targets per method**. There are 96 episodes in the within-range primary stratum; 48 test extrapolation. No outcome-dependent redesign or retry occurred.

## Primary results

Each method has 32,400 eligible benign observations and 60 intervention events in this stratum.

| Method | Benign alarm points | Benign alarm rate | Attack-point recall | Events overlapped / fresh onsets | Events with premature clearing | Maximum clearing delay after physical return |
|---|---:|---:|---:|---:|---:|---:|
| Fused hysteresis | 354 | 1.093% | 91.718% | 60 / 48 | 4 | 0.18 s |
| Mode hysteresis | 514 | 1.586% | 92.008% | 60 / 48 | 0 | 0.86 s |
| Nominal entry + fixed return | 167 | 0.515% | 91.667% | 60 / 48 | 0 | 0.76 s |
| **Envelope entry + fixed return** | **277** | **0.855%** | **92.029%** | **60 / 48** | **0** | **1.18 s** |

The candidate reduced benign alarm points by **21.75%** relative to fused hysteresis and **46.11%** relative to mode hysteresis. It preserved event coverage and had no premature-clear events or unalarmed pre-return samples after first detection. Fused hysteresis had four premature-clear events and 55 such unalarmed samples. All 60 detected candidate events cleared within the five-second recovery allowance.

The predeclared criterion required at least 25% benign-alarm reduction against **both** controls. It failed against fused hysteresis, so `primary_test.passed` is **false**. Recovery and event-coverage requirements passed. This conclusion is not changed by favorable secondary comparisons.

The simpler nominal-entry/fixed-return ablation reduced benign points by **52.82%** versus fused hysteresis and also avoided premature clearing. Its attack-point recall was slightly lower (by 0.052 percentage points), with the same event-hit counts. This suggests that separating the recovery decision deserves further study; it does not establish that a model bank is necessary. Selecting this ablation as the next preferred design after inspecting results is an exploratory decision requiring fresh confirmation.

False alarms have several meanings. The candidate reduced **benign alarm duration**, but produced **155.56 benign alarm episodes/hour**, versus fused hysteresis's 100.00 and the simpler ablation's 33.33. These short synthetic episodes provide only 0.18 eligible benign hours in the primary stratum; hourly rates are normalized descriptive quantities. Attack-interval F1 also penalizes post-command recovery alarms: candidate F1=0.6561, fused hysteresis=0.7278, and nominal/fixed-return=0.7211. Retaining a physically justified alarm after command corruption ends does not improve attack-interval precision automatically. [All thirteen-method results](TABLES.md) retain these trade-offs and AP.

Within-range benign counts by condition also expose the trade-off. Fused hysteresis produced 0 unchanged-normal, 354 authorized-offset and 0 authorized-slowdown alarms. The envelope candidate produced 100, 80 and 97 respectively. Its reduction at command jumps therefore came with new alarms in other legitimate motion. The nominal/fixed-return ablation produced 0, 167 and 0.

## Extrapolation and task dependence

For the mass/damping setting beyond the sampled model range, candidate benign alarms rose to **10,789/16,200 (66.60%)**, compared with fused hysteresis **936/16,200 (5.78%)**. The candidate still overlapped all 30 events, but only 20 had fresh alarm onsets, versus 24 for fused hysteresis. Persistent benign alarms make overlap alone misleading. The simpler fixed-return ablation had **1,143/16,200 (7.06%)**, so it also failed to improve benign alarms in this stratum.

The envelope candidate's outside-range alarms occurred in unchanged normal motion (3,492 points), authorized-offset episodes (3,942) and authorized-slowdown episodes (3,355). Its observed failure is broader than the authorized jump alone. A sampled envelope calibrated inside a restricted model family does not reliably accommodate parameter extrapolation.

Within-range effects also depend on task/plant. Candidate versus fused benign counts were A/low **130 vs 188**, A/high **70 vs 0**, B/low **7 vs 129**, and B/high **70 vs 37**. The aggregate gain is not a uniform gain across conditions. Detailed grouped records are preserved in the validation report.

## Evidence quality and limits

The 23 synthetic tests passed on their first execution. A fresh process passed **8,332 checks**, replaying decisions and normal calibration, checking score identities and independently recomputing contingency counts. No simulation/training failure occurred. The one supervised run took **63.578 seconds wall**, **63.114 CPU seconds**, with **88.66 MiB** sampled peak RSS and approximately **66.71 MiB** of outputs, inside 600s/300s/1GiB/96MiB limits. A separate post-run numerical QA compared eight versus sixteen RK4 substeps on twelve full trajectories: maximum absolute state difference 3.7641e-6, below the 1e-4 reference tolerance. This supports numerical resolution only. Process-memory monitoring is sampled. Exact dependency versions, commands, revision/dirty state, seeds, hashes, logs and terminal outcomes are saved. The previous v0.5 scientific/reporting artifacts and all earlier bound inputs remain unchanged.

The physical-return criterion is evaluator-defined distance to a nominal reference, not verified plant safety. Sensor truthfulness, protected commands, known noise scale, common initial state, absence of delays/friction/backlash beyond the declared damping, and shared simulator/model equations are strong assumptions. Parameter-range membership is not guaranteed state enclosure. There are only two fresh motion tasks and three deterministic plant settings with paired noise seeds. There are no population confidence intervals, significance claims or independent-robot generalization claims. Unknown-context positives count as misses; the 12 primary context-gap events explain the difference between overlap and conservative fresh-onset counts.

The bounded literature review found older interval/adaptive-threshold methods and recent recovery-related AUV work. Exact novelty remains unresolved, especially for the latter's full manuscript/code. Independent entry and return criteria are not, on their own, an original contribution. This experiment establishes a concrete trade-off and an extrapolation failure of **our specified candidate**, not a reproduced defect of CASPER, TWINE or another paper.

## Decision and next bounded research step

Keep fused hysteresis, the nominal-entry/fixed-return ablation, ARX and the following/rolling-mean controls. Do not promote the sampled envelope to the final method. The next research target is **model-adequacy evidence that distinguishes a legitimate dynamics change from command inconsistency without allowing a widened entry model to clear an existing alarm**. First determine the available trusted evidence and whether those cases are identifiable; compare with interval/set-membership fault diagnosis and recovery literature before proposing a new rule. Use this exposed cycle only for development. Freeze disjoint physical assumptions and conditions—such as actuator lag, independently varied mass/damping, new trajectories and noise—before any new confirmatory evaluation. A new candidate must beat the simpler fixed-return control on both alarm duration and episodes, retain event evidence, and expose its failure boundary. No further experiment is silently authorized or reported as completed here.

The original-contribution paper remains the destination. This completed milestone supplies measured evidence for the next design decision; it does not settle the final title or journal.
