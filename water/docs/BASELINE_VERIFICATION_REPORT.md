# Verification of the three water baseline collections

Audit date: **16 October 2026**. Scope: verify the acquired papers, extracted material, project summaries, bibliography records and available author code. The three paper identities are supported by primary records. **The audit does not give all three methods a scientific or execution clearance.** It found substantive problems in authentic sources, alongside missing reproducibility evidence.

## Verdict by method

| Method | Identity and local material | Scientific / implementation findings | Decision |
|---|---|---|---|
| **CAROTS** | ICML/PMLR paper and matched pinned author repository verified; source snapshot intact | Test-label threshold/metric selection, broken alternative threshold wiring, loader-configuration and causal-checkpoint concerns; hardware/dependencies untested | Retain as the first conditional reproduction candidate; repair and test the declared evaluation path before any run |
| **IT-DT** | arXiv v1 preprint verified; figures and manuscript source intact; peer-reviewed version not verified | Alarm annotation conflicts with the displayed KL score/threshold; ambiguous metric/complexity details; code, matrices and underlying measurements unavailable | Useful for learning the model-based approach; keep numerical reproduction and performance claims on hold |
| **Digital-twin ensemble** | Scientific Reports article and corresponding PMC material verified | Incorrect reference identifiers, mathematical/robustness inconsistencies, metric and dataset questions; executable code/results unavailable | Retain for critical reading and prior-art awareness; do not use it as a trusted numerical benchmark or the technical foundation of our method |

Primary records: [CAROTS](https://proceedings.mlr.press/v267/kim25aa.html), [IT-DT v1](https://arxiv.org/abs/2603.01621v1), [ensemble](https://www.nature.com/articles/s41598-026-53863-z). Detailed checks and corrections are in [CAROTS verification](../baselines/carots/VERIFICATION_REPORT.md), [IT-DT verification](../baselines/it_dt/VERIFICATION_REPORT.md) and [ensemble verification](../baselines/dt_ensemble/VERIFICATION_REPORT.md). A real publication record establishes that a work exists; it does not independently establish that its experiments occurred as described or that its conclusions are correct.

## File integrity and extraction checks

The reproducible local audit is [INTEGRITY_AUDIT.json](../baselines/INTEGRITY_AUDIT.json), generated with `python3 tools/audit_baseline_resources.py` from `water/`. It checked all **110 acquired objects and 79 reading derivatives** against their saved byte counts/SHA-256. All passed. The 73 pinned CAROTS repository objects also matched their Git blob identifiers; all derivative source hashes matched.

| Check | Coverage | Result and limit |
|---|---:|---|
| PDF metadata, text parsing and complete rasterization | 24 PDFs, 113 pages counting duplicate/version copies | No failed pages; two PDFs emitted system font-cache warnings but rendered successfully. Representative scientific figures were also visually inspected; rasterization alone is not semantic validation |
| Original versus extracted archive bytes | 32 CAROTS files and 7 IT-DT files | All regular-file contents identical; no source archive was compiled |
| Ensemble XML extractions | 7 tables, 5 figure elements including algorithm, 1 reference list | Parsed trees are semantically identical to the corresponding source elements; plain-text excerpts remain lossy reading aids |
| Image decoding | 10 PNG/JPEG files | Decoded successfully |
| Python / shell parsing | 37 author Python files; 15 shell scripts | AST / `bash -n` passed; imports, dependencies and runtime behavior remain untested |
| Graph containers | 2 NumPy files | Numeric headers/payload sizes valid; SWaT 51×51 and WADI 123×123. This does not establish feature alignment or causal correctness |
| Checkpoint containers | 2 ZIP-based `.pth` files | ZIP CRC checks passed; pickle/model contents were never loaded. These are CUTS+ component checkpoints, not final CAROTS detector weights |

No corruption or extraction substitution was detected in this scope. The originals were preserved. File hashes detect changes relative to the acquisition record; they are not proof of scientific validity or a security guarantee for executing code.

## Material findings

**CAROTS — execution and evaluation need explicit changes.** The pinned `threshold.py` alternative `ratio` path checks `val_scores` but reads nonexistent `val_score`; the predictor does not supply the required validation-score array. Simply switching the threshold option therefore does not create a usable clean-calibration path. The predictor modifies a cloned configuration but constructs loaders with the original configuration. The fresh causal-discoverer training path also requires review of last-versus-best checkpoint selection. These are static findings with file/line evidence in the method report, not claimed runtime measurements. The paper's broad superiority wording must be read against individual table rows; the full model is not uniformly best, including its WADI result.

**IT-DT — the alarm figure is internally inconsistent as displayed.** The original timeline marks an IT-DT alarm around 543 seconds, while the blue KL score is below the red 0.40 threshold at that time. The first displayed post-onset crossing is approximately 590 seconds. These times are visual estimates, not digitized score measurements. The underlying score arrays and plotting script are unavailable, so this establishes a figure/decision-rule discrepancy rather than what the actual experiment did. Minor rounding/aggregation and per-step covariance-computation questions are documented separately.

**Ensemble — several claims need correction or supporting evidence.** Reference 24 supplies a DOI for an unrelated work while naming Cohen et al.'s genuine randomized-smoothing paper; other identifier errors are recorded individually. Equation 7 divides a Gaussian residual quadratic form by the channel count but assigns the unscaled chi-square distribution to it. The displayed smoothing-radius formula with the stated inputs gives **0.032897**, not **0.05**. The cited Gaussian-smoothing result is for the **L2** norm, whereas the article claims an **L∞** certificate without the needed justification. [Cohen et al., original proceedings](https://proceedings.mlr.press/v97/cohen19c.html)

The ensemble's Table 3 gives FPR equal to `100% − precision` in every row. Those quantities have different denominators; absent confusion counts and aggregation details, this is an unresolved metric-definition question. Figure 3's WADI-to-Tennessee-Eastman difference is **0.6** percentage points from its displayed values, not the caption's **2.2**. The SWaT validation-day and sampling-rate issues remain unresolved. These findings warrant withholding numerical trust; they do not establish intentional fabrication or identify how the manuscript was written.

The same table labels a comparator “LSTM” while citing TABOR, whose inspected method uses timed automata and Bayesian networks. The citation therefore does not establish the identity of the claimed LSTM implementation. This is a consequential comparison gap, separate from whether TABOR is a real paper.

## Bibliography coverage and limits

The complete supplied inventories are retained in [CAROTS reference checks](../baselines/carots/REFERENCE_CHECKS.json), [IT-DT reference checks](../baselines/it_dt/REFERENCE_CHECKS.json) and [ensemble reference checks](../baselines/dt_ensemble/REFERENCE_CHECKS.json). CAROTS contains 81 BibTeX records, of which 54 appear in the rendered bibliography; 27 unused records are kept distinct. IT-DT has 28 entries representing 27 unique works because one is duplicated. The ensemble has 31 entries.

Each method report records actual primary-metadata coverage, corrections and unresolved entries. Metadata identity is separate from whether a source supports a particular sentence. Selected consequential citation claims were checked against accessible original sources; **every statement in every cited work has not been verified**. Failed access or an incorrect DOI does not prove that the named paper is nonexistent. No global retraction clearance, author-authenticity investigation or misconduct determination is claimed.

IT-DT's 28 entries all matched primary metadata, including its duplicate; the ensemble's 31 entries yielded 29 identified intended works and two partial records. Those identities include entries with citation-field errors. The ensemble has three incorrect DOI references (13, 24 and 26), with separately verified intended works. Its other bibliography problems include author lists and a chapter misdescribed as a book. Preserved bibliographies must not be copied into our paper without independent correction and claim-specific checking.

CAROTS identity lookups were attempted for all 54 rendered references: 51 have scoped primary/author identity evidence, two have only primary-title records with incomplete metadata, and one WADI-paper primary record remained inaccessible. The 27 unused BibTeX records were inventoried but not independently researched. Across the three rendered bibliographies, **all 113 entries received an identity lookup attempt**, with 108 scoped identity matches and five partial/inaccessible records. These counts include the IT-DT duplicate and are not counts of unique works, verified claims or trustworthy experiments.

## Consequences for this project

Keep the three resource packs and their unchanged originals, but use their verification reports before citing any specific claim. Use CAROTS to learn and prepare a bounded reproduction specification. IT-DT and the ensemble remain conditional reading material, and stronger independently verifiable twin comparators should be sought before fixing the experimental set. Three collected papers do not satisfy the scientific comparison requirement by themselves.

SWaT/WADI files and provider approval remain absent. Exact common releases, code execution and all published performance claims remain unverified by reproduction. No model or dataset loader was run; no dependencies were installed, and no training, author contact or publishing occurred during this audit.

The installed ARS-Codex `deep-research` fact-check guidance and PDF skill informed this work. Three native workers checked separate papers; the parent checked file integrity, cross-file consistency and selected mathematical/visual findings. This was a source audit with shared project context, not blinded independent replication or a formal journal review. Project instructions override the skill's generic medical evidence hierarchy, fuzzy-title acceptance and inference of fabrication from failed searches.
