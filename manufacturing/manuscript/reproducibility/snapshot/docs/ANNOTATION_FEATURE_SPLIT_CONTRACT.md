# CASPER right-arm annotation, feature and chronological split contract

Manufacturing / Haiqa Mushtaq. **Version 0.1, 16 October 2026 — frozen for design review; not admitted for execution.** This document defines a normal-only comparison using the original CASPER v3 right-arm controller recording. It does not select a final architecture, approve training or claim that a twin has been validated.

The authoritative machine-readable companion is [casper_right_arm_contract_v0.1.json](../configs/casper_right_arm_contract_v0.1.json). Exact input identity comes from the [release register](DATASET_IDENTITY_REGISTER.md), label interpretation from the [label/time audit](CASPER_LABEL_TIME_AUDIT.md), and field semantics from the [controller schema](CASPER_SENSOR_SCHEMA.md). This is a new **normal-only controller group**. It must not be confused with the earlier external-IMU group or supervised controller group in the [comparison protocol](COMPARISON_PROTOCOL.md).

## One source, one arm and one annotation convention

Use only `datasets/raw/casper/v3/original/dataset/right_arm.csv`: **1,762,650 data rows**, excluding the header; **1,978,193,094 bytes**; SHA-256 `181662e25de09c1f4ed05e0877a65c40225752d6f54575ddb1cdf8a0cf29a334`. The [received-byte identity manifest](../datasets/manifests/casper_v3_identity.json) links this file to original CASPER provider v3 and the previously verified archive. No left-arm, IMU, network or successor-collection observations enter this comparison.

Every range below is **zero-based, half-open**: `[start, end)` includes the first row and excludes `end`. A data row's one-based CSV record number is `row + 2`, because record 1 is the header. Row numbers are provenance and evaluator coordinates, never detector features.

The target is the file's literal `Anomaly State`: `1` means the recorded application schedule is in a changed-speed interval; `0` means the schedule is outside those intervals. Preserve the target name `recorded-controller-schedule-v0.1`. It is not independently measured physical-effect onset, malicious-intent ground truth, or a fault-versus-attack classification. Both arms received the schedule flag, but the matched later command source varies right-arm speed; this is why the right arm is selected. Historical executing-source provenance remains incomplete.

| Event | Positive data-row range | Positive rows | First-positive timestamp string | Last-positive timestamp string |
|---|---|---:|---|---|
| 1 | `[1080004, 1123205)` | 43,201 | `311258.376` | `313418.376` |
| 2 | `[1166405, 1209605)` | 43,200 | `315578.426` | `317738.376` |
| 3 | `[1252805, 1296005)` | 43,200 | `319898.426` | `322058.376` |
| 4 | `[1339205, 1382405)` | 43,200 | `324218.426` | `326378.376` |
| 5 | `[1425606, 1468806)` | 43,200 | `328538.47599999997` | `330698.426` |
| 6 | `[1512006, 1555206)` | 43,200 | `332858.47599999997` | `335018.426` |
| 7 | `[1598406, 1641606)` | 43,200 | `337178.47599999997` | `339338.426` |
| 8 | `[1684806, 1728007)` | 43,201 | `341498.47599999997` | `343658.47599999997` |

The positive total is **345,602 rows**. The JSON preserves all 17 alternating schedule runs and each event's preceding, first, last and following record. Exact serialized strings preserve source values; their long decimal tails do not establish clock precision. No new labels were inferred from sensor values or detector outputs.

The initial zero-flag prefix is `[0, 1080004)`. Treating it as commissioning data is an explicit assumption inherited from the study design, not proof that every observation was uncompromised. Every later zero-flag interval is **recovery/inter-event scheduled-zero**, including the final `[1728007, 1762650)` tail. Retain these intervals in evaluation and report them separately; never move them into training, model selection or calibration.

## Permitted observations

| Role | Exact source column | Permitted values | Unit and use |
|---|---|---|---|
| Joint position | `Actual Joint Positions` | Six vector elements, indices 0–5 | Radians under the source-supported UR mapping |
| Joint velocity | `Actual Joint Velocities` | Six vector elements, indices 0–5 | Radians/second under the same mapping |
| Time context | `Timestamp` | Current minus preceding timestamp within one continuous segment | Controller elapsed seconds; state propagation and gap detection only |

There are **12 observation channels**, plus relative time context. Joint order is base, shoulder, elbow, wrist 1, wrist 2 and wrist 3 under the mapped UR convention. A physical-state prediction must be formed before consuming the state it predicts. At arrival, relative time may advance the predicted state; compare the arriving joint measurements with that prediction, score, then synchronize the observer. A simpler comparator may score the arriving measurements directly, but receives no extra information.

Exclude every other source column, including `Anomaly State`, `Safety Status`, `Execution Time`, currents, temperatures, forces, Cartesian fields and acceleration. Also exclude absolute time, row index, event IDs, schedule boundaries, command targets, speed-scaling signals, label derivatives and future summaries. Do not introduce authenticated commands, observed task-phase IDs or a timestamp-aligned IMU reference: these are not established inputs. Phase may be an internal estimate derived causally from permitted observations; it is not supplied ground truth. Observed velocity must not silently redefine the reference's nominal authorized progression; doing so would remove the distinction this study tests.

This information-access group **assumes** the received joint measurements and elapsed clock remain uncompromised while command speed is manipulated. The dataset does not establish their authentication. An identical authorized speed change would be observationally indistinguishable without additional trusted policy context.

## Exact chronological partitions

Use the initial prefix length `N = 1080004`. Compute cumulative boundaries with integer arithmetic: `floor(N × p / 100)` for `p = 0, 50, 65, 80, 100`. Do not randomize or stratify rows.

| Partition | Data-row range | Raw rows | First timestamp string | Last timestamp string | Permitted use |
|---|---|---:|---|---|---|
| Training | `[0, 540002)` | 540,002 | `257258.126` | `284258.22599999997` | Fit transforms and model/reference parameters |
| Normal development | `[540002, 702002)` | 162,000 | `284258.276` | `292358.22599999997` | Select configurations/checkpoints by a predeclared normal-only objective |
| Normal calibration | `[702002, 864003)` | 162,001 | `292358.276` | `300458.276` | Fit the alarm threshold after model selection |
| Held-out normal | `[864003, 1080004)` | 216,001 | `300458.326` | `311258.326` | Final normal alarm/coverage evaluation only |

The **final replay is continuous `[864003, 1762650)`**. Its initial held-out-normal portion establishes online state before the first event; the replay then continues through every scheduled positive and recovery interval. The normal reporting slice and mixed reporting slice are evaluator views of the same run. **Do not reset at the first positive flag, later event boundaries, or returns to zero.** The model receives neither labels nor those boundaries.

Reset dynamic state and trailing buffers at the start of training, development, calibration and final replay. Training-fitted parameters carry forward; an online state from a preceding partition does not. A recurrent state may use all earlier allowed observations within its own segment. Split before filtering, window creation, feature selection or parameter fitting. No centered smoothing, future interpolation or cross-partition context is permitted.

These are contiguous portions of one acquisition, not independent robot runs or verified cycle-group partitions. No cycle ID is fabricated, and partition boundaries have not been chosen from detector performance.

## Gaps, initialization and score coverage

A stream breaks when `Δt <= 0` or `Δt > 0.075 seconds`. The threshold is a declared rule between the observed nominal 0.05-second steps and the observed 0.1-second step; it does not diagnose why a sample is absent. Mark the intervening duration unknown, retain both original records, reset dynamic state/buffers at the next record and restart warmup. Do not fill samples. Invalid/nonfinite joint values likewise become unscored unknowns and break continuity; the received full schema audit found none.

A timestamp-only pass located the sole right-arm gap between rows **16570 and 16571**, `258086.626` → `258086.726`, a **0.100-second** step. It lies inside training. No further gap under this rule occurs in development, calibration or final replay. This scan parsed timestamp scalars throughout the file and only selected boundary flags; it did not parse sensor vectors or generate model arrays.

Declare a **provisional common warmup floor of 1,528 preceding observations**. This is motivated by the already audited CASPER pipeline's 1,529-observation score support; it is not a chosen window size for our new models and does not make a controller adaptation a faithful CASPER reproduction. An endpoint at segment start plus 1,528 is the first potentially score-eligible position under this floor.

| Continuous stream | Initial unscored rows | First potentially eligible endpoint |
|---|---|---:|
| Training before gap | `[0, 1528)` | 1,528 |
| Training after gap | `[16571, 18099)` | 18,099 |
| Development | `[540002, 541530)` | 541,530 |
| Calibration | `[702002, 703530)` | 703,530 |
| Final replay | `[864003, 865531)` | 865,531 |

Warmup observations can initialize permitted causal state. They are excluded from scored endpoints; individual training-loss eligibility must follow the later model specification. **1,529 is not a bound on recurrent state history.** A stateful twin may retain information throughout its continuous partition segment. Exact model-specific initialization, filter support, history windows, score aggregation and handling of uncertainty remain execution gates. If a model needs longer initialization, revise the common rule before looking at final attacks. All excluded rows and unscored events must remain visible.

## Preprocessing, selection and calibration

Fit scaling and any permitted feature transformation using training rows only. Development may choose among a finite, recorded set of configurations using normal prediction or reconstruction behavior; the objective and tie rule must be specified before a pilot. Calibration is reserved for the threshold after those choices. No imputation, additional channel, hidden attack-labelled validation or adaptation policy is implicitly approved here.

Keep model/reference parameters, residual calibration and alarm thresholds fixed during final replay. Updating causal state after scoring is permitted; online parameter fitting, threshold adaptation and use of true labels are not. A future adaptation study requires a separate contract.

At the single declared operating point, larger scores mean more anomalous. For `m > 0` eligible normal-calibration scores, sort ascending and use the one-based nearest rank `ceil(0.99 × m)`. The selected score is the threshold; alarm only when `score > threshold`. Equality does not alarm. If no eligible calibration scores exist, evaluation is blocked. This produces an empirical calibration operating point, not a guarantee of a 1% future false-alarm rate.

## Evaluation semantics

The primary experimental contrast is the **progression-aware twin versus its otherwise matched progression-omitted variant**. A simple joint-velocity deviation detector and normal-trajectory template are mandatory controls; an ordinary causal predictor should be specified before the pilot. All receive the same eligible information and normal-only development/calibration access. Do not choose a preferred variant, composite metric or operating point after inspecting attacks.

Primary results are reported jointly: **unadjusted point precision, recall and F1 on eligible mixed-slice endpoints**, **held-out-normal point exceedance**, **held-out-normal alarm episodes and episodes per verified eligible hour**, and **score coverage in both slices**. The point-metric population is exactly the scheduled-change/recovery slice **`[1080004, 1762650)`**, not that slice pooled with earlier held-out-normal observations. Report TP, FP, FN, TN, eligible endpoint counts and all unknown/excluded counts. Different class prevalence or discarded endpoints must not be hidden inside a headline score.

Use the shared structural eligibility mask determined by the common warmup, gaps and invalid-input policy. Any method-specific missing scores remain visible and must not silently remove endpoints for other methods. A head-to-head claim requires comparable coverage or a missing-score policy declared before final scoring; this remains an execution gate. No detector outcomes have been generated to select such a policy.

Event recall and delay remain **mandatory secondary analyses**. The eight positive intervals are long enough that a single alarm per interval is a weak measure on its own. All eight form the event denominator. A detected event has at least one eligible threshold-positive endpoint inside its row range. An event with no alarm is missed; an event with no eligible score is also counted as missed and identified as a coverage failure. Do not remove difficult or unscored events after seeing results.

For an interval containing an alarm, report the first eligible alarm timestamp inside the interval minus its first-positive-flag timestamp in controller seconds. Name this **schedule-relative interval-overlap delay**. If an alarm was already active before the interval, flag it as **pre-existing**: its continued overlap can give delay zero but is not a fresh detection onset. Separately report the first new eligible negative-to-positive alarm transition inside each interval and its schedule-relative delay, or `no_new_onset`. An unknown preceding state does not establish a new transition. Do not reset episodes at event or reporting-slice boundaries to manufacture onsets.

Neither delay is physical-effect onset latency, acquisition/transport latency or a precise cross-device delay. Missed intervals retain a null overlap delay and appear alongside intervals containing alarms. No independently validated onset-uncertainty duration is available; do not invent a grace period or label shift.

Average precision is a supporting output on the same eligible mixed-slice endpoints. No majority-window target, point adjustment or hindsight threshold optimization is allowed in the main comparison. Mixed-trace confusion counts measure agreement with the recorded schedule; they do not prove a scientific attack/healthy distinction. Report recovery/inter-event scheduled-zero behavior separately from the held-out-normal block. If a full-replay point summary is later added, label its different population explicitly and do not substitute it for the declared primary slice.

An observed alarm episode is a contiguous sequence of eligible positive endpoint decisions within one continuous segment. An unknown/unscored observation or gap ends an observed segment, not necessarily the underlying alarm condition. A positive first eligible endpoint after warmup, a gap or an unknown has an unknown prior onset: count the observed episode and mark it **left-censored**, not a known fresh onset. A positive episode reaching stream end, a gap or an unknown is likewise right-censored. Labels and reporting-slice boundaries never reset episodes. Do not add test-selected smoothing, persistence or cooldown.

For held-out-normal exposure, sum elapsed intervals only between adjacent eligible endpoints both in that reporting block and continuous segment. Exclude warmup, gaps, unknown intervals and boundary-crossing durations; never extrapolate duration after the last observation. Count each observed episode with at least one eligible positive endpoint in the held-out-normal block once, including censored episodes with their flags, and divide by verified eligible hours. Name the result **observed alarm episodes per eligible hour**, not an incident-arrival rate. Report the numerator, denominator and censoring counts. If exposure is zero, report `NA`. Other undefined metrics likewise remain `NA` with their counts.

Do not construct confidence intervals or significance claims by pretending correlated rows are independent experiments. The eight scheduled intervals occur in one acquisition. Repeated model seeds would measure computational variation, not independent robot replication.

## Evidence, execution record and remaining gates

The ignored [boundary/gap receipt](../local/right_arm_contract_review/boundary_and_gap_receipt.json) preserves 40 selected records, exact strings, the observed gap, source-evidence hashes, interpreter/platform, working directory, command, script hash and repository state. All 32 event-boundary records matched the earlier audit. The raw file's size, modification time and read-only mode were unchanged; the six source-evidence files were unchanged. This task relied on the earlier full-file integrity audit rather than repeating a two-gigabyte hash.

Commands from `/Users/matrixusman/CUI/DigitalTwin`:

```sh
python3 manufacturing/local/right_arm_contract_review/build_contract.py
python3 manufacturing/local/right_arm_contract_review/validate_contract.py
```

The builder performs metadata extraction and writes the contract/receipt. The validator checks the metadata contract without model execution. Preserve their outputs before any rerun; the ignored scripts and validation receipt carry their own hashes. No dataset arrays, fitted transforms, scores, model, raw-file changes or benchmark results were produced.

Before execution admission: settle model-specific initialization and histories; save the normal-only selection rule/configurations; resolve independent-implementation and code-use designations; validate a future loader, hidden-label boundary, metric definitions and stream resets with clearly labelled synthetic fixtures; and prepare an isolated environment and bounded pilot plan. The original CASPER detector uses IMU, while TWINE and CatBoost use different supervision/protocols. This contract does not turn them into an already fair three-paper comparison.
