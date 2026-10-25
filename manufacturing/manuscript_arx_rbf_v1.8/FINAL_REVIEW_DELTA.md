# Final review delta: revision 1.8

24 October 2026. Same separately executing Codex source/manuscript reviewer as INDEPENDENT_REVIEW.md. This is a focused source/layout delta check, not human author approval, rendered-page inspection or a new scientific review. The earlier review is preserved unchanged.

## Disposition

**PASS for the inspected delta. No additional substantive/source-claim correction required.** The scientific decision is unchanged: this is an accurate completed research manuscript for author review, but not ready for the intended original-method journal submission. Failed advancement criteria, prior-art limitations and physical-evidence limitations remain explicit.

All 35 TeX sources/tables were compared against the earlier reviewed snapshot. Exactly three files changed; the other 32 are byte-identical:

1. `main.tex`: removed only the generic article-navigation paragraph after the introduction. No result, interpretation, limitation or contribution claim was removed.
2. `references.tex`: changed bibliography item spacing from 1pt to 0pt. All 28 bibliographic identities, inspected versions and author-reported acceptance qualifications remain unchanged.
3. `sections/gain_results.tex`: the figure caption now describes the stars as the candidate/comparator chosen by the predeclared rule, replacing 'prospectively selected'. This is more precise: the selection rule was fixed before outcomes, while the selected identity follows the declared development selection. No metric or gate changed.

## Trace figure verification

Read both v1.7 and v1.8 trace PDFs using the existing project-local pypdf interpreter, without writing either asset. Each contains one page. Independently confirmed that the decoded drawing streams are exactly equal and have SHA-256 `efd346f8de759d9dbdd4183f945187b482cfa73a5f50f6f76e0cee55bd689ef7`. MediaBox and CropBox both change only from `[0,0,489.6,259.2]` to `[0,0,489.6,267.2]`. The receipt's original/final asset and repair-script hashes match the actual files.

This verifies an 8pt upper page-box extension with no change to the plotted drawing instructions. It does not independently establish that the final assembled PDF has no clipping; root's final rendered-page inspection must establish visual quality. No old sealed study or manuscript asset was modified by this reviewer.

## Final source identities

Final 35-source manifest SHA-256: `27c78a4da8269df85f2c19b0cfc52920e859097d51cc0a1a4d7f1af4f4874620`. These are the exact bytes reviewed after the three edits. Any later substantive change requires a further delta check.

| File relative to v1.8 | SHA-256 |
|---|---|
| `main.tex` | `aeccddfa802ffa7be13b14bdbc774f54a42c1df919e0dabc043e4cf063716d4b` |
| `references.tex` | `f239342fb3dc579bcb40aea3f4b3e9f5dc8c06842ac8cce2d943c35a4c6d4da2` |
| `sections/comparators.tex` | `cb0e0b9962432c5f780d02b73f1d18f0d2456a6a5fb8d355031fbfba32937372` |
| `sections/conditional_prediction.tex` | `14cb599dcc906a75c9529fcfe943b75ef209dcc20b150e70056dab8abc7b2d03` |
| `sections/context_experiment.tex` | `86a68e495a6990fbfff68642ff397edacbc2786845b27d7a2289d583bbde9761` |
| `sections/context_method.tex` | `b0acd6b28a0731282890af2a7d825a1c93f668c3c1bc139df5f5b11936a172ae` |
| `sections/context_results.tex` | `8f4079a156411d27505e51c76030b16eedbd2ba855905f8e464289dc33bfc772` |
| `sections/discussion.tex` | `07fb60788844d65d09220cf63ca7d4320518279b6c4900b97d7edd3ad32d8a1c` |
| `sections/earlier_results.tex` | `1420f443474f32354a7867f7be4cf66cd8063be01524ed3990d84350e75745f6` |
| `sections/experiments.tex` | `25656be2f385032babc51ac6fc22b4da9e3ecb4eb4bb0d54c64634666682750a` |
| `sections/gain_method.tex` | `bc79a2fbaf4166c722e57c7f27043132c4b18deda1c3df59cf636ac6ff943e35` |
| `sections/gain_results.tex` | `27e99d14cfc6895d1aeac746c798846738f6771b12d19ad8551ff77a3c43fc20` |
| `sections/methods.tex` | `6bbf301f8e3b15b6efd4f6c1871943e57bc7c5c42708f27d936d87a2cc019458` |
| `sections/metrics.tex` | `78abbe33b3ebff041c4d4bd5e60e41a4a3a482966fcefc7115c6061b609c7557` |
| `sections/provenance.tex` | `9f65ceb171bb3f937e4103a7a33437ae515a6be3e3b8551e8fdfb9377365e032` |
| `sections/results.tex` | `c6e55a83fe5d8a729e59eabfe4b25140ebca1123c32ed019cb166bb07e63b35c` |
| `sections/uncertainty.tex` | `5cb1c8fa2278780cc732513b1b95246d4cbc59029aa7d50d4321f3d350a86ffc` |
| `generated/attack.tex` | `f35a9544bc20a4da52d90424068bdc053b00a8f91074b55f54bf16377e979f65` |
| `generated/audit.tex` | `7d082c12a4f34d36dd5850fc8d10b2178b76c3a1ca767326c4ce263ed19c9108` |
| `generated/context_final.tex` | `993c7a1f3b777a1a88af2bacbedb290f24b12004d1d8b47eca713b4a687713d6` |
| `generated/extended.tex` | `95f31cafc11fb6820f6ea573824d0ded89eaa7427df350961876c5d1aad64ec8` |
| `generated/fivefold.tex` | `f64836ad79a1440ea31944e1dfe37eeb23195e499375acf57952fc7fbce92459` |
| `generated/forecast.tex` | `6ad78db74c5449926b201ba1bd48c5ebfc72e74d7becccbbf8d67b305edd39ea` |
| `generated/gain_pilot.tex` | `824340a46339abb779d1f7ffe6b8f0157cc70ad9d7d45b0f2e231f04bd7dd5dc` |
| `generated/imu.tex` | `7c2c540804a4e649674d98a99838762c01576e9632cf680b67fdd8e1888f376c` |
| `generated/matched_review.tex` | `76f3da30730acdbc789b952826c627c1ffb1d793fb8982df2c7835d4d81517cb` |
| `generated/metrics.tex` | `b1469ffdf4198aac15f1817486cc2311ead7bf41f7d1a3128a981db8478bdc70` |
| `generated/noise.tex` | `6bb65a0446f10aadd7f9b723446d87aca7a18924be39158ab491edb60f5c50eb` |
| `generated/normal.tex` | `878a82e85ac9811ecb7a407c70317912861c8a2383a41705b17d9cefb5da47f4` |
| `generated/normal_all.tex` | `3c9c746441ac88847a09594cab3d15ddc4a4e03ec60a02c0d26054164e5c9098` |
| `generated/selection.tex` | `e2281dae87b8bb998283e4c697ee5aaa463b86f1e727e947e2ec07e646d94244` |
| `generated/strata.tex` | `dff413ccd90f91e0d5688e344f62a65c4e4df536f2ba7d27b303914bab41f4ab` |
| `generated/strata_review.tex` | `b6494171a032cf2dd6e2c0a1f6b036c31dd84b25b4c4b5e2773b3f56125929eb` |
| `generated/timing_review.tex` | `d5c8250fe20a8fb7df0483c0af8ecc1aa69f66b31695cb9af175b80067e9449c` |
| `generated/window.tex` | `94575b2b0e9124d2f1f6c6fb1f6220823fd18192fef1177a429437f9f81e711c` |

## Review and layout artifact identities

| File relative to v1.8 | SHA-256 |
|---|---|
| `INDEPENDENT_REVIEW.md` | `e88c7d4c485684b0a31af385c43caa9e8b283034c47ab2634061ada89dbbe9bd` |
| `TRACE_LAYOUT_REPAIR.json` | `a92dc837f160df49bdff5f315fa6cb271a159e2815bbf6f0910da293f6b518bc` |
| `figures/trace.pdf` | `ff2353698b04b61c4ca10ed48c83b69b82bd6dc053dc9a6e6f32e6fb732441e7` |
| `repair_trace_bounds.py` | `ff75dc783e0c2962aee2a30d8581378967b4ed1737960d616c7363fb2311b4df` |

The compiled manuscript PDF is not yet bound by this source delta; the root's final build/render/package receipts should record its identity and page count.
