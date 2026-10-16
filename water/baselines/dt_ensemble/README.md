# Digital-twin/deep-learning ensemble study collection

**Verification update — 16 October 2026:** [The source audit](VERIFICATION_REPORT.md) confirms the publication identity but finds material mathematical, metric, citation and protocol issues. Keep this paper on experimental hold; published claims remain unvalidated.
Collected for the water project on **16 October 2026**. This folder holds public paper materials and our audit notes. **No implementation, model execution or reproduced result exists here.**

**Paper:** Ali Sayghe, Mohammad D. Alahmadi and Abdulrahman A. Gharawi, *A digital twin and deep-learning ensemble for cyber attack detection in industrial control systems at the IoT edge*. *Scientific Reports* **16**, 23318 (2026). [Publisher / DOI](https://www.nature.com/articles/s41598-026-53863-z): `10.1038/s41598-026-53863-z`. Peer-reviewed journal article; individual review reports were not verified.

Received **13 October 2025**; accepted **14 May 2026**; published **22 May 2026**; publisher's version-of-record date **27 July 2026**. Use the current version of record for study. The separately collected accepted manuscript is historical material, not a second baseline.

## Start reading

1. Open the [version-of-record PDF](artifacts/papers/Ensemble_ScientificReports_VOR.pdf). Begin with the Methods definitions of the plant, process model, EKF, residual and ensemble score.
2. Explain Equation 5 (state correction), Equation 13 (alarm gate), and the adaptive-threshold/drift paragraphs separately. The alarm gate does not by itself specify which observations are admitted to learning.
3. Read [DATASETS.md](DATASETS.md) and [EXPERIMENTS.md](EXPERIMENTS.md), especially the unresolved SWaT day numbering, sampling rate and certified-normal window selection.
4. Use [PUBLISHED_RESULTS.md](PUBLISHED_RESULTS.md) to find the authors' tables, graphics and reference list. Treat their statements as claims to scrutinize.
5. Write your own summary and questions. This collection does not attest that a researcher has read or understood the article.

## Collection map

| Material | Location |
|---|---|
| Current article | [VOR PDF](artifacts/papers/Ensemble_ScientificReports_VOR.pdf), [publisher HTML](artifacts/papers/publisher.html) |
| Historical accepted version | [Accepted manuscript PDF](artifacts/papers/Ensemble_accepted_manuscript.pdf) |
| Official PMC package | [PDF](artifacts/pmc/PMC13402577.1.pdf), [XML](artifacts/pmc/PMC13402577.1.xml), [plain text](artifacts/pmc/PMC13402577.1.txt), and five article JPGs in `artifacts/pmc/` |
| PMC metadata | [pmc_oa.json](artifacts/metadata/pmc_oa.json); article ID `PMC13402577`, version 1, PMID `42174001` |
| Local table/reference extractions | [Extraction index](artifacts/extracted/INDEX.json); derivatives of the article, not author experiment logs |
| Publisher citation and bibliography | [paper.ris](artifacts/references/paper.ris), [author_bibliography.ris](artifacts/references/author_bibliography.ris) |
| Project citation | [CITATION.bib](CITATION.bib) |
| Actual retrievals, sources, versions, byte counts and hashes | [Resource manifest](../RESOURCE_MANIFEST.json) |
| Benchmark permissions and receipt | [Acquisition status](../DATASET_ACQUISITION_STATUS.md) |

The article has seven tables, four figures and an algorithm image, plus 31 references. No supplementary-material element was present in the inspected PMC XML. Bibliography collection does not verify its entries or their relevance. Saved HTML can depend on remote assets; use the PDF and separately saved media for offline reading.

The article is **CC BY 4.0** ([license](https://creativecommons.org/licenses/by/4.0/)), subject to any excluded third-party credit lines. Retain authors, title, DOI, version, license and an indication of changes in reused material. PMC is an additional source of the downloaded package; NIH/NLM does not endorse this project. The original XML/text/media are preserved separately from local derivatives. These rights do not license the datasets or unreleased software. Artifacts stay ignored locally; publishing remains a separate authorization.

## What is missing

The publisher states that experimental result files and trained models are not publicly available; access by author request is conditional. Source code is promised upon publication, but no matched public runnable repository, software license, release, checkpoint, fitted physical model, aligned score stream or complete run log was verified in the bounded search.

The nearby author repositories for a 2025 SCADA case study and a physics-informed generative framework describe different papers. They are not substitutes for this article's implementation. No author was contacted. Exact SWaT/WADI files and access approval remain absent. This article is close prior work to study critically; it is not approved for numerical reproduction. See the [detailed evidence audit](../../docs/literature/CAUSAL_AND_ENSEMBLE.md).
