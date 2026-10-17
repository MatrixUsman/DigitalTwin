# Normal-only reference adequacy results

17 October 2026. All observations are synthetic. This study uses commissioning and normal operation only; no attack experiment or attack recovery claim. AFTER remains a proposed title.

## Outcome

The normal-only search selected ARX orders 8, 16 and 32 for Q1, Q2 and Q3 respectively (ridge 1e-7). All improve the matched ARX(4) normal prediction error. Q2 changes from an infeasible allowance to 108/108 normal clearing opportunities. The overall normal-admission criterion still fails: Q2 has 93.32% eligible points satisfying the inequality (required 95%); Q3 retains an allowance above the 0.1 tolerance. These are normal forced-latch diagnostics, not detected attacks or physical recovery events.

## Selected references versus matched ordinary control

Both references use the same 100-observation initialization, training-only scales and three commissioning episodes. The same ARX(4) coefficients match the old saved fit exactly. The allowance here uses five normal episodes, not v0.8's nineteen; compare the paired columns here, not different-cycle allowance numbers.

| Plant | Selected order | ARX(4) allowance | Selected allowance | Allowance decrease | ARX(4) mean RMSE | Selected mean RMSE | Selected feasible normal points | Normal clearances | Admission |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Q1 | 8 | 0.055330 | 0.055298 | 0.06% | 0.009477 | 0.009337 | 99.82% | 108/108 | Pass |
| Q2 | 16 | 0.146910 | 0.071592 | 51.27% | 0.010203 | 0.009716 | 93.32% | 108/108 | Fail |
| Q3 | 32 | 0.191250 | 0.117495 | 38.56% | 0.015865 | 0.014388 | 0.00% | 0/108 | Fail |

RMSE is standardized across four state channels and averaged over episodes. Every plant has 29,700 fresh eligible observations and 108 probe starts. A probe forces an active diagnostic latch and checks ten consecutive qualifying observations within five seconds. It ignores alarm entry priority and cannot establish attack sensitivity.

## All roles on fresh normal conditions

| Plant | Role | Model | Allowance | Worst episode q99 error | Feasible fraction | Cleared/probes |
|---|---|---|---:|---:|---:|---:|
| Q1 | baseline_arx4 | arx_04_1e-07 | 0.055330 | 0.041611 | 99.80% | 108/108 |
| Q1 | command | command | 2.134352 | 1.938681 | 0.00% | 0/108 |
| Q1 | one_step_arx4 | arx_04_1e-07 | 0.064907 | 0.044025 | 97.92% | 108/108 |
| Q1 | selected_arx | arx_08_1e-07 | 0.055298 | 0.040612 | 99.82% | 108/108 |
| Q1 | selected_fir | fir_64_1e-07 | 0.232232 | 0.155549 | 0.00% | 0/108 |
| Q1 | selected_reference | arx_08_1e-07 | 0.055298 | 0.040612 | 99.82% | 108/108 |
| Q2 | baseline_arx4 | arx_04_1e-07 | 0.146910 | 0.071718 | 0.00% | 0/108 |
| Q2 | command | command | 2.152846 | 1.936556 | 0.00% | 0/108 |
| Q2 | one_step_arx4 | arx_04_1e-07 | 0.121143 | 0.050419 | 0.00% | 0/108 |
| Q2 | selected_arx | arx_16_1e-07 | 0.071592 | 0.063822 | 93.32% | 108/108 |
| Q2 | selected_fir | fir_64_1e-07 | 0.397098 | 0.280878 | 0.00% | 0/108 |
| Q2 | selected_reference | arx_16_1e-07 | 0.071592 | 0.063822 | 93.32% | 108/108 |
| Q3 | baseline_arx4 | arx_04_1e-07 | 0.191250 | 0.121482 | 0.00% | 0/108 |
| Q3 | command | command | 2.205772 | 2.036618 | 0.00% | 0/108 |
| Q3 | one_step_arx4 | arx_04_1e-07 | 0.180728 | 0.069546 | 0.00% | 0/108 |
| Q3 | selected_arx | arx_32_1e-07 | 0.117495 | 0.102382 | 0.00% | 0/108 |
| Q3 | selected_fir | fir_64_1e-07 | 0.459578 | 0.274918 | 0.00% | 0/108 |
| Q3 | selected_reference | arx_32_1e-07 | 0.117495 | 0.102382 | 0.00% | 0/108 |

The selected reference equals the selected ARX on every plant; those duplicated roles are not independent methods or corroboration. FIR(64), selected from nine FIR configurations per plant, is worse in this search. One-step ARX uses measured history and is not a free reference. The command-as-state control is deliberately simple.

## Sensor-noise diagnostic

This analysis was added after the normal results and changes no consumed choice. For a hypothetical perfect reference, use the declared independent Gaussian noise and fixed training scales. Let F be the CDF of the maximum absolute standardized sensor noise. The empirical maximum B from 5,500 allowance points has CDF F(b)^5500. A future population feasibility of at least 95% requires B <= 0.1 - F^-1(0.95).

| Plant | Single-point noise q95 | Maximum allowance compatible with 95% population feasibility | Probability that noise-only calibration leaves that margin |
|---|---:|---:|---:|
| Q1 | 0.028251 | 0.071749 | 0.999828 |
| Q2 | 0.027914 | 0.072086 | 0.999897 |
| Q3 | 0.041737 | 0.058263 | 2.18584e-09 |

For Q3 this probability is about 2.19e-9 even with a perfect reference. This is a conditional Gaussian calculation, not a measured probability across robots, a general impossibility theorem or proof about arbitrary noise. It shows why reducing model error alone is insufficient for this particular maximum-plus-discrepancy rule. Ordinary noise-aware estimation/testing is established prior art; the calculation itself is not a novel algorithm. Independent numerical implementations agree.

## Execution and limitations

- 63 candidate fits: 21 per plant; 0 rejected/failed candidates. Nine development episodes per plant selected models; five estimated allowances; five archived episodes checked them.
- 81 newly generated normal episodes, plus fifteen archived checks; six recorded roles and 576 outcomes, including duplicated selected-reference/ARX roles. No attack observations were loaded for model fitting or generation.
- Twenty-three pre-run synthetic tests passed after one test-exception correction. The reporting retry has one additional merge regression. Post-run verification passed 10,293 checks, including exact refitting, selection, predictions, independent clearance arithmetic and admission.
- Completed run: 14.748 s wall, 14.296 s CPU, 113.97 MiB sampled RSS, 117.66 MiB worker peak, 28.02 MiB outputs.
- The first attempt stopped on a duplicate reporting key after selection, before fresh generation (2.603 s wall / 2.278 s CPU). It is preserved. A separately versioned reporting fix verified byte-identical fit files and identical scientific candidate/selection records before proceeding. No scientific retry or changed configuration.
- Existing Q1/Q2/Q3 plants, controller, simulator and noise assumptions; dependent seeds. New command conditions are not independent physical acquisitions. Old normal data were reused with explicitly recorded roles, not relabeled unseen evidence.
- ARX/FIR model selection is ordinary system identification. Full recent paper-level reproductions, a distinct new mechanism and author approval remain unresolved. This study is complete as normal-only development and is not a journal-readiness decision.

[Finite plan](PLAN.md) · [prior art](PRIOR_ART.md) · [verification](VERIFICATION.json) · [noise calculation](NOISE_DIAGNOSTIC.json) · [next mechanism requirements](DECISION.md).
