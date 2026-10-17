# Innovation, synchronization and correction evidence: close prior-art audit

**Date:** 17 October 2026 (Asia/Karachi). **Scope:** manufacturing's empirical motion observer, original CASPER v3, right-arm controller-input route. This is a targeted primary-source investigation using the installed academic-research-suite deep-research workflow, not an exhaustive systematic review, experimental comparison, or human reading attestation. No dataset observations, fitted arrays or protected tests were opened; no training, calibration, installation or external contact occurred.

## Decision

The available evidence does **not** support a new-estimator, new-digital-twin, new-phase-detection, new-surprise-measure or newly discovered accommodation-failure claim. Bayesian state prediction/correction, innovation monitoring, phase-based anomaly detection, and combining a mismatch term with distributional discrepancy all precede this project.

A defensible prospective contribution is a **single-acquisition empirical comparison of scoring choices within a fixed motion observer**, documenting whether correction evidence adds useful information beyond its prospective residual and conventional surprise scores under the same inputs, state updates and normal-only calibration. This remains a question, not a beneficial result or an established literature gap. It is narrower than a generally superior cybersecurity detector and does not alone meet the breadth expected of a strong general-method paper.

The present residual already uses nominal progression: it compares the measurement with the prediction formed from the propagated **prior**. Therefore describe the principal pair as **with versus without an additional correction-discrepancy score term**, not progression evidence versus no progression evidence. The state trajectory is identical in the pair.

## Primary evidence and limits

Dates below distinguish first dissemination from later versions. Older sources remain methodological background and reasons for necessary controls; they do not fill the project's recent-paper quota. Bibliographic existence, manuscript access and executable code are assessed separately.

| Source / identity / status | Direct evidence inspected | Consequence and code limits |
|---|---|---|
| **Särkkä and Svensson, Bayesian Filtering and Smoothing, second edition**, Cambridge University Press, 2023; DOI [10.1017/9781108917407](https://doi.org/10.1017/9781108917407). Scholarly textbook, not a recent detector paper. | Author-hosted [prepublication manuscript](https://users.aalto.fi/~ssarkka/pub/bfs_book_2023_online.pdf), indexed p.104, Eqs.6.38–6.43, gives discrete-state prediction, emission reweighting and evidence normalization. [Institutional metadata](https://research.aalto.fi/en/publications/bayesian-filtering-and-smoothing-3/) confirms edition and identifier. Full browser fetch exceeded its size limit; only the explicitly indexed equation passage was inspected. | Our categorical phase propagation and observation update instantiate this familiar filtering structure. A circular transition and an empirical reference do not establish a new filter. No author example-code revision was inspected or imported. No stability or calibrated-uncertainty guarantee transfers automatically. |
| **Mehra and Peschon, “An innovations approach to fault detection and diagnosis in dynamic systems,” Automatica 7(5), 637–640, September 1971**, DOI [10.1016/0005-1098(71)90028-8](https://www.sciencedirect.com/science/article/abs/pii/0005109871900288). Peer-reviewed correspondence. | Publisher metadata and abstract explicitly connect innovation-process statistics to detection/diagnosis for linear Gaussian systems. Full text was not obtained here. | Innovation/residual detection is classical. This record is contextual evidence, not sufficient detail for a faithful implementation. No code/release verified; no CASPER or robot-security result implied. |
| **Willsky, “A Survey of Design Methods for Failure Detection in Dynamic Systems,” Automatica 12(6), 601–611, November 1976**, DOI [10.1016/0005-1098(76)90041-8](https://www.sciencedirect.com/science/article/pii/0005109876900418). Peer-reviewed survey. | [Author-hosted full manuscript](https://willsky.lids.mit.edu/publ_pdfs/15_pub_AUTO.pdf): §II p.602, Eqs.4–10 separates prediction, innovation and correction; §III pp.603–604 discusses filter sensitivity and the gain/residual trade-off, including reduced steady-state fault residual with higher gain. Publisher metadata matches. | The possibility that better tracking weakens a residual detector is established background. Our experiment may characterize that trade-off in one recording; it cannot claim to discover it. No runnable source identified; linear-model conclusions do not prove our observer's behavior. |
| **Itti and Baldi, “Bayesian Surprise Attracts Human Attention,” NIPS 2005, Advances in Neural Information Processing Systems 18**, official [proceedings record](https://papers.neurips.cc/paper_files/paper/2005/hash/0172d289da48c48de8c5ebf3de9f7ee1-Abstract.html). Peer-reviewed conference paper; author page uses the 2006 proceedings-publication citation. No DOI verified. | Official [full paper](https://papers.neurips.cc/paper/2822-bayesian-surprise-attracts-human-attention.pdf), §1 p.2, Eqs.1–2 defines surprise as posterior-to-prior KL. The [author explanation](https://ilab.usc.edu/surprise/) connects belief change with surprise and distinguishes it from observation information. | A prior/posterior discrepancy is established. Our bounded Jensen–Shannon choice is not the same formula and does not inherit a novelty or theoretical-optimality claim. No matched robot implementation/revision inspected. The experiments concern attention, not industrial cyberattacks. |
| **Ahrens, Ahrens and Schotten, “A machine-learning phase classification scheme for anomaly detection in signals with periodic characteristics,” EURASIP Journal on Advances in Signal Processing 2019, 27**, DOI [10.1186/s13634-019-0619-3](https://link.springer.com/article/10.1186/s13634-019-0619-3). Accepted 26 March, published 2 May 2019; preprint [1811.12119](https://arxiv.org/abs/1811.12119), 29 November 2018. Peer-reviewed journal article. | Publisher full text §§2.4,3, Appendix A and §8.2 describes phase classification, variable periods, confusion-driven phase merging, and a nearest-reference phase classifier using seasonal averages. Data include PTB ECG, Modbus traffic and synthetic waveforms; exact downloaded release hashes were not audited. | Phase labels, period discovery, ambiguity handling and seasonal-reference classification are prior art. Appendix §8.2 motivates a simple phase-alignment comparator if claiming value beyond classical alignment. No matched author implementation/license/revision verified; linked Modbus repository is a dataset, not the method code. Offline period segmentation must not be silently ported into causal replay. |
| **Çatal et al., “Anomaly detection for autonomous guided vehicles using Bayesian surprise,” IROS 2020, 8148–8153**, DOI [10.1109/IROS45743.2020.9341386](https://doi.org/10.1109/IROS45743.2020.9341386). Published conference paper; [author-institution record](https://biblio.ugent.be/publication/8700871) verifies metadata and abstract. Exact first-online date not verified. | Institutional abstract describes learned prior/posterior models and unsupervised surprise-based anomaly detection using warehouse AGV RGBD observations. The listed published PDF is **UGent only**; lawful open full text and corresponding author code were not found in this bounded search. | Direct robotic anomaly-detection precedent prevents claiming the first use of Bayesian belief change for robots. Equation, preprocessing, split and threshold details remain unverified. Different platform/modality; **background only**, not admitted as a fair CASPER comparator. |
| **Xu et al., “Anomaly Transformer: Time Series Anomaly Detection with Association Discrepancy,” ICLR 2022**, [OpenReview identifier LzQQ89U1qm_](https://openreview.net/forum?id=LzQQ89U1qm_), [arXiv:2110.02642v5](https://arxiv.org/abs/2110.02642v5). Peer-reviewed conference paper; preprint v1 6 October 2021, v5 29 June 2022. | Author [full manuscript HTML](https://arxiv.org/html/2110.02642), §§3.1–3.2, Eqs.3,6 and Appendix E.2 combines reconstruction with association-distribution discrepancy and compares error-only, discrepancy-only and combinations. [Author repository](https://github.com/thuml/Anomaly-Transformer) identifies MIT license and point-adjusted evaluation. OpenReview direct access hit browser verification; manuscript and author links established correspondence. | “Residual plus discrepancy” is not generically new. Its attention associations are not Bayesian phase posteriors, and reconstruction/window access differs from our prospective forecast. Background, not an automatic matched control. Repository revision was not pinned in this pass; source was not executed and threshold behavior was not audited. No CASPER experiment established. |
| **McGarry and Nelson, “Cognitive Based Detection of Anomalous Sequences Using Bayesian Surprise,” Expert Systems 42(9), e70106**, DOI [10.1111/exsy.70106](https://onlinelibrary.wiley.com/doi/10.1111/exsy.70106), first published **28 July 2025**; accepted 15 July 2025. Peer-reviewed journal article, inside the recent window. | Publisher full HTML §§3.1–3.2 and Data Availability; [institutional record](https://sure.sunderland.ac.uk/id/eprint/19259/) corroborates identity. Uses probabilistic suffix trees on discrete Hospital Sepsis, Chess, Wisconsin Card Sorting and BioFamilies sequences. Publisher links [author repository](https://github.com/kenmcgarry/BayesSurprise), whose Data and R-code directories were observed. Institutional PDF fetch failed, but publisher full HTML was accessible. | Contemporary sequence-anomaly surprise work; no continuous joint telemetry, periodic robot or CASPER claim. **Background only.** Code license, revision, preprocessing and execution correspondence remain unaudited; no implementation copied. Its presence does not establish our detector is equivalent or inferior. |

For recent transferable neural controls, retain the existing [ModernTCN audit](REPLACEMENT_COMPARATORS_2026-10-17.md). The [author repository](https://github.com/luodhhh/ModernTCN) was independently reopened: it links ICLR 2024 manuscript `vpJMJerXHU`, advertises five tasks and has MIT license. This pass did not resolve its current-conditioned reconstruction versus our frozen prospective-prediction rule. It remains a **conditional modified-protocol transfer**, not execution-ready and not a published CASPER baseline. Do not substitute age or venue for role compatibility. The CASPER, TWINE and CatBoost dispositions remain in [COMPARATOR_ADMISSION.md](../COMPARATOR_ADMISSION.md).

## What the present score is and is not

The following is our algebraic analysis of the implemented design, not a result attributed to a paper or a new theorem. Let `p` be the predicted phase weights, `m_k` the frozen template vectors, `z` the standardized 12-vector and `D_k = ||z-m_k||²/12`. With `e_k=D_k/(2τ)`, the measurement update uses

`Z = Σ_k p_k exp(-e_k)`, `q_k = p_k exp(-e_k)/Z`.

The two scores already implemented are `R/a` and `R/a + JSD(p,q)/b`, where `R=||z-Σ_k p_k m_k||²/12` and `a,b` are training-only means. For positive support,

`KL(q||p) = Σ_k q_k log(q_k/p_k) = -log Z - Σ_k q_k e_k`.

Thus a classical posterior/prior information-gain score and the predictive mixture energy `L=-log Z` are closely related to this update. The Jensen–Shannon term has **no identical decomposition**. Call `L` a predictive **energy** unless a normalized and validated observation-density model is explicitly justified; the current bandwidth is an empirical training statistic, not established sensor-noise variance. A Gaussian interpretation would require stating its dimensional scaling and common normalizer and would still not establish calibration.

There is also a direct distinction between the residual of a mixture mean and component-wise fit:

`Σ_k p_k D_k = R + Σ_k p_k ||m_k-Σ_j p_j m_j||²/12`.

Ambiguous phases can therefore impair the mean prediction without every template component fitting badly. The present development report's substantial phase ambiguity and weaker one-step prediction than AR must remain visible. A correction term might compensate for a weak score representation rather than reveal a new physical security mechanism. Only the proposed comparisons can resolve that explanation on the available recording.

`C` is unsigned redistribution, not measured physical phase error, speed, malicious intent or command authenticity. A large current measurement deviation that changes all component energies similarly can yield little belief redistribution; correction-only scoring may miss such cases. These are mathematical possibilities, not observed CASPER outcomes.

## Required comparison roles before calibration

This table is a **design recommendation only**. New scoring variants are not implemented, calibrated or admitted by this note. Additions require a separately versioned development plan and synthetic/normal-only validation; preserve existing observer v0.1.

| Role | Status / recommendation | Scientific purpose |
|---|---|---|
| Same observer `R/a` versus `R/a+C/b` | Existing primary pair; retain exactly matched states, predictions and feature access | Isolate the incremental correction-discrepancy score term. This does not remove all progression information from R. |
| Same observer `C` alone | Required cheap explanatory control; monotone scaling does not matter to rank/quantile calibration | Distinguish useful combination from correction evidence alone dominating the result. |
| Same observer `L=-log Σ p exp(-D/(2τ))` | Required conventional predictive-energy control; stable log-sum-exp, same state/reference/bandwidth | Check whether the result is obtainable from the update's ordinary evidence normalization instead of an added JS term. |
| Same observer `K=KL(q||p)` | Recommended cheap classical-surprise control; no extra fitting; test numerical support and identity | Directly compare bounded JS evidence with familiar Bayesian surprise. It is explanatory, not a new primary endpoint or a post-test choice. |
| Velocity deviation, selected AR, fixed periodic template | Existing essential controls; retain irrespective of their eventual strength | Establish whether observer complexity adds anything beyond direct speed variation, local prediction and recurrence. |
| Unconstrained following and free-running observer | Auxiliary only; preserve existing common warmup and score alignment | Characterize effect of state-update behavior. Long free propagation diffuses the phase weights; a weak diffusive reference is not proof that all fixed references fail. Keep the ordinary fixed template visible. |
| Deterministic causal phase alignment with timing evidence | Conditional: needed before claims of superiority over phase alignment or of value from probabilistic phase uncertainty | Must define past-only phase selection, timing-deviation score, ties/ambiguity, causal history and normal-only choices. An offline DTW/period oracle is not a fair online comparison. Current free/follow variants do not establish equivalence to all classical aligners. |
| One recent capable prediction/control method | Still requires admission; ModernTCN is conditional | Broad performance claims require a compatible stronger contemporary method. A narrow score audit need not claim to beat the entire literature or pad a three-paper roster. |

Freeze the entire score roster and analysis interpretation before calibration/final exposure. Do not use final attacks to select between C, K, L, combinations or state-update variants. The primary hypothesis remains R versus R+C; report all declared alternatives even if the new term is redundant or worse. No statistical superiority conclusion is available from normal-development fit quality.

## Claim and evidence boundary

**Current supported statement:** the empirical phase observer has a tested causal implementation and internally checked normal-development recurrence, prediction and synchronization on one CASPER acquisition. Its weights are descriptive uncertainty, not calibrated physical confidence. It has not demonstrated security benefit.

**Prospective narrow question:** on the frozen right-arm recording, with telemetry/time assumed truthful and the same training, score support and normal-only threshold rule, does adding JS correction evidence change detection of the eight scheduled speed-intervention intervals compared with the same observer's prospective residual, and how does that trade-off compare with C, K, L and simple controls?

**Not supported by that design alone:** generalization across robots, independent runs, tasks, faults or authorized speed changes; discrimination of malicious intent; recovery from forged telemetry; validated physical digital-twin fidelity; a new filtering theory; first use of surprise; detection superiority in manufacturing. Eight intervals are eight events within one acquisition, not eight independent plants or experiments. An authorized speed change can be observationally indistinguishable from the recorded intervention under this feature/trust boundary.

If broad claims are retained, independent recordings and a justified contemporary comparator must be admitted before final exposure. Merely cutting this acquisition into more windows, changing random seeds, or using the left arm as if independently labelled does not supply that evidence. If this remains a focused case study, revise the title/abstract/claim scope accordingly, keep a negative result publishable in principle, and do not promise a leading-journal outcome.

## Search record and unresolved verification

The queries below were executed through public web search during this audit; pages were opened only when they supplied primary publisher, proceedings, institutional-author manuscript or author-code evidence. Search dates were 17 October locally. This log does not certify completeness.

- `Bayesian surprise attracts human attention Itti Baldi 2009 prior posterior KL divergence`
- `Kalman filter innovation based fault detection chi square Willsky 1976 survey model based failure detection dynamic systems`
- `phase estimation anomaly detection periodic motion hidden Markov phase industrial robots alignment`
- `site.klab.caltech.edu Itti Baldi Bayesian surprise 2009 pdf`
- `site:ilab.usc.edu Itti Baldi 2009 surprise pdf`
- `"A Machine-Learning Phase Classification Scheme" anomaly paper`
- `"Bayesian surprise" "anomaly detection" robot`
- `"Anomaly detection for autonomous guided vehicles using Bayesian surprise" arxiv`
- `"Anomaly detection for autonomous guided vehicles" github`
- `"A survey of design methods for failure detection in dynamic systems" DOI`
- `"phase" "anomaly detection" "Jensen-Shannon" robot`
- `"Anomaly Detection for Autonomous Guided Vehicles" pdf Catal`
- `Anomaly Transformer association discrepancy ICLR 2022 OpenReview github`
- `"prior" "posterior" "Jensen-Shannon" "anomaly detection" time series`
- `"Bayesian surprise" "industrial" anomaly detection 2024 2025`
- `"An innovations approach to fault detection" 1971 publisher`
- `site:papers.neurips.cc "Bayesian Surprise Attracts Human Attention"`
- `site:arxiv.org "Jensen-Shannon" "prior" "anomaly"`
- `site:proceedings.mlr.press "anomaly detection" "phase" 2024 2025`
- `site:openreview.net periodic anomaly detection 2024 2025 alignment`
- `Sarkka Bayesian filtering smoothing pdf author 2023 prediction update equations`
- `"Cognitive Based Detection of Anomalous Sequences Using Bayesian Surprise" github`
- `"Cognitive Based Detection of Anomalous Sequences Using Bayesian Surprise" McGarry pdf`

Access/verification failures retained: AGV full text institution-restricted; both ICLR OpenReview direct openings encountered browser verification; the Aalto book full PDF exceeded the web-tool size cap; Sunderland PDF direct retrieval failed while Wiley HTML succeeded. A guessed ModernTCN arXiv URL `2311.02594` resolved to **scBeacon**, a different paper, and was rejected; it is not a ModernTCN identifier. A guessed NIPS hash failed and was replaced with the verified official proceedings identifier above. Search results from third-party summaries, generated research-project pages and article-sharing sites were not used as evidence. No absence result was treated as proof that a paper/codebase does not exist.

No complete citation-network/retraction/patent review or runnable-code replication was performed. No experimental paper was admitted from this audit alone. Source metadata and equations support the scoped overlap assessment; empirical performance and precise novelty remain unresolved.
