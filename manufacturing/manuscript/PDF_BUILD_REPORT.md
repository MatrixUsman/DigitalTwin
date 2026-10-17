# PDF build and visual review — 17 October 2026

The [working-draft PDF](../output/pdf/correction-evidence-casper-study.pdf) is **18 A4 pages**, compiled directly from the LaTeX manuscript. Every final page was rendered and inspected. Tables, equations, plots, numbering, references and accented names are readable, with no observed clipping or overlap. Unconfirmed author declarations remain visibly pending.

## Tooling and exact build

Used the [official Tectonic 0.17.0 release](https://github.com/tectonic-typesetting/tectonic/releases/tag/tectonic%400.17.0), Apple Silicon binary. Its archive SHA-256 matched the publisher's release digest: `a3f1cac7c5678f01661a92212f58480ae3b0634115d880dbc59e2953ded45667`. Binary and resource cache stay under ignored `local/pdf_build_v0.1/`; no system package installation. TeX bundle identity: `6ffe055852f8faf66c0acbe1a7fb27f87b869a90bad1204f3bf4d9683f597c7c`.

The final build ran offline with `--untrusted` and shell escape disabled. Source hashes matched before and after compilation. The first build fetched TeX/font resources; no manuscript or dataset contents were uploaded. The separate `.venv-pdf/` uses Python 3.15.0, Pillow 13.0.0 and pypdf 6.21.0. Existing Poppler rendered pages at 120 dpi. The final compiler produced no warnings, missing-character messages, overfull boxes or unresolved references.

From `manufacturing/`:

```sh
.venv/bin/python manuscript/tools/build_pdf.py
.venv-pdf/bin/python manuscript/tools/inspect_pdf.py
.venv/bin/python manuscript/tools/verify_package.py --receipt local/pdf_build_v0.1/package_check.json
```

A changed build needs a new visual review. [Build receipt](reproducibility/PDF_BUILD_RECEIPT.json) binds source bytes, command, compiler and output. [Review receipt](reproducibility/PDF_REVIEW.json) identifies all inspected pages and the experiment-immutability checks. Logs and setup failures remain in ignored local storage; generated page previews use `tmp/pdfs/` and can be regenerated.

## Formatting corrections

Made the PGF bar-width option explicit, selected Unicode-aware fonts for XeTeX, allowed a source/configuration sentence to wrap, displayed the eight unchanged event ranges as aligned rows, and removed enlargement of naturally narrow tables. The obsolete front-page PDF-pending notice was replaced by the still-applicable author-review notice. No method, threshold, result, dataset or scientific conclusion changed. All eight numeric table/macro source files remained byte-identical, and all 52 experimental source/configuration files plus 133 frozen bindings still match.

Initial compilation stopped on an unrecognized plotting key. A subsequent nonfinal preview revealed a missing accented glyph and an overlong interval list. The inspection helper was corrected to resolve indirect PDF annotation objects. The first helper captured source hashes only after compilation; its intermediate preview receipt is explicitly not accepted as an exact binding because source edits overlapped backend completion. The final helper now verifies pre/post identities. None of these were experimental failures or model reruns.

## Review limits

This was an assistant typesetting review, not author approval, independent peer review or a new experiment reproduction. Text/structure checks passed; pypdf's optional fontTools notice limits complete extraction of one mathematical font, so equations were also visually inspected. All fonts are embedded. The pdfLaTeX branch remains untested. Contributions, affiliations, funding/conflicts, final author approval and venue requirements remain pending.

PDF SHA-256: `c849f75b14b913646b1f756e5f73cf211163dc590216db693cd0d7cb72a4bd6f`.
