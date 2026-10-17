# CASPER: comparator admission audit

Audit date: **17 October 2026, Asia/Karachi**. Manufacturing / Haiqa Mushtaq. Bounded AI-assisted manuscript, metadata and static-code verification; no raw observations or upstream programs were opened/executed in this audit. This updates the decision, not the historical collection record or frozen Group D protocol.

**Decision:** the original external-IMU experiment belongs in a **separate comparison track, currently on hold**. A controller-input CNN can be specified as an **independent, CASPER-inspired reimplementation with disclosed modifications**. It would not be a faithful reproduction, and the original notebook is not admitted for copying/execution while its reuse terms remain unresolved.

## Publication and source identity

Hakan Kayan, Ryan Heartfield, Omer Rana, Pete Burnap and Charith Perera, *CASPER: Context-Aware IoT Anomaly Detection System for Industrial Robotic Arms*, ACM Transactions on Internet of Things 5(3), article 18. DOI [10.1145/3670414](https://doi.org/10.1145/3670414). The corrected [author-hosted VOR](https://ngcharithperera.gitlab.io/publications/pdfs/Kayan2024a.pdf) is 36 pages; its first page identifies V1.1, **5 February 2025**. The journal article is within our recent-paper window; the correction is not a new baseline publication.

The fresh [Crossref deposit](https://api.crossref.org/works/10.1145/3670414) records August 2024 for online publication and 31 August for print. Its DOI creation date, 1 June 2024, is **not** treated as a verified first-online date. The [Cardiff ORCA record](https://orca.cardiff.ac.uk/id/eprint/165098/) corroborates journal/author identity and acceptance on 13 May 2024, and supplies an accepted manuscript. The publisher landing page returned HTTP 403 in this audit. The available corrected VOR supports full-text study; the exact correction scope remains unresolved.

| Artifact | Verified identity |
|---|---|
| Existing corrected VOR | [Local PDF](../../baselines/casper/artifacts/casper_corrected_vor_v1.1.pdf); SHA-256 `323efce849d75e16833f166983a7387b6d8f86760ce889fe4918ff2f775be186`; hash rechecked |
| Original author repository | [hkayann/1D-CNN-Anomaly-Detection-via-CASPER](https://github.com/hkayann/1D-CNN-Anomaly-Detection-via-CASPER/tree/bff03c91d155bf3134f6d801d3a4f4af7ea78adb); current head rechecked as `bff03c91d155bf3134f6d801d3a4f4af7ea78adb` (commit 2 February 2025) |
| Original notebook | [Pinned snapshot](../../baselines/casper/artifacts/source_snapshot/notebooks/casper.ipynb); SHA-256 `3f1beff113c904473cb554aa79edde7af31d777c4731eb93ba900e3aa4a5fea0` |
| Code-use evidence | Complete untruncated current tree has no LICENSE; GitHub metadata license is null and `/license` returns 404. README displays an MIT badge, but no complete grant was found. Reuse permission remains unverified |
| Later TinyML repository | [Pinned successor](https://github.com/hkayann/Real-time-Anomaly-Detection-in-Industrial-Robotic-Arms-via-TinyML/tree/41b907749b7e5882319690a627a251e93fa99982), full MIT LICENSE verified. This is a different repository/collection/workflow; its license and models do not establish permission or run correspondence for the original notebook |

Fresh public HTTP metadata, complete trees, README/license bytes and retrieval statuses are retained in ignored [CASPER audit receipts](../../local/comparator_admission_20261017/casper/). No access control was bypassed and no author was contacted. Public visibility or a badge alone is not recorded as resolved software permission.

## Claims connected to the inspected implementation

Cell numbers below are **zero-based JSON cell positions** in the pinned notebook. Detailed full-paper context and figure discrepancies remain in the [reading notes](../../baselines/casper/READING_NOTES.md) and [original paper-to-code study](../PAPER_CODE_TRACEABILITY.md).

| Question | Manuscript/code evidence | Admission consequence |
|---|---|---|
| Release and observations | Paper describes the original UR3e pick-and-place collection. Cells 1–2 load `nicla.csv`, skip six lines and use nine acceleration/gyroscope/magnetometer dimensions. The external IMU lacks aligned timestamps and is described as about 18–22 Hz. | This is not our twelve controller q/qdot channels with controller relative time. Exact published-run bytes are not identified by a filename. Our original v3 receipt does not establish their input hash. |
| Labels and counts | Notebook manually aligns/assigns intervention intervals. The earlier full audit found a 750-row discrepancy between a Table 11 IMU total and the inspected inputs. | Do not transfer IMU annotation or counts to the right-arm schedule labels. Exact experiment/run mapping remains unresolved. |
| Preprocessing | Cell 21 applies a trailing median over 20 samples. Cell 82 separates a normal prefix 60/20/20, fits the scaler on its training partition and constructs 755-observation next-step histories. | Normal-only forecasting is scientifically relevant. Our split-first/gap-reset rules must nevertheless replace any preprocessing history crossing a partition boundary. |
| Architecture/configuration | Cell 82 and paper Figure 11(a): four Conv1D layers, 32 filters, kernel 5, ReLU; two max-pool layers (pool 3), flatten and dense nine-output prediction. Adjacent training helper specifies Adamax/MSE, maximum 100 epochs, batch 1,024 and early-stopping patience 5. | Sufficient architectural detail for a clearly independent predictor design, but not a uniquely identified published checkpoint/environment. A twelve-output controller implementation changes the inputs and target. |
| Trained versus evaluated model | Cell 85 loads `../models/1DCNN.keras` after fitting. The fresh complete original repository tree contains no such checkpoint. | The saved training history does not prove which weights produced subsequent results. No checkpoint was deserialized here. |
| Score and support | Cells 89/92 inverse-transform predictions, calculate nine-channel RMSE and sum 755 residuals. Cell 95 majority-labels aggregation windows. Combined median/history/aggregation support spans 1,529 raw observations in the prior lineage audit. | Original-unit IMU residuals and majority-window labels differ from our common endpoint labels and controller units. Any normalization/aggregation change must be named. |
| Threshold selection | Cell 97 searches 1,000 thresholds over evaluated mixed-run scores and retains best F1 against those anomaly labels. | **Not permitted in our held-out evaluation.** Frozen normal-only calibration is a deliberate protocol modification; no upstream oracle-selected result enters our ranking. |
| Resource/result provenance | Stored notebook outputs and paper measurements are author-reported; cell 88's timing denominator uses `num_batches × batch_size`. Environment/run/checkpoint identity and last-batch accounting are not established. | Do not import these as our runtime or detection measurements. Local software/pilot results are a separate ordinary control. |

The audit finds identified compatibility/provenance gaps, not evidence that the article is fabricated. A peer-reviewed source is still subject to method and run verification.

## Final designation

1. **Faithful reproduction: not established.** Original release/hash, manual label alignment, evaluated checkpoint, dependency versions, code-use grant and reported-run mapping remain unresolved. The upstream best-test-F1 procedure cannot become our main evaluation even if those gaps close.
2. **Group A external-IMU comparison: separate track, held.** It requires its own exact annotation, time/support and normal-only calibration plan. It is not authorized by Group D's pilot.
3. **Group D controller-input CNN: independent reimplementation candidate.** Use published algorithmic description, independently written code, the fixed q/qdot information budget and unchanged chronological/calibration/evaluation contract. Document changes to dimensions, scaling, gaps and endpoint scoring. Do not copy the unlicensed notebook or claim the original CASPER result was reproduced. A complete numerical configuration, synthetic isolation/alignment tests, environment compatibility and a new bounded resource plan are still required before fitting.
4. **TinyML successor: related-data reserve.** Its explicit MIT grant is useful evidence for that project only. Its later observations and reported threshold choices require the separate [replacement-method audit](REPLACEMENT_COMPARATORS_2026-10-17.md); they do not retroactively settle the original paper.

The current admission decision is complete; reconstructing the original published experiment is not. See the [central decision](../COMPARATOR_ADMISSION.md) for the proposed fair comparison set and outstanding execution gates.
