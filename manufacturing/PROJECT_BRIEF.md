# Manufacturing research project — initial scope

Last updated: 16 October 2026. Project owner: **Haiqa Mushtaq**. Ownership is an organizational assignment, not a decision about academic authorship.

This is an independent academic research project on cybersecurity of manufacturing cyber–physical systems. Its current stage is literature, code and open-data feasibility audit, explicitly activated by the user while water awaits access. No baseline has been reproduced, no benchmark dataset has been acquired for this project, and no experimental results exist.

## Provisional direction

Working title: **“Process- and Sequence-Aware Digital Twins for Cyberattack Detection in Manufacturing.”**

Candidate question: Can a digital twin conditioned on production phase, permitted operation sequences, and changeover context distinguish malicious command or sequence deviations from legitimate production changes and ordinary process faults?

This is a hypothesis to investigate, not a novelty claim or finalized architecture. The current recommendation is **industrial robotic arms**, anchored to the original CASPER pick-and-place collection. Its public download route is verified without institutional approval. **CASPER (2024), TWINE (2026), and CatBoost on CASPER (2026)** form a critical-learning set with matched author-code leads; none is admitted for numerical comparison yet. Release ambiguity, unequal input/training access, code-license gaps and evaluation defects remain. See the [selection report](docs/BASELINE_SELECTION_REPORT.md). The final threat model, trusted measurements, twin representation and title remain undecided; available data may not support the original broad changeover question.

The distinction between an attack, a fault, and an authorized transition must come from documented ground truth. “Cyber-physical,” predictive maintenance, or generic ICS branding alone does not establish cybersecurity relevance or manufacturing data. A simulator, a detector dashboard, and a state-coupled digital twin are different artifacts and must be described accurately.

## Scope and decision criteria

- Screen main comparative papers published from **16 October 2023 through 16 October 2026**, preferably 2024–2026. Record online, issue, and preprint dates separately; keep older background separate.
- Select manufacturing-specific data and comparable protocols. SWaT and WADI are not imposed on this project. Do not reuse water findings as manufacturing evidence.
- Require identifiable process semantics, attack labels or documented injection events, normal operation, and timing before claiming process-aware cyberattack detection can be evaluated.
- Establish what the proposed twin knows at each timestamp, how its state is synchronized, and what independent trusted information exists. A predictive model alone is not automatically a validated twin.
- Keep title, mechanism, comparison set, and contribution provisional until a faithful baseline and an explicit literature-gap audit support decisions.

## Setup deliverables and next stage

The [literature register](docs/LITERATURE_EVIDENCE.md) links a bounded primary-source, manuscript and static-code audit. The [access checklist](docs/DATASET_ACCESS_CHECKLIST.md) and [reproduction plan](docs/REPRODUCTION_PLAN.md) identify prerequisites. CASPER is the conditional first method to study/reproduce, with a corrected and disclosed calibration protocol; there is no execution-ready baseline or frozen release.

The user selected manufacturing next while water waits for external access. This audit does not initiate manufacturing implementation, bulk data acquisition, simulator execution, paid services, training, or publication. The smart-grid project remains independently scoped.

## Shared publication and writing preferences

Apply the confirmed [shared publication standards](../docs/PUBLICATION_STANDARDS.md): aim for leading field-appropriate journals through rigorous distinct research, use natural precise academic prose, and develop distinctive titles grounded in the supported contribution. The user also records intended future EB-2 use; individual authorship, impact and publication claims must remain factual. Existing titles stay provisional, and no publication or immigration outcome is assured.
