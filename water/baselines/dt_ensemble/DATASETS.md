# Ensemble dataset requirements and gaps

**Verification update — 16 October 2026:** [The source audit](VERIFICATION_REPORT.md) confirms the publication identity but finds material mathematical, metric, citation and protocol issues. Keep this paper on experimental hold; published claims remain unvalidated.
Checked **16 October 2026**: **SWaT/WADI access approval and raw files have not been received or verified**. Downloading this open-access article does not grant dataset permission. See [acquisition status](../DATASET_ACQUISITION_STATUS.md) and the [provider checklist](../../docs/DATASET_ACCESS_CHECKLIST.md).

## Published description

| Dataset | Authors' described data and split | Unresolved issue |
|---|---|---|
| SWaT | 51 features, 11 days, 946,722 total samples; training days 1–7 (634,374), validation day 8 (86,065), test days 9–11 (226,283). Validation described as normal-only; test described as containing all 41 attacks. | Exact release, filenames, filtering, timestamps and labels absent. Official December-2015 description has seven normal days followed by four days with attacks; the article's normal day 8 needs explanation. |
| WADI | 123 features, 16 days, 1,221,370 samples, 15 attack types; training days 1–11, validation day 12, test days 13–16. | Exact collection/revision, dropped channels, label corrections, split timestamps and preprocessing artifacts unverified. |
| Tennessee Eastman | 52 variables, 20 fault conditions; training hours 1–32, validation 33–36, test 37–48. | Outside our shared SWaT/WADI numerical comparison. Fault conditions are not automatically cyberattacks; release and generation protocol unresolved. |

Source: [publisher](https://www.nature.com/articles/s41598-026-53863-z), “Experimental setup and datasets,” Table 2 and Data availability; [local VOR PDF](artifacts/papers/Ensemble_ScientificReports_VOR.pdf). Counts above are author-reported, not local file measurements.

The paper describes a **10 Hz** evaluated stream and a **50-sample / five-second** window. The relationship to the eventual provider files' actual cadence must be established; do not silently reinterpret samples as seconds or resample to force agreement. It also describes training-statistic min–max scaling, adaptive EWMA normalization and imputation without a released complete preparation pipeline. Their ordering, fitted state and information access require clarification.

The article's “publicly available” wording links to iTrust but does not remove provider access/redistribution conditions. No raw manifest, processed release, source-data supplement or matching preprocessing code was found. No exact equivalence with CAROTS or IT-DT is established.

## Common-project receipt and preparation

Store authorized original provider files once under water's ignored `datasets/raw/`, unchanged. Record source/release, authorized user(s), filenames, SHA-256 hashes, schema, timestamps and label provenance; keep private approval details under water's ignored `local/`. Do not put raw data in this baseline folder, Git, or sibling sector projects.

After receipt, freeze the same raw release, eligible observations, attack annotations and evaluation intervals for all water methods. Keep reproducible conversions under `datasets/processed/`. Split chronologically before windowing; isolate fitting, development, calibration and final evaluation. Preserve gaps and episode boundaries. Prevent imputation, adaptive normalization and gating from seeing future values or test labels.

Using our common clean protocol will require an explicit deviation record if the authors' original split remains unreconstructable. A filename or matching dataset name is insufficient for a faithful reproduction. No benchmark loading or preparation was performed in this collection task.
