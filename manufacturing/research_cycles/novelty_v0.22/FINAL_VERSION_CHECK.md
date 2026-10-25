# Ghanipoor et al.: final-version check

Audit date: 2026-10-24. Project: manufacturing; owner: Haiqa Mushtaq; operator: Codex research subagent. Scope: bounded primary-source inspection and author-code provenance, without cloning, execution, contact, dataset access, or access-control bypass.

## Decision

**The 2026 journal article exists, but its full text was not obtained in this check. Whether it closes the sufficient-sensitivity gap in the 2025 preprint remains unresolved.** A new method must not be called novel merely because the accessible preprint leaves that question open. The final article needs equation-level comparison before the candidate contribution is admitted.

The accessible preprint is strong close prior art for learning residual filters with formal incremental robustness properties. It cannot establish that a 2026 sufficient-detection claim is new. Conversely, publication metadata and the abstract do not establish that the final article proves a lower sensitivity bound.

## Exact records and inspection coverage

### Published journal record — metadata verified; final equations inaccessible

Ghanipoor, F.; Ferrari Trecate, G.; van de Wouw, N.; Murguia, C. *Provably robust data-driven sensor fault diagnosis using incrementally stable recurrent equilibrium networks*. **Automatica 191 (September 2026), 113096**. DOI: [10.1016/j.automatica.2026.113096](https://doi.org/10.1016/j.automatica.2026.113096).

- [Publisher article](https://www.sciencedirect.com/science/article/pii/S0005109826002803): search-index preview exposed the title, authors, volume, article number, abstract and open-access designation. Direct opening returned HTTP 403; no body, proofs, supplement or final reference list was inspected.
- [EPFL DECODE publications](https://www.epfl.ch/labs/decode/dependable-control-and-decision-group/publications/): author-lab listing independently confirms the title, author order, journal, year, volume and DOI. Its detailed-record and publisher links did not yield readable full text.
- [EPFL institutional discovery record](https://graphsearch.epfl.ch/en/publication/64388483-db0e-4b11-ae49-ebd0ba9075b2): bibliographic/abstract coverage only; links to the [Infoscience record](https://infoscience.epfl.ch/entities/publication/64388483-db0e-4b11-ae49-ebd0ba9075b2), which was not retrievable through the available web tool.
- [TU/e author profile](https://research.tue.nl/en/persons/farhad-ghanipoor/): inspected as another institutional route; the accessible outputs did not supply this final article.

Search results also exposed a ResearchGate journal record saying no full text was available. No full-text request was made. This secondary access observation is not claim evidence.

### Accessible preprint — exact version inspected

[arXiv:2504.19688v1](https://arxiv.org/html/2504.19688v1), submitted **28 April 2025, 11:28:32 UTC**, *Data-Driven Sensor Fault Diagnosis with Proven Guarantees using Incrementally Stable Recurrent Neural Networks*. Authors: Farhad Ghanipoor, Carlos Murguia, Giancarlo Ferrari Trecate, Nathan van de Wouw. [Abstract/history record](https://arxiv.org/abs/2504.19688) lists only v1 at inspection. License shown: CC BY 4.0.

Inspection covered Theorem 1, equations (6)–(7), Remark 1, the empirical training discussion, Section IV's repository pointer, and the conclusion. Equation (6) bounds the residual response **above** by a constant times the target fault norm. It is not a positive lower response bound. Remark 1 treats the corresponding large upper gain as a necessary sensitivity condition; small cross-sensor gain supplies an insensitivity guarantee. Training additionally encourages target-fault response empirically using artificial fault examples. The conclusion leaves direct parameterization guaranteeing sufficient sensitivity to future work.

This conclusion is **v1-specific**. The journal title and author order differ. A same-work relationship is plausible, but the version differences and final theorem content have not been verified. Do not cite the journal DOI as evidence for v1's stated limitation.

## Actual author repository

Section IV of the inspected preprint directly links [DecodEPFL/faultDiag](https://github.com/DecodEPFL/faultDiag), so this is stronger provenance than a name-based repository search.

- Read-only GitHub connector inspection: repository metadata, root contents, current `main` commit metadata, and pinned README.
- Observed `main`: [`6a4e0a81051fe2d8025b58cb3b21db6f6efc57f9`](https://github.com/DecodEPFL/faultDiag/tree/6a4e0a81051fe2d8025b58cb3b21db6f6efc57f9); commit date and repository pushed date: **2025-03-25T16:28:51Z**.
- Root entries: `README.md`, `data/`, `data_generating_sys/`, `main.py`, `post_process.py`, `results/`, `src/`.
- [Pinned README](https://github.com/DecodEPFL/faultDiag/blob/6a4e0a81051fe2d8025b58cb3b21db6f6efc57f9/README.md) supplies only the repository name and a brief sensor-fault-diagnosis description. It gives no final-paper correspondence or reproduction protocol.
- No root license file was listed; repository metadata reported `license: null`. **Reuse permission remains unresolved**; this is not proof that no license exists anywhere in the tree.
- No source implementation, dependencies, dataset terms, trained weights or numerical results were audited. No clone, installation or execution occurred. Code availability is verified for the linked preprint; final-version correspondence and execution readiness are not.

## Bounded query/access log

Searches included the exact final title; final title plus `pdf`, `sufficient`, `sensitivity`, `Remark`, and `future`; the final DOI; author/institution combinations; and publisher-domain queries for `S0005109826002803` plus `sufficient` or `sensitivity`. Searches were used to locate primary publisher, institution and author routes. Unrelated retrieved records were not treated as evidence.

Opened the publisher article, EPFL discovery and Infoscience records, DECODE publication listing and its links, TU/e author profile, arXiv abstract/history, and arXiv v1 HTML. The arXiv history supplied one displayed version. The unsuccessful attempt to retrieve a v2 did not establish that another journal manuscript is absent. Read-only GitHub requests used repository metadata, `/contents/`, `/commits/main`, and the pinned raw README. No citation-verification API, author request, or paywall workaround was used.

## Consequence for the proposed manufacturing direction

The proposed identity-minus-contractive adapter and protected scale need their own proof, precise assumptions and independent evidence. They must then be compared against **the final paper's actual result**, including the role of thresholds, calibration, faults and initial conditions. Even a valid lower bound would not by itself establish novelty over other existing lower-gain/detectability constructions. Until that comparison is possible, the contribution status is **a mathematical design hypothesis under prior-art challenge**, not a verified new method and not journal-ready evidence.
