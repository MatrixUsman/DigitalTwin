# Scientific decision after normal-only reference development

17 October 2026. The user-authorized normal-only milestone is complete. No attack experiment was run. The AFTER title remains provisional; existing manuscript claims/results were not rewritten.

## What changed and what it establishes

A predeclared search chose ordinary ARX orders 8/16/32 for Q1/Q2/Q3, reducing normal prediction errors relative to the same-initialization ARX(4). Its fitted scales and baseline coefficients were verified against the original artifacts. This is measured reference-model improvement within the declared simulator, not original algorithmic novelty. FIR, one-step following and command-as-state controls remain visible, as do every candidate and failure.

The recovery rule becomes algebraically reachable on Q2 and clears all 108 normal probes, but its qualifying-point fraction is 93.32%, below the frozen 95% rule. Q3 remains algebraically infeasible because its empirical allowance is 0.117495 > 0.1. The full normal-admission criterion fails. Do not weaken the consumed gate or reuse the fresh normal scenarios as unseen evidence.

The post-study Gaussian diagnostic identifies a second obstacle. With the simulator's Q3 sensor noise and a hypothetical perfect reference, a maximum allowance estimated from 5,500 independent normal points leaves enough margin for 95% population feasibility with probability about 2.19e-9. This is conditional on the declared noise/scales and concerns the specific maximum-plus-discrepancy construction. It is not a universal recovery impossibility result. Dwell alone cannot fix its poorly allocated noise margin.

## Concrete requirements for the replacement

1. Keep the selected references as ordinary controls. Give any proposed mechanism and its simple competitors the same fitted models, inputs, initialization and normal-data budget.
2. Separate reference bias, measurement noise and uncertainty about physical deviation. An empirical maximum of noisy residuals cannot be treated as a clean bound on model error and then indiscriminately added to another noisy observation.
3. Define what evidence would support physical return over a short causal window under approved commands. Distinguish estimated return, abstention due to insufficient evidence and alarm clearing. No hidden true state or attack-end label may enter the decision.
4. Compare the replacement with ordinary residual averaging, likelihood/equivalence tests, state estimators with covariance and same-reference fixed-return/hysteresis rules. A familiar confidence interval, average or sequential test is a control, not an automatic contribution.
5. Before any attack campaign, require a new prospectively specified normal-only check of attainable false-clear/abstention trade-offs, including correlated/misspecified noise, bias and legitimate command changes. Selected model orders must not be retuned on the exposed H/I/J results.
6. Only if a concrete distinction from close prior art and normal feasibility are both established, freeze a complete alarm machine, compatible paper methods, meaningful fresh attack/plant conditions and all outcomes. No author approval or journal readiness can be inferred from this development result.

The immediate next design problem is **a noise-aware return decision that can distinguish persistent physical deviation from uncertain measurements without learning the deviation into its reference**. Its formula and novelty are not finalized. The close interval/recovery and robot-identification papers must be confronted at the mechanism level; original CASPER/edge and FAIL-Detect are still not faithfully reproduced under this command-driven simulation.
