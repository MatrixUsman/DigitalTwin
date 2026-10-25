# Review of the two supplied v1.6 texts

19 October 2026. Active project: manufacturing. This is a review intake and targeted evidence check, not a manuscript revision, a new experimental protocol, or an author-approved change of contribution.

The user's request was to go through both attachments carefully. The first contains a scientific critique; the second proposes a comprehensive execution brief. Imperatives inside the second attachment have been assessed as proposed work, not silently executed. Neither document is identified as an actual journal decision letter. No editorial obligation or completed human review is inferred.

## Source identity and review scope

Both attachments were read in full. Their supplied attachment IDs and SHA-256 identities are:

| Source | Attachment ID | Bytes | SHA-256 |
|---|---|---:|---|
| A — critique beginning “Usman, I would not submit version 1.6 yet” | `f2f8910d-39c3-4e14-adca-9c8f1da0c40d` | 22,202 | `4e588c0fa9b4f7fa9591423d1574c8a885a3ee6aeef1b474876539db270b78f0` |
| B — proposed execution brief beginning “Work directly in this research repository” | `1c80222c-c941-4d04-8426-c4cc8c90de64` | 23,796 | `3958f710d4ac6868b7d4d2e203040ad7be2e5358667d8417fddd3b5755b04201` |

Reviewed against the sealed [v1.6 source](../manuscript_arx_rbf_v1.6/README.md), research code, saved result summaries, current instructions and primary-source literature. The existing PDF remains 276,192 bytes, SHA-256 `7340da1c62f2c894f0e6a64d63f9d4c56adb62595ff61015fa7f60703331716e`. Starting Git revision: `3139d7bd863b47372e0ff2329c312e2a7625ebc1`; starting working tree clean.

The academic-research-suite revision-coach guidance informed interpretation. A separate AI agent checked code and saved artifacts. Another checked the prior-art lead and returned preliminary findings before a model-capacity failure; the primary assistant independently reopened and checked the accessible source. This is AI-assisted verification, not independent human peer review. No new experiment, training, original dataset inspection or PDF rebuild occurred.

## Assessment

The critique's central concern is supported: the tested RBF correction has not established a worthwhile reliable improvement, and the present work does not yet fulfill the user's original-method contribution objective. Stronger wording or another title cannot resolve that gap. The second text is a useful proposed work specification, but its default empirical-study direction is a substantive choice, not an accepted replacement for that objective.

Saved v0.14 summaries agree with the review: base dual and RBF dual have 7,156 and 7,012 benign alarm points; fresh detections are 101 and 105; both overlap 108 attacks; gap points increase from two to three; Q1 benign points increase from 2,397 to 2,522. The 2.01% reduction misses the declared 10% benefit target. RBF no-dwell has 1,195 benign points but approximately 1,501 starts/hour versus 1,191.9 for RBF dual. These rates derive from only 0.495 pooled eligible benign hours. The original failed outcome remains controlling. See [v0.14 results](../research_cycles/attack_audit_v0.14/RESULTS.md).

The [five-fold report](../research_cycles/fivefold_v0.16/RESULTS.md) and [recent-forecast report](../research_cycles/forecast_baselines_v0.17/RESULTS.md) support the review's distinctions: RBF improves two of five pooled folds and five of fifteen plant–fold pairs; the nine recent-model runs stop at CPU admission and report development prediction errors. These are neither new independent robot acquisitions nor a matched attack/recovery comparison.

## Targeted findings against implementation

| Concern | Verified evidence | Classification and implication |
|---|---|---|
| 1,100 eligible scores versus complete clearance windows | [Residual gate](../research_cycles/residual_twin_v0.13/model.py), lines 94–103; [audit inference](../research_cycles/attack_audit_v0.14/audit_core.py), lines 45–55. Entry starts at zero-based index 100. Prefix residuals do not populate clearance windows. Five-point readiness starts at 104; 41-point readiness starts at 140. A ten-step qualifying clearance can first occur at 149. | Reporting ambiguity, not a demonstrated denominator error. Explain separate scoring and clearance readiness. Methods already mention complete post-prefix windows; the algorithm can be more explicit. |
| RBF centers and bandwidth across folds | [Fold fitting](../research_cycles/fivefold_v0.16/core.py), lines 31–41, calls [training-only correction fitting](../research_cycles/residual_twin_v0.13/model.py), lines 45–69. Actual means, scales, centers, numerical bandwidth and coefficients are refitted. Fixed choices are order, center count, width multiplier and ridge. | No full-data fitted-center reuse evident in the checked path. Clarify experiments.tex:78. Retrospective selection still prevents treating this as nested independent validation. |
| Invalid history | Gate known status uses cumulative validity; invalid history resets the streak and retains an active alarm. The final inference interface rejects incomplete observations. | Document the behavior; the completed campaign does not validate missing-data operation. |
| Missing matched no-dwell method | Frozen [config](../research_cycles/attack_audit_v0.14/config.json) and audit_core.py:37–43 include `rbf_dual_nodwell` but no matching base variant. | Genuine comparison gap. A new base no-dwell result on exposed conditions would be an exploratory extension; preserve the original 17-method roster. |
| Missing timing distributions | [evaluation.py](../research_cycles/attack_audit_v0.14/evaluation.py):23–48 records detection/fresh delays, return indices, clearance delays, misses and already-inactive flags. Saved `local/attack_audit_v0.14/runs/audit_001/outcomes.json` contains 3,213 records. | Reporting/analysis gap. Summaries can use saved outcomes without training or new simulation. Misses and absent/censored clearance must remain visible. |
| Real-time cost | worker.py:65–72 records 189 shared whole-episode inference times. | Existing timing cannot establish per-method, per-step latency. That claim would require a separate measurement. |
| Short gate inequality | Score is the infinity norm of the same standardized residual. Saved RBF thresholds are approximately 0.03696633, 0.03712238 and 0.05740000, all below 0.1. | Five complete valid non-exceedances force the short-window mean below 0.1. Earlier residuals can still delay the qualifying streak; universal redundancy is not established. |
| Meaning of “Clear 108/108” | evaluation.py:44–48 counts an alarm already inactive at physical return as delay zero. | Disclosed definition, but the label can mislead. “Inactive by return + 5 s” is more literal. A joint detection/support/clearance outcome would be additional exploratory analysis on existing results. |

## Closest prior-art access update

The [KFUPM institutional record](https://pure.kfupm.edu.sa/en/publications/a-digital-twin-based-cybersecurity-architecture-for-fdi-anomaly-d/) identifies Kaisar et al. as a peer-reviewed 2026 article in *IEEE Open Journal of the Communications Society*, volume 7, pages 12709–12728, DOI [10.1109/OJCOMS.2026.3739185](https://doi.org/10.1109/OJCOMS.2026.3739185).

The [public manuscript text](https://www.researchgate.net/publication/415129086_A_Digital_Twin-based_Cybersecurity_Architecture_for_FDI_Anomaly_Detection_and_Isolation_in_Next_Generation_Robotic_Vehicles) now exposes Table 4, Eq. 31 and Algorithm 1. It explicitly identifies itself as an accepted, not fully edited author version; its opening dates/DOI contain template placeholders. Exact first-online date and final-PDF identity remain unverified. Direct PDF retrieval did not succeed in the delegated check.

Table 4 combines alarm severity, observer consistency and recovery conditions. Eq. 31 measures sliding observer agreement. Algorithm 1 synchronizes the kinematic estimate to the EKF in NOMINAL and resets it to the last trusted state when entering RESCUE. Therefore, its reference is not globally measurement-decoupled. It addresses pose-sensor corruption and control handover, whereas our study monitors downstream command corruption against a protected reference. That difference does not itself establish novelty. The old full-algorithm-inaccessible statement needs updating in a future revision; complete comparator admission remains unfinished.

## Concern coverage and proposed dispositions

Source order is retained below. Actions are proposals, not completed revisions or inferred author commitments.

| Source | Concern and manuscript surface | Disposition / evidence required |
|---|---|---|
| A §1 | Interpretation of original results; results/discussion | Preserve failed criterion, plant worsening, gap increase and inconsistent prediction benefit. Verified against existing reports and saved aggregate evidence. |
| A §2 | Equations, trust boundaries, honest metrics and readable presentation | Preserve these strengths. Reviewer found no obvious mathematical error; that is not a full proof/implementation validation. No new complete derivation audit or visual QA was performed here. |
| A §3A | Originality; title/abstract/introduction/conclusion | Contribution gap remains. State a mechanism or precise new empirical knowledge and the evidence it needs. Do not adopt the suggested title or change the intended paper destination automatically. |
| A §3B | Kaisar comparison; related work/discussion/reference 17 | Access obstacle partly resolved as above. Complete version-qualified method comparison before an originality argument or implementation admission. |
| A §3C | Industrial scope and independent evidence; data/methods/limitations | Three parameterizations share one simulator family; nominal IMU forecasting does not validate recovery. Stronger simulation can support a scoped virtual study. New seeds alone do not provide external validity. |
| A §3D | Recent forecasters and 17-method roster; experiments/results | Keep task/history/budget correspondence explicit. More forecasting training is not automatically the missing recovery comparison. Counts of controls are not counts of reproduced published systems. |
| A §3E | Practical benign burden; results/discussion | Report occupancy, fragmentation, exposure, delay and continuity together. No universally acceptable alarm rate or operational advantage is established by the 10% experimental target. |
| A §3F | Timing, clearance name and return tolerance; metrics/results | Saved timing summaries and literal labels can improve reporting. Express each plant/channel's standardized tolerance in native units. Define a joint outcome before using it; mark old-data analysis exploratory. |
| A §3G | Accessible reproducibility; experiments/availability/appendices | Hashes and a LaTeX archive do not supply executable research materials. Package exact K13/L13/M13 definitions, command transforms/boundaries, fitted artifacts, 15 plant–fold outcomes, metrics and figure regeneration. Local reviewer packaging need not entail public release or a second manuscript supplement. |
| A §3H | Declarations | Move unfinished author tasks outside submission prose in a future revision, while retaining pending status and truthful AI disclosure. Sole-author instruction does not prove scientific approval. Independent human review is not a universal venue requirement. No venue is currently selected. |
| A §4 | Buffers, folds, missing control and uncertainty | Findings above distinguish ambiguity from comparison gaps. Paired condition-level analysis must preserve dependence; adjacent rows and computational seeds are not independent robots. |
| A §4 | Short window and sensitivity | The conditional inequality is supported. Any sensitivity experiment needs a purpose, fixed settings, selection rule and bounded protocol; final attacks cannot select an operating point. |
| A §5 | Structure and figure legibility | Reduce repeated qualifications and operational logs while retaining scientific limits/budgets. Check Figure 7 readability in a future build. Preserve the user's one-paper, no separate supplement and 15-page requirements. |
| A §6 | Proposed revision sequence | A useful recommendation, not an editorial acceptance requirement or authority to launch work. Its empirical contribution choice requires reconciliation with the existing objective. |

The second attachment substantially covers those concerns. Its extra implementation requirements are accounted for as follows:

| B section | Assessment / pending evidence |
|---|---|
| 1–2: workspace and register | Preserve sealed versions and existing user work; this intake records verified concerns. The embedded execution instruction has not launched its pipeline. |
| 3: original findings | Supported; keep originals, verified corrections, exploratory analyses and fresh frozen outcomes distinct. No new code defect invalidating the central numbers was demonstrated in this check. |
| 4: exact methods and focused tests | Concrete and useful. Full command generation, evaluator isolation and complete support audit remain future work; targeted checks above are narrower. |
| 5: closest literature | New access verified; complete comparison with Kaisar, RESCUE and relevant observer/correction literature remains pending. |
| 6: contribution | Empirical direction is evidence-compatible but not yet the user's chosen replacement objective. Positive results are not required, and a new mechanism is not established. |
| 7: matched control/sensitivity | Scientifically relevant proposals. Original exposed results cannot confirm an outcome-informed improvement. No new experiment performed. |
| 8: fresh evaluation | Freeze justified condition families and all decisions before exposure. More simulator runs do not become independent physical acquisitions. No protocol or new campaign admitted here. |
| 9: real data and published methods | Correct task and information-access boundaries; retain untouched-test protection, licenses and full-versus-modified reproduction distinctions. No new dataset opened or comparator admitted here. |
| 10: timings/cost/uncertainty | Much can use stored outputs. Operational latency needs appropriate measurement. Joint metrics, native tolerances and defensible paired uncertainty remain to be produced. |
| 11: bound diagnostics | Assumption-satisfying versus misspecified tests, supplied versus estimated bounds, and false-certificate denominators need separation. Zero observed failures is not a rare-event guarantee. |
| 12: reproducibility package | Prepare local replay/generation instructions with lawful data acquisition and license exclusions; test in a clean environment. No public-access claim or publication is authorized by an archive's existence. |
| 13: manuscript/declarations | Evidence-led revision is appropriate; preserve one-paper constraint, current title until a new choice, and actual approval status. Funding/conflicts were previously answered; do not invent further author attestations. |
| 14: final deliverables | Useful acceptance checklist for a future execution task. Compilation/software checks alone cannot establish scientific readiness. Author approval and journal-specific requirements remain distinct. |

## Handoff

The review is complete at intake level. A bounded next task could assemble the exact prior-art comparison, reconstruct missing descriptive timing/condition summaries from saved evidence, and specify the matched base no-dwell comparison. These steps would clarify the available contribution before another model or training study. They have not been executed by this intake.

No current title, contribution decision, model, threshold, frozen campaign, manuscript, PDF or submission declaration was changed. Original voraus-AD test signals remain unopened. Publication, external contact and paid or lengthy compute retain their existing authorization requirements.
