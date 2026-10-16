# CASPER — learning and conditional reproduction candidate

Paper: [CASPER: Context-Aware IoT Anomaly Detection System for Industrial Robotic Arms](https://doi.org/10.1145/3670414), ACM ToIT, August 2024. [Author-hosted corrected VOR](https://iotgarage.net/publications/pdfs/Kayan2024a.pdf), V1.1 dated 2025-02-05.

Author code: [1D-CNN-Anomaly-Detection-via-CASPER](https://github.com/hkayann/1D-CNN-Anomaly-Detection-via-CASPER/tree/bff03c91d155bf3134f6d801d3a4f4af7ea78adb), revision `bff03c91d155bf3134f6d801d3a4f4af7ea78adb`. No license identified in inspected tree. The successor TinyML repository is a separate code/data record.

Data: [original CASPER](https://www.kaggle.com/datasets/hkayan/industrial-robotic-arm-anomaly-detection), provider v3, 2023-02-11, CC BY-SA 4.0; local bytes/hashes pending. Published method detects externally sensed robot-motion deviations; it is a non-twin comparator.

Before execution: resolve code-use terms, full clock/label alignment, corrected-IMU provenance, partition/window isolation and threshold calibration. Inspected notebook selects best F1 using anomaly labels; this cannot be our held-out protocol. Any correction must be disclosed.

[Detailed code/manuscript audit](../../docs/literature/COMPARATOR_SCREEN_2026-10-16.md) · [selection decision](../../docs/BASELINE_SELECTION_REPORT.md). No code checkout, model execution or benchmark result in this folder.
