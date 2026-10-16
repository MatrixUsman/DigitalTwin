# Configurations — Smart manufacturing

The [right-arm contract v0.1](casper_right_arm_contract_v0.1.json) defines dataset identity, recorded schedule annotations, twelve permitted joint-state channels, relative-time use, chronological row ranges, gap/warmup policy and normal-only calibration. Its [explanation](../docs/ANNOTATION_FEATURE_SPLIT_CONTRACT.md) records assumptions and limits. It is frozen for **design review**, not an executable model configuration or training admission.

Model-specific transforms, histories, initialization, score definitions, finite candidate grids, seeds and runtime budgets still need separate specifications. Changing the selected inputs/partitions/annotation convention requires a new contract version and a reason recorded before final attack scoring.

Keep private paths/credentials in ignored `local/` under the project root. Every run must save a resolved configuration and hash. Defaults imported from a sibling project or an upstream method require explicit review; never inherit its thresholds, test decisions or fitted transforms silently.

Protocol changes after test inspection require disclosure and an appropriate new evaluation design, not repeated tuning on the same held-out attacks.
