# Baselines — Smart manufacturing

The critical-learning shortlist is [CASPER 2024](casper/README.md), [TWINE 2026](twine/README.md), and [CatBoost on CASPER 2026](catboost/README.md). Each has source/admission notes and an ignored pinned source pack. No main method is execution-ready. CASPER is the conditional first reproduction candidate.

The [paper-to-code map](../docs/PAPER_CODE_TRACEABILITY.md) gives current reading coverage and links detailed notes for each candidate. Full manuscript coverage is one of three; code availability is not a substitute for the two missing papers.

Start with the [data/materials guide](../docs/DATA_AND_BASELINE_STUDY.md) and [paper-to-code study](../docs/BASELINE_CODE_STUDY.md). The [source-pack manifest](SOURCE_PACK_MANIFEST.json) records **67 pinned artifacts** (18 source/config/doc files, 34 author-reported tables, 15 figures) plus three repository-tree receipts. Reported results remain author artifacts, not our runs. One full manuscript is collected; two remain inaccessible. There is no validated runnable environment, executed model or project detector implementation. See [literature evidence](../docs/LITERATURE_EVIDENCE.md), the [manuscript audit](../docs/MANUSCRIPT_COLLECTION_AUDIT.md) and [comparison protocol](../docs/COMPARISON_PROTOCOL.md).

From the project root, place future author-code checkouts under ignored `baselines/vendor/<method>/`. For each method, keep a small tracked provenance/deviation record: exact paper/version, source URL, commit, license, dataset assumptions, original protocol, our protocol changes, environment/lock, device patches, and execution status. Public availability is not proof of reproducibility.

Every main method must be evaluated on this project's agreed data/releases under its frozen protocol. Do not copy published headline scores into measured-results tables or reuse another project's fitted model as if reproduced here.
