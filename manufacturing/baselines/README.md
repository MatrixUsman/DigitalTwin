# Baselines — Smart manufacturing

The critical-learning shortlist is [CASPER 2024](casper/README.md), [TWINE 2026](twine/README.md), and [CatBoost on CASPER 2026](catboost/README.md). These folders contain source/admission notes only, not complete resource packs or reproduced models. No main method is execution-ready. CASPER is the conditional first reproduction candidate.

Consult [literature evidence](../docs/LITERATURE_EVIDENCE.md) and the [reproduction plan](../docs/REPRODUCTION_PLAN.md). This directory currently contains no model checkout or implementation.

From the project root, place future author-code checkouts under ignored `baselines/vendor/<method>/`. For each method, keep a small tracked provenance/deviation record: exact paper/version, source URL, commit, license, dataset assumptions, original protocol, our protocol changes, environment/lock, device patches, and execution status. Public availability is not proof of reproducibility.

Every main method must be evaluated on this project's agreed data/releases under its frozen protocol. Do not copy published headline scores into measured-results tables or reuse another project's fitted model as if reproduced here.
