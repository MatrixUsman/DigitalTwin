# Manufacturing baselines: dataset release and byte correspondence

Audited **16 October 2026**, manufacturing / Haiqa Mushtaq. Scope: independent comparison of preserved provider receipts, manuscript/code evidence and four fresh public metadata responses. No dataset body was downloaded, no author code was executed, and no model, preprocessing output or benchmark result was produced in this task.

**We have identified and hashed our original CASPER v3 files. We have not established that all three papers used those exact bytes, annotations or inputs.** CASPER has the strongest numerical bookkeeping match; TWINE explicitly links the original listing but uses different observations; CatBoost's references point to the successor listing while its code uses filenames appearing in both. None of these evidence levels should be upgraded to an exact published-run match.

## Two provider listings, separately dated

Public provider metadata was re-read between **18:05:41 and 18:05:44 UTC on 16 October 2026**, without an account or credentials. Version, date, license and size below are provider fields observed at that time; this does not reconstruct historical license text for every earlier revision.

| Property | Original pick-and-place collection | CASPER 1 & 2 collection |
|---|---|---|
| Author listing | [Industrial Robotic Arm — Pick and Place](https://www.kaggle.com/datasets/hkayan/industrial-robotic-arm-anomaly-detection) | [Industrial Robotic Arm — IMU Data (CASPER 1 & 2)](https://www.kaggle.com/datasets/hkayan/industrial-robotic-arm-imu-data-casper-1-and-2) |
| Provider slug | `hkayan/industrial-robotic-arm-anomaly-detection` | `hkayan/industrial-robotic-arm-imu-data-casper-1-and-2` |
| Current version / timestamp | **3**, `2023-02-11T13:03:14.397Z` | **2**, `2024-09-01T09:55:44.95Z` |
| Earlier provider versions | v1 `2023-02-11T10:09:26.063Z`; v2 `2023-02-11T12:34:58.703Z` | v1 `2024-02-16T18:13:45.32Z` |
| License field at this check | **CC BY-SA 4.0** | **MIT** |
| Inventory | Five members, **7,899,312,074 bytes** uncompressed | Fourteen CSVs, **3,065,646,348 bytes** uncompressed |
| Local acquisition status | Original v3 archive and five unmodified members received previously | No archive/member bytes received in this audit; metadata only |
| Provider member digests | None exposed in the inspected `view`/`list` JSON | None exposed in the inspected `view`/`list` JSON |

Primary endpoints: original [metadata](https://www.kaggle.com/api/v1/datasets/view/hkayan/industrial-robotic-arm-anomaly-detection) and [inventory](https://www.kaggle.com/api/v1/datasets/list/hkayan/industrial-robotic-arm-anomaly-detection); successor [metadata](https://www.kaggle.com/api/v1/datasets/view/hkayan/industrial-robotic-arm-imu-data-casper-1-and-2) and [inventory](https://www.kaggle.com/api/v1/datasets/list/hkayan/industrial-robotic-arm-imu-data-casper-1-and-2).

The original identity fields and complete name/size inventory match the metadata saved around our acquisition. This establishes that the current listing still agrees with that receipt. We did not redownload the archive or rehash its multi-gigabyte contents in this correspondence task.

The successor's MIT field does **not** replace the original listing's CC BY-SA receipt, establish a historical relicensing event, or license either paper's implementation. Preserve attribution and each acquisition's applicable terms separately. Dataset, paper and code licenses are different records; this report provides no authorization to upload raw data.

### File overlap is partial, and size equality is insufficient

| Original v3 member | Received bytes | Successor v2 inventory counterpart | Correspondence established |
|---|---:|---|---|
| `dataset/nicla.csv` | 138,908,648 | `nicla.csv`, same advertised size | Same basename and size only across listings; successor bytes/hash unmeasured |
| `dataset/right_arm.csv` | 1,978,193,094 | `right_arm.csv`, same advertised size | Same basename and size only across listings; successor bytes/hash unmeasured |
| `dataset/left_arm.csv` | 1,965,113,819 | Not in the fourteen-file inventory | Original-only member in the inspected inventories |
| `dataset/arms.pcap` | 3,703,911,932 | Not listed | Original-only member in the inspected inventories |
| `nicla_fixed.csv` | 113,184,581 | Not listed | Original-only member in the inspected inventories |

The successor's other twelve names are `IMU_10Hz.csv`, `IMU_20Hz_freq_drop.csv`, `IMU_20Hz_freq_drop_2.csv`, `IMU_2Hz.csv`, `IMU_Acc_Gyro_20Hz.csv`, `IMU_earthquake.csv`, `IMU_extra_weigth.csv`, `IMU_hitting_arm.csv`, `IMU_hitting_platform.csv`, `IMU_magnet.csv`, `quaternions_20Hz.csv`, and `quaternions_no_idle.csv`. The spelling `weigth` is the provider's filename. These representation/frequency/disturbance files are not interchangeable with the original recording. Their names alone do not establish chronology, schemas, labels or cyberattack semantics; their contents were not acquired or inspected here.

## Which release does each baseline actually identify?

| Baseline and frozen source | Actual collection/file evidence | Published input/split digest evidence | Byte-identity verdict |
|---|---|---|---|
| **CASPER**, DOI [10.1145/3670414](https://doi.org/10.1145/3670414); notebook `bff03c91d155bf3134f6d801d3a4f4af7ea78adb` | Corrected manuscript §6.3/Table 11 describes IMU, two controller files and PCAP. Notebook cells 1–2/10 describe the IMU/controller sources and read `nicla.csv`/`right_arm.csv`; detection uses the IMU. Our acquired original v3 inventory matches that multimodal collection. `nicla_fixed.csv` is not the specified detector input. | No published raw-file SHA-256, annotation/split hash or checkpoint-to-data receipt found in the inspected paper/notebook/tree. | **Strong collection and score-count correspondence, no exact published-byte proof.** Figure 11's total and class counts agree with received-length/static-label arithmetic. Table 11's IMU count differs by 750. |
| **TWINE**, DOI [10.1016/j.iot.2026.101976](https://doi.org/10.1016/j.iot.2026.101976); code `841e1195acf90835c4c427e0fb48d10c08ed30d5` | README lines 27–28 explicitly link the original pick-and-place listing and name `right_arm.csv`. `scripts/training.ipynb` cell 2 reads `/right_arm.csv`; `simulation_robotic_arm.ipynb` cell 13 reads `./Data/right_arm.csv`. No explicit release number is pinned. | No input/split checksums or saved selected-row manifest found in the complete inspected repository. Full paper remains inaccessible, so paper-specific release details remain unverified. | **Original-listing and loader-schema correspondence.** Our v3 right-arm file is a plausible compatible source, not a verified copy of the publication's actual input. The 63-feature training path and five-feature demonstration are different code paths. |
| **CatBoost on CASPER**, DOI [10.1109/LSENS.2026.3656499](https://doi.org/10.1109/LSENS.2026.3656499); code `7f2a691f94f548e6b7c744ee0eeee287489a8639` | Publisher-deposited reference 8 cites CASPER 2024; reference 10 names the **CASPER 1 & 2** Kaggle listing. README points to that listing/DataPort with malformed Markdown links. `final_multi_run.py` lines 59–89 loads `data/nicla.csv` and `data/right_arm.csv`, both basenames present in both listings. | No acquired-data digest, version pin, sampled-row IDs or split-array hashes found in the inspected code/result artifacts. Stored run summaries do not contain original observations or prediction-level provenance. Full paper remains inaccessible. | **Dataset-family/filename correspondence only; collection version unresolved.** Neither the reference nor filenames prove original v3, successor v2 or identical cross-listing bytes were used. |

Source anchors: [CASPER notebook](https://github.com/hkayann/1D-CNN-Anomaly-Detection-via-CASPER/blob/bff03c91d155bf3134f6d801d3a4f4af7ea78adb/notebooks/casper.ipynb), [TWINE README](https://github.com/mubashar-iqbal/TWINE/blob/841e1195acf90835c4c427e0fb48d10c08ed30d5/README.md), [CatBoost loader](https://github.com/Priyanshu-byte-coder/CatBoost_Anomaly_Detection_implementation/blob/7f2a691f94f548e6b7c744ee0eeee287489a8639/final_multi_run.py), and locally preserved [CatBoost Crossref record](../baselines/catboost/artifacts/crossref.json). These anchors identify available sources, not executed publication revisions.

## Labels, times and processing are also different

| Baseline | Input/preprocessing observed in source | Label source | Timestamp and chronology behavior |
|---|---|---|---|
| CASPER CNN | Nine external-IMU features; skip six startup records, trim 897 rows, trailing median width 20; normal prefix split 60/20/20; training-fitted standardization; 755-step forecasting plus 755-residual aggregation. | Manual eight-interval IMU annotation after inspecting GyroX, in filtered coordinates (cells 21–25). Score targets use majority labels over 755 predicted positions (cell 95). This is not a direct timestamp join to controller flags. | IMU file has no time column. Controller data is consulted during annotation, but its clocks do not supply IMU timestamps. Variable acquisition/start offsets are described by the notebook. Exact physical onset/delay remains unresolved. |
| TWINE full-feature training | Expands vectors; selects six scalars plus all vector coordinates: **63 inputs under our completely audited original schema**, a static inference rather than an executed loader count. Timestamp, safety status and target are excluded. The demonstration instead uses five scalar inputs and every hundredth row. | Original controller `Anomaly State`, renamed `Anomaly_State`, is a supervised training target. No manual IMU intervals or acceleration-derived labels enter these paths. | The CSV has native controller time, but the source selects features without it and randomly splits rows; the demo resets indices after a random split. It does not preserve a chronological evaluation stream. |
| CatBoost main script | Reads raw-style IMU with six skipped records; samples up to 100,000 rows independently per modality. Controller fields expand to **64 inputs under the audited schema**; IMU has nine values, padded before stacking below controller rows. Fits scaling before random 60/20/20 partitioning. | Controller rows retain `Anomaly State`. IMU rows get **synthetic** labels when acceleration magnitude exceeds the selected sample's 95th percentile (lines 186–206). These targets do not reproduce CASPER's eight motion intervals. | Controller timestamp is not included in constructed features; random sampling resets row indices. The two modalities are stacked as separate observations, not joined by time. The window helper is defined but not used by the main preprocessing path. |

The 64-versus-63 controller difference follows from CatBoost retaining `Safety Status` in addition to the fields selected by TWINE. It does not establish either paper's actual final feature count without complete publication/run provenance. It also means substituting one author's feature array for another is a scientific protocol change, not a harmless file-path adjustment.

For our received original files, a full schema audit supports `Timestamp` as **controller-boot-relative seconds** through matched acquisition-field definitions and official RTDE documentation. That interpretation improves on the earlier receipt's unverified-unit wording, but no boot-to-UTC anchor or cross-device synchronization log exists. The two arms have separate clocks; identical rowwise schedule flags do not establish simultaneous physical effects. The external IMU still has no time column. See [sensor/clock evidence](CASPER_SENSOR_SCHEMA.md); do not copy the earlier receipt's superseded unit uncertainty as the current conclusion, or overstate this update as synchronized ground truth.

## Our hashes: exactly what they prove

The original archive and member hashes below come from the completed [receipt](../datasets/manifests/casper_v3_receipt.json), whose integrity/profile checks are described in [the identity audit](CASPER_DATASET_IDENTITY.md). They are locally measured received-byte identities, **not author-published checksums**.

| Received artifact | SHA-256 |
|---|---|
| `original_casper_v3.zip` | `07f2daf948c8244c396c7b4d2fe4c475880a3a6577f982fc1738b5379b0e5409` |
| `dataset/arms.pcap` | `e58032aa4058375f865f3b19348fd56042b8a4f29dff92178ab54f11b07d1bb9` |
| `dataset/left_arm.csv` | `35552b683edcdd15be403f050c391979d1bc6f652908bbe5066323b79f9af777` |
| `dataset/nicla.csv` | `02653ba6d81cbfd1f47a1a71522f2c10a48fc9d8dee41e59d7df8d66608b5cd1` |
| `dataset/right_arm.csv` | `181662e25de09c1f4ed05e0877a65c40225752d6f54575ddb1cdf8a0cf29a334` |
| `nicla_fixed.csv` | `601fccb447f5c661ac5fe2885d5c38741aed979c58f6e9ce193768ad50ed4fe7` |

The prior positional comparison found original post-startup `nicla.csv` and `nicla_fixed.csv` numerically equivalent after IEEE-754 binary64 parsing, with canonical numeric-sequence hash `83b8bd6702a32b3c033c1cb27cace44856759adaf1f3cb22e23d73d667e19a0b`. Their byte hashes differ. This equivalence does not turn the fixed file into labelled, synchronized, filtered or independent data; its historical transformation process is still undocumented.

The strongest CASPER correspondence is narrower than a content hash: our received length plus the pinned notebook's eight slices and window operations produces **676,807 score positions**, with **341,608 positive** and **335,199 negative** majority targets. Those totals equal Figure 11's confusion-matrix marginals. Predictions and thresholds were not generated to obtain this check. Numerous files could have the same counts, so this cannot identify unique experimental bytes. [Exact lineage and qualifications](CASPER_ANNOTATION_LINEAGE.md).

## Fresh metadata receipts and audit limits

The four small JSON responses are preserved under ignored `manufacturing/local/baseline_dataset_correspondence/`. Their raw bytes total 23,908. The receipt `metadata_receipts_network.json` records URLs, UTC times, response status, byte counts and SHA-256; `metadata_receipts.json` preserves the preceding sandbox-DNS failures. The ordinary web tool could not parse these endpoints, but bounded standard-library HTTPS retrieval succeeded with HTTP 200 for all four. Neither failure implies a restricted dataset.

| Receipt file | Bytes | SHA-256 |
|---|---:|---|
| `original_view.json` | 7,195 | `64488ff5e399fc1cf443ff4ddea8604c7c557dea4ea80821ede84a1b91dd8548` |
| `original_list.json` | 1,797 | `cb73324ccc9b8c86c6e803eeeee7f08384cb96361bec6b808a4ed1d6c459c09c` |
| `casper12_view.json` | 10,096 | `a296275fb07269fcf8568183eed7c2ece91865f195e5b0a8eeee3ffd855fd469` |
| `casper12_list.json` | 4,820 | `c87c489c21e15ae12cb312b3c33005fd837b9df76eef6c7a7a54437b83323442` |

Working directory was the repository root. Retrieval used Python standard-library `urllib.request` GETs to the four API URLs above, `User-Agent: Kaggle/1.7.4`, timeout 20 seconds and a 1 MiB maximum per response; JSON was parsed before saving. No archive or single-member download endpoint was opened. Static source review parsed notebook JSON/read source text; it did not import those modules. Prior raw-file hashes and schema measurements were referenced, not remeasured here. Current listing metadata does not prove that a historical publication used its current latest version.

## Decision for the next stage

Keep **original CASPER v3 as our received reference release**, with its original terms and hashes. A future common-release experiment can deliberately make methods use these bytes, but cannot retroactively prove they were used in the publications. Any changed inputs, labels, chronology or calibration must be disclosed as modified-protocol author-code execution or an independent implementation, as appropriate.

Three unresolved decisions remain before a fair run: which information-access track each method belongs to; which fixed labels and temporal targets are defensible; and whether unavailable manuscript/run evidence permits faithful reproduction at all. Sharing a listing or filename does not settle these decisions. In particular, do not pool CASPER's normal-only external sensing, TWINE's supervised controller data and CatBoost's mixture of controller flags with synthetic IMU labels into one headline ranking. The [comparison protocol](COMPARISON_PROTOCOL.md) remains proposed; no training admission is granted by this audit.
