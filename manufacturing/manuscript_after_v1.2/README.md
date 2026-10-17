# AFTER — prose revision 1.2

Current PDF: `manufacturing/output/pdf/AFTER-Muhammad-Usman-revised.pdf`.

The user requested more natural prose after reporting an AI-detector flag. This revision improves clarity, flow and academic readability. It makes no promise about detector classifications and does not disguise the assistance used. The sole-author byline, factual AI-assistance disclosure, funding/conflict statements and all scientific limitations remain intact. No manuscript was uploaded to a detector service.

The abstract, introduction, related work, selected methods/results paragraphs, discussion, conclusion and explanatory appendix text were copyedited. Repeated project-management phrasing was reduced; explanations now connect the observed behavior to its cause. Technical definitions and terminology remain consistent. This is a style revision of the same scientific evidence, not a new experiment or stronger contribution claim.

The base edition and its source ZIP remain unchanged. The new `main.tex`, `sections/`, `generated/`, `figures/` and `references.bib` are independently editable. All equations, proofs, tables, figures, citation commands, reference targets and numerical tokens were compared with revision 1.1. The full diff and paragraph changes are saved alongside the audit. A successful first offline build produced 20 pages, all rendered and inspected.

Commands, from the workspace root:

```sh
manufacturing/.venv-reproduction-v02/bin/python manufacturing/manuscript_after_v1.2/build_pdf.py
manufacturing/.venv-pdf/bin/python manufacturing/manuscript_after_v1.2/audit.py
manufacturing/.venv-pdf/bin/python manufacturing/manuscript_after_v1.2/package.py
```

The academic-research-suite writing-quality guidance and PDF workflow were applied inline. The work uses localized, reviewable LaTeX patches; it does not claim execution of the suite's full formal review-roadmap pipeline or independent human review. The whole-manuscript request includes the abstract, which was copyedited without changing its numerical findings. No declaration that it was left untouched is made.

See [revision notes](REVISION_NOTES.md), the [previous evidence ledger](../manuscript_after_v1.1/CLAIM_EVIDENCE.md), [reference audit](../manuscript_after_v1.1/REFERENCE_AUDIT.md) and [submission notes](../manuscript_after_v1.1/SUBMISSION_NOTES.md). The original novel-detector objective remains unmet. Human review and journal-specific preparation are still required before submission.
