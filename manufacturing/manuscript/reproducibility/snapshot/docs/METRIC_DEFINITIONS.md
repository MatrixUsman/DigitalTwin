# CASPER right-arm metric definitions

## Material Passport

- Origin skill/mode: academic-research-suite / experiment-agent / plan.
- Project/owner: manufacturing / Haiqa Mushtaq.
- Date/version: 16 October 2026 / metric specification v0.1.
- Verification status: **specified before detector execution; not implemented or benchmark-validated**.
- Inputs: [annotation/feature/split contract](ANNOTATION_FEATURE_SPLIT_CONTRACT.md), [original machine-readable contract](../configs/casper_right_arm_contract_v0.1.json), [question and threat model](RESEARCH_QUESTION_AND_THREAT_MODEL.md).

This specification resolves metric and missing-score choices left open in the earlier design contract. It preserves that contract's row ranges, schedule annotation, single operating point and continuous replay. It does not authorize model fitting or final evaluation. The definitions below describe our comparison, not the original papers' evaluation rules.

## Populations, score identity and coverage

All indices refer to zero-based data rows, excluding the CSV header. End indices are excluded. Let `y_i` be the recorded schedule flag, `t_i` the native right-arm elapsed timestamp, `s_i` a scalar score whose larger values mean greater deviation, and `a_i = 1[s_i > tau]`. The score's target is the **current endpoint's flag**. No window-majority labels, point adjustment, grace period, post-hoc label shift or interpolation is allowed.

| Population | Row range | Required use |
|---|---|---|
| Calibration | `[702002, 864003)` | Set the threshold once, after normal-only model selection |
| Held-out normal | `[864003, 1080004)` | Final normal alarm burden and coverage |
| Mixed schedule/recovery | `[1080004, 1762650)` | Primary point metrics and supporting average precision |
| Final replay | `[864003, 1762650)` | One continuous state/episode stream; no reset between the two reporting slices |

The structural eligibility mask `E_i` is shared across methods and determined only by the frozen input-validity, gap and common-warmup rules. It is not inferred from detector outputs. With the current 1,528-preceding-observation warmup and audited gap locations, the expected eligible populations are:

- Calibration: **160,473** of 162,001 raw rows, starting at row 703,530.
- Held-out normal: **214,473** of 216,001 raw rows, starting at row 865,531.
- Mixed schedule/recovery: all **682,646** rows: **345,602** schedule-positive and **337,044** schedule-zero.
- Complete final replay: **897,119** of 898,647 raw rows. There is no new warmup at row 1,080,004.

These are contract-derived expected counts, not generated predictions. A loader must validate them before scoring. Any future change in required history needs a versioned common mask fixed before final outcomes, not selective trimming for one method.

For each partition and reporting slice retain `raw_rows`, `structurally_eligible_rows`, structural exclusions by reason, `finite_scored_rows`, unexpected missing/nonfinite scores, and positive/zero support. Report both `finite_scored_rows/raw_rows` and `finite_scored_rows/structurally_eligible_rows`; use `NA` if a denominator is zero. Warmup is an expected coverage exclusion, not a detector failure.

**Comparative admission requires a finite score for every structurally eligible row** in development, calibration and final replay. A crash, nonfinite score, model-specific abstention, duplicate score, missing endpoint, wrong row identity or timestamp misalignment fails that run's admission. Preserve its failure record and coverage; do not silently remove it from the declared run matrix. Do not repair missing decisions with alarm/non-alarm imputation, forward-filling, or a favorable intersection of methods' scored rows. Finite-subset diagnostics may help investigate a failure, but must be labelled `diagnostic_incomplete_run` and cannot enter the primary comparative table. If an otherwise permitted model cannot meet the common support, resolve that limitation using normal data before final release.

Structural unknowns remain distinct from computational failures: an input-invalid row, a declared gap and warmup are visible in the shared mask. They break observed alarm continuity. An unexpected model-missing score also makes observed alarm state unknown for diagnostics, while still failing comparative admission. Neither case is evidence that the underlying physical condition stopped.

## One fixed calibration rule

Each method/declared stochastic replicate is calibrated independently using its own complete finite scores on the **same normal-calibration endpoints**. After fitting/selection, reset causal state at calibration start, use the declared warmup, score before updating state, and hold fitted parameters and residual normalization fixed.

For `m > 0` scores sorted ascending as `z_(1), ..., z_(m)`, define:

```text
k = ceil(99*m/100) = (99*m + 99) // 100
tau = z_(k)                 # one-based rank
alarm = score > tau         # equality is not an alarm
```

For the current expected `m = 160473`, `k = 158869`. Save `m`, `k`, the exact stored threshold, score dtype, score-artifact hash and the number of calibration scores strictly above it. No interpolation, epsilon, jitter or randomized tie-breaking is allowed. Use the numeric value at that rank. NumPy's default quantile interpolates and therefore is not this rule; its documented `inverted_cdf` method is the corresponding discontinuous empirical-quantile convention. The explicit rank above remains authoritative. [NumPy quantile documentation](https://numpy.org/doc/stable/reference/generated/numpy.quantile.html)

If `m = 0`, any eligible calibration score is missing/nonfinite, or the expected mask does not match, no valid threshold exists for this protocol. Do not fall back to test statistics. Constant calibration scores legitimately produce zero calibration exceedances under strict `>`; record that fact without changing the rule.

This is an empirical calibration point near a 1% upper-tail budget, **not a guarantee of 1% future false positives or a calibrated episode-arrival rate**. There is no second test-selected operating point. Final labels, final scores, final normal alarm burden and recovery segments cannot tune the threshold or select a method. Residual scaling/fusion and causal score aggregation are method choices to freeze earlier. This protocol permits **no separate post-threshold persistence or cooldown**: every decision remains exactly `1[score > tau]`. A later alarm-filtering study would require a separate declared protocol, not an undocumented transformation of these decisions.

## Point metrics: counts first

Compute the primary binary metrics only on structurally eligible endpoints in the mixed schedule/recovery slice, and only for an admitted complete run. Each endpoint has unit weight. Report the four integer counts alongside the metrics:

```text
TP = count(y == 1 and a == 1)
FP = count(y == 0 and a == 1)
FN = count(y == 1 and a == 0)
TN = count(y == 0 and a == 0)
precision = TP / (TP + FP)
recall    = TP / (TP + FN)
F1        = 2*TP / (2*TP + FP + FN)
```

Use the positive class `1`, with no macro, weighted-class or micro averaging. Check `TP + FP + FN + TN = eligible mixed rows`. Each metric is `NA` only when **its own denominator** is zero. Consequently, with positive labels but no alarms, precision is `NA`, recall is zero and F1 is zero. With neither positive labels nor alarms, all three are `NA`. Compute F1 from counts; propagating an undefined precision through a harmonic-mean formula would incorrectly erase a defined zero F1. The underlying formulas and zero-denominator cases are documented by [scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_fscore_support.html); our explicit `NA` policy supersedes any library default replacement value.

For held-out normal, report **point exceedance** `number of alarm-positive eligible endpoints / eligible normal endpoints`, with numerator and denominator. It measures alarms in the assumed commissioning regime, not a verified population false-positive probability. Separately report the same count/rate for all schedule-zero rows inside the mixed slice and for each recovery/inter-event interval; these are not independently certified healthy operation.

Do not pool the held-out-normal prefix into primary mixed-slice confusion counts. Such pooling changes prevalence and is a different analysis. Do not let long true-negative periods or aggregate accuracy replace the declared metrics.

## Average precision and tied scores

Average precision (`AP`) is a supporting ranking metric on exactly the same complete mixed-slice population. Sort **distinct score values** descending. Include all observations tied at a value together; neither input order nor labels may break a tie. At distinct score group `g`, let cumulative precision be `P_g`, cumulative recall be `R_g`, and `R_0 = 0`. Then:

```text
AP = sum_g (R_g - R_(g-1)) * P_g
```

This noninterpolated recall-increment definition differs from trapezoidal precision–recall area. Name the output **average precision**, not an unspecified “PR-AUC.” [Scikit-learn AP documentation](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html)

If there are no positive labels or no eligible rows, report `NA` with that reason. If every eligible label is positive, AP is 1 for finite scores but conveys no negative-class separation; retain the support count. Scores must be finite before sorting. AP does not choose an operating threshold; no best-F1 or optimal-threshold result is generated from final labels.

## Observed alarm episodes and native-time exposure

An observed episode is a maximal run of adjacent original-row endpoints with `E_i = 1`, finite scores and `a_i = 1` within one continuous stream segment. A known eligible negative endpoint closes it. A gap, unscored/unknown endpoint or stream end terminates the **observed segment**, with cessation unobserved. Keep a stable episode ID across evaluator reporting slices and schedule transitions; labels never reset or join episodes.

- **Left-censored:** its first positive endpoint has no immediately preceding eligible finite decision in the same segment. Its true alarm onset is unknown. Count the observed episode, but do not call it a fresh onset.
- **Right-censored:** its last positive endpoint is followed by an unknown/gap/end rather than an observed eligible negative decision. Its cessation is unknown.
- A reporting boundary is not censoring of the global episode. Record separately whether the episode crosses the reporting slice's start/end.

For a reporting set `H`, eligible exposure in seconds is:

```text
T_H = sum(t_i - t_(i-1))
      over original-adjacent rows i-1 and i that both belong to H,
      both are structurally eligible with finite scores,
      and belong to the same continuous stream segment.
```

Use verified native elapsed seconds. Exclude every gap/unknown/warmup or reporting-boundary-crossing interval. Do not substitute `row_count / 20`, count isolated points as positive exposure, interpolate or extrapolate after the final point. Preserve exact source timestamp serialization in provenance; computing reported seconds cannot establish greater clock accuracy.

For held-out normal `H`, count each global observed episode with at least one eligible positive endpoint in `H` once. The rate is `episode_count / (T_H / 3600)`, or `NA` if `T_H = 0`. Report count, seconds, hours, censoring counts and boundary-crossing counts. Call it **observed alarm episodes per eligible hour**, not independent incident arrivals. Very short observed slices can legitimately have a large rate; retain the denominator. For an incomplete run this is only a diagnostic, never a way to rescue comparative admission.

## Eight schedule-event outcomes and delay

All **eight** fixed positive intervals remain in the event denominator. For each `[b_e, c_e)`, save its exact row bounds, first-positive native time, eligible/scored counts, coverage exclusions, and these outcomes:

1. `interval_overlap_hit`: any eligible positive decision within the interval. `event_recall = number of hits / 8`. An interval with no eligible score is a miss and an explicit coverage failure, not removed.
2. `first_overlap_row/time` and `schedule_relative_overlap_delay_seconds = t_first_overlap - t_b_e`, or `null` with reason `no_overlap_alarm` when missed. A delay is evaluated relative to the recorded flag, not independently measured physical onset.
3. `pre_existing_alarm`: `true` if the first event row and its immediately preceding row have eligible positive decisions in the same segment; `false` if that boundary has known decisions and no continuous positive alarm crosses it; `unknown` if its prior/current decision state is unavailable. A continuing alarm can give zero overlap delay without fresh detection.
4. `first_fresh_onset_row/time`: the first `0 -> 1` decision transition inside the event, requiring the immediately preceding original row to have an eligible finite zero decision in the same segment. Its schedule-relative delay is `t_onset - t_b_e`. A positive first scored point after unknown/warmup is not a known transition. If absent, save `no_new_onset`; this can coexist with an overlap hit.
5. The overlapping episode IDs and their censoring flags. These explain whether apparently different event hits came from one sustained alarm.

Also report `events_with_fresh_onset / 8`, explicitly separate from interval-overlap event recall. The complete eight-row table is mandatory. If summarizing delay, report the number of detected intervals, misses and intervals without a fresh onset beside median/range; do not encode missed delays as zero, omit them from the event denominator or present detected-only delay as whole-system effectiveness. No grace window or boundary relabelling is justified by the available physical-onset evidence.

## Joint comparison and computational cost

The primary contrast remains the progression-aware observer/twin against its otherwise matched progression-omitted variant. The mixed-slice P/R/F1/counts, held-out-normal point exceedance, episode burden and both coverage measures are **joint mandatory outcomes**. AP and all event outcomes are mandatory supporting outputs. Report paired differences in their natural units and the full comparison/control table. A favorable AP or event-hit count cannot conceal worse false alarms, coverage failures or inferior ordinary-detector controls. No post-hoc composite score, preferred seed, omitted variant or chosen operating point may declare a winner.

Runtime is separate from detection delay. Future run records must distinguish fit time, calibration time, model load/setup, input parsing, and sequential online processing. Measure online processing with a monotonic wall clock at batch size 1, covering feature transformation, state propagation, scoring and state update. Record hardware, interpreter/dependencies, synchronization needed for any accelerator, record count, total seconds, seconds per input record, throughput, and—if instrumented consistently—per-record median and nearest-rank 95th percentile. Include warmup input processing in the separately labelled whole-replay processing cost. Record instrument/timing overhead and whether file I/O is included. No recorded compute time establishes transport latency, physical onset latency or live real-time deployment.

The declared stochastic replicate seeds are **17, 42 and 2026**, paired across the progression-aware and progression-omitted variants. Calibrate each fitted replicate separately. Run deterministic controls once and identify their deterministic status; comparing that one control with three stochastic runs does not create three independent control replications. Retain all per-seed metrics, counts, statuses and matched-seed differences. Summarize complete defined values using unweighted mean, median and minimum/maximum; never pool score sequences/confusion counts across seeds, ensemble them or choose the most favorable seed. For the primary paired effect, report `aware minus omitted` for F1, normal point exceedance and normal episodes/hour together with coverage; positive F1 and negative burden differences point in different desirable directions and must not be collapsed into a post-hoc scalar winner.

Repeats measure computational variation on **one recording**, not independent robots or attacks. Retain every declared replicate and failure. If a frozen run is incomplete, report all run statuses and no complete-case comparative average that silently drops the failed run. No comparative claim is admitted until all frozen run outcomes are accounted for under the failure policy. Do not construct confidence intervals or significance tests by treating rows, adjacent windows, eight schedule intervals or repeated seeds as independent plant experiments. Undefined metrics stay visible. If any replicate's metric is `NA`, the corresponding aggregate is `NA` with the reason and number defined; the individual defined values still appear. An all-undefined or selectively defined average is not a favorable result.

## Hand-verifiable synthetic acceptance examples

Everything in this section is **synthetic arithmetic**, not CASPER observations or benchmark performance. These cases specify expected behavior for future implementation tests; this document alone is not evidence that an executable metric implementation passes them. Toy eligibility masks test metric arithmetic in isolation; they do not instantiate CASPER's 1,528-record warmup or authorize a shorter production mask.

| Case | Synthetic input | Expected result |
|---|---|---|
| Threshold equality | Calibration scores `[1, 1, 2, 3]` | `m=4`, `k=4`, `tau=3`; scores 3 and 4 produce decisions 0 and 1 respectively |
| Quantile interior rank | Calibration scores integers 1 through 100 | `k=99`, `tau=99`; exactly score 100 exceeds threshold |
| Tied-score AP | Scores `[0.9, 0.9, 0.2]`, labels `[1, 0, 1]` | First tied group: precision `1/2`, recall `1/2`; final group precision `2/3`, recall 1; `AP=7/12`. Swapping tied rows changes nothing |
| No alarms, positives present | Labels `[1, 0]`, alarms `[0, 0]` | `TP=0, FP=0, FN=1, TN=1`; precision `NA`, recall 0, F1 0 |
| No positive labels, one alarm | Labels `[0, 0]`, alarms `[1, 0]` | Precision 0, recall `NA`, F1 0, AP `NA`; normal exceedance `1/2` |
| Neither positives nor alarms | Labels `[0, 0]`, alarms `[0, 0]` | Precision/recall/F1/AP all `NA`; normal exceedance 0 |
| Pre-existing episode | Times `[0, .05, .10, .15, .20]`; event rows `[2,4)`; alarms `[0,1,1,1,0]`; all eligible | One episode, not censored; event overlap hit at `.10`, overlap delay 0, pre-existing `true`, no fresh onset inside event. Full-slice exposure `.20 s` |
| Unknown between positives | Times `[0, .05, .10, .15, .20]`; alarms `[0,1,unknown,1,0]`; row 2 structurally excluded | Two observed episodes: first right-censored, second left-censored. Exposure includes only edges `0→1` and `3→4`: `.10 s`. Second episode is not a known fresh onset |
| Unexpected model missing score | Same unknown example, but row 2 is structurally eligible | Run fails comparative admission; coverage `4/5`; no primary F1/AP from the remaining four rows and no shared-mask shrinkage |
| Empty exposure | A reporting slice with one eligible alarm-positive endpoint | One observed episode, exposure zero, episode rate `NA`; retain censoring/boundary context |

Further future software checks must verify whole-episode continuity across reporting/event boundaries, all-eight event denominators, no final-label access in calibration/state updates, exact tied-score grouping, mask/score row identity, source-clock exposure and fail-closed missing-score admission. These definitions do not substitute for those tests or for a protected final-evaluation gate.
