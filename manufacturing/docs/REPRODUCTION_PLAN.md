# Proposed manufacturing reproduction plan

Planning updated 16 October 2026 after the user authorized original-CASPER acquisition, manuscript follow-up, Step 0 teaching and a fair comparison protocol. Receipt/structural inspection and targeted manuscript/code collection are complete within their documented coverage; no environment, dependency installation, simulator execution or training has occurred. Read the newer [comparison protocol](COMPARISON_PROTOCOL.md) for explicit separate information-access groups, split/calibration proposals and unresolved gates.

## 1. Resolve the setting and evidence

Prioritize original CASPER industrial robotic-arm pick-and-place observations. Receipt hashes and a structural profile are recorded in the [identity audit](CASPER_DATASET_IDENTITY.md); cross-clock annotation and scientific suitability remain separate issues. Define malicious interventions separately from faults and authorized speed/task changes. Specify the evaluation target: anomaly detection, attack classification, or command/sequence consistency. Do not promise attack attribution from anomaly scores alone.

The [selection report](BASELINE_SELECTION_REPORT.md) recommends **CASPER 2024 → TWINE 2026 → CatBoost 2026** for critical study. CASPER is the conditional first reproduction candidate; no numerical baseline is admitted yet. Complete missing full manuscripts, release reconciliation, code-use permissions and paper-to-run mapping first. Keep the 2025 edge paper as related-data reserve. FactoryIO/LOTL/MIT/TEP are independent alternatives, not interchangeable data.

### Proposed method-specific work, not executed

| Method | Required decision before pilot |
|---|---|
| CASPER 1D-CNN | Audit synchronization and label derivation; partition before rolling filters/windows; confirm original code license or specify our independent implementation. Replace best-test-F1 threshold selection with an independently calibrated rule and disclose the deviation. |
| TWINE | Obtain full manuscript; reconcile full-feature RF100, five-feature/subsampled simulation and SHAP RF50 paths; fix demo length/model-reference inconsistencies. Study local detector separately from Azure display/state synchronization. A local-only run cannot be called a reproduced cloud/twin deployment. |
| CatBoost | Obtain full manuscript/run provenance and resolve code license. Do not run the inspected synthetic-label/padded-row pipeline as a cyber benchmark. A CatBoost control using authentic aligned labels, common features, train-only scaling and independent splits is our **independent implementation under a changed protocol**, not faithful reproduction. |

The original collection contains different modalities; CASPER uses external IMU while TWINE uses controller telemetry, and the methods have different supervision. Predefine an equal-input track or explicitly separate information-access/supervision tracks. Changing inputs, labels and splitting can change the scientific task. If no fair protocol is possible with available episodes, revise the comparison before training.

## 2. Freeze a reproducible evaluation contract

After access and method selection, freeze dataset identities/hashes, training/validation/test partitions, observable channels, attack/event semantics, normal periods, warmup, missing-data rules, and evaluation script specification. Use the same release and evaluation rules across comparative methods. Keep faithful paper reproduction distinct from any protocol correction and our independent implementation; disclose all changes.

Do not tune thresholds, hyperparameters, feature selection, or preprocessing on held-out test attacks. Partition by chronology and production run/cycle before constructing windows, with context gaps where required. Do not forward-fill across splits or use future interpolation. For any later adaptive method, score each observation before allowing an update and record state transitions.

Report unadjusted point metrics where meaningful, event detection and delay, and false alarms per operating hour or production cycle. Document alarm merging, event matching, missing events, and undefined metric cases. Point adjustment is not a substitute for raw scores; any reproduction requiring it must be separately labelled. No metric is evidence of industrial deployment.

## 3. Proposed minimal implementation, after audit approval

Keep all artifacts project-local. Run commands from `manufacturing/` and use its dedicated ignored `.venv/`, selecting Python and pinning dependencies only after checking the chosen baseline. Paths below resolve from this project root. Do not share mutable environments with water or smart grids or modify system packages.

| Location | Proposed responsibility |
|---|---|
| `src/manufacturing_dt/` | Dataset adapters, chronological/run-aware partitions, process-state interfaces, evaluation |
| `tests/` | Small clearly labelled synthetic fixtures and meaningful loader/split/metric checks |
| `configs/` | Immutable dataset, protocol, model, and seed specifications |
| `baselines/` | Pinned upstream references or separately labelled reimplementations, after license checks |
| `datasets/` | Local ignored raw/derived artifacts plus permitted manifests; no raw data in Git |
| `experiments/` | Run manifests, commands, logs, environment/code revisions, and permitted outputs |
| `papers/`, `docs/`, `manuscript/` | Permitted literature artifacts, evidence/decisions, and eventual writing |

Record seeds, dependency versions, hardware, code revisions/dirty state, configurations, data and split hashes, full commands, timestamps, and logs for every reported experiment. A synthetic smoke test is never a benchmark result.

## 4. Tests to specify before real evaluation

- Loader: explicit schema/units, timestamp monotonicity and duplicates, missing channels, categorical process states, and attack/fault/normal label mapping. Never silently coerce a fault into an attack.
- Split: no timestamp, cycle, or run overlap; no duplicated simulated replay across partitions; windows and fitted transforms respect split boundaries.
- Temporal state: no future samples or test labels in twin initialization, context inference, residuals, or features; test reset/warmup rules across jobs.
- Metrics: hand-checkable confusion matrices, no-positive cases, event boundaries, multiple alarms per event, delay, and false-alarm time denominators.
- Provenance: manifest identifies synthetic fixtures explicitly and distinguishes source release from local transforms.

## Stop conditions and completion criteria

Stop before substantial implementation when access, label semantics, baseline eligibility, or protocol are unresolved. Resolve costs and platform feasibility before any VM/simulator work; obtain approval for paid compute, lengthy training, or publishing. A future first reproduction is complete only when the authorized baseline runs on a verified release with frozen evaluation, documented deviations, and traceable logs. No such reproduction exists now.
