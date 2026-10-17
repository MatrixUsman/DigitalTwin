# Manufacturing baseline admission rules

Established 16 October 2026 for Haiqa Mushtaq's independent manufacturing project. Apply the shared research/publication rules and [current selection report](BASELINE_SELECTION_REPORT.md). Three papers is the initial study target; it is not permission to relax scientific requirements or a complete eventual comparison set.

| Requirement | Admission evidence |
|---|---|
| Recent | First journal/proceedings publication in 2023-10-16–2026-10-16; prefer 2024–2026. Record earlier preprints, corrections and issue dates separately. |
| Manufacturing | Actual robot, production/assembly process or chemical manufacturing. Water-treatment data and generic IoT/network corpora do not become manufacturing because a paper says “Industry 4.0.” |
| Accessible now | Provider/author provenance, explicit data terms, identifiable version/files and a working public retrieval route. Distinguish catalogue visibility, successful response headers, downloaded bytes and validated data. |
| Same data | Three papers must demonstrably evaluate the same identifiable collection if we claim a published shared-data trio. Similar names, the same simulator or a method we could port are insufficient. Freeze exact received files for future reruns. |
| Same scientific task | Identify anomaly detection versus supervised classification, physical faults versus malicious interventions, and available training labels. Keep unequal supervision in separate comparison tracks. |
| Same observable information | Audit IMU, controller telemetry, commands, timestamps and labels. Same collection with different sensors/trust assumptions is not an equal-information comparison. Explain any feature adaptation as a modified method. |
| Useful role | Prefer a strong learned detector, a direct twin comparator and another complementary control. Do not require all controls to be twins, or count several algorithms from one article as several papers. |
| Reproducible | Matched manuscript and author code; revision, license, dependencies, preprocessing, score alignment and configuration identified. Otherwise label an independent reimplementation and its unresolved assumptions. |
| Clean evaluation | Split by time and independent run/cycle before windows; train-only fitting; no held-out attack labels in thresholds, tuning, checkpoint selection or variant selection. Disclose upstream deviations. |
| Defensible metrics | Unadjusted metrics and explicit coverage; event/delay only with reliable boundaries; false alarms on independent normal operation. Never rank copied headline scores from incompatible protocols. |
| Feasible | Bounded local pilot plan after audit; no assumed CUDA, hardware robot, commercial simulator or cloud account. Paid services and lengthy runs need approval. |
| Genuine twin contribution | Identify represented process state, model, synchronization, prediction and trusted observations. An Azure object or classifier is not evidence of a validated physical model or a useful twin contribution. |

Use **learning candidate**, **conditional comparative candidate**, **hold**, **background**, and **execution-ready** explicitly. A missing full manuscript, dataset citation or license is an unresolved fact, not proof of fabrication. No candidate is execution-ready at this stage.

## Recorded transfer-track decision — 17 October 2026

The [admission decision](COMPARATOR_ADMISSION.md) selects a comparison design that includes an explicitly transferred general time-series detector (ModernTCN), alongside ordinary motion controls and matched mechanism variants. This is a disclosed extension of the search scope, **not satisfaction of the published common-dataset-trio criterion**. Every eventual local rerun must still use identical admitted CASPER bytes and information access. Keep paper/role selection, numerical specification, software validation and execution readiness separate. The original three papers have Group D dispositions; no recent-paper implementation is yet execution-ready. The implemented velocity control is an independent ordinary control, not a recent paper.
