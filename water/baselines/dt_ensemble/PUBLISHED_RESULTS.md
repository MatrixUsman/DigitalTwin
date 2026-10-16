# Ensemble published results and asset index

**Verification update — 16 October 2026:** [The source audit](VERIFICATION_REPORT.md) confirms the publication identity but finds material mathematical, metric, citation and protocol issues. Keep this paper on experimental hold; published claims remain unvalidated.
**These are Sayghe, Alahmadi and Gharawi's published claims and assets, not measurements from our project.** No result has been reproduced. Preserve attribution to the [Scientific Reports article](https://www.nature.com/articles/s41598-026-53863-z), DOI `10.1038/s41598-026-53863-z`, version of record **27 July 2026**, under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), subject to third-party exclusions.

Use the [local VOR PDF](artifacts/papers/Ensemble_ScientificReports_VOR.pdf) for the complete presentation. The official PMC XML, plain text and media are in `artifacts/pmc/`; the [extraction index](artifacts/extracted/INDEX.json) maps local tables, captions and references to source IDs. The [resource manifest](../RESOURCE_MANIFEST.json) records actual files, sources and hashes. Extracted copies are derivatives of the article, not released experimental output. Plain-text extraction flattens table structure; consult the PDF or XML for cell/column boundaries.

## Tables

| Number / XML ID | Contents |
|---|---|
| [Table 1 / `Tab1`](artifacts/extracted/tables_01.xml) | Hyperparameters, seeds, training/inference batch settings and stated tuning budget |
| [Table 2 / `Tab2`](artifacts/extracted/tables_02.xml) | Dataset characteristics |
| [Table 3 / `Tab3`](artifacts/extracted/tables_03.xml) | SWaT detection metrics and latency comparison |
| [Table 4 / `Tab4`](artifacts/extracted/tables_04.xml) | Component-removal ablations |
| [Table 5 / `Tab5`](artifacts/extracted/tables_05.xml) | Component latency breakdown |
| [Table 6 / `Tab6`](artifacts/extracted/tables_06.xml) | Reported resistance to added adversarial attacks |
| [Table 7 / `Tab7`](artifacts/extracted/tables_07.xml) | Added attack configurations and evaluation definition |

Table 3 reports SWaT precision **97.6%**, recall **96.2%**, F1 **96.9%** and latency **25.4 ms**. Figure 3 reports F1 **96.9% on SWaT**, **95.3% on WADI** and **94.7% on Tennessee Eastman**. These literature values are not comparable to another paper's headline scores without reconciling releases, splits, labels, thresholds and metrics. Separate model evaluation across datasets does not by itself establish transfer without retraining.

Do not use these numbers as optimization targets or evidence of our method's expected performance. The paper's latency metric also must not be substituted for attack detection delay.

## Figures and algorithm

All files below are in `artifacts/pmc/` and are original PMC-distributed article media.

| Locator | Filename | Contents |
|---|---|---|
| Algorithm 1 / `Figa` | [Algorithm image](artifacts/pmc/41598_2026_53863_Figa_HTML.jpg) | Detection-pipeline pseudocode |
| Figure 1 / `Fig1` | [Architecture](artifacts/pmc/41598_2026_53863_Fig1_HTML.jpg) | Physical plant, twin, ML ensemble and fusion architecture |
| Figure 2 / `Fig2` | [Latency](artifacts/pmc/41598_2026_53863_Fig2_HTML.jpg) | Relative and absolute component inference latency |
| Figure 3 / `Fig3` | [Dataset comparison](artifacts/pmc/41598_2026_53863_Fig3_HTML.jpg) | Reported F1 and uncertainty across three datasets |
| Figure 4 / `Fig4` | [Noise sensitivity](artifacts/pmc/41598_2026_53863_Fig4_HTML.jpg) | Reported detection and false-positive behavior versus signal-to-noise ratio |

The figures are rendered publication assets. No underlying plotting arrays, seeds-to-output mapping, per-sample scores, complete logs or plot-generation scripts were verified. No supplementary-material elements occur in the inspected PMC XML. These absence statements concern this inspected public collection, not all materials the authors may hold.

## References and version handling

- [Publisher bibliography RIS](artifacts/references/author_bibliography.ris), [extracted reference text](artifacts/extracted/references_01.txt) and PMC XML preserve **31 references**. Each remains a lead requiring separate identity and claim-support verification before reuse.
- [Publisher citation RIS](artifacts/references/paper.ris) and [CITATION.bib](CITATION.bib) identify this paper.
- Keep `artifacts/papers/Ensemble_accepted_manuscript.pdf` distinct from the current VOR. Do not silently merge wording, table values or protocols across versions.
- The current Data availability text withholds experimental results/trained models and promises code. Saving publication tables does not close that reproducibility gap. See [EXPERIMENTS.md](EXPERIMENTS.md).
