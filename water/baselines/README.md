# Water baseline resource collection

Collected **16 October 2026** for structured study. The three papers have separate folders. Their published claims and upstream files are **not our experimental results**. These remain learning papers, not three execution-ready baselines.

**Read the [verification report](../docs/BASELINE_VERIFICATION_REPORT.md) first.** The collection passed file-integrity checks, but the audit found material scientific, citation and code issues. CAROTS remains conditional; IT-DT and the ensemble are on numerical-reproduction hold. Per-paper reports and reference inventories distinguish identity verification from support for a claim.

| Folder | Available locally | Still missing or unresolved |
|---|---|---|
| [CAROTS](carots/README.md) | ICML paper, arXiv v1 PDF/HTML/TeX, bibliography, source figures/tables; 57 pinned author-code files; 16 SWaT/WADI CUTS+ graph/checkpoint/log artifacts | Authorized raw data, final detector checkpoints/aligned scores/full run logs, validated environment and corrected evaluation |
| [Information-Theoretic Digital Twins](it_dt/README.md) | arXiv v1 PDF/HTML/TeX, bibliography, three figure PDFs and inline tables | Matched public executable code, fitted model matrices, run artifacts and exact dataset releases |
| [Digital-twin/deep-learning ensemble](dt_ensemble/README.md) | Publisher version of record and accepted PDF, PMC PDF/XML/text, four figure images and algorithm image, seven extracted tables, 31-reference bibliography | Matched public code, trained models, scores/logs and protocol/release clarification |

**Start with the [paper study guide](../docs/PAPER_STUDY_GUIDE.md)** and each folder's `METHOD_TO_CODE.md`: [CAROTS](carots/METHOD_TO_CODE.md), [IT-DT](it_dt/METHOD_TO_CODE.md), [ensemble](dt_ensemble/METHOD_TO_CODE.md). Then consult `EXPERIMENTS.md`, `DATASETS.md`, `PUBLISHED_RESULTS.md` and `CITATION.bib`. The assistant's detailed source study is complete; actual researcher reading belongs in [the reading record](../papers/notes/READING_RECORD.md). Read CAROTS first, followed by IT-DT and the ensemble, using [the mechanism comparison](../docs/MECHANISM_COMPARISON.md) to distinguish their update and trust assumptions.

The CAROTS map traces real pinned author files/functions and records new CPA forecast-input and SOC averaging discrepancies; their runtime effects remain unmeasured. The twin maps provide conceptual implementation requirements because no matched author code is verified. Bibliographies remain preserved author material with per-paper verification inventories; identity checks do not verify every cited claim, and all cited full texts have not been downloaded.

## Dataset status

**SWaT and WADI are not downloaded.** The [official request](../docs/DATASET_REQUEST_PREPARATION.md) was submitted once with explicit user consent and website success confirmation. Email delivery and provider approval remain unverified. Public mirror listings include filenames that match CAROTS, but provider permission and byte equivalence remain unresolved. See [the acquisition status and mirror inventory](DATASET_ACQUISITION_STATUS.md) and [the receipt checklist](../docs/DATASET_ACCESS_CHECKLIST.md).

Store future authorized originals once under `water/datasets/raw/`; each baseline's `DATASETS.md` records its expected inputs. This avoids inconsistent duplicated datasets. No release has been frozen for all three methods.

## Provenance and storage

- [RESOURCE_MANIFEST.json](RESOURCE_MANIFEST.json): source URLs, retrieval attempts, byte counts and SHA-256 hashes for **110 downloaded objects** (24,796,785 bytes, approximately 23.6 MiB). These include metadata and multiple manuscript versions, not 110 papers.
- [DERIVED_ARTIFACTS.json](DERIVED_ARTIFACTS.json): **79 local reading derivatives** (7,369,776 bytes), each tied to its source hash and extraction method. These include safely extracted source files, PDF text, previews and XML table/reference excerpts.
- [INTEGRITY_AUDIT.json](INTEGRITY_AUDIT.json): subsequent hash, format, all-page PDF rendering, syntax and container checks of those 189 objects. Further bibliography-audit sources are recorded separately by the per-paper verification reports; the acquisition counts above describe the original collection.
- [acquisition_sources.json](acquisition_sources.json): explicit public download specification. CAROTS code and water artifacts are pinned to commit `63a41f45a2ae680d5cdbb2d5739e7a11264867cb` and checked against Git blob identities.
- Downloaded originals live in ignored `artifacts/`; the CAROTS snapshot is in ignored `carots/vendor/author_code/`. The snapshot is selective, not a Git clone: unrelated repository datasets and results were deliberately excluded. Its `datasets/` directory contains loader code, not benchmark recordings.
- Paper, code and third-party figure/class-file licenses differ. Preserve notices and credit lines. Local availability does not grant permission to republish everything. Files were not pushed to GitHub.

The collection was prepared with the installed research skill's source-verification guidance and PDF inspection tools. Source archives were extracted without compilation; author code and checkpoint files were not executed or deserialized. Three main PDFs were checked with `pdfinfo`, text extraction and first-page visual inspection. Some HTML snapshots reference remote assets; use the PDFs and extracted figures for offline reading.

## Recreate the public collection

From `water/`, using Python's standard library and the already installed Poppler tools:

```sh
python3 tools/collect_baseline_resources.py
python3 tools/prepare_baseline_resources.py
```

The collector verifies existing files, records failures and does not install dependencies, obtain datasets or run models. Its initial successful run used Python 3.15.0 and Poppler 26.10.0; this is **not a validated scientific-model environment**. Re-downloads of mutable web pages can change; retain the original manifest and archive when comparing versions.

No training, reproduced benchmark scores, researcher-attested reading, or experimental-admission decision is implied. See [the selection report](../docs/BASELINE_SELECTION_REPORT.md) and [reproduction plan](../docs/REPRODUCTION_PLAN.md) before implementation.
