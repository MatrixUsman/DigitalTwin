# Protected prediction and persistent-deviation prior art

24 October 2026. Bounded primary-source investigation by the `prior_art` child agent. Read the current manufacturing handoff, `CLAIM_INTENT.md`, and academic-research-suite bibliography/source-verification guidance. This is a source and mechanism audit, not human peer review, a systematic review, an execution admission or a novelty certificate. Root owns synthesis, session records and the final candidate decision.

## Finding

Protected prediction, predictor/observer disagreement, persistent-bias invisibility, covariance-normalized discrepancies, guarded recovery and trusted-state resynchronization already have close prior art. A new neural wrapper or renamed residual cannot establish originality. The stronger unresolved design question is whether a monitor can retain **authorized-motion evidence across its entire information path**, including action conditioning and state resets, while handling legitimate model drift. Even this is only a candidate question: existing trajectory-attack observers and intermittently authenticated estimation are substantial competitors.

## Inspected source record

### P1. Gualandi and Papadopoulos: measurement-free actuation prediction

*From Passive Monitoring to Active Defence: Resilient Control of Manipulators Under Cyberattacks*. [arXiv:2603.13003v2](https://arxiv.org/html/2603.13003v2); first posted 13 March 2026, revised 26 May 2026. The [author metadata](https://arxiv.org/abs/2603.13003) report ICRA 2026 acceptance. Full HTML §§II–IV and relevant discussion/proof inspected; final proceedings byte identity was not established. No matched repository located in this bounded search; that is not proof of absence.

Equations 14–16 periodically initialize an open-loop predictor from the KF, propagate it using commanded input, and subtract it from the KF estimate. Equations 17–24 propagate the joint error/discrepancy covariance and normalize the discrepancy by a Mahalanobis form. Theorem 2 is a nominal pointwise Gaussian claim. Theorem 3 separates nominal actuation loss from frozen-gain stability. The paper already identifies integrator-related persistent sensor-bias invisibility. Assumption 2 permits additive sensor attacks only and excludes actuator/control/timing corruption. Consequently, this is strong mechanism overlap but not an unmodified benchmark for our command-deviation threat.

### P2. Gualandi, Larsson and Papadopoulos: further active defence

*Active Defense Against False Data Injection Attacks in Robotic Manipulators*. [arXiv:2605.17950v3](https://arxiv.org/html/2605.17950v3), first posted 18 May, version 3 dated 21 May 2026. The [author record](https://arxiv.org/abs/2605.17950) states an abridged version was accepted to IFAC World Congress 2026; final proceedings version not inspected. Full HTML §§2–3 and resynchronization discussion inspected.

Equations 12–18 reuse periodic KF initialization, measurement-free actuation propagation and covariance-aware comparison. The active interventions are virtual damping and manipulating redundant degrees of freedom. The authors explicitly discuss drift limiting the resynchronization interval. The threat again concerns sensor injections. This blocks treating periodic-reset protected prediction, its uncertainty growth, or active slowing as an untouched contribution. It does not establish that their reset policy fails under their evaluated conditions. Code revision/license were not verified.

### P3. Kaisar et al.: dual observers and recovery supervision

*A Digital Twin-Based Cybersecurity Architecture for FDI Anomaly Detection and Isolation in Next Generation Robotic Vehicles*. IEEE OJCOMS 7, 12709–12728 (2026), DOI [10.1109/OJCOMS.2026.3739185](https://doi.org/10.1109/OJCOMS.2026.3739185). [Institutional record](https://pure.kfupm.edu.sa/en/publications/a-digital-twin-based-cybersecurity-architecture-for-fdi-anomaly-d/) and [public accepted-author text](https://www.researchgate.net/publication/415129086_A_Digital_Twin-based_Cybersecurity_Architecture_for_FDI_Anomaly_Detection_and_Isolation_in_Next_Generation_Robotic_Vehicles) checked. The latter retains placeholder header dates/DOI; use the institutional identifier, not placeholders. Exact first-online date/final-PDF identity and author code remain unresolved.

Inspected §§IV–V, Eq.31–32, Table 4 and Algorithm 1. NOMINAL synchronizes the kinematic state to the EKF; RESCUE initializes from cached trusted state. Recovery requires cleared alarms and observer agreement, with dwell/path criteria. Eq.31 averages exponential observer discrepancies. The text correctly limits its direct measurement-decoupling derivative to fixed initial condition and fixed control. Thus guarded recovery, dual-model disagreement and caching an accepted state are prior art. The distinction between direct and closed-loop dependence must be respected when adapting it.

### P4. Pan et al.: attacks on desired trajectories

*Observer based attack detection and security control for UAVs against attacks on desired trajectory*. Journal of the Franklin Institute 361(11), 106920 (July 2024), DOI [10.1016/j.jfranklin.2024.106920](https://doi.org/10.1016/j.jfranklin.2024.106920). [Publisher abstract/introduction/section previews](https://www.sciencedirect.com/science/article/pii/S0016003224003417) inspected; complete equations and code inaccessible/unverified.

The threat is corruption of the desired trajectory transmitted from ground control. The detector combines tracking error with state-estimation error using an unknown-input observer; separate estimation and disturbance compensation support control. This directly blocks the broad claim that adding authorized-trajectory error to predictive consistency is itself new. Full equation-level compatibility must be resolved before declaring an algorithmic distinction or executing a faithful comparator. A 2021 predecessor is also listed in the query trail, not newly admitted.

### P5. Khazraei and Pajic: intermittent trusted information

*Attack-resilient state estimation with intermittent data authentication*. Automatica 138, 110035 (April 2022), DOI [10.1016/j.automatica.2021.110035](https://doi.org/10.1016/j.automatica.2021.110035). [Publisher article](https://www.sciencedirect.com/science/article/pii/S000510982100563X) and [public author manuscript](https://par.nsf.gov/servlets/purl/10319604) inspected. Foundational background outside the main comparator window.

This treats bounded-noise LTI plants and sparse resilient estimation with explicit intrusion detectors. It derives conditions for unbounded undetected state-estimation error and analyzes intermittent authenticated sensor observations. Authentication is an actual information-integrity assumption, not the fact that a statistical detector is quiet. Relevant conditions differ between pointwise and over-time attackability. This blocks claiming that occasional trusted anchors or integrity-aware resets are broadly new. It does not directly establish a solution for all truthful-measurement actuator-deviation monitoring tasks. No code revision/license inspected.

### P6. Aftabi et al.: adaptive watermarking in manufacturing

*DynaMark: A Reinforcement Learning Framework for Dynamic Watermarking in Industrial Machine Tool Controllers*. [arXiv:2508.21797v2](https://arxiv.org/html/2508.21797v2), 23 July 2026; v1 29 August 2025. [Author metadata](https://arxiv.org/abs/2508.21797) and [publisher DOI](https://doi.org/10.1109/TASE.2026.3715642) identify IEEE T-ASE 2026. Full HTML §§II–III and Appendix G inspected. The method varies private excitation covariance and trades detection with control/energy costs under an explicit local boundedness assumption. Sensor replay and command manipulation are its threat. Active excitation therefore has close, manufacturing-specific prior art and expands our passive-monitor scope.

Author-linked [repository](https://github.com/navidaftabi/DynaMark) inspected through the GitHub connector: main revision `9e72c647b0b767211a93bc794284456d95827c88`, committed 11 September 2026. Top-level tree has no LICENSE file; repository metadata `license` is null. This means reuse permission is unresolved, not definitively absent. No file implementation audit, download, installation or execution occurred. Comparator status: source/code lead, not execution-ready.

### P7. Finite-sample switching and mission recovery are also established

[Sensor Switching Control Under Attacks Detectable by Finite Sample Dynamic Watermarking Tests, arXiv:1909.00014v1](https://arxiv.org/html/1909.00014), 30 August 2019: inspected §§I, III and V. It uses protected but less accurate sensing, finite-sample tests and a switching dwell condition. It explicitly distinguishes finite-time requirements from asymptotic detector results. This is foundational overlap, not an admitted recent manufacturing comparator; code/final publication identity not checked.

[Dash, Chan and Pattabiraman, SpecGuard, arXiv:2408.15200v1](https://arxiv.org/html/2408.15200v1), 27 August 2024: inspected §§1–2 and recovery-mode description. Author metadata identify a CCS 2024 version. Mission constraints, state reconstruction and proactive/reactive recovery control are already investigated. This does not supply our exact passive physical-return objective, but prevents a broad claim that mission-aware recovery or a separate recovery controller is new. No full reproduction or code audit performed.

## Candidate implications for the root's synthesis

These are **our design inferences**, not findings claimed by the papers.

1. Draw the full information path before choosing architecture. A recurrence without a direct measurement argument may still depend on corrupted/unauthorized state through its initialization, applied actions, phase or later resets. A structural sensitivity calculation must include those paths. Direct measurement independence alone is too weak a claim.
2. Distinguish three references: desired authorized trajectory; a nominal plant driven by protected planned actuation; and a plant predictor driven by actual controller output. They answer different questions. Two methods cannot be ranked fairly while one receives the authorized trajectory and another only the corrupted command stream.
3. A potential narrower research problem is a **quantified resynchronization rule that preserves a minimum sensitivity to sustained unauthorized motion while bounding nominal drift**. Necessary comparison: no reset, periodic reset, ordinary protected reference/KF, and a trusted-anchor method. This is not yet a selected candidate, original algorithm or theorem. A rule that is only low-residual gating, dwell or clipping is unlikely to survive this prior art.
4. Do not erase previously accumulated discrepancy merely by aligning a model to current measurements. But retaining it forever can falsely treat a legitimate reference change as an attack. An explicit command-version/authorization contract and an observability limitation are needed. Authorization changes alone are not new information if every comparator already has them.
5. Under simultaneous unobservable plant deviation and forged measurements, a passive monitor may have indistinguishable attacked and nominal histories. A detector cannot fix that with architecture alone. Extra trusted measurements or active probing change information access; their cost and prior art must be acknowledged.

No candidate is admitted by this review. The parent should combine these constraints with its independent mechanism/statistical audits, then either formulate a precisely bounded distinction or reject the route.

## Query and access trail

Search date: 24 October 2026. Browser searches were targeted, not a systematic exhaustive retrieval. English queries included:

- `Kaisar "digital twin" "3739185"`; exact Kaisar title plus `pdf`, `github`, and `consistency-gated`.
- `"robot" "attack" "prediction" "resynchronization" detector`; `"Gualandi" "Papadopoulos" "2603.13003" code`; exact Gualandi title plus `github`.
- `"unknown input observer" "attack" "recovery" "2024" robot`; exact Nguyen discrete-time UIO title.
- `"dynamic watermarking" "2024" "robot" attack detection`; `"dynamic watermarking" sensor attacks linear systems finite sample 2024 2025`; `"DynaMark" "Aftabi" github`.
- `"secure" "resynchronization" "observer" attack`; `"attack" "reset" "predictor" "trusted" state estimation`; `"intermittent authentication" "state estimation" attacks`.
- `"fault detection" "reset" "observer" "bias"`; `"anomaly detection" "prediction" "resynchronization"`; `"cyber" "observer" "reinitialization" attack`; `"attack detection" "trusted" "anchor" "robot"`.
- Exact Pan desired-trajectory title plus `pdf`; MARS title plus `usenix`; SpecGuard exact title.

Gualandi v1 HTML was opened first, then the newer identified v2 used for the analysis. Companion v1 HTML returned a cache miss; v3 succeeded. Nguyen's `https://hal.science/hal-04620642/document` was inaccessible; it supplies no equation-level conclusion here. Search hits on ResearchGate request-only entries, generated synthesis sites and bibliographic mirrors were leads only. Kaisar's publicly readable author manuscript was used as primary text, with version caveats. MARS and other returned papers are uncompleted leads, not implied source audits. No evidence from unrelated grid papers was transferred to manufacturing.

The source synopses are intentionally compact (under 200 derived words per paper); no extended direct quotations copied. Existing local records and immutable packages were not edited. No dataset signal/test exposure, numerical experiment, contact, paid resource, publication or Git mutation was performed.
