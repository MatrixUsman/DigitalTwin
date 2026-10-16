# SWaT/WADI acquisition status

Checked **16 October 2026**. The user explicitly reports **no iTrust approval received**. No raw SWaT or WADI files were downloaded, and no model was run. The search did find public mirrors; the unresolved issue is whether they provide the permitted, identical releases needed for a defensible comparison.

## Best matching public listings found

The following are **remote host metadata**, not measured local dataset properties or verified official checksums.

| Dataset/source | Listed file | Remote bytes | Match and limitation |
|---|---|---:|---|
| [THUML / Hugging Face](https://huggingface.co/datasets/thuml/Time-Series-Library/tree/2b66e59ee19dac8f6f19fb5d4997f289fdfea357/SWaT) | `SWaT_Dataset_Normal_v1.xlsx` | 130,566,907 | Matches CAROTS's loader filename; original release and provider permission not established |
| Same pinned listing | `SWaT_Dataset_Attack_v0.xlsx` | 116,016,616 | Matches CAROTS's loader filename; contents and annotations not inspected |
| [Giovanni Monco / Kaggle](https://www.kaggle.com/datasets/giovannimonco/wadi-data), version 1 | `WADI_14days_new.csv` | 493,730,164 | Matches CAROTS; no release/provenance description supplied |
| Same listing | `WADI_attackdataLABLE.csv` | 109,308,247 | Matches CAROTS; no source checksum or permission evidence supplied |

Total listed size of these four files: **849,621,934 bytes**, approximately 810.3 MiB before any working copies or additional metadata. This is not a downloaded-data count.

Hugging Face pin: `2b66e59ee19dac8f6f19fb5d4997f289fdfea357`. Its listed LFS SHA-256 values are:

```text
SWaT_Dataset_Normal_v1.xlsx  fb7bb0a9c10f86ad29d8f2ae4fd09284e7db70c76350f5b2afcca58d9ace6c49
SWaT_Dataset_Attack_v0.xlsx  6cc72c24425453879bac1565cae4c6f35ad585a578510ab2a27b325d1bac2e8d
```

The SWaT mirror advertises CC BY 4.0 and Kaggle's WADI metadata advertises Apache 2.0; these are uploader claims. Neither establishes separate authorization from the dataset provider. Kaggle metadata reports version 1, last updated 25 October 2024, with an empty provenance description. Current metadata snapshots are saved in ignored [artifacts/dataset_sources/](artifacts/dataset_sources/) and hashed in [RESOURCE_MANIFEST.json](RESOURCE_MANIFEST.json).

Additional processed-array, reduced-subset and incomplete mirrors are recorded in the [earlier search](../docs/DATASET_ACCESS_CHECKLIST.md). None supplies stronger evidence for an authorized, original pair. No inference is made that a particular mirror is unlawful; permission was simply not established in this audit.

## Why no mirror download was promoted to our dataset

The provider's [terms](https://www.sutd.edu.sg/itrust/itrust-labs/datasets/terms-of-usage/) prohibit recipient sharing and direct additional users to request access. Public visibility and a matching filename do not resolve that condition or establish release identity. Following the project's data rules, only mirror metadata was collected. The assistant did not submit a request or contact anyone.

The supported route is the [official request form](https://www.sutd.edu.sg/itrust/request-for-datasets/) using the researcher's own university email. The current form requires a university/organisation email and excludes personal addresses; it does not state a faculty-only restriction. The user's reported COMSATS Sahiwal student address is a plausible application route, not approval.

## Release matching is still conditional

| Method | Dataset evidence | What remains before matching |
|---|---|---|
| [CAROTS](carots/DATASETS.md) | Loader identifies normal v1 / attack v0 SWaT and WADI A2-style filenames | Obtain permitted files; verify schema, timestamps, startup removal, label corrections and hashes |
| [IT-DT](it_dt/DATASETS.md) | Manuscript reports both datasets | Exact filenames/releases and executable preprocessing are unspecified/unverified |
| [Ensemble](dt_ensemble/DATASETS.md) | Manuscript reports both datasets | Exact releases, split definitions and day-8 normal-validation discrepancy need resolution |

Provider pages themselves label WADI A2 differently: the summary says **19 November 2019**, the characteristics page **19 December 2019**. Preserve received archive labels and documentation. Do not silently rename a release to make it appear matched.

## Receipt checklist for the next acquisition

1. Establish the permitted source and authorized researcher(s); retain approval/download details privately in `water/local/`.
2. Obtain original normal and attack recordings, release README/schema and attack-interval annotations. Initial work needs process telemetry, not every PCAP collection.
3. Save untouched files under `water/datasets/raw/<dataset>/<release>/`; compute local SHA-256 and sizes. Compare against supplied provider metadata where available.
4. Reconcile headers, labels, timestamps, gaps and startup handling before freezing the shared releases. Record unknowns instead of copying mirror metadata into measured fields.
5. Keep every method on the agreed raw inputs and evaluation rules; document any reimplementation or protocol deviation.

Authorized access and release verification remain unfinished. Reading the collected papers can proceed now.
