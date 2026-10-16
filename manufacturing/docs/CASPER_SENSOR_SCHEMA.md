# CASPER controller schema and clock interpretation

**Manufacturing / Haiqa Mushtaq — 16 October 2026.** This extends the [received-file identity audit](CASPER_DATASET_IDENTITY.md). The original acquisition receipt, raw bytes and prior executed audit scripts are unchanged. The task was a deeper data study before training, not a model experiment.

## What the complete scan established

Both received controller CSVs were parsed from beginning to end, including every nested numeric vector. Each has **1,762,650 rows** and the same 20-field header. Across both files, the scan validated **3,525,300 rows and 232,669,800 scalar numeric values**, counting timestamps and labels. It found:

- No unexpected top-level field count, nested vector length, empty field, parse error, nonnumeric vector element or nonfinite value (`NaN`/infinity).
- Eight vectors of length six, three vectors of length three, and nine scalar fields in **every row** of both files.
- Integer-valued `Safety Status` and `Anomaly State` throughout. The earlier annotation audit separately established labels 0/1 and eight positive intervals.
- Both SHA-256 digests still exactly match the original receipt. Hashing occurred while streaming the bytes being parsed; nothing was rewritten.

There are **66 scalar values per row**, including time and label. Excluding those leaves **64 possible observables**, not an approved model input set. `Safety Status`, for example, has discrete semantics; treating it as an arbitrary continuous measurement needs justification. No signal ranges, anomaly plots, model scores, correlations or feature rankings were computed.

The prior report's first-1,000-row shape observation is now strengthened to a full two-file shape/numeric check. This verifies syntactic numeric usability, **not physical calibration, authenticity, absence of corrupted measurements or benchmark fairness**.

## Controller data dictionary

The source-field mapping below is obtained by static inspection of the author's [RTDE capture file, pinned revision `41b907749b7e5882319690a627a251e93fa99982`](https://github.com/hkayann/Real-time-Anomaly-Detection-in-Industrial-Robotic-Arms-via-TinyML/blob/41b907749b7e5882319690a627a251e93fa99982/rtde/control_loop_connector_v1.py). Its `field_names` list at line 122 and both `writerow` calls at lines 244 and 252 exactly match our received header/order. An AST-only check confirms that mapping; no capture code was imported or executed.

The file is in a later author repository and writes `state_right_v3.csv`/`state_left_v3.csv`, rather than the provider's published names. **We have not established the exact executing commit, software version, RTDE recipe or configuration that generated the downloaded v3 bytes.** The mapping is strong source evidence, not a completed generation provenance chain.

Units marked “unresolved here” were not independently established for this data release. Do not silently fill them from generic engineering assumptions or use them in a physical constraint until verified.

| Received column | Values per row | Author source field | Interpretation / supported units |
|---|---:|---|---|
| `Timestamp` | 1 | `timestamp` | Controller elapsed time; seconds supported by source mapping and UR documentation; see clock limits below |
| `Actual Joint Positions` | 6 | `actual_q` | Joint angles; radians under the mapped UR convention |
| `Actual Joint Velocities` | 6 | `actual_qd` | Joint angular velocities; rad/s under the mapped UR convention |
| `Actual Joint Currents` | 6 | `actual_current` | Measured joint currents; units unresolved here |
| `Actual Cartesian Coordinates` | 6 | `actual_TCP_pose` | Tool translation plus rotation-vector orientation; release-specific units/frame validation pending |
| `Actual Tool Speed` | 6 | `actual_TCP_speed` | Three translational components in m/s, three angular components in rad/s under RTDE definition |
| `Generalized Forces` | 6 | `actual_TCP_force` | TCP wrench; coordinate frame and units require further validation |
| `Temperature of Each Joint` | 6 | `joint_temperatures` | Joint temperatures; °C |
| `Execution Time` | 1 | `actual_execution_time` | Controller thread timing; ms in current UR documentation, not detector latency |
| `Safety Status` | 1 | `safety_status` | Integer safety-state code; not an attack label |
| `Tool Acceleration` | 3 | `actual_tool_accelerometer` | Tool accelerometer channels; units/frame unresolved here |
| `Norm of Cartesion Linear Momentum` | 1 | `actual_momentum` | Scalar momentum-related quantity; preserve the original misspelled header; units unresolved here |
| `Robot Current` | 1 | `actual_robot_current` | Robot current; units unresolved here |
| `Joint Voltages` | 6 | `actual_joint_voltage` | Joint voltages; V under RTDE definition |
| `Elbow Position` | 3 | `elbow_position` | Elbow position in robot base coordinates; release-specific unit validation pending |
| `Elbow Velocity` | 3 | `elbow_velocity` | Elbow velocity in robot base coordinates; release-specific unit validation pending |
| `Tool Current` | 1 | `tool_output_current` | Tool current; mA in the author's capture-file comment |
| `Tool Temperature` | 1 | `tool_temperature` | Tool temperature; °C under RTDE definition |
| `TCP Force` | 1 | `tcp_force_scalar` | Scalar force; N in the author's capture-file comment; distinct from the six-component wrench |
| `Anomaly State` | 1 | `anomaly_state_sent` | Application-generated 0/1 schedule flag; evaluation annotation, excluded from model features |

Official interpretation sources: [UR RTDE guide](https://docs.universal-robots.com/tutorials/communication-protocol-tutorials/rtde-guide.html), [joint-angle definition](https://www.universal-robots.com/manuals/EN/HTML/SW5_25_1/Content/prod-scriptmanual/all_scripts/get_actual_joint_positio.htm), and [joint-velocity definition](https://www.universal-robots.com/manuals/EN/HTML/SW10_15/Content/prod-scriptmanual/all_scripts/get_actual_joint_speeds.htm). Joint order under the documented UR convention is base, shoulder, elbow and three wrist joints; do not equate these six indices with Cartesian axes. Current documentation defines a field, but does not certify a historical sensor's calibration or acquisition configuration. The two scalar “force”/“momentum” fields should not be combined with vector wrench channels merely because their names seem related.

The nine-channel external Nicla schema is already validated in the [identity report](CASPER_DATASET_IDENTITY.md): acceleration, gyroscope and magnetometer axes. Its raw and fixed files contain no timestamps or labels. This controller audit does not resolve IMU scaling, orientation estimation, mounting frame, label alignment or trustworthiness.

## Clock meaning: strengthened evidence, remaining limits

The capture source maps each CSV `Timestamp` directly from that arm's `state.timestamp`; its comment identifies elapsed time since controller startup. The [official RTDE definition](https://docs.universal-robots.com/tutorials/communication-protocol-tutorials/rtde-guide.html) supplies the unit, seconds. The companion [connector](https://github.com/hkayann/Real-time-Anomaly-Detection-in-Industrial-Robotic-Arms-via-TinyML/blob/41b907749b7e5882319690a627a251e93fa99982/rtde/connector.py) defaults to 20 Hz and passes the frequency to RTDE output setup.

**Updated interpretation:** boot-relative controller seconds are now source-supported for the matched field; use that explicit source mapping when documenting within-controller elapsed time. The earlier receipt's “units unverified” entry records the evidence available at acquisition and has deliberately not been rewritten. The original executing capture revision remains unresolved, so call this a source-supported interpretation, not experimentally verified synchronization.

Consequences:

1. A controller timestamp is **not UTC**, a calendar date, or the host PC's clock. No boot-time anchor, host-time alignment or synchronization log was acquired; there is no justified conversion to wall-clock time.
2. Two arms have separate clocks. Their equal row numbers and identical annotation flags do not prove simultaneous measurements. The prior observed right-minus-left offset varies from 7.096 to 7.346; under the mapped unit these are seconds.
3. The measured 0.05 intervals are consistent with 20 Hz under that mapping. Retain the five left-arm and one right-arm 0.1 intervals as gap evidence. Their causes—sampling, transport, skipped messages or another acquisition effect—were not identified. UR documents that output messages can be skipped; that possibility is not a diagnosis of these specific gaps.
4. Knowing a controller field's unit does **not** establish a Nicla clock or exact physical-effect onset. Do not promote this improvement in field semantics into a validated cross-modal detection-delay claim.

## What the capture code says about labels

The source computes elapsed **host** time using `time.time()` (lines 135–142), then receives right/left controller states (146–147). A timed schedule selects `anomaly_state_sent` (164–230); both CSV writer calls attach that same flag to their respective received states. This is consistent with the observed complete positional equality of arm labels.

This source observation indicates an application schedule annotation rather than an independent sensor-confirmed instant of physical impact. Host time is calculated before the two receive calls, and controller timestamps come from the robots. Their latency and offset cannot be reconstructed precisely from these CSVs alone. The paper itself discusses synchronization limitations in Section 6.6 of the [corrected CASPER manuscript](../baselines/casper/artifacts/casper_corrected_vor_v1.1.pdf).

The code comments describe intended train/validation/test durations, but those comments are **not our split approval**. All future partitions must follow the [comparison protocol](COMPARISON_PROTOCOL.md), with test attacks excluded from tuning. We did not rerun the controller or infer label changes from measured attack responses.

## Audit artifacts and checks

Executed from repository root:

```sh
python3 manufacturing/scripts/audit_casper_controller_schema.py
```

The [new standard-library utility](../scripts/audit_casper_controller_schema.py) streamed the two files sequentially. Left-arm validation took approximately **45.37 seconds**, right-arm **45.97 seconds**; these are local data-audit timings, **not model runtime measurements**. No environment or dependency installation was required.

The new [audit manifest](../datasets/manifests/casper_controller_schema_audit.json) records the input receipt hash, unchanged raw hashes, script hash, timestamps, interpreter/platform, output profile hash and pinned source/doc snapshots. Detailed profiles, exact source mappings and documentation snapshots remain ignored under `local/casper_controller_schema_audit/`. No raw sensor payload, network endpoint or packet content is included in tracked artifacts.

Checks passed: all expected rows and nested dimensions, numerical types/finiteness, source-header/order correspondence, received-byte hashes, and integer-valued state/label fields. This audit did not validate signal realism, exact label delay, physical calibration, independent run count, process dynamics, data permission for redistribution, or the eventual benchmark loader.

Next bounded data task: resolve the annotation/feature manifest and clock-assumption policy for the selected information-access group. Keep the lack of an IMU clock and historical capture configuration explicit. Select features for scientific/availability reasons before examining held-out detector outcomes.
