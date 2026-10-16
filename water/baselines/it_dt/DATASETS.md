# IT-DT dataset requirements and gaps

Status checked **16 October 2026**: **no local SWaT/WADI raw files or provider approval verified**. [Acquisition status](../DATASET_ACQUISITION_STATUS.md) and the [provider access checklist](../../docs/DATASET_ACCESS_CHECKLIST.md) govern receipt. Materials downloaded for this baseline are papers and source assets, not benchmark data.

## What the manuscript specifies

| Dataset | Manuscript evidence | Still needed |
|---|---|---|
| SWaT | Section III-A identifies a model using seven days of normal operation; selected state order `n=12`. Section V reports detection and a separate Attack #41 example. | Provider release, original filenames and hashes; exact train/calibration/test timestamps; feature/control mapping; attack metadata and how Attack #41 was identified. |
| WADI | Section III-A identifies a model using fourteen days of normal operation; selected state order `n=25`. Section VI-A refers to `p=127` measurements. | Provider release/revision, filenames and hashes; retained channels and control inputs; missing-column handling; exact timestamps and label interpretation. |

Evidence: [versioned manuscript](https://arxiv.org/html/2603.01621v1), Sections III–VI; [local PDF](artifacts/papers/IT_DT_arxiv_2603.01621v1.pdf).

The paper does not supply a verified raw-file manifest, conversion script or processed dataset archive. Scaling, missing-value handling, startup exclusion, sampling/resampling, control-input eligibility and validation partition size cannot be reconstructed confidently from the accessible description alone. Its seven/fourteen-day identification claim also needs reconciling with the separate attack-free validation period so calibration is independent of fitting.

CAROTS' expected SWaT `Normal_v1` / `Attack_v0` files and WADI A2 2019 paths are **candidates for a common project release**, not evidence that IT-DT used those exact versions. Likewise, channel counts alone cannot establish release equivalence.

## How data will eventually be organized

- Obtain authorized provider files once under water's ignored `datasets/raw/`; keep their original bytes unchanged. Do not duplicate raw files into every baseline folder or create links into another sector's project.
- Record authorized user(s), provider terms, original names, source/release, byte counts and SHA-256 hashes before loading. Keep private approval records under water's ignored `local/`.
- Freeze one common raw release, label/attack annotation and eligible input specification for all three methods. Keep conversions and method-specific preparation under `datasets/processed/` with provenance.
- Split normal data chronologically before windowing, preserve episode boundaries/gaps, and fit every transform/model only on its designated development partition. Specify a separate calibration partition and normal-only evaluation interval.
- Resolve residual timestamp/score alignment, warm-up coverage and reset rules. Keep held-out test attacks closed until every compared method and evaluation decision is frozen.

The eventual common protocol may differ from the publication. Record that explicitly; matching the name “SWaT” or “WADI” is not a same-release reproduction. No dataset loading, preprocessing or synthetic replacement benchmark was performed in this collection task.
