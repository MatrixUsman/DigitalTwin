# Ensemble verification report

Audited **16 October 2026**, using the installed research skill's bounded fact-check/source-verification workflow and the project's stricter primary-source rules. This is an evidence audit, not a reproduction, accusation of misconduct, or guarantee that every statement in the paper is correct.

**Decision: authentic publication; material scientific and bibliographic problems; retain for critical reading, keep numerical reproduction on hold.** The downloaded files represent the identified article. Authentic provenance does not validate its experiments. The article's results cannot presently be independently checked because matched implementation, exact dataset preparation and underlying experimental outputs remain unavailable.

## Identity, versions and status

- [Publisher article](https://www.nature.com/articles/s41598-026-53863-z), DOI `10.1038/s41598-026-53863-z`, *Scientific Reports* 16, article 23318, and the three authors agree with the local PDF, PMC XML and [Crossref record](https://api.crossref.org/works/10.1038%2Fs41598-026-53863-z). `CITATION.bib` is consistent with those records.
- Publisher history: received 2025-10-13; accepted 2026-05-14; published 2026-05-22; version of record 2026-07-27. The accepted PDF and VOR are distinct versions of one article. Both inspected versions already contain the normal-only tuning clarification, 10 Hz statement, problematic smoothing radius, and incorrect reference DOIs discussed below. The text's mention of a previous manuscript version does not identify a separate published correction.
- The article is a journal research article under the publisher's [peer-review policy](https://www.nature.com/srep/journal-policies/peer-review). Its individual review reports were not available in this audit. Peer review is not a correctness certificate.
- Current publisher page has no correction/retraction notice found; refreshed [PMC metadata](https://pmc-oa-opendata.s3.amazonaws.com/PMC13402577.1/PMC13402577.1.json) reports `is_retracted: false`; Crossref has no `update-to` record in the inspected response. This is a dated, bounded status check, not proof no concern exists elsewhere.
- CC BY 4.0 is present in publisher/PMC license text, subject to credit-line exclusions. It does not grant rights to the datasets or unreleased software.

## Coverage of our four guides and citation

The audit read `README.md`, `DATASETS.md`, `EXPERIMENTS.md`, `PUBLISHED_RESULTS.md` and `CITATION.bib` against the actual VOR PDF/XML and relevant accepted-manuscript passages. Local assertions about missing code/data were also rechecked against the public sources. Instructions and proposed future procedures are not empirical claims.

| Guide claim group | Source anchor and outcome |
|---|---|
| Authors/title/venue/identifier/dates/license/PMC identifiers | Publisher history, PMC front matter and refreshed metadata agree. No correction needed in our citation. |
| Seven tables, four numbered figures plus algorithm, 31 references, no supplementary element | Counted in the actual XML: 7 `table-wrap`, 5 `fig` (including `Figa`), 31 `ref`. Correct. This is inspected-package coverage, not proof all author materials are public. |
| SWaT 51/11 days/946,722; split 634,374/86,065/226,283; WADI 123/16 days/1,221,370/15; TE 52/20 faults/825,000/48 h | Table 2 and experimental setup, VOR pp. 8–9. Correct transcriptions of author claims, not verified dataset measurements. SWaT split sums to its stated total. External consistency remains unresolved below. |
| Day/hour split assignments; 10 Hz; window 50 samples/5 seconds; preprocessing | Setup, Table 1 caption and synchronization/data-preparation passages. Correct transcriptions. Not sufficient to reconstruct the data pipeline. |
| Twin, EKF, detectors, fusion, normal-only tuning, certified-normal adaptation and seven-day buffer | Methods, Equations 4–17 and update paragraphs, VOR pp. 4–8. Our guides accurately distinguish state correction from parameter/calibration updates. Implementation and admission rule remain missing. |
| 500 TPE trials/48 h single A100; eight-A100 DGX; Python 3.9.7/TensorFlow 2.11.0/PyTorch 1.13.0/MATLAB R2023a; ten listed seeds; batch 64/1 | Setup and Table 1 with its caption. All correctly copied. TPE versus Gaussian-process wording remains inconsistent. These are not installed dependencies or locally executed configurations. |
| SWaT 97.6/96.2/96.9%, 25.4 ms; WADI/TE F1 95.3/94.7% | Table 3 and Figure 3 caption. Correct transcriptions of published values. No run outputs validate them. |
| Table and media labels; no score arrays, plots scripts, models or complete logs found | XML inventory and availability paragraph agree. Publication tables/figures are not experiment outputs. |
| Table 3 FPR equals 100% minus precision | Recomputed for all six rows. Pattern confirmed, but the computation actually used cannot be established from rounded means alone. |

Our extracted guides did not invent the principal reported numbers. The important corrections are to confidence in the source: the following errors and gaps must accompany any future use. Links to this report have been added to all four guides; original publisher files and bibliography remain unchanged.

## Scientific consistency findings

| ID | Finding and exact source | Consequence |
|---|---|---|
| E01 — material mathematical error | Equation 7 defines `s = (rᵀ S⁻¹ r)/m`, then describes `s` as chi-square with `m` degrees of freedom (VOR p. 4). For a zero-mean Gaussian innovation with correctly specified covariance, the **unscaled** quadratic form has that distribution; `s` instead follows `chi-square(m)/m`. | The claimed analytical calibration needs the scaling corrected and its distributional assumptions validated. This does not reveal which scaling an unreleased implementation used. |
| E02 — material mathematical/citation error | The paragraph after Equation 17 (VOR p. 6) substitutes sigma=.02, pA=.95 and pB=.05 into `sigma/2*(Phi^-1(pA)-Phi^-1(pB))` and states radius approximately .05 for the infinity norm. Direct evaluation gives **0.03289707253902944**. [Cohen et al., Theorem 1](https://proceedings.mlr.press/v97/cohen19c/cohen19c.pdf), p. 3, gives an **L2** guarantee under Gaussian smoothing, not that stated infinity-norm guarantee. | Both the arithmetic and norm claim require correction. A conservative conversion to an infinity-norm radius requires the input dimension (`R/sqrt(d)`); .05 is not justified by the displayed argument. The article does not supply the required probability-bound certification artifacts. |
| E03 — inconsistent noise description | Contributions/conclusion call smoothing autoregressive, while Equation 17 specifies covariance `sigma² I`. | A temporal noise model and its corresponding certificate are missing. Do not import the claimed robustness guarantee. |
| E04 — material metric question | All six Table 3 FPR entries equal `100 − precision`: 12.7, 10.5, 6.8, 5.2, 11.4 and 2.4 percent. Standard FPR is `FP/(FP+TN)`; the complement of precision is `FP/(TP+FP)`. | Needs confusion counts, per-seed scores and denominator definitions. Pattern alone is not proof of how the authors calculated the metric. Table 3 cannot currently establish a standard FPR comparison. |
| E05 — dataset/protocol conflict | Setup assigns SWaT day 8 normal-only validation and all 41 attacks to days 9–11 (VOR p. 8). [Provider December-2015 description](https://www.sutd.edu.sg/itrust/itrust-labs/datasets/dataset-characteristics/swat/) has seven normal days followed by four attack days; [the cited dataset paper](https://link.springer.com/chapter/10.1007/978-3-319-71368-7_8) agrees. | No release/filtering/timestamp manifest reconciles the accounts. It is a reproduction blocker, not proof the data were fabricated. |
| E06 — sampling/count mismatch needing explanation | VOR pp. 4/9 describes 10 Hz, while 946,722 samples over 11 continuous days is about .996 Hz; a complete 10 Hz stream over 11 days would have 9,504,000 samples. WADI/TE totals also do not establish a common 10 Hz stream. | Missing resampling/coverage protocol. Do not interpret a 50-sample window as five seconds in our evaluation until actual timestamps and transformations justify it. |
| E07 — arithmetic caption error | Figure 3 caption (VOR p. 13) labels WADI→TE change as 2.2 percentage points; `95.3−94.7 = 0.6`. The 2.2 difference is SWaT→TE. | Caption error; does not itself disprove the plotted F1 values. |
| E08 — ambiguous attack count | Table 2 lists 41 SWaT attacks, 15 WADI attacks and 20 TE fault conditions, while abstract/conclusion says 56 scenarios across three datasets. `41+15=56`; including 20 faults gives 76 conditions, but faults are not automatically attacks. | Clarify the denominator and separate cyberattacks from process faults. |
| E09 — incomplete formal/online specification | Equation 15 asserts an estimator bound without a derivation, sample complexity or stated assumptions sufficient to imply the claimed detection guarantee. `always eventually response` in the LTL passage does not express a finite response deadline. Certified-normal admission and order of updates relative to scoring are not fully defined. | Claimed guarantees, finite safety deadlines and contamination resistance cannot be accepted from these statements alone. These are limitations of the supplied specification, not results of a formal verification run. |
| E10 — comparison identity problem | Table 3's `LSTM` row cites ref. 18, TABOR; the [author's thesis chapter reproducing TABOR](https://pure.tudelft.nl/ws/portalfiles/portal/56228536/phd_thesis_proof.pdf), Chapter 6, describes timed automata and Bayesian networks. Intro/related work also use refs. 17/18 to attribute RNN/LSTM accuracy. Ref. 17 is the SWaT dataset chapter. | The citation does not identify the LSTM implementation reported in the table. Require exact baseline code/configuration; do not treat that numerical row as a reproduced TABOR or a verified LSTM comparison. The 93% RNN statement was not supported by the inspected dataset abstract; full-text support remains unverified. |

Other arithmetic checks passed: all six F1 values in Table 3 agree with the displayed precision/recall after rounding; Table 4 differences, Table 5 latency sum/rounded percentages, and Table 6 improvements are internally consistent. Passing arithmetic does not verify measurement authenticity. Confidence intervals, 10-seed repeatability, attack generation, runtime and hardware claims cannot be independently validated without outputs.

## Bibliography audit: all 31 entries

[REFERENCE_CHECKS.json](REFERENCE_CHECKS.json) holds each printed entry, identifier checks, source URL, metadata and manual decision. Raw public metadata responses are retained under ignored `artifacts/verification/`. Crossref publisher deposits were inspected directly; title, author and venue/date fields were compared, rather than using a fuzzy title score. DOI lookup 429 responses were retried successfully. Failed or incomplete lookups are not classified as fabricated.

**29 cited works have an identified primary/provider/author-deposited record, including entries with incorrect citation fields. Two remain partial:** ref. 3's exact 2024 statistics version was inaccessible; ref. 27 has a matching author-uploaded manuscript but its claimed publisher/volume/review status remains unverified. This does **not** mean 29/31 claims are verified.

| Ref | Identity decision | Important detail |
|---|---|---|
| 1 | Identified; author list incomplete | Berkeley author record lists six authors; citation lists only Cárdenas without `et al.`. |
| 2 | Identified | Crossref has a title-word-order typo; Miller/Rowe, venue, pages and DOI match. |
| 3 | Partial/inaccessible version | Statista URL found; exact Vailshery 2024 edition and 75-billion-IIoT claim not verified. |
| 4–10 | Identified | Publisher-deposited title/authors/venue/year match. Individual underlying results were not replicated. |
| 11 | Identified; underspecified citation | IEC identifies **TS 62443-6-2:2025**, published 2025-01-21, as the evaluation methodology for 62443-4-2. Full standard was not purchased/read. |
| 12 | Identified; bibliographic error | Real Grieves chapter, DOI `10.2514/5.9781624105654.0175.0200`, in *Complex Systems Engineering: Theory and Practice*, pp. 175–200, AIAA. `Theory and Practice` is not its publisher. |
| 13 | Identified; wrong DOI and authors | Correct DOI **10.1109/MSEC.2023.3271225**. Nine authors, with Allison third; Weippl is absent. Printed `10.1109/MSEC.2023.3285929` did not resolve in Crossref. Author arXiv 2305.00639 and institutional record corroborate the corrected identity. |
| 14–15 | Identified | Matching publisher-deposited records. Ref. 14's other paper/code is not the ensemble implementation. |
| 16 | Identified; minor initial difference | Crossref gives S.R. Rahman; article shortens to S. Rahman. Metadata existence does not certify the study's quality or claims. |
| 17–23 | Identified | DOI metadata match (TranAD/TABOR expanded titles are stored as title plus subtitle). Citation support concerns for refs. 17/18 are separate from identity. |
| 24 | Identified intended paper; **wrong unrelated DOI** | Cohen/Rosenfeld/Kolter ICML 2019 paper verified in [PMLR](https://proceedings.mlr.press/v97/cohen19c.html). Printed DOI `10.1007/s12110-009-9068-2` identifies **Assortative Pairing and Life History Strategy**, Figueredo/Wolf, *Human Nature* (2009). Do not reuse that DOI. |
| 25 | Identified | Matching Automatica record. Actual null-space attack assumptions still require their own reading. |
| 26 | Identified intended paper; **wrong DOI** | Publisher DOI is **10.1038/s41598-025-01933-z**. Printed `10.1038/s41598-025-12345-6` did not resolve in Crossref. PMC separately adds the correct identifier; this is not an extraction invention. |
| 27 | Partial | Matching Asad Yaseen author-uploaded manuscript on ResearchGate; no matched primary publisher issue record established. A text search did not substantiate the cited 67% LLM exploit-code figure. Do not treat absent search hits as proof the manuscript is nonexistent. |
| 28–31 | Identified | IEEE/Elsevier/ACM deposited records, and USENIX's own PBFT proceedings page, establish identity. They do not establish the ensemble paper's claimed numerical comparisons. |

The bibliography's original XML/RIS/text was deliberately preserved. Corrections belong in this audit or a future independently checked bibliography, not silently inside downloaded sources. Ref. 24's misuse also affects replay-attack attribution: a computer-vision smoothing theorem is not a source for the paper's stated replay-residual behavior.

## Code and experimental readiness

The publisher still promises code while withholding result files/models. The public `asayghe1` account was rechecked (16 repositories), alongside exact-title/DOI search and prior mapped repository descriptions. No repository was verified as implementing this specific paper. This bounded negative search is not proof no implementation exists privately or elsewhere. No code, weights, dataset or untrusted serialization was executed.

Keep this paper as closest-mechanism prior art and a critical-reading exercise. **Do not copy its formulas, confidence claims, bibliography, FPR column or headline scores into our methodology/results without resolving the issues.** It is not presently an execution-ready comparator. No author/provider was contacted, no dataset access was obtained, and no training or paid compute occurred.

## Reproducibility of this audit and limits

Working directory: workspace root. Public metadata was read with Python 3.15 stdlib `urllib.request`/`json` and primary-source web browsing; source tables parsed with `xml.etree.ElementTree`; arithmetic used `statistics.NormalDist().inv_cdf`, ordinary sums and the harmonic mean. Audit source inventory and hashes are in [VERIFICATION_ARTIFACTS.json](VERIFICATION_ARTIFACTS.json). Newly retrieved metadata is separate from the existing collection manifest. Sources and access date are included per reference; no secrets or restricted datasets were used.

The parent audit checks collection-wide hashes/readability/extractions. This subaudit covers every factual/numeric claim group in our four guides and citation, all 31 reference identities, and selected material scientific/citation-support issues in the manuscript. It is not a theorem-by-theorem proof, full peer review of 31 cited works, comprehensive misconduct investigation, or empirical validation of the paper. Human researchers still need to read and defend their own summaries.
