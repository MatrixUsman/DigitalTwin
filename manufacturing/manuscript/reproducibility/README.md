# Local reproducibility package: what has and has not been reproduced

This package belongs to the completed manufacturing case study. It is not a new experimental result, an author-code reproduction of CASPER/TWINE, or an independently reproduced study.

| Level | Included evidence | Actual status |
|---|---|---|
| Presentation regeneration | Saved aggregate JSON; exact generator; tables, numerical macros, two PGFPlots sources and reference register | Byte-for-byte regeneration checked locally; no raw data/model execution |
| Source/configuration identity | 52 exact files, 12 historical specification files and seven aggregate/freeze/test records in the manifest | All 71 bundled hashes checked |
| Software tests | Frozen test sources and original 324-test receipt | Original campaign tests recorded; copied snapshot suite not independently reexecuted for this manuscript |
| Saved-score arithmetic | Original campaign audit referenced by completion record | Previously performed on saved arrays; manuscript check reconciles aggregate counts, not AP from individual scores |
| End-to-end experiment reproduction | Code, configuration and dependency identities; access/replay instructions | Not independently performed; raw data, fitted artifacts, complete original run logs/scores and receipt chain remain outside this folder |
| PDF build | LaTeX and PGFPlots sources; pinned project-local Tectonic | Compiled locally from unchanged inputs during each accepted build; 18 pages visually inspected; see the separate PDF build/review records |

`SOURCE_MANIFEST.json` binds the exact files. Its `unbundled_dependencies` field retains the **complete original 133-binding dependency inventory**, including some files also copied into `entries`; the field name does not mean all 133 are absent. Resolve entries first and then the original authorized local store. Dataset contents and private download information are excluded.

The experiment used revision `b207e0758c1dd90fbd09d3aa4de943a11d7f08cb` **with dirty source snapshots**. Checking out that commit alone is insufficient. The 52 exact hashes identify the executed code/configuration; later manuscript commits do not change the experiment's identity. Snapshot specifications preserve earlier readiness language intentionally. Current completion is in `inputs/FINAL_CAMPAIGN_V0.1_RECORD.json`, not a rewrite of the prospective freeze.

See [REPRODUCE.md](REPRODUCE.md), [DATA_ACCESS.md](DATA_ACCESS.md) and [the declaration/release checklist](../editorial/AUTHOR_DECLARATIONS_AND_RELEASE.md). No public archive, code license or distribution approval has been selected.

PDF compilation now uses [the pinned local builder](../tools/build_pdf.py); [build/report](../PDF_BUILD_REPORT.md). The original static validation receipt did not compile TeX. Neither a PDF nor its layout review constitutes an independent scientific reproduction.
