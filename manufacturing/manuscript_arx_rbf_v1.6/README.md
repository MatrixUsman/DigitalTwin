# ARX–RBF manuscript, revision 1.6

Title: **ARX–RBF Motion Modeling for Cyberattack Detection and Recovery Monitoring in Industrial Robots**. Requested sole byline: Muhammad Usman, COMSATS University Islamabad, Sahiwal Campus, Pakistan. Neutral journal format, one article with all supporting sections inside it; no separate supplement.

This revision adds measured five-fold chronological validation of the proposed ARX–RBF model and its ARX control, official-model-code ModernTCN/iTransformer/TimeMixer runs on common normal IMU targets, explicit recent-paper correspondence and a moderately expanded conclusion. Prior simulation findings, including the failed primary improvement criterion, remain unchanged. The previous manuscript packages are preserved.

## Reading the comparisons

- The simulated robot track evaluates protected-command references, attack detection and physical return under the declared trust assumptions.
- The real IMU track compares normal prediction on an already-used nominal recording. The new three-seed runs use unchanged author model classes under a modified forecasting protocol and finite CPU budgets. They do not reproduce the papers' original benchmarks or establish attack performance.
- The five folds are expanding chronological refits on existing synthetic commissioning episodes, with earlier-selected settings. They are retrospective stability diagnostics, not independent attack confirmation or nested model selection.
- MVT-Flow remains an unexecuted offline candidate. Its independent public process signals and original test outcomes were not accessed in this revision.

`RECENCY_AND_CORRESPONDENCE.md`, `REVISION_RESPONSE.md`, the claim/reference ledgers and the two study packages describe the boundaries in detail. The bibliography retains 20 works, including 18 cited versions from 2024–2026; the two older works are mathematical background. Classical controls remain useful independently of publication recency.

## Compile the standalone source archive

Unpack the archive into a new directory and run `pdflatex main.tex` twice with a normal LaTeX installation containing the packages listed in the preamble. The bibliography is already rendered in `references.tex`; `references.bib` retains the metadata. All input files and included vector figures are present. No external dataset, compiler download or training is required to compile the article.

Within the original workspace, the recorded offline build uses the existing verified Tectonic installation:

```sh
.venv-reproduction-v02/bin/python manuscript_arx_rbf_v1.6/build_pdf.py --document main
.venv-pdf/bin/python manuscript_arx_rbf_v1.6/audit.py
```

Run these from the manufacturing project directory. The archived standalone package contains the manuscript dependencies; the workspace holds the build/audit tooling and complete scientific records.

## Evidence and release state

`MAIN_BUILD_RECEIPT.json` binds the actual PDF to its source. `FORECAST_ASSET_RECEIPT.json` binds the new table and prose to verified saved outcomes. `AUDIT.json`, `VISUAL_QA.json`, `SOURCE_ARCHIVE.json` and `PACKAGE_MANIFEST.json` record the final checks and hashes. The review is performed by the same assistant, not an independent scientific replication.

No journal submission or public release is claimed. The AI-assistance disclosure is retained. Final human authorship/contribution review, manuscript approval and a suitable journal decision remain necessary; the byline instruction alone does not establish those facts. No novel superior detector or general physical safety claim is supported by this revision.
