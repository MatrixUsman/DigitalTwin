# Dataset access and release checklist

Audit date: **2026-10-16**. **No raw SWaT or WADI dataset files are present in the audited workspace. Provider approval remains pending.** The assistant submitted the user-authorized official request for both datasets and observed website confirmation; details are recorded below. External storage was not searched without a supplied location.

**Stage 3 follow-up:** the user reconfirmed non-receipt. The [identity audit](DATASET_IDENTITY_AUDIT.md), [candidate release register](../datasets/manifests/RELEASE_CANDIDATES.json) and [observed inventory](../datasets/manifests/LOCAL_INVENTORY_2026-10-16.json) separate provider claims, code expectations, remote metadata and locally measured fields. Receipt checks below remain open: timestamp/label inspection and raw-file hashes cannot be completed without originals.

**Stage 1 update:** the user supplied their university email and explicitly agreed to the terms/privacy consent and submission. The [official application](DATASET_REQUEST_PREPARATION.md) was submitted in Safari for SWaT/WADI, with website confirmation observed by the post-submission clock check at **2026-10-16 16:15:51 UTC**; this is an observation bound, not an exact server timestamp. The form's default date **17 October 2026** was preserved because it was already that date in Singapore. The private record is kept under ignored `water/local/`. No approval, download link or dataset receipt is established. Bounded mirror checks did not establish a stronger authorized acquisition route.

**Earlier user correction, 2026-10-16:** the researcher reported having a COMSATS Sahiwal student university email, superseding the earlier statement of no affiliation/email. The address was subsequently supplied privately and entered in the authorized request; mailbox operation, delivery and dataset eligibility remain unverified. The [official COMSATS Sahiwal student-email form](https://sahiwal.comsats.edu.pk/IT_Forms/Student_Email_ID_Request_Form_converted.pdf) lists the `@students.cuisahiwal.edu.pk` domain; this establishes an institutional student-email route, not approval of this individual request.

The [current iTrust request form](https://www.sutd.edu.sg/itrust/request-for-datasets/) requires a university/organisation email, excludes personal addresses, and shows no faculty-only requirement or student ban. The user's supplied student address was used for the submitted request; only iTrust can confirm approval. The mailbox's operation and email delivery have not been independently verified. Public-paper reading can proceed while approval is pending.

## Provider evidence and unresolved release choices

| Dataset | Verified provider description | Release decision still required |
|---|---|---|
| SWaT December 2015 | A1 describes 7 normal days and 4 attack days, 51 sensor/actuator variables. A2 provides normal v0/v1; v1 removes the initial 30 minutes. | Match actual normal/attack files to release and documentation; do not remove startup twice. |
| WADI / WaDi | A1 describes 14 normal days and 2 attack days, 123 sensor/actuator variables. A2 revises unstable readings and attack labels. | Confirm A1 versus A2 and exact correction state; names alone do not establish release equivalence. |
| December 2023 paired collection | Provider describes a clean paired operation/CrossOver collection. | Optional later regime-change evidence only; not a substitute for the original attack benchmark. |

Sources: [SWaT characteristics](https://www.sutd.edu.sg/itrust/itrust-labs/datasets/dataset-characteristics/swat/), [WADI characteristics](https://www.sutd.edu.sg/itrust/itrust-labs/datasets/dataset-characteristics/wadi/), [release summary](https://www.sutd.edu.sg/itrust/itrust-labs/datasets/summary-of-available-datasets/).

The official pages are not internally consistent in every label: the summary lists WADI A2 as **19 November 2019**, whereas its characteristics page dates the update **19 December 2019**. The summary calls the December 2023 SWaT collection A10, while the characteristics text calls it A9. Preserve the supplied archive/readme labels, original filenames, dates, and hashes; do not silently resolve these differences by renaming files.

CAROTS expects names including `SWaT_Dataset_Normal_v1`, `SWaT_Dataset_Attack_v0`, `WADI_14days_new.csv`, and `WADI_attackdataLABLE.csv`; these are **code expectations, not files we possess**. See the [CAROTS evidence](literature/CAROTS_AND_INFORMATION_THEORETIC.md). Candidate choice: SWaT December 2015 corrected normal v1 plus attack v0 and WADI A2, subject to authorized receipt and exact verification. No release is frozen yet.

## Access checklist

- [x] Confirm current access state: the user reports no iTrust approval received. A permitted acquisition source and local receipt remain outstanding.
- [x] Review the [official request page](https://www.sutd.edu.sg/itrust/request-for-datasets/) and [terms](https://www.sutd.edu.sg/itrust/itrust-labs/datasets/terms-of-usage/). The user explicitly agreed to the stated terms/privacy consent before both consent boxes were checked and the request submitted.
- [x] Use the researcher's supplied university email and requester identity; retain the exact address only in the ignored private record. The fields were read back before submission. This confirms what was entered, not mailbox operation, email delivery or provider approval.
- [x] Submit the request for **SWaT and WADI** and preserve the website confirmation/observation time privately. The form requests dataset families, not exact releases. No request identifier or download link was displayed. See [submission record summary](DATASET_REQUEST_PREPARATION.md); do not submit a duplicate while this request is pending.
- [ ] Receive and privately record provider approval, its date, authorized users, permitted scope, applicable terms and download route. Exact releases remain subject to receipt and verification.
- [ ] Obtain the original process/historian normal and attack recordings, README/schema, and corrected attack interval table for each selected release. PCAPs are unnecessary for the initial process-telemetry plan.
- [ ] Check free space against actual archives, extraction, derived data, and run outputs before downloading. No download size or runtime is assumed.

iTrust's published terms require credit and publication notification, prohibit sharing the dataset with other users, and disclose requester/organization names and request dates. Each collaborator must arrange their own access where required. Keep benchmark data away from public repositories, shared artifacts, chat uploads, and cloud jobs until both the terms and explicit user authorization permit the action. [Provider terms](https://www.sutd.edu.sg/itrust/itrust-labs/datasets/terms-of-usage/)

## Receipt and integrity checklist

- [ ] Store untouched originals under this project's ignored `datasets/raw/<dataset>/<release>/` or an authorized external read-only location. Derived files belong in `datasets/processed/`. Keep credentials/approval emails in `local/`, never Git. Paths resolve from `water/`; other collaborators/projects need their own permitted access.
- [ ] Record byte size and SHA-256 of every raw archive/file, provider filename, acquisition date, and source/terms reference. Hash before and after a loader check; do not rewrite originals.
- [ ] Inspect schema, header rows, sheets/encoding, timestamp format, timezone or its absence, cadence, units, variable roles, and missing markers.
- [ ] Confirm labels against release-specific documentation and attack intervals. WADI A2's provider convention is attack `-1`, normal `1`; explicitly map to internal attack `1`, normal `0`. Never guess from numerical sign.
- [ ] Record actual row counts, date ranges, gaps, duplicates, constant/all-missing channels, excluded columns, and known startup removals. Provider variable counts need not equal a parsed table's total columns.
- [ ] Preserve gaps created by removed unstable periods. Do not create windows across discontinuities or treat noncontiguous rows as adjacent seconds.
- [ ] Verify feature/label alignment after header removal, trimming, downsampling, and window creation using row identifiers and timestamps.
- [ ] Freeze one raw manifest and one split/preprocessing manifest shared across methods before final training. Keep alternative releases in separately named experiments.
- [ ] Check future Git index before committing: no raw/derived data, private URLs, credentials, or data-bearing logs. Ignore rules cannot prevent forced additions.

## Proposed manifest fields (not populated data)

```text
dataset_id, provider_release_label, source_document_version
original_filename, local_relative_path, bytes, sha256, acquired_at
normal_or_attack, timestamp_format, timezone_status, sample_interval
schema_hash, feature_names_and_roles, label_mapping, attack_table_hash
raw_rows, parsed_rows, start_time, end_time, gap_policy
header_and_startup_handling, excluded_columns_with_reasons
approval_reference_local_only, permitted_use, terms_reference
```

A manifest must distinguish provider facts from measured file properties. All measured fields are currently **unknown**, not zero. Checksums identify files but do not establish access permission.

## Alternative-source search — 2026-10-16

The user requested searches beyond iTrust. Public repository listings, metadata, dataset cards, and paper availability statements were inspected. **No dataset contents were downloaded, loaded, or uploaded.** Listed filenames, sizes, and row counts below are host/author metadata, not measured local file properties. None of these leads yet establishes a complete, authorized pair of the selected releases.

| Source | Observed evidence | Remaining limitation |
|---|---|---|
| [THUML Time-Series-Library, SWaT](https://huggingface.co/datasets/thuml/Time-Series-Library/tree/ffdb671c1a34bbed9fa689dbc4bcbf1ac7c5ba4a/SWaT) | Lists `SWaT_Dataset_Normal_v1.xlsx` (131 MB) and `SWaT_Dataset_Attack_v0.xlsx` (116 MB), plus four CSV derivatives. The THUML code repository links this host. | Strongest SWaT technical lead: names match CAROTS inputs. Actual contents, official-file equivalence, complete annotations, and permission remain unverified. Card advertises CC BY 4.0; mirror-specific iTrust authorization was not established. |
| [THULab/SWaT](https://huggingface.co/datasets/THULab/SWaT/tree/main) | Lists train/test `.tsfile` derivatives. Card cites THUML and says timestamps are reconstructed from row index. | Transformed data cannot silently substitute for original timestamped recordings in event/delay evaluation. Release and permission unresolved. |
| [Vishal Agrawal's Kaggle SWaT](https://www.kaggle.com/datasets/vishala28/swat-dataset-secure-water-treatment-system) | Public metadata/file-list API lists `normal.csv`, `attack.csv`, `merged.csv`; version 3, uploader-supplied CC0 tag. | Exact release and split/label handling unverified. In particular, an attack-only CSV need not be the original mixed normal/attack test recording. Download authentication and contents not tested. |
| [FTSAD WADI directory](https://github.com/EmorZz1G/FTSAD/tree/main/datasets/WADI) | Lists `WADI_train.npy`, `WADI_test.npy`, `WADI_test_label.npy` as small Git LFS pointer files; README instructs use of Git LFS. | Processed-array lead. Underlying object availability, original release, preprocessing, retained timestamps, labels, and data permission remain unverified. A code license does not itself establish third-party dataset permission. |
| [Giovanni Monco's Kaggle WADI](https://www.kaggle.com/datasets/giovannimonco/wadi-data) | A [research notebook](https://github.com/rezahamzeh69/ics-ot-wadi-hybrid-ids/blob/main/ics_ot_wadi_hybrid_ids.ipynb) explicitly downloads this dataset slug and expects normal and attack CSV files. The Kaggle page resolves. | The dynamic file list and license were inaccessible to the browser. Current files, completeness, release, and permission remain unverified; the notebook's expectations are not a current file inventory. |
| [TinyML dissertation repository](https://github.com/MJ636UoW/TinyML_based_increamental_LSTM) | Metadata lists a roughly 2 MB `WADI_attackdataLABLE.7z`; the similarly named CSV is empty. No normal WADI file was found in the root listing. | Partial lead only; archive contents not inspected, release and permission unknown. Cannot establish the normal/attack pair needed for training/evaluation. |
| [Industrial Sensor Anomaly Detection Dataset, Kaggle](https://www.kaggle.com/datasets/colabsss/industrial-sensor-anomaly-detection-dataset) | A [publisher paper, data-collection and availability sections](https://link.springer.com/article/10.1007/s10791-026-10468-4) links it and describes transformed subsets of 1,000 SWaT and 500 WADI samples. Kaggle page/API could not be inspected fully with the browser tool. | Paper-reported reduced subsets, not verified full recordings or replacements for the agreed benchmark. Their derivation and permission remain unresolved. |

False leads were also checked: [Conviss/visual_dataset/WADI](https://github.com/Conviss/visual_dataset/tree/main/WADI) contains a processing script, and [ICS-Evasion-Attacks/WADI](https://github.com/scy-phy/ICS-Evasion-Attacks/tree/master/Data/WADI) provides instructions/features rather than the data. AnomalyBERT and AFMF direct users to request the official data. A repository README mentioning a dataset does not establish that it hosts it.

iTrust's [current terms](https://www.sutd.edu.sg/itrust/itrust-labs/datasets/terms-of-usage/) prohibit recipient sharing. This is an unresolved permission issue for the mirrors, **not proof that any particular host lacks separate authorization**. Keep the standard university-email request as the best-supported acquisition route while retaining these alternative-source leads for verification.

## Acquisition-session correction — 2026-10-16

The later resource-collection task retrieved the Kaggle public metadata/file-list APIs successfully, resolving the earlier dynamic-page access limitation. Version 1 lists `WADI_14days_new.csv` (493,730,164 bytes) and `WADI_attackdataLABLE.csv` (109,308,247 bytes), with an uploader Apache 2.0 label and no provenance description. The current THUML SWaT listing was pinned at `2b66e59ee19dac8f6f19fb5d4997f289fdfea357`; exact remote sizes and LFS hashes are retained in the [acquisition record](../baselines/DATASET_ACQUISITION_STATUS.md). These observations supersede only the earlier listing-access limitation, not the permission or release-equivalence unknowns.

Provider pages and mirror **metadata** were saved and hashed during resource collection. At that stage, raw/processed dataset folders were empty and no request had been submitted by the assistant. The later user-authorized [official submission](DATASET_REQUEST_PREPARATION.md) supersedes that no-submission status; approval and benchmark receipt are still pending. Public papers and CAROTS artifacts have been collected separately in [baseline packs](../baselines/README.md). A `.npy` graph or `.pth` causal-discoverer checkpoint in that pack is an upstream model artifact, not a received raw dataset.
