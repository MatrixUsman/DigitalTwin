# AFTER manuscript, revision1.1

Completed neutral-format manuscript with **Muhammad Usman** as sole listed author. The current deliverable is `manufacturing/output/pdf/AFTER-Muhammad-Usman.pdf`. The title is retained from the previous draft; it names the investigation rather than a newly validated detector.

This revision integrates the completed covariance-aware return-bound diagnostic and common-input CASPER-style training study with the earlier attack/recovery and commissioning results. Eight tables and four vector figures derive from saved artifacts. Funding/conflict declarations follow the user's confirmation. The AI-assistance declaration is factual. Historical evidence and author records remain unchanged.

`main.tex` is the entry point; `sections/`, `generated/` and `figures/` contain its inputs. The bibliography is embedded for a self-contained build; `references.bib` supplies equivalent entries for journal-template conversion. Compile with XeLaTeX (multiple passes) or Tectonic. The source ZIP can be edited independently of the experiment storage. It contains no raw dataset or fitted model.

Local generation/build/audit commands from workspace root:

```sh
manufacturing/.venv-plots-v03/bin/python manufacturing/manuscript_after_v1.1/present.py
manufacturing/.venv-reproduction-v02/bin/python manufacturing/manuscript_after_v1.1/build_pdf.py
manufacturing/.venv-pdf/bin/python manufacturing/manuscript_after_v1.1/audit.py
```

Build attempts are preserved under `local/manuscript_after_v1.1/pdf_build/`. Attempt001 failed because an italic8-point font was not cached; a math-only equivalent avoided that dependency. Attempt002 compiled but visual review identified sparse forced pages and an underfull line. Attempt003 failed on a9-point footnote font; an ordinary inline provider link avoided it. Attempt004 compiled offline after typography changes. No font/package was installed or downloaded, and no scientific parameter changed.

The final PDF has 20 pages. All pages were rendered and visually inspected; the final TeX log has no overfull/underfull boxes, undefined references or missing characters. `AUDIT.json` records 2,461 successful editorial/evidence checks, including all prior scientific package hashes, numerical claim arithmetic, source/presentation/build identities, citation order and the sole-author metadata. `VISUAL_QA.json` binds the reviewed page renders. These checks are not independent scientific peer review.

The standalone editable source is `manufacturing/output/AFTER-Muhammad-Usman-source.zip`. `package.py` builds it from an explicit source-only whitelist and seals the current revision, final PDF and archive. It excludes raw observations, fitted models, third-party manuscripts and private environment/run storage. The archive is a typesetting package; the complete local experiment history remains separate.

Read [submission notes](SUBMISSION_NOTES.md), [claim evidence](CLAIM_EVIDENCE.md), [reference audit](REFERENCE_AUDIT.md) and [revision scope](EDITORIAL_SCOPE.md). This is the completed manuscript revision, not a publication-readiness guarantee, proof of original-detector superiority or final human approval. No submission/publication occurred.
