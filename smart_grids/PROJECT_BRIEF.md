# Smart-grid research project brief

Updated: **2026-10-16**. Stage: **setup and preliminary scoping only**.

Project owner: **Muhammad Usman Sanghla**. Ownership records responsibility for this workspace; it does not establish paper authorship or author order.

## Provisional direction

**Working title:** Topology and State Consistency for Digital-Twin Cyberattack Detection in Smart Grids.

**Candidate question:** Under explicitly stated observability and trusted-input assumptions, can a digital twin use consistency between electrical measurements and network topology to distinguish malicious measurement or breaker-status changes from legitimate switching and load changes?

The title, mechanism, scope, and novelty remain undecided. This is an independent power-system project, not a renamed water-system adaptation gate. Initial emphasis is on attack detection and diagnosis; closed-loop mitigation and live deployment are outside the present scope.

An initial study could compare an electrical-state residual against a topology-conditioned residual. That is a hypothesis to investigate, not an implemented method or a novelty claim. The full audit must establish what existing state estimators, topology-error detectors, and digital twins already do.

## Decisions still needed

- Choose one electrical setting: AC distribution, transmission, or DC microgrid. Results across these are not automatically comparable.
- Specify available measurements, units and reference frames, sensor locations, sampling rates, topology information, and which inputs are independently trusted.
- Separate normal load variation, authorized switching, physical faults, sensor faults, and cyberattacks in the labels. A voltage deviation alone does not identify malicious intent.
- Define whether the twin is a steady-state estimator, dynamic simulator, or synchronized model. A topology diagram or power-flow case alone is not an operational digital twin.
- Determine whether suitable chronological attack recordings exist, or whether a clearly labelled simulated study is necessary. Network-only logs cannot validate an electrical-state consistency claim by themselves.

If attackers can forge both measurements and every topology/status input, physical consistency alone may not identify the attack. Observability, model mismatch, and trusted-input assumptions must bound any claim.

## Current evidence and boundaries

Two recent digital-twin security papers and two data/simulator leads have been screened in [the evidence register](docs/LITERATURE_EVIDENCE.md). They are not reproduction-ready baselines. No grid dataset, model, experiment code, trained model, or benchmark result has been acquired or created for this project. No environment has been installed or tested.

Future principal baseline papers should fall within **2023-10-16 through 2026-10-16**, preferably 2024–2026. Older methodological references and dataset descriptions remain background; dataset age is not governed by the paper window. SWaT/WADI are not required for this project. Future grid comparisons must use the same verified releases, scenarios, measurement access, and evaluation rules.

The agreed full-audit sequence is **water → manufacturing → smart grids**. Until the smart-grid stage is authorized, maintain these scoping documents without expanding into implementation or training. See [status](STATUS.md), [access checklist](docs/DATASET_ACCESS_CHECKLIST.md), and [proposed reproduction plan](docs/REPRODUCTION_PLAN.md).

## Shared publication and writing preferences

Apply the confirmed [shared publication standards](../docs/PUBLICATION_STANDARDS.md): aim for leading field-appropriate journals through rigorous distinct research, use natural precise academic prose, and develop distinctive titles grounded in the supported contribution. The user also records intended future EB-2 use; individual authorship, impact and publication claims must remain factual. Existing titles stay provisional, and no publication or immigration outcome is assured.
