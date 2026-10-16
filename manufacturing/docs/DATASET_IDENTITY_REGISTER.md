# CASPER release, labels, timestamps and file hashes

Manufacturing / Haiqa Mushtaq. Identification date: **16 October 2026**. This register identifies our actual local source files and the limits of their annotations and clocks. It is not a split manifest, processed dataset, reproduced experiment or proof that every paper used identical bytes.

## Exact collection

| Field | Identified value |
|---|---|
| Provider | Hakan Kayan, Kaggle |
| Listing | [Industrial Robotic Arm – Pick and Place Dataset](https://www.kaggle.com/datasets/hkayan/industrial-robotic-arm-anomaly-detection) |
| Dataset identifier | Kaggle ID **2888917**, `hkayan/industrial-robotic-arm-anomaly-detection` |
| Received provider version | **3** |
| Version creation timestamp | **2023-02-11T13:03:14.397Z** in the provider's version history; also its `lastUpdated` field |
| Provider version note | “Data Update 2023/02/11”; no detailed correction history established |
| Listed data license | **CC BY-SA 4.0**; separate from paper and software licenses |
| Access | Public unauthenticated download; no institutional approval was needed |
| Original receipt | 16 October 2026; archive received and hashed by **17:08:32 UTC** |
| Download route | Latest-version endpoint, bracketed by v3 metadata checks; not a claimed immutable version-specific download URL |
| Preserved payload | One archive and five extracted members; **10,723,331,182 bytes** combined |
| Local storage | `manufacturing/datasets/raw/casper/v3/`; originals read-only and excluded from Git |

A fresh metadata-only check still reports the same version, license and five-member inventory. The [baseline correspondence review](BASELINE_DATASET_CORRESPONDENCE.md) retains that check and distinguishes the newer **CASPER 1 & 2**, provider v2 dated 1 September 2024. The latter is a separate listing, includes additional recordings and has separate license metadata; it is not our acquired release. Equal filenames or advertised sizes do not establish equal bytes.

Primary provenance is the [original receipt](../datasets/manifests/casper_v3_receipt.json). The [consolidated identity manifest](../datasets/manifests/casper_v3_identity.json) links the separate integrity, label/clock, schema and source evidence. Later audits preserve the original receipt rather than rewriting what was known at acquisition.

## Exact local bytes

Member paths below are relative to `datasets/raw/casper/v3/original/` inside the manufacturing project. The archive is one directory above that. Hashes are **SHA-256 of complete received files**, not hashes of extracted text, parsed numbers or samples.

| File | Bytes | SHA-256 |
|---|---:|---|
| `original_casper_v3.zip` | 2,824,019,108 | `07f2daf948c8244c396c7b4d2fe4c475880a3a6577f982fc1738b5379b0e5409` |
| `dataset/arms.pcap` | 3,703,911,932 | `e58032aa4058375f865f3b19348fd56042b8a4f29dff92178ab54f11b07d1bb9` |
| `dataset/left_arm.csv` | 1,965,113,819 | `35552b683edcdd15be403f050c391979d1bc6f652908bbe5066323b79f9af777` |
| `dataset/nicla.csv` | 138,908,648 | `02653ba6d81cbfd1f47a1a71522f2c10a48fc9d8dee41e59d7df8d66608b5cd1` |
| `dataset/right_arm.csv` | 1,978,193,094 | `181662e25de09c1f4ed05e0877a65c40225752d6f54575ddb1cdf8a0cf29a334` |
| `nicla_fixed.csv` | 113,184,581 | `601fccb447f5c661ac5fe2885d5c38741aed979c58f6e9ce193768ad50ed4fe7` |

The original archive passed full decompression/CRC checks at receipt. A fresh whole-file pass on 16 October 2026 rehashed **all six files** and matched every original hash and size; raw files remain read-only and ignored, and the original receipt is unchanged. See the [separate integrity recheck](../datasets/manifests/casper_v3_integrity_recheck.json). These fingerprints freeze local identity; the inspected provider metadata does not publish an independent matching checksum. Agreement with our receipt demonstrates unchanged bytes, not authenticity of every measurement or correctness of labels.

A standard [checksum file](../datasets/manifests/casper_v3.sha256) is provided. From the **manufacturing directory**, its read-only verification command is:

```sh
shasum -a 256 -c datasets/manifests/casper_v3.sha256
```

The actual fresh verification command and observed outcomes are recorded separately in this task's integrity receipt. The standard command above is provided for future repeat checks; it is not a claim that an additional redundant verification was run.

## Label inventory

| File / convention | What is present | Interpretation and limits |
|---|---|---|
| `left_arm.csv` | `Anomaly State`: 1,417,048 zeros and 345,602 ones across 1,762,650 rows; eight contiguous positive runs | An application schedule flag. Matched later capture code attaches the same schedule to both arms; it does not establish that this arm itself received changed-speed commands. |
| `right_arm.csv` | Same binary counts and eight positive runs; positional labels exactly match left | Schedule flags support identifying documented changed-operation intervals. They are not independently measured physical-impact onset or evidence of malicious intent in each row. |
| Raw `nicla.csv` | Six startup records, then 1,751,682 nine-channel numeric rows; **no label column** | Do not copy controller labels by row index. Starts, rates and clocks differ. |
| `nicla_fixed.csv` | Nine named channels and 1,751,682 numeric rows; **no label column** | Same numeric sequence as raw Nicla after startup removal under the verified binary64 comparison. The name “fixed” does not mean labelled or synchronized. |
| Network capture | Container and packet timing metadata | No attack annotations established by this container-header audit. Packet contents and potential application fields were not decoded. |
| CASPER notebook annotation | Eight manually selected intervals after trimming/filtering IMU data | Retrospective source-code annotations, not an extra provider label file. A filtered endpoint is offset by 916 numeric rows from the raw coordinate. The final-end prose/code disagreement is six samples. |
| CatBoost source's IMU target | Acceleration-norm percentile creates positive labels during preprocessing | **Synthetic outlier targets**, not the provider's attack ground truth or CASPER's manual intervals. No such derivative was generated here. |

The [label/time audit](CASPER_LABEL_TIME_AUDIT.md) records the exact boundary convention and clock evidence. Detailed event indices, before/after records and losslessly preserved timestamp strings are in ignored local audit storage. All intervals use explicit zero-based half-open row ranges. Eight positive runs do not demonstrate eight independent experiments; label-zero recovery intervals are not automatically clean commissioning data.

The controller schedule, manually observed IMU changes and physical effect onset are different annotations. The later source's command target is the right arm while both files receive the schedule flag; its exact historical execution against these bytes remains unproven. Do not use the flag as per-arm attack localization truth without further evidence.

## Timestamp interpretation

Controller `Timestamp` is source-supported as **seconds since that controller started**, through matched capture code and official UR definitions. It is not UTC or a shared clock. The original executing capture revision/configuration and wall-clock anchors remain unresolved. The exact strings and boundary timestamps are preserved by the [label/time audit](CASPER_LABEL_TIME_AUDIT.md).

| Time field | First / minimum recorded value | Last / maximum recorded value | Interpretation |
|---|---|---|---|
| Left controller | `257250.83` | `345383.52999999997` | Original serialized strings; boot-relative seconds |
| Right controller | `257258.126` | `345390.626` | Original serialized strings; separate boot-relative seconds |
| Network capture | `2022-06-15T08:57:52.509154659Z` | `2022-06-16T09:26:45.327336274Z` | UTC representations of recorded epoch values; not a verified clock calibration |
| Either IMU file | Absent | Absent | Only row ordering is directly available |

The capture contains one little-endian PCAPNG v1.0 section and one interface with an explicit **10⁻⁹-second timestamp resolution**, and no offset option (format default: zero). All **14,582,826** packet blocks are timestamped Enhanced Packet Blocks, matching CASPER Table 11's packet count. In file order there are **2 adjacent duplicate timestamps and 2,579 backward steps**, with a largest backward step of **173,938 ns**. Timestamp resolution does not establish clock accuracy. A future loader must preserve original ordering and explicitly decide how to handle these reversals; this audit did not sort or rewrite the capture.

Container framing/file boundaries and retained packet lengths passed. This **does not establish lossless capture**: interface-statistics contents, packet checksums and traffic completeness were not evaluated. The parser interpreted only container headers and clock options using the [IETF PCAPNG Internet-Draft -05](https://www.ietf.org/archive/id/draft-ietf-opsawg-pcapng-05.html), not a published RFC. Packet protocols, addresses and payloads were not decoded. Five grouped **synthetic parser checks** passed; they are software checks, not benchmark results. Detailed profiles and synthetic fixtures remain in ignored local audit storage, with hashes in the integrity receipt.

- Left and right controllers have separately increasing clocks. Earlier complete scans found no duplicate/backward values; rounded deltas are predominantly 0.05, with five left and one right 0.1 intervals. The gap causes are unknown.
- Their same-row time offset varies from 7.096 to 7.346 under the supported seconds interpretation. Equal labels and row numbers do not synchronize the devices.
- Neither IMU file contains timestamps. **No exact per-observation time, calendar date, physical detection delay or false alarms per hour can be recovered simply by dividing row indices by 20.**
- Despite its `.pcap` suffix, `arms.pcap` is a **PCAPNG container**. Its packet-time interpretation must use the recorded section/interface options, not assume classic-PCAP encoding. Capture timestamps do not automatically synchronize the IMU or the controller boot clocks.

Provider release dates, ZIP member dates, host capture times, robot elapsed times and IMU row indices have separate meanings. A calendar representation of a recorded capture timestamp is not proof that the host clock was accurate or that a known local timezone was used.

## Connection to our three papers

| Candidate | Strongest available connection | Still not established |
|---|---|---|
| CASPER | Original listing and filenames; matching controller row count; our IMU length and code annotation pipeline agree with Figure 11's class totals | Published raw-file/checkpoint hashes. Table 11 gives 750 fewer IMU rows; annotation time alignment remains uncertain. |
| TWINE | Pinned loader requests `right_arm.csv`, and its feature expansion can be mapped to our schema | Paper-run file hashes/version and complete manuscript protocol; filename equality is not a byte match. |
| CatBoost on CASPER | Script reads original `nicla.csv`/`right_arm.csv`; reported metrics link to saved author summaries | Exact release and sampled row IDs; citation also points to successor listing and IMU labels differ from provider/controller labels. |

The [paper-specific correspondence record](BASELINE_DATASET_CORRESPONDENCE.md) supplies exact source revisions and evidence. **Our local source bytes are identifiable; identical bytes behind all three published experiments are not verified.** No paper's headline score is imported as a result for this release.

## Identification versus experiment admission

This stage establishes a concrete local release and explicitly records absent labels/timestamps. Missing IMU time is an observed absence, not a field to fabricate. The next stage needs a separately versioned annotation/feature/split contract, supported evaluation units, normal-only calibration and a disclosed reproduction designation. The [comparison protocol](COMPARISON_PROTOCOL.md) retains those gates. No train/test split, new attack annotation, model or experiment has been created by this identification task.
