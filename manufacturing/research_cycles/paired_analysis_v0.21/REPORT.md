# Episode-paired analysis of the completed contextual-recovery study

## Material Passport

- Project: manufacturing; analysis v0.21, 19 October 2026 (Asia/Karachi).
- Mode: saved-result validation and descriptive reporting, after final exposure.
- Inputs: hash-bound v0.19 synthetic outcomes; no new training, simulation or real-data access.
- Verification: replayed descriptive arithmetic; this is not independent scientific replication.
- Original criterion: failed, preserved without changing a clause or denominator.

## What was already complete, and what this adds

v0.19 already reported pooled and task/plant/intervention summaries, delay missingness, and an independent audit of uncertainty-band and recrossing behavior. The v1.7 reviewer archive already passed clean extraction, saved-table replay and synthetic tests. Those completed tasks were not rerun or relabelled as new experiments.

This addendum joins each context_set outcome to the same episode from base_dual, context_hysteresis and global_set. It reports signed within-episode differences, win/tie/loss counts, fresh-detection and joint-success discordance, and complete delay denominators. Its compact archive includes the saved summary inputs and a dependency-free replay. It does not change the manuscript or replace the original reviewer archive.

## Population and interpretation

Each contrast matches all 216 synthetic episodes: 72 benign episodes (2.36 eligible hours) and 144 interventions. The same two task families, six plant configurations and three noise seeds recur across conditions. The 648 paired rows are three comparisons of the same 216 episodes, not 648 independent experiments. Results describe this finite simulator grid; neither samples nor noise seeds provide independent robots or acquisitions.

Every delta is candidate minus comparator. For alarm occupancy, alarm starts, outside-inactive points and delays, a negative value is preferable in that one metric. For fresh detection and joint success, a positive value is preferable. A single-metric win does not imply overall superiority. Point counts are sampled at 0.02 seconds. Benign counts concern benign episodes only; post-intervention recovery occupancy is not silently called a false alarm.

## Pooled paired effects

| Comparator | Metric | Pairs observed / possible | Candidate wins / ties / losses | Sum of paired differences | Mean paired difference |
|---|---|---:|---:|---:|---:|
| base_dual | alarm_points | 72 / 72 | 72 / 0 / 0 | -4.186e+04 | -581.403 |
| base_dual | alarm_episodes | 72 / 72 | 72 / 0 / 0 | -3247 | -45.0972 |
| base_dual | outside_inactive | 144 / 144 | 0 / 62 / 82 | 679 | 4.71528 |
| base_dual | joint | 144 / 144 | 0 / 62 / 82 | -82 | -0.569444 |
| base_dual | fresh | 144 / 144 | 8 / 136 / 0 | 8 | 0.0555556 |
| base_dual | fresh_delay | 136 / 144 | 0 / 104 / 32 | 10.46 | 0.0769118 |
| base_dual | clear_delay | 144 / 144 | 144 / 0 / 0 | -118 | -0.819722 |
| context_hysteresis | alarm_points | 72 / 72 | 0 / 56 / 16 | 131 | 1.81944 |
| context_hysteresis | alarm_episodes | 72 / 72 | 9 / 63 / 0 | -11 | -0.152778 |
| context_hysteresis | outside_inactive | 144 / 144 | 98 / 46 / 0 | -337 | -2.34028 |
| context_hysteresis | joint | 144 / 144 | 50 / 94 / 0 | 50 | 0.347222 |
| context_hysteresis | fresh | 144 / 144 | 0 / 144 / 0 | 0 | 0 |
| context_hysteresis | fresh_delay | 144 / 144 | 0 / 144 / 0 | 0 | 0 |
| context_hysteresis | clear_delay | 144 / 144 | 0 / 5 / 139 | 7.8 | 0.0541667 |
| global_set | alarm_points | 72 / 72 | 5 / 59 / 8 | 27 | 0.375 |
| global_set | alarm_episodes | 72 / 72 | 10 / 62 / 0 | -14 | -0.194444 |
| global_set | outside_inactive | 144 / 144 | 17 / 125 / 2 | -88 | -0.611111 |
| global_set | joint | 144 / 144 | 2 / 140 / 2 | 0 | 0 |
| global_set | fresh | 144 / 144 | 0 / 144 / 0 | 0 | 0 |
| global_set | fresh_delay | 144 / 144 | 10 / 134 / 0 | -1.38 | -0.00958333 |
| global_set | clear_delay | 144 / 144 | 19 / 125 / 0 | -0.66 | -0.00458333 |

Delay sums are descriptive sums of per-episode seconds, not elapsed wall time or an operational event-rate quantity. Clear-delay preference is conditional: an alarm already off at return can have zero delay despite earlier loss of physical support.

The tradeoff against base_dual is consistent across benign episodes: all 72 have fewer alarm points and starts. The candidate gains eight fresh detections but loses joint support in 82 of 144 intervention episodes, with no joint-support gain. Among the 136 episodes where both methods freshly detect, 32 have later candidate detection and 104 tie. The eight events without a fresh base-dual detection remain explicit; their missing delays are not replaced by zero or discarded from the detection denominator.

The matched recovery-component comparison is stronger than a pooled-total difference alone: relative to context_hysteresis, outside-inactive time improves in 98 episodes and ties in 46, with no worsening. Joint success improves in 50 episodes and never worsens. This comes with more benign occupancy in 16 episodes (56 ties), although alarm starts decrease in nine (63 ties). Clearance occurs later in 139 events and ties in five. The component therefore changes a measurable support/occupancy tradeoff, without establishing an original algorithm or satisfying the overall declared criterion.

Context conditioning offers a modest and heterogeneous comparison against global_set: outside-inactive counts improve in 17 episodes, tie in 125 and worsen in two. Both methods have 62 joint successes, but they are not exactly the same successes: 60 overlap, two favor each method. Benign occupancy improves in five episodes and worsens in eight. This does not support uniform superiority of contextual conditioning.

## Fresh detection, joint success and delay denominators

| Comparator | Fresh both / candidate only / comparator only / neither | Joint both / candidate only / comparator only / neither |
|---|---:|---:|
| base_dual | 136 / 8 / 0 / 0 | 62 / 0 / 82 / 0 |
| context_hysteresis | 144 / 0 / 0 / 0 | 12 / 50 / 0 / 82 |
| global_set | 144 / 0 / 0 / 0 | 60 / 2 / 2 / 80 |

Each discordance row uses all 144 intervention episodes. A fresh detection is an alarm rising edge within the scheduled intervention; overlap by an already-active alarm is a different outcome. Joint success requires overlap detection, zero post-onset outside-tolerance inactive points, an observed sustained physical return and inactivity within five seconds of that return. It includes detection latency in the support condition. It is a strict finite-grid outcome, not a safety guarantee.

All four methods overlap all 144 interventions, and all 144 have an evaluator-defined sustained physical return. All have an observed clearance-delay value, with no censored clearance among detected/returned events. However, context_set and global_set are already inactive at return in two events each, and context_hysteresis in 116; base_dual is active in all 144. A shorter clearance delay therefore cannot be read as better recovery recognition on its own. The saved missingness records separately report missed overlap, missing fresh detection, absent return, clearance censoring and already-inactive status.

## Task and plant strata

The table reports signed differences in counts. All finer task × plant × condition cells (three paired noise seeds per cell), intervention and matched/shifted strata are retained in paired.json and paired_effects.csv, including zero effects. These are descriptive decompositions, not a selection process for favorable conditions.

| Comparator | Stratum | Benign point difference | Outside-inactive point difference | Joint-success difference |
|---|---|---:|---:|---:|
| base_dual | task: L19 | -25406 | 218 | -34 |
| base_dual | task: S19 | -16455 | 461 | -48 |
| base_dual | plant: Q1 | -5084 | 104 | -15 |
| base_dual | plant: Q2 | -4671 | 81 | -11 |
| base_dual | plant: Q3 | -3704 | 150 | -15 |
| base_dual | plant: U1 | -16372 | 50 | -11 |
| base_dual | plant: U2 | -6514 | 105 | -15 |
| base_dual | plant: U3 | -5516 | 189 | -15 |
| base_dual | plant_group: matched | -13459 | 335 | -41 |
| base_dual | plant_group: shifted | -28402 | 344 | -41 |
| context_hysteresis | task: L19 | 52 | -125 | 31 |
| context_hysteresis | task: S19 | 79 | -212 | 19 |
| context_hysteresis | plant: Q1 | 0 | -18 | 5 |
| context_hysteresis | plant: Q2 | 0 | -37 | 10 |
| context_hysteresis | plant: Q3 | 0 | -108 | 9 |
| context_hysteresis | plant: U1 | 8 | -47 | 8 |
| context_hysteresis | plant: U2 | 7 | -40 | 9 |
| context_hysteresis | plant: U3 | 116 | -87 | 9 |
| context_hysteresis | plant_group: matched | 0 | -163 | 24 |
| context_hysteresis | plant_group: shifted | 131 | -174 | 26 |
| global_set | task: L19 | 8 | -15 | -1 |
| global_set | task: S19 | 19 | -73 | 1 |
| global_set | plant: Q1 | 0 | 0 | 0 |
| global_set | plant: Q2 | 0 | -2 | 0 |
| global_set | plant: Q3 | 0 | -23 | -1 |
| global_set | plant: U1 | 2 | 0 | -1 |
| global_set | plant: U2 | -5 | -18 | 0 |
| global_set | plant: U3 | 30 | -45 | 2 |
| global_set | plant_group: matched | 0 | -25 | -1 |
| global_set | plant_group: shifted | 27 | -63 | 1 |

## Statistical interpretation audit

All eleven research-skill checks were considered. No p-values, sampling confidence intervals, hypothesis tests or seed bootstrap are reported. A finite-grid percentile is an order-statistic summary, not a confidence interval.

| Check | Assessment for this analysis |
|---|---|
| Simpson-type aggregation reversal | Paired task/plant/intervention cells are supplied; global_set effects vary by condition, so pooled gains are not called uniform. |
| Ecological fallacy | Episode-level outcomes are not generalized to robots, sites or people. |
| Selection/Berkson bias | The finite, deliberately constructed simulator grid is not a random deployment sample. |
| Collider bias | No adjustment regression is fitted; conditional delay subsets are labelled and paired with full-event discordance. |
| Base-rate neglect | 72 benign and 144 intervention episodes and 2.36 benign hours are explicit; no deployment precision is inferred. |
| Regression to the mean | Same-episode simultaneous method contrasts; no extreme-case pre/post improvement inference. |
| Survivorship bias | All 216 episode pairs per contrast remain present; missing fresh delays and clearance reasons are explicit. |
| Look-elsewhere effect | All declared contrasts, metrics and strata retained; no significance search or best-stratum claim. |
| Forking paths | This is explicitly post-final reporting; original success requirements remain unchanged and failed. |
| Correlation/causality | Matched mechanism differences describe this simulated intervention, without real-robot causal generalization. |
| Reverse causality | Outcome summaries do not fit a causal model or tune the detectors. |

## Verification and limits

Eight explicitly synthetic unit tests pass. Replay verifies 6,189 arithmetic/coverage conditions, producing 648 episode pairs, 267 group contrasts and 1167 metric rows. Original pooled/stratified totals and delay distributions are independently reconstructed from all 2,376 saved method–episode outcomes. The initial schema collision failed before any derived scientific output; ATTEMPT_HISTORY.json preserves that failure and its reporting-only correction.

The replay starts from saved episode outcomes. It does not regenerate physical trajectories or re-evaluate alarm streams; those checks were completed and sealed in v0.19. It cannot establish simulator fidelity, original method novelty, a reproduced published detector, or independent physical confirmation. This addendum changes no model choice, threshold, original success requirement, manuscript or submission status.
