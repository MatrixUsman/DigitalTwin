# AFTER — single-paper revision 1.4

18 October 2026. Revised using the organization and explanatory detail of the teacher's supplied example. The user's subsequent instructions require **one paper, no separate supplement, and more graphs**.

- **PDF:** `../output/pdf/AFTER-Muhammad-Usman-v1.4.pdf` — **15 pages total**, including appendices and references.
- **Editable LaTeX:** `../output/AFTER-Muhammad-Usman-v1.4-latex.zip`.
- Nine main sections; seven figures; 14 table floats, including two numbered algorithms; 20 cited references.
- Sole requested byline: Muhammad Usman. Existing title retained as provisional; no new title approval inferred.

The paper now separates Introduction, Literature Review, Methods, Experiments, Evaluation Metrics, Comparison Methods and Baselines, Results, Discussion and Conclusion. It explains the state and trust assumptions, ARX/RBF equations, fitting and causal monitoring algorithms, finite selection grid, actual selected settings, data populations, chronological preprocessing, calibration, five studies, full final roster, ablations and costs. Earlier supporting derivations, IMU study, complete comparison tables, residual diagnostic and source identities are integrated into this same document. The conclusion stays short.

The seven figures show the model, all 30 saved tuning candidates, CNN learning curves, detection/false-alarm/recovery contrasts, a saved recovery trace, matched component removals and uncertainty feasibility. Three comparison/tuning plots are new presentations of saved results. No model, training run, simulation condition or benchmark measurement was added.

## Evidence and review

[Structure mapping](STRUCTURE_MAPPING.md) records the example's page-by-page organization and the boundaries on adaptation. The exemplar's prose, figures, references, authors and scientific claims were not copied. Its PDF is not included in our archive.

[The audit](AUDIT.json) passes **1,338 checks**, including all source/result bindings in v0.13, v0.14 and v0.15, all 49 bindings in the previous revision, exact preservation of earlier generated tables, every newly plotted value and all 20 citation keys. [Visual QA](VISUAL_QA.json) covers all 15 final pages. The final build has no unresolved references, missing glyphs or overfull boxes. Seven underfull-line diagnostics remain; the corresponding text was inspected and is readable. This is same-assistant consistency/visual review, not independent peer review.

The [reference audit](REFERENCE_AUDIT.md) retains the earlier verified sources and access limits. Eighteen cited publication versions are dated 2024–2026; older background and preprints remain identified. No new literature search or expanded verification is claimed for this layout task.

The candidate's declared improvement criterion remains failed; its short window changes no decisions. The ordinary protected reference already supplies the main evidence-retention benefit. The revision does not establish a novel detector, superiority over CASPER, industrial safety or journal acceptance. The user's original-contribution goal, compatible paper-level reproductions and human author review remain open. Data access and original-test exposure status are unchanged.

## Rebuild

From `/Users/matrixusman/CUI/DigitalTwin`:

```sh
manufacturing/.venv-reproduction-v02/bin/python manufacturing/manuscript_after_v1.4/assemble_revision.py
manufacturing/.venv-reproduction-v02/bin/python manufacturing/manuscript_after_v1.4/render_references.py
manufacturing/.venv-plots-v03/bin/python manufacturing/manuscript_after_v1.4/generate_assets.py
manufacturing/.venv-reproduction-v02/bin/python manufacturing/manuscript_after_v1.4/build_pdf.py --document main
manufacturing/.venv-pdf/bin/python manufacturing/manuscript_after_v1.4/audit.py
```

The local builder uses the existing verified Tectonic 0.17.0 binary and cached resources. No resources were downloaded. The assembled `main.tex`, section files, numeric `references.tex`, generated tables and vector figures can also be compiled twice with a conventional XeLaTeX installation. The archive needs no raw observations for compilation. Reassembling inherited introductory prose or regenerating scientific plots requires the retained workspace evidence; those optional scripts are not needed to compile the supplied source.

The final A4 layout has a 10-point body with 11-point leading, 0.60-inch margins and two columns. Headings use ordinary journal hierarchy; the last bibliography page has one explicit column break. This is a neutral format, not a copied publisher class.

## Preserved revision attempts

- Initial offline build lacked `size10.clo`; a second build lacked the square proof-symbol font. Existing cached class/font resources were used instead, without installing packages.
- Early drafts were 19, 17 and 16 pages. Repeated explanations were condensed, graph dimensions and headings adjusted, and narrow equations/table columns repaired. All scientific outcomes remain unchanged.
- Two local editing helper invocations failed (one patch format and one paragraph selector); their partial/no-change outcomes were inspected and corrected. A malformed read-only tool expression produced no filesystem change.
- The first editorial audit mistook the LaTeX section-command definition for a content section. Restricting that check to the document body corrected the parser; no manuscript content changed for that repair.
- All compiler attempts remain under ignored `local/manuscript_after_v1.4/pdf_build/`. Earlier manuscripts, the teacher PDF, experiments and sibling projects were preserved.

No publication, upload, new data processing, training, paid compute, assistant Git staging/commit/push or system-wide package change occurred.
