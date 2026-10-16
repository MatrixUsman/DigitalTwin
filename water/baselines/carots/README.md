# CAROTS learning and reproduction pack

Acquired **16 October 2026** for the water project. This is a collection of author/publisher materials and our audit notes. **No model has been run and no results have been reproduced.**

**Paper:** Causality-Aware Contrastive Learning for Robust Multivariate Time-Series Anomaly Detection. HyunGi Kim, Jisoo Mok, Dongjun Lee, Jaihyun Lew, Sungjae Kim and Sungroh Yoon. ICML 2025, PMLR 267:30591–30608, 13–19 July 2025. [Publisher record](https://proceedings.mlr.press/v267/kim25aa.html); [citation](CITATION.bib). The separate arXiv v1 was submitted 4 June 2025, identifier `2506.03964v1`.

## Start here

1. Read the [published paper](artifacts/papers/CAROTS_ICML2025.pdf), beginning with Figure 1 and Sections 3–5. Explain the causal discoverer, the two augmentors, the encoder and the anomaly scores in your own words.
2. Read [datasets and release questions](DATASETS.md), then [original experiments and required changes](EXPERIMENTS.md).
3. Consult the [published-results guide](PUBLISHED_RESULTS.md). Keep the authors' reported measurements separate from our future runs.
4. Trace the [author README](vendor/author_code/README.md), [configuration](vendor/author_code/config.py), [data loader](vendor/author_code/datasets/build.py) and [predictor](vendor/author_code/models/carots/predictor.py). Reading these files does not require installing dependencies or running scripts.

CAROTS is our conditional first reproduction candidate and a non-twin comparison. Study both full CAROTS and CAROTS-dagger, which removes ensemble scoring; these are two variants of one paper. Their value here is testing what a twin adds beyond a learned detector. This selection does not establish that CAROTS is the strongest detector generally.

## What is stored

| Location | Contents and provenance |
|---|---|
| `artifacts/papers/` | Published proceedings PDF, arXiv v1 PDF and HTML. |
| `artifacts/source/` | Original arXiv source archive; extracted `arxiv_v1/` contains manuscript, bibliography, figure PDFs and table TeX. |
| `vendor/author_code/` | Selective, unmodified author files pinned to `63a41f45a2ae680d5cdbb2d5739e7a11264867cb`: 57 files including model code, scripts and two overview images. This is a source snapshot, not a complete Git checkout. |
| `artifacts/upstream_results/` | 16 author artifacts for SWaT/WADI: CUTS+ graphs, plots, validation logs and causal-discoverer checkpoints. These are not final CAROTS detector weights or our results. |
| `artifacts/metadata/` | Publisher/conference records, repository tree and issue snapshots. Issue reports are leads, not reproduced defects. |

The snapshot deliberately excludes the upstream top-level `data/` and `results/` trees; only the separately identified SWaT/WADI result artifacts were retained. Unrelated SMAP/MSL/SMD datasets were not collected. See the [resource manifest](../RESOURCE_MANIFEST.json) for exact URLs, byte counts, hashes and acquisition outcomes. No SWaT/WADI dataset files or provider approval have been received; see the [shared acquisition status](../DATASET_ACQUISITION_STATUS.md).

## Rights and remaining gaps

The [code license](vendor/author_code/LICENSE) is **Modified MIT License (Non-Commercial with Permission)**; retain its notice. The arXiv manuscript/source record specifies **CC BY-NC-SA 4.0**. These are different permissions; do not transfer a code license to datasets or assume every asset has identical terms. Local acquisition does not authorize uploading the bundle.

No final detector checkpoint, aligned anomaly-score archive, complete detector run logs, dependency lock or separate runnable supplement was found. The official [ICML presentation page](https://icml.cc/virtual/2025/poster/45960) had no downloadable poster/slides located and explicitly lacked a SlidesLive embed. OpenReview access was blocked. These are bounded search findings, not proof such materials do not exist.

Continue through the [detailed CAROTS audit](../../docs/literature/CAROTS_AND_INFORMATION_THEORETIC.md), [expanded audit](../../docs/literature/EXPANDED_SEARCH_2026-10-16.md), [selection report](../../docs/BASELINE_SELECTION_REPORT.md) and [water roadmap](../../docs/RESEARCH_ROADMAP.md). A researcher has not been marked as having read this paper.
