# Research-question and contract review

Manufacturing / Haiqa Mushtaq. **16 October 2026.** Independent design review of the selected right-arm route, using the recorded dataset, paper/code and clock audits. This is a proposed-design critique, not a model validation, security certification or novelty assessment. No models or attacks were executed.

## Decision and scope

The right-arm route is feasible for a bounded study of **documented command-speed manipulations under truthful controller telemetry**. It is narrower than monitoring a fully compromised controller and narrower than distinguishing attacks from authorized changeovers or physical faults. The original broad changeover/sequence question is not supported by this one-task recording.

Use the six joint positions, six joint velocities and within-controller elapsed differences under the [source-supported field interpretation](CASPER_SENSOR_SCHEMA.md). A candidate observer can represent nominal task progression and predict the corresponding motion state. State correction must not silently redefine the allowed progression. Ordinary forecast accuracy is not sufficient evidence that the representation is a validated physical twin.

The source corpus supports eight schedule-flagged interventions in one repeated task. Labels identify scheduled intervals, with uncertain physical onset; see the [label/time audit](CASPER_LABEL_TIME_AUDIT.md). Published behavior on this corpus cannot establish general manufacturing security, unseen-task generalization, attack attribution, physical safety or live protection.

## Required dispositions

| Review concern | Required disposition before execution |
|---|---|
| **Trust boundary** | Restrict the attacker to command/application-path speed manipulation. Assume joint observations, timestamps, monitoring process and commissioning data remain trustworthy. Explicitly exclude controller/firmware or recorder compromise. The matched capture script both sends commands and logs observations; it does not demonstrate independent authentication or a protected monitor. |
| **Attack versus authorized operation** | State that the experiment treats the recorded interventions as disallowed deviations from a fixed nominal task. The detector has no authenticated task/authorization context. Its alarm cannot establish malicious intent. |
| **Speed absorbed by synchronization** | Keep nominal progression learned from normal data. Compute innovation before correction and retain the correction/progression discrepancy. An observer that integrates observed velocity or freely follows inferred rate can absorb the tested manipulation. Score-before-update alone does not prevent this. |
| **Trivial comparison** | Include a simple joint-velocity magnitude/profile detector and a simple nominal periodic reference. CASPER already contains a periodic-template comparison. A complicated observer is not justified if these controls explain the result. |
| **Twin interpretation** | State the actual estimated variable and correspondence to this asset. Validate normal-data state consistency and prospective prediction without inventing physical phase truth, joint-command authorization or inverse dynamics. If evidence supports only a behavioral observer, use that term. |
| **Clock leakage** | Exclude absolute boot time, global row number, label-derived position and the known attack schedule. Relative time is available for state propagation and validity checks, not a hidden schedule feature. Clock units do not establish physical attack onset. |
| **Single 0.1-second interval** | Choose gap handling before detector output is available. Preserve the observed gap, reset or propagate under a declared policy, and expose lost/warmup coverage. Do not interpolate a missing state or let one acquisition irregularity become an attack predictor. |
| **Final replay continuity** | Carry state continuously through all final flagged and flag-zero periods. Resets/exclusions can depend on partition boundaries or observable data validity, not on true attack starts, ends or recovery labels. No per-event initialization with privileged knowledge. |
| **Normal evaluation** | Retain a held-out initial scheduled-normal block for the main normal-alarm assessment. Later zero flags may include recovery and are not independently certified benign. Report them separately rather than treating all zero rows as interchangeable healthy data. |
| **Long positive intervals** | Eight long intervals make eventual event-hit recall easy for a noisy detector. Pair event outcomes with unadjusted point performance, normal alarm burden, coverage and per-event delay. Do not make event recall alone the evidence of success. |
| **Timing of alarms** | A delay from the first positive controller flag is a recorded schedule-reference delay. Do not rename it precise physical attack-onset delay. Include missed and unscored events, not only detected-event averages. |
| **Phase ground truth** | No cycle or phase IDs are available. A learned phase is a model state; numerical fit or apparent periodicity does not independently validate physical task segmentation. |
| **Test isolation** | All eight final events remain evaluator-only. Parameters, checkpoint choice, phase-rate bounds, aggregation, score fusion, threshold and preferred variant must be selected without those outcomes. Preserve negative results after the frozen final evaluation. |

## Baseline and evidence consequences

TWINE's supervised random forest, CatBoost's inspected script and CASPER's external-IMU CNN do not form a faithful three-way comparison with a normal-only joint-state observer. Preserve them as learning papers and admit only methods with matching information access. A modified objective, feature set or implementation must be named explicitly. The [comparison protocol](COMPARISON_PROTOCOL.md) needs a distinct right-arm normal-only group; do not silently reinterpret the existing groups.

CASPER already studies repetitive-motion prediction and periodic templates. The CASPER+ programme overlaps task segmentation and IMU-to-state ideas. Therefore the broad use of phase, a reference model or an external sensor is not an established novelty claim. The potentially testable issue is whether preserving nominal progression evidence during synchronization adds value beyond simpler controls. That remains an untested hypothesis.

The recording permits a useful initial study, but repeated random seeds do not add independent tasks or attack campaigns. Eight interventions in one acquisition cannot support broad population claims or strong causal attribution. Additional independently acquired runs/tasks and controlled benign changes would be needed for broader claims; a leading-journal outcome is not established by the present scope.

## Go/no-go rules

Proceed toward software tests only after the annotation/feature/split contract fixes raw identity, label semantics, chronological partitions, permitted inputs, valid-time/reset rules, calibration and comparison units. Proceed toward a bounded model pilot only after the implementation/configuration and finite normal-only selection rules are documented and validated. The current review grants no training, paid compute or publication authorization.

Stop or narrow the claim if normal-only evidence does not support a repeatable state representation, if a required input is unavailable or untrusted under the chosen threat model, or if the observer needs test-event labels to initialize or choose its progression policy. A failure of the observer to outperform a simple velocity or template control is a reportable negative result, not a reason to revise the holdout.

## Concrete contract review

Reviewed the [question/threat-model decision](RESEARCH_QUESTION_AND_THREAT_MODEL.md), [annotation/feature/split contract](ANNOTATION_FEATURE_SPLIT_CONTRACT.md) and its [JSON companion](../configs/casper_right_arm_contract_v0.1.json). The final reviewed snapshots were fingerprinted at **2026-10-16T18:27:18.796791Z**:

| Artifact | SHA-256 of reviewed snapshot |
|---|---|
| `configs/casper_right_arm_contract_v0.1.json` | `3e88c87761b16aa808af188b8419fa48c3ef938a68441c70d1ba05467a779a25` |
| `docs/ANNOTATION_FEATURE_SPLIT_CONTRACT.md` | `83bbcd1cf7e0bb99dfa2d8e9f6c5154ef1641f6f67878992845810586eb78f82` |
| `docs/RESEARCH_QUESTION_AND_THREAT_MODEL.md` | `c16601ffe811ce63126eebb3cac7be6d9fb3f98cf531c95ce10234d16e62a291` |

These fingerprints identify the reviewed versions; a later edit requires checking the changed material. A small read-only standard-library check independently confirmed the cumulative-floor split boundaries, positive-row total of 345,602 and placement of every positive event after the normal prefix. It did not parse raw sensor arrays, fit models or calculate detector performance.

**Disposition: the metadata design is coherent for the restricted study; execution is not admitted.** No direct label, future-observation or partition-overlap leak was identified in the written contract. The selected q/qdot features, relative-time use, normal-only selection/calibration, continuous final replay and explicit exclusion of true event boundaries from runtime are consistent with the narrow threat model. This is a review of a plan, not verification that an eventual loader or model enforces it.

The review identified three metric edge cases and the snapshots above resolve them:

1. Event-hit recall was too weak as the main outcome for eight long intervals. The contract now requires joint reporting of mixed-slice unadjusted point metrics, held-out-normal alarm burden and coverage; all eight event outcomes remain mandatory secondary analyses.
2. An alarm already active before a flag transition can overlap that interval at delay zero without a new detection. The contract now records pre-existing alarms, interval-overlap delay and fresh negative-to-positive transitions separately, without resetting episodes at labels or reporting slices.
3. A positive first scored point after warmup/gap/unknown has an unobserved onset. The contract now flags left/right censoring and names its rate observed alarm episodes per eligible hour. Exposure includes only intervals between adjacent eligible endpoints within the held-out-normal slice; no boundary duration is invented. Episode counts, exposure and censoring must accompany the rate.

A common structural mask and explicit missing-score/coverage gate also prevent a method from silently improving its conditional score by abstaining on difficult endpoints. Model-specific histories, the provisional 1,528-observation warmup floor, initialization, score aggregation/fusion, normal-development objectives and missing-score policy remain specified execution gates. They must be settled before final scoring; a design-review freeze does not imply those implementation choices are complete.

The question document addresses the remaining scientific concerns explicitly: truthful telemetry is assumed; the collector's real trust boundary is unverified; current velocity must not automatically replace nominal progression; a simple velocity control is essential; phase truth is absent; and a twin claim depends on normal-only state/prediction validation. No fatal contradiction was identified within that restricted scope. The single task, single acquisition, scheduled labels and unverified novelty still limit the research claim.
