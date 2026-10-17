# Claim and source coverage

This is a bounded self-audit, not external review or a blanket guarantee about every possible claim.

| Manuscript claim | Evidence |
|---|---|
| 216 episodes, thirteen methods, 2,808 outcomes | v0.8 `roster.json`, `outcomes.json`, `summary.json`; complete replay in `VERIFICATION.json` |
| 50.24% benign reduction; primary failure | `aggregate.json`: pooled `learned_uncertainty_return` versus `nominal_fixed_return`; pre-generation `PLAN.md` and `FREEZE.json` |
| 36/108 versus 108/108 timely clearances | Same pooled rows; all event records; return arithmetic checked separately |
| Removing allowance yields 140 versus 309 benign alarms and 108 versus 104 fresh onsets | `matched_no_allowance` versus candidate; identical entry thresholds in all three plant calibration records |
| Q2/Q3 cannot satisfy candidate return condition | Frozen inequality in `mechanism.py` and calibrated allowances 0.191489/0.209284 against 0.1; `NORMAL_ADMISSION.json` is explicitly post-exposure |
| 21/135 return-definition disagreements | `reference_disagreements.json`; no change to historical v0.7 evaluation |
| 189/216 complete empirical reference enclosures | `VERIFICATION.json` truth diagnostics; not a 95% coverage claim |
| Conditional discrepancy and interval-box bounds | Algebraic proofs in manuscript and `ANALYSIS.md`; synthetic checks; these elementary results are not asserted to be novel theory |
| 14 tests; 9,610 post-run checks | Frozen test log and verification receipt; three additional restricted-input replays recorded separately |
| Restricted scientific information use | Frozen source; `INFORMATION_FLOW_CHECK.json` confirms three selected episodes replay identically with only the three permitted observation keys. Worker passes a broader episode dictionary, so no sandboxed API boundary is claimed |
| Run time/memory/output | Completed `supervisor.json` and worker `summary.json`; sampled and process-lifetime peaks distinguished |
| CASPER/edge identities and input mismatch | Prior full-manuscript/code audit preserved in v0.7 `SOURCES_AND_ADMISSION.md` |
| FAIL-Detect published status, code/sign/quantile correspondence | Official RSS record, author HTML/project/repository revision and pinned functional predictor/caller/license. Printed-sign statement limited to arXiv v1, not the raster proceedings PDF |
| RESCUE | Saved arXiv:2610.13516v1 HTML; explicitly preprint, not a confirmed peer-reviewed comparator |
| Interval/RAPIO/Kaisar relations | Prior primary-source ledgers; incomplete full-method access remains disclosed |
| Author details and AI assistance | Only supplied facts used; no invented personal declarations or review approvals |

Seven bibliography keys are cited and accounted for. All thirteen pooled method rows and all 39 plant benign counts match saved artifacts. The common full-result CSV additionally contains precision, recall, AP, coverage, alarm rates, gap counts and return/miss outcomes by plant and task. No published headline score or third-party figure is used as our experimental result.

Scientific limitations: one simulator, three commissioned assets, three new task families, paired noise replicates, empirical uncertainty with shifted tasks, conservative unknown-context behavior, and no paper-faithful full recent-method reproduction. Originality and the intended overall improvement remain unestablished. These are reasons to withhold submission readiness, not formatting issues.
