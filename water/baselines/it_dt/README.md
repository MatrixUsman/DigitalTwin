# IT-DT study collection

Collected for the water project on **16 October 2026**. This is a collection of the authors' published materials and our audit notes. **No IT-DT implementation, reproduction or experiment has been performed here.**

**Verification update:** the arXiv paper and source identity are confirmed, but the [independent collection audit](VERIFICATION_REPORT.md) found a material mismatch between Figure 3's plotted score and alarm marker, an unresolved F1 arithmetic/aggregation question, and protocol/citation gaps. Keep IT-DT for critical study; it is **on hold as a numerical baseline**. Authentic files do not validate the reported experiments.

**Paper:** Inda Kreso, Mehran Tarif, Fatemeh Moradi, Iman Khazrak, Mostafa M Rezaee and Mohammadhossein Homaei, *Information-Theoretic Digital Twins for Stealthy Attack Detection in Industrial Control Systems: A Closed-Form KL Divergence Approach*. [arXiv:2603.01621v1](https://arxiv.org/abs/2603.01621v1), submitted **2 March 2026**. DOI: `10.48550/arXiv.2603.01621`. Only the preprint is verified; its arXiv DOI does not establish peer review.

## Start reading

The assistant's [method and implementation-requirements study](METHOD_TO_CODE.md) explains identification, Kalman estimation, residual distributions, KL scoring and fixed calibration. It maps equations to required inputs/state/outputs, not invented author functions. Use it with the [three-paper study guide](../../docs/PAPER_STUDY_GUIDE.md) and [mechanism comparison](../../docs/MECHANISM_COMPARISON.md), then record your own reading/questions in [the researcher record](../../papers/notes/READING_RECORD.md). Assistant reading is complete; researcher reading and understanding are unconfirmed.

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

The source archive contains seven files. Its three tables are part of the manuscript, not independent experiment-output files. The bibliography is preserved as supplied. The [reference audit](REFERENCE_CHECKS.json) matches all 28 entries to primary metadata (27 distinct works, including one duplicated reference); most adjoining claims still require full-text verification. See the [verification report](VERIFICATION_REPORT.md) for checked claims, metadata corrections and limitations.

The article is **CC BY-SA 4.0** ([license](https://creativecommons.org/licenses/by-sa/4.0/)). Retain author attribution, source/version and license when using its text or figures; mark adaptations. Preserve the separate license/copyright notices in `IEEEtran.cls`. Article licensing does not grant SWaT/WADI rights or establish a detector-code license. Downloaded artifacts remain ignored local material; publication permission is a separate decision.

## What is missing

No matched author detector implementation, executable configuration, dependency lock, fitted system matrices, checkpoints, aligned scores, run logs or figure-generation scripts were verified. Exact-title/arXiv searches and a bounded check of the corresponding author's public repositories did not resolve these gaps. A TeX source archive is not experimental source code.

The [official SWaT/WADI request](../../docs/DATASET_REQUEST_PREPARATION.md) was submitted with explicit consent and website confirmation; email delivery, approval and raw-file receipt remain unverified. Exact release identity and protocol ambiguities remain unresolved. Any later implementation written from this manuscript must be identified as **our reimplementation**, with assumptions and deviations recorded. This remains a learning paper and conditional model-based comparator, not an execution-ready baseline. See the [detailed audit](../../docs/literature/CAROTS_AND_INFORMATION_THEORETIC.md).
