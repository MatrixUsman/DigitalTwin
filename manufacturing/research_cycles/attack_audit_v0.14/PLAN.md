# Frozen candidate attack/recovery audit

17 October 2026 (Asia/Karachi). The user explicitly requested evidence for the v0.13 candidate's novelty and attack-detection advantage. This authorizes a small, separately versioned local audit. It does not assert that an advantage or novelty must exist.

## Purpose and admission

The nonlinear correction failed v0.13's all-plant prediction-improvement criterion. That failure remains unchanged. Every reference nevertheless provided the maximum available long/dual return evidence in that normal pilot. The present task asks a different question: does the fixed candidate have an attack/recovery benefit, and which component causes it? This is a bounded diagnostic of a saved candidate, not an automatic promotion past the old gate or a journal-confirmation campaign.

No refitting, hyperparameter search or new mechanism is allowed. Load the v0.13 base, linear and RBF fits and their unchanged thresholds. New controls receive threshold-only calibration from the same five old normal episodes per plant. CUSUM's reference value is computed from three training episodes only. Every scientific choice is frozen before generating new observations. The earlier exposed CASPER recording is not accessed.

## Data and threat model

Use the preserved two-joint simulated robot, controller, sensor-noise model and Q1/Q2/Q3 plant definitions. Three new task parameterizations, new offsets/durations/slowdown and deterministic noise streams are specified in config.json. Three tasks × three plants × three seeds × seven conditions = 189 episodes. Each has 1,200 points at 50 Hz; discard 100 initialization points, leaving 1,100 eligible points. There are 81 wholly benign episodes and 108 attack episodes. Plant identities and simulator families are reused; these are new parameter combinations, not independent robots.

Conditions: unchanged operation; authorized offset and slowdown; unauthorized brief offset, persistent offset, hold and slowdown. In authorized cases approved and executed commands agree. In attacks only executed commands change. Measured states are honest but noisy, and approved commands and the clean initialization are trusted. No sensor-spoofing, missing-context, compromised trusted channel or real-robot claim follows. Detector interfaces receive only observations, approved commands and completeness flags. True/uncorrupted same-plant states and schedule labels belong only to the evaluator.

The simulator can compute truth, but no detector sees it. Seal every saved score/reference/alarm stream before joining truth or publishing any outcomes. State runs continuously through the episode; no reset occurs at attack onset/end. Thresholds and fitted parameters remain fixed.

## Roster and calibration

Seventeen registered methods: base point/instantaneous-return/long-return/dual-return; linear point/dual; RBF point/instantaneous-return/long-return/dual/no-dwell; one-step-following ARX point/dual; RBF applied to the following reference with dual return; persistence; trailing 21-observation mean predictor; and one-sided scalar CUSUM on the base score. All observations and approved commands are available equally, although simpler controls may use a subset.

The following-reference ablations reuse the same ARX coefficients. The RBF-following ablation also reuses the frozen head, so its changed feature distribution must be disclosed; it is not a separately optimized competing model. Point alarms are strict score exceedances. Return methods retain the v0.13 tolerance 0.1, windows 1 or 41 or (5,41), dwell 10, and entry priority. The no-dwell variant uses 1. Persistence predicts the last measured observation; mean21 uses past observations only. CUSUM accumulates `max(0, previous + base_score - k)` after initialization, where k is the mean plus one standard deviation of training base scores. It is not reset at alarms or labels. Its threshold and other new score thresholds use rank 5,445/5,500 on normal calibration. Existing thresholds are checked for exact calibration parity.

Equal point-quantile calibration does not equalize alarm-state duration; report both calibration and fresh benign occupancy. Comparisons between base_dual and rbf_dual share the same rule; rbf_dual versus rbf_long removes the short window only; rbf_dual_nodwell removes dwell. CASPER/Edge learned IMU papers are not renamed as these command/state controls. This study is not a full recent-paper reproduction.

## Metrics and unchanged decision rule

Report unadjusted precision/recall/F1 against the corruption schedule, average precision of continuous scores, complete coverage, benign alarm points and episodes/hour, every event's overlap/fresh onset/miss and schedule delay. Schedule labels are not physical-damage labels. Retained post-corruption alarms count as schedule false positives; also report the separate physical-return outcomes so that this is interpretable.

Physical return is evaluator-only: first run of ten post-corruption states within 0.1 standardized distance of the uncorrupted same-plant trajectory. From the first detected event point until return, report every unalarmed point and any premature falling edge, including gaps during corruption. If return is absent, censor at the episode end and retain that outcome. For detected-and-returned events, record first alarm-free point at/after return within 250 observations and delay. Report unalarmed-at-return separately; it must not conceal premature clearing. Misses never disappear from event denominators.

**Primary candidate advantage:** rbf_dual must, on each plant, have at least as many overlap and fresh hits, no more premature-clear events, at least as many timely clearances, and no higher benign occupancy or pre-return gap count than base_dual. Additionally, pooled benign occupancy or pre-return gap count must fall by at least 10%, with a nonzero comparator denominator. No post-result relaxation. Report zero/undefined denominators explicitly. This is a pragmatic effect-size gate, not a statistical significance or novelty test. All 17 methods and all task/condition/plant strata remain visible regardless of this outcome.

Additional predeclared contrasts: base_dual versus following_dual (reference-following effect), rbf_dual versus rbf_long and no-dwell (gate components), and comparison with simple/CUSUM controls. Secondary wins cannot replace a failed primary result. Shared simulator/trajectories and three paired noise seeds do not support independent-robot population inference; no p-values are planned.

## Bounds, tests and provenance

One no-retry attempt, 120 s wall / 90 s CPU / 1 GiB sampled RSS / 128 MiB output. v0.13 measured 16.1 s for 81 episodes; this 189-episode, no-training study is a small bounded extension. Preserve failure and incomplete outcomes if the cap is exceeded. No paid compute, publishing, full CNN training or data acquisition.

Before execution, synthetic tests cover causal controls, trusted-input separation, no model mutation, calibration order-statistic/ties, CUSUM recurrence, event onsets/offsets, premature clears and censored/missed return cases. Freeze code, configurations, saved fits and allowed normal files. Record commands, environment, revisions, resource use, logs and source hashes. A fresh-process verifier replays saved inference and independently checks contingency counts and recovery arithmetic. Separate exact identities, floating-point tolerance checks and scientific scope.
