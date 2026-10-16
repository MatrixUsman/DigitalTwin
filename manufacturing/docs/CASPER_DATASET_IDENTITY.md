# Original CASPER: received files and identity audit

**16 October 2026. Manufacturing / Haiqa Mushtaq.** The user authorized collecting the original CASPER files and identifying them before training. Acquisition and the bounded identity audit are complete. This report contains data provenance and structural checks, **not model results**. No environment, model, detector threshold, attack tool, simulator, or network capture replay was run.

**Later same-day follow-up:** the [full sensor-schema study](CASPER_SENSOR_SCHEMA.md) supersedes this report's bounded nested-field check and strengthens controller-clock interpretation to source-supported boot-relative seconds. The [annotation study](CASPER_ANNOTATION_LINEAGE.md) traces manual IMU labels and score support. Historical receipt/profile statements below are retained; cross-device timing and original capture execution remain unresolved.

**Subsequent release/clock pass:** use the [consolidated identity register](DATASET_IDENTITY_REGISTER.md) for fresh six-file hash verification, exact timestamp strings, PCAPNG header findings and the distinction between shared schedule flags and per-arm physical effects. This historical receipt report remains unchanged below; its original integrity-only capture coverage is superseded by the later header audit.

## Receipt and source

Source: [Hakan Kayan's original Industrial Robotic Arm — Pick and Place collection](https://www.kaggle.com/datasets/hkayan/industrial-robotic-arm-anomaly-detection), [provider metadata](https://www.kaggle.com/api/v1/datasets/view/hkayan/industrial-robotic-arm-anomaly-detection), and [provider file inventory](https://www.kaggle.com/api/v1/datasets/list/hkayan/industrial-robotic-arm-anomaly-detection). This is **not** the newer CASPER 1 & 2 listing.

- Provider revision: **version 3**, `2023-02-11T13:03:14.397Z`; provider title, revision, date, license and five-file inventory were rechecked before downloading.
- Listed data license: **[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)**. Retain attribution, version and modification notices; consult the license for any future sharing. This audit does not authorize publication or upload of dataset contents. Code licenses are separate.
- Access: public, unauthenticated Kaggle download; no institutional application, password or Kaggle token used. The working endpoint serves the latest revision; metadata checks before and after acquisition both resolved to version 3. A revision-specific archive URL is not asserted.
- Acquisition started `2026-10-16T17:04:49Z`; the archive was received and hashed by `17:08:32Z`; five-member integrity verification/extraction finished at `17:08:42Z` (UTC; local Asia/Karachi date remains 16 October).
- Compressed archive: **2,824,019,108 bytes**. Original member bytes: **7,899,312,074**. Combined preserved archive and extracted payload: **10,723,331,182 bytes** (about 10.72 GB decimal, excluding small audit artifacts).
- Local archive: `datasets/raw/casper/v3/original_casper_v3.zip`. Unmodified member bytes: `datasets/raw/casper/v3/original/`. Both are ignored by Git; originals were made read-only after verification. There are no symlinks to water or grid data.
- [Machine-readable receipt](../datasets/manifests/casper_v3_receipt.json) records source metadata hashes, exact bytes, SHA-256, ZIP CRC, timestamps, commands and audit references. Provider metadata and detailed profiles are retained in ignored `local/casper_v3_receipt/`. No transient signed redirect URL was retained.

The archive SHA-256 is `07f2daf948c8244c396c7b4d2fe4c475880a3a6577f982fc1738b5379b0e5409`. Provider metadata did not supply independent SHA-256 checksums. Our hashes freeze received bytes; passing CRC/decompression is an integrity check, not proof of accurate labels or published-result correspondence.

| Archive member | Received bytes | SHA-256 |
|---|---:|---|
| `dataset/arms.pcap` | 3,703,911,932 | `e58032aa4058375f865f3b19348fd56042b8a4f29dff92178ab54f11b07d1bb9` |
| `dataset/left_arm.csv` | 1,965,113,819 | `35552b683edcdd15be403f050c391979d1bc6f652908bbe5066323b79f9af777` |
| `dataset/nicla.csv` | 138,908,648 | `02653ba6d81cbfd1f47a1a71522f2c10a48fc9d8dee41e59d7df8d66608b5cd1` |
| `dataset/right_arm.csv` | 1,978,193,094 | `181662e25de09c1f4ed05e0877a65c40225752d6f54575ddb1cdf8a0cf29a334` |
| `nicla_fixed.csv` | 113,184,581 | `601fccb447f5c661ac5fe2885d5c38741aed979c58f6e9ce193768ad50ed4fe7` |

All five received sizes match the provider inventory. The extractor rejected unexpected/duplicate paths, traversal, symbolic links and encrypted members, then read every member to EOF to validate ZIP CRC while hashing. No network packet content was decoded or executed.

## Observed schemas, labels and clocks

These measurements come from complete streaming CSV scans. They are not detector performance, nor do they establish generalization to another robot or production run.

| File | Actual record structure | Observed annotation/clock facts |
|---|---|---|
| `left_arm.csv` | One header, **1,762,650 data rows**, 20 top-level CSV fields; all rows have the expected field count | `Anomaly State`: **1,417,048 zeros**, **345,602 ones**; eight contiguous positive runs. Strictly increasing numeric `Timestamp`; five steps round to 0.1 and 1,762,644 to 0.05 |
| `right_arm.csv` | One header, **1,762,650 data rows**, same 20-field header and consistent field counts | Same label counts and eight positive runs. Strictly increasing numeric `Timestamp`; one step rounds to 0.1 and 1,762,648 to 0.05 |
| Original `nicla.csv` | Six initial records with widths 1, 2, 9, 9, 9 and 11; then **1,751,682 rows of nine finite numeric values** | Nine motion-sensor channels; no embedded timestamp or anomaly label. The pinned author notebook explicitly skips those six startup records |
| `nicla_fixed.csv` | Header `AccX, AccY, AccZ, GyroX, GyroY, GyroZ, MagX, MagY, MagZ`; **1,751,682 numeric data rows** | No timestamp or anomaly label. Its numeric sequence is equivalent to the original's post-startup sequence under the audit's binary64 parsing, as detailed below |
| `arms.pcap` | Archive/member integrity and hash verified | Not decoded. Packet timestamps, network labels, endpoints and synchronization have not been audited |

The arm headers include `Timestamp`, `Anomaly State`, joint positions/velocities/currents, Cartesian coordinates, tool speed, generalized forces, joint temperatures/voltages, acceleration, elbow position/velocity, and scalar status/measurement fields. **Twenty CSV fields does not mean twenty scalar model inputs.** A bounded first-1,000-row right-arm check found eight six-element vector fields, three three-element vector fields and nine scalar fields. Excluding timestamp and label would yield 64 scalar values **if** that complete expansion and schema are validated across the full file; this is not a selected feature set. The whole-file audit parsed field widths, timestamp and label, but did not validate every nested vector or physical unit.

No malformed arm record widths, duplicate header names, invalid/duplicate/backward timestamps, blank records, or labels other than 0/1 were found. Timestamp deltas above are rounded to six decimals to avoid treating floating-point representation noise as separate intervals. Potential gaps are retained; no interpolation, resampling or repaired timeline was produced.

**Clock origin, units and timezone are not established by the received CSVs or the inspected acquisition documentation.** Store timestamps in their native units. A 0.05 step is consistent with the author's nominal 20 Hz description if units are seconds, but this audit does not convert the values into UTC/calendar time or claim verified end-to-end timing. First/last values and complete label-run boundaries are in ignored `schema_profile.json`.

Both arm files carry exactly the same label at every row index, but the right-minus-left timestamp difference takes six values from **7.096 to 7.346 native units**. Therefore equal row numbers and labels do not demonstrate simultaneous observations. Do not concatenate these as independent runs, synchronize by row index, or assign physical-time delay without a justified clock mapping. No explicit run/cycle/job identifier appears in the inspected header. Periodic pick-and-place motion is not itself an annotated cycle segmentation.

## What `nicla_fixed.csv` actually changes

A complete, positional comparison matched all **1,751,682** numeric rows after skipping the original's first six records and the fixed file's header. There were **zero row mismatches after parsing as IEEE-754 binary64**, while textual fields differed in every row. Canonicalizing each row to nine little-endian binary64 values gives the same SHA-256 for both sequences:

`83b8bd6702a32b3c033c1cb27cace44856759adaf1f3cb22e23d73d667e19a0b`

This establishes a measured numerical correspondence for these files, not their undocumented authoring history or exact decimal equivalence beyond the chosen numeric representation. The fixed file adds a header and changes serialization; **it supplies no clock alignment, labels, filtered series or separate experiment**. Keep both original byte hashes. A future loader can exploit the established correspondence only through a documented derivative manifest, without pretending its bytes match raw `nicla.csv`.

## Label provenance and the comparison limit

The provider describes deliberately increasing/decreasing joint velocity around a normal setting. This supports a controlled motion-deviation detection task; the flag alone does not distinguish malicious intent, authorized speed change, physical consequences or recovery. Label-zero intervals after an intervention are not automatically pristine commissioning data.

The [original author notebook at revision `bff03c91d155bf3134f6d801d3a4f4af7ea78adb`](https://github.com/hkayann/1D-CNN-Anomaly-Detection-via-CASPER/blob/bff03c91d155bf3134f6d801d3a4f4af7ea78adb/notebooks/casper.ipynb), zero-based cells 1–25, explains mismatched acquisition rates and manual IMU annotation. It skips six startup records, trims 897 observations, applies a trailing rolling median of width 20, then assigns eight manually identified intervals. The notebook's claimed annotation accuracy was not independently established. The local copy and its SHA-256 are linked from the receipt; it was read as JSON, not executed.

Separate this retrospective label preparation from model training and calibration. Do not reconstruct labels by maximizing detector performance or silently transfer arm flags to IMU row numbers. A fixed published annotation can support a disclosed reproduction analysis, but cannot establish exact physical event onset or trustworthy detection delay without independent timing evidence. No new anomaly boundary was inferred from sensor plots in this audit.

The arm records contain an initial **1,080,004 label-zero rows**, followed by eight positive runs interspersed with zero-labelled periods; the final positive run ends at exclusive row **1,728,007**. These are inventory facts, not an approved split or a partition optimized around test performance. The original notebook truncates controller data to 1,728,000 rows, so that choice is not equivalent to preserving this full release. Full interval boundaries remain in ignored audit storage to support later controlled annotation work. No model scores or signal-dependent split choices were examined.

## Executed commands and remaining work

Working directory: repository root `/Users/matrixusman/CUI/DigitalTwin`.

```sh
python3 manufacturing/scripts/acquire_casper_v3.py
python3 manufacturing/scripts/profile_casper_v3.py
python3 manufacturing/scripts/inspect_casper_alignment.py
```

These standard-library utilities are [acquisition/integrity](../scripts/acquire_casper_v3.py), [streaming schema profile](../scripts/profile_casper_v3.py), and [file/clock correspondence](../scripts/inspect_casper_alignment.py). Network access was approved for public metadata/archive/notebook retrieval. No packages were installed. The schema profiler was refined after identifying the fixed file's first record as a header, then rerun; the final profile distinguishes this header from malformed numeric data. These are audit utilities, not the benchmark loader or a validated model pipeline.

Completed: original release receipt, immutable payload preservation, complete archive integrity and hashes, all-file CSV structural inventory, binary label counts/runs, native-clock checks, and original/fixed IMU numerical correspondence.

Still required before training:

1. Match each paper's actual inputs and label generation to these frozen bytes; author filenames alone are insufficient. Preserve exact-code, modified-protocol and independent-reimplementation distinctions.
2. Resolve clock origin/unit documentation and IMU annotation uncertainty. Confirm whether honest event/delay evaluation is feasible; otherwise limit claims to the supported row/sample units and clearly disclosed annotations.
3. Define trusted observations and separate controller-only and external-IMU comparisons. Exclude labels, timestamps as shortcuts and unavailable future context from detector inputs.
4. Freeze development/calibration/final evaluation roles, boundaries and purge rules before window construction. This apparent continuous collection is not evidence of independent cross-run replication.
5. Validate the eventual loader, full vector schema, preprocessing, alignment and metrics with labelled synthetic tests and bounded real-data checks. No split files, fitted transforms, features, training outputs or benchmark results have been produced.
