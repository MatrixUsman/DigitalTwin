# CASPER — learning and conditional reproduction candidate

Paper: [CASPER: Context-Aware IoT Anomaly Detection System for Industrial Robotic Arms](https://doi.org/10.1145/3670414), ACM ToIT, August 2024. [Author-hosted corrected VOR](https://iotgarage.net/publications/pdfs/Kayan2024a.pdf), V1.1 dated 2025-02-05.

Author code: [1D-CNN-Anomaly-Detection-via-CASPER](https://github.com/hkayann/1D-CNN-Anomaly-Detection-via-CASPER/tree/bff03c91d155bf3134f6d801d3a4f4af7ea78adb), revision `bff03c91d155bf3134f6d801d3a4f4af7ea78adb`. README has an MIT badge, but the complete tree has no corresponding license text; code-use terms remain unresolved. The successor TinyML repository is a separate code/data record.

Data: [original CASPER](https://www.kaggle.com/datasets/hkayan/industrial-robotic-arm-anomaly-detection), provider v3, 2023-02-11, CC BY-SA 4.0; archive and five original files now received with [hashes/identity evidence](../../docs/CASPER_DATASET_IDENTITY.md). Published method detects externally sensed robot-motion deviations; it is a non-twin comparator. The corrected VOR PDF and selected author notebook are now stored in ignored `artifacts/`; see the [collection audit](../../docs/MANUSCRIPT_COLLECTION_AUDIT.md).

Before execution: resolve code-use terms, full clock/label alignment, corrected-IMU provenance, partition/window isolation and threshold calibration. Inspected notebook selects best F1 using anomaly labels; this cannot be our held-out protocol. Any correction must be disclosed.

[Detailed code/manuscript audit](../../docs/literature/COMPARATOR_SCREEN_2026-10-16.md) · [selection decision](../../docs/BASELINE_SELECTION_REPORT.md). No code checkout, model execution or benchmark result in this folder.

Current reading pack: [pinned source and author artifacts](../SOURCE_PACK_MANIFEST.json), [code study](../../docs/BASELINE_CODE_STUDY.md), and [annotation lineage](../../docs/CASPER_ANNOTATION_LINEAGE.md). These collected source snapshots are not an executed reproduction. Figure 11's four-convolution architecture matches the code; its label-class totals match our static index arithmetic. Table 11's 750-row discrepancy remains unresolved.
