# Proposed manufacturing reproduction plan

Planning only, 16 October 2026. No code, environment, dependency installation, dataset download, simulator execution, or training is authorized by this setup document. Detailed manufacturing audit follows the water audit in the user's requested sequence.

## 1. Resolve the setting and evidence

Select one manufacturing process after assessing observable production state and lawful data access. Define malicious interventions separately from faults and authorized job/recipe/changeover transitions. Specify the evaluation target: anomaly detection, attack classification, or command/sequence consistency. Do not promise attack attribution from anomaly scores alone.

Expand the [seed register](LITERATURE_EVIDENCE.md) into a full audit of relevant in-window detection methods. Verify manuscripts, dates, author code, licenses, data releases, preprocessing, splits, thresholds, metrics, and resource requirements. The current three twin papers do not establish a ready common detection benchmark; **first main baseline selection is blocked**. The Factory I/O author workflow is a conditional feasibility lead, not a committed reproduction or proof of eligibility.

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
