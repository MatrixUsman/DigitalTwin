# Comparison roster for the narrow CASPER case study

**17 October 2026. Design decision only; calibration and final admission pending.** Read with the [contribution/scope decision](CONTRIBUTION_AND_EVIDENCE_SCOPE.md), [paper admission ledger](COMPARATOR_ADMISSION.md) and unchanged [evaluation protocol](EVALUATION_PROTOCOL.md). This supersedes the earlier expectation that three recent learning papers would necessarily form our experimental ranking. It does not alter their source facts or convert background into reproductions.

## Core roster and roles

The principal question concerns an additional correction-discrepancy term within one fixed observer. The core design contains **eleven deterministic score/control variants**, seven already implemented and four still requiring a versioned implementation/normal-validation plan. All receive no more than the common q/qdot/relative-time budget; velocity subsets are declared. The same protected evaluation populations and endpoint support apply. There is no attack result for any variant.

| ID | Score / method | Why it is included | Actual readiness |
|---|---|---|---|
| O-R | Synchronized observer `R/a` | Principal residual-only reference, with nominal phase propagation and measurement correction retained | Implemented; existing full-training artifact and normal-development scores |
| O-RC | Same observer `R/a+C/b` | Principal incremental correction-evidence test, identical states/predictions to O-R | Implemented; same artifact/normal-development study |
| O-C | Same observer `C=JSD(p,q)` | Does correction alone account for the combination? | **Design only** |
| O-K | Same observer `K=KL(q||p)` | Classical Bayesian surprise, rather than implying JS belief change is new | **Design only** |
| O-L | Same observer `L=-log Σ p_k exp(-D_k/(2τ))` | Ordinary predictive mixture energy; tests a conventional alternative to mean residual plus JS | **Design only** |
| O-Rv | Same observer `Rv=(1/6)Σ_velocity(z_j-Σp_k m_kj)²` | Phase-conditioned velocity mismatch; checks whether direct speed evidence explains the outcome | **Design only**; full 12-channel observer state retained, only scoring restricted to velocity |
| V-Z | Maximum absolute standardized joint velocity | Direct amplitude evidence without phase estimation | Selected full-training velocity artifact; normal-development complete |
| T-32 | Frozen 32-bin periodic template | Repetition and a deterministic reference without the diffusive filter | Selected full-training template artifact; normal-development complete |
| AR-4 | Channelwise AR(4), ridge 0.001 | Ordinary causal prediction; strongest existing one-step normal predictor | Selected full-training artifact; normal-development complete |
| O-Follow | Existing unconstrained-following observer residual | Auxiliary state-update diagnostic; not matched to O-R's trajectory | Implemented and normal-development tested |
| O-Free | Existing free-running observer residual | Auxiliary propagation diagnostic; diffusion makes it a limited reference | Implemented and normal-development tested; do not omit T-32 |

The six same-state variants O-R/O-RC/O-C/O-K/O-L/O-Rv must share one state trajectory at each endpoint. O-Follow/O-Free deliberately change that trajectory and are labelled auxiliary. O-Rv does not refit a velocity-only observer or select phase from the current velocity residual. Position-only experiments, new phase grids, altered diffusion or new score combinations are outside this roster.

Rv quantifies velocity mismatch against the full observer's prior prediction; it does not isolate alignment's causal effect or demonstrate post-alignment residual suppression. The frozen historical protocol's “progression-aware/omitted” wording maps to O-RC/O-R, respectively, with both retaining nominal progression. Record this terminology clarification explicitly in the forthcoming versioned execution manifest; preserve the hashed historical protocol.

## Exact score semantics and extension requirements

Use the existing training-fitted standardizer, reference, transition, initialization, bandwidth and scales. For the six same-state scores, propagate from past state with actual elapsed time, form the prior prediction, inspect the current observation to compute prospective residual/update evidence, emit the scores and then commit the correction. No label, attack boundary, future measurement or current-target refitting enters this sequence. C/K/L necessarily use the current measurement to quantify correction; they are not pre-measurement forecasts.

`p` denotes the propagated phase prior, `q` the proposed corrected distribution, `D_k` the existing squared standardized 12-channel template distance divided by 12, and `τ` the pinned positive bandwidth. Natural logarithms are used. C remains the implemented Jensen–Shannon divergence, not its square-root distance. `K=Σ q_k log(q_k/p_k)` uses the conventional `0 log 0 = 0` limit. Positive prior support is expected from the declared transition, but implementation must verify it rather than silently smooth zero/invalid inputs. L is an unnormalized **energy**, not an asserted sensor likelihood or calibrated probability.

The new singleton scores C/K/L/Rv need no new tunable fusion weights or scale fitting: each later receives its own frozen-protocol 99th-percentile threshold. O-R/O-RC retain their existing training-only scales; no scale is estimated from calibration. New numerical tolerances, finite-support behavior and roundoff handling must be specified before testing/execution. Required tests include:

- Independent small-array arithmetic, identical-distribution C/K limits, KL orientation, stable log-sum-exp and underflow cases; verify `L=K+Σq_kD_k/(2τ)` where mathematically defined.
- Mixture-mean/component-distance identity and Rv's exact six-channel indexing; a synthetic phase-aligned speed-amplitude change distinguishes velocity mismatch from a position-only alignment story. Label every artificial trajectory **synthetic**, not a realistic cyberattack or benchmark result.
- All six scores share exactly the same state/prediction/reference; changing which scores are exported cannot change state updates. Training/development observations cannot modify the pinned reference after fitting.
- Causal score-before-state-commit order, label/future-suffix independence, gap/split isolation, identical complete eligible support, finite outputs, immutable sources/artifacts and preserved failures.
- Bounded runner provenance, output/storage estimates and ledger behavior. This is a new development version, not permission to remove consumed v0.1 attempt records.

Normal-only extension replay must use the existing permitted development region and immutable artifact identities, without refitting or choosing the best new score by its development distribution. Specify the exact command, source/configuration hashes, limits and admission checks in a new plan before execution. Existing normal-development reuse remains disclosed. This document itself runs nothing and does not certify implementation readiness.

## Conditional methods and claims they would be needed for

| Candidate | Disposition now | Trigger for further work |
|---|---|---|
| Deterministic causal phase alignment with progress/timing evidence | Close-prior-art control, **not implemented or admitted** | Required before claiming superiority over alignment methods or value specifically from probabilistic phase uncertainty. Define causal phase selection, history, tie/ambiguity handling and timing score; never port offline warping or attack-defined segmentation silently. Current narrow claim makes neither assertion. |
| ModernTCN (ICLR 2024) | **Conditional secondary modified-protocol transfer**, not core scientific necessity for a within-filter score question | Useful for broad competitive-performance claims, which are currently withheld. Resolve current-conditioned reconstruction versus frozen past-state prediction language, dependencies/configuration and bounded resources before any run. No published CASPER experiment exists. |
| CASPER-inspired controller CNN | Optional independent implementation; original code-use issue unresolved | Pursue only with a defined comparison role and fresh implementation derivation. Not faithful external-IMU CASPER reproduction. |
| Original CASPER / TWINE / CatBoost methods | Existing [admission designations](COMPARATOR_ADMISSION.md) preserved | External-IMU/supervised inputs and information access prevent a forced common Group D ranking. Source availability alone does not remedy this. |

The recency window remains 2023-10-16 through 2026-10-16 for main **paper** candidates. It does not exclude necessary classical controls or make recent incompatible papers preferable. The original goal of three recent same-task experimental papers is unsatisfied; the selected narrow study does not claim that goal has been met.

## Interpretation and final admission

Prespecify R versus R+C as principal. C/K/L/Rv are explanatory comparisons, not four chances to choose a new primary method after seeing attacks. Report all eleven declared variants and failures. Show common support, separate false-alarm burden, detection counts/events/delay and resource use under the frozen metrics. A conditional neural or alignment candidate can enter only through an explicit pre-final roster revision with its implementation and protocol admitted; no hidden post-test additions.

Current admission is **scientific role/design selection**. Four scores are missing implementations, the calibration/final runner is unfinished, actual threshold/model freeze is pending and no independent dataset has entered. The existing [selected controls](../experiments/SELECTED_CONTROLS_V0.1.json) and [observer registry](../experiments/OBSERVER_ARTIFACTS_V0.1.json) preserve seven existing variants; they are not edited to imply new artifacts. The previous 254-test receipt remains historical and cannot be presented as covering these unimplemented extensions.
