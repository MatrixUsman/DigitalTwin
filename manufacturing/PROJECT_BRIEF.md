# Manufacturing research project

Last updated: 17 October 2026. Project owner: **Haiqa Mushtaq**. Ownership is an organizational assignment, not a decision about academic authorship.

This is an independent academic research project on cybersecurity of manufacturing cyber–physical systems. Its current stage is beginner teaching, original CASPER receipt/identity audit, targeted manuscript study and comparison planning. The original CASPER archive and five members have been acquired with integrity checks and hashes; a corrected CASPER manuscript, pinned code/documents and explicitly author-reported tables/figures are stored locally. A [study guide](docs/DATA_AND_BASELINE_STUDY.md) connects full controller-schema validation, annotation lineage and paper-to-code findings. No baseline has been reproduced and no experimental performance results exist.

## Provisional direction

Working title: **“Digital Twins for Robotic Motion Integrity: The Role of State Synchronization.”** The twin designation remains conditional on state/prediction/coupling validation.

Selected feasibility question: **Does retaining a nominal cycle-progression reference during state synchronization improve a motion twin's detection of CASPER's recorded right-arm speed changes under normal-only calibration?**

The [question/threat-model decision](docs/RESEARCH_QUESTION_AND_THREAT_MODEL.md) selects a **normal-only right-arm controller-telemetry study** using joint positions, joint velocities and relative elapsed time. The restricted adversary changes motion commands; telemetry/time delivered to an assumed protected monitor remain truthful. No authentication or resistance to fully compromised controller firmware is established by the dataset. Model parameters/reference/calibration stay fixed during replay; the subject is state synchronization, distinct from water's provisional parameter-adaptation question.

The earlier question about attacks versus authorized changeovers and faults is deferred because the original collection lacks the required independent ground truth. External-IMU reproduction remains a separate track. **CASPER (2024), TWINE (2026), and CatBoost on CASPER (2026)** remain learning papers, not three comparable admitted methods. Right-arm simple velocity/template/AR controls now come first for feasibility; a controller-input CASPER CNN is a modified implementation. TWINE/CatBoost's supervised workflows cannot be pooled unchanged into the normal-only comparison. Novelty remains unverified; see the [dated overlap screen](docs/literature/RQ_PRIOR_ART_SCREEN_2026-10-16.md).

The distinction between an attack, a fault, and an authorized transition must come from documented ground truth. “Cyber-physical,” predictive maintenance, or generic ICS branding alone does not establish cybersecurity relevance or manufacturing data. A simulator, a detector dashboard, and a state-coupled digital twin are different artifacts and must be described accurately.

## Scope and decision criteria

- Screen main comparative papers published from **16 October 2023 through 16 October 2026**, preferably 2024–2026. Record online, issue, and preprint dates separately; keep older background separate.
- Select manufacturing-specific data and comparable protocols. SWaT and WADI are not imposed on this project. Do not reuse water findings as manufacturing evidence.
- Require identifiable process semantics, attack labels or documented injection events, normal operation, and timing before claiming process-aware cyberattack detection can be evaluated.
- Establish what the proposed twin knows at each timestamp, how its state is synchronized, and what independent trusted information exists. A predictive model alone is not automatically a validated twin.
- Keep title, mechanism, comparison set, and contribution provisional until a faithful baseline and an explicit literature-gap audit support decisions.

## Setup deliverables and next stage

Use the [complete paper roadmap](docs/PAPER_ROADMAP.md) for current completion states, remaining implementation/scientific gates, manuscript development and submission. It does not authorize the future runs or publication it describes.

The [identity register](docs/DATASET_IDENTITY_REGISTER.md) records exact received bytes; the [manuscript audit](docs/MANUSCRIPT_COLLECTION_AUDIT.md) retains one full paper and two access gaps. The [annotation/feature/split contract](docs/ANNOTATION_FEATURE_SPLIT_CONTRACT.md) and [JSON specification](configs/casper_right_arm_contract_v0.1.json) now define the selected controller group. The [comparison protocol](docs/COMPARISON_PROTOCOL.md) keeps it separate from earlier IMU and supervised groups. The [evaluation protocol](docs/EVALUATION_PROTOCOL.md) now defines common eligible support, threshold-only calibration, metrics, fixed repeats and procedural protection of both final slices. The [freeze record](experiments/FINAL_TEST_FREEZE_RECORD.json) is pending; no calibrated artifact or final run exists. Data/evaluation definitions and foundational synthetic loader/metric tests are complete; model-specific transforms, initialization, scoring, fitting tests, normal-only selection objectives and pilot execution admission remain open.

The user selected manufacturing next while water waits for external access, then authorized original-CASPER collection/identification and protocol preparation. The [loader/metric software milestone](docs/SOFTWARE_VALIDATION.md) now passes 83 synthetic tests in a local isolated environment. The [bounded pilot](docs/BOUNDED_PILOT_PLAN.md) is specified but its control/supervisor and real-data fit remain pending. Data-audit utilities and synthetic software checks are not model reproductions or benchmark results. Simulator execution, paid services, training and publication remain outside this stage. The smart-grid project remains independently scoped.

## Shared publication and writing preferences

Apply the confirmed [shared publication standards](../docs/PUBLICATION_STANDARDS.md): aim for leading field-appropriate journals through rigorous distinct research, use natural precise academic prose, and develop distinctive titles grounded in the supported contribution. The user also records intended future EB-2 use; individual authorship, impact and publication claims must remain factual. Existing titles stay provisional, and no publication or immigration outcome is assured.
