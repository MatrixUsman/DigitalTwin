# Project brief

Status: audit and setup only. Updated **16 October 2026 (Asia/Karachi)**.

Project ID: `water`. Owner: **Muhammad Usman** (project responsibility, not a final authorship decision). This project inherits [shared workspace rules](../AGENTS.md) and has its own [status/handoff](STATUS.md). Run future commands from `water/`.

## Research scope

**Provisional title:** Trust-Gated Digital Twins for Cyberattack Detection in Water Infrastructure.

**Candidate question:** Can a digital twin adapt to legitimate operational changes without learning corrupted measurements as normal behaviour?

Sector: water-treatment and water-distribution industrial control systems. Shared evaluation datasets: **SWaT and WADI**, with releases and access still unconfirmed. The publication window for main baseline papers is **16 October 2023–16 October 2026**, inclusive, preferably 2024–2026. This restriction concerns papers, not the age of the datasets.

The mechanism, title, and novelty are not finalized. No implementation, baseline reproduction, training run, or experimental result exists in this project. Literature claims are not our measurements.

## Working hypothesis, not a contribution claim

Investigate whether an explicit acceptance rule for adaptation can reduce false alarms under legitimate change while limiting contamination from malicious measurements. A fixed reference model and a guarded adaptive model are candidate designs, not selected architecture. First specify whether adaptation changes model parameters, residual calibration, alarm thresholds, or state estimates.

The information available to the gate must be stated. Recorded actuator values are not automatically authenticated commands. With all relevant observations forgeable and no independent trusted signal, legitimate changes and attacks may be observationally indistinguishable. Existing adaptive/gated twin methods must be compared before any novelty claim; see the [literature evidence](docs/LITERATURE_EVIDENCE.md).

SWaT/WADI attack detection alone cannot establish successful adaptation to legitimate changes. That requires verified regime-change evidence or a separately labelled, physically justified evaluation. Synthetic measurement stress tests cannot substitute for that evidence.

## Initial audit outcome

The observations below describe the original single-water workspace before the three-project reorganization. Shared machine information remains at the workspace root; research evidence and future data/runs are local to this project.

- The workspace was empty when inspected. No Git repository, source PDF, `literature_candidates.md`, dataset files, or existing experiments were present.
- The previous conversation was subsequently supplied as text in this chat. It is a lead source, not verified evidence. The referenced `ijcatr15081004 (1).pdf` itself is still unavailable.
- No SWaT/WADI files were found **within this workspace**. No external dataset path or access authorization has been confirmed; no whole-computer search was performed.
- **Correction, 2026-10-16:** the researcher reports having a COMSATS Sahiwal student university email, superseding the earlier statement of no affiliation/email. The exact address and dataset access are unverified. The [iTrust request form](https://www.sutd.edu.sg/itrust/request-for-datasets/) requires a university/organisation email and shows no faculty-only requirement or student ban, so the standard request route is now plausible; provider approval remains pending and no request or inquiry has been submitted. See the [access checklist](docs/DATASET_ACCESS_CHECKLIST.md).
- Local hardware: Apple M5 Pro, 18 CPU cores, 24 GB memory, 20-core Metal GPU, approximately 49 GiB free disk space at inspection. CUDA is not available through this local hardware; PyTorch/MPS compatibility has not been tested.
- Candidate evidence and implementation limitations are recorded separately. No dataset contents were downloaded or uploaded; no access request or author message was sent.

## Deliverables and next decision

| Document | Purpose |
|---|---|
| [AGENTS.md](AGENTS.md) | Persistent research and workspace rules |
| [Literature evidence](docs/LITERATURE_EVIDENCE.md) | Candidate eligibility, verified sources, unresolved claims |
| [Dataset access checklist](docs/DATASET_ACCESS_CHECKLIST.md) | Access, releases, provenance, safe storage |
| [Workspace audit](../docs/WORKSPACE_AUDIT.md) | Observed compute, missing inputs, inspection commands |
| [Reproduction plan](docs/REPRODUCTION_PLAN.md) | First baseline, proposed environment/structure, evaluation and tests |
| [Research skill setup](../docs/RESEARCH_SKILL_SETUP.md) | Pinned ARS-Codex installation and project-specific usage rules |

Recommended first executable baseline: **CAROTS (ICML 2025), including its no-ensemble variant**, conditional on data access and resolution of code/protocol issues. An author-code run with a clean calibration threshold will be a **modified-protocol evaluation**, not a reproduction of its reported optimal-test-F1 result. The information-theoretic twin remains a later candidate for an explicitly identified independent implementation.

The next milestone is an authorized, bounded baseline setup: freeze data manifests and evaluation protocol, resolve implementation issues, and pass loader/split/metric tests before training. This audit stops before that milestone. Paid compute, lengthy training, and publishing require approval.

## Shared publication and writing preferences

Apply the confirmed [shared publication standards](../docs/PUBLICATION_STANDARDS.md): aim for leading field-appropriate journals through rigorous distinct research, use natural precise academic prose, and develop distinctive titles grounded in the supported contribution. The user also records intended future EB-2 use; individual authorship, impact and publication claims must remain factual. Existing titles stay provisional, and no publication or immigration outcome is assured.
