# IT-DT study collection

Collected for the water project on **16 October 2026**. This is a collection of the authors' published materials and our audit notes. **No IT-DT implementation, reproduction or experiment has been performed here.**

**Paper:** Inda Kreso, Mehran Tarif, Fatemeh Moradi, Iman Khazrak, Mostafa M Rezaee and Mohammadhossein Homaei, *Information-Theoretic Digital Twins for Stealthy Attack Detection in Industrial Control Systems: A Closed-Form KL Divergence Approach*. [arXiv:2603.01621v1](https://arxiv.org/abs/2603.01621v1), submitted **2 March 2026**. DOI: `10.48550/arXiv.2603.01621`. Only the preprint is verified; its arXiv DOI does not establish peer review.

## Start reading

1. Read the [PDF](artifacts/papers/IT_DT_arxiv_2603.01621v1.pdf), starting with Sections III–IV and Algorithm 1. Identify the control inputs, observed measurements, estimated state, innovation residual and detection score.
2. Use the [HTML manuscript](artifacts/papers/IT_DT_arxiv_2603.01621v1.html) to navigate equations and references. Locally saved HTML may retain online asset links; the PDF is the complete offline reading copy.
3. Read [DATASETS.md](DATASETS.md) and [EXPERIMENTS.md](EXPERIMENTS.md) before treating the method as reproducible. Distinguish Kalman state correction from parameter learning and threshold updates.
4. Use [PUBLISHED_RESULTS.md](PUBLISHED_RESULTS.md) to locate the authors' tables and figures. They are literature evidence, not our results.
5. Write your own explanation and unresolved questions. Downloading these files does not mark the paper as read by a researcher.

## Collection map

| Material | Local location / status |
|---|---|
| Pinned manuscript | [PDF](artifacts/papers/IT_DT_arxiv_2603.01621v1.pdf), [HTML](artifacts/papers/IT_DT_arxiv_2603.01621v1.html), [arXiv record](artifacts/metadata/arxiv_record.html) |
| Original source archive | [arXiv v1 source](artifacts/source/arxiv_2603.01621v1.source) |
| Extracted manuscript and bibliography | [Manuscript.tex](artifacts/source/arxiv_v1/Manuscript.tex), [references.bib](artifacts/source/arxiv_v1/references.bib) |
| Three original figure PDFs | [Architecture](artifacts/source/arxiv_v1/architecture.pdf), [window sensitivity](artifacts/source/arxiv_v1/fig_sensitivity.pdf), [KL timeline](artifacts/source/arxiv_v1/fig_kl_timeline.pdf) |
| Typesetting support | `artifacts/source/arxiv_v1/IEEEtran.cls`, `00README.json`; not detector code |
| Citation for this paper | [CITATION.bib](CITATION.bib) |
| Sources, byte counts, hashes and actual retrieval outcomes | [Resource manifest](../RESOURCE_MANIFEST.json) |
| Benchmark receipt and permission | [Shared acquisition status](../DATASET_ACQUISITION_STATUS.md) |

The source archive contains seven files. Its three tables are part of the manuscript, not independent experiment-output files. The bibliography is preserved as supplied; its entries and their support for claims require separate verification.

The article is **CC BY-SA 4.0** ([license](https://creativecommons.org/licenses/by-sa/4.0/)). Retain author attribution, source/version and license when using its text or figures; mark adaptations. Preserve the separate license/copyright notices in `IEEEtran.cls`. Article licensing does not grant SWaT/WADI rights or establish a detector-code license. Downloaded artifacts remain ignored local material; publication permission is a separate decision.

## What is missing

No matched author detector implementation, executable configuration, dependency lock, fitted system matrices, checkpoints, aligned scores, run logs or figure-generation scripts were verified. Exact-title/arXiv searches and a bounded check of the corresponding author's public repositories did not resolve these gaps. A TeX source archive is not experimental source code.

Raw SWaT/WADI files and access approval have not been received. Exact release identity and protocol ambiguities remain unresolved. Any later implementation written from this manuscript must be identified as **our reimplementation**, with assumptions and deviations recorded. This remains a learning paper and conditional model-based comparator, not an execution-ready baseline. See the [detailed audit](../../docs/literature/CAROTS_AND_INFORMATION_THEORETIC.md).
