# AFTER — manuscript revision 1.3

**18 October 2026.** Revised in neutral journal format at the user's request, after verifying independent public-data and published-comparator sources. Sole requested byline: Muhammad Usman. The existing proposed title is retained; this does not record a new title approval.

- Main: `../output/pdf/AFTER-Muhammad-Usman-v1.3.pdf` — **11 pages**, 20 cited references, three tables and two vector figures.
- Supplement: `../output/pdf/AFTER-Muhammad-Usman-v1.3-supplement.pdf` — **12 pages**, eight tables and two vector figures.
- Editable package: `../output/AFTER-Muhammad-Usman-v1.3-latex.zip`.
- [Teacher response](REVIEW_RESPONSE.md), [reference audit](REFERENCE_AUDIT.md), [machine-readable checks](AUDIT.json), [visual review](VISUAL_QA.json).

The main paper now gives the explicit ARX/RBF reference and state machine, normal-only optimization, selected parameters, datasets and splits, a separate baseline section, five validation studies, full final audit, ablations, costs and a 76-word conclusion. Longer derivations, earlier experiments, IMU learning curves, extra metrics and data/code admission move to the supplement. All 20 references are cited; 18 cited publication versions are dated 2024–2026. Access limitations and older/preprint histories are disclosed, not erased to satisfy the recency count.

## Scientific status

The candidate failed its declared normal and attack/recovery improvement requirements. The short-window ablation changes no alarms. Protected-reference evidence retention is also achieved by the ordinary base model. This revision does not establish a novel detector, superiority over CASPER, physical safety or journal acceptance. Full compatible published-method reproduction, a worthwhile distinct contribution and author approval remain open. The user's original-contribution goal has not been silently replaced by document completion.

[Evidence admission v0.15](../research_cycles/evidence_admission_v0.15/DECISION.md) verifies the original voraus-AD release and pinned MVT-Flow code. The received file's metadata match the original split and execution counts. Its process signals and original test remain unopened; MVT-Flow has not run. Objective/layer discrepancies and a conditional padding issue are documented. FactoryNet remains partially admitted, with release/source-independence issues. These sources are future evidence, not additional experimental results in this manuscript.

## Build and provenance

No fitting, simulation or training occurred during this revision. New tables and figures use saved outcomes; older tables and retained figures are copied from revision 1.2. The visual audit covers every final page. The local consistency audit passes 1,177 checks, including 303/757/34 bindings in the v0.13/v0.14/v0.15 packages and preservation of the previous main source/PDF. This is a same-assistant consistency audit, not independent peer review. The research and PDF skills supplied bounded workflow guidance; no complete ARS multi-agent pipeline or external detector service was invoked.

From the repository root, the local commands are:

```sh
manufacturing/.venv-plots-v03/bin/python manufacturing/manuscript_after_v1.3/generate_assets.py
manufacturing/.venv-reproduction-v02/bin/python manufacturing/manuscript_after_v1.3/render_references.py
manufacturing/.venv-reproduction-v02/bin/python manufacturing/manuscript_after_v1.3/build_pdf.py --document main
manufacturing/.venv-reproduction-v02/bin/python manufacturing/manuscript_after_v1.3/build_pdf.py --document supplement
manufacturing/.venv-pdf/bin/python manufacturing/manuscript_after_v1.3/audit.py
```

The local builder uses the previously verified Tectonic 0.17.0 binary and cached resources. A numeric linked bibliography is generated from `references.bib`; the build does not require BibTeX or a remote service. A conventional XeLaTeX installation can compile the extracted archive's `main.tex` and `supplement.tex` twice using the supplied `references.tex` and generated assets. Regenerating scientific figures requires the full locally retained research artifacts; compilation alone does not.

Preserved build history: the first two attempts failed on uncached font metrics; the third produced an incomplete bibliography because `unsrt.bst` was unavailable. The fourth supplement build had one overfull identifier. These were corrected using cached typography, a generated bibliography and breakable paths. A missing `pdfplumber` import in the editorial audit was replaced with existing pypdf/Poppler; no dependency was installed. Final builds have no unresolved references or overfull/underfull diagnostics. The first Matplotlib call emitted unwritable cache warnings; its scoped cache is now explicit. All attempts remain in ignored `local/manuscript_after_v1.3/`.

The user's accidental stash was restored with its index state and verified against stash `63d29ed3368b749cf397d8ecc8571c99b13d7155` before manuscript editing resumed. The stash was retained as a backup. No assistant commit, push, upload, publication, system-wide package change or sibling-project mutation occurred.
