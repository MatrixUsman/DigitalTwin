# ARX–RBF manuscript, revision 1.8

**ARX–RBF Motion Modeling for Cyberattack Detection and Recovery Monitoring in Industrial Robots**  
Muhammad Usman — COMSATS University Islamabad, Sahiwal Campus

24 October 2026. One integrated manuscript: 19 pages, six figures and 28 references. The existing selected title and byline are preserved. This revision completes the authorized candidate investigation and reports its failed outcome. It is an accurate completed research manuscript for author review, **not a journal-ready original-method contribution**. No journal submission or public release has occurred.

The new normal-only study evaluates all 33 prespecified methods. The selected constrained correction improves prediction RMSE by 11.06% but worsens the empirical radius proxy by 8.37% against the selected direct-reference control. It also loses the matched-gain accuracy comparison. An ordinary clipped linear control has lower error and radius than all six constrained neural candidates. No attack campaign or longer training followed this failure. The manuscript preserves earlier failed criteria and the exposed-data limitations. Established contraction and saturation bounds do not establish theorem novelty.

The PDF is `output/pdf/ARX-RBF-Muhammad-Usman-v1.8.pdf` relative to the manufacturing project. The editable archive is `output/ARX-RBF-Muhammad-Usman-v1.8-latex.zip`. These are manuscript artifacts, not a complete experimental rerun package. Third-party raw data, model environments, vendor code and private run storage are excluded from the archive. `AUTHOR_ACTIONS.md` records the unresolved scientific, human-author and venue decisions.

## Build and checks

From the extracted source archive, compile `main.tex` with Tectonic. All transitive TeX inputs and the six used vector figures are included; the bibliography is embedded through `references.tex`, with `references.bib` retained for editing. Standard LaTeX packages must already be available or obtained under the user's own environment policy. The retained local build used Tectonic 0.17.0 offline with an existing cache.

From the manufacturing project, the actual revision commands were:

```sh
.venv-plots-v03/bin/python manuscript_arx_rbf_v1.8/integrate_diagnostics.py
.venv-plots-v03/bin/python manuscript_arx_rbf_v1.8/integrate_pilot.py
.venv-pdf/bin/python manuscript_arx_rbf_v1.8/repair_trace_bounds.py
.venv-plots-v03/bin/python manuscript_arx_rbf_v1.8/repair_matched_layout.py
python3 manuscript_arx_rbf_v1.8/build_pdf.py --document main
.venv-pdf/bin/python manuscript_arx_rbf_v1.8/audit.py
pdftoppm -r 105 -png output/pdf/ARX-RBF-Muhammad-Usman-v1.8.pdf local/manuscript_arx_rbf_v1.8/render_006/page
python3 manuscript_arx_rbf_v1.8/package.py
```

The final build passes 288 manuscript consistency checks. All 19 pages were visually inspected, directly or by byte identity to the exact earlier inspected render. Source review verifies the new 33-row table and prior-art qualifications. Separate review checks 790 prior-package bindings (771 distinct paths), with no preserved file changed. These are AI-assisted technical checks, not external scientific replication, peer review, human author approval or a publication-readiness certificate.

The main project records are `research_cycles/gain_limited_v0.23/RESULTS.md`, its frozen protocol/reviews, and `research_cycles/novelty_v0.22/decomposition/RESULTS.md`. This source directory retains the claim ledger, independent reviews, build, audit, layout, acronym-advisory, source-archive and package receipts. The generic two-column manuscript is not tailored to a selected venue; its 19-page length also exceeds the earlier 15-page editorial target. Further compression cannot resolve the substantive contribution failure.
