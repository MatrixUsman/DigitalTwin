# Configurations — Smart manufacturing

The [right-arm contract v0.1](casper_right_arm_contract_v0.1.json) defines dataset identity, recorded schedule annotations, twelve permitted joint-state channels, relative-time use, chronological row ranges, gap/warmup policy and normal-only calibration. Its [explanation](../docs/ANNOTATION_FEATURE_SPLIT_CONTRACT.md) records assumptions and limits. It is frozen for **design review**, not an executable model configuration or training admission.

The [evaluation policy v0.1](casper_right_arm_evaluation_v0.1.json) references the unchanged data contract and fixes common support/counts, calibration rank/ties, metrics, missing-score admission, seeds and final protection. Read its [protocol](../docs/EVALUATION_PROTOCOL.md). This is planning metadata, not executable enforcement. Its document hashes identify the reviewed versions; changing those specifications requires a versioned reconciliation.

Model-specific transforms, histories, initialization, score definitions, finite candidate grids, normal-only selection objectives and runtime budgets still need separate specifications. Final stochastic seeds are 17, 42 and 2026; deterministic controls run once. Changing the selected inputs/partitions/annotation convention requires a new contract version and a reason recorded before calibration and final outcomes.

Keep private paths/credentials in ignored `local/` under the project root. Every run must save a resolved configuration and hash. Defaults imported from a sibling project or an upstream method require explicit review; never inherit its thresholds, test decisions or fitted transforms silently.

Protocol changes after test inspection require disclosure and an appropriate new evaluation design, not repeated tuning on the same held-out attacks.

The [pilot v0.1](casper_right_arm_pilot_v0.1.json) specifies a future deterministic velocity-deviation control on bounded training/development prefixes. It is proposed and unexecuted; model/runner/actual command remain pending. Calibration and final access are excluded. The immutable evaluation policy's readiness fields describe its earlier planning snapshot; current implementation status is in [SOFTWARE_VALIDATION.md](../docs/SOFTWARE_VALIDATION.md) and [STATUS.md](../STATUS.md), without changing those frozen bytes.
