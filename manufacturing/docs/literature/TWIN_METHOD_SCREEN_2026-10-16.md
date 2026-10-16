# Manufacturing digital-twin method screen

Audit date: **16 October 2026, Asia/Karachi**. This is a bounded primary-source screen for the manufacturing project, owned by Haiqa Mushtaq. No detector, notebook, simulator, checkpoint or attack script was executed; no benchmark dataset was downloaded. It is not an exhaustive review or an experimental validation. The main-paper window is **2023-10-16–2026-10-16**, inclusive. An article's publication, its code's existence, its data accessibility and its readiness for a common protocol are separate findings.

The shared academic-research-suite's source-verification guidance was used, subject to the project's engineering-specific evidence rules. A paper is not marked human-read by this report.

## Most relevant finding: TWINE uses the Kayan robotic-arm corpus

**Mubashar Iqbal, Sabah Suhail, Simon Freudenthaler, Muhammad Fahim and Raimundas Matulevicius. “TWINE: ISO 23247-compliant digital twin and explainable AI framework for anomaly detection.”** Internet of Things **38**, 101976. DOI **10.1016/j.iot.2026.101976**. [Publisher](https://www.sciencedirect.com/science/article/pii/S254266052600106X); [Queen's University Belfast institutional record](https://pure.qub.ac.uk/en/publications/twine-iso-23247-compliant-digital-twin-and-explainable-ai-framewo/).

- **Dates/status:** the institutional record explicitly identifies a peer-reviewed article, early online **2026-05-26**, issue **July 2026**. The record supplies an accepted manuscript under CC BY. Its [PDF](https://pure.qub.ac.uk/files/689658736/TWINE.pdf) returned HTTP 403 in both browser retrieval and an independent ordinary HTTP request. Publisher-indexed abstract/introduction and institutional metadata were accessible; the full paper was **not read** in this screen.
- **Scientific role:** a manufacturing robotic-arm digital-twin/XAI integration comparator. The publisher describes supervised ML, SHAP and an Azure implementation. “ISO 23247-compliant” remains the authors' characterization: this audit does not certify standards compliance. The accessible abstract emphasizes operational anomalies; it does not independently establish attack-versus-fault discrimination.
- **Actual dataset evidence:** the [author repository README](https://github.com/mubashar-iqbal/TWINE/tree/841e1195acf90835c4c427e0fb48d10c08ed30d5) explicitly links the [Kayan industrial robotic-arm dataset](https://www.kaggle.com/datasets/hkayan/industrial-robotic-arm-anomaly-detection) and names **`right_arm.csv`**. Both inspected notebooks read that filename. This establishes a concrete shared-corpus lead for comparisons with papers using that corpus. It does **not** establish a shared release/hash, identical feature eligibility, identical partitions or equivalent attack ground truth.

### Matched code and observed behavior

Repository: `mubashar-iqbal/TWINE`; observed default-branch revision **`841e1195acf90835c4c427e0fb48d10c08ed30d5`**, commit timestamp **2026-05-22T10:12:45Z**. GitHub metadata and the actual `MIT-LICENSE.txt` identify MIT terms. README credits copying from `h1548782/seleniumforest`; preserve that provenance. The included license notice names Scott Chacon and others rather than the paper's authors, so record the inherited notice without inventing ownership. Dataset terms require their own provider audit.

| Source at that revision | Direct observation | Implication for admission |
|---|---|---|
| [scripts/training.ipynb](https://github.com/mubashar-iqbal/TWINE/blob/841e1195acf90835c4c427e0fb48d10c08ed30d5/scripts/training.ipynb), zero-based cells 2–10 | Reads `right_arm.csv`, renames columns, expands list-valued fields; includes six scalar features and expanded vector fields. Target is `Anomaly_State`. Uses a stratified random 80/20 split, seed 42, and a 100-tree RF. Reports weighted precision/recall/F1. | This is a supervised classifier; it must not silently be compared with normal-only detectors as if training access were identical. The split does not establish independent production runs or temporal separation. Freeze a common split and label policy before execution. |
| Same notebook, cells 15–16 | Replaces the fitted variable with a 50-tree, depth-10 RF before SHAP analysis, using the same training split. | The explanation model differs from the earlier 100-tree evaluation model. Do not attribute those explanation plots to the first model without reconciliation. |
| [simulation_robotic_arm.ipynb](https://github.com/mubashar-iqbal/TWINE/blob/841e1195acf90835c4c427e0fb48d10c08ed30d5/simulation_robotic_arm.ipynb), cells 13–23 | Reads `./Data/right_arm.csv`; takes every 100th row; keeps five scalar inputs; performs a random 80/20 split. The loop processes five held-out rows, but a later metric cell compares predictions with `y_test[:15]`. | This is a separate demonstration path with different features/subsampling. The 5-versus-15 length mismatch is a static source defect, not an executed failure. |
| [scripts/anomaly_detection.py](https://github.com/mubashar-iqbal/TWINE/blob/841e1195acf90835c4c427e0fb48d10c08ed30d5/scripts/anomaly_detection.py) | `train_model` fits a 100-tree RF, seed 42. `predict_model(..., model)` uses global `rf` rather than its passed `model` argument. | Pin and test the selected path; do not present code visibility as run readiness. |
| [scripts/digital_twin_azure.py](https://github.com/mubashar-iqbal/TWINE/blob/841e1195acf90835c4c427e0fb48d10c08ed30d5/scripts/digital_twin_azure.py) and [schema](https://github.com/mubashar-iqbal/TWINE/blob/841e1195acf90835c4c427e0fb48d10c08ed30d5/model/digital-twin-schema.json) | Azure receives five measured properties plus the predicted anomaly state. Functions fetch/update twin properties and plot state. | The inspected twin is an observational state representation coupled to classifier output. No physics residual/state estimator was found in these files. This is not proof that the complete paper makes no broader claim. |

The README recommends Python 3.7.9 and unpinned dependencies. Azure authentication and an account are part of its complete demonstration. Local RF evaluation could be separated in a future declared adaptation, but that would not reproduce the whole cloud twin. No cloud resource was created or paid service used.

**Decision:** retain as a **conditional shared-corpus learning and implementation candidate**. Exact dataset release/labels, common inputs, chronological or run-independent evaluation, publication-method correspondence and executable compatibility remain to be resolved. The full manuscript remains inaccessible in this screen. Do not describe it as a proven physics-based cyberattack detector.

## Additional direct manufacturing twin leads

### LOTL-Hunter — rich public artifact listing, different corpus

**Carol Lo, Thu Yein Win, Zeinab Rezaeifar, Zaheer Khan and Phil Legg. “LOTL-hunter: Detecting multi-stage living-off-the-land attacks in cyber-physical systems using decision fusion techniques with digital twins.”** Future Generation Computer Systems **180**, 108382. DOI **10.1016/j.future.2026.108382**. [Publisher](https://www.sciencedirect.com/science/article/pii/S0167739X26000166); [UWE institutional record](https://uwe-repository.worktribe.com/output/15595608/lotl-hunter-detecting-multi-stage-living-off-the-land-attacks-in-cyber-physical-systems-using-decision-fusion-techniques-with-digital-twins); [institutional manuscript](https://sure.sunderland.ac.uk/id/eprint/19869/1/1-s2.0-S0167739X26000166-main.pdf).

The manuscript front matter records acceptance **2026-01-16**, online **2026-01-20**, issue **July 2026**; UWE explicitly identifies peer review. The PDF was retrieved and method/limitations sections examined after browser retrieval timed out. It describes a simulated pick-and-place manufacturing process using Siemens NX MCD and PLCSim Advanced, explicitly operating the twin disconnected from a physical counterpart. Its method fuses supervised process LSTM-FCN predictions, OPC UA Isolation Forest output, process alarms and host alerts in one-minute intervals. Its single-process, 2.5-hour scenario and reported 50 minutes of lost process telemetry restrict generalization. Those are the authors' experimental descriptions, not our measurements.

The [author repository](https://github.com/carolsworld/LOTL-Hunter/tree/e8cac191912ec7386364c1644698a0d19f586695) is matched by the paper's data-availability statement. Observed revision **`e8cac191912ec7386364c1644698a0d19f586695`**, timestamp **2026-01-21T09:32:37Z**. GitHub reports no license; no license file appears in its recursive tree. Thus public visibility is established, while software/data reuse terms remain unresolved.

Metadata lists process CSVs, process raw-data ZIP, network feature ZIPs, host features, preprocessing, four notebooks, model files, anomaly logs and result files. **Raw OPC UA/TCP-IP captures are not public in this repository:** [`data/Raw/OTnetwork.txt`](https://github.com/carolsworld/LOTL-Hunter/blob/e8cac191912ec7386364c1644698a0d19f586695/data/Raw/OTnetwork.txt) says to contact the authors because of size. No contact was made.

Selected static code observations:

- [`NX_TSC_sktime_LSTMFCNClassifier_5Features_Final.ipynb`](https://github.com/carolsworld/LOTL-Hunter/blob/e8cac191912ec7386364c1644698a0d19f586695/notebooks/NX_TSC_sktime_LSTMFCNClassifier_5Features_Final.ipynb), cell 37, uses a stratified random 70/30 split with seed 3; cycle/source independence needs audit.
- [`OPCUANetwork_IsolationForest_Final.ipynb`](https://github.com/carolsworld/LOTL-Hunter/blob/e8cac191912ec7386364c1644698a0d19f586695/notebooks/OPCUANetwork_IsolationForest_Final.ipynb), cell 34, fits seven contamination settings, 0.05–0.35. The setting-selection path was not fully audited; it must not be assumed independent of test labels.
- [`standardisation.py`](https://github.com/carolsworld/LOTL-Hunter/blob/e8cac191912ec7386364c1644698a0d19f586695/scripts/Process/standardisation.py) truncates each input to its last 2,000 rows or prepends beginning rows when short, then generates labels from instance number ranges. This is length/schema normalization, not evidence of numerical train-only scaling. Original run chronology and label assignment need reconstruction before reuse.

**Decision:** useful direct cyberattack/twin prior art and a possible separate manufacturing benchmark after permissions/protocol checks. It is **not the same dataset as Kayan/CASPER or FactoryIO_TSC**. Do not force it into a same-dataset trio or treat published component variants as three separate papers. Recreating the testbed entails commercial Windows-oriented software; offline analysis of authorized recordings is a separate feasibility question.

### FactoryIO_TSC — accessible code/data listing, one paper and six classifier implementations

**Carol Lo, Thu Yein Win, Zeinab Rezaeifar, Zaheer Khan and Phil Legg. “Digital Twins of Cyber Physical Systems in Smart Manufacturing for Threat Simulation and Detection with Deep Learning for Time Series Classification.”** ICAC 2024, pp. 1–6. DOI **10.1109/ICAC61394.2024.10718749**. [Institutional record](https://uwe-repository.worktribe.com/output/12042560/digital-twins-of-cyber-physical-systems-in-smart-manufacturing-for-threat-simulation-and-detection-with-deep-learning-for-time-series-classification); [IEEE DOI](https://doi.org/10.1109/ICAC61394.2024.10718749).

The institutional record gives conference **28–30 August 2024**, publication **2024-10-23** and accepted-manuscript status/CC BY. A published IEEE conference paper is established; review-history details were not independently extracted. [Manuscript access](https://uwe-repository.worktribe.com/OutputFile/13319720) returned 403; no full-method reading is claimed.

The [matched author repository](https://github.com/carolsworld/FactoryIO_TSC/tree/419b946c182f21f4be3d53a0b68300f045a92cd9) cites the DOI. Observed revision **`419b946c182f21f4be3d53a0b68300f045a92cd9`**, timestamp **2024-11-12T11:03:47Z**. GitHub metadata gives no license and no license file appears in the tree. README describes a simulated quality-checking conveyor scene, ten scenario labels, OpenPLC, and six sktime classifier notebooks. The listing includes `Raw data.zip`, `factoryiodata.csv`, a scene, collection/filtering scripts and a model ZIP. No listed data or model was downloaded or deserialized. Exact label causation, run-level independence and evaluation protocol remain unaudited. A labelled abnormal motion pattern is not by itself proof of a distinct cyberattack mechanism.

**Decision:** useful manufacturing testbed/method-learning lead. Publicly visible archives do not yet establish unrestricted data reuse. Commercial Factory I/O is needed for scene recreation; availability of existing CSVs is a separate matter. This is **one paper**, not six independent recent baseline papers.

## Other leads screened or excluded

| Lead | Primary evidence and reason for separate treatment |
|---|---|
| **Digital Twin-assisted anomaly detection for industrial scenarios**, Alcaraz and Lopez; International Journal of Critical Infrastructure Protection 47 (2024), 100721; DOI [10.1016/j.ijcip.2024.100721](https://www.sciencedirect.com/science/article/pii/S1874548224000623) | Publisher excerpts describe a manufacturing testbed, discrepancy detection, LOF/OCSVM/mean-shift and APT experiments. Full manuscript, exact online day, versioned common dataset and matched author code were not verified. Relevant direct prior art; not an admitted shared-corpus baseline. |
| **Enhancing Security in Smart Robot Digital Twins Through Intrusion Detection Systems**, Vasilica et al.; Applied Sciences 15(9),4596, **2025-04-22**, DOI [10.3390/app15094596](https://www.mdpi.com/2076-3417/15/9/4596) | Publisher identifies a robot-cell architecture, but numerical detector evaluation uses CICIDS2017, 4SICS2015 and CIC Modbus network datasets. This does not establish robotic process-state evaluation. Matched author code/release identity unverified. Excluded from a Kayan process-telemetry trio. |
| **Digital-Twin-Enabled, Time-Aware Anomaly Detection for Industrial Cyber-Physical Systems**, Mbasso; first published **2025-12-31**, DOI [10.1049/dgt2.70016](https://doi.org/10.1049/dgt2.70016) | Publisher explicitly reports SWaT/HAI and an operator-facing twin. This does not satisfy our manufacturing-specific dataset requirement merely because its introduction mentions factories. |
| **HSU TwinFlow**, OASIcs DX 2026, DOI [10.4230/OASIcs.DX.2026.7](https://drops.dagstuhl.de/entities/document/10.4230/OASIcs.DX.2026.7) | Official proceedings describe synthetic production-system fault detection/diagnosis. Useful future physical-context background, but fault labels cannot silently become cyberattack labels. This screen does not establish three recent cyberattack detectors on it. |
| **LATTICE**, Xu, Ali and Yue; DOI [10.1145/3582571](https://doi.org/10.1145/3582571) | ACM gives publication **2023-07-22**, outside our window. Preprint [2309.15995](https://arxiv.org/abs/2309.15995) is also before the cutoff. Its CPS framing does not create manufacturing-specific cyberattack data. Background only. |
| **Balta et al., DT-based cyberattack detection for CPMS** | The existing [seed register](../LITERATURE_EVIDENCE.md) records initial online publication in February 2023. A 2024 issue date cannot move it into our main window. Retain as important background; no new full audit performed here. |

## Evidence boundaries and reproducibility record

Publication evidence was checked through primary publisher/institutional pages. Public GitHub API metadata and recursive file listings were read without repository execution. Selected code was fetched as text from immutable revision URLs and parsed as JSON where appropriate; code cells were not run. No package installation, cloud setup, author contact or dataset request occurred.

The command environment was `/Users/matrixusman/CUI/DigitalTwin`; Python's standard-library `urllib.request`, `json` and `hashlib` were used for HTTP/metadata/text handling. `pdftotext` extracted a temporary LOTL-Hunter PDF, then the temporary file was removed. Initial sandbox HTTP requests failed DNS; approved network reads then succeeded for GitHub and the Sunderland PDF. TWINE/UWE PDF 403 failures remain explicit. No failed fetch was labelled evidence that an article is false.

Recheck exact public metadata with these **proposed inspection commands**; they are not training commands:

```text
GET https://api.github.com/repos/mubashar-iqbal/TWINE
GET https://api.github.com/repos/mubashar-iqbal/TWINE/git/trees/841e1195acf90835c4c427e0fb48d10c08ed30d5?recursive=1
GET https://api.github.com/repos/carolsworld/LOTL-Hunter/git/trees/e8cac191912ec7386364c1644698a0d19f586695?recursive=1
GET https://api.github.com/repos/carolsworld/FactoryIO_TSC/git/trees/419b946c182f21f4be3d53a0b68300f045a92cd9?recursive=1
```

Selected **locally measured source-byte SHA-256** values from temporary/in-memory retrieval (these are paper/code hashes, **not dataset hashes**):

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| LOTL-Hunter Sunderland PDF | 13,129,128 | `de36e019fabaf3381cd2eb9b79782ea4ec257826f8057ec62b8fb4bc07294b55` |
| TWINE `scripts/training.ipynb` at pinned revision | 25,560 | `3bcaa5264946a6448a129ed952836b7db236cc67a206bdacc7f0db24219379ad` |
| TWINE `simulation_robotic_arm.ipynb` at pinned revision | 14,802 | `3f46dd3916c9acb10cc93509f1abd40dae425e8ad9367878585fd0f1ad2b0edb` |
| TWINE `scripts/anomaly_detection.py` at pinned revision | 1,746 | `42b6b9fe80d20e16814f6f84ad6aa4ba8a2e4e7090db9116d014b31cf5123f27` |
| TWINE `MIT-LICENSE.txt` at pinned revision | 1,072 | `b60c044f81876f350bf5e309071bfc2057c444efd07d2b82790b786049d9d83f` |

## Search record

Queries executed through web search on the audit date included:

```text
"digital twin" "cyber" "manufacturing" dataset detection 2024 2025 2026
"digital twin" "cyberattack" "HAI" manufacturing
"digital twin" "Tennessee Eastman" attack detection 2024 2025
"digital twin" "robot" "cyberattack" dataset 2024 2025
"digital twin" "2024" "Factory I/O" cyber dataset
"digital twin" "manufacturing" "cyber" dataset github 2025
"FactoryIO_TSC" paper
"S0167739X26000166"
"LOTL-Hunter" github
"LOTL-Hunter" dataset
"Digital twin-assisted anomaly detection for industrial scenarios"
"TRIST" "container-based" dataset github
"iRobot security dataset" github
"TWINE" "ISO 23247" dataset
"TWINE" "digital twin" Kayan github
"TWINE: ISO" pdf
"TWINE" "101976" dataset
"TWINE" "anomaly detection" "Iqbal"
"TWINE" "right_arm"
```

Additional broad queries substituted 2024, 2025 and 2026 separately and excluded water/grid/review/survey terms; title-followup searches resolved primary records. These searches are bounded discovery, not proof that no other suitable work exists.

**Next bounded action:** integrate TWINE with the independently screened Kayan-corpus papers, verify that the same authorized corpus and task can support all three, obtain the accessible full manuscript if possible, and map each paper's exact training/label/split assumptions. Until then the proposed trio is a learning set and evidence-backed candidate set, not three execution-ready reproductions.
