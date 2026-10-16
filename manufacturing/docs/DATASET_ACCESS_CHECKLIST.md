# Manufacturing dataset and testbed access checklist

Audit status, **16 October 2026**: no manufacturing benchmark data files have been acquired. Public provider metadata, small documentation and download response headers were checked. This is not a claim about private files outside the workspace. No simulator, VM or benchmark archive was acquired.

Recommended anchor: **original CASPER pick-and-place v3**, from [Hakan Kayan's provider listing](https://www.kaggle.com/datasets/hkayan/industrial-robotic-arm-anomaly-detection). Metadata identifies 2023-02-11, CC BY-SA 4.0, five files totalling 7,899,312,074 bytes. A public unauthenticated archive request returned HTTP 200 / ZIP / 2,824,019,108 bytes; body unread. **Institutional approval was not required for this observed public route.** Local hashes, schema and label validation remain pending. See the [full provider/access evidence](literature/OPEN_DATASET_SCREEN_2026-10-16.md).

## Candidate access paths

| Candidate | Artifact type | Local access | Outstanding decision |
|---|---|---|---|
| [Original CASPER](https://www.kaggle.com/datasets/hkayan/industrial-robotic-arm-anomaly-detection) — priority | Physical robot, IMU/controller/network recording, documented velocity deviations | Public endpoint checked; no local raw files | Reconcile original vs corrected IMU, clocks/labels, exact bytes across methods, input trust and supervision. Record original CC BY-SA 4.0 terms |
| [CASPER 1 & 2](https://www.kaggle.com/datasets/hkayan/industrial-robotic-arm-imu-data-casper-1-and-2) — separate listing | Mixed original filenames and newer physical-disturbance recordings; v2, 2024-09-01; MIT metadata | Public endpoint checked; no local raw files | Not automatically the original release. Equal file sizes are not hashes. Do not inherit this license or disturbance labels into the original collection |
| [MIT Manufacturing Operations v1](https://zenodo.org/records/17238360) | Synthetic machining/assembly; CC BY 4.0; about 18 GB archives | Maker archive headers checked; no local raw files | Three-paper adoption unestablished; separate attack/failure fields, exclude debug/future columns; `y_label` is not attack-only |
| [CMU TEP manipulations v1](https://doi.org/10.1184/R1/23805552.v1) | Chemical-manufacturing attack simulation; CC BY 4.0; about 7.05 GB archive | Archive headers checked; no local raw files | Distinct from TEP fault data; verify normal-file terms, independent runs and exact method overlap |
| [FactoryIO_TSC](https://github.com/carolsworld/FactoryIO_TSC) / [LOTL-Hunter](https://github.com/carolsworld/LOTL-Hunter) | Separate manufacturing simulation corpora, publicly listed artifacts | No datasets, scenes, VMs or models acquired | Different datasets; code/data licenses unresolved; LOTL raw network data partly by request; licensed regeneration |
| [Factory I/O / MinTWin author workflow](https://github.com/csmcguan/mintwin-svm-factoryio) | Older simulation/workflow background | None | No in-window baseline eligibility established; simulator and code licensing still need review |
| [NIST SMS Test Bed](https://www.nist.gov/laboratories/tools-instruments/smart-manufacturing-systems-sms-test-bed) | Physical manufacturing observations and data services | None; endpoints/data packages not exercised | Whether any release contains attacks, faults, changeovers, synchronized commands, and usable labels; exact access terms and version |

These are alternatives, not a commitment to evaluate all. The [selection report](BASELINE_SELECTION_REPORT.md) documents original-CASPER source/file overlap for the learning set; byte-identical release and comparable label/input access are not yet established. The [literature register](LITERATURE_EVIDENCE.md) records paper-specific uncertainty separately.

## Original CASPER receipt checklist

- [x] Identify author/custodian and original listing, version/date, advertised license and filenames.
- [x] Verify a public archive response without credentials; record that no body was read.
- [x] Identify recent paper/code links to original filenames; distinguish the newer collection.
- [ ] Recheck current release/terms and local storage before bounded acquisition; retain provider metadata with receipt.
- [ ] Download only the scoped files/archive into ignored `datasets/raw/casper/<release>/`; preserve originals.
- [ ] Verify archive integrity and compute local SHA-256/byte sizes. Provider sizes are not measurements.
- [ ] Map `dataset/nicla.csv`, `dataset/right_arm.csv`, and `nicla_fixed.csv`; identify what the correction changes before adopting it. Left-arm/PCAP are not required merely because present in the archive.
- [ ] Verify timestamp units, clock offsets, sample rates/gaps, labels and run boundaries; reconcile paper table with actual `Anomaly State` and sensor alignment.
- [ ] Establish independent training/calibration/evaluation periods and each method's permitted inputs/training labels.
- [ ] Freeze release and derivative manifests only after these checks. No benchmark or local dataset hash is currently available.

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

Public access, received bytes, a functioning loader, and a defensible benchmark are separate milestones. Only the first is verified for the preferred collection. No dataset access application is necessary for the tested public route; no blanket permission for uploading data or starting experiments follows.
