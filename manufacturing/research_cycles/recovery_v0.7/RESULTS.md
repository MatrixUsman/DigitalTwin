# Fresh recovery confirmation — completed

17 October 2026. All observations are **synthetic**, generated entirely in software. No physical equipment, raw CASPER access, new neural training or paid compute was required. This cycle is now exposed.

The selected fixed-return candidate **failed its predeclared primary improvement criterion**. It prevented observed premature clearing but increased benign alarm time against ordinary fused hysteresis. This result must remain visible in any contribution paper.

| Frozen comparison | Fixed return | Fused hysteresis | Mode hysteresis |
|---|---:|---:|---:|
| Benign alarm points / 59,400 | 2,778 | 2,452 | 6,844 |
| Benign alarm fraction | 4.68% | 4.13% | 11.52% |
| Benign alarm episodes | 41 | 45 | 175 |
| Event overlap / 90 | 90 | 90 | 90 |
| Fresh onset / 90 | 72 | 72 | 72 |
| Events with premature clearing | 0 | 3 | 0 |
| Clear within 5 s / detected-returned | 90/90 | 90/90 | 90/90 |
| Unadjusted command-interval F1 | 0.6496 | 0.6770 | 0.5195 |

The candidate had **13.30% more** benign alarm points than fused hysteresis. It reduced them 59.41% against mode hysteresis; the target required at least 25% reduction against both. Other primary clauses passed. All 18 missing fresh onsets for the candidate were context-gap events; later overlap is not a counted new onset. Its maximum return-relative clearing delay was 0.92 s. All 90 events had evaluator-defined return; this does not certify safety.

## Component findings

At the **same entry threshold**, the candidate had zero premature-clear events, compared with five for ordinary hysteresis, 44 with no dwell and one with no noise margin. Benign alarm points were respectively 2,778, 2,389, 1,813 and 2,486. These diagnostics have different calibration alarm counts (153, 65, 44 and 72); they isolate decision behavior, not equal calibration burden.

Removing reference-based entry, while retaining reference-based recovery, produced exactly the same alarm and unknown arrays in all 144 episodes. The added entry component therefore has no observed decision benefit here. Reference-only entry gave 2,547 benign points and no premature clears. Ordinary following hysteresis achieved F1 0.7954 with 1,529 benign points but cleared prematurely in all 90 events. CUSUM missed nine events and did not clear within the recovery window in any of its 81 detected-returned events.

These are component effects in the specified simulator, not a faithful reproduction of a weakness in CASPER, TWINE or the Edge paper. No new algorithmic novelty is established. Strong controls and negative results are retained in [all-method and plant-stratum tables](TABLES.md).

## Freshness and execution

- Frozen before generation: two new analytic tasks, three independently varied plants, actuator lag/noise changes, three paired noise seeds and eight conditions; 144 episodes, 23 methods, **3,312 outcomes**.
- Ten scientific source/spec files and 809 old inputs bound by `FREEZE.json`; normal thresholds sealed before fresh generation; all scores sealed before joint labels/outcomes.
- Fourteen synthetic tests passed; **14,635 fresh-process checks** passed. Verification includes shared-code replay and separate metric arithmetic, not external replication.
- One successful supervised experiment: **81.959 s wall**, **81.472 s CPU**, **273.05 MiB** peak measured memory, **84.65 MiB** outputs. Caps: 600 s / 300 s / 1 GiB / 160 MiB. No scientific failures or retries.
- Post-exposure presentation and manuscript checks do not change the frozen scientific code, scores, thresholds or primary criterion. PDF build failures are separately preserved.

## Scientific decision

Use the measured recovery trade-off and matched-entry removals in the manuscript. Do not describe the candidate as an overall improvement. The intended original-contribution objective remains active: a specific model-adequacy/recovery mechanism needs distinction from close prior art and fresh virtual confirmation. Independent dynamics simulation and properly admitted public recordings remain feasible evidence routes; physical hardware is not required.

The separate [LaTeX manuscript](../../manuscript_recovery_v0.7/main.tex) and PDF are an author-review draft, not a submission-ready original-method paper. Conditional journal target: ISA Transactions; scope fit and remaining source/author gates are recorded in [source/admission review](SOURCES_AND_ADMISSION.md). The earlier CASPER manuscript/PDF and all scientific freezes remain preserved.
