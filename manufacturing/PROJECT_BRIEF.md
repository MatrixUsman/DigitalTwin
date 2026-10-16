# Manufacturing research project — initial scope

Last updated: 16 October 2026. Project owner: **Haiqa Mushtaq**. Ownership is an organizational assignment, not a decision about academic authorship.

This is an independent academic research project on cybersecurity of manufacturing cyber–physical systems. Its current stage is setup and initial scoping. No baseline has been reproduced, no dataset has been acquired for this project, and no experimental results exist.

## Provisional direction

Working title: **“Process- and Sequence-Aware Digital Twins for Cyberattack Detection in Manufacturing.”**

Candidate question: Can a digital twin conditioned on production phase, permitted operation sequences, and changeover context distinguish malicious command or sequence deviations from legitimate production changes and ordinary process faults?

This is a hypothesis to investigate, not a novelty claim or finalized architecture. The manufacturing process, observability assumptions, threat model, twin representation, and evaluation datasets remain undecided. A production-line or assembly-cell case could make sequence constraints meaningful; an additive-manufacturing case would require a different process model. We will select one coherent setting after evidence and access checks.

The distinction between an attack, a fault, and an authorized transition must come from documented ground truth. “Cyber-physical,” predictive maintenance, or generic ICS branding alone does not establish cybersecurity relevance or manufacturing data. A simulator, a detector dashboard, and a state-coupled digital twin are different artifacts and must be described accurately.

## Scope and decision criteria

- Screen main comparative papers published from **16 October 2023 through 16 October 2026**, preferably 2024–2026. Record online, issue, and preprint dates separately; keep older background separate.
- Select manufacturing-specific data and comparable protocols. SWaT and WADI are not imposed on this project. Do not reuse water findings as manufacturing evidence.
- Require identifiable process semantics, attack labels or documented injection events, normal operation, and timing before claiming process-aware cyberattack detection can be evaluated.
- Establish what the proposed twin knows at each timestamp, how its state is synchronized, and what independent trusted information exists. A predictive model alone is not automatically a validated twin.
- Keep title, mechanism, comparison set, and contribution provisional until a faithful baseline and an explicit literature-gap audit support decisions.

## Setup deliverables and next stage

The [literature register](docs/LITERATURE_EVIDENCE.md) contains a bounded primary-source screen, not a completed systematic review. The [access checklist](docs/DATASET_ACCESS_CHECKLIST.md) and [reproduction plan](docs/REPRODUCTION_PLAN.md) identify prerequisites. No ready common benchmark or first main baseline is established.

The user requested later audits one project at a time: water, then manufacturing, then smart grids. This setup does not initiate manufacturing implementation, data downloads, simulator execution, paid services, training, or publication.
