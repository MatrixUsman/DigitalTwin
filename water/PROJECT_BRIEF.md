# Project brief

Status: source collection, reading preparation and data-access audit. Updated **16 October 2026 (Asia/Karachi)**. The later acquisition request authorizes local public resource collection; model implementation and training have not begun.

Project ID: `water`. Owner: **Muhammad Usman** (project responsibility, not a final authorship decision). This project inherits [shared workspace rules](../AGENTS.md) and has its own [status/handoff](STATUS.md). Run future commands from `water/`.

**Current access update:** the official SWaT/WADI request was submitted after the user supplied the university email and explicitly accepted the stated terms/privacy consent. Website confirmation was observed by the post-submission clock check at **2026-10-16 16:15:51 UTC**; this is not an exact server timestamp. The form's default **17 October 2026** date was preserved because Singapore was already on that date. Approval, download access and dataset receipt remain pending. Exact personal details are retained only in ignored local storage. See the [request summary](docs/DATASET_REQUEST_PREPARATION.md); no duplicate submission is needed.

## Research scope

**Provisional title:** Trust-Gated Digital Twins for Cyberattack Detection in Water Infrastructure.

**Candidate question:** Can a digital twin adapt to legitimate operational changes without learning corrupted measurements as normal behaviour?

Sector: water-treatment and water-distribution industrial control systems. Shared evaluation datasets: **SWaT and WADI**, with releases and access still unconfirmed. The publication window for main baseline papers is **16 October 2023–16 October 2026**, inclusive, preferably 2024–2026. This restriction concerns papers, not the age of the datasets.

The mechanism, title, and novelty are not finalized. No model implementation by us, baseline reproduction, training run, or experimental result exists in this project. Author source and published artifacts are now available in the [three-paper collection](baselines/README.md); literature claims are not our measurements.

## Working hypothesis, not a contribution claim

Investigate whether an explicit acceptance rule for adaptation can reduce false alarms under legitimate change while limiting contamination from malicious measurements. A fixed reference model and a guarded adaptive model are candidate designs, not selected architecture. First specify whether adaptation changes model parameters, residual calibration, alarm thresholds, or state estimates.

The information available to the gate must be stated. Recorded actuator values are not automatically authenticated commands. With all relevant observations forgeable and no independent trusted signal, legitimate changes and attacks may be observationally indistinguishable. Existing adaptive/gated twin methods must be compared before any novelty claim; see the [literature evidence](docs/LITERATURE_EVIDENCE.md).

SWaT/WADI attack detection alone cannot establish successful adaptation to legitimate changes. That requires verified regime-change evidence or a separately labelled, physically justified evaluation. Synthetic measurement stress tests cannot substitute for that evidence.

## Initial audit outcome

The observations below describe the original single-water workspace before the three-project reorganization. Statements about no submitted request describe that historical audit stage; the later authorized submission is recorded above. Shared machine information remains at the workspace root; research evidence and future data/runs are local to this project.

- The workspace was empty when inspected. No Git repository, source PDF, `literature_candidates.md`, dataset files, or existing experiments were present.
- The previous conversation was subsequently supplied as text in this chat. It is a lead source, not verified evidence. The referenced `ijcatr15081004 (1).pdf` itself is still unavailable.
- No SWaT/WADI files were found **within this workspace**. No external dataset path or access authorization has been confirmed; no whole-computer search was performed.
- **Earlier correction, 2026-10-16:** the researcher reported having a COMSATS Sahiwal student university email, superseding the earlier statement of no affiliation/email. At that audit stage, the exact address and dataset access were unverified and no request or inquiry had been submitted. The [iTrust request form](https://www.sutd.edu.sg/itrust/request-for-datasets/) required a university/organisation email and showed no faculty-only requirement or student ban. The later private address supply and authorized submission are recorded above; approval remains pending. See the [access checklist](docs/DATASET_ACCESS_CHECKLIST.md).
- Local hardware: Apple M5 Pro, 18 CPU cores, 24 GB memory, 20-core Metal GPU, approximately 49 GiB free disk space at inspection. CUDA is not available through this local hardware; PyTorch/MPS compatibility has not been tested.
- Candidate evidence and implementation limitations were recorded separately. During the initial audit, no dataset contents were downloaded or uploaded, and no access request or author message was sent.

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

The immediate next milestone is structured reading of the collected papers while authorized dataset receipt remains pending. Later baseline setup must freeze data manifests and evaluation protocol, resolve implementation issues, and pass loader/split/metric tests before training. Paid compute, lengthy training, and publishing require approval.

## Shared publication and writing preferences

Apply the confirmed [shared publication standards](../docs/PUBLICATION_STANDARDS.md): aim for leading field-appropriate journals through rigorous distinct research, use natural precise academic prose, and develop distinctive titles grounded in the supported contribution. The user also records intended future EB-2 use; individual authorship, impact and publication claims must remain factual. Existing titles stay provisional, and no publication or immigration outcome is assured.
