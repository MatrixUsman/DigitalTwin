# Manufacturing dataset and testbed access checklist

Setup status, 16 October 2026: no manufacturing data files have been acquired or confirmed in this newly created project folder. This is not a claim about private files outside the workspace. No dataset, simulator, VM, or paper attachment was downloaded for this setup.

## Candidate access paths

| Candidate | Artifact type | Local access | Outstanding decision |
|---|---|---|---|
| [Factory I/O / MinTWin author workflow](https://github.com/csmcguan/mintwin-svm-factoryio) | Simulated manufacturing production-line experiment; code/capture instructions visible | None; no VM, scene, or captures acquired | Public fixed dataset versus regeneration; code/data permissions; paid simulator license and Windows/VM compatibility; documented attack ground truth and protocol |
| [NIST SMS Test Bed](https://www.nist.gov/laboratories/tools-instruments/smart-manufacturing-systems-sms-test-bed) | Physical manufacturing observations and data services | None; endpoints/data packages not exercised | Whether any release contains attacks, faults, changeovers, synchronized commands, and usable labels; exact access terms and version |

These are alternatives to investigate, not a commitment to evaluate both. No common release shared by candidate methods is established. The [literature register](LITERATURE_EVIDENCE.md) records paper-specific data uncertainty separately.

## Before acquiring or using any data

- [ ] Confirm publisher/custodian, exact release/version/date, license, access agreement, redistribution and derivative-data restrictions.
- [ ] Obtain authorized access without contacting authors or submitting forms on the user's behalf unless instructed.
- [ ] Record filenames, byte sizes, hashes, origin, acquisition date, provenance, and label definitions in a manifest without committing raw data.
- [ ] Identify actual manufacturing process and physical versus simulation provenance; record simulator, scene, controller, model, and seed versions if generated.
- [ ] Separate malicious interventions, physical faults, quality defects, and authorized transitions. Verify attack start/end semantics and success/physical impact if known.
- [ ] Verify timestamps/time zones, sampling rates, sensors, actuators, command logs, controller state, job/recipe identifiers, and run/cycle boundaries.
- [ ] Check normal-operation coverage, transitions/changeovers, duplicated runs, missing periods, warmup, resets, and attack recovery.
- [ ] Establish chronological train/validation/test partitions and run/cycle grouping before windowing. Keep correlated replayed runs together.
- [ ] Define which channels and process context are observable to the detector at decision time. Avoid labels or future state as features.
- [ ] Confirm whether twin initialization, physical parameters, state synchronization, and independent references can be reconstructed from permitted artifacts.
- [ ] Preserve raw files unchanged and outside Git; keep derived data local with documented transforms and provenance.

Access, a data catalog entry, a functioning loader, and a defensible benchmark are separate milestones. None implies the next automatically.
