# Manuscript editorial revision

This revision tightens the prose of `../manuscript_recovery_v0.7/` at the user's request. The original manuscript, PDF and 260-file scientific package remain unchanged.

The title-page status notice, repeated process commentary and redundant qualifications were removed. The introduction, discussion, conclusion and declarations were shortened. Results, evidence limits, incomplete source verification and the AI-assistance disclosure remain explicit. No experimental choices or findings changed.

The [revised PDF](../output/pdf/alarm-recovery-model-mismatch-revised.pdf) has 14 pages, compared with 17 in the original. All 20 generated table/figure assets and eight display-math blocks are unchanged; all nine references remain cited. Source-bound build receipts, [editorial checks](EDITORIAL_AUDIT.json) and [visual QA](PDF_QA.json) record verification. Both editorial builds succeeded offline. No data were loaded and no experiment was run.

Rebuild from the workspace root using the existing isolated environment:

```sh
manufacturing/.venv-reproduction-v02/bin/python manufacturing/manuscript_recovery_v0.7r1/build_pdf.py
```

The build uses the existing local Tectonic cache. A changed build needs fresh PDF QA; the current audit binds the delivered version. This is a local editorial revision, not a submission or public release. Author declarations and approval remain pending where stated in the manuscript.
