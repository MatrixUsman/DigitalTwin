# Contribution decision after the frozen attack audit

17 October 2026. This decision uses the complete v0.14 run and the source audit; it was written after joint evaluation. The original objective remains a publishable, original manufacturing-security contribution.

## What the evidence supports

The working model was tested against 16 controls and ablations on 189 synthetic episodes, including 108 unauthorized-command interventions. Models and thresholds were fixed before these outcomes. Every registered run completed, and the saved results passed 30,448 verification checks.

| Proposed claim | Decision and evidence |
|---|---|
| The implemented reference can predict without following corrupted physical motion | Supported within the simulator and protected-command assumptions. After initialization, changing measured states leaves the protected predictions unchanged. This is an implementation property, not a new concept or sensor-attack guarantee. |
| The nonlinear correction improves the useful detection/recovery trade-off | The declared criterion failed. Compared with the same base reference and gate, benign alarm points fell from 7,156 to 7,012 (2.01%, below the required 10%); one plant worsened and pre-return gap points rose from two to three. |
| The short recovery window adds value | No alarm changed when this component was removed across all 189 episodes. It has no demonstrated contribution in this experiment. |
| A protected reference retains evidence better than an observation-following predictor | Supported for this synthetic comparison. With the same return rule, the base reference had two pre-return gap points; the following predictor had 2,970. The ordinary base model already achieves the benefit. |
| The candidate is the best attack detector | Unsupported. The following point detector has stronger schedule F1 (0.9202 versus 0.6407), while clearing earlier relative to physical recovery. Schedule detection and recovery monitoring are distinct objectives. |
| The model is algorithmically novel | Not established. Residual compensation, RBF corrections, command-driven prediction, accumulated evidence and window/dwell alarm rules have close precedents. The audit identifies overlap and remaining access gaps; it is not an exhaustive absence proof. |
| The model outperforms CASPER or Edge CASPER | Not tested here. Their IMU prediction tasks and available inputs differ from this command/state simulation. These controls are not full paper reproductions. |

The single registered early-clear event for the candidate occurs near attack onset while true physical deviation is still below tolerance. It remains in the frozen metric, but is not evidence of clearance during a large remaining deviation. A separately labelled post-study diagnostic in [RESULTS.md](RESULTS.md) explains this distinction for every method. No safety claim follows from either calculation.

## Research decision

Keep the tested code, reference fits, complete outcomes and failed criterion. Do not promote the RBF-plus-dual-window assembly as the manuscript's established improvement. Do not choose the no-dwell ablation retrospectively and describe this same experiment as fresh confirmation of it. The source audit and experiment have answered the requested question: this candidate currently lacks both a demonstrated distinct mechanism and the declared practical advantage.

The useful finding is a measurable separation between detecting a corrupt command interval and monitoring the motion that remains afterwards. A new contribution must solve a specific unresolved part of that problem under justified information access. Reusing a standard protected reference alone would not establish originality.

## Next bounded investigation

Start with independent evidence and a compatible published method before designing another component:

1. Audit the latest FactoryNet manuscript, author code and dataset card at exact revisions. It is a promising public-data lead because its schema distinguishes setpoints from feedback. Resolve older repository descriptions against manuscript v5; separate real recordings from simulation and repackaged sources such as voraus-AD.
2. Establish permissions, downloadable release identities, timestamps, session/task/robot grouping, and command/measurement correspondence from metadata. Admit selected observations only after that check. No FactoryNet observation was downloaded or opened in this task.
3. Determine whether its labels support faults, cyberattacks, or only nominal motion. Protected commands and independently known recovery must not be inferred from a column name. Fault data could validate reference accuracy; it would not by itself confirm cybersecurity effectiveness.
4. Map the closest executable baseline to the actual permitted signals, fit/selection rule and outputs. Separate normal-only evaluation from supervised methods and original-paper metrics. Resolve code-use terms before executing imported software.
5. Choose a new mechanism only if this audit identifies a concrete limitation that ordinary reference, following, persistence and accumulation controls do not already address. Predeclare the claim, comparison, cost and fresh evidence before attack outcomes are inspected.

This is a plan for the next investigation, not completed dataset admission or a new accepted model. No physical laboratory is required for the plan. Public recordings and clearly labelled simulation remain the authorized direction; the simulation conditions consumed here are now exposed.

## Manuscript consequence

The current PDF remains unchanged. These results may support methods-development notes and an honest limitations discussion, but they do not satisfy the intended original-contribution claim. The teacher's reference, structure and page-limit requests remain tracked separately. Author approval, a compatible paper comparison and a defensible contribution are still needed before a submission-ready claim.

Sources and access limits: [novelty audit](NOVELTY_AUDIT.md). Full numbers and figures: [result report](RESULTS.md). Frozen specification: [plan](PLAN.md).
