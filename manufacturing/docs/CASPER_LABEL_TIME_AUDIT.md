# CASPER labels and timestamp audit

Manufacturing / Haiqa Mushtaq. Audited **16 October 2026**. This report identifies recorded labels, clocks and their limits for the received original CASPER v3 files. It is a data/source audit, not an experiment, new annotation set or approved split. Raw files were unchanged. No detector, upstream notebook, capture program, packet replay or cloud service was executed.

The key distinction is between **a scheduled controller flag**, **a manually annotated IMU interval** and **the instant a physical effect occurs**. These are different quantities in this collection. They must not be silently substituted for one another.

## Evidence and scope

The earlier complete CSV profiles establish record counts, label runs, monotonicity and positional correspondence. Their original hashes and timestamps remain preserved. This follow-up checked those profiles, the [full controller-schema audit](CASPER_SENSOR_SCHEMA.md), the [static annotation lineage](CASPER_ANNOTATION_LINEAGE.md) and the pinned author capture source. It then streamed both controller CSVs, parsing only **34 known boundary/endpoint records per file** to retain their timestamp strings and flags exactly. It did not parse full sensor vectors again or repeat full-file hashing; current byte-integrity verification is recorded separately by the parent dataset audit.

Detailed values and boundary metadata stay in ignored `local/casper_release_audit/label_time_review.json`. This includes each file's first/last/minimum/maximum timestamp, every positive run's first and last recorded timestamp, adjacent negative records and decimal elapsed differences. No sensor measurements are retained in that review JSON. The associated script and evidence hashes make the selection reproducible.

## File-level label and clock inventory

| File | Recorded data rows | Labels actually present | Timestamps actually present | Meaning / limit |
|---|---:|---|---|---|
| `dataset/left_arm.csv` | 1,762,650 | `Anomaly State`, binary 0/1 | `Timestamp`, numeric | Matched source supports a shared application schedule flag and this arm's own elapsed controller time. |
| `dataset/right_arm.csv` | 1,762,650 | `Anomaly State`, binary 0/1 | `Timestamp`, numeric | Same schedule annotation at every row index as the left file; this does not prove simultaneous physical samples. |
| `dataset/nicla.csv` | 1,751,682 after six startup records | **None** | **None** | Nine external IMU channels. Raw numerical row order is available; a measured time axis is not. |
| `nicla_fixed.csv` | 1,751,682 after its header | **None** | **None** | Same ordered numerical values under the recorded binary64 comparison; not a timestamp/label repair. |
| `dataset/arms.pcap` | Packet records not audited here | Not established | Not established by this task | Archive/member integrity is recorded elsewhere. Do not infer a usable synchronization clock or attack truth without a separately scoped passive packet audit. |

Both controller files have **1,417,048 zero-labelled rows** and **345,602 positive rows**, comprising eight contiguous positive runs. The first zero run contains 1,080,004 rows; the final zero run contains 34,643. The recorded positive runs contain 43,201 rows for events 1 and 8 and 43,200 for each of events 2–7. These are recording intervals, not eight independent physical experiments.

The earlier full scan found no missing/nonbinary label values and no invalid, duplicated or backward timestamps. `Safety Status` is a separate integer controller-state field; it must not be substituted for `Anomaly State` or interpreted as a cyberattack label.

## Controller time: what is now known

The matching [capture source](https://github.com/hkayann/Real-time-Anomaly-Detection-in-Industrial-Robotic-Arms-via-TinyML/blob/41b907749b7e5882319690a627a251e93fa99982/rtde/control_loop_connector_v1.py) writes `state_left.timestamp` and `state_right.timestamp` into the respective CSV columns (lines 244–257). Its field comment at line 96 and the [official UR RTDE definition](https://docs.universal-robots.com/tutorials/communication-protocol-tutorials/rtde-guide.html) support **seconds since that controller started**. This later source matches the received header/order, but its exact historical executing revision and configuration have not been established.

| Property | Left controller | Right controller |
|---|---:|---:|
| First-to-last recorded span, rounded to 0.001 s under the supported unit mapping | 88,132.700 s | 88,132.500 s |
| Prior full-audit steps rounded to six decimal places: 0.05 s | 1,762,644 | 1,762,648 |
| Prior full-audit steps rounded to six decimal places: 0.10 s | 5 | 1 |
| Invalid / duplicate / negative steps found in prior full audit | 0 / 0 / 0 | 0 / 0 / 0 |

These spans are about 24 hours 29 minutes; they are observed endpoint differences, not certified acquisition duration or a duration for the IMU. Timestamp strings sometimes contain long decimal tails from serialization. The review subtracts the original strings with `Decimal`, preserving those tails in ignored JSON. **Exact decimal arithmetic does not add clock precision.** Rounded summary values above do not replace the original strings.

Because the prior whole-file audit found strictly increasing timestamps, the verified first and last values are also the recorded minimum and maximum. This inference depends on the same received bytes; raw-file hash verification remains a separate check. The earlier profile stored parsed floating-point numbers, so the current exact endpoint strings were read from the original CSV rather than reconstructed from that profile.

Neither file supplies a controller boot-time calendar anchor or timezone. The clocks are not UTC, local wall time or the host clock. Both arms' same-index labels match, but their right-minus-left clock differences vary from 7.096 to 7.346 seconds under the source-supported mapping. Equal row indices therefore cannot be treated as a validated synchronous join. The gap causes are unresolved; a nominal 20 Hz setting does not justify inserting fabricated samples.

## What the controller labels annotate

Static source review gives the following order:

1. Record a host-clock starting value, then calculate `time.time() - initial_time` on each loop (lines 135–142).
2. Receive a right-arm state and a left-arm state (146–147).
3. Select a speed setting and flag from elapsed **host** time (164–230).
4. Attach the same `anomaly_state_sent` flag to both received state records (244–257).
5. Send subsequent motion parameters conditionally on robot waypoint/state checks (278 onward).

The schedule contains eight 2,160-second positive periods, starting after 54,000 host-elapsed seconds and alternating with normal settings. It encodes intended changes in the right-arm speed setting. **The flag is not an independent observation of when the commanded speed took effect.** It is attached to states received before the later conditional command sends. Latency, buffering, motion phase and the exact execution path are not recovered from the CSV alone.

A further source distinction matters: lines **78–88** keep every left-arm waypoint parameter at `arm_speed_default`, while lines **232–240** use scheduled `arm_speed_sent` in the right-arm parameters. Both CSVs nevertheless receive the same flag. Thus a positive left-file row cannot, from its label alone, be described as proof of a manipulated left-arm command or an observed left-arm physical anomaly. It marks the shared scheduled interval. Historical generation provenance remains incomplete, so this is supporting source evidence, not proof of the precise executing acquisition program.

The selected boundary checks confirm the recorded pattern **0 → 1 … 1 → 0** around all eight runs in each file. For each event the ignored JSON stores the previous negative, first positive, last positive and next negative timestamp. Their intervals bound a **recorded flag transition**, not physical attack onset/cessation. At thousandth-second reporting precision, the first-to-last-positive spans are 2,159.950–2,160.000 seconds; first-positive-to-next-record spans are 2,160.000–2,160.050 seconds. The different definitions and endpoint inclusivity must remain explicit.

## IMU labels are a separate annotation layer

The original and fixed IMU CSVs carry neither a timestamp nor an anomaly flag. The full prior correspondence check compared every numerical row after raw startup removal / fixed header removal and found **zero binary64 numerical mismatches**. Both canonical numerical streams have SHA-256 `83b8bd6702a32b3c033c1cb27cace44856759adaf1f3cb22e23d73d667e19a0b`. Every compared row differed in at least one textual field. This supports numerical correspondence under the specified representation, not identical source bytes, exact decimal-text equivalence, a new experiment, or undocumented provider processing history.

The [pinned CASPER notebook](https://github.com/hkayann/1D-CNN-Anomaly-Detection-via-CASPER/blob/bff03c91d155bf3134f6d801d3a4f4af7ea78adb/notebooks/casper.ipynb) manually marks eight changed-motion intervals after removing 897 numerical rows and applying a trailing width-20 median. The first 19 incomplete filter positions disappear. Therefore:

```text
filtered endpoint f -> raw numerical row f + 916
                   -> original CSV record f + 923 (one-based)
```

This is an index transformation, **not a clock conversion**. The filtered value depends on 20 raw observations, so its endpoint label is not automatically a label for all supporting inputs. The fixed file has the same numerical ordering after its header; it does not solve manual-label alignment or enable seconds-based delay measurement.

The eight source slices contain **342,740 positive filtered positions**, different from 345,602 controller positive records. Distinct sampling/order, transformations and manual boundaries mean these counts are not supposed to be made equal by padding or copying flags. Source-code endpoint 1,716,450 versus prose endpoint 1,716,456 remains a six-sample ambiguity. No boundary was edited or selected from detector scores. Detailed interval indices and uncertainties remain in the [annotation study](CASPER_ANNOTATION_LINEAGE.md) and ignored review JSON.

## Rules for the eventual loader and evaluation

- Preserve controller `Anomaly State` as **recorded schedule annotation** and exclude it from detector inputs. Preserve `Safety Status` separately; feature eligibility is a scientific decision, not an automatic schema inclusion.
- Preserve raw IMU ordering and record the chosen annotation layer/version. Do not manufacture timestamps with `row / 20`, copy controller labels by row number, or call `nicla_fixed.csv` prelabelled data.
- Do not equate label 0 with independently verified healthy, uncompromised operation. The initial scheduled-normal prefix is a candidate commissioning segment under the authors' assumptions; later zero-labelled recovery/gap periods require explicit treatment. Dataset labels alone do not prove absence of other disturbances or authorized changes.
- For controller-event evaluation, report whether an event means a scheduled command interval, measured deviation or some independently annotated physical effect. Detection delay relative to a schedule flag must be labelled as such, with synchronization limits; it is not automatically physical-effect detection delay.
- For untimestamped IMU evaluation, retain sample-index alignment and report clock limitations. Physical seconds, real-time latency and false alarms per hour need a justified time base. Eight ordinal correspondences do not provide one.
- Keep event and split manifests separate. Source comments naming training/validation/test phases are not our split approval, and no held-out attack labels may select thresholds or model variants.

## Reproducible review and limits

Executed from `/Users/matrixusman/CUI/DigitalTwin`:

```sh
python3 manufacturing/local/casper_release_audit/review_label_time.py
```

The ignored standard-library script records its hash, interpreter/platform, start/end timestamps, exact command and hashes of prior profiles, capture mapping/source, UR snapshots and schema manifest. It validates the source receipts; checks label-run arithmetic; verifies 34 timestamp/flag records per controller including all four boundary positions for eight events; and checks every manual-annotation endpoint translation by +916. It writes only its own review JSON. No feature values, new labels, fitted transforms, benchmark arrays or performance results were created.

Open issues: historical executing acquisition revision/configuration, wall-clock anchors, cross-device/IMU synchronization, independently measured physical onset, annotation uncertainty, final feature/split/target contracts and the paper's unexplained 750-row IMU table-count discrepancy. These limits persist after successful integrity and schema checks.
