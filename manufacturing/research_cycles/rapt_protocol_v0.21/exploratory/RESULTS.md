# RAPT transfer replay: completed exploratory evidence

The released RAPT detector now has a measured transfer result on the complete exposed Q1 simulation grid. Its conditional prediction scores did not reliably represent continuing deviation from the protected command trajectory. This observation concerns our transferred task; RAPT's paper does not claim a physical-recovery guarantee, and this experiment does not refute its humanoid OOD results.

## What ran

The single fitted Q1/seed17 checkpoint selected at normal-development epoch 14 was loaded without modification. K13 training statistics and L13 calibration stayed fixed. All 36 existing episodes were scored, using both released model-only and hybrid gates, before any evaluator-only truth was opened. There were 129,600 input rows, 126,000 eligible rows, 12 benign episodes and 24 intervention episodes. All observations are synthetic and the grid was already exposed in v0.19. Nothing was trained, recalibrated or newly confirmed here.

Both modes produced identical risk series and decisions on this population. The range gate added no detections.

| Quantity | Both fixed modes |
|---|---:|
| Events detected / total | 9 / 24 |
| Fresh event detections / total | 9 / 24 |
| Missed events | 15 |
| Benign point alarms | 5,175 / 70,800 (7.309%) |
| Benign alarm starts | 109 over 0.3933 eligible hours (277.12/hour) |
| Unadjusted precision / recall / F1 | 0.11028 / 0.10026 / 0.10503 |
| Average precision | 0.10961 |
| Inactive while physically outside the declared tolerance | 9,448 / 10,689 points (88.390%) |
| Detection delay among the nine detected events | median 0.02 s; maximum 4.66 s |
| Detected events with an alarm fall before physical return | 9 / 9 |

Normal episodes contributed 2,483 alarms over 35,400 eligible points; authorized-change episodes contributed 2,692 over 35,400. Fifteen misses remain outside the nine-event delay denominator. All 24 physical returns were observed under the fixed evaluator; nine detected events became inactive within five seconds of return, six of them already inactive at return. That last number must not be interpreted as successful recovery recognition.

## Brief versus persistent deviation

The table reports the median across three simulation seeds of each episode's first- or last-quarter median risk. Alarm threshold is strictly greater than 1. Every condition is shown, including the cases that do not support a simple “risk always decays” account. Quarter definitions were frozen before replay.

| Task | Intervention | Fresh detections | First-quarter risk | Last-quarter risk | Inactive / outside points in last quarter |
|---|---|---:|---:|---:|---:|
| L19 | Brief offset | 3/3 | 2.553 | 4.078 | 0/9 |
| L19 | Persistent offset | 3/3 | 1.248 | 0.807 | 396/396 |
| L19 | Hold | 0/3 | 0.401 | 0.446 | 396/396 |
| L19 | Slow | 3/3 | 0.364 | 0.531 | 396/396 |
| S19 | Brief offset | 0/3 | 0.166 | 0.058 | 6/6 |
| S19 | Persistent offset | 0/3 | 0.110 | 0.028 | 351/351 |
| S19 | Hold | 0/3 | 0.043 | 0.039 | 351/351 |
| S19 | Slow | 0/3 | 0.035 | 0.095 | 351/351 |

For L19 persistent offsets, the detector initially reacts and later becomes inactive while motion remains outside the protected reference tolerance. For S19, even the first-quarter risk is low and all interventions are missed. These are two different behaviors. Task transfer, the fitted conditional dynamics, predictive variance and conservative calibration could all contribute; the experiment does not isolate a causal explanation. The network's parameters remain fixed throughout, so this is not evidence that online parameter training absorbed an attack. Its recurrent state and previous-observation conditioning continue during replay.

## Scope and comparison limits

This is a complete execution of the released detector core with a transferred input and training protocol. Its four observations and four protected desired-motion inputs replace the original humanoid observation/action interface; desired motion is not an authenticated measured motor torque or the original policy output. The baseline is a verified preprint, not a confirmed peer-reviewed publication. The source audit also records differences between the paper formulas and released scoring/gating code. We preserve the code's behavior. Primary sources are the [RAPT v2 manuscript](https://arxiv.org/html/2602.01515v2) and [author repository](https://github.com/csiro-robotics/RAPT).

The existing v0.19 ARX controls were fitted in earlier commissioning cycles; RAPT uses K13/M13/L13. They therefore do not form a common-training superiority table here. One trained seed and one simulated plant do not establish generalization to robots, real faults, maliciously forged sensors or additional training seeds. Replaying an exposed grid is exploratory even when the new checkpoint and scoring rules were frozen beforehand.

The useful finding is a concrete distinction between predicting the next observed state and retaining evidence that motion remains inconsistent with protected intent. Any proposed improvement must address that distinction while also reducing benign alarms, use comparable commissioning data, and show value beyond ordinary reference observers and accumulation/reset controls. These results do not supply that improved mechanism or establish originality.

## Provenance and verification

Exact commands, run from `manufacturing/`:

```
.venv-forecast-v016/bin/python -m unittest discover -s research_cycles/rapt_protocol_v0.21/exploratory -p 'test_*.py' -v
.venv-forecast-v016/bin/python research_cycles/rapt_protocol_v0.21/exploratory/run.py
.venv-forecast-v016/bin/python research_cycles/rapt_protocol_v0.21/exploratory/verify.py
```

Six synthetic checks passed. The single monitored replay completed in 4.023 seconds wall and 3.688 CPU; inference accounted for 2.420 seconds. Peak worker RSS was 409,190,400 bytes (390.23 MiB); complete output size was 2,679,443 bytes. All limits remained enforced: 120 seconds wall, 90 CPU, 1 GiB RSS and 50 MiB output. No failed attempt or retry occurred.

`FREEZE.json` binds 243 identities; SHA-256 is `35619d5219b2296e141f1262038bff521ba08b8f659d2f4b064fe7098f25ff43`. `SCORES_SEALED.json` records all 36 score hashes before the truth join. A fresh process replayed the checkpoint for all 36 episodes and recovered every saved per-channel score, risk and decision exactly; 708 checks passed, including unchanged inputs and access ordering. `VERIFICATION.json` hashes the complete run outputs. The separate independent review passed 3,920 checks, reconstructing gates and all reported metrics without importing the evaluation helpers. Access ordering is supported by the source and recorded ledger, not an independent operating-system trace.

Artifacts: `local/rapt_protocol_v0.21/exploratory_Q1_001/`, including all 72 mode outputs, per-episode outcomes, summaries, timings, provenance, access record and terminal resource receipt. The original normal-run freeze, v0.19 package and manuscripts remain unchanged.
