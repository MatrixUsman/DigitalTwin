# CAROTS verification report

Audit date: **16 October 2026**. Scope: the collected CAROTS paper/source, author-code snapshot, four project guides, citation record and bibliography inventory. ARS `fact-check` / source-verification guidance was applied subject to the project rules. This is a static source audit, not execution, a full peer review, or a guarantee of correctness. Original downloads remain unchanged.

**Decision: retain for learning and as a conditional reproduction candidate. The paper and matched author repository are real, but the supplied code is not ready for our evaluation protocol.** No evidence found here establishes fabrication. Several concrete software and reporting problems require attention before a numerical comparison.

## Identity, version and provenance

| Item | Observation and evidence |
|---|---|
| Publication | The [PMLR record](https://proceedings.mlr.press/v267/kim25aa.html) confirms the exact title, six authors, ICML 2025, volume 267 and pages 30591–30608. Its citation gives 13–19 July 2025. This is a peer-reviewed conference paper, not merely an arXiv submission. |
| Separate preprint | [arXiv v1](https://arxiv.org/abs/2506.03964v1) was submitted 4 June 2025. `10.48550/arXiv.2506.03964` identifies the preprint; no proceedings DOI was supplied or invented. The author-name capitalization differs between the two official metadata records; our two citation entries preserve their respective forms. |
| Repository match | The proceedings explicitly links `kimanki/CAROTS`. The [pinned commit](https://github.com/kimanki/CAROTS/commit/63a41f45a2ae680d5cdbb2d5739e7a11264867cb) exists. The selective snapshot excludes other datasets; it is not a complete clone. The parent artifact audit separately verifies the 73 downloaded Git objects against their recorded blob IDs. |
| Rights | [Code LICENSE](vendor/author_code/LICENSE) explicitly restricts commercial use. The arXiv record links a CC BY-NC-SA 4.0 manuscript license. Neither establishes dataset permissions. |
| Updates/corrections | No correction/retraction notice appeared on the inspected proceedings/arXiv records. An exact-title correction/retraction/erratum search located no matching notice. This bounded observation is **not** a comprehensive retraction clearance. OpenReview forum access remained behind a browser challenge, so review discussions were not checked. |

The collection contains the genuine published table/figure materials rather than newly generated benchmark output. Hash/container checks establish byte integrity, not that the authors' experiments occurred exactly as described. No author code was imported or executed, and no checkpoint was deserialized.

## Audit of our extracted claims

The four guides and `CITATION.bib` were read against the local published PDF, source and pinned code. No incorrect paper identity, invented DOI, invented local data access, or invented project result was found in those guides. The following observations delimit their support.

| Guide claims | Evidence / outcome |
|---|---|
| Normal training; 20% validation; standardization; length-ten windows; batch 256; 30 epochs; three seeds; LSTM | Published PDF Section 5.1, PDF page 6; [source](artifacts/source/arxiv_v1/main.tex), lines 366–370; `config.py` confirms defaults. These describe reported practice, not a reconstructed run manifest. The actual three seed values and per-run resolved configurations are not provided in the collected result files. |
| Factor-five water downsampling, A40 hardware, validation-loss checkpoint, best F1, no point-adjusted F1 in paper | Published Appendix B, PDF page 16; source lines 549–552. The code has additional behavior below, so the prose is not proof of implementation equivalence. |
| Dataset filenames and release questions | [Loader](vendor/author_code/datasets/build.py), lines 209–249 and 266–289, supports the names in `DATASETS.md`. These strings and paper Table 7 sequence counts cannot establish original file hashes or equivalence across papers. |
| Full versus no-ensemble variant | Published Table 1, PDF page 7, and [table source](artifacts/source/arxiv_v1/table/main.tex) explicitly distinguish CAROTS and CAROTS-dagger. Both belong to one paper. The current predictor always adds the two scores; a validated dagger execution path is still needed. |
| Source inventory | All 13 `table/*.tex` files and five figure TeX wrappers are referenced by `main.tex`; the five corresponding source figure PDFs are present. The parent audit checks bytes/container validity. The source belongs to arXiv v1; this audit does not claim every source asset is pixel-identical to the proceedings version. |
| CUTS+ artifact role | [CAROTS trainer](vendor/author_code/models/carots/trainer_carots.py), lines 20–25, loads the checkpoint into `model.causal_discoverer`. [CUTS+ trainer](vendor/author_code/models/carots/trainer_cuts_plus.py), lines 381–388 and 418–427, writes causal-discovery best loss/checkpoints. `best_result.txt` is validation loss, not detector F1. The parent header-only audit observed 51×51 and 123×123 numeric graph-array shapes; this does not establish valid feature ordering or training provenance. |

## Findings that block an unchanged execution

The links below resolve to the unmodified local snapshot; online code is pinned at [the audited commit](https://github.com/kimanki/CAROTS/tree/63a41f45a2ae680d5cdbb2d5739e7a11264867cb).

| ID | Finding and consequence | Exact evidence / required response |
|---|---|---|
| C-01 — high | **Test-label threshold optimization and separate oracle F1 reporting.** Changing a threshold setting alone would leave test-selected headline F1. | [threshold.py](vendor/author_code/threshold.py), lines 28–34; [predictor.py](vendor/author_code/models/carots/predictor.py), lines 60–70 and 149–158. Implement development-only calibration and fixed-threshold precision/recall/F1 as a declared protocol change. |
| C-02 — high | **The alternative ratio threshold is statically broken.** The predictor never supplies validation scores; the branch then asserts their existence. Even if supplied, it reads `self.val_score`, while the constructor defines `self.val_scores`. | `threshold.py`, lines 22–23 and 37–41; `predictor.py`, line 60. Do not recommend switching `best_f1` to `ratio` as a ready fix. No runtime test was performed. |
| C-03 — high | **SWaT features and labels undergo different row removal.** Labels are extracted from all parsed rows, then features lose their first row. Independent median downsampling does not repair the association. | `datasets/build.py`, lines 232–249. Confirm headers against authorized originals and pair timestamp/feature/label rows before filtering. The mismatch is visible in source; its exact effect on a specific received release is not yet measured. |
| C-04 — high | **Missing-row deletion, median labels and caches complicate faithful chronology.** WADI independently drops wholly missing columns and rows in normal/test data. Median-of-five labels can erase attacks present in only one or two samples. Cached filenames encode rate but not source hash, split ratio or preprocessing revision. | `datasets/build.py`, lines 29–45, 260–290; [util.py](vendor/author_code/datasets/util.py), lines 4–15. Preserve gaps and ordered schemas, record coverage, define label aggregation explicitly, and use provenance-bound caches in processed storage. This is an inference from code, not a measured benchmark effect. |
| C-05 — high | **Test-as-validation branch exists.** | `datasets/build.py`, lines 242–245 and 282–285. Forbid `TRAIN_RATIO >= 1`. Default 0.8 takes the chronological normal-only branch; do not imply the default already leaks test labels into training. |
| C-06 — medium | **Paper/code clipping differs.** | Appendix B specifies 1.0; [config.py](vendor/author_code/config.py), line 93, sets CAROTS solver clipping to 0.5. The CUTS+ component has separate clipping settings; do not conflate them. Record the chosen implementation and deviation. |
| C-07 — medium | **Intended inference-loader flags are applied to the wrong config object.** | `predictor.py`, lines 18 and 23–29, changes cloned `self.cfg` but constructs loaders from `cfg`. [loader.py](vendor/author_code/datasets/loader.py), lines 8–11 and 25–31, consumes the original shuffle/drop-last flags. Defaults therefore retain shuffled/dropped-tail training-score passes; CL/CD training scores can be paired in different orders when added. Test loader remains unshuffled by default. Quantify impact only after a controlled adapter/test, not by assumption. |
| C-08 — medium | **Fresh and cached causal-discoverer paths use different selection behavior.** | `trainer_carots.py`, lines 20–25, loads a saved best checkpoint, but lines 29–35 copy the model after fresh CUTS+ training. `trainer_cuts_plus.py`, lines 381–390, saves best checkpoints and returns without reloading them. If the best epoch differs from the final epoch, a clean run and cached run can start CAROTS from different discoverers. |
| C-09 — medium | **Potential batch-size-one inference shape failure.** | [scorer_carots.py](vendor/author_code/models/carots/scorer_carots.py), lines 60–66, uses unconstrained `.squeeze()`. A singleton final batch can become a scalar, but `predictor.py`, lines 87–92, accepts only one- or two-dimensional scores. This is a conditional static finding; actual release-specific batch remainder is unknown. |
| C-10 — high for this machine | **CUDA and environment remain unvalidated.** | `trainer_carots.py`, lines 26/37, and common trainer preparation use CUDA. No dependency lock or tested CPU/MPS adaptation exists. Syntactic validity does not imply imports, dependencies, numerical behavior or hardware portability work. |

Other retained caveats: `config.py` enables point-adjusted output even though the paper excludes it; the unadjusted AUPRC uses trapezoidal PR integration, not average precision; script settings alone do not document hyperparameter-selection data; and upstream weights lack complete data/split/configuration provenance. Existing guides already distinguished these issues correctly.

## Published numerical and claim consistency

The reported WADI difference is genuine to the paper: Table 1 gives full CAROTS F1 **0.143** and CAROTS-dagger **0.391**. AUROC is **0.502** versus **0.622**, and AUPRC **0.056** versus **0.260**. These are published measurements, not values we reproduced. Accordingly, the broad superiority wording in Section 5.2 must not be copied as an established conclusion: for example, CARLA exceeds both variants on MSL P-15 AUPRC/F1. It is valid to study both variants; it is not valid to describe the full ensemble as uniformly better.

There is also a small internal reporting discrepancy: full CAROTS SWaT F1 is **0.791 in Table 1** and **0.792 in Table 4**. The source tables reproduce that difference, so it is not a text-extraction error. Different experimental runs or rounding may explain it, but the necessary per-run output is unavailable. Preserve each value with its table rather than silently harmonizing them. No allegation about intent follows.

The work assumes stable normal causal relations and learns predictive/Granger-style structure. Its observational graph and synthetic augmentation experiments do not independently establish the physical causal graph of a water plant, resistance to poisoned adaptation, or live deployment. Those remain questions for our study, not inherited verified capabilities.

## Bibliography coverage

[REFERENCE_CHECKS.json](REFERENCE_CHECKS.json) inventories **81 source BibTeX records**, of which **54 appear in the rendered bibliography** and **27 are unused source-library records**. Every rendered reference received a primary identity lookup attempt. **51 have scoped primary or author-deposited identity matches**; **two have primary title records but insufficient exposed metadata** (GCFormer and Granger 1969); **one remains unavailable for primary verification** (the WADI paper, whose ACM/DOI/registry retrieval failed). This is not 51 fully verified citation-support claims: some matches verify only preprint identity or author-hosted metadata while journal/proceedings details remain inaccessible. The 27 unused records were inventoried but not independently checked. Failed access is not evidence of fabrication.

Important metadata distinctions recorded in that file:

- The SWaT reference uses the CRITIS **2016 conference year**; the [publisher chapter](https://link.springer.com/chapter/10.1007/978-3-319-71368-7_8) was published **22 November 2017**. Preserve both dates when citing its version.
- Neural Granger Causality has a **2021 online / 2022 issue** distinction; CTAD has a **2023 online / 2024 issue** distinction. These do not make the papers fake.
- The [official t-SNE record](https://www.jmlr.org/papers/v9/vandermaaten08a.html) gives **9(86):2579–2605**; the supplied bibliography uses **9(11)** and omits pages. This may reflect issue/month versus article-number conventions. Use the publisher export for a future project citation; do not edit the archived bibliography.
- The PhysioNet 2017 reference misparses **Li-wei H. Lehman** as surname **Li-wei**. The [official challenge manuscript](https://physionet.org/files/challenge-2017/1.0.0/papers/065-469.pdf) supports correcting a future citation to `Lehman, Li-wei H.`. The reference exists; the problem is author-name formatting.
- RawECGNet has different displayed preprint/journal author lists. The [authors' repository citation](https://github.com/aim-lab/AFtoolkit) includes Eran Zvuloni and uses Shany Biton Brimer, corroborated by the [journal metadata in PubMed](https://pubmed.ncbi.nlm.nih.gov/38787663/). Thus the apparent preprint author discrepancy is not evidence of a fabricated journal reference. CAROTS uses the shorter name Shany Biton; use the exact cited version in our future bibliography.
- The [JAIR causal-discovery survey](https://www.jair.org/index.php/jair/article/view/13428) has [23 April 2023 errata](https://www.jair.org/index.php/jair/article/download/13428/26913) affecting an illustration, a separation-set definition and table clarifications. Consult the corrected manuscript before relying on those details. This correction concerns a cited background survey, not a CAROTS correction notice.
- The point-adjustment caution has direct support in the [AAAI evaluation paper](https://ojs.aaai.org/index.php/AAAI/article/view/20680). The other cited works were generally checked for identity, not all their experimental findings or every sentence they support.

This is deliberately a coverage statement, not an “all references verified” certificate. Before citing a particular source in our paper, inspect the exact version and passage for our intended claim. Remaining metadata resolution and a comprehensive claim-support audit are separate from confirming this resource pack's provenance.

## Changes made and limits

Added this report and the reference inventory; linked them from the reading pack and expanded its pending-execution notes. No downloaded paper, author bibliography, source code or weights were changed. Existing correct protocol warnings were retained. The parent audit handles all-resource hashes, PDF/container readability and local-link/syntax checks; those are software/artifact checks, not benchmark validation.

No data were loaded, author functions run, packages installed, experiments performed, authors contacted or files published. Next: learn the model with these findings visible, then prepare a proposed adaptation/deviation specification and synthetic loader/metric tests once implementation is authorized. Dataset permission and exact-release matching remain unresolved.
