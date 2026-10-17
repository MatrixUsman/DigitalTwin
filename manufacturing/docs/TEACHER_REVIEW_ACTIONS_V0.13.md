# Teacher review and model-first revision record

**Editorial update, 18 October 2026:** [Revision 1.3 response](../manuscript_after_v1.3/REVIEW_RESPONSE.md) completes the 11-page main article, separate supplement, 20-reference expansion, model/experiments/baselines/splits/metrics/optimization/ablations/cost sections and short conclusion. Independent original voraus-AD/MVT-Flow source admission is complete at the documented metadata/static-code level. The candidate improvement and novelty gates remain failed/unresolved; faithful compatible paper-level reproduction and author approval remain open. The following v0.13/v0.14 entries are historical and are not silently rewritten.


**Subsequent scientific update, 17 October 2026:** [v0.14](../research_cycles/attack_audit_v0.14/RESULTS.md) completed the saved model's attack/recovery comparison and [novelty audit](../research_cycles/attack_audit_v0.14/NOVELTY_AUDIT.md). Seventeen controls/ablations ran on 189 synthetic episodes. The declared practical-improvement criterion failed and no distinct algorithmic contribution is established. The short window changed no alarms; the ordinary protected reference already achieves the main retention benefit. These are concrete experiments and a documented model decision, not fulfillment of the requested original contribution, compatible paper-baseline reproduction, reference expansion or ≤15-page revision. The earlier v0.13 snapshot remains sealed in its package. The [current contribution decision](../research_cycles/attack_audit_v0.14/CONTRIBUTION_DECISION.md) governs further work.

17 October 2026. The user supplied the comments below and then requested an actual proposed model. This turn therefore implemented and tested [a concrete candidate](../research_cycles/residual_twin_v0.13/MODEL_PROPOSAL.md) before another journal-manuscript revision. The existing 20-page PDF remains a historical manuscript, not a teacher-approved or submission-ready replacement. The teacher's remaining editorial requirements remain open.

## Supplied comments, preserved verbatim

> Conclusion should be short a lot of things useless is there can be shifted to supplementary material
>
> Reference increase to 20-25
> Make sure references are and valid and should be real and 75% refrences should be at least 2-3 years old papers no more old
>
> Introduction and related work is short should be more
> Contribution of our should be highlighted here at end
>
> Related work write weak points at end
>
> Total pages should be no more then 15
>
> Proposed model is missing
>
> And experiments section is missing
>
> Experimentation and datasets etc is missing baselines and valuations
>
> Evaluation matrix these 3 things in experiments
>
> Results
> 1 Optimization of proposed model and optimization tehcnuqiues
> Which are optimal parameters
>
> Machine deep learning or transformers approach
> existing state of the art studies discussions
>
> Results optimization procedures state of the art discussion
> Proposed model optimal parameters
>
> Evolution study
> Competition cost and discussion will come which summarize all this
>
> Didn’t mention baselines separately
>
> Five four validation experiments and experiments on validation
> Splitting
>
> There are many ambiguities, find a good baselines and try to extend them,
>
> use skills also. etc we have already baselines

Whitespace and paragraph spacing have been normalized; spelling is retained. These are supplied teacher comments, not independently verified teacher authorship.

## Interpretation and action map

| Request | Working interpretation / concrete action | Current disposition |
|---|---|---|
| Proposed model | Specify maintained state, prediction, learned parameters, inputs, update rules, alarm entry/return and trust assumptions; implement and test | Candidate implemented in v0.13; equations, diagram and 18 tests available. Scientific improvement criterion failed. |
| Optimization and optimal parameters | Finite, declared normal-only model selection; all candidates and selected settings | 30 fits complete, with selected settings and no omitted failures. Use “selected within the grid,” not global optimality. |
| ML/DL/transformer | Choose architecture for the question and data; explain why it is appropriate | Candidate uses a shallow RBF nonlinear head. Existing CASPER-style CNN study remains a separate input track. No transformer is inserted solely for terminology. |
| Explicit experiments | Separate data/conditions, splits, implementation, baselines, metrics and statistical units | New model proposal and results spell these out. Integration into the main article remains pending. |
| Evaluation matrix | Assumed to mean evaluation metrics plus a model/experiment comparison matrix | Proposed five-experiment matrix is documented. Ask teacher only if their intended meaning differs; do not fabricate measurements. |
| Evolution study | Assumed to mean ablation study | Base/linear/nonlinear and normal-return diagnostics implemented. Attack-component ablations remain unrun for this candidate. |
| Competition cost | Assumed to mean computational cost and comparison | Actual bounded pilot wall/CPU/RSS/output recorded. End-to-end deployment latency and per-method cost superiority are not established. |
| Four/five validation experiments | Five distinct scientific questions, with separate eligibility and evaluation rules | Defined in MODEL_PROPOSAL.md. Only initial normal-reference experiment completed; count neither software tests nor noise seeds as independent validation studies. |
| Existing baselines | Preserve manuscript-to-code correspondence and compare compatible inputs | CASPER/Edge architectural work is available but not full paper reproduction. Command/state controls share information in v0.13; no ranking against published IMU metrics. |
| Introduction and contributions | Explain the operational problem, close existing work, and exact demonstrated contribution | Expanded article prose pending evidence/claim decision. Do not label the candidate's generic components as established novelty. |
| Related-work weaknesses | End with a source-supported limitation/gap synthesis | Focused overlap note added. Distinguish inaccessible details and incompatible tasks from proved paper weaknesses. |
| 20–25 real references; ≥75% recent | Interpret as at least 75% published within the latest 2–3 years (2024–2026 preferred), not “at least three years old” | Full citation expansion still pending. For 22 references at least 17 must be recent. Verify publisher metadata, manuscript support and date/status; no padding with irrelevant papers. |
| Short conclusion, supplement, ≤15 pages | Rebuild main text around one scientific argument; move detailed historical experiments and configurations to a separate supplement | Not yet typeset. The current PDF is 20 pages and does not meet this requirement. Preserve it while preparing a new revision. |

The interpretations of “evolution,” “competition cost” and the date wording are assumptions, not teacher-confirmed requirements.

## Intended main-article organization

Aim for 14 pages including references, leaving one page of margin. Approximate allocation: title/abstract 0.5; introduction 1.5; related work 1.5; proposed method 2; experiments 2; results/model selection/ablations 2.5; discussion/limitations 1; conclusion 0.25; declarations/references 2.25. Actual rendering determines compliance.

1. Introduction: concrete monitoring problem, why current evidence is insufficient, and supported contributions at the end.
2. Related work: recent robotic anomaly detectors, model-based references/residual learning, uncertainty and recovery. End with a precise gap comparison, not unsupported criticism.
3. Proposed method: state and inputs, equations, initialization/training, trust assumptions, inference and alarm logic, cost.
4. Experimental design: datasets/simulation, information access, split identities, training/calibration, separate baselines and ablations, metrics and units of evidence.
5. Results: all declared model-selection results, unchanged primary outcomes, ablations and computational cost. Separate synthetic and real-data tracks.
6. Discussion: comparison with close methods, limitations and practical meaning of mixed/negative results.
7. Short conclusion: findings and their supported scope only.

Supplement: detailed historical runs, full candidate grid/configuration tables, extended event outcomes, source/hash inventories, auxiliary derivations and reproducibility commands. Main text retains the assumptions, main comparison, primary failures and essential limitations; moving them out would mislead readers.

## Evidence gate before a contribution-paper rewrite

The new candidate exists and runs, but adding its section cannot create a demonstrated novel contribution. The all-plant normal prediction gate failed: Q2 improved modestly; Q1 RMSE and Q3 tail error worsened slightly. All return-window diagnostics succeed equally in these normal settings, so they do not establish a proposed-rule advantage. No new attack outcomes exist. Choose a distinguishable mechanism and a measurable benefit before presenting this as the intended original-contribution paper. The next revised draft must state this status accurately if written before that evidence exists.

Skills used: academic-research-suite revision-coach and experiment planning/execution/validation guidance applied inline. This is a practical action record, not a formal full-team review certificate or completed response-to-reviewers package. User authorization to build/test the model governs the small local pilot; no paid compute, lengthy training, contact or publication occurred.
