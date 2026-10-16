# Manufacturing dataset and testbed access checklist

Receipt status, **16 October 2026**: the user authorized original CASPER acquisition. The archive and all five members are now stored unchanged under ignored `datasets/raw/casper/v3/`, with full ZIP CRC checks and SHA-256 hashes. See [CASPER_DATASET_IDENTITY.md](CASPER_DATASET_IDENTITY.md) and the [receipt manifest](../datasets/manifests/casper_v3_receipt.json). No other dataset, simulator or VM was acquired.

Recommended anchor: **original CASPER pick-and-place v3**, from [Hakan Kayan's provider listing](https://www.kaggle.com/datasets/hkayan/industrial-robotic-arm-anomaly-detection). Metadata identifies 2023-02-11 and CC BY-SA 4.0. Local byte measurements confirm the 2,824,019,108-byte archive and 7,899,312,074 bytes across five members. **Institutional approval was not required for this public route.** Dataset bytes/structure are identified; aligned IMU event labels, original capture provenance and experiment partitions remain unresolved. The later [sensor study](CASPER_SENSOR_SCHEMA.md) supports boot-relative seconds for controller clocks; it does not establish IMU synchronization. The [earlier provider/access screen](literature/OPEN_DATASET_SCREEN_2026-10-16.md) is historical access-only evidence.

## Candidate access paths

| Candidate | Artifact type | Local access | Outstanding decision |
|---|---|---|---|
| [Original CASPER](https://www.kaggle.com/datasets/hkayan/industrial-robotic-arm-anomaly-detection) — priority | Physical robot, IMU/controller/network recording, documented velocity deviations | Original archive + five files received, CRC/SHA-256 recorded | Resolve cross-clock event mapping, exact paper-run correspondence, input trust and supervision. Original CC BY-SA 4.0 terms retained |
| [CASPER 1 & 2](https://www.kaggle.com/datasets/hkayan/industrial-robotic-arm-imu-data-casper-1-and-2) — separate listing | Mixed original filenames and newer physical-disturbance recordings; v2, 2024-09-01; MIT metadata | Public endpoint checked; no local raw files | Not automatically the original release. Equal file sizes are not hashes. Do not inherit this license or disturbance labels into the original collection |
| [MIT Manufacturing Operations v1](https://zenodo.org/records/17238360) | Synthetic machining/assembly; CC BY 4.0; about 18 GB archives | Maker archive headers checked; no local raw files | Three-paper adoption unestablished; separate attack/failure fields, exclude debug/future columns; `y_label` is not attack-only |
| [CMU TEP manipulations v1](https://doi.org/10.1184/R1/23805552.v1) | Chemical-manufacturing attack simulation; CC BY 4.0; about 7.05 GB archive | Archive headers checked; no local raw files | Distinct from TEP fault data; verify normal-file terms, independent runs and exact method overlap |
| [FactoryIO_TSC](https://github.com/carolsworld/FactoryIO_TSC) / [LOTL-Hunter](https://github.com/carolsworld/LOTL-Hunter) | Separate manufacturing simulation corpora, publicly listed artifacts | No datasets, scenes, VMs or models acquired | Different datasets; code/data licenses unresolved; LOTL raw network data partly by request; licensed regeneration |
| [Factory I/O / MinTWin author workflow](https://github.com/csmcguan/mintwin-svm-factoryio) | Older simulation/workflow background | None | No in-window baseline eligibility established; simulator and code licensing still need review |
| [NIST SMS Test Bed](https://www.nist.gov/laboratories/tools-instruments/smart-manufacturing-systems-sms-test-bed) | Physical manufacturing observations and data services | None; endpoints/data packages not exercised | Whether any release contains attacks, faults, changeovers, synchronized commands, and usable labels; exact access terms and version |

These are alternatives, not a commitment to evaluate all. The [selection report](BASELINE_SELECTION_REPORT.md) documents original-CASPER source/file overlap for the learning set. Our received release is identified; its exact equivalence to every published run and comparable label/input access remain unestablished. The [literature register](LITERATURE_EVIDENCE.md) records paper-specific uncertainty separately.

## Original CASPER receipt checklist

- [x] Identify author/custodian and original listing, version/date, advertised license and filenames.
- [x] Verify public retrieval without credentials; distinguish the earlier header-only check from subsequent full acquisition.
- [x] Identify recent paper/code links to original filenames; distinguish the newer collection.
- [x] Recheck current release/terms and local storage before bounded acquisition; retain provider metadata with receipt.
- [x] Download the scoped archive and five members into ignored `datasets/raw/casper/v3/`; preserve originals.
- [x] Verify archive integrity and compute local SHA-256/byte sizes; distinguish provider metadata from local measurements.
- [x] Identify schemas and numeric original/fixed correspondence: fixed Nicla adds a header and changes serialization, with the same parsed numeric sequence after six raw startup records. It supplies no alignment/labels. Left-arm/PCAP were preserved but are not automatically detector inputs.
- [x] Inventory exact serialized controller timestamp endpoints and flag boundaries, source-supported units, native gaps/offsets, label counts and missing run/cycle identifiers; distinguish recorded flags from physical onset.
- [x] Identify PCAPNG container/clock options and all packet timestamps; record nonmonotonic steps without reordering raw data. Verify absence of IMU time/label columns.
- [x] Rehash archive and all five members against the preserved receipt; save a [consolidated manifest](../datasets/manifests/casper_v3_identity.json) and standard [checksum file](../datasets/manifests/casper_v3.sha256).
- [ ] Establish original executing capture configuration, calendar anchors/cross-device synchronization and defensible IMU event mapping; resolve the paper's 750-row IMU discrepancy and exact published-run byte identity.

The [current identity register](DATASET_IDENTITY_REGISTER.md) separates completed observations from these remaining scientific-use gaps. Same schedule flags on both arms do not imply identical commanded perturbations; the inspected later source varies right-arm speed while keeping left-arm speed at default.
- [ ] Establish independent training/calibration/evaluation periods and each method's permitted inputs/training labels.
- [x] Record the received release manifest and measured hashes.
- [ ] Freeze annotation/derivative/split manifests only after their separate provenance and chronology checks.

## General checklist for other collections and unresolved use gates

The original-CASPER receipt items above are complete only within their stated scope. The general checklist below remains reusable; acquisition does not complete its scientific-use gates.

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

Public access, received bytes, a training-ready loader, and a defensible benchmark are separate milestones. Access/receipt and a read-only structural profile are complete for the preferred collection; no training-ready adapter or benchmark is validated. No blanket permission for uploading data or starting experiments follows.

## Selected right-arm study contract — later same-day decision

The user subsequently requested a feasible question/threat model and exact annotations, permitted features and chronological splits. The [right-arm contract](ANNOTATION_FEATURE_SPLIT_CONTRACT.md) now defines recorded schedule labels, twelve joint-state channels, relative-time use, four chronological normal blocks and one continuous final replay. This closes **definition of those metadata fields for the restricted controller study**, not independent validation of onset, clean commissioning or a benchmark loader. The broader IMU/cross-clock and published-run questions above remain unresolved for their own tracks. Model-specific transforms, initialization/scoring and executable isolation/metric tests still precede a pilot.
