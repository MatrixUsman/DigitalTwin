# ARX–RBF manuscript revision 1.7

Completed reporting revision, 19 October 2026. One 15-page paper with four figures and 22 references; no separate manuscript supplement. The requested title and Muhammad Usman byline are retained. Revision 1.6 and its 61 sealed bindings are unchanged.

The paper integrates the original 17-method audit, the separately versioned 18-method matched replay, and the newly frozen 216-episode, 11-method contextual-envelope evaluation. The original RBF criterion and the new composite criterion both fail. A measured improvement over matched contextual hysteresis does not establish an original superior detector. The user's intended original-contribution goal remains unresolved.

From the `manufacturing/` directory:

```sh
.venv-reproduction-v02/bin/python manuscript_arx_rbf_v1.7/build_pdf.py --document main
.venv-pdf/bin/python manuscript_arx_rbf_v1.7/audit.py
```

The build uses the verified existing Tectonic compiler and local cache without resource downloads. Every build attempt is preserved under `local/manuscript_arx_rbf_v1.7/pdf_build/`. `MAIN_BUILD_RECEIPT.json` binds the source files actually compiled; `AUDIT.json` records 554 passing consistency checks. `VISUAL_QA.json` binds the final PDF and individually inspected rendered pages. `SOURCE_ARCHIVE.json` checks all members of the editable single-document archive. `PACKAGE_MANIFEST.json` seals this revision and its outputs.

The source ZIP contains the LaTeX document, bibliography and figure dependencies. It does not contain the fitted models or experimental runs and is insufficient to rerun the scientific study by itself. The separately prepared local reviewer package contains executable study records; neither a public code release nor journal submission is claimed.

Evidence: `research_cycles/review_extension_v0.18/`, `research_cycles/context_recovery_v0.19/`, `NEW_EVIDENCE_ASSETS.json`, `CLAIM_LEDGER.md` and `REVISION_RESPONSE.md`. See `AUTHOR_ACTIONS.md` for actual pending human review, contribution attestation, journal-policy checks and release approval. Technical completion is not human author approval or publication readiness.

The installed PDF skill marker executed successfully once immediately before this revision was created. The academic-research-suite and PDF workflows informed source verification, claim tracing and rendered-page review; they do not constitute independent peer review.
