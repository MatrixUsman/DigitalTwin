# Configurations — Smart manufacturing

**Current status:** [all eleven frozen final methods completed](../docs/FINAL_CAMPAIGN_REPORT_V0.1.md), with no configuration changes after calibration. Earlier readiness language below belongs to historical specifications, whose hashes remain unchanged. Actual execution/access/outcomes live in the separate [completion record](../experiments/FINAL_CAMPAIGN_V0.1_RECORD.json); the final holdout is exposed.

The [right-arm contract v0.1](casper_right_arm_contract_v0.1.json) defines dataset identity, recorded schedule annotations, twelve permitted joint-state channels, relative-time use, chronological row ranges, gap/warmup policy and normal-only calibration. Its [explanation](../docs/ANNOTATION_FEATURE_SPLIT_CONTRACT.md) records assumptions and limits. It is frozen for **design review**, not an executable model configuration or training admission.

The [evaluation policy v0.1](casper_right_arm_evaluation_v0.1.json) references the unchanged data contract and fixes common support/counts, calibration rank/ties, metrics, missing-score admission, seeds and final protection. Read its [protocol](../docs/EVALUATION_PROTOCOL.md). This is planning metadata, not executable enforcement. Its document hashes identify the reviewed versions; changing those specifications requires a versioned reconciliation.

Model-specific transforms, histories, initialization, score definitions, finite candidate grids, normal-only selection objectives and runtime budgets still need separate specifications. Final stochastic seeds are 17, 42 and 2026; deterministic controls run once. Changing the selected inputs/partitions/annotation convention requires a new contract version and a reason recorded before calibration and final outcomes.

Keep private paths/credentials in ignored `local/` under the project root. Every run must save a resolved configuration and hash. Defaults imported from a sibling project or an upstream method require explicit review; never inherit its thresholds, test decisions or fitted transforms silently.

Protocol changes after test inspection require disclosure and an appropriate new evaluation design, not repeated tuning on the same held-out attacks.

The historical [pilot v0.1](casper_right_arm_pilot_v0.1.json) specified the smaller velocity control on bounded prefixes. Its single attempt is complete; preserve that configuration and consult the [actual pilot report](../docs/PILOT_REPORT.md), rather than its original planning-status fields. Calibration and final access are excluded. The immutable evaluation policy's readiness fields describe its earlier planning snapshot; current implementation status is in [SOFTWARE_VALIDATION.md](../docs/SOFTWARE_VALIDATION.md) and [STATUS.md](../STATUS.md), without changing those frozen bytes.


The separately versioned [controls v0.1](casper_right_arm_controls_v0.1.json) was declared before real fitting and executed once; preserve its bytes. It fixes the seven ordinary candidates, full normal-only populations, finite selection and resource limits. See the [plan](../docs/SIMPLE_CONTROLS_PLAN.md), [actual report](../docs/CONTROL_STUDY_REPORT.md) and [selected-artifact registry](../experiments/SELECTED_CONTROLS_V0.1.json). No calibration/final access is enabled by this file.

The separately versioned [observer v0.1](casper_right_arm_observer_v0.1.json) and its hash-bound [plan](../docs/OBSERVER_VALIDATION_PLAN.md) were declared before the completed normal-only validation. Preserve their bytes and the consumed attempt record. It reuses pinned selected references, fits only training bandwidth/scales, and fixes state dynamics, matched ablation, diagnostics and resource caps. [Actual results](../docs/OBSERVER_VALIDATION_REPORT.md) support an empirical observer; no calibration/final access is enabled.

The [score extension v0.1](casper_right_arm_score_extension_v0.1.json) and [bound plan](../docs/SCORE_EXTENSION_PLAN_V0.1.md) were executed once with no fitting. They bind the frozen observer, development-only support, six score definitions, exact historical parity, 66 preserved dependencies and four resource caps. Preserve bytes and the consumed attempt. See the [actual report](../docs/SCORE_EXTENSION_REPORT_V0.1.md); this configuration does not admit calibration/final access.

`casper_right_arm_campaign_v0.1.json` is the consumed scientific/execution specification for actual eleven-method freezing, threshold-only calibration and final budgets/rules. Preserve its hash. Final scoring/evaluation have now completed under the later explicit user authorization. Old planning/preparation-only fields remain historical; [actual execution report](../docs/FINAL_CAMPAIGN_REPORT_V0.1.md).
