# Smart-grid data access and suitability checklist

Updated **2026-10-16**. **No smart-grid dataset files have been acquired for this project.** No external storage path or authorization has been confirmed. Repository documentation and provider metadata are leads, not local dataset access. No download, licence acceptance, or request has been performed.

## Candidate routes

1. **Observed/testbed event data:** investigate the creator-provided MSU/ORNL Power System Attack Datasets. First determine whether its published sampling preserves the chronology and topology/event information our question requires. If not, restrict its role to explicitly described classification or seek suitable source recordings.
2. **Synthetic electrical trajectories:** investigate PNNL GridSTAGE only if a labelled simulation study fits the question and dependencies are available. A generated scenario must remain labelled simulated, even if based on an IEEE network case. A simulator cannot establish field effectiveness.

Primary source descriptions and known limitations are in [the evidence register](LITERATURE_EVIDENCE.md). Neither route is selected. SWaT/WADI access does not provide grid data or permission for this project.

## Before acquisition

- [ ] Record provider, exact release/commit, licence and terms, permitted users/use, redistribution rules and citation requirements. Public download availability alone is not complete permission evidence.
- [ ] Confirm the source includes electrical-state measurements needed by the question, not solely packets, intrusion alerts or event names.
- [ ] Verify timestamps, sequence ordering, sampling/downsampling, original versus derived files, and event/scenario identifiers. Do not reconstruct unknown chronology by sorting arbitrary row identifiers.
- [ ] Establish available topology, switching history, breaker status, line/bus mapping, sensor placement, operating conditions and trusted signals. Identify oracle-only information that the detector cannot use.
- [ ] Separate authorized switching, load changes, physical faults, equipment/sensor errors and malicious actions. Check if benign events and attacks can be matched on operating conditions without using test labels for model selection.
- [ ] Check simulator/toolbox licences, local availability, disk requirements and reproducibility before proposing any download or run. No paid dependency or compute is authorized.

## On later authorized receipt

- [ ] Preserve raw originals unchanged under ignored project-local storage (for example `datasets/raw/<source>/<release>/`); never publish them by default. Keep credentials and private URLs in ignored local records.
- [ ] Record original names, byte sizes, SHA-256, source/version, acquisition date, terms and readme references. No manifest values are populated yet.
- [ ] Verify units (including per-unit bases), voltage/current phase conventions, reference/slack bus, angle conventions, bus/branch mapping, timestamps/timezones, cadence and missingness.
- [ ] Preserve complete runs/scenarios; distinguish independent scenario seeds from many correlated windows of one trajectory. Identify duplicate or derived copies across proposed splits.
- [ ] Verify attack and benign-event labels separately from feature fields. Remove scenario IDs, post-event alarms or ground-truth fields that would reveal the answer unless they are legitimate declared detector inputs.
- [ ] For simulation, record engine/version, case revision, solver/time step, loads, controllers, noise, sensors, event schedules, topology changes, random seeds and convergence checks. Keep simulator truth separate from simulated observed measurements.
- [ ] Freeze shared releases, splits, measurement access and preprocessing across future comparisons. If chronology is unavailable, document the narrower task instead of claiming online detection.

Proposed manifest: `source_id, release_or_commit, data_kind, original_filename, bytes, sha256, terms_reference, acquisition_date, topology_hash, sensor_map_hash, units_and_bases, timestamp_and_cadence, scenario_id, seed_if_simulated, event_label_provenance, split_group, preprocessing_revision`. All file-derived fields remain **unknown**.
