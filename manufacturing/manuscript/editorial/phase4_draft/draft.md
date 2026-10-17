# Body

## Introduction



A motion monitor for a repetitive robot must account for where the robot is in its task. The same joint position can be expected at one stage and inconsistent with another. Existing robot-monitoring studies use temporal alignment, prediction or execution progress to make this distinction: CASPER evaluates motion anomalies using external inertial measurements, while progress-dependent monitoring and Bayesian interaction primitives explicitly represent temporal state . These precedents motivate a precise question about an observer's output: does the evidence contained in a measurement correction improve detection beyond its prospective prediction error?


Prediction and correction serve different purposes. A predictor estimates the next observation from available history. A measurement update then changes the state estimate to account for the new observation. Innovation-based failure detection and the relationship between tracking sensitivity and residuals are established topics . Likewise, posterior-to-prior divergence is an established measure of Bayesian surprise . Their existence does not imply that combining a residual with a correction statistic will improve a particular security monitor. A normal observation can legitimately change a phase estimate, and an abnormal observation can be poorly explained without greatly redistributing phase weights.


We examine that question on the original CASPER right-arm recording using joint positions, joint velocities and relative elapsed time. A fixed empirical phase observer supplies a prospective residual and a Jensen–Shannon correction discrepancy. The primary comparison adds the discrepancy to the residual while holding the observer trajectory, observations, fitted reference and evaluation support constant. Both variants already incorporate nominal progression. This comparison therefore isolates an added score term, not the presence of progression or a new state estimator.


The study provides three bounded outputs: an explicit same-observer comparison with classical surprise and ordinary controls; a complete chronological evaluation that separates normal calibration from final outcomes; and a reproducible record of the resulting detection–false-alarm trade-offs. All eleven deterministic methods are retained. The scope is a descriptive study of one acquisition, not a claim that phase estimation or score fusion is new, nor a reproduction of published CASPER performance. We use the term empirical motion observer: the implementation has measured-state correspondence and causal synchronization, but no validated robot dynamics or independently calibrated physical-state uncertainty.


The findings support only a small correction-score effect. Absolute detection is weak, and simple controls match or exceed several observer outcomes. Reporting this result requires more than counting event hits. A detector that alarms often during normal motion can intersect every long intervention interval while recognizing few of its positive observations. We therefore examine point metrics, alarm episodes, complete event outcomes and schedule-relative delays together. This choice follows the broader need to align security-learning evaluation with the information and operational setting being claimed .

## Related work and comparison scope




## Robot monitoring and digital-twin frameworks.

CASPER uses an external inertial measurement unit (IMU), periodic/statistical references and learned next-observation predictors to detect altered arm motion . Its later edge-computing study combines task segmentation with prediction on external IMU signals . Our controller-input experiment changes the observation and trust boundary. Consequently, published scores from those experiments are not entries in our numerical comparison, and our implementations are not called CASPER reproductions.


TWINE describes a digital-twin and explainable-learning framework using a supervised random-forest classifier. Its accepted manuscript specifies an 80/20 train–test split using train_test_split and labelled training examples . Our fit and model-selection partitions contain normal observations only and are chronological. Moving TWINE into this task would change its supervision and input protocol; retaining attack-labelled training would instead change ours. We therefore treat it as related framework work rather than an admitted normal-only comparator. We do not reproduce its cloud deployment or make a standards-compliance claim for our observer.



## Phase, alignment and prospective prediction.

Bayesian Interaction Primitives jointly infer phase, phase velocity and trajectory state . Periodic Interaction Primitives address repeated motion through periodic representations and observation-conditioned inference . Park et al. use a hidden Markov model (HMM) with a distribution over execution progress and a progress-dependent anomaly threshold . These works establish that phase-aware monitoring and state correction are not new by themselves. Their platforms, modalities and tasks differ from the present recording. We neither import their reported performance nor claim superiority over implementations that were not run.



## Residual and distributional evidence.

Classical innovation monitoring separates prediction error from state correction . Bayesian surprise measures posterior-to-prior Kullback–Leibler (KL) divergence . Anomaly Transformer combines reconstruction error with a discrepancy between attention associations ; those associations are not our phase probabilities. These precedents motivate retaining KL surprise and predictive mixture energy alongside the chosen Jensen–Shannon statistic. They also preclude a generic novelty claim based on combining error and discrepancy.


Our comparison set is defined by the narrow scientific question. It contains a matched residual/correction pair, explanatory scores from the same observer, two state-update variants and three ordinary controls. It does not establish competitive performance against the full recent neural-detection literature. The project's recent-paper screen covered 16 October 2023 through 16 October 2026; older references here are methodological foundations, not recent experimental baselines. Source versions, manuscript-access gaps and paper-to-code decisions are recorded in the accompanying reference and comparator registers.

## Problem, threat model and data




## Observation and trust boundary

At observation index [math], the monitor receives six actual joint positions [math], six actual joint velocities [math], and elapsed native time [math]. Positions and velocities are interpreted in radians and radians per second, respectively, following the audited controller-field mapping. The model cannot use labels, source-row identifiers, absolute clock values, commanded targets, safety status, current, torque, other-arm channels, network traffic or external IMU measurements. Source coordinates remain available to the evaluator for alignment. The velocity control intentionally uses only the six-velocity subset of the shared information budget.


The restricted adversary alters the command/application path governing motion speed while the monitoring telemetry and its clock remain truthful. The dataset does not establish authenticated telemetry or resistance to compromised controller firmware. The study asks whether scheduled speed interventions produce detectable deviations under this assumption. It does not identify the adversary's entry point, infer malicious intent, distinguish faults from authorized changes, or demonstrate mitigation. If authorized and unauthorized actions produce identical permitted observation histories, a detector using only those histories cannot distinguish them. That is an input-identifiability limit, not an empirical failure rate estimated here.



## Release identity and annotation meaning

We use the original CASPER provider collection, version 3, rather than the separate later ``CASPER 1 & 2'' listing . The selected original file is dataset/right_arm.csv, containing 1,762,650 data rows. Its byte size is 1,978,193,094 and its SHA-256 identity is given in Appendix . The file was retained unchanged. Our right-arm route is distinct from the externally sensed detection experiment described in the CASPER paper .


Local schema and annotation audits established twelve selected joint-state channels, native controller timing and eight contiguous positive flag intervals. The flags describe a scheduled intervention program. They are not independently measured physical-impact onsets, and a zero flag after an intervention is not proof of complete physical recovery. Matched capture-source inspection indicates that the same flag was written to both arm logs while the right-arm speed changed; the left arm therefore does not supply a second independent attacked robot. Cross-device synchronization with the IMU or packet trace was not established and is unnecessary for this single-stream analysis.


This is one repetitive pick-and-place acquisition. The eight scheduled intervals, millions of samples and repeated motion cycles are dependent observations from that acquisition. The dataset provides no independent labels for legitimate changeovers, attack intent or corresponding mechanical faults within our admitted track. We retain these limitations when interpreting every detection count. No other dataset or synthetic attack was added to the final comparison.

## Empirical observer and comparison methods




## Training-only reference and scaling

Let [math]. Training-only population moments give

Moments are accumulated using Welford's algorithm. Constant or nonfinite channels fail admission; no clipping, imputation, resampling or future-looking interpolation is used. All reference/parameter fitting uses the 536,946 eligible training targets. Warmup observations can initialize causal state but are excluded from those fitting targets.


The periodic reference comprises [math] standardized mean vectors [math] and a training-estimated period [math] seconds. Period estimation samples every twentieth observation from the first eligible training segment, up to 10,000 observations. It examines mean squared twelve-channel differences for lags 1–121; candidates 2–120 must be local minima. Minimum objective, then smaller lag, breaks ties. The selected lag is converted using actual elapsed-time differences. For each candidate bin count, a bootstrap clock template initializes a fixed phase offset from each segment's warmup, after which eligible training endpoints produce the final bin means. Empty bins or missing admissible periods fail. Appendix  records the finite configuration search; no final outcome selected the period or bins.



## Phase propagation and measurement correction

The dynamic state is a categorical distribution over the [math] phase bins. Each segment begins uniformly. Given previous posterior [math] and native [math], define the circular shift operator [math] by linearly distributing probability between adjacent bins for a forward displacement [math]. The prior is

This is a fixed empirical transition, not an identified robot-dynamics equation. Repeated fractional shifts introduce numerical diffusion.


Before the current measurement influences state, the observer predicts

The current observation then supplies template distances and a tentative posterior:

Normalization is computed stably in log space. The bandwidth is the larger of [math] and the training mean of [math]; its fitted value is [math]. These radial-basis weights are a pseudo-likelihood, not a calibrated model of physical sensor noise.


With [math], correction evidence is

Natural logarithms are used; zero-mass terms contribute zero. The statistic lies in [math] apart from numerical tolerance. It measures unsigned belief redistribution, not physical phase error, speed or attack probability. All scores are emitted before the tentative posterior is committed. No score changes the fitted reference, bandwidth, normalizer or threshold.



## Primary contrast and explanatory scores

Training-only mean residual and correction values are [math] and [math]. The primary scores are

Both scores use exactly the same prior, posterior, prediction and subsequent state trajectory. Removing [math] does not remove progression or measurement correction from the observer. The sum has equal coefficients after training-mean scaling; no fusion-weight search was performed.


Four explanatory outputs use that same observer: O-C is raw [math]; O-K is [math]; O-L is the predictive mixture energy [math]; and O-Rv is the mean standardized squared residual restricted to the six velocity channels. The last output still obtains its state from all twelve channels. Two auxiliary update policies retain [math]: O-Follow uses likelihood-only phase correction after warmup, while O-Free omits measurement correction after warmup but keeps nominal propagation and mixing. All three policies share ordinary correction during initialization. The free-running distribution's diffusion limits what this comparison says about fixed references.


The energy and KL outputs are related by the direct identity

for positive prior support. Also,

These algebraic decompositions motivate conventional controls and ambiguity analysis; they are not claimed as new theorems. Jensen–Shannon discrepancy has no identical KL decomposition. Equally poor likelihoods can leave a posterior unchanged, whereas an informative normal measurement can change it substantially.



## Ordinary controls

V-Z takes the maximum absolute training-standardized deviation across joint velocities. T-32 predicts from the fixed 32-bin template. Its warmup chooses the minimum cumulative-loss integer phase offset, with the smallest offset breaking ties; thereafter only elapsed time advances the phase. It makes no current-observation phase adjustment.

AR-4 is a separate autoregression for each standardized channel,

Training minimizes mean squared prediction error plus [math], with an unpenalized intercept. Its score is mean twelve-channel squared residual. The current sample enters history only after scoring. This is teacher-forced one-step monitoring, not autonomous simulation or a cross-channel vector autoregression. Singular/nonfinite fits fail rather than trigger altered regularization. These controls are our implementations; none is a claimed faithful reproduction of a cited paper.

## Evaluation design and execution




## Chronological partitions and common support

Table  defines zero-based data rows excluding the header, with half-open ranges. Splitting precedes history construction. A new segment begins when [math] or [math] seconds. Each partition starts independently, except that final normal and mixed slices are two reporting regions of one continuous replay. Every method excludes the same first 1,528 observations after a segment start; no method-specific denominator is trimmed. Training contains a restart at row 16,571. Final replay contains one initial warmup and no later resets.





## Selection, freezing and threshold calibration

Seven ordinary candidates were declared: one velocity control, two templates with 32/64 bins, and four autoregressions crossing orders 1/4 with ridge values 0.001/0.1. Template and autoregression selection separately minimized normal-development prediction mean squared error (MSE), with declared candidate order resolving ties. No cross-family winner was selected. The 32-bin template and order-4, ridge-0.001 autoregression were retained without refitting on development. The observer reused the selected template and the same normal development for internal checks; this reuse is disclosed rather than described as independent validation. Its mixing rate and scoring definitions had no outcome-driven sweep.


The complete eleven-method roster, fitted artifacts, transformations, initialization, formulas, budgets and reporting rules were locally frozen before calibration. These records are prospective experiment records, not an externally registered study or independently blinded protocol. Each method then received the same 160,473 eligible normal-calibration scores. For ascending scores [math], the fixed operating point is

where [math]. Strict exceedance handles ties. Calibration sets thresholds only; it cannot choose a model, seed, combination, percentile, persistence rule or checkpoint. This empirical quantile does not guarantee a future 1% false-alarm rate.



## Outcome definitions

The mixed population contains 345,602 schedule-positive and 337,044 schedule-zero observations. Unadjusted precision, recall and F1 use counts of true positives (TP), false positives (FP), false negatives (FN) and true negatives (TN). Average precision (AP) groups equal scores, evaluates precision after each whole tie group enters, and sums precision times recall increments. There is no point adjustment or test-optimized threshold. Undefined quantities are retained as undefined rather than replaced by a favorable number. Mixed prevalence is reported because it affects precision and the constant-score AP reference.


Protected-normal burden comprises the fraction of eligible points alarmed and the number of contiguous alarm episodes per eligible native-time hour. Exposure sums adjacent eligible timestamp differences within a continuous segment; it does not substitute a nominal sample count for elapsed time. Episodes crossing report boundaries or warmup are explicitly classified. Schedule-zero mixed intervals are reported separately from the held-out normal population and are not assumed to be certified recovery.


An event-overlap hit requires an alarm on at least one eligible positive point. A fresh onset requires the start of a new alarm episode within the interval; an alarm already active at the boundary can overlap without being fresh. Delay is measured from the recorded flag onset to the first qualifying alarm. Misses retain null delays and remain in the eight-event denominator. Detected-only summaries explicitly state the number detected. No attack boundary initializes phase or changes a score, threshold or state. There is no cooldown or persistence filter.



## Protected execution and integrity checks

All eleven methods are deterministic and ran once, with no stochastic seed. The policy seeds 17, 42 and 2026 were reserved for stochastic methods; none was admitted. Final feature replay saved all aligned scores and hashes without parsing labels. The delayed evaluator was admitted only after the complete score seal and accepted resource-supervisor receipt. Joint outcomes were inspected after every evaluation completed. One scoring attempt and one evaluation attempt succeeded; there were no failed final attempts or retries.


The implementation was covered by 324 synthetic software tests. The same 52 source and configuration identities and 133 frozen input bindings remained unchanged during the campaign. A separate saved-result audit recomputed metric, episode, event and recovery arithmetic, with seven hand-checkable synthetic examples preceding it. Its millions of coordinate assertions are software checks, not independent experiments. It did not reopen raw observations or replay a detector. Original-label verification belonged to the evaluator; the supplemental arithmetic audit reconstructed labels from the frozen schedule and was not independent reannotation.

## Results




## Coverage and normal-development correspondence

Every method produced 897,119 finite eligible final scores: 214,473 in the protected normal slice and 682,646 in the mixed slice. Eligible coverage is 100%. Raw final coverage is 99.829967%; the only 1,528 exclusions are the common initial warmup. No missing scores explain the weak detection. Protected-normal exposure is 2.97878\ hours for every method.


Earlier normal-only checks supported a recurring 38-second reference and prospective state synchronization, but did not establish accurate latent phase. The synchronized observer's development one-step MSE was 0.338911, compared with 0.002094\ for the ordinary autoregression. The declared ambiguity criterion was met at 53.12% of sampled diagnostic endpoints. The criterion used normalized entropy above 0.5 or circular resultant below 0.5; these are descriptive diagnostics, not calibrated confidence bounds or independently observed phase errors. This evidence already limited the observer interpretation before final scoring.



## Point detection and normal alarm burden

Table  shows all declared methods in their frozen order. O-RC achieved F1 0.017292\ and point recall 0.8805%. Its protected-normal point alarm fraction was 0.9941%, with 554\ episodes or 185.98\ episodes per eligible hour. Thus a point-alarm fraction close to the calibration percentile coexisted with frequent alarm episodes. No method exceeded 4.0217% point recall.






The primary O-RC minus O-R contrast increased F1 by 0.000689011. It added 122 true-positive points while removing 32 mixed false-positive points, 27 protected-normal alarm points and ten protected-normal episodes. Normal episode rate decreased by 3.3571/hour. These paired recorded outcomes are slightly favorable to the added correction term, with unchanged coverage. Their small size and low absolute recall do not establish useful general detection or a newly effective security mechanism.


The ordinary AR-4 achieved F1 0.018846\ and AP 0.507711, both above O-RC, with slightly fewer normal alarm points (2,109 versus 2,132). It produced 1,302 normal episodes, or 437.09/hour, compared with 554 for O-RC. The fixed template T-32 achieved the largest F1 (0.074737) and recall (4.0217%), but its normal point alarms reached 1.3997% and mixed scheduled-zero alarms 3.6912%. These are trade-offs, not a single global ranking. No scalar utility was declared to choose a winner after exposure.


Mixed positive prevalence was 50.6268%. The constant tied-score AP reference is that prevalence; observed AP ranged from 0.490596 to 0.507711. Values near this reference do not establish useful broad ranking separation. This reference is arithmetic, not an additional detector run. Precision reflects the recorded schedule's unusually high positive prevalence and is not an estimated field attack precision.



## Explanatory scores and update-policy ablations

Correction-only O-C and KL surprise O-K had slightly higher F1 than O-RC, but 342.76 and 349.47 normal episodes/hour, respectively. The energy score O-L, velocity residual O-Rv, free-running and unconstrained-following residuals remained close to O-R on the reported point outcomes. The direct velocity control was also similar. These are descriptive similarities, not evidence from an equivalence test. They do not isolate a causal benefit of progression, nor justify attributing detection to a uniquely observer-specific mechanism. The free-running variant's diffusive near-uniform state is a limitation of that particular ablation.



## All eight events and schedule-relative delay

No method had an alarm already active at any of the eight event starts. In this recording, every overlap hit therefore also had a fresh onset. O-R, O-L, O-Rv, O-Follow, O-Free and V-Z missed event 5 entirely. Each remaining method hit all eight. Appendix  retains every delay and miss, and every scheduled-zero recovery interval.




O-RC first alarmed 9.20 seconds after the event-5 schedule flag. On the seven events both primary methods hit, five first-alarm delays were identical; O-RC was 2.05 seconds later on event 6 and approximately 0.05 seconds later on event 7. It was not earlier on any shared hit. Its detected-only median of 9.45 seconds, compared with 9.70 seconds for O-R, uses eight and seven events respectively and cannot establish faster matched detection.


Each scheduled interval contains more than 43,000 positive observations. Any one alarm suffices for an overlap hit. O-RC's eight hits therefore coexist with 342,559 false-negative positive observations, frequent normal episodes and AP near the prevalence reference. Short first-alarm delays here do not imply sustained recognition of the scheduled deviation or verified detection of its physical onset.



## Measured resources

Table  reports the whole-worker measurements. Both phases stayed within their frozen caps: scoring 900 seconds wall/600 seconds CPU and evaluation 1,800/1,200 seconds; both allowed 1 GiB worker resident memory and 256 MiB output. The hardware was a local Apple M5 Pro with 24 GiB host memory, using Python 3.15.0 and the standard library. No GPU or paid compute was used.




Per-method processing costs, initialization/parsing decomposition and per-record latency quantiles were not instrumented. The recorded whole-roster execution is locally feasible under its limits, but cannot determine whether the correction term's small gain had a measurable compute advantage or penalty relative to a control. No edge-device, transport-latency or live-deployment conclusion follows.

## Interpretation, limitations and independent evidence




## What correction evidence contributed

The narrow hypothesis receives limited descriptive support: at the frozen operating rule, adding the correction term increased F1 slightly and reduced normal alarm counts. It also added one event hit. That finding does not establish strong detection. The low positive-point recall and frequent normal episodes remain central, and ordinary controls offer comparable or stronger outcomes on several measures. The evidence does not warrant describing the method as a generally superior detector or a validated digital twin.


The experiment cannot attribute the small gain to progression itself. Both primary outputs share nominal propagation, measurement correction and state history. Moreover, velocity measurements can retain direct speed evidence even after position is aligned: if [math], then [math]. Aligning [math] need not remove the velocity-amplitude change. The similarity of direct-velocity and observer residual outcomes is consistent with that alternative explanation, but does not establish it causally. A different feature or alignment ablation prompted by this result would be a new exploratory analysis.


The observer's uncertainty is also part of the interpretation. A mixture mean can poorly represent several plausible phases, as Equation  shows. The normal-development ambiguity and substantially better one-step autoregression suggest that the observer is not an especially accurate predictor for these inputs. A correction statistic might partly compensate for limitations of its residual representation. No independent phase truth, posterior-coverage calibration or causal mechanism experiment resolves that explanation here.



## Limits of the evidence


## One acquisition.
 The study contains one task recording with eight dependent intervention intervals. It supplies within-recording descriptions, not a sample of robots, factories, tasks or attack campaigns. We do not use an ordinary row bootstrap, treat intervals as independent deployments, or construct significance claims from deterministic repeated computation. No confidence interval is offered for a cross-robot population that was not sampled.


## Ground truth and trust.
 Schedule flags provide reproducible scoring boundaries but do not establish exact physical onset, malicious intent, trusted command provenance or healthy recovery. Truthful monitoring telemetry is an assumption. No result transfers to an adversary who consistently forges all monitored channels, nor establishes separation between faults, benign speed changes and attacks.


## Development and model scope.
 The same normal-development partition selected template resolution and supported observer diagnostics. That reuse is disclosed. The reference is an empirical collection of joint means, not a mechanically constrained model. Its inferred phase need not be unique, and the mean of possible states need not lie on a physically realizable trajectory. The free-running comparison is affected by numerical diffusion. Eleven methods do not constitute eleven independently reproduced recent papers or comprehensive detector benchmarking.


## Operating rule and cost.
 The normal-calibrated 99th percentile was fixed for the study; other alarm budgets, persistence rules and application utilities were not compared. We cannot infer an operationally acceptable false-alarm rate from this percentile. Per-method latency and computational overhead are unavailable. The scalar traces and current results cannot establish real-time transport, actuator safety or prevention of physical harm.



## Planning fresh evidence after exposure

The original final holdout is now exposed. A new score, threshold, persistence rule, input choice or preferred method motivated by these outcomes must be described as exploratory. Repeating or reshuffling the same recording does not create a new confirmation set. The local reproducibility package preserves the original outcome and separates future design decisions from it.


Two public sources motivate a next admission audit rather than an immediate broader claim. The voraus-AD study provides separately collected robot executions with joint-state measurements and physical anomalies . It could test whether a motion-only procedure applies to variable executions on another platform. It does not supply cyberattack intent. NIST's robot position-accuracy resource documents controller recordings under speed, payload and temperature conditions ; these may support a benign-condition challenge after file and condition semantics are verified. Different condition files are not proof of recorded within-run changeovers. Neither source has been downloaded or admitted to this study.


A future protocol must establish acquisition/session groups, original file identities, units, clock continuity and annotation provenance before fixing whole-group training, development, calibration and final assignments. CASPER's period, fitted scaler, 1,528-row warmup and gap rule cannot simply transfer. Source-specific refitting would test applicability, not zero-shot cross-robot transfer. Any newly developed model must be selected without new final outcomes; only a frozen model tested on genuinely reserved independent recordings could support a new confirmatory claim.


A stronger cybersecurity question requires repeated acquisitions with documented authorized and unauthorized command changes, truthful monitoring, and trusted context that makes the distinction observable. Fault recordings alone cannot supply that evidence. No suitable laboratory access or independent cyber recording is assumed. The companion post-exposure evidence plan specifies admission gates, permitted claims and stopping decisions; it is a proposal, not an executed experiment or external preregistration.

## Conclusion


This controlled CASPER study found a small descriptive benefit from adding correction discrepancy to an empirical motion observer's residual: F1 increased from 0.016603\ to 0.017292\ with slightly fewer normal alarms. Absolute detection remained weak. The correction variant alarmed on only 0.8805% of positive observations and produced 185.98\ normal episodes/hour, despite fresh alarms in all eight long scheduled intervals. Ordinary controls matched or exceeded several outcomes with different false-alarm costs.

Both primary variants retained nominal progression, so the comparison does not establish progression's isolated value. The evidence supports a narrow score-comparison finding and a caution about interpreting event hits without point coverage and normal burden. It establishes neither a novel digital twin nor general cybersecurity performance. Further design changes prompted by these exposed outcomes are exploratory; broader confirmation requires appropriately reserved independent recordings and a source-specific protocol.

## Declarations and reproducibility



## Data availability.

The original CASPER provider and version are identified in Section  and the data receipt . The provider metadata inspected at acquisition stated CC BY-SA 4.0. The original dataset is not redistributed in this manuscript package. A current provider download must be matched to the recorded file size and SHA-256; a similarly named or newer release must not be silently substituted. The package includes aggregate results, source identities and an access recipe, not private download information or raw trajectories. Redistribution terms for data-derived artifacts require review before public release.



## Code and artifact availability.

A local draft package contains the exact 52 tested source/configuration files, historical scientific specifications, frozen aggregate results, a deterministic table/figure generator, the bibliography and verification scripts. No upstream vendor code or third-party paper figures are bundled. Saved row-level scores, fitted models, complete run snapshots, resource logs and original access ledgers remain in local experiment storage, with identities recorded in the package. The public repository/archive, release identifier and code license are not selected or approved. Regenerating presentation assets is not an independent rerun of data loading, fitting and scoring. The reproduction guide explicitly separates these levels.



## Author contributions.

The requested author order is Muhammad Usman, then Haiqa Mushtaq. Individual conceptualization, methodology, software, validation, formal analysis, data curation and writing roles are each author's actual Contributor Roles Taxonomy (CRediT) contributions. Project-folder ownership and assistant work do not establish human contributions. Affiliations, corresponding author and approval of the manuscript by both authors are confirmation.


## Funding and competing interests.

Funding sources, grant identifiers and competing interests are author declarations. The absence of an entry is not a declaration of no funding or no conflicts.



## Ethics and permissions.

This work analyzes an existing robot dataset; no new human-participant recruitment or physical robot intervention was conducted by this study. No institutional exemption or ethics approval is claimed. Any applicable institutional determination remains author/institution confirmation. Manuscript tables and plots are newly generated from our saved aggregate outputs, with no copied third-party figures. The local package has not been published or submitted. Dataset terms, code licensing and any source-specific obligations must be checked before distribution; access to a paper does not automatically permit republishing its content.



## AI-assistance disclosure.

Artificial intelligence (AI) assistance through OpenAI Codex was used for research planning, primary-source checks, software implementation and tests, experiment orchestration, result analysis, manuscript drafting and reproducibility checks. The reported numerical findings come from preserved executable runs, not generated hypothetical benchmark results. Human reading, interpretation and approval of all claims and code remain to be confirmed by the authors; this draft does not attest that those checks have happened. Tool/version records available in the work logs should accompany the eventual disclosure. Exact model identifiers for sessions not recorded are not inferred. No target journal has been selected, so venue-specific AI-use requirements remain unresolved and must be checked against that venue's current policy before submission.

## Exact identity and completed execution



All row ranges are zero-based data-row indices excluding the header. The original right-arm SHA-256 is
\begin{quote}\small.\end{quote}
The selection freeze is
\begin{quote}\small,\end{quote}
and the immutable pre-execution final freeze is
\begin{quote}\small.\end{quote}
The latter retains historical not-started fields; actual completion is in the separate completion record. Experiment code was recorded at Git revision  with dirty-worktree patches and exact file snapshots. That revision alone is insufficient to reconstruct the executed bytes. The package binds the full tested file inventory instead of treating the manuscript's later repository revision as the experimental version.


The protected scoring run began at 06:21:17.705600 UTC on 17 October 2026 and was accepted at 06:25:51.061961 UTC. Label joining began at 06:26:30.415287 UTC, after all streams sealed; evaluation completed at 06:27:12.073582 UTC. The source checksum matched before and after both phases. Logical access and attempt records provide procedural protection, not an operating-system lock or an independent data custodian. Historical completed commands, from the manufacturing project directory, are:

These commands document consumed attempts. They are not instructions to remove ledgers or rerun the exposed campaign in place. The reproduction guide specifies fresh-workspace and artifact requirements separately.


## Candidate selection and frozen thresholds



Table  retains every declared ordinary candidate. Template and autoregression objectives are mean standardized prediction MSE; the velocity score is a different quantity and is not a cross-family objective. Its singleton is retained without selection. Exact ties follow the declared order. The observer's fixed mixing rate, training-only bandwidth and mean scales are specified in Section . There were no neural checkpoints or attack-selected seeds.




## Complete counts, event delays and recovery intervals



Table  preserves all confusion counts and protected-normal alarm counts. Mixed counts use 682,646 observations; normal point counts use 214,473 eligible observations. All normal boundary-censoring counts were zero in this campaign. All eight event intervals were fully eligible. Their half-open rows are [math], [math], [math], [math], [math], [math], [math] and [math].





Table  reports all eight scheduled-zero intervals following successive events. Columns Z1–Z7 end at the next event start; Z8 ends at the recording's end. Entries are alarm observations divided by eligible observations. These intervals are not independently certified recovery states. Full start/end rows, native exposure, episode rates and censoring are retained in the aggregate JSON, so the table does not replace the detailed record.



## Artifact regeneration and claim traceability



The manuscript package's  maps named claim groups to primary-source locations or exact experiment/configuration records.  records source versions and access limits;  and the DOI-visible bibliography are generated from that register.  binds every generated table, numerical macro and PGFPlots figure to the saved inputs and generator. No figure uses raw trajectories or newly tuned outputs. The verifier checks source identities, citation keys, cross-references, complete method/event coverage and deterministic regeneration. These checks do not substitute for author comprehension, external peer review or visual PDF inspection.
