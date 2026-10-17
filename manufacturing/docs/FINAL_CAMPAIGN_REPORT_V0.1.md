# Protected final campaign and joint analysis

## Material Passport

Manufacturing / Haiqa Mushtaq; 17 October 2026; academic-research-suite bounded execution and statistical-interpretation guidance. Verification: **all eleven declared deterministic methods completed scoring and evaluation; complete saved-score arithmetic audit passed**. This is an internal single-acquisition CASPER case study, not a paper-baseline reproduction, independent replication or external peer review. Actual artifacts and revisions are in the [completion record](../experiments/FINAL_CAMPAIGN_V0.1_RECORD.json).

## Main conclusion

Adding correction discrepancy gave a **small descriptive improvement** over the otherwise identical residual score, but the campaign does **not establish a useful general digital-twin detector or strong attack detection**. O-RC's unadjusted F1 was **0.017292** and point recall **0.008805**—only **0.8805%** of schedule-positive observations alarmed. No method exceeded **4.0217% point recall** at its frozen threshold. The ordinary controls match or exceed several observer outcomes, with different false-alarm trade-offs.

The primary contrast is **O-RC minus O-R**, not a progression-present versus progression-absent experiment. Both retain nominal progression and share the same state/predictions. These results answer whether the **correction-score term** helped; they do not independently identify a causal benefit of progression itself.

No model, feature, seed, threshold, percentile, mask or score combination was changed after the freeze. No new winner-selection rule was introduced. The holdout is now exposed: any redesign motivated by these findings is exploratory and needs suitable fresh evidence for a new confirmatory claim.

## Execution, provenance and outcome release

The latest user request [explicitly authorized](../experiments/FINAL_CAMPAIGN_EXECUTION_AUTHORIZATION_V0.1.json) the previously frozen final commands/budgets. The [pre-execution freeze](../experiments/FINAL_TEST_FREEZE_RECORD.json) remains unchanged, including its historical not-started fields. The separate [completion record](../experiments/FINAL_CAMPAIGN_V0.1_RECORD.json) carries actual starts, completion, artifact hashes and all eleven terminal rows. Source/configuration bytes are the same **52 tested files** covered by **324 passing synthetic tests**; all **133 frozen input bindings** remain intact. No new fit or stochastic replicate was run. Seeds 17/42/2026 remain an unused policy here because every method is deterministic.

- Final scoring started `2026-10-17T06:21:17.705600+00:00` and was accepted at `2026-10-17T06:25:51.061961+00:00`. It continuously replayed `[864003,1762650)` and sealed **897,119 scores per method**, **9,868,309 scores total**, plus all raw coordinates. Fitted parameters were unchanged. No labels were parsed by the scorer, and only the initial/common warmup reset occurred.
- The evaluator was admitted after that complete score seal; label joining began `2026-10-17T06:26:30.415287+00:00`. All timestamp/label coordinates and eight annotation runs were validated. First outcome-write intent was logged at `2026-10-17T06:26:42.693518+00:00`; this is conservative local artifact exposure, not an assertion that a person read it.
- Every method's evaluation completed at `2026-10-17T06:27:12.073582+00:00`. Joint results were inspected only after all methods were terminal. **One scoring attempt and one evaluation attempt, both accepted; zero failed final attempts or retries.** No early result altered any remaining execution.
- Scoring manifest SHA-256: `d201971ea12f472ff38feabbe41a53efcc89aca0046c9bf3388a5ebeeebab521`. Evaluation manifest SHA-256: `cfac9bc0b58223a554c2bbf170eefa6a0da1f7ffb75f82e56600280f623c251f`. These receipts bind exact commands, interpreter/dependencies/hardware, source snapshot, configuration, thresholds, raw identity, source checks, masks, logs and artifact bytes.

Raw data was opened read-only and checked before/after both phases. No system packages, skill files, sibling-project datasets or frozen implementations were changed, and nothing was uploaded, published, committed or pushed by this task.

## Complete method comparison

All figures below use the frozen nearest-rank 99% normal calibration and strict `score > threshold`. P/R/F1/AP are fractions in `[0,1]`; normal point alarms are percentages. No point adjustment, persistence, cooldown, test-selected operating point or incomplete support trimming was applied. Methods remain in declared order.

| Method | Precision | Point recall | F1 | Average precision | Normal point alarms | Normal episodes / eligible h | Event overlap | Fresh onset |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| O-R | 0.4659 | 0.008452 | 0.016603 | 0.506108 | 1.0067% | 189.34 | 7/8 | 7/8 |
| O-RC | 0.4785 | 0.008805 | 0.017292 | 0.506414 | 0.9941% | 185.98 | 8/8 | 8/8 |
| O-C | 0.5092 | 0.009705 | 0.019047 | 0.506135 | 0.9861% | 342.76 | 8/8 | 8/8 |
| O-K | 0.5058 | 0.009777 | 0.019183 | 0.506193 | 0.9917% | 349.47 | 8/8 | 8/8 |
| O-L | 0.4659 | 0.008513 | 0.016720 | 0.506284 | 1.0053% | 189.34 | 7/8 | 7/8 |
| O-Rv | 0.4655 | 0.008446 | 0.016591 | 0.502845 | 1.0048% | 189.34 | 7/8 | 7/8 |
| O-Follow | 0.4656 | 0.008368 | 0.016441 | 0.504844 | 1.0043% | 189.34 | 7/8 | 7/8 |
| O-Free | 0.4664 | 0.008461 | 0.016620 | 0.506295 | 0.9964% | 189.34 | 7/8 | 7/8 |
| V-Z | 0.4622 | 0.008414 | 0.016528 | 0.506759 | 0.9969% | 189.34 | 7/8 | 7/8 |
| T-32 | 0.5277 | 0.040217 | 0.074737 | 0.490596 | 1.3997% | 200.42 | 8/8 | 8/8 |
| AR-4 | 0.5006 | 0.009604 | 0.018846 | 0.507711 | 0.9833% | 437.09 | 8/8 | 8/8 |

The mixed slice contains **345,602 positive / 337,044 zero observations**, so scheduled-positive prevalence is **50.6268%**. A constant tied score has AP equal to that prevalence by the defined formula; this is an arithmetic reference, not an added evaluated detector. Observed AP ranges from **0.490596 to 0.507711**, close to that reference. Small decimal differences do not establish reliable ranking or practical generalization. Precision is tied to this artificial schedule prevalence, not an estimated field cyberattack rate.

O-R/O-RC are normalized residual and residual-plus-JS; O-C is JS alone; O-K is KL surprise; O-L is predictive mixture energy; O-Rv uses only velocity residual from the same full observer. O-Follow and O-Free change state correction as frozen; V-Z is maximum standardized velocity deviation; T-32 is the fixed 32-bin periodic template; AR-4 is the ordinary channelwise autoregression. Formulas and artifact identities remain in the [campaign configuration](../configs/casper_right_arm_campaign_v0.1.json).

## Counts, normal burden and coverage

| Method | TP | FP | FN | TN | Normal alarm points | Normal episodes | Mixed scheduled-zero alarms |
|---|---:|---:|---:|---:|---:|---:|---:|
| O-R | 2,921 | 3,349 | 342,681 | 333,695 | 2,159 / 214,473 | 564 | 0.9936% |
| O-RC | 3,043 | 3,317 | 342,559 | 333,727 | 2,132 / 214,473 | 554 | 0.9841% |
| O-C | 3,354 | 3,233 | 342,248 | 333,811 | 2,115 / 214,473 | 1,021 | 0.9592% |
| O-K | 3,379 | 3,301 | 342,223 | 333,743 | 2,127 / 214,473 | 1,041 | 0.9794% |
| O-L | 2,942 | 3,373 | 342,660 | 333,671 | 2,156 / 214,473 | 564 | 1.0008% |
| O-Rv | 2,919 | 3,352 | 342,683 | 333,692 | 2,155 / 214,473 | 564 | 0.9945% |
| O-Follow | 2,892 | 3,320 | 342,710 | 333,724 | 2,154 / 214,473 | 564 | 0.9850% |
| O-Free | 2,924 | 3,345 | 342,678 | 333,699 | 2,137 / 214,473 | 564 | 0.9925% |
| V-Z | 2,908 | 3,383 | 342,694 | 333,661 | 2,138 / 214,473 | 564 | 1.0037% |
| T-32 | 13,899 | 12,441 | 331,703 | 324,603 | 3,002 / 214,473 | 597 | 3.6912% |
| AR-4 | 3,319 | 3,311 | 342,283 | 333,733 | 2,109 / 214,473 | 1,302 | 0.9824% |

All confusion totals equal **682,646 mixed observations**. All methods have **100% eligible coverage** and **no missing/nonfinite scores**. Complete-final raw coverage is **99.829967%** (897,119 / 898,647); the only 1,528 exclusions are the shared initial warmup. Normal raw coverage is **99.292596%**; mixed coverage is 100%. Missing observations did not explain or inflate the weak recall.

Protected-normal exposure is exactly **10,723.60000000003 native seconds** (about **2.97878 eligible hours**) for every method, using adjacent eligible timestamps rather than a nominal rate. Normal episode censoring and report-boundary crossing counts are zero for every method. An episode is a contiguous observed alarm run, not an independent security incident. O-RC's **554 episodes** correspond to **185.98 per eligible hour**, despite its point alarm fraction being near 1%. The calibration percentile did not promise a low episode-arrival burden.

## Primary paired result and ordinary controls

Against O-R, O-RC had **122 more TP, 32 fewer mixed FP, 27 fewer normal alarm points and 10 fewer normal episodes**. F1 changed by **+0.0006890112** (about **+0.0689 percentage points**); normal point alarm fraction changed by **−0.0001258900** (−0.012589 percentage points), and normal episode rate by **−3.3571/hour**. Both retain full coverage. The added term did help these recorded paired outcomes slightly, without higher measured normal alarm burden. Its absolute recall and F1 remain poor; this is not a broad superiority claim.

The ordinary **AR-4** achieved higher F1 (**0.018846**) and AP (**0.507711**) than O-RC, with slightly fewer normal alarm points (**2,109 versus 2,132**). It produced many more normal episodes (**1,302 versus 554**). Thus it does not dominate every operational outcome. The ordinary **T-32** attained the largest F1 (**0.074737**) and recall (**4.0217%**), but normal point alarms rose to **1.3997%** and mixed scheduled-zero alarms to **3.6912%**; its AP was **0.490596**. Its larger F1 cannot be presented without those costs.

**V-Z** and the same-observer velocity residual **O-Rv** produced very similar recorded outcomes to the full residual; unconstrained and free-running residual variants were also close, and all six missed event 5. These observations do not demonstrate that synchronization/progression adds useful detection value beyond simple alternatives. They are descriptive similarities, not a statistical equivalence test or causal explanation of the scores. The free-running observer's documented diffusion toward a nearly uniform state remains a limitation of that comparison.

Correction-only JS/KL scores attained slightly higher F1 than O-RC, but **342.76 / 349.47 normal episodes per hour**, versus **185.98** for O-RC. There is no declared scalar utility that turns these mixed outcomes into one global winner.

## Every event, including misses and fresh onsets

In this campaign **none of the 88 method/event starts had a pre-existing alarm**, and every observed overlap hit also had a fresh onset. Consequently overlap and fresh-onset delays happen to coincide. The two definitions were still evaluated separately; this coincidence must not become an assumption in other data. A sustained pre-existing alarm was not counted as fresh by the software.

The table gives **schedule-relative fresh/overlap delay in seconds** for every declared method and every interval. `MISS` remains in the denominator and is not zero delay. Display rounds to two decimals; exact native strings and row identities are retained in the artifacts and [88-row event export](../experiments/FINAL_CAMPAIGN_V0.1_EVENTS.csv). These are delays from the recorded flag, not independently established physical attack onset.

| Method | Event 1 | Event 2 | Event 3 | Event 4 | Event 5 | Event 6 | Event 7 | Event 8 | Misses / 8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| O-R | 9.70 | 3.45 | 10.10 | 8.85 | MISS | 4.60 | 29.00 | 12.05 | 1 |
| O-RC | 9.70 | 3.45 | 10.10 | 8.85 | 9.20 | 6.65 | 29.05 | 12.05 | 0 |
| O-C | 9.25 | 3.00 | 9.65 | 8.40 | 6.25 | 4.15 | 1.85 | 9.45 | 0 |
| O-K | 9.25 | 3.00 | 9.65 | 8.40 | 6.25 | 4.10 | 1.85 | 9.45 | 0 |
| O-L | 9.70 | 3.45 | 10.10 | 8.85 | MISS | 4.60 | 29.00 | 12.05 | 1 |
| O-Rv | 9.70 | 3.45 | 10.10 | 8.85 | MISS | 4.60 | 29.00 | 12.05 | 1 |
| O-Follow | 9.70 | 3.45 | 10.10 | 8.85 | MISS | 4.55 | 29.00 | 12.10 | 1 |
| O-Free | 9.70 | 3.45 | 10.10 | 8.85 | MISS | 4.60 | 29.00 | 12.10 | 1 |
| V-Z | 9.70 | 3.40 | 10.10 | 8.85 | MISS | 4.55 | 29.00 | 12.10 | 1 |
| T-32 | 9.65 | 3.30 | 9.95 | 8.60 | 9.05 | 4.40 | 28.85 | 9.75 | 0 |
| AR-4 | 9.80 | 3.55 | 10.20 | 8.95 | 8.80 | 4.70 | 28.35 | 11.70 | 0 |

| Method | Delays defined / all events | Misses | Detected-only median, s | Detected-only range, s |
|---|---:|---:|---:|---:|
| O-R | 7/8 | 1 | 9.70 | 3.45–29.00 |
| O-RC | 8/8 | 0 | 9.45 | 3.45–29.05 |
| O-C | 8/8 | 0 | 7.33 | 1.85–9.65 |
| O-K | 8/8 | 0 | 7.33 | 1.85–9.65 |
| O-L | 7/8 | 1 | 9.70 | 3.45–29.00 |
| O-Rv | 7/8 | 1 | 9.70 | 3.45–29.00 |
| O-Follow | 7/8 | 1 | 9.70 | 3.45–29.00 |
| O-Free | 7/8 | 1 | 9.70 | 3.45–29.00 |
| V-Z | 7/8 | 1 | 9.70 | 3.40–29.00 |
| T-32 | 8/8 | 0 | 9.35 | 3.30–28.85 |
| AR-4 | 8/8 | 0 | 9.38 | 3.55–28.35 |

O-RC adds an event-5 hit at **9.20 s**, where O-R has no alarm anywhere in the interval. For the **seven events both hit**, their first delays are identical for five events; O-RC is **2.05 s later** on event 6 and approximately **0.05 s later** on event 7. It is not earlier on any shared detected interval. Comparing its eight-event median of 9.45 s with O-R's seven-event median of 9.70 s would therefore not establish faster matched detection.

High event-hit counts coexist with very sparse point coverage inside events. All intervals are fully scored; the O-RC detail is:

| Event | Source rows, half-open | Eligible observations | Alarm observations | Within-event point recall | Overlapping alarm episodes |
|---|---|---:|---:|---:|---:|
| 1 | [1080004, 1123205) | 43,201 | 432 | 1.0000% | 110 |
| 2 | [1166405, 1209605) | 43,200 | 445 | 1.0301% | 115 |
| 3 | [1252805, 1296005) | 43,200 | 441 | 1.0208% | 116 |
| 4 | [1339205, 1382405) | 43,200 | 432 | 1.0000% | 113 |
| 5 | [1425606, 1468806) | 43,200 | 143 | 0.3310% | 49 |
| 6 | [1512006, 1555206) | 43,200 | 376 | 0.8704% | 57 |
| 7 | [1598406, 1641606) | 43,200 | 412 | 0.9537% | 105 |
| 8 | [1684806, 1728007) | 43,201 | 362 | 0.8379% | 55 |

Each long interval contains over 43,000 positive observations. Any single alarm suffices for overlap recall. O-RC's eight hits and short first-alarm delays therefore cannot conceal its **342,559 false-negative positive observations**, high normal episode rate and near-prevalence AP. This is evidence of a weak operating point, not sustained reliable recognition of the scheduled changes. Full episode identifiers, source bounds and censoring flags for every method/event are preserved in the hashed local `saved_results_audit.json` referenced by the completion record.

## Scheduled-zero recovery and inter-event burden

Recovery flags denote scheduled-zero observations, not independently certified healthy operation. The eight columns below follow the eight predefined zero-labelled intervals: after event 1/before event 2 through after event 7/before event 8, then after event 8. Values are **alarm points / eligible observations**. Full boundaries, exposure, episode rates and censoring for all **88 method/slice combinations** are in the [recovery export](../experiments/FINAL_CAMPAIGN_V0.1_RECOVERY.csv).

| Method | Zero 1 | Zero 2 | Zero 3 | Zero 4 | Zero 5 | Zero 6 | Zero 7 | Zero 8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| O-R | 419/43,200 | 437/43,200 | 426/43,200 | 432/43,201 | 427/43,200 | 435/43,200 | 434/43,200 | 339/34,643 |
| O-RC | 421/43,200 | 432/43,200 | 427/43,200 | 422/43,201 | 422/43,200 | 430/43,200 | 423/43,200 | 340/34,643 |
| O-C | 418/43,200 | 425/43,200 | 422/43,200 | 423/43,201 | 401/43,200 | 408/43,200 | 408/43,200 | 328/34,643 |
| O-K | 429/43,200 | 429/43,200 | 425/43,200 | 435/43,201 | 408/43,200 | 417/43,200 | 420/43,200 | 338/34,643 |
| O-L | 422/43,200 | 435/43,200 | 427/43,200 | 430/43,201 | 433/43,200 | 440/43,200 | 440/43,200 | 346/34,643 |
| O-Rv | 419/43,200 | 435/43,200 | 427/43,200 | 433/43,201 | 427/43,200 | 436/43,200 | 434/43,200 | 341/34,643 |
| O-Follow | 417/43,200 | 428/43,200 | 426/43,200 | 428/43,201 | 425/43,200 | 425/43,200 | 430/43,200 | 341/34,643 |
| O-Free | 424/43,200 | 433/43,200 | 429/43,200 | 425/43,201 | 428/43,200 | 436/43,200 | 432/43,200 | 338/34,643 |
| V-Z | 425/43,200 | 435/43,200 | 442/43,200 | 438/43,201 | 425/43,200 | 432/43,200 | 437/43,200 | 349/34,643 |
| T-32 | 1,314/43,200 | 1,329/43,200 | 2,018/43,200 | 1,302/43,201 | 1,363/43,200 | 1,296/43,200 | 2,419/43,200 | 1,400/34,643 |
| AR-4 | 418/43,200 | 418/43,200 | 435/43,200 | 426/43,201 | 430/43,200 | 428/43,200 | 423/43,200 | 333/34,643 |

## Measured resources and cost limits

| Phase | Supervised wall, s | Worker CPU, s | Peak worker RSS, MiB | Outputs including manifest, MiB |
|---|---:|---:|---:|---:|
| score-final | 270.890 | 270.520 | 143.19 | 102.317 |
| evaluate-final | 44.778 | 44.660 | 902.50 | 0.188 |

Both phases remained within their frozen caps (scoring 900 s wall / 600 s CPU, evaluation 1,800 s / 1,200 s; both 1 GiB worker RSS and 256 MiB output). Hardware and environment are unchanged: local Apple M5 Pro, 24 GiB host memory, manufacturing Python 3.15.0 venv, standard library, one CPU worker. Scoring's **0.301442 ms per input observation** is a coarse **whole-worker average including source checks, positioning/parsing, warmup, all methods, writes and supervision**. It is not isolated inference latency, a per-record percentile, transport latency or physical detection delay.

The frozen runner did not instrument isolated per-method processing, initialization/IO decomposition or per-record median/p95. Those finer cost measurements are unavailable; this reporting limitation prevents claiming that the small correction-score gain is computationally free, more expensive by a measured amount, or cheaper than a control. The whole-roster execution is locally feasible under its limits; live deployment is not demonstrated.

## Verification and interpretation checks

The separate saved-result audit rehashed every score/metric artifact and all frozen inputs, checked all native coordinates/masks, reconstructed thresholds' decisions, recomputed all confusion/AP/normal/recovery/episode/event outputs, and checked the primary paired differences. It used **no raw dataset opens and no detector replay**. Its **2,699,097 assertions include per-row clock/mask checks**, not independent experiments. Seven hand-checkable synthetic arithmetic examples preceded it. The audit itself took **5.033 s**, **279.83 MiB** peak RSS, with a preserved accepted supervisor receipt. Labels for this extra arithmetic check were reconstructed from the frozen schedule after the actual evaluator had verified the original labels; it is not an independent raw-label reannotation.

| Interpretation check | Disposition |
|---|---|
| Simpson's paradox / hidden aggregation | All methods, eight events and eight zero intervals retained; normal and mixed populations separate. Aggregate F1 is not a claim about every interval. |
| Ecological fallacy | Rows, alarms and intervals are not robots or independent installations. |
| Berkson/selection bias | One selected repetitive acquisition; no representative field-sampling claim. |
| Collider bias | No post-score success filter, favorable intersection or outcome-conditioned subgroup admission. |
| Base-rate neglect | Mixed prevalence 50.6268% explicitly reported; precision does not transfer to field attack prevalence. |
| Regression to the mean | No pre/post improvement study, extreme-run selection or follow-up regression claim. |
| Survivorship bias | All eleven runs and eight events per method retained; zero failed final attempts; misses remain explicit. |
| Look-elsewhere effect | Primary contrast fixed; all secondary variants shown; no p-value or post-hoc winner claim. |
| Forking paths | Artifact/configuration/metric freeze predates exposure; no test-tuned thresholds or scientific changes. |
| Correlation versus causation | Descriptive score ablation on one recording; no causal cyber/physical protection claim. |
| Reverse causality / future leakage | Scores emitted before state commit; labels joined only after all streams seal; no attack prediction or pre-onset causation claim. |

No confidence intervals or significance tests treat adjacent rows, eight dependent intervals or seeds as independent robot experiments. No stochastic variability is estimated because all methods are deterministic. Dataset schedule flags do not establish malicious intent, fault/attack separation, authenticated telemetry or exact physical onset.

## What this supports, and the next research decision

The supported conclusion is a **small within-recording correction-score effect with poor absolute detection**, plus a clear demonstration that event overlap must be interpreted alongside point recall and normal alarm burden. Ordinary controls provide strong reasons to withhold a general detector-superiority or digital-twin claim. This does not establish novelty or leading-journal readiness.

Preserve this complete negative/mixed result. The next useful work is an author-understood limitations/methods/results draft and a separate plan for independent evidence and any proposed redesign. New annotation investigations, different features, persistence rules, thresholds, models or preferred variants motivated by these outcomes must be labelled **exploratory**. A repeat or reshuffle of this recording does not create a fresh confirmatory test. No such redesign, extra training or new data collection occurred here.

Exact completed commands (cwd: manufacturing):

```text
.venv/bin/python scripts/run_campaign.py --check-final
.venv/bin/python scripts/run_campaign.py --score-final
.venv/bin/python scripts/run_campaign.py --evaluate-final --score-run experiments/runs/campaign_v0.1_score-final_2026-10-17T062117.703085_0000
.venv/bin/python local/final_campaign_v0.1/review/audit_results.py --selftest
.venv/bin/python local/final_campaign_v0.1/review/run_audit.py
.venv/bin/python local/final_campaign_v0.1/review/build_report.py
```

The one-attempt records remain consumed. [All-method CSV](../experiments/FINAL_CAMPAIGN_V0.1_METRICS.csv), [complete event CSV](../experiments/FINAL_CAMPAIGN_V0.1_EVENTS.csv), [complete recovery CSV](../experiments/FINAL_CAMPAIGN_V0.1_RECOVERY.csv), [machine-readable summary](../experiments/FINAL_CAMPAIGN_V0.1_SUMMARY.json) and [completion record](../experiments/FINAL_CAMPAIGN_V0.1_RECORD.json) retain the full comparison, not only the main pair.
