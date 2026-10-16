# TWINE: reading notes and connection to author code

Audit date: **16 October 2026**. Project: manufacturing; owner: Haiqa Mushtaq. Scope: source verification and static reading with the installed research skill's bounded source-verification workflow. No training, notebook execution, Azure access, paid service or author contact occurred. These notes do not certify that a researcher has read or understood the paper.

**Reading coverage is partial:** the complete manuscript is still inaccessible. The institutional abstract, bibliographic records, repository README, both complete notebooks, all three Python modules and the twin schema were inspected. Paper section/equation/table correspondence remains unverified. Code facts below describe the collected revision, not necessarily the exact experiment reported in the article.

## 1. Verified identity and available sources

Mubashar Iqbal, Sabah Suhail, Simon Freudenthaler, Muhammad Fahim and Raimundas Matulevičius. *TWINE: ISO 23247-compliant digital twin and explainable AI framework for anomaly detection*. **Internet of Things 38, 101976 (2026)**. DOI: [10.1016/j.iot.2026.101976](https://doi.org/10.1016/j.iot.2026.101976). The [Queen's University Belfast record](https://pure.qub.ac.uk/en/publications/twine-iso-23247-compliant-digital-twin-and-explainable-ai-framewo/) records online publication on 26 May 2026 and the July issue. The [Munster Technological University record](https://pure.mtu.ie/en/publications/twine-iso-23247-compliant-digital-twin-and-explainable-ai-framewo-2/) independently identifies it as a peer-reviewed journal article. It is within our date window; peer review does not establish reproducibility.

The [author repository](https://github.com/mubashar-iqbal/TWINE/tree/841e1195acf90835c4c427e0fb48d10c08ed30d5) explicitly links this DOI. The pinned revision is `841e1195acf90835c4c427e0fb48d10c08ed30d5`; the complete tracked-file snapshot is under [artifacts/source_snapshot](artifacts/source_snapshot/). Its README discloses copying from `h1548782/seleniumforest`, and the collected MIT license covers the repository code. This does not change the original dataset's separate license. Individual artifact hashes and retrieval provenance are in the [source pack manifest](../SOURCE_PACK_MANIFEST.json).

Follow-up checks: all nine collected TWINE file sizes and SHA-256 hashes match that manifest. Notebook JSON and Python syntax were parsed without importing or executing the source. Local links in these notes resolved. These are document/source-integrity checks, not runtime tests.

Public manuscript follow-up in this session:

| Route | Observation | Conclusion |
|---|---|---|
| New MTU institutional record above | Bibliography and abstract available; document access leads to the DOI, with no local manuscript link | Useful primary metadata/abstract; no full text obtained |
| [Tartu InfoSec publication list](https://infosec.cs.ut.ee/Main/Publications) | Current list inspected; no TWINE manuscript link found | No copy located on that inspected page; not proof that Tartu holds none |
| Exact title/DOI and author/PDF searches, including Tartu/ETIS discovery | Returned existing institutional, CHESS, repository and publisher records; no new downloadable author manuscript found | Search failure is an access gap, not evidence of nonexistence |
| [Publisher article](https://www.sciencedirect.com/science/article/pii/S254266052600106X) | Ordinary web fetch returned HTTP 403 | Full publisher text unavailable through this route |

Earlier checks found a QUB accepted-manuscript listing marked CC BY, but both ordinary PDF routes failed. They were not blindly retried here. The [collection audit](../../docs/MANUSCRIPT_COLLECTION_AUDIT.md) preserves those failures. No new PDF was acquired in this follow-up.

## 2. What the available paper description actually supports

The institutional abstract presents an ISO 23247-oriented architecture joining digital-twin services, supervised anomaly detection and SHAP explanations for industrial robotic arms. It claims physical/digital synchronization and reports a proof of concept. The abstract does **not** establish the exact feature set, split, numerical results, timing measurements, physical state estimator or compliance test used. These require the manuscript. Its anomaly examples concern operational deviations; malicious intent is not established by an alarm alone. [Institutional abstract](https://pure.mtu.ie/en/publications/twine-iso-23247-compliant-digital-twin-and-explainable-ai-framewo-2/)

The useful learning question is: **what does putting a detector inside a synchronized digital representation add, and how would we measure that contribution?** The code lets us inspect a possible implementation, but does not answer the full research question by itself.

## 3. Trace the three distinct code paths

All notebook cell numbers below are **zero-based array indices**, counting both code and Markdown cells. They are stable identifiers at the pinned revision; execution counters are not used.

### A. Full controller-feature classification

Source: [scripts/training.ipynb](artifacts/source_snapshot/scripts/training.ipynb).

| Method operation | Exact source anchor | What it does and what remains uncertain |
|---|---|---|
| Load observations | Cell 2 | Reads `/right_arm.csv`; README points to the original CASPER listing. Filename/link alone do not identify the exact bytes used in the paper. |
| Parse vector fields | Cells 3–5 | Renames spaces to underscores, detects lists using the first nonempty value, and expands coordinates using `ast.literal_eval`. Parsing is local to each row; no temporal window is constructed. |
| Select input and target | Cell 6 | Six scalar features plus every expanded vector coordinate; target `Anomaly_State`. Applied to our audited original schema, this means **63 candidate features**: six scalars and 57 vector coordinates. This is a static schema inference, not an executed loader result or a verified paper feature count. `Timestamp`, `Safety_Status` and the target are not selected as inputs. |
| Partition | Cell 8 | `train_test_split(..., test_size=0.20, random_state=42, stratify=y)` shuffles rows. Related timestamps/cycles can enter both partitions. It does not measure held-out future episodes under our intended protocol. |
| Fit detector | Cell 9 | Supervised `RandomForestClassifier`: 100 trees, unlimited depth, minimum split 2, minimum leaf 1, seed 42, all CPU cores. Attack/anomaly labels are used in training. |
| Predict and evaluate | Cells 10–11 | Predicts labels, reports accuracy, **class-support-weighted** precision/recall/F1 and confusion matrix. Weighted F1 is not positive-class anomaly F1. A class report is also printed. |
| Inspect model features | Cells 12–13 | Tree impurity feature importance for that 100-tree classifier. This is a model statistic, not causal evidence about the plant. |
| Replace model for explanation | Cell 15 | Reassigns `rf_model` to **50 trees with maximum depth 10**, fits it again, and constructs `shap.TreeExplainer`. This is a different model from the one evaluated in cell 10. |
| Explain and plot | Cells 16–22 | Samples up to 1,000 test rows with seed 42, handles SHAP output formats, draws SHAP/PDP/ICE plots and a feature table. The plots explain the replacement model unless execution order was altered. No evidence establishes an altered published execution order. |

The six scalar features are `Norm_of_Cartesion_Linear_Momentum`, `Robot_Current`, `Tool_Current`, `Tool_Temperature`, `TCP_Force` and `Execution_Time`. The source spelling `Cartesion` is preserved. Units and semantics should follow the [audited schema](../../docs/CASPER_SENSOR_SCHEMA.md), not guessed column names.

### B. Five-feature Azure demonstration

Source: [simulation_robotic_arm.ipynb](artifacts/source_snapshot/simulation_robotic_arm.ipynb).

Cell 13 loads `./Data/right_arm.csv`. Cell 16 keeps five scalar inputs—the same list above except `Execution_Time`—and the label, then takes every hundredth row. It makes a random 80/20 split with seed 42 **without** stratification and resets indices. These rows are not a chronological stream. Cell 19 calls the 100-tree training helper and sends only the first five rows of this shuffled test set through prediction, twin update and plotting. The name “simulation” here describes a replay demonstration; it does not establish a physical robot dynamics simulator.

| Script/function | Exact location | Connection to the claimed architecture |
|---|---|---|
| `train_model` | [anomaly_detection.py](artifacts/source_snapshot/scripts/anomaly_detection.py), lines 13–35 | Trains a 100-tree, seed-42 RF and prints accuracy/confusion matrix. This is the supervised decision component. |
| `predict_model` | Same file, lines 42–56 | Predicts one current row. It accepts `model` but calls global `rf`; the current helper sequence sets that global, but substituting the argument does not change the model actually used. |
| `connect_azure`, `get_twin_state` | [digital_twin_azure.py](artifacts/source_snapshot/scripts/digital_twin_azure.py), lines 14–27 and 44–47 | Create a cloud client and read stored properties. Credentials and service creation were not attempted. |
| `update_machine` | Same file, lines 54–91 | Writes the five observed feature values and predicted anomaly flag into the twin using JSON patches. No forecast/residual or physical state-estimation equation is present in this function. |
| `plot_twin_state` | Same file, lines 98–161 | Reads stored values and displays a dashboard/alarm. This visualization alone does not show improved detection or a validated synchronization latency. |
| Twin schema | [digital-twin-schema.json](artifacts/source_snapshot/model/digital-twin-schema.json) | Five double-valued properties and one integer anomaly property under a DTDL interface. No process dynamics, topology relations, expected trajectory or physical constraints are specified in this schema. |

The classifier receives dataframe measurements, rather than an independently predicted twin state. The inspected detector does not use a twin residual. A future claim that the twin improves detection needs a component ablation and a documented mechanism; the supplied data flow does not establish that claim.

### C. Explanation helper and demonstration inconsistencies

[predictive_maintenance.py](artifacts/source_snapshot/scripts/predictive_maintenance.py), `explain_prediction` (lines 8–31), trains another 100-tree model, predicts the test set, and explains rows it predicts positive. It does not directly receive the already fitted detector. With identical data, parameters and dependencies its predictions may agree, but that equivalence is not established by passing the detector object. SHAP attributions explain model output under the explainer's assumptions; they do not prove an actual component fault or attack cause.

Additional static findings that must be resolved before any demonstration:

- Simulation cell 19 emits five predictions, while cell 23 compares them with 15 labels. That path has incompatible lengths as written. It was not executed to manufacture an error report.
- Cell 29 calls `pm.create_shap_beeswarm_all`, which is not defined in the collected module. An alarm image referenced by the dashboard is absent from the tracked source pack.
- The schema and demonstration have five inputs; the training notebook has 63 under our schema. A 63-feature trained classifier cannot simply be inserted into the five-feature path.
- The README recommends Python 3.7.9 and gives unpinned dependency installation instructions, not a reproducible environment lock. We have not installed them or tested runtime compatibility.
- No notebook output establishes an independently reproduced score, timing, or learned artifact. The full manuscript is required to determine which of these paths supports each published claim.

## 4. Fair-comparison decision

**Learning candidate: retain. Numerical baseline: hold.** TWINE is relevant for understanding architecture, deployment plumbing and explanations. Its supervised controller-feature access differs from CASPER's normal-only external-IMU detector. Sharing an archive does not make their information access equal.

A future local RF run with common features, chronological episode splits and our metric definitions would be **author-code execution under a modified protocol** if we preserve the method and document patches. Rebuilding a standalone RF with our own design choices would be an **independent implementation**. Neither should be described as a faithful replication of TWINE's entire cloud framework. See [the proposed comparison protocol](../../docs/COMPARISON_PROTOCOL.md).

Before admission, resolve:

1. Full paper access and an explicit mapping from each experiment/table to a code path, revision and configuration.
2. Dataset version/hashes and whether all controller observables were genuinely available and trustworthy under the attack model.
3. Same eligible features and training-label access across comparative methods; chronology/episode splits frozen before windowing or selection.
4. Which fitted model the SHAP figures explain, and whether the explanation quality has a task-relevant evaluation.
5. What synchronized state the twin adds, how it affects the detector, and whether physical fidelity/latency claims have evidence.
6. Compatible dependencies and repaired demo errors, recorded as modifications; no Azure deployment is needed merely to study the RF.

## 5. Reading order and questions for the researcher

Read the institutional abstract first, then README, training cells 2–10, cells 15–22, simulation cells 16/19/23, the three functions that train/predict/update, and the schema. Keep the full-manuscript task open.

Try to explain, in your own words: What is an observation versus a predicted state? Which labels train this detector? Why is a randomly shuffled replay different from testing future operation? Which model produced the accuracy table, and which model is explained? What would have to be removed for a meaningful “without the twin” comparison? What evidence would justify a causal or cybersecurity interpretation of an anomaly?

These questions are learning prompts, not a completed comprehension assessment. Our current evidence supports a precise static-code study and partial paper reading, not a full paper replication or a claim that TWINE is invalid.
