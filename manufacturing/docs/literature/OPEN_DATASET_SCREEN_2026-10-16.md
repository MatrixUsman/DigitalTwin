# Open manufacturing dataset feasibility screen

Audit date: **16 October 2026 (Asia/Karachi)**. Project: manufacturing; owner: Haiqa Mushtaq. This is a bounded primary-source and access audit using the installed academic research skill. It is not dataset acquisition, loader validation, a systematic review, or an experiment. No benchmark archive or CSV body was read or saved. Small provider documentation, the MIT data dictionary, and public API metadata were read in memory. Download checks opened HTTP responses and closed them without reading their bodies.

## Decision

There are usable public routes outside SWaT/WADI. **The original CASPER pick-and-place collection is the most useful immediate anchor for the independently emerging robotics paper shortlist.** Its public release and download route are verified below, and TWINE's author code explicitly identifies it. The three-paper intersection still requires the separate manuscript audit; matching a data family is not sufficient.

**MIT's Manufacturing Operations synthetic data is the clearest alternative for separate malicious and non-malicious anomalies.** Its two stages are machining and assembly, its license is explicit, and an archive endpoint answered without an account. However, three recent papers using this exact collection have **not** been established. It is a promising alternative dataset anchor, not yet a confirmed common benchmark for three published methods.

**CMU's Tennessee Eastman manipulation collection is the strongest alternative for documented cyberattack telemetry and existing author tooling.** It represents simulated chemical manufacturing. It must not be confused with the common Tennessee Eastman *fault* dataset. **CASPER** offers real robotic-arm sensing and public author data but combines malicious-motion experiments with non-cyber physical disturbances. **ICS-Flow** has process logs and attacks, but its bottle-filling process still includes water tanks and valves, so it is less distinct from the user's water project than the other choices.

Rankings below concern data feasibility and fit. They do not establish a three-paper intersection or that any associated method is a digital twin.

| Priority | Candidate and release | Public access evidence | Scientific fit and principal qualification |
|---|---|---|---|
| 1: paper shortlist | Original CASPER pick-and-place, author Kaggle version 3, 2023-02-11 | Public metadata lists CC BY-SA 4.0; full archive response 200 without login | Real robot, matched original multimodal file inventory, high/low velocity anomalies. Need exact cyber threat interpretation and common inputs across papers |
| 2: alternative | MIT Manufacturing Operations, version 1, publication date 2025-09-30; DOI `10.5281/zenodo.17238360` | Zenodo metadata and documentation; CC BY 4.0; maker archive HEAD returned 200 | Synthetic machining + assembly, malicious and benign anomalies; compelling sector separation. Recent-method adoption and simulator availability unresolved |
| 3: alternative | CMU TEP manipulations, version 1; DOI `10.1184/R1/23805552.v1` | Figshare public metadata, CC BY 4.0, unauthenticated archive GET headers returned 200 | Chemical-process attack responses with component labels; normal training file separately identified in author code. Not a discrete assembly line |
| Secondary robotics | CASPER 1 & 2 author Kaggle collection, version 2, 2024-09-01 | Public metadata lists MIT license; archive and individual-file download responses returned 200 without login | Distinct listing combines original files with physical-disturbance material; do not substitute it silently for the original |
| Lower priority | ICS-Flow author Kaggle release, version 2, 2023-07-19 | Public metadata lists CC BY-NC-SA 4.0; archive and PLC-log download responses returned 200 without login | Simulated bottling line, network/process logs, explicit attacks; water-adjacent process and short collection |

## 1. MIT Manufacturing Operations synthetic collection

Primary sources: [Zenodo record](https://zenodo.org/records/17238360), [metadata API](https://zenodo.org/api/records/17238360), [README](https://zenodo.org/api/records/17238360/files/README.md/content), [distribution statement](https://zenodo.org/api/records/17238360/files/distribution_statement.txt/content), [column dictionary](https://zenodo.org/api/records/17238360/files/column_categories.xlsx/content).

The provider identifies MIT Lincoln Laboratory as creator. The maker stage machines a cube with holes; the assembler stage attaches a plate. The nominal training directory contains non-malicious anomalies. Attack directories contain both benign and malicious anomalies. Provider documentation describes Parquet data, summary PDFs/PNGs and generation configurations in YAML. The release page was created 2025-10-02 despite the stated publication date 2025-09-30; retain both fields.

| Provider file | Advertised bytes | Provider MD5; **not locally measured raw-data hashes** |
|---|---:|---|
| `maker.zip` | 2,853,182,971 | `c8d0a32bc03366130f6344e3a11f40fb` |
| `assembler.zip` | 15,140,412,420 | `f82eb1cd6cf650c6f4c8d2ebee0ee6d7` |
| `column_categories.xlsx` | 22,497 | `fab29f0f99837177156928c8cb8aaf3d` |
| `README.md` | 1,511 | `6715c076e517704292a52b1552cf46e3` |
| `distribution_statement.txt` | 872 | `f1952d8b3e07561140ada2b28f7f1b97` |

The metadata and README explicitly identify **CC BY 4.0**. The distribution statement records public release and retains copyright/government-rights text; public access does not mean absence of attribution requirements. HEAD on `https://zenodo.org/api/records/17238360/files/maker.zip/content` returned 200 and the expected byte length, without authentication. The assembler archive was listed, not separately opened.

The small dictionary was inspected as XLSX XML in memory. Its Maker sheet identifies `maker_start_ts`, `maker_end_ts`; Assembler identifies `assembler_start`, `assembler_end`. Label columns distinguish `attack_occurred` from `in_attack_period`, and include equipment failure/compromise indicators. **`y_label` combines degradation failures and malicious attacks. It is not a cyberattack-only target.** Debugging columns are separately identified; the README explicitly excludes them from model inputs. Color-based per-column eligibility was not fully visually audited.

Before admission: confirm timestamp units, production-cycle identity, chronology, allowed feature availability at decision time, label vocabulary, exact attack mechanisms and independent scenarios/seeds. End-of-cycle quality information could be unavailable for an earlier alarm. Full generation configurations and a simulator were not inspected. The documentation supports a synthetic manufacturing experiment; it does not establish a synchronized physical digital twin.

## 2. CMU Tennessee Eastman manipulation collection

Primary sources: [versioned record](https://doi.org/10.1184/R1/23805552.v1), [metadata API](https://api.figshare.com/v2/articles/23805552), [README](https://ndownloader.figshare.com/files/42151236), [author simulator](https://github.com/pwwl/tep-attack-simulator), [normal training file metadata in author tree](https://api.github.com/repos/pwwl/ics-anomaly-attribution/git/trees/91e6947b69a60b3d4c68923f26619e536e25d49b?recursive=1).

The record documents **286 manipulations** varying component, pattern and magnitude. Its README specifies 41 sensor and 12 actuator variables, an attack-label column with 1 during manipulation and 0 otherwise, and 96,001 timesteps per trace. These are provider descriptions, not counts measured here. File names encode pattern, magnitude and component. The normal file `data/TEP/TEP_train.csv` is listed separately in the author repository at **83,244,584 bytes**.

| Artifact | Advertised bytes | Provider digest |
|---|---:|---|
| `tep-manipulations.tar.gz`, file ID 42047130 | 7,052,483,136 | MD5 `1d4cd965ab46b4dfd495d1e20d9e4810` |
| `README.txt`, file ID 42151236 | 6,264 | MD5 `2217c8949f9b201315fcc0657d5c9a6a` |

Metadata: public, not confidential, not embargoed, downloads enabled, **CC BY 4.0**. `timeline.firstOnline` is 2023-08-29, the custom Date field is 2023-08-30, and API created/posted fields are 2026-03-19. Treat these as different provenance fields; the latter does not make this a newly collected 2026 dataset. The README gives approximate generation date 2022-04-01.

Archive HEAD returned 403, but a subsequent unauthenticated **GET opened only to response headers** returned 200, gzip type and the expected size. No archive body was consumed. Thus a working public route was observed, not a completed download.

Simulator revision resolved to `2bbead7ffcaa844bae2c7743c231e9c8f80b27c1`; BSD-3-Clause shown by GitHub. [Formatting script](https://github.com/pwwl/tep-attack-simulator/blob/2bbead7ffcaa844bae2c7743c231e9c8f80b27c1/process_matlab_TEP.py) assigns attack labels to rows `[5*2000:7*2000]`, names 53 variables and excludes enumerated failed manipulations. It is code evidence about generation, not an audit of all released traces. The README reports MATLAB R2021a/Simulink for generation; reading pre-generated CSVs does not inherently require MATLAB.

Before admission: verify the normal file's applicable data terms separately from the manipulation record, reconcile included/failed scenarios, inspect whether timestamps were discarded, and preserve independent simulation/run boundaries. Do not use attack periods as normal calibration. A common plant name does not make this identical to Rieth's fault corpus or other authors' attack simulations.

## 3. CASPER industrial robotic-arm data: two distinct listings

### Original pick-and-place collection: priority for matching papers

Primary sources: [author dataset](https://www.kaggle.com/datasets/hkayan/industrial-robotic-arm-anomaly-detection), [metadata](https://www.kaggle.com/api/v1/datasets/view/hkayan/industrial-robotic-arm-anomaly-detection), [file list](https://www.kaggle.com/api/v1/datasets/list/hkayan/industrial-robotic-arm-anomaly-detection), [TWINE author repository naming this dataset](https://github.com/mubashar-iqbal/TWINE).

The provider identifies **version 3**, 2023-02-11, **CC BY-SA 4.0**, and **7,899,312,074 bytes**. All three listed version timestamps fall on 2023-02-11. Dataset age is not the baseline-paper age restriction. The original descriptor specifies normal joint velocity 1.05 rad/s and anomalous periods with higher or lower velocity. A velocity change is observable; malicious intent still requires the experiment's attack scenario, not an assumption that every changed speed is hostile.

| Original release path | Advertised bytes |
|---|---:|
| `dataset/arms.pcap` | 3,703,911,932 |
| `dataset/left_arm.csv` | 1,965,113,819 |
| `dataset/nicla.csv` | 138,908,648 |
| `dataset/right_arm.csv` | 1,978,193,094 |
| `nicla_fixed.csv` | 113,184,581 |

Unauthenticated GET of `https://www.kaggle.com/api/v1/datasets/download/hkayan/industrial-robotic-arm-anomaly-detection` returned 200, ZIP type, **2,824,019,108 bytes**, on the provider's storage host. No response body was read. A single-file request using `right_arm.csv` without its `dataset/` prefix returned 404; it does not negate the verified archive route.

The newer listing below advertises the same sizes for `nicla.csv` and `right_arm.csv`. **Equal sizes are not byte identity.** Its MIT metadata is also different from the original CC BY-SA metadata; use the original collection's documented terms for original-file acquisition, and preserve both records. The reason and exact transformation behind `nicla_fixed.csv` are unverified; do not replace the original with the corrected file silently. Confirm the paper/code expectation, sensor synchronization, and label corrections before freezing releases.

### Newer CASPER 1 & 2 collection: separate release and experiment scope

Primary sources: [author Kaggle record](https://www.kaggle.com/datasets/hkayan/industrial-robotic-arm-imu-data-casper-1-and-2), [metadata](https://www.kaggle.com/api/v1/datasets/view/hkayan/industrial-robotic-arm-imu-data-casper-1-and-2), [file list](https://www.kaggle.com/api/v1/datasets/list/hkayan/industrial-robotic-arm-imu-data-casper-1-and-2), [author code](https://github.com/hkayann/Real-time-Anomaly-Detection-in-Industrial-Robotic-Arms-via-TinyML), [2024 manuscript](https://iotgarage.net/publications/pdfs/Kayan2024a.pdf).

Kaggle identifies Hakan Kayan, version 2 dated 2024-09-01, **MIT** license, and 3,065,646,348 total uncompressed bytes across 14 CSVs. The current author code links this upload directly. Its earlier CASPER repository explicitly redirects to that code. Revision resolved to `41b907749b7e5882319690a627a251e93fa99982`.

The file list includes `nicla.csv` (138,908,648 bytes), `right_arm.csv` (1,978,193,094), multiple frequency/representation variants, and five disturbance files. The author description concerns UR3e screwdriving, painting and pick-and-place; disturbances include impact, weight, magnetic interference and simulated earthquake. These are not all cyberattack labels. The 2024 manuscript separately describes controller-driven joint-velocity changes and notes label synchronization challenges between arm and external sensor. Its table lists two arm files plus network capture, whereas this newer Kaggle list has one arm CSV and no PCAP. The original release above contains those missing modalities. **Do not claim the newer upload is the entire 2024 paper collection.**

Unauthenticated latest-archive GET headers: 200, ZIP, **958,911,130 bytes**. Individual `nicla.csv` download endpoint: 200, ZIP, **33,828,419 bytes**. Bodies were not read. Explicit version-number API variants tried earlier returned 404; the tested latest route must be resolved and frozen again at acquisition.

Before admission: map each experiment to exact files and labels; inspect cycle/task IDs, frequency changes and temporal alignment; separate anomaly type from malicious intent. Full code/license-file consistency and three recent methods using the identical collection remain unresolved. The 2023 PerCom artifact falls before the main baseline window and cannot silently fill a third recent slot.

## 4. ICS-Flow: accessible, but water-adjacent

Primary sources: [author dataset](https://www.kaggle.com/datasets/alirezadehlaghi/icssim), [metadata](https://www.kaggle.com/api/v1/datasets/view/alirezadehlaghi/icssim), [file listing](https://www.kaggle.com/api/v1/datasets/list/alirezadehlaghi/icssim), [dataset manuscript](https://arxiv.org/pdf/2305.09678), [ICSSIM](https://github.com/AlirezaDehlaghi/ICSSIM), [flow generator](https://github.com/AlirezaDehlaghi/ICSFlow).

The manuscript's Section III describes two PLCs controlling a conveyor and water-bottle filling. Section IV describes three hours, initially one attack-free hour followed by intermittent attacks. Attack logs carry Unix start/end times. IT and NST labeling answer different network questions; neither should automatically become a physical-impact label.

Author Kaggle version 2 is dated 2023-07-19, with **CC BY-NC-SA 4.0** and six files:

| File | Advertised bytes |
|---|---:|
| `Dataset.csv` | 21,747,277 |
| `attacker_machine_summary.csv` | 10,326 |
| `attacker_summary.csv` | 80 |
| `snapshots_PLC1.csv` | 4,424,830 |
| `snapshots_PLC2.csv` | 3,626,077 |
| `traffic.pcap` | 1,971,608,339 |

The unauthenticated latest archive responded 200, ZIP, **465,018,506 bytes**; the PLC1-only response was a **602,428-byte ZIP**. No body was read. Code revisions resolved to ICSSIM `bcfd1844d3f063850c69f2643f6a052bac03d8ec` and ICSFlow `449ffa56f71fa8a329e870da5d858325a821a8b3`; the flow generator is MIT-licensed, which does not replace the dataset's non-commercial/share-alike terms.

Before admission: inspect process-log synchronization and permitted inputs, verify versions and both label conventions, and retain recovery intervals and episode boundaries. Network-only methods and process-aware methods have different information access. This dataset is an alternative to SWaT, but not a clean break from water-handling processes.

## Additional leads and exclusions

| Lead | Primary evidence | Decision |
|---|---|---|
| TU Wien smart-factory malware traffic | [Version 1.0.1, 2025-03-19](https://researchdata.tuwien.ac.at/records/ghdc6-45k78), DOI `10.48436/ghdc6-45k78`; CC BY 4.0 plus citation requirement; 136.6 GiB listed files, 173 GB PCAP described; benign training and attack recordings | Genuine factory and public listing, but network/flow corpus; physical state correspondence is not established. No download-response check. Do not use as sufficient evidence for a process twin |
| RoHuCAD 1.0, 2024-11-26 | [Provider](https://zenodo.org/records/14142968), [API](https://zenodo.org/api/records/14142968); CC BY 4.0, two roughly 4.5/4.8 GB ROS bags; human gestures, unsafe behavior, normal assembly annotations | Genuine manufacturing collaboration; no cyberattack ground truth established. Exclude from main cyberattack benchmark |
| HAI | [Provider repository](https://github.com/icsdataset/hai) describes thermal-power/pumped-storage emulation combining boiler, turbine and water process | Open industrial data, but not evidence for a discrete manufacturing sector. Keep for a separately scoped energy decision, without modifying the grid project |
| Generic Tennessee Eastman fault corpus | [Harvard Dataverse identifier](https://doi.org/10.7910/DVN/6C3JR1) and [attack-simulator authors' distinct source](https://github.com/pwwl/tep-attack-simulator) | Common TEP fault data is not the CMU cyber-manipulation collection. Do not count fault diagnosis as attack detection merely because TEP is named |
| Factory I/O MODBUS collection | [Brno provider record](https://www.fit.vut.cz/research/result/c177152/.cs) links IEEE DataPort and notes licensing | Scenario/simulator lead; full public access, exact terms and attack releases unverified in this screen |

## Access checks and reproducibility limits

Working directory for commands: `/Users/matrixusman/CUI/DigitalTwin`. Standard-library Python `urllib.request`, `json`, `zipfile` and XML parsing were used for metadata and dictionary reads. Sandboxed network requests initially failed DNS; the same bounded reads succeeded through approved network execution. Web rendering failed for some Zenodo/CMU endpoints and IEEE DataPort was blocked by robots; successful provider APIs resolved some, not every, gap.

For each Kaggle slug, the executed pattern was:

```python
# Public metadata GETs; no credentials.
urllib.request.urlopen("https://www.kaggle.com/api/v1/datasets/view/" + slug)
urllib.request.urlopen("https://www.kaggle.com/api/v1/datasets/list/" + slug)
# Open latest file response, inspect headers, immediately close: no read().
req = urllib.request.Request(
    "https://www.kaggle.com/api/v1/datasets/download/" + slug,
    method="GET", headers={"User-Agent": "Kaggle/1.7.4"})
with urllib.request.urlopen(req, timeout=15) as response:
    status = response.status
    content_type = response.headers.get("Content-Type")
    content_length = response.headers.get("Content-Length")
```

No signed redirect URLs, credentials, dataset contents or measured dataset SHA-256 values were saved. File sizes and MD5 values above are provider metadata, not acquisition manifests. A response success demonstrates a working public endpoint at this check, not archive integrity, reproducible parsing or experimental quality. Dataset licenses must be retained with the chosen bytes at acquisition.

Searches included `manufacturing cybersecurity dataset Factory I/O process data attacks Zenodo`, `Festo manufacturing cyber attack dataset open process telemetry`, `ICS-Flow dataset GitHub Zenodo manufacturing`, `Tennessee Eastman cyberattack dataset GitHub`, `CASPER Kayan dataset github`, and exact-title/provider follow-ups. Broader searches returned unrelated robot/fault/network material; no claim of exhaustive coverage is made.

## Next bounded decision

Cross this dataset screen with the independent recent-paper audit. Select one coherent task and verify that three methods can use the same authorized release and information set. If three papers have not already evaluated an exact release, state that plainly: porting eligible methods onto a new common collection is a **new evaluation**, not a faithful reproduction of their published dataset results. The user should not be told that three matched baselines exist until this intersection is demonstrated.

For the current robotics paper shortlist, prioritize the **original CASPER pick-and-place version 3**, including its exact modality and label choices. MIT machining/assembly is a distinctly manufacturing alternative with explicit malicious-versus-benign labels; CMU TEP is an alternative for documented chemical-process manipulations. None needs an iTrust institutional request based on the successful public routes above. Acquisition, archive validation, feature/label profiling and model execution remain unperformed.
