# CASPER normal convergence study v0.11

**Completed under the user's explicit resource approval.** One run produced all nine declared outcomes. Read the [measured results and interpretation](RESULTS.md) and [learning curves](figures/normal_learning_curves.png).

- CASPER-style seeds 17/42/2026: each stopped by patience at epoch 27 and saved epoch 22; standardized development MSE 0.017703 / 0.017451 / 0.017458.
- Compact Edge-style seeds: each reached the 100-epoch cap while improving; MSE 0.044730 / 0.043451 / 0.042700. They remain training-limited.
- AR(4): MSE 0.006074, lowest on this filtered normal prefix. All simple controls are unchanged.
- Cost: 764.794 s wall, 753.252 s CPU, 553.05 MiB sampled RSS, 2.68 MiB run outputs, within the approved limits.
- Verification: 17 pre-run synthetic tests and 3,754 post-run integrity/numerical checks passed. All prior studies and PDFs remain intact.

[All outcomes](all_outcomes.csv), [all per-channel errors](per_channel_errors.csv), [verification receipt](VERIFICATION.json), [presentation provenance](PRESENTATION.json), [actual run](../../local/casper_convergence_v0.11/runs/pilot_001/summary.json).

The [plan](PLAN.md) and [freeze](FREEZE.json) are preserved pre-execution snapshots; the plan's pending-approval wording is historical. [Actual approval](RUN_AUTHORIZATION.json) and the [execution receipt](../../local/casper_convergence_v0.11/execution_authorization.json) record the subsequent user instruction. The single attempt is consumed; do not rerun or increase its budget automatically.

This is a normal-development adequacy study of independent architectural implementations. It establishes neither original-paper reproduction nor attack superiority. The [mechanism and fair-comparison requirements](../casper_comparison_v0.10/DECISION.md) remain the next scientific work. No new PDF or attack evaluation was produced.
