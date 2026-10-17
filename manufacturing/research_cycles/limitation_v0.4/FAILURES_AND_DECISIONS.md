# Attempt history and decisions

17 October 2026. Preserve this history alongside the consumed attempt directories.

| Attempt | Outcome | Disposition |
|---|---|---|
| `tests_001` | 21/22 synthetic tests passed. Offset subtraction in a float32 fixture differed from 2 by at most 3.8146973e-6; default `assert_allclose` was stricter than float32 spacing. | Preserved failed log. Changed only the fixture tolerance to one float32 spacing at the fixture maximum; no intervention data had been executed or inspected. |
| `tests_002` | 22/22 synthetic tests passed. | Created the pre-execution freeze with 10 source and 260 input identities. |
| `replay_001` | Completed all six models × 189 cases, then sealed predictions/calibration and computed all 4,536 outcomes. | Retained without rerun or scientific change. |
| `verify_001` | 26,374/26,374 separate arithmetic/inference/identity checks passed. | Retained the independent-process receipt. |
| Presentation | Three PNG/SVG figures generated. | Inspected all figures; restricted the example plots' score axes to nonnegative values. No scientific values changed. The report uses exact F1 values rather than describing a 1.85-fold change as a doubling. |

A preliminary console-only descriptive query attempted a median for groups with zero detected events and emitted NumPy empty-slice warnings. No reported value uses that NaN: the saved report generator explicitly returns `null` for an empty conditional-delay set and preserves all misses. This was not a scoring or verification failure. Matplotlib built a project-local font cache normally.

The calibrated CUSUM is a tested standard-method candidate, not a selected final algorithm. Its higher long-event point recall accompanies fewer event hits than point scoring and substantial post-event alarms. The 45-point rolling mean has the strongest mean F1 among the declared CNN scoring rules for long deviations. This observation informs future development; it cannot retroactively select a confirmatory final method on these exposed outcomes. No additional fit, tuning, best-seed choice or suppression of cases occurred.

Next scientific work should address brief sensitivity, persistent evidence and justified recovery under explicit physical/context assumptions. A more elaborate observer must beat ordinary smoothing, accumulation and reset controls and differ precisely from prior work. Neither the measured effect nor the tested ordinary improvements establish novelty by themselves.
