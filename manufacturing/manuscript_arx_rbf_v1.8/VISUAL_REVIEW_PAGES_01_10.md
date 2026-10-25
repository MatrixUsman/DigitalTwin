# Read-only visual review: pages 1–10

Reviewed on 24 October 2026 by the separate `mechanism_audit` AI agent. The PDF skill was applied for rendered-page inspection. This is layout QA, not independent human peer review, source verification, scientific acceptance, or journal-readiness approval. No manuscript source or PDF was modified by this reviewer.

**Final layout result: pass for pages 1–10.** The initial Figure 2 label crop was reported and is resolved in the final page 10. No unresolved text/figure/table overlap, clipped content, unreadable table, or broken page balance was found in the assigned pages. Pages 11–19 belong to the root review and are not approved by this report.

## Final artifact and inspection coverage

- PDF: `output/pdf/ARX-RBF-Muhammad-Usman-v1.8.pdf` (19 pages).
- PDF SHA-256: `cea29f95fee91afe51324386846c2b3eccb96abb46c4bf51733ff44d56c00a2b`.
- Build: `local/manuscript_arx_rbf_v1.8/pdf_build/attempt_004/receipt.json`; the saved receipt PDF identity matches the current file.
- Final images: `local/manuscript_arx_rbf_v1.8/render_004/page-01.png` through `page-10.png`.
- Directly inspected: all ten pages in `render_001`; changed page 2 in `render_002`; changed pages 2–8 in `render_003`; final changed page 10 in `render_004`.
- Reuse is supported by exact SHA-256 equality: final pages 1–9 match `render_003`; pages 1 and 9 there match the directly inspected `render_001` versions. Thus every final assigned page is either directly inspected or byte-identical to the inspected image. This is not an inference from unchanged source text.

| Page | Final page image SHA-256 | Coverage |
|---:|---|---|
| 1 | `c8ecbf31ab6365b7c865c568126216b8dd9cdddfbf4e7dc9d94942cb76b201a5` | Exact rendered equality to directly inspected page |
| 2 | `ab4974461a3417a0efb9411e95e386228205c10d74fd2575d172aaeb020ab25d` | Exact rendered equality to directly inspected page |
| 3 | `650a4772754106dbc59298d7eab60768e2b538e730fdcf4cc4467823d1485926` | Exact rendered equality to directly inspected page |
| 4 | `033289c0d365b4895ff02305f3ceab76639a4d7a21b0075f48b820d0143e8af9` | Exact rendered equality to directly inspected page |
| 5 | `82a3e449affe9aabe1c97c27b9b578f13b5310b9a8c5c711a1e5c43f6fb79111` | Exact rendered equality to directly inspected page |
| 6 | `cca31a57ef5f31a9149c48e3afe6e196dee1ccf6224ba252d5251d52d53c64ad` | Exact rendered equality to directly inspected page |
| 7 | `913e087f1c474aab2f84e32e63678edeef0a2c25bbf1202fc75aa6605edcab45` | Exact rendered equality to directly inspected page |
| 8 | `2c51be162ed7e5cc52f16f064f0b99d624f2d0269d7f3b3f7f9a8701d3a44379` | Exact rendered equality to directly inspected page |
| 9 | `34260a89035b38fca98a51e675a74be3bf9ab831f5290f1db114246a29c3696d` | Exact rendered equality to directly inspected page |
| 10 | `8265dbb6e7e0104dc99fc4388e444c29781ee2ddf9585870a778309657e4eb95` | Final page directly inspected |

## Observed layout

| Pages | Assessment |
|---|---|
| 1 | Title, author block, abstract and two-column introduction fit within margins. Title wrapping and abstract density are acceptable. |
| 2–3 | Contributions, literature review, section transitions and equations are legible, with no collisions or cropped equation numbers. |
| 4 | Figure 1 and both algorithm tables fit their assigned widths. The diagram text is smaller than body text but remains readable; algorithm steps and captions do not overlap. |
| 5–8 | Dense two-column methods, experimental details and metrics remain readable. Full-width Tables 3–4 fit, and columns/section starts remain ordered without conspicuous empty blocks. |
| 9 | Tables 5–8 and their captions fit. The longer Table 7 caption is dense but readable, and the single-column tables remain within the column bounds. |
| 10 | Tables 9–10 and the three-panel Figure 2 fit. The final vertical score label is complete; axes, legends, captions and body text are separated. |

## Defect and resolution

In the earlier builds, Figure 2's top-panel vertical label, “Score / threshold,” was clipped at the figure canvas's upper edge. The problem was confirmed by rendering `figures/trace.pdf` separately at 200 dpi, rather than attributing it to the page viewer. The root applied an 8 pt upper MediaBox/CropBox extension, recorded in `TRACE_LAYOUT_REPAIR.json`, preserving the drawing stream. Final page 10 was then visually re-inspected: the label is now fully visible, and the added height does not introduce table/caption overlap or a page-margin defect.

Inspection used `view_image` on the rendered PNGs. The supplementary diagnostic was `pdftoppm -r 200 -png -singlefile manufacturing/manuscript_arx_rbf_v1.8/figures/trace.pdf /tmp/manufacturing_trace_qa`, from the workspace root; a temporary `sips` crop also helped isolate the label. A preliminary attempted Python/Pillow crop failed because system Python lacked Pillow; no package was installed and the failure did not modify source artifacts. Hash checks used Python standard-library `hashlib` only.

This assessment concerns the 869×1228 page renderings and the final PDF identity above. It does not establish print proofing at every zoom level or compliance with a particular journal's typography template. The paper's scientific and authorship gates remain separate.
