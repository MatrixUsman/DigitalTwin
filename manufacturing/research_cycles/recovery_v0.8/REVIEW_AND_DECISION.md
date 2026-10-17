# Scientific review and publication decision

17 October 2026. Single-agent self-review using the research skill's integrity/methodology/journal-fit criteria; not external peer review or an independent reviewer panel. The user's intended destination remains an original contribution paper. It has not been silently replaced with an accepted negative case-study objective.

## Findings supported by the completed experiment

- One complete frozen run: 216 episodes, thirteen decisions, 2,808 outcomes. Fourteen pre-run synthetic tests and 9,610 post-run checks passed. The launch infrastructure failure and verifier thread-setting failure are preserved separately.
- Clean commissioning reduced model uncertainty enough for clearance on Q1, but its empirical allowances on Q2/Q3 (0.19149/0.20928) exceed the fixed return tolerance 0.1. The proposed inequality therefore cannot clear on those plants, regardless of measurements. This is an analytical obstruction, not a lack of additional training epochs.
- The candidate reduced benign alarms from 621 to 309 versus nominal fixed return, but cleared within five seconds in only 36/108 detected-returned events. Its declared primary criterion failed.
- At the exact same entry threshold, removing the uncertainty allowance produced 140 benign alarm points instead of 309, retained 108 event overlaps, restored all 108 fresh onsets rather than 104, and cleared 108/108 rather than 36/108. Both had zero premature clears. The allowance is empirically harmful in this declared test; it must not be retained merely to make the mechanism look distinctive.
- Paired-plant and nominal-reference return times differed in 21/135 intervention episodes. The counterfactual error envelope covered 189/216 complete eligible trajectories. Fixed scenario design does not establish exchangeability or a 95% coverage guarantee.
- Common command-history loss caused all 27 command-dependent misses. They remain misses; unknown context is not a true negative. These results describe the stated information restriction.

## Gate decisions

| Gate | Decision | Reason |
|---|---|---|
| Implementation and numerical consistency | Pass within recorded scope | Frozen source/input identities, complete outcome coverage, independent count/return calculations, exact single-thread fit replay and selected physics replay |
| Candidate overall advantage | Fail | Finite recovery criterion failed; same-threshold simpler ablation is stronger |
| Precise original algorithm | Unestablished | ARX identification, free references, uncertainty bounds and dwell are established; elementary bounds do not establish originality |
| Compatible paper-level comparison set | Incomplete | Strong ordinary controls executed; recent functional-CP component adapted; full CASPER/edge/FAIL-Detect experiments not reproduced and close RAPIO/Kaisar access incomplete |
| Fresh confirmation | Complete for v0.8 only | New tasks/settings and pre-outcome freeze; now exposed and cannot confirm a redesign |
| Journal scope | Conditional fit | ISA Transactions includes simulation-supported analysis/design; current guide still not retrieved |
| Submission declarations and author approval | Incomplete | Haiqa affiliation, actual individual roles, funding/conflicts and both-author review remain unconfirmed |
| Journal-ready original-method paper | **Do not admit** | Scientific and author gates above are substantive |

## Specific next research decision

Reject the present uncertainty-addition rule as the proposed contribution. Retain the stronger no-allowance decision and learned-reference hysteresis as controls, not as automatically novel replacements. Before another confirmation campaign, a revised mechanism must pass a **normal-only clearance-feasibility gate**: demonstrate reachable return conditions on every declared operating regime, and distinguish reducible reference bias from uncertainty that makes clearance unidentified. An uncertainty flag should not be advertised as physical recovery.

The smallest useful next investigation is commissioning-only diagnosis of reference error versus model class, with no new attack exposure: identify whether parameter/actuator mismatch can be modeled tightly enough to support the requested clearance tolerance. Any proposed change must specify its distinction from interval/recovery prior art and give the same fitted reference to ordinary controls. Only after that distinction and normal-only feasibility hold should new attack conditions be frozen. This decision prevents another expensive confirmatory run of a rule that cannot clear by construction.

The source-backed derivations and measured results may support a focused analysis manuscript, subject to novelty assessment and author choice. They do not meet the user's intended new-method contribution by themselves. No manuscript was submitted or published and no author facts were invented.
