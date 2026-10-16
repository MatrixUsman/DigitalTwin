# Literature evidence and baseline admission table

Audit date: **16 October 2026 (Asia/Karachi)**. Inclusion window: **16 October 2023–16 October 2026**, inclusive. Prefer 2024–2026. This is a targeted audit of supplied leads plus one reserve candidate, not an exhaustive systematic review.

The workspace initially had no notes or `literature_candidates.md`; the user subsequently pasted the earlier conversation. [Candidate register](literature_candidates.md) records those leads. No paper's numerical results were reproduced. “Both datasets” below means a primary source reports SWaT and WADI; it does **not** establish common releases, comparable metrics, or our dataset access.

Evidence labels: **verified** = observed directly in the linked primary source; **reported** = authors' experimental assertion, not independently replicated; **unverified** = insufficient evidence; **inaccessible** = retrieval failed; **not located** = bounded searches found no matched artifact, not proof of nonexistence. Peer-reviewed venue status does not mean that its experimental claims have been validated by this project.

A subsequent [ARS fact-check](RESEARCH_READINESS_REVIEW.md) rechecked CAROTS threshold/reporting versus checkpoint selection, distinguished ensemble alarm gating from update admission, and reconfirmed that release equivalence and local dataset access remain unresolved.

## Main candidate papers: bibliographic evidence

| Candidate / primary record | Publication date and peer review | DOI / identifier | Both datasets? | Decision |
|---|---|---|---|---|
| **CAROTS**, Kim et al., *Causality-Aware Contrastive Learning for Robust Multivariate Time-Series Anomaly Detection*. [PMLR/ICML](https://proceedings.mlr.press/v267/kim25aa.html) | ICML 2025 proceedings, 13–19 July 2025; peer-reviewed. Preprint 4 June 2025. Exact first-online proceedings date not verified. | `pmlr-v267-kim25aa`; `arXiv:2506.03964`; no publisher DOI shown | Yes, manuscript | **First conditional reproduction candidate**, full and no-ensemble variants |
| **Information-Theoretic Digital Twins (IT-DT)**, Kreso et al. [arXiv record](https://arxiv.org/abs/2603.01621) | 2 March 2026 preprint; peer-reviewed publication **not verified** | `arXiv:2603.01621`; `10.48550/arXiv.2603.01621` | Yes, manuscript | Later provisional twin reimplementation candidate |
| **Causal Digital Twins (CDT)**, Homaei et al. [Publisher](https://www.sciencedirect.com/science/article/pii/S2666827025002075) | Online 17 December 2025; March 2026 issue; accepted journal article. Dates from author-uploaded published manuscript; direct publisher access blocked. | `10.1016/j.mlwa.2025.100824`; preprint `2510.09616` | Yes, manuscript | Hold for code/protocol clarification |
| **DPDGAD**, Liao et al. [Publisher](https://www.sciencedirect.com/science/article/pii/S1474034624001952) | August 2024 issue; peer-reviewed journal venue. Exact first-online/acceptance dates unverified. | `10.1016/j.aei.2024.102547` | Yes, publisher abstract | Hold: full text and usable author code unverified |
| **Digital-twin/deep-learning ensemble**, Sayghe et al. [Scientific Reports](https://www.nature.com/articles/s41598-026-53863-z) | Published 22 May 2026; version of record 27 July 2026; peer-reviewed journal | `10.1038/s41598-026-53863-z` | Yes, full text | Hold: protocol and code gaps; close prior art for gating |

Full titles/authors, manuscript versions, source access, publication histories and code details are in the linked evidence records below. A preprint DOI is not evidence of peer review. An issue date and an online date are recorded separately when known.

## Reproduction evidence table

| Method | Dataset releases | Preprocessing and evaluation evidence | Code / access | Principal limitations and unresolved items |
|---|---|---|---|---|
| CAROTS | Code expects SWaT Normal v1 / Attack v0 and WADI A2 filenames; hashes/provider equivalence unverified | Normal validation; training scaling; factor-five aggregation; optimal-test-F1 paths in code need replacement; manuscript excludes PA-F1 | [kimanki/CAROTS](https://github.com/kimanki/CAROTS), pinned code evidence, modified non-commercial license | CUDA assumptions, possible alignment issue, raw-folder cache writes, aggregation/metric mismatch. [Detailed audit](literature/CAROTS_AND_INFORMATION_THEORETIC.md) |
| IT-DT | Exact releases/files unverified | State-space identification and KL residual monitor; normal calibration described; window-selection label provenance unclear | Full preprint accessible; author code/license and published venue not located | Missing reproducible preprocessing/splits; Gaussian and transition assumptions. [Detailed audit](literature/CAROTS_AND_INFORMATION_THEORETIC.md) |
| CDT | Exact releases/files unverified | SWaT day split described; WADI split and threshold provenance unresolved | Published author copy and preprint accessible; matching author code not located, request restriction stated | Version differences and nonstandard FPR definition. [Detailed audit](literature/CAUSAL_AND_ENSEMBLE.md) |
| DPDGAD | Exact releases/files unverified | Anomaly-free training mentioned; full preprocessing, validation and metrics protocol inaccessible | Publisher abstract/snippets only; similarly named empty repository is not verified author code | Cannot infer reproducibility from abstract scores. [Detailed audit](literature/DPDGAD_AND_BASELINE.md) |
| Ensemble | Exact releases/files unverified | Normal-only validation and gated adaptation described; SWaT day-8/cadence requires reconciliation | Full publisher text accessible; matched runnable author code not verified | Existing gate/adaptation overlaps proposed concept; physics artifacts and certification rule unresolved. [Detailed audit](literature/CAUSAL_AND_ENSEMBLE.md) |

No main candidate currently clears **all** execution gates: authorized data, matched releases, inspectable implementation, tested dependencies/device, and a frozen test-independent evaluation. The recommendation ranks the work needed next; it is not an endorsement of published rankings.

## Additional recent reserve comparator

**CARLA**, Darban et al., *CARLA: Self-supervised contrastive representation learning for time series anomaly detection*. [Publisher / DOI 10.1016/j.patcog.2024.110874](https://www.sciencedirect.com/science/article/pii/S0031320324006253). Online 10 August 2024, January 2025 issue; peer-reviewed journal publication is within the window, although the first preprint (18 August 2023) predates it. Both datasets are reported; [MIT author code](https://github.com/zamanzadeh/CARLA) is available. Exact releases are unresolved. Static code tracing finds test-F1-guided checkpoint selection as well as threshold optimization; paper/code preprocessing also differs. Reserve only, with substantial protocol changes required. [Full evidence](literature/DPDGAD_AND_BASELINE.md).

## Background and evaluation references — separate from main detectors

| Work | Verified role and status | Why separate |
|---|---|---|
| Fung, Zeng, Bauer, *Attributions for ML-based ICS Anomaly Detection: From Theory to Practice* | [NDSS 2024](https://www.ndss-symposium.org/ndss-paper/attributions-for-ml-based-ics-anomaly-detection-from-theory-to-practice/), peer-reviewed, `10.14722/ndss.2024.23216`; proceedings manuscript and [author code](https://github.com/pwwl/ics-anomaly-attribution) accessible. SWaT/WADI release documentation is useful. | Attribution/evaluation study, not a new twin detector; default random-window validation needs adaptation. [Evidence](literature/DPDGAD_AND_BASELINE.md) |
| Kampourakis et al., *Digital Twin Degradation: Detecting Cyber Physical Attacks via Temporal Inconsistencies* | [arXiv:2608.16159](https://arxiv.org/abs/2608.16159), 17 August 2026 preprint; full manuscript accessible; peer review/code unverified | SWaT, HAI, BATADAL; **no WADI evaluation verified**. Relevant to novelty review, not the shared-pair table. [Evidence](literature/CAUSAL_AND_ENSEMBLE.md) |
| Maxwellson, smart-manufacturing/APT architecture paper referenced by `ijcatr15081004 (1).pdf` | Author-posted manuscript located; DOI printed as `10.7753/IJCATR1508.1004`; publisher/date/review verification incomplete | Original attachment absent; manufacturing architecture is background, not an established SWaT/WADI experimental baseline. [Evidence and limitations](literature/ARCHITECTURE_BACKGROUND.md) |

## Recommended first milestone

Reproduce the **CAROTS architecture and both predeclared score variants using author code under our common, modified protocol**. Do not run its test-optimized threshold/F1 workflow. Verify the label pipeline and local device path first. Record every difference from the source paper; do not describe the resulting numbers as an exact replication of its published optimal F1. [Proposed reproduction plan](REPRODUCTION_PLAN.md)

Keep IT-DT as the later model-based twin candidate; missing code would make it our reimplementation. Keep CDT, DPDGAD and the ensemble on hold until evidence gaps are resolved. The existing gated/adaptive ensemble means that “we gate updates” alone is not a defensible novelty claim. The first result sought is a traceable baseline report, not a superiority claim.

Search coverage included exact titles/acronyms, publisher/proceedings records, arXiv full manuscripts, author or institution manuscript copies, repository links, and title/DOI/code searches. Source versions and code revisions are listed in individual records. No authors were contacted and no unavailable facts were filled from the previous conversation.
