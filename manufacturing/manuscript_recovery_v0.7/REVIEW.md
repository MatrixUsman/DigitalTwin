# Scoped manuscript review — 17 October 2026

Performed inline by the same Codex agent using academic-research-suite claim/source and experiment guidance, plus the PDF render/inspect workflow. This is **not external peer review**, an independent research team review or a human-author reading attestation.

| Check | Outcome |
|---|---|
| Question, trust boundary and available information | Explicit protected approved commands, truthful noisy sensing, downstream command changes; detector cannot see schedule, true state or actual plant parameters |
| Contribution statement | Full primary failure and unestablished algorithm novelty stated in abstract, results and conclusion; no paper-faithful baseline or physical safety claim |
| Comparison completeness | All 23 methods included, with stable IDs, equal-budget and matched-entry tracks distinguished; saved incompatible IMU CNNs retained separately |
| Metric interpretation | Command-label F1 distinguished from benign-only burden and evaluator return; unknowns, misses, conditional delays and absent fresh onsets retained |
| Component inference | Dwell effect at fixed entry threshold reported; exact equality of entry ablation checked; co-varying plant parameters not described as isolated lag causality |
| Source support | Nine cited keys resolved; five local primary source/metadata files hashed; remaining partial-access limits explicit; CASPER venue corrected from the frozen v0.5 note |
| Numerical traceability | Generated tables/figures read saved JSON/arrays; key numerical claims asserted in `audit.py`; complete outcome CSV and 92-row aggregate retained |
| Provenance | Ten scientific sources and 809 prior inputs preserved; old model bytes unchanged; normal and score seals retain the chronology; one scientific attempt |
| Authors and AI | Names/order supplied; Muhammad Usman’s supplied COMSATS Sahiwal affiliation recorded; Haiqa’s affiliation/individual roles/funding/conflicts unconfirmed; substantive AI involvement disclosed; no unsupported human approval statement |
| Journal decision | ISA Transactions conditionally fits the subject and simulation-analysis route; originality/author readiness gate remains open; no acceptance/ranking/fee assertion |

## PDF review

The completed PDF has **17 pages**. All pages were rendered with Poppler at 85 dpi and visually inspected in nine two-page/one-page spreads, covering title/abstract, equations, tables, figures, appendices, declarations and all references. No clipped content, overlapping text, missing symbols, table overflow or unresolved citations was observed. The TeX log has no overfull-box, missing-character or undefined-reference warnings. Data plots were additionally inspected as PNGs. Render paths and final PDF hash are bound in `PDF_QA.json`.

Preserved build attempts:

1. Offline attempt 001 failed because a sans-serif math-transpose font was not cached. Replaced the transpose glyph with standard mathematical `\top`; scientific meaning unchanged.
2. Offline attempt 002 reached PDF generation but lacked `cmr7.pfb`.
3. Resource-download attempt 003 failed DNS resolution inside the sandbox. No manuscript content was uploaded.
4. Approved compiler-resource retrieval completed attempt 004 using the existing local compiler and a separate project cache. Only missing compiler resources were retrieved; no system install occurred.
5. Attempt 005 successfully rebuilt the complete PDF offline.
6. After the user requested assistant-drafted declarations, attempt 006 rebuilt offline with Muhammad Usman’s previously supplied affiliation and explicit unconfirmed statements for unknown personal facts. Changed pages were rendered and inspected; unchanged pages were compared pixel-for-pixel to the inspected version.
7. Attempt 007 made the final layout refinement to keep individual references from splitting across pages. It rebuilt offline; the two changed reference pages were inspected. All 17 final pages are covered by visual review or exact unchanged-render comparison.

These are document-production failures, not experiment retries. Scientific sources and frozen results were unchanged. The exact original-contribution claim remains scientifically unfinished; this report must not be interpreted as approving a novel-method submission.
