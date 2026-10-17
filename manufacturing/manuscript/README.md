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

## PDF stage, deferred

No TeX compiler is installed on the inspected PATH. This deliverable has **not been compiled or visually checked**. Static syntax/citation checks cannot establish page quality or even successful TeX compilation. When a project-local or approved TeX installation is available, run from this folder:

```sh
pdflatex -halt-on-error -interaction=nonstopmode main.tex
pdflatex -halt-on-error -interaction=nonstopmode main.tex
```

The main file directly inputs the generated numbered bibliography; no BibTeX run is required. `references.bib` is a companion for later venue conversion. Packages used include `lmodern`, `geometry`, `amsmath`, `amssymb`, `booktabs`, `graphicx`, `microtype`, `xcolor`, `pgfplots` with `groupplots`, `hyperref` and `xurl`. Compile without shell escape. Then check missing references/glyphs, overfull boxes, figure/table legibility, float placement and every rendered page. Do not treat the unrendered plots as publication-ready figures.

## What still needs people or new evidence

Both authors must read and explain the methods/results, verify individual contributions, approve the text and complete declarations. Select a suitable venue only after assessing contribution and evidence scope, then check its current formatting and AI-assistance requirements. The current weak findings must remain visible. Broader claims require the independent-evidence work described in the plan; that plan has not acquired data or run experiments. No publication, upload or submission occurred.
