# Claim-to-evidence map — revision 1.6

| Main-paper claim | Evidence | Interpretation boundary |
|---|---|---|
| State, ARX recurrence, RBF correction and gate | `research_cycles/residual_twin_v0.13/model.py`, `MODEL_PROPOSAL.md`; inherited `commissioning_v0.9/models.py`; `attack_audit_v0.14/audit_core.py` | Actual code and mathematical description; no new algorithmic novelty claim. |
| Thirty correction fits and selected settings | `local/residual_twin_v0.13/runs/pilot_001/candidates.json`, `selection.json`, `summary.json` | Selected from a finite normal-only grid, not global optimum. |
| Selected-settings table: normal changes and thresholds | Same saved selection/summary; `generate_assets.py` | Percentage changes derived from the saved base/RBF values. |
| 189 episodes, 17 methods and complete support | `local/attack_audit_v0.14/runs/audit_001/catalog.json`, `config.json` in its research cycle, `summary.json` | Synthetic tasks and repeated plant structures; not independent robot acquisitions. |
| Complete final table and in-paper Appendix B metrics | Saved audit `summary.json`; generated tables bound in `ASSET_RECEIPT.json` | No point adjustment, post-result threshold search or omitted declared method. |
| Failed primary, 2.0123% reduction and plant deterioration | Saved `summary.json/primary`; plant strata | Secondary improvements do not overturn the predeclared criterion. |
| Short-window equivalence and falling-edge clarification | `research_cycles/attack_audit_v0.14/DESCRIPTIVE_DIAGNOSTICS.json` | Explicit post-study diagnostic; instantaneous deviation and registered continuity are different targets. |
| Recovery trace figure | Saved `score_N14_Q2_17_persistent_offset.npz`, paired truth, calibration and Q2 base scale | Post-study illustration, not new independent evidence. |
| E1/E2 earlier findings | Sealed `recovery_v0.8`, `commissioning_v0.9` reports; byte-identical revision-1.2 generated tables | Different calibration/population; no pooled ranking across study versions. |
| IMU prediction errors and training limits | `casper_convergence_v0.11/RESULTS.md`, `all_outcomes.csv`, original saved histories; retained figure/table | Development MSE only; independent implementations, no attack superiority. |
| E4 20/36 result and Gaussian bounds | `return_bound_v0.12/RESULTS.md`, saved verifier and retained proof/table | Oracle-informed synthetic residual signals and conditional assumptions. |
| Costs and checks | Each study's supervisor, summary, verification and provenance | Whole-pipeline costs and software consistency, not physical validation or standalone deployment latency. |
| voraus-AD original identity/counts and MVT-Flow concerns | `evidence_admission_v0.15/PACKAGE_MANIFEST.json`, `DECISION.md`, metadata and static/synthetic code checks | No process signal inspection or baseline execution; code mismatch is not proof of invalid publication results. |
| FactoryNet status | Pinned primary manuscript, code and dataset card in the same admission package | Author-reported totals, partly incomplete synthetic snapshot, no downloaded signals. |
| Existing method/survey statements | `REFERENCE_AUDIT.md`, full BibTeX and source receipts | Verification scope varies; inaccessible full algorithms and unexecuted methods remain explicit. |

No numeric result was invented to satisfy a reviewer item. No new significance test, confidence interval, robustness guarantee, sensor-forgery defense or independent real-robot replication is claimed.

## Added explanatory material

- Sections 3–6 and the two algorithms expand the same model and protocol. `residual_twin_v0.13/model.py` and `attack_audit_v0.14/audit_core.py`/`evaluation.py` resolve constant-feature handling, causal windows, alarm ordering, AP ties and conditional recovery denominators.
- Tuning plot: all 30 saved `candidates.json` entries and role-specific `selection.json` decisions. No new search or fit.
- Trade-off/component plots: recorded pooled `summary.json` values, including percentage conversion of benign fractions. `FIGURE_VALUES.json` stores every plotted value; the editorial audit checks each against its saved input.
- All prior generated table files remain byte-identical; learned-curve and uncertainty-heatmap PDFs remain unchanged. Earlier supplementary content is incorporated into the article, with repeated prose condensed.
- The teacher PDF supplies organization only; it supplies no manufacturing model, result, reference quota or novelty evidence.


## Added evidence in revision 1.6

| Statement | Saved evidence | Boundary |
|---|---|---|
| Five chronological folds refit both references; RBF improves 2/5 pooled folds and 5/15 plant–fold cases | `research_cycles/fivefold_v0.16/VERIFICATION.json`, `RESULTS.md`, sealed fitted arrays | Retrospective normal development with previously selected settings; no nested selection or independent attack confirmation |
| ModernTCN, iTransformer and TimeMixer run three seeds each using official model classes | `research_cycles/forecast_baselines_v0.17/FREEZE.json`, full campaign summaries, per-seed logs/checkpoints | Modified common-IMU forecasting protocol, not published benchmark or complete cyberattack-detector reproduction |
| All nine runs stop by declared CPU admission; complete per-seed outcomes appear in the new table | Full run records and `FORECAST_ASSET_RECEIPT.json` | No claim of convergence; checkpoint selection uses already-exposed normal development |
| Cited recent comparator papers fall in the declared window | `RECENCY_AND_CORRESPONDENCE.md`, prior full-reference audit, official proceedings/manuscripts and author code | Publication versions differ from first preprints; recency alone does not imply state of the art or fair task equivalence |

Original attack-audit findings and the failed primary improvement criterion are unchanged. New normal prediction numbers cannot establish a superior attack detector. No result is substituted for an unexecuted MVT-Flow or full CASPER experiment.
