# Claim-to-evidence map

All paths below resolve from `manufacturing/`. The source study versions and their frozen evidence are unchanged. This manuscript introduces no experiment.

| Manuscript claim | Evidence | Interpretation |
|---|---|---|
| 216 episodes, 13 rules, 2,808 outcomes; failed primary criterion | `local/recovery_v0.8/runs/confirmation_002/{roster,outcomes,aggregate,summary}.json` | Prospectively frozen synthetic evaluation; three configurations in one simulator |
| 621 → 309 benign alarms, 36/108 timely clearances | `aggregate.json`, pooled nominal_fixed_return and learned_uncertainty_return | The 50.24% burden reduction does not satisfy the complete primary criterion |
| Matched no-allowance control: 140 benign, 108/108 timely, zero early | Same aggregate, matched_no_allowance | Identical entry threshold; not a separately calibrated equal-budget comparison |
| Q2/Q3 cannot clear because b > 0.1 | `calibration.json`; `research_cycles/recovery_v0.8/mechanism.py` | Algebraic consequence of this rule, not a universal limitation of uncertainty-aware monitors |
| 21/135 return-time disagreements; 189/216 trajectory enclosure | `reference_disagreements.json`; `research_cycles/recovery_v0.8/VERIFICATION.json` and `ANALYSIS.md` | Same-plant evaluator counterfactual versus nominal reference; empirical enclosure only |
| 63 candidate fits; selected ARX 8/16/32 | `local/commissioning_v0.9/runs/normal_002/{candidates,selection,summary}.json` | Finite normal-only search; ordinary ARX/FIR identification |
| 81 new normal episodes plus 15 reused checks; 576 recorded outcomes | `normal_roster.json`, `summary.json`, `metrics.json` | Reused normal episodes remain development/archived material; duplicate selected roles are not extra evidence |
| Allowance decreases 51.27% and 38.56%; overall admission fails | `fresh_summary.json` | Within-study matched ARX(4), common 100-point initialization, five allowance episodes; no replacement attack experiment |
| Conditional perfect-reference margin probability ≈ 2.19e-9 on Q3 | `research_cycles/commissioning_v0.9/NOISE_DIAGNOSTIC.json` and `noise_diagnostic.py` | Post-study independent Gaussian calculation with fixed scales, N=5500, delta=.1, gamma=.95; not robot-population evidence or finite-check probability |
| Timely clearance and early clearance are separate metrics | `research_cycles/recovery_v0.6/metrics.py`, inherited by v0.8 | Timely means a known inactive observation within five seconds from the evaluator's return-window start; already-cleared alarms also qualify |
| Unknown command context | `recovery_v0.8/mechanism.py`, inherited `recovery_v0.5/observer.py`, `metrics8.py` | Unknowns stay in eligible support, cannot detect attacks and get AP score -1; coverage reported explicitly |
| Numerical bounds | New manuscript Sections 3 and 7, derivations displayed | Elementary conditional geometry/probability, not asserted new interval theory or new detector |
| Resource costs and software checks | Both studies' `VERIFICATION.json`, run `supervisor.json` and `summary.json` | Actual whole-run costs and checks; neither deployment latency nor physical validation |

The paper does not assert superiority over CASPER, its successor, full FAIL-Detect, RESCUE or other recent complete systems. It does not claim hardware validation, public code release, a safe reset policy, novelty of ARX/hysteresis, successful author review, or journal acceptance. The original contribution goal is not silently marked complete by this editorial deliverable.
