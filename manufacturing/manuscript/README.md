# Manufacturing manuscript — local working draft

**Correction Evidence in Robotic Motion Monitoring: A Controlled CASPER Study**

Authors in the user-supplied order: **Muhammad Usman; Haiqa Mushtaq**. This is a LaTeX draft of the completed eleven-method study, not a submitted paper. Affiliations, actual contributions, funding, conflicts, corresponding author and both authors' final approval remain pending. The title describes the measured case study; novelty, broad cybersecurity effectiveness and a validated physical twin are not established.

Start with [main.tex](main.tex), [the findings explained](../docs/FINDINGS_EXPLAINED_V0.1.md) and [the independent-evidence plan](../docs/POST_EXPOSURE_INDEPENDENT_EVIDENCE_PLAN_V0.1.md). The original holdout is exposed. Changes motivated by its outcomes are exploratory; rerunning or reshuffling it does not create fresh confirmation.

## What is included

- `sections/`: introduction, close related work, threat/data scope, equations, evaluation, all results, limitations, conclusion, declarations and appendices. The abstract was drafted after the results and conclusions.
- `generated/` and `figures/`: deterministic tables, numerical macros and two PGFPlots figures from frozen aggregate results. No copied third-party figures, raw trajectories or synthetic benchmark results.
- `editorial/`: source verification, a 65-group claim/evidence map, 13-reference register, author/release questions and an explicitly internal review.
- `reproducibility/`: exact tested source/configuration copies, historical scientific specifications, aggregate outcomes and immutable identities. Raw datasets, vendor code/PDFs, fitted models and row-level scores are not redistributed.
- `tools/`: offline asset generation and static package validation. These tools do not train or replay a model.

## Rebuild and check presentation assets

From `manufacturing/`, using the existing isolated interpreter:

```sh
.venv/bin/python manuscript/tools/build_assets.py --check
.venv/bin/python manuscript/tools/verify_package.py --receipt local/manuscript_v0.1/package_check.json
```

Without `--check`, `build_assets.py` regenerates the presentation files from the saved JSON. After an intentional prose edit, review the affected claim span/evidence and update the registry before accepting a new check; never silently replace a result. See [reproduction levels](reproducibility/README.md) and [commands/dependencies](reproducibility/REPRODUCE.md).

## PDF build and review

The [18-page PDF](../output/pdf/correction-evidence-casper-study.pdf) has been compiled and visually inspected. [PDF_BUILD_REPORT.md](PDF_BUILD_REPORT.md) records the exact source/output identities, isolated tooling, fixes and review limits. This is a working draft; author declarations remain pending.

The pinned Tectonic 0.17.0 compiler and TeX cache are in ignored `local/pdf_build_v0.1/`; the separate `.venv-pdf/` contains rendering/inspection dependencies. No system package was installed. From `manufacturing/`, rebuild using the cached resources without network access:

```sh
.venv/bin/python manuscript/tools/build_pdf.py
.venv-pdf/bin/python manuscript/tools/inspect_pdf.py
```

A changed PDF needs a new page inspection. Initial resource downloads require the explicit `--allow-resource-downloads` option and appropriate network access. The compiler runs with `--untrusted` and shell escape disabled. Source hashes are checked before and after compilation. The inspected PDF is not an independent scientific review or a submission-ready declaration.

The main file directly inputs the generated numbered bibliography; no BibTeX run is required. `references.bib` is a companion for venue conversion. Unicode font support is selected for XeTeX; a pdfLaTeX branch remains in the source but has not been compiled here. The original static-package receipt and writing passport are historical; the separate PDF receipts record this completed stage.

## What still needs people or new evidence

Both authors must read and explain the methods/results, verify individual contributions, approve the text and complete declarations. Select a suitable venue only after assessing contribution and evidence scope, then check its current formatting and AI-assistance requirements. The current weak findings must remain visible. Broader claims require the independent-evidence work described in the plan; that plan has not acquired data or run experiments. No publication, upload or submission occurred.
