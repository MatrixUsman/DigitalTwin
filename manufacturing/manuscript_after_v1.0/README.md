# Consolidated AFTER manuscript

17 October 2026. One polished, 14-page LaTeX/PDF manuscript consolidating the completed recovery v0.8 and commissioning v0.9 studies. The output is [AFTER-manuscript.pdf](../output/pdf/AFTER-manuscript.pdf); editable source is [main.tex](main.tex).

This is an author-review/submission draft, not an accepted paper or evidence that the original novel-detector objective has been achieved. It presents the measured limitation, matched controls, normal-only reference improvements and conditional noise analysis. The uncertainty-addition candidate's failed primary criterion remains explicit. AFTER is the existing proposed title, not a new algorithm or a confirmed final author title. No journal template compliance is claimed.

The abstract, argument and conclusion were rewritten around both completed studies. Six tables and two vector figures derive from sealed JSON artifacts. All 13 attack-study methods and all distinct normal-reference roles remain visible. No additional model was fitted, no simulation ran, and no dataset was opened for new analysis.

## Rebuild from the workspace root

```sh
manufacturing/.venv-plots-v03/bin/python manufacturing/manuscript_after_v1.0/present.py
manufacturing/.venv-reproduction-v02/bin/python manufacturing/manuscript_after_v1.0/build_pdf.py
manufacturing/.venv-pdf/bin/python manufacturing/manuscript_after_v1.0/audit.py
```

The builder uses the existing verified Tectonic compiler and cached resources offline. Each build attempt is preserved under `manufacturing/local/manuscript_after_v1.0/pdf_build/`. The first attempt failed because a 7-point math font was absent from the cache; using the already available 8-point subscript font resolved it without downloading or changing packages. An initial presentation-script syntax error was corrected before any figure or table was generated. No scientific input changed.

`PRESENTATION.json` records result and presentation hashes; `BUILD_RECEIPT.json` records the compiler, exact command and PDF hash; `AUDIT.json` records integrity, citation and numeric checks. All rendered pages were inspected, with final renders kept in ignored local QA storage. [CLAIM_EVIDENCE.md](CLAIM_EVIDENCE.md) and [REFERENCE_AUDIT.md](REFERENCE_AUDIT.md) explain claim support and source limitations.

Before submission, both authors must review the text and confirm affiliations, actual contributions, funding and conflicts. A scientific contribution assessment and a compatible journal decision remain separate from editorial completion. Do not remove necessary factual qualifications, invent declarations or treat this draft as proof of a successful replacement mechanism. The intended original-contribution direction remains active. No upload, publication or Git mutation was performed for this deliverable.
