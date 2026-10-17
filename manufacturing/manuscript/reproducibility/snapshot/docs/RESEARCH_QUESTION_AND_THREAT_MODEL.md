# Research question and threat model — manufacturing

Decision date: **16 October 2026**. Owner: **Haiqa Mushtaq**. Status: **selected direction for a bounded feasibility study; no model, experiment or novelty claim established**. The user requested a feasible question and threat model, then explicitly included annotation, permitted features and chronological splits. This document records an AI-assisted recommendation made under that delegated scope; it does not attest to human reading or invent an experimental result.

## Chosen question

> **Does retaining a nominal cycle-progression reference during state synchronization improve a motion twin's detection of CASPER's recorded right-arm speed changes under normal-only calibration?**

In plain language: a monitor needs to follow where a robot is in its task. If it also follows every change in how quickly the robot moves, it might absorb the very deviation we want it to detect. We will test whether keeping the expected progression as a separate reference helps. That failure mode is a hypothesis, not an observed finding about CASPER, TWINE or our own model.

The selected input is **right-arm joint positions and velocities**, with that arm's relative elapsed time. We choose this because the [schema audit](CASPER_SENSOR_SCHEMA.md) establishes explicit physical-state fields and source-supported clock units, and the [label/time audit](CASPER_LABEL_TIME_AUDIT.md) connects recorded flags to the intended right-arm intervention schedule. No cross-device alignment is needed. The [contract](ANNOTATION_FEATURE_SPLIT_CONTRACT.md) specifies the exact source, labels, features and partitions.

This replaces the earlier broad question about distinguishing attacks, faults and legitimate changeovers. Original CASPER does not supply the independently labelled cases needed to answer that question. It also changes the earlier IMU-first proposal for the main twin study: external-IMU reproduction remains useful but separate. Its missing timestamps and phase ground truth would limit a physical progression claim. A controller-input version of the CASPER CNN is **our modified-input implementation**, never an unchanged reproduction.

Provisional title: **“Digital Twins for Robotic Motion Integrity: The Role of State Synchronization.”** Retain “digital twin” only if the representation and validation requirements below are met; otherwise describe the method as a motion observer. Title quality cannot substitute for an actual contribution.

## What is observable and what is assumed

| Dimension | Study definition |
|---|---|
| Represented system | The right UR3e arm in the original CASPER repetitive pick-and-place recording |
| Data | Original CASPER v3, frozen right-arm CSV hash; one acquisition, one task, eight scheduled positive intervals |
| Observable state | Six `Actual Joint Positions` and six `Actual Joint Velocities`; supported units radians and rad/s |
| Time | Within-arm timestamp differences; not UTC, host time or an authenticated clock |
| Evaluation annotation | Recorded `Anomaly State` schedule flags, with exact half-open row intervals; not independently measured physical-effect onset |
| Commissioning assumption | Initial scheduled-zero prefix represents the permitted reference regime and is sufficiently clean for fitting/calibration; the dataset does not forensically certify this |
| Authorized-operation assumption | During evaluation, the intended task and nominal operating regime stay fixed. The detector receives no trusted authorization/changeover signal |
| Intended output | An alarm indicating motion inconsistent with that reference; not proof of malicious intent, exploit type or physical damage |

All three subquestions inherit this same system, collection, recorded acquisition, restricted command-intervention family and offline-replay scope; geography is not an evaluation variable. They do not add new robots, legitimate changeovers, faults or spoofing attacks:

1. Does a causal phase-following observer reduce the apparent discrepancy during the recorded changed-speed intervals compared with a fixed nominal reference?
2. Does retaining progression/correction evidence improve the declared detection/false-alarm trade-off relative to the otherwise same observer without that evidence?
3. Does any benefit remain against simple joint-velocity and ordinary prediction controls receiving the same permitted information?

These are algorithmic comparisons on a fixed recording. They are not causal identification of a real intrusion or a general claim about industrial attacks.

## Restricted threat model

| Element | Included assumption and boundary |
|---|---|
| Protected property | Conformance of robot motion to an assumed permitted repetitive operating regime |
| Attacker objective | Change execution speed through motion-command parameters or the application command path |
| Attacker access | Ability to cause the studied command-level velocity changes. No phishing, credential theft or exploit chain is implemented or validated |
| Attacker knowledge | No secrecy assumption about the detector is required, but adaptive/white-box evasion is **not evaluated** by replaying fixed recorded interventions |
| Trusted observation path | Joint-state telemetry and timestamp values reaching the monitor are truthful; monitor, stored reference, calibration and initial fitting data are uncompromised |
| Attacker cannot do, within this model | Forge the monitor's telemetry/time, rewrite detector state/parameters, poison commissioning, fully compromise controller firmware or the monitoring collector |
| Defender access | Past and current allowlisted joint-state values; relative clock increments for model evolution and gap handling; frozen normal-data parameters |
| Defender does not receive | Schedule flag, event number/boundaries, absolute boot time, file position, command authorization labels, other modalities or future observations |
| Response | Record an alarm/score/uncertainty state. No stop command, mitigation, robot actuation or safety guarantee |

The trusted telemetry path is a **restriction of the study**, not a security property demonstrated by CASPER. The matched author collection source both sends motion settings and records controller states; it does not establish an independently protected monitor or authentication. A fully compromised controller or collector is outside this threat model. A real system would need a separately justified way to enforce the assumed monitoring boundary.

The recorded interventions are deliberately changed motion settings. Treating those changes as unauthorized is the stated fixed-regime security scenario. An authorized operator could produce an identical physical trace: without an independent authorization signal, this detector cannot distinguish those cases. Mechanical faults, workload changes and sensor faults can also produce alarms; this dataset cannot establish their separation from attacks.

## Minimum meaningful twin representation

The proposed model represents **task motion**, not complete robot dynamics, motor torque, collision safety or a whole factory. It must maintain an asset-specific evolving state, make prospective predictions of measured joint state and document how observations synchronize that state. This operational requirement is consistent with NIST's emphasis on physical-system representation and prediction; it is our study definition, not a claim of standards compliance. See [NIST digital twins](https://www.nist.gov/digital-twins) and its [manufacturing use-case report](https://nvlpubs.nist.gov/nistpubs/ams/NIST.AMS.400-2.pdf).

A minimal candidate has:

- A normal task trajectory `q_ref(phase)` and expected joint velocity/progression learned from the designated **training** partition.
- A maintained estimate of where the arm is on that trajectory, with explicit ambiguity/uncertainty. Phase is inferred; it is not a supplied or independently verified production-phase label.
- A fixed nominal progression law. The current measured speed is evidence to check, not automatically the authorized speed to adopt.
- A documented causal state-correction rule and a separate progression/correction discrepancy. Model parameters, normalization, reference progression and thresholds remain fixed during evaluation.

At each eligible record, use its clock increment and **prior state** to propagate the nominal model; predict the joint observation without using the current joint values; compare the arriving joint values with that prediction; compute the declared innovation and correction/progression discrepancy; emit the score; only then apply the declared synchronization rule for the next record. A correction proposed from the current observation can be part of its score, but cannot be used to replace the pre-correction prediction. No future alignment or full-trace dynamic time warping is permitted in a claimed causal replay.

Integrating the current measured velocity as if it were the nominal command can make altered speed unsurprising by construction. Both an unconstrained phase follower and a bounded-correction variant must therefore disclose their rate/state policy. “Score before update” alone does not prove persistent deviations remain visible after several updates.

Before attack scoring, normal-only development must support repeatable trajectory structure, useful prospective prediction, bounded state uncertainty and a defensible correspondence between latent progress and observed joint motion. Check phase ambiguities and recurrence without inventing task labels from attack intervals. If this representation fails, keep the simple predictor comparison and remove the twin claim; do not choose a new architecture using final attack results.

## Necessary controls and what each tests

Every main control uses the same twelve measurements, normal-data partitions, relative-time policy and calibration rule. Exact implementations and finite hyperparameter grids are a later method-specification task; they must be fixed before attack scoring.

| Control | Scientific purpose / designation |
|---|---|
| Simple joint-velocity deviation score | Essential because the recorded intervention changes speed. Use training-derived normalization and normal calibration; no speed cutoff selected on attacks |
| Periodic reference/template | Tests whether ordinary repeated-motion structure is sufficient; CASPER already studies a phase-aligned periodic template |
| Ordinary causal predictor, initially autoregression | Tests whether an explicit synchronized task state adds value over a small generic predictor |
| Compact CNN predictor, if needed after the pilot | Informed by CASPER, but controller inputs and corrected evaluation make it a disclosed modified implementation |
| Same observer without progression/correction scoring | Main ablation isolating the proposed evidence channel, with the same state policy |
| Same observer with unconstrained phase following | Separate ablation of synchronization policy; causal and given the same observations, not an offline oracle |
| Fixed/free-running nominal reference | Measures the cost of avoiding synchronization, including accumulated normal drift |

Do not turn every ablation into another “paper baseline.” CASPER, TWINE and CatBoost remain the three learning papers. TWINE/CatBoost's inspected supervised classifiers require different labelled training and cannot enter this normal-only ranking unchanged. Three comparable recent published methods are **not yet established**. A strong final paper may require more appropriate comparators and independent data; no quota will be filled by mislabelling reimplementations.

## Evaluation that can refute the idea

The versioned [annotation/feature/split contract](ANNOTATION_FEATURE_SPLIT_CONTRACT.md) fixes the raw reference and prospective partitions. Normal training fits transforms/reference parameters; normal development selects configurations; separate normal calibration sets the nearest-rank 99th-percentile threshold; a held-out normal block measures actual alarm burden. The final replay then continues through every recorded intervention/recovery interval without resets triggered by labels.

Record **unadjusted point precision, recall and F1 against the schedule labels**, actual held-out-normal point exceedance and alarm episodes, score coverage, all eight interval outcomes and delays from recorded flag transitions. Later scheduled-zero recovery periods must be reported separately from held-out pre-intervention normal data. Delays are relative to the recorded schedule, not verified physical onset. Native-clock duration excludes declared gaps/unknown coverage; do not use wall-clock or cross-device assumptions.

The main scientific contrast is progression-aware versus otherwise matched progression-omitted monitoring, accompanied by the simple controls. Evidence for benefit requires improved declared detection behavior without concealing a deterioration in held-out-normal alarms or coverage. If the outputs trade off these objectives, report the trade-off; do not tune thresholds on final attacks to manufacture a winner. Exact analysis/operating-point specifications must be frozen with the model configurations before the first final score is examined.

An event hit alone is weak evidence for eight long intervals: a noisy detector may eventually alarm within all of them. Point behavior, normal burden, misses and coverage therefore accompany every event table. One trace is not millions of independent experiments; random seeds measure fitting variability, not independent-plant generalization.

The proposed contribution is unsupported if simple velocity/template controls perform as well, removing progression evidence has no effect, normal synchronization produces excessive alarms, or results depend on favorable annotation edits/exclusions. If the task is trivial for simple controls, report that and reassess scope. Do not add synthetic difficulty and call it a newly observed physical attack.

## Feasibility and publication limits

Qualitative FINER assessment: **feasible for a bounded local study**, relevant to monitoring under a specified command threat, and interesting because state tracking and anomaly preservation can conflict. **Novelty remains unverified.** Offline public-data analysis is within current authorization; robot experiments, external services and publications are separate actions. These judgments are planning assessments, not an acceptance score.

Twelve float32 channels for 1,762,650 records require approximately **84.6 MB** before timestamps, indices, libraries and model state (arithmetic estimate). A streaming parser and small template/AR/state models are plausible on the recorded M5 Pro / 24-GB machine; do not materialize every overlapping window. Runtime and training memory require a later bounded pilot. No environment or training is created here.

The [dated prior-art screen](literature/RQ_PRIOR_ART_SCREEN_2026-10-16.md) records important overlap: CASPER already has periodic alignment; the TinyML follow-up studies task segmentation and prediction residuals; CASPER+ proposes state reconstruction/segmentation. General twin synchronization also has prior literature. Therefore adding a phase variable, a template, segmentation or a “twin” label is insufficient novelty. The specific evidence-preservation comparison still needs a broader targeted review and experiments.

Strong journal claims would additionally need suitable independent tasks/runs or another justified dataset/testbed, relevant competitive methods, a defensible state model and transparent uncertainty. Current data support a **single-recording feasibility study of scheduled motion deviations**. They do not establish authorized-change handling, fault/attack discrimination, arbitrary sensor-spoofing robustness, physical safety, transfer to other robots, real-time deployment or publication readiness.

The manufacturing question concerns **state synchronization with a fixed reference**. Water's provisional question concerns **adapting model/calibration parameters under potentially corrupted measurements**. This distinction organizes the projects; separate publishable contributions still require evidence and an overlap review.

## Next bounded action

Review the machine-readable contract and independent [contract critique](RQ_CONTRACT_REVIEW.md), then specify the simple velocity/template/AR baselines and the normal-only state-validation procedure. Implement and test the loader, split isolation, time/gap handling and metrics only in the next authorized step. No training, final attack scores, new labels inferred from detector outputs or frozen claims of novelty follow from this decision.
