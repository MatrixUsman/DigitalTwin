# Selecting three useful baselines for the water project

Date: **2026-10-16**. Status: **proposed selection rules and provisional learning shortlist; no three-method experimental set is approved**.

This is a project-specific research protocol, not an official industry certification or a claim that there are three universally best algorithms. The immediate task is literature selection and learning. Dataset acquisition can proceed in parallel, but experiments remain dependent on authorized access, exact releases and implementation checks.

## What “best” means here

A useful baseline makes a scientific comparison informative, fair and reproducible. We should be able to explain why it is included, run it under our information constraints, and determine what any difference in results means. A high published F1 score, a digital-twin title, journal prestige, citation count or a newer date alone does not establish this.

The selection logic follows established security-ML concerns about inappropriate baselines, data leakage, biased parameter selection, measures and threat models. These are discussed in Arp et al., [Dos and Don'ts of Machine Learning in Computer Security](https://www.usenix.org/conference/usenixsecurity22/presentation/arp), especially the [full manuscript](https://www.usenix.org/system/files/sec22-arp.pdf), sections 2.2–2.4. This 2022 paper is **methodological background**, outside our detector-baseline date window; it is not one of the three detector papers.

For time-series evaluation, [PATE, KDD 2024](https://repository.tudelft.nl/record/uuid%3A7169450d-a8e9-493a-88ba-30be018af4ab), DOI `10.1145/3637528.3671971`, examines temporal evaluation and limitations of point-adjusted F1. It is an evaluation reference, not an adopted detector or an automatic change to our metrics. Our frozen evaluation remains governed by [the reproduction proposal](REPRODUCTION_PLAN.md).

## First distinguish three kinds of selection

1. **Learning paper:** worth studying for its method, assumptions or close relationship to our question. Missing code does not prevent reading it.
2. **Eligible comparator candidate:** passes scope/date/data screening and has a credible implementation route. Some unresolved details may still require a hold.
3. **Ready experimental baseline:** exact inputs, code/specification, dependencies, protocol changes and development checks are resolved. No current method has reached this state in our workspace.

Three papers is a manageable starting reading set, not a universal publication requirement. Three papers also do not replace simple sanity controls or the fixed/ungated/gated ablations needed to test our own claim. CAROTS and CAROTS-dagger are two variants from **one paper**, not two independent papers.

## Admission rules

Record **pass**, **conditional/unknown**, or **fail for this comparison** against each rule, with evidence and the exact unresolved question. A missing fact is not automatically proof that a paper is wrong. Do not sum arbitrary points: a high relevance score cannot compensate for missing data or forbidden label access.

| Rule | Evidence we require | Consequence if unmet |
|---|---|---|
| 1. Verifiable identity and recency | Primary publisher/proceedings or arXiv record; exact title, authors, identifier and version. Main window **2023-10-16–2026-10-16**, preferably 2024–2026. Record first preprint, online publication and issue dates separately | Outside-window work is background/sanity control, not one of the three recent main papers. Do not use a late issue date to hide an earlier publication |
| 2. Publication status | Verify peer-reviewed status, corrections/withdrawals where applicable and full manuscript availability. Prefer peer-reviewed main comparators; label preprints explicitly | A preprint may remain a provisional candidate if justified, but must not be represented as peer reviewed. Venue reputation does not validate the code or results |
| 3. Both shared benchmarks | For our initial shortlist, the manuscript or supplement explicitly evaluates **both SWaT and WADI**. A name in related work, an unused loader or a third-party comparison table is insufficient | A one-dataset method is a separate transfer/reimplementation candidate or background, not a silent replacement for the agreed pair |
| 4. Same detection task and information | Normal-operation fitting and chronological process-telemetry anomaly/cyberattack detection; available sensor/actuator inputs, labels and trusted metadata documented | Supervised attack-type classification, future-looking batch analysis, network-only IDS or different simulator tasks need a separate comparison track |
| 5. Identifiable releases and comparable coverage | Original file versions, startup removals, label revisions, chronology, sampling cadence, feature roles and usable time coverage. Ultimately freeze identical authorized source files across methods | Paper-level dataset-name agreement is only screening evidence. Unresolved versions remain conditional; do not directly compare published numbers |
| 6. A reproducible implementation route | Matched author code and license, commit, architecture, training stages, hyperparameters, preprocessing, checkpoint selection and score generation; alternatively a sufficiently complete mathematical specification | “Code available on request” is unresolved until received. Independent code must be labelled a reimplementation and its missing choices documented |
| 7. Test-independent selection | Audit preprocessing fit, checkpoint choice, hyperparameter search, threshold selection, score fusion and final reporting separately. Only designated development data may influence them | If upstream code uses test labels/measurements for selection, it cannot run unchanged. A repair must preserve the method and be declared a modified protocol; otherwise hold/exclude |
| 8. Usable output and causal timing | Recover timestamp-aligned scores/decisions and actual information availability; use the same evaluator, event definitions and coverage policy | A headline aggregate score or point-adjusted predictions alone are insufficient. Do not credit alarms before their input window is available |
| 9. Measurable twin/adaptation relevance | Across the selected set, include an explicit state/prediction model and a comparator close to our update/adaptation claim. Describe state updates, parameter updates, residual calibration and thresholds separately | A paper titled “digital twin” without a specified implemented twin may remain conceptual background; a static method alone cannot test an adaptation claim |
| 10. Feasible and lawful execution | Dataset/user permission, code license, dependencies, device path, runtime and storage within an approved budget; reproducible run records | Keep a scientifically important but infeasible comparator documented as unavailable. Do not substitute a weak model without explanation or assume CPU/MPS compatibility |

Date policy proposed for consistent screening: assess a peer-reviewed paper against its first publisher/proceedings publication date, retaining earlier preprint history; assess a preprint against its first public version and keep it in the preprint category. Do not count versions of the same work as separate baselines. Exact first-online dates that cannot be verified remain unresolved.

The provider documents revisions within [SWaT](https://www.sutd.edu.sg/itrust/itrust-labs/datasets/dataset-characteristics/swat/) and [WADI](https://www.sutd.edu.sg/itrust/itrust-labs/datasets/dataset-characteristics/wadi/). Therefore “all use SWaT/WADI” does not establish identical files, labels or evaluation. See the existing [access/release checklist](DATASET_ACCESS_CHECKLIST.md).

## How the three should complement one another

| Slot | Scientific job | What we learn |
|---|---|---|
| A. Competitive non-twin detector | Test whether the twin provides value beyond a learned detector on the same observations | Practical preprocessing, representation learning and an executable comparator |
| B. Explicit model-based/fixed twin | Establish a transparent process/state prediction and residual reference | What the twin models, how it synchronizes and where model mismatch enters |
| C. Closest credible adaptive/hybrid twin method | Challenge the specific proposed update/gating mechanism | What prior work already adapts, how updates are admitted and what our hypothesis must add |

This is a recommended coverage pattern for the current question, not a rigid rule that every paper must fit one slot. If the question changes, revisit the set. Do not select three nearly identical networks just to reach a number, and do not exclude the closest prior method because it is difficult or reports strong results. If slot C cannot be reproduced, retain it in related work, disclose the comparison gap and continue searching; do not claim to have beaten it.

Methods share source releases, eligible information, development/test isolation and metric definitions. They need not have identical architectures, optimal hyperparameters or all internal transforms. Preserve justified method-specific processing, give comparable tuning opportunities, and record any extra physical information or supervision.

## Initial three-paper learning set

The subsequent [expanded search and selection report](BASELINE_SELECTION_REPORT.md) retained these three for structured study and added new reserve/prior-art findings. Use that report for the current reading sequence; this document defines the admission rules. Selection for study does not establish experimental readiness.

These are recommended **for learning and targeted audit**, not declared the three best models or an execution-ready set.

| Paper | Why learn it / how it works | Status and what still blocks numerical use |
|---|---|---|
| **CAROTS**, ICML 2025: *Causality-Aware Contrastive Learning for Robust Multivariate Time-Series Anomaly Detection* | Slot A. Causality-aware contrastive representations; study full score fusion and the no-ensemble variant. [Proceedings](https://proceedings.mlr.press/v267/kim25aa.html), [author code](https://github.com/kimanki/CAROTS) | First conditional reproduction candidate. Both datasets are recorded in the existing manuscript audit. Author code is available, but test-optimized threshold/reporting, split safeguards, alignment and device path need the documented changes/checks. Not executed |
| **IT-DT**, 2 March 2026: *Information-Theoretic Digital Twins for Stealthy Attack Detection in Industrial Control Systems: A Closed-Form KL Divergence Approach* | Slot B. A compact model chain to study: subspace identification → Kalman filtering → residual-distribution monitoring. [arXiv record](https://arxiv.org/abs/2603.01621), [manuscript](https://arxiv.org/html/2603.01621v1) | Verified version is a **preprint**, reporting both datasets. No matched author implementation is verified in our bounded audit. Release/preprocessing and window-selection provenance need resolution. Any manuscript-based code would be our reimplementation |
| **Digital-twin/deep-learning ensemble**, Scientific Reports, 22 May 2026: *A digital twin and deep-learning ensemble for cyber attack detection in industrial control systems at the IoT edge* | Slot C. Study the distinction between residual alarm gating, state assimilation, threshold adaptation and parameter updates. [Publisher/full text](https://www.nature.com/articles/s41598-026-53863-z) | Reports both datasets and describes adaptive behavior, making it useful close prior art. Public runnable author code is not verified; the availability section promises code. Existing release/day-split/cadence and normal-certification questions keep execution **on hold** |

The third recommendation is a **critical reading priority**, not a quality endorsement. Its described update behavior is relevant to the question; its unresolved evidence is a reason for careful reading, not for accepting its results. CDT remains a direct-twin reserve and DPDGAD a graph-method reserve under the [existing audit](LITERATURE_EVIDENCE.md).

If we insist on **three peer-reviewed methods with runnable author code**, this learning set does not satisfy that requirement. We should continue searching and retain blank experimental slots instead of weakening or concealing the rule. Reading a preprint is useful even if it never enters the main comparison.

## A compact candidate record

### Additional bounded search in this session

Three additional non-twin leads were checked by a read-only research worker. These are screening findings, not executed reproductions or an exhaustive search. Mutable repository branches were inspected without pinning a commit in this pass; any later code admission must pin and recheck them.

| Lead | Observed primary evidence | Current disposition |
|---|---|---|
| **CCM-TAD — Cluster-Aware Causal Mixer for Online Anomaly Detection in Multivariate Time Series** | [ICML 2026 / PMLR 306](https://proceedings.mlr.press/v306/murad26a.html), conference 6–11 July 2026; [arXiv 2506.00188](https://arxiv.org/abs/2506.00188), first preprint 30 May 2025. Both SWaT/WADI in the [author manuscript](https://arxiv.org/pdf/2506.00188), Appendix C. [Author-lab MIT code](https://github.com/Secure-and-Intelligent-Systems-Lab/CCM-TAD) | Recent reserve, not an upgrade to ready. The inspected [training implementation](https://raw.githubusercontent.com/Secure-and-Intelligent-Systems-Lab/CCM-TAD/main/exp/exp_anomaly.py) calls test evaluation each epoch and uses test F1 for checkpoint/optimization decisions. It requires more than a threshold replacement. WADI 2017 is reported; exact SWaT files and common release equivalence remain unresolved |
| **CATCH — Channel-Aware Multivariate Time Series Anomaly Detection via Frequency Patching** | [ICLR 2025 proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/hash/2b25c39788e5cf11d3541de433ebf4c0-Abstract-Conference.html), [arXiv 2410.12261](https://arxiv.org/abs/2410.12261), first preprint 16 October 2024; [author code](https://github.com/decisionintelligence/CATCH). The [proceedings manuscript](https://proceedings.iclr.cc/paper_files/paper/2025/file/2b25c39788e5cf11d3541de433ebf4c0-Paper-Conference.pdf), section 4 and Appendix A.1, includes SWaT but no WADI evaluation in its listed datasets | Excluded from our strict published-both-datasets starting set. This does not prove its algorithm cannot run on WADI; such an extension would be our evaluation, not a previously reported shared-pair experiment |
| **SensitiveHUE — Multivariate Time Series Anomaly Detection by Enhancing the Sensitivity to Normal Patterns** | Candidate KDD 2024 DOI `10.1145/3637528.3671919`; [publisher retrieval](https://dl.acm.org/doi/10.1145/3637528.3671919) failed in this pass. [Repository](https://github.com/yuesuoqingqiu/SensitiveHUE) contains SWaT/WADI configuration, but its README still says under review | Hold: publication/full-text identity, dates, dataset claims, license and complete protocol need verification. Repository configurations alone do not pass rule 3. No main-comparator admission |

These findings support retaining CAROTS as the first conditional practical baseline while auditing the twin slots. They do not establish that CAROTS is the strongest-performing algorithm.

### Record template

For each candidate, save one record linked from the evidence table:

```text
Identity: title, authors, identifier, versions, publication dates, review status
Role: A/B/C or background; why it tests our question
Data: SWaT and WADI manuscript locators, exact releases or unknown
Information: features, physical metadata, labels/supervision, causal timing
Method: equations/stages; twin/update definitions where relevant
Preprocessing: rows/features/gaps/scaling/windows/score alignment
Selection: validation, checkpoints, tuning, threshold, score fusion, test access
Evaluation: unadjusted point/event metrics, latency, coverage, false alarms
Implementation: author linkage, URL, license, commit, dependencies, commands
Limitations: source-supported versus audit-inferred; unresolved questions
Decision: learning / eligible-conditional / hold / ready / excluded-for-this-set
Reason and next action; audit date and evidence locators
```

## Search and decision procedure

1. Search primary proceedings/publisher records and full manuscripts using combinations of `SWaT WADI`, `digital twin`, `adaptive`, `drift`, `anomaly detection`, `state estimation` and `code`; constrain publication dates using primary metadata.
2. Follow relevant papers' references and forward citations to identify close alternatives, then verify the primary records. Search-engine hits and repository stars are leads only.
3. Screen scope, dates, both datasets and task first. Deduplicate preprint/published versions. Record exclusions with a specific reason.
4. Read methods/experiments/appendices; inspect matched repository entry points. Audit selection and evaluation separately rather than accepting the README's score.
5. Keep methods conditional until release compatibility and a credible implementation route are clear. Select the best-supported set by role, information fairness, reproducibility, relevance and feasible cost, with written trade-offs—not a fabricated numeric ranking.
6. Discuss the final three-paper learning set with the researcher; do not infer that reading a paper authorizes its code execution or establishes human understanding.
7. Admit methods to execution only after data and development checks. Freeze the selected methods/variants before final test scoring; never replace a baseline because its measured test score makes our method look worse.

**Immediate priority under the user's latest instruction:** apply this screen and complete the three-paper learning/comparison decision before implementation. Start by reading CAROTS and checking the two twin roles. Access preparation remains useful independent work and does not require waiting for literature selection to finish.

## Scope of this update

Applied the installed ARS bounded source-verification guidance, with project rules overriding generic medical evidence hierarchies and approximate-match citation shortcuts. Primary evaluation references, provider pages, CAROTS proceedings, IT-DT record/manuscript and the ensemble publisher sections were checked. Existing audit findings remain linked with their limits. No exhaustive systematic review, independent performance validation, dataset acquisition, code execution or final three-baseline admission is claimed.
