# Manuscript revision 1.5 — selected title

Title: **ARX–RBF Motion Modeling for Cyberattack Detection and Recovery Monitoring in Industrial Robots**.

The user requested the PDF using the recommended title on 18 October 2026. This is a title-only revision of the sealed `../manuscript_after_v1.4/` package. The visible title and PDF metadata change. One obsolete self-name clause (“AFTER names the investigation”) is removed; the sentence stating that a new state-of-the-art detector is not validated remains. All scientific sections, tables, figures, references, declarations and findings are unchanged.

The output is `../output/pdf/ARX-RBF-Muhammad-Usman-v1.5.pdf`: one 15-page paper, including appendices and references, with Muhammad Usman as the requested sole byline. There is no separate supplement. The editable archive is `../output/ARX-RBF-Muhammad-Usman-v1.5-latex.zip`.

From the manufacturing directory:

```sh
.venv-reproduction-v02/bin/python manuscript_arx_rbf_v1.5/build_pdf.py --document main
.venv-pdf/bin/python manuscript_arx_rbf_v1.5/audit.py
```

The build uses the existing local compiler and cached resources, without network access. All final LaTeX inputs and figure assets are included for ordinary XeLaTeX/Tectonic compilation elsewhere; the repository build helper additionally expects the recorded local compiler/cache paths. The bibliography is already rendered in `references.tex`, with `references.bib` retained for editing. No prior assembler needs to run.

`BASE_IDENTITY.json` binds the base package and unchanged assets. `MAIN_BUILD_RECEIPT.json` records the compiler, command and source identities. `AUDIT.json` records title/content/build checks; `VISUAL_QA.json` records rendered-page comparison and inspection. Inherited reference and claim ledgers describe the prior scientific audit; they are not a new literature verification. No experimental result, training, raw-data access, submission or publication occurred in this revision. Scientific contribution and human approval requirements are unchanged.
