# Revision 1.7 execution outcome and issue register

19 October 2026. This record answers the user's execution attachment after the completed review intake. The destination remains an original, scientifically defensible improvement. Completing this bounded investigation does not establish that contribution or authorize a change to a negative-results publication objective. All new final outcomes are now exposed.

## What the experiments establish

The missing matched control is implemented and evaluated in [v0.18](../research_cycles/review_extension_v0.18/RESULTS.md). On the original exposed simulation grid, base and RBF without dwell have 1,198 and 1,195 benign alarm points, respectively, and both freshly detect 108/108 interventions. RBF therefore accounts for only three fewer benign points (0.25%) under the matched no-dwell policy. Removing dwell has the much larger effect and increases fragmentation: base starts rise 598 to 761 and RBF starts 590 to 743. Neither the matched comparison nor the original failed 10% criterion establishes an RBF contribution.

Trace diagnosis identified an interaction between noise-driven entry, legitimate command transients and persistence/clearance logic. This motivated the finite [v0.19 protocol](../research_cycles/context_recovery_v0.19/PLAN.md): two command-context memories, selected from normal development, a contextual empirical residual allowance, and separate evidence for entry and return. The same ARX reference is retained; online parameter adaptation is not introduced. Global allowances, ordinary hysteresis, point thresholds and temporal entry rules provide explanatory controls.

One frozen campaign evaluated 216 new synthetic episodes and 11 methods (2,376 method–episode outcomes): two new task families, six plant parameterizations, three paired seeds, benign changes and four corruptions. The final run used 103.197 seconds wall time, 102.722 seconds CPU, 78.42 MiB sampled RSS and 205.36 MiB output, within its declared limits. Failed cost/storage admissions and the subsequent lossless export adapter remain recorded. No new raw robot observation or test was opened.

The contextual two-sided candidate **failed its prospective composite criterion**. Against base dual, benign points decrease 42,193 to 332 and starts decrease 3,341 to 94, but p95 fresh delay increases 0.040 to 0.731 seconds, outside-tolerance inactive points increase 0 to 679, and joint successes fall 144 to 62. This is not an overall success.

The matched recovery ablation does show a component effect: outside inactivity decreases 1,016 to 679 and joint successes increase 12 to 62 versus contextual hysteresis, at the cost of benign points increasing 201 to 332. A global-envelope control already achieves 62 joint successes with 305 benign points. Context does not dominate this control. All these numbers are synthetic results, not physical operating guarantees.

The separate [independent technical review](../research_cycles/context_recovery_v0.19/INDEPENDENT_REVIEW.md) confirms 29,381 arithmetic checks and all 11 prospective clauses. Its post-evaluation decomposition identifies 299 inactive-outside points before initial detection and 380 later; 321 occur after a first sustained return followed by another tolerance crossing. Of the total 679 points, 678 are in the uncertainty band. No falling edge occurs while outside tolerance. The weakness is delayed entry and re-entry as well as the cost of conservative return evidence; it is not a demonstrated implementation violation.

## Issue register

| ID | Issue | Disposition and evidence |
|---|---|---|
| R01 | Score versus clearance readiness | Resolved as a reporting clarification. Score index 100, short-window readiness 104, long-window readiness 140 and earliest ten-step dual clearance 149 remain unchanged. No implementation bug was found or repaired. |
| R02 | Fold-specific fitting | Resolved as a wording clarification. Fixed center counts/bandwidth multipliers differ from fitted coordinates/scales/numerical bandwidth, which use permitted training data. No leakage repair is claimed. |
| R03 | Missing base no-dwell | Executed in v0.18; original streams replay exactly. The favorable no-dwell occupancy result does not materially depend on RBF. |
| R04 | Delays, fragmentation, conditional clearance | Existing outputs analyzed without retraining; timing and plant/task/intervention strata are included in reporting assets. Inactivity by return + 5 seconds is explicitly conditional and does not establish uninterrupted alarm support. |
| R05 | Task/attack definitions and physical tolerances | Exact transformations, boundary behavior, chronology and native tolerance scales documented in the revised methods and experiment sections. Tolerances are diagnostic, not certified safety limits. |
| R06 | Kaisar comparison | Accessible accepted author manuscript inspected through Eq. 31, Table 4 and Algorithm 1; version identified. Final publisher PDF and matched runnable code remain unverified. See precision note below. |
| R07 | Finite improvement study | Implemented, tested, selected on normal development and evaluated once under a prospective freeze. Overall criterion fails; no post-final selection or retrospective relaxation. |
| R08 | Originality | Open. Input-dependent thresholds, empirical uncertainty sets and hysteresis have close prior art. No new algorithmic distinction or superiority over a full published robotic-security system is established. |
| R09 | Independent real evidence | Open for online cyberattack recovery. Nominal CASPER IMU forecasting is a different task. voraus-AD is a separately received fault source whose process signals/test remain unopened; it cannot supply absent trusted commands, cyber labels or recovery truth. |
| R10 | Recent full published comparators | Open. Prior ModernTCN/iTransformer/TimeMixer executions use official model code under a modified normal-forecasting protocol and are resource-limited; they are not reproductions of complete security systems. |
| R11 | Reproducibility delivery | Updated source, configurations, saved synthetic predictions/truth, episode results, provenance and replay tools are provided locally. Consult the package's build and clean-extraction receipts for its exact tested closure; no public availability or release permission is implied. |
| R12 | Human/journal decisions | Open. Author contributions and final approval must come from the author. Journal selection, current template/policies, disclosure wording and release/permission review are pending. No submission occurred. |

## Prior-art precision note

The pre-final prior-art note is hash-bound and remains unchanged. In Kaisar et al.'s accepted Table 4, RESCUE-to-HANDOVER includes cleared severity, residual consistency and minimum dwell. Direct RESCUE-to-NOMINAL instead includes cleared severity, residual consistency and a path-error proxy bound for a run of steps; minimum dwell is not listed in that direct guard. The revised manuscript distinguishes those transitions. This clarification does not change any experimental source or decision.

## What remains before the intended contribution paper

The existing record can support a detailed report of tested mechanisms and their limitations. It does not yet support the user's intended claim of an original detector with a worthwhile overall advantage. The manuscript is a working revision for review, not a declaration of scientific submission readiness.

The next research decision should precede another experiment: identify a defensible mechanism distinction and an achievable operating objective in light of the measured uncertainty-band/re-entry limitation, or establish a compatible independent-data/comparator track. A future mechanism needs its own finite development budget, fair global/temporal controls and fresh frozen conditions. Reusing this campaign for design would be exploratory. An offline fault-detection direction would change the question and must be discussed, not silently adopted. Another open-ended search or an outcome-selected threshold is not authorized by this completed cycle.

The revised manuscript and local reviewer archive preserve the old failures and the new component tradeoff. They do not replace the original-contribution objective. The next bounded action is author/teacher review of this outcome and a concrete choice of research direction, without claiming that either has already happened.
