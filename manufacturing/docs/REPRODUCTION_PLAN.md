# Manufacturing reproduction and implementation plan

Current execution record, **17 October 2026**: the [full-training control study](CONTROL_STUDY_REPORT.md) completed one bounded normal-only attempt after **205 synthetic tests passed across 34 source/configuration files**. Seven candidates each fitted 536,946 eligible training targets and produced 160,472 aligned development scores. The selected methods are the fixed velocity-deviation control, 32-bin periodic template and AR(4) with ridge 0.001. [Selected artifact identities](../experiments/SELECTED_CONTROLS_V0.1.json) are recorded for later calibration. These are independent ordinary controls, not digital twins or paper reproductions.

The [earlier smaller pilot](PILOT_REPORT.md) and [83-test loader/metric foundation](SOFTWARE_VALIDATION.md) remain preserved historical milestones. Both the pilot and full-training control-study v0.1 attempts are consumed; the concrete commands in their reports document completed runs, not commands to repeat. No calibrated threshold or final attack benchmark exists. Use [PAPER_ROADMAP.md](PAPER_ROADMAP.md) for the lifecycle and [COMPARATOR_ADMISSION.md](COMPARATOR_ADMISSION.md) for current paper-specific decisions. The initial three learning papers do not constitute three admitted experimental baselines.

**Current scope decision:** the [selected question and threat model](RESEARCH_QUESTION_AND_THREAT_MODEL.md) prioritize normal-only right-arm state/progression monitoring under a restricted command-path adversary. The [annotation/feature/split specification](ANNOTATION_FEATURE_SPLIT_CONTRACT.md) and [evaluation rules](EVALUATION_PROTOCOL.md) remain frozen. Essential control implementations and normal-only artifact selection are complete. The empirical observer has since been normal-only validated. The [scope decision](CONTRIBUTION_AND_EVIDENCE_SCOPE.md) narrows the claim to a single-acquisition score study; next specify and validate the bounded C/K/L/Rv extensions in the [core roster](COMPARISON_ROSTER_DECISION.md). ModernTCN remains conditional on broader claims. Freeze the complete comparison roster before threshold calibration. Calibration and both final slices remain closed; the control milestone does not establish twin fidelity, novelty or attack sensitivity.

## 1. Resolve the setting and evidence

Prioritize original CASPER industrial robotic-arm pick-and-place observations. Receipt hashes and a structural profile are recorded in the [identity audit](CASPER_DATASET_IDENTITY.md); cross-clock annotation and scientific suitability remain separate issues. Define malicious interventions separately from faults and authorized speed/task changes. Specify the evaluation target: anomaly detection, attack classification, or command/sequence consistency. Do not promise attack attribution from anomaly scores alone.

The historical [selection report](BASELINE_SELECTION_REPORT.md) identified **CASPER 2024 → TWINE 2026 → CatBoost 2026** for critical study. The subsequent [admission audit](COMPARATOR_ADMISSION.md) supersedes that shortlist's experimental implications. CASPER's original IMU reproduction remains a separate held track; TWINE's full manuscript now establishes incompatible supervision/inputs for Group D; the inspected CatBoost implementation is excluded from Group D and its full manuscript remains unavailable. ModernTCN is a conditional transferred-method candidate requiring a disclosed adapter and evaluation corrections. FactoryIO/LOTL/MIT/TEP remain independent alternatives, not interchangeable data.

### Paper-specific routing, no reproduction executed

| Method | Current designation and remaining work |
|---|---|
| CASPER 1D-CNN | Separate original-IMU reproduction held for checkpoint correspondence, original code terms and protocol resolution. Any controller-input CNN must be justified and identified as an independent modified implementation; it is not part of the completed essential-control suite. |
| TWINE | Full accepted manuscript obtained and audited. Background/critical study for Group D because supervised random-row training and wider features differ from our normal-only protocol. Any supervised/cloud comparison needs a separately defined track. |
| CatBoost | Background/critical study; inspected synthetic-label/padded-modality pipeline is excluded from Group D. Full manuscript, run correspondence and code-use gaps remain. A supervised classifier cannot become a normal-only control merely by changing its split. |
| ModernTCN | Conditional transferred-method candidate, not a published CASPER baseline. Specify the reconstruction/prediction interface, implement the adapter and remove upstream test-based selection/point adjustment under a documented modified protocol before execution admission. |

The original collection contains different modalities; CASPER uses external IMU while TWINE uses controller telemetry, and the methods have different supervision. Predefine an equal-input track or explicitly separate information-access/supervision tracks. Changing inputs, labels and splitting can change the scientific task. If no fair protocol is possible with available episodes, revise the comparison before training.

## 2. Freeze a reproducible evaluation contract

After access and method selection, freeze dataset identities/hashes, training/validation/test partitions, observable channels, attack/event semantics, normal periods, warmup, missing-data rules, and evaluation script specification. Use the same release and evaluation rules across comparative methods. Keep faithful paper reproduction distinct from any protocol correction and our independent implementation; disclose all changes.

Do not tune thresholds, hyperparameters, feature selection, or preprocessing on held-out test attacks. Partition by chronology and production run/cycle before constructing windows, with context gaps where required. Do not forward-fill across splits or use future interpolation. For any later adaptive method, score each observation before allowing an update and record state transitions.

Report unadjusted point metrics where meaningful, event detection and delay, and false alarms per operating hour or production cycle. Document alarm merging, event matching, missing events, and undefined metric cases. Point adjustment is not a substitute for raw scores; any reproduction requiring it must be separately labelled. No metric is evidence of industrial deployment.

## 3. Project implementation and remaining adapters

Keep all artifacts project-local. Run commands from `manufacturing/` and use its dedicated ignored `.venv/`, selecting Python and pinning dependencies only after checking the chosen baseline. Paths below resolve from this project root. Do not share mutable environments with water or smart grids or modify system packages.

| Location | Responsibility |
|---|---|
| `src/mfg_twin/` | Implemented loader/contract/replay/metrics, ordinary controls and bounded study/supervisor; candidate twin and paper adapters remain separate work |
| `tests/` | 205 passing synthetic checks covering data/evaluation, ordinary controls, selection and resource/provenance behavior; future methods require their own checks |
| `configs/` | Immutable dataset, protocol, model, and seed specifications |
| `baselines/` | Pinned upstream references or separately labelled reimplementations, after license checks |
| `datasets/` | Local ignored raw/derived artifacts plus permitted manifests; no raw data in Git |
| `experiments/` | Run manifests, commands, logs, environment/code revisions, and permitted outputs |
| `papers/`, `docs/`, `manuscript/` | Permitted literature artifacts, evidence/decisions, and eventual writing |

Record seeds, dependency versions, hardware, code revisions/dirty state, configurations, data and split hashes, full commands, timestamps, and logs for every reported experiment. A synthetic smoke test is never a benchmark result.

## 4. Checks required for subsequent methods and final evaluation

- Loader: explicit schema/units, timestamp monotonicity and duplicates, missing channels, categorical process states, and attack/fault/normal label mapping. Never silently coerce a fault into an attack.
- Split: no timestamp, cycle, or run overlap; no duplicated simulated replay across partitions; windows and fitted transforms respect split boundaries.
- Temporal state: no future samples or test labels in twin initialization, context inference, residuals, or features; test reset/warmup rules across jobs.
- Metrics: hand-checkable confusion matrices, no-positive cases, event boundaries, multiple alarms per event, delay, and false-alarm time denominators.
- Provenance: manifest identifies synthetic fixtures explicitly and distinguishes source release from local transforms.

## Stop conditions and completion criteria

Stop the affected method's progression when access, label semantics, baseline eligibility or protocol are unresolved. Preserve the completed independent-control evidence rather than equating it with unresolved paper admission. Resolve costs and platform feasibility before any VM/simulator work; obtain approval for paid compute, lengthy training or publishing. A first paper reproduction is complete only when its authorized method runs on a verified release with frozen evaluation, documented deviations and traceable logs. No paper reproduction exists now. The next bounded milestone is the versioned C/K/L/Rv score extension and independent-source admission design; the full-roster freeze, calibration and protected final campaign follow their own gates.
