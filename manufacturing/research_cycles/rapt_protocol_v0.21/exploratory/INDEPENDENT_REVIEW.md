# Independent saved-outcome review: exploratory RAPT transfer

19 October 2026 (Asia/Karachi). AI-assisted independent arithmetic/source review; no model inference, training or new simulation was run.

**Verification passed: 3,920 independent identity, arithmetic and coverage checks.** All 243 frozen bindings match; all 36 score artifacts remain sealed. The complete Q1 population and both released modes are retained.

## Scope and checks

Read the frozen protocol, unmodified author gate implementation, worker access order and saved outputs. Independently recomputed both gate risks from saved per-channel loss and measured observations; alarms from strict risk > 1 with excluded warmup; confusion counts; alarm starts; overlap/fresh detection; return/clearance; outside-inactive support; first/final-quarter diagnostics; pooled/task/condition summaries; and tie-aware average precision. No primary evaluation, summary or quarter helper was imported. Every retained risk gate and alarm matches exactly; scalar distributions match within 1e-10 floating tolerance.

The access ledger and source ordering show all scores sealed before evaluator-only truth was loaded. This is an audit of recorded ordering, not an independent operating-system access trace. Saved per-channel loss is accepted as input here; the baseline agent separately verifies checkpoint inference.

## Complete pooled results

| Mode | Fresh / all | Misses | Benign alarms / observations | Starts per benign hour | F1 | AP | Outside-inactive / outside |
|---|---:|---:|---:|---:|---:|---:|---:|
| rapt_model | 9 / 24 | 15 | 5175 / 70800 | 277.119 | 0.105032 | 0.109608 | 9448 / 10689 |
| rapt_hybrid | 9 / 24 | 15 | 5175 / 70800 | 277.119 | 0.105032 | 0.109608 | 9448 / 10689 |

All 36 episodes contribute 129,600 rows and 126,000 eligible rows per mode. There are 12 benign episodes (70,800 eligible observations) and 24 interventions. Both modes produce identical risks and alarms in this run; neither is selected as preferable.

## Missingness and conditional recovery

```json
[
  {
    "mode": "rapt_model",
    "events": 24,
    "overlap_misses": 15,
    "fresh_delay_missing": 15,
    "physical_return_missing": 0,
    "clearance_unavailable_due_to_miss": 15,
    "clearance_censored_after_detected_return": 0,
    "already_inactive_at_return": 6,
    "observed_clearances": 9
  },
  {
    "mode": "rapt_hybrid",
    "events": 24,
    "overlap_misses": 15,
    "fresh_delay_missing": 15,
    "physical_return_missing": 0,
    "clearance_unavailable_due_to_miss": 15,
    "clearance_censored_after_detected_return": 0,
    "already_inactive_at_return": 6,
    "observed_clearances": 9
  }
]
```

Delay summaries must retain their observed denominator and all 24 event outcomes. Missed events are not assigned zero delay. Zero/short clearance after a detected event does not imply sustained support. The simulated physical-return quantity is a diagnostic introduced by this study; RAPT does not promise recovery certification.

## Early versus late risk

Each condition contains six episodes per mode. Numbers below are finite-grid descriptive diagnostics; risk is the median of the six episode-wise quarter medians. Quarter membership was fixed before replay. Both modes coincide, so the table prints model-only once while all hybrid outcomes remain saved.

| Condition | First / last quarter median risk | First / last alarm points | Quarter points each | First / last outside points | First / last inactive-outside | Episodes with lower late median |
|---|---:|---:|---:|---:|---:|---:|
| brief_offset | 1.36114 / 2.05605 | 6 / 9 | 15 | 9 / 15 | 3 / 6 | 3 / 6 |
| persistent_offset | 0.675517 / 0.414853 | 239 / 0 | 747 | 741 / 747 | 502 / 747 | 6 / 6 |
| hold | 0.222218 / 0.242141 | 0 / 0 | 747 | 741 / 747 | 741 / 747 | 3 / 6 |
| slow | 0.198897 / 0.312493 | 0 / 0 | 747 | 693 / 747 | 693 / 747 | 0 / 6 |

A lower final-quarter risk is not by itself a baseline failure. It may reflect trajectory changes, conditioning on recent measured state, learned variance, task shift, calibration or inadequate transfer. This single Q1/seed17 checkpoint and four-channel desired-command protocol do not identify one cause. These outcomes establish poor performance for this specific transferred configuration, not a refutation of the original humanoid experiments or a demonstrated advantage of another method.

## Comparison integrity and interpretation

Older v0.19 ARX/reference controls used different fitting populations. They are not ranked against this RAPT transfer. The fixed author architecture, saved epoch-14 checkpoint, normal-only selection and calibration remain unchanged. This is one author-code detector-component transfer on already exposed synthetic conditions, not full-paper reproduction, a fresh confirmatory test, independent physical evidence or a novelty result. No replacement success rule was introduced.

The reviewer found no arithmetic discrepancy in the saved outputs. The findings justify preserving the transfer diagnostic and investigating source-matched evidence or a separately frozen matched-training comparison. They do not justify tuning a new detector on these outcomes and calling the same grid independent confirmation.

## Evidence identity

- Freeze SHA-256: `35619d5219b2296e141f1262038bff521ba08b8f659d2f4b064fe7098f25ff43`.
- Saved result SHA-256: `418062b95123eb2521604b87764c6e8522f7c6b98785b37e4f31d6e6b1d5fd5a`.
- Saved outcomes SHA-256: `64405e17edc7b77ffad0dc44a8b267dc23f6c14de5127faaab832dbc7b5e7c92`.
- Score seal SHA-256: `83041156aa109cacddf1b55672256407c2a139cbd6f02ca166e03f39fcf96163`.
- Audit interpreter: `.venv-reproduction-v02/bin/python` (NumPy 1.26.4); working directory: `manufacturing/`.
- Only this review document was written by the reviewer. Original inputs, scores, models, protocol and manuscript were read without mutation.
