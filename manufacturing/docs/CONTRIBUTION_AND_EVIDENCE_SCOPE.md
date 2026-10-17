# Contribution and evidence-scope decision

**Decision date:** 17 October 2026, Asia/Karachi. **Project:** manufacturing / Haiqa Mushtaq. **Status:** prospective study-design decision; no attack result or established novel method. Prepared with the shared academic-research-suite's bounded primary-source review and synthesis workflow. Three delegated source investigations inform this decision; this is AI-assisted internal review, not external peer review or a human-reading attestation.

## Decision and proposed claim

**Proceed with a focused single-acquisition score-comparison study. Do not proceed under a claim of a new digital twin, a new phase estimator, or general manufacturing cybersecurity robustness.** The existing evidence is sufficient to motivate this narrow experiment, not to assert its outcome. A leading-journal general-method claim would need substantially more evidence and a distinct contribution; acceptance cannot be inferred from a well-audited implementation.

The proposed question is:

> On the frozen original-CASPER right-arm recording, does adding measurement-correction discrepancy to the same empirical motion observer's prospective residual provide useful detection evidence, compared with residual-only, conventional surprise/energy scores and simple controls, under the same normal-only calibration?

The contribution being investigated is a **controlled empirical assessment of scoring choices and their limitations**, with traceable data/protocol decisions. It is not the invention of phase tracking or the discovery that tracking can accommodate faults. Exact use of Jensen–Shannon discrepancy in this particular setting is not sufficient novelty on its own. The bounded search did not establish an exclusive or previously unstudied method.

Scope-corrected working title: **“Correction Evidence in Robotic Motion Monitoring: A CASPER Case Study.”** This describes a study, not a positive finding. It supersedes the earlier observer/twin titles for planning; the final title depends on actual evidence. The cybersecurity setting remains the documented command-path intervention scenario, with monitoring telemetry and time assumed truthful.

## Close prior art and what remains to test

Full identities, dates, manuscript locators, code/access limits and search records are in the [periodic-alignment audit](literature/PERIODIC_ALIGNMENT_PRIOR_ART_2026-10-17.md) and [innovation/synchronization audit](literature/INNOVATION_SYNCHRONIZATION_PRIOR_ART_2026-10-17.md). Older foundations are necessary background and reasons for controls; they do not count as recent baseline papers.

| Proposed element or claim | What primary sources already establish | Consequence for this study |
|---|---|---|
| Repetitive robot alignment, segmentation and next-observation residuals | [CASPER, 2024](https://doi.org/10.1145/3670414), §§6.4.2–6.4.5; [Kayan et al., edge robotic-arm monitoring, 2025](https://doi.org/10.1109/JIOT.2025.3569780), §§V–VI | These are close manufacturing precedents. Their external-IMU inputs, annotation uncertainty and run/protocol questions prevent treating them as identical controller-input comparisons. |
| State prediction, measurement correction and anomaly residuals | [Mehra and Peschon, 1971](https://doi.org/10.1016/0005-1098(71)90028-8); [Willsky, 1976](https://willsky.lids.mit.edu/publ_pdfs/15_pub_AUTO.pdf), §II | Our categorical observer instantiates established filtering ideas. No new-estimator claim. |
| Following a deviation can weaken fault residuals | Willsky, §III, pp.603–604, explicitly discusses gain, tracking and detection sensitivity | Do not claim to discover the accommodation trade-off; determine whether it matters here, without assuming an attack result. |
| Joint inference of phase/trajectory and future motion | [Bayesian Interaction Primitives, CoRL 2017](https://proceedings.mlr.press/v78/campbell17a.html); [Periodic Interaction Primitives, ICRA 2020](https://doi.org/10.1109/ICRA40945.2020.9196676) | Phase, periodic reference, correction and prospective prediction are established. Neither paper is a matched CASPER reproduction. |
| Progress-conditioned anomaly decisions and periodic alignment | [Park et al., ICRA 2016](https://doi.org/10.1109/ICRA.2016.7487160); [Ahrens et al., 2019](https://doi.org/10.1186/s13634-019-0619-3), including nearest-reference classification and ambiguity handling | A phase variable or progress-aware score alone is not a contribution. Superiority over alignment methods would require a separate causal alignment comparator. |
| Online unsupervised segmentation | [ClaSS, PVLDB 2024](https://doi.org/10.14778/3659437.3659450) | Segmentation is an established, distinct task. Do not use intervention boundaries as task phases or equate a change point with malicious intent. |
| Belief redistribution as anomaly evidence | [Itti and Baldi, NIPS 2005](https://papers.neurips.cc/paper_files/paper/2005/hash/0172d289da48c48de8c5ebf3de9f7ee1-Abstract.html); [Çatal et al., IROS 2020](https://biblio.ugent.be/publication/8700871); [McGarry and Nelson, 2025](https://doi.org/10.1111/exsy.70106) | Classical Bayesian surprise must be visible. The AGV abstract is verified but full text is restricted; no uninspected equation or performance claim is imported. |
| Combining residual/reconstruction error and distributional discrepancy | [Anomaly Transformer, ICLR 2022](https://arxiv.org/abs/2110.02642), §§3.1–3.2, Appendix E.2 | Generic error-plus-discrepancy fusion is not new. Different association semantics prevent claiming equivalence or importing headline scores. |
| Strong recent transferable model | [ModernTCN, ICLR 2024](https://github.com/luodhhh/ModernTCN), [local source audit](literature/REPLACEMENT_COMPARATORS_2026-10-17.md) | Conditional secondary transfer only; current-conditioned reconstruction is distinct from our prospective forecast. No CASPER result or adapter execution is established. |

Our interpretation follows source evidence, not venue rank. [Arp et al., USENIX Security 2022](https://www.usenix.org/system/files/sec22-arp.pdf), §2.1 and the evaluation discussion, supports the methodological need to disclose sampling/label bias and use appropriate comparisons; it does not validate our particular design.

## What the matched comparison actually isolates

Both existing principal scores use the **same propagated phase prior, prediction, current measurement and corrected state**. The residual already contains nominal progression information. Therefore R versus R+C removes **one correction-discrepancy score term**, not all progression, synchronization or measurement correction from the observer. Neither score changes its fitted reference during replay.

The frozen historical evaluation text calls this contrast “progression-aware/omitted.” This document clarifies that label for the same principal contrast; it does not silently amend the hashed protocol or change an endpoint. The forthcoming versioned execution manifest must explicitly map the historical wording to O-R/O-RC and their exact score semantics before admission.

Let `p` be prior phase weights, `m_k` the frozen standardized 12-channel templates, `z` the current standardized observation, and `D_k=||z-m_k||²/12`. The update uses `q_k=p_k exp(-D_k/(2τ))/Z`. The existing scores are `R/a` and `R/a+C/b`, with `R=||z-Σp_k m_k||²/12`, `C=JSD(p,q)`, and training-only scales `a,b`. The new explanatory scores are defined in the [roster decision](COMPARISON_ROSTER_DECISION.md).

Our algebra, not a new theorem, gives `L=-log Z=KL(q||p)+Σq_k D_k/(2τ)`. It also gives `Σp_kD_k=R+Σp_k||m_k-Σp_jm_j||²/12`. Thus correction can be related to ordinary predictive energy, while a mixture-mean residual can be poor because phase is ambiguous. A score gain need not establish a new physical mechanism. Jensen–Shannon discrepancy has no identical KL decomposition; neither discrepancy is a calibrated attack probability.

There is another competing explanation: under pure time reparameterization, `q(t)=q0(φ(t))` but `qdot(t)=q0′(φ(t)) φdot(t)`. Aligning position alone does not remove speed-amplitude mismatch from the velocity channels. We therefore **do not assume synchronization hides CASPER's speed interventions**. A phase-conditioned velocity-residual control is required to examine the direct speed evidence. This is an analytic possibility, not an observed attack result.

Rv is a **prior-prediction velocity residual within the full q/qdot observer**. Its results can support a direct-velocity alternative explanation; it cannot independently establish alignment's causal effect or prove post-alignment residual suppression.

## Evidence scope and limitations

| Available or missing evidence | What can be supported | What cannot be inferred |
|---|---|---|
| One repetitive acquisition; eight scheduled intervention intervals | Descriptive, within-recording detection outcomes against schedule annotations | Eight independent experiments, cross-robot/task/factory generalization, precise physical impact onset |
| Full normal-training/control/observer development with recorded provenance | Causal implementation, feasible resources and internal normal-data checks | Attack sensitivity, robustness or novel security benefit |
| Normal observer checks passed; same development reused after template selection | Internal development evidence with disclosed reuse | Independent validation or calibrated latent-phase accuracy |
| Observer one-step MSE 0.338911 versus AR 0.002094; 53.12% descriptive phase ambiguity | A strong reason to retain the simple AR and ambiguity-aware score explanations | Observer predictive superiority, phase ground truth, calibrated confidence |
| Free-running observer diffuses almost to uniform | Behavior of that particular diffusion/update policy | Failure of every fixed reference; the deterministic template remains essential |
| Controller flags copied to both arms while right-arm speed is manipulated | Dataset annotation lineage and restricted right-arm study | A second independently attacked robot from the left-arm file |
| Truthful q/qdot/time assumed; no authenticated command/context input | Detection of recorded deviations under that trust assumption | Intent, authorization, resistance to fully forged controller telemetry |
| No independently labelled legitimate changes or faults admitted | Explicit unresolved external-validity questions | Fault/attack discrimination, acceptable alarms during changeovers |

Numerical development findings above come from the existing [observer report](OBSERVER_VALIDATION_REPORT.md), not a new run. Millions of rows, recurring cycles, windows and random seeds do not create independent acquisitions. The eight intervals are dependent events in the same recording. Follow the frozen descriptive metrics; do not introduce independent-row/event/seed significance tests or confidence intervals suggesting population-level replication.

An identifiability limit follows directly from our input boundary: if authorized and unauthorized changes produce identical permitted observation histories, any detector using only those histories must give the same output (or output distribution if randomized). An extra fault dataset cannot resolve that ambiguity. Trusted commands or independent sensing would require an explicitly different threat/input track.

## Comparison and falsification commitments

The [roster decision](COMPARISON_ROSTER_DECISION.md) selects the scientific comparison set for this narrow question. It distinguishes seven existing score/control variants from four new, unimplemented explanatory scores. No three-paper ranking or execution admission is implied.

- Keep **R versus R+C** as the principal contrast. Preserve identical states, parameters, features, eligible endpoints and threshold rule. Report every declared variant, not a preferred score chosen after test exposure.
- Add correction-only C, classical KL surprise K, predictive mixture energy L, and phase-conditioned velocity residual Rv before calibration. If a conventional score accounts for the outcome, do not claim a new scoring principle. If C alone explains the outcome, do not claim the combination needs residual evidence. If Rv explains it, report direct speed mismatch as an alternative explanation.
- Retain selected velocity, fixed-template and AR controls regardless of their eventual strength. A strong simple control may remove the rationale for observer complexity.
- Report the frozen joint outcomes: unadjusted P/R/F1 and counts, held-out-normal exceedance and episodes/hour, AP, all eight event outcomes with schedule-relative delay/misses, coverage and costs. More detections with greater normal burden are a trade-off, not unconditional superiority. Do not create a post-test composite winner or change threshold budgets.
- A failed/null contrast, weak prediction, ambiguity or unsuccessful comparator is a result to preserve. Redesign after final exposure becomes exploratory and requires fresh evidence for confirmation.

No numerical success margin or power claim is invented from eight dependent intervals. No threshold, attack metric or model choice was obtained from protected observations during this task. The existing [evaluation protocol](EVALUATION_PROTOCOL.md) and pending [final freeze](../experiments/FINAL_TEST_FREEZE_RECORD.json) remain unchanged.

## Breadth decision and next bounded work

The [independent-source screen](literature/INDEPENDENT_EVIDENCE_SCREEN_2026-10-17.md) and [admission plan](INDEPENDENT_EVIDENCE_PLAN.md) recommend **voraus-AD** for a separate variable-execution/physical-fault track and **NIST UR5** for benign operating-condition evidence. These sources are not admitted or downloaded as datasets. They do not supply cyber labels merely by containing anomalies. CASPER 1 & 2 is not presumed independent; overlapping original-sized files require explicit lineage/duplicate checks.

For a broad cybersecurity paper, obtain genuinely independent, compatible cyber recordings or design an authorized testbed study with repeated acquisitions, varied tasks/conditions and matched benign/fault/attack cases. No such facility, new recording or trusted context is currently available. Until then, retain the case-study scope and withhold cross-system/intent/robustness claims.

**Stage 11 is complete as a scope-revision and comparison-design decision.** The evidence does not yet establish an empirical contribution, publication readiness or a fully executable roster. Next: specify a separately versioned, bounded score-extension plan, implement/test C/K/L/Rv and validate them on permitted normal data while preserving observer v0.1. In parallel, complete source-specific admission design for independent evidence. ModernTCN and causal alignment remain conditional on broader claims; no large neural experiment is justified merely to fill a paper quota. Calibration and both final slices remain closed until their existing gates are satisfied.

## Provenance and verification boundary

The review's claim-intent manifest and before-edit hash inventory are in ignored `local/contribution_review/`. The three source notes retain queries, versions, access failures and primary citations. Additional root searches used the terms `"Jensen Shannon" "phase" "anomaly detection" robot`, `"Jensen-Shannon" "prior" "posterior" "anomaly detection"`, `"Bayesian surprise" anomaly detection autonomous guided vehicles Catal 2020`, and `site.usenix.org "Dos and Don'ts of Machine Learning in Computer Security"`; the official USENIX manuscript and institutional AGV record were inspected. These bounded searches are not proof of novelty or an exhaustive systematic review.

This task used public literature/metadata and existing safe reports. No raw observations, new training, calibration/final replay, additional dataset admission, external messages, paid compute or publication occurred. Frozen plans, source/configuration files and artifact registries are checked against the before-review inventory at handoff. Subsequent implementation needs its own recorded plan, tests and run evidence.
