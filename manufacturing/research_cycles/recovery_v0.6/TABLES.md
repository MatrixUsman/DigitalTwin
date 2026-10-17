# All declared results — generated from saved artifacts

Synthetic results. AP ranks unknown observations last; F1 uses every eligible attack target. Benign alarms exclude attack-containing episodes.

## within_range

| Method | Benign alarms / points | Alarm episodes/h | Recall | F1 | AP | Events hit | Fresh hits | Early-clear events | Cleared ≤5s / returned detected |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Persistence | 236/32400 | 405.56 | 3.45% | 0.0572 | 0.1060 | 43/60 | 43/60 | 43 | 43/43 |
| AR(4) | 205/32400 | 550.00 | 2.85% | 0.0480 | 0.1866 | 55/60 | 55/60 | 55 | 55/55 |
| ARX(4) | 1077/32400 | 4127.78 | 88.49% | 0.7876 | 0.7139 | 60/60 | 51/60 | 60 | 60/60 |
| Following error | 652/32400 | 1744.44 | 92.03% | 0.8396 | 0.9216 | 60/60 | 48/60 | 60 | 60/60 |
| Following mean (45) | 301/32400 | 105.56 | 91.21% | 0.7809 | 0.7644 | 60/60 | 48/60 | 51 | 60/60 |
| Following CUSUM | 4035/32400 | 61.11 | 87.78% | 0.3519 | 0.1476 | 48/60 | 36/60 | 0 | 0/48 |
| Fused error | 288/32400 | 394.44 | 91.80% | 0.7575 | 0.8304 | 60/60 | 48/60 | 60 | 60/60 |
| Fused hysteresis | 354/32400 | 100.00 | 91.72% | 0.7278 | 0.8304 | 60/60 | 48/60 | 4 | 60/60 |
| Mode hysteresis | 514/32400 | 116.67 | 92.01% | 0.7061 | 0.8305 | 60/60 | 48/60 | 0 | 60/60 |
| Envelope error | 402/32400 | 2194.44 | 92.04% | 0.6657 | 0.8034 | 60/60 | 48/60 | 0 | 60/60 |
| Envelope hysteresis | 625/32400 | 133.33 | 92.03% | 0.6116 | 0.8034 | 60/60 | 48/60 | 0 | 60/60 |
| Nominal entry + fixed return | 167/32400 | 33.33 | 91.67% | 0.7211 | 0.8304 | 60/60 | 48/60 | 0 | 60/60 |
| Envelope entry + fixed return | 277/32400 | 155.56 | 92.03% | 0.6561 | 0.8034 | 60/60 | 48/60 | 0 | 60/60 |

## extrapolation

| Method | Benign alarms / points | Alarm episodes/h | Recall | F1 | AP | Events hit | Fresh hits | Early-clear events | Cleared ≤5s / returned detected |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Persistence | 98/16200 | 300.00 | 2.94% | 0.0490 | 0.1050 | 21/30 | 21/30 | 21 | 21/21 |
| AR(4) | 78/16200 | 411.11 | 2.36% | 0.0400 | 0.1841 | 26/30 | 26/30 | 26 | 26/26 |
| ARX(4) | 550/16200 | 4366.67 | 88.01% | 0.7786 | 0.7064 | 30/30 | 25/30 | 30 | 30/30 |
| Following error | 1998/16200 | 11111.11 | 92.03% | 0.6073 | 0.9182 | 30/30 | 24/30 | 30 | 30/30 |
| Following mean (45) | 1073/16200 | 511.11 | 91.10% | 0.6744 | 0.7591 | 30/30 | 24/30 | 21 | 30/30 |
| Following CUSUM | 10089/16200 | 33.33 | 89.96% | 0.2370 | 0.1242 | 27/30 | 9/30 | 0 | 0/27 |
| Fused error | 636/16200 | 500.00 | 91.66% | 0.6984 | 0.8225 | 30/30 | 24/30 | 30 | 30/30 |
| Fused hysteresis | 936/16200 | 188.89 | 91.59% | 0.6610 | 0.8225 | 30/30 | 24/30 | 0 | 30/30 |
| Mode hysteresis | 3659/16200 | 688.89 | 91.97% | 0.4438 | 0.8228 | 30/30 | 24/30 | 0 | 30/30 |
| Envelope error | 8569/16200 | 20166.67 | 92.01% | 0.2896 | 0.7873 | 30/30 | 24/30 | 0 | 30/30 |
| Envelope hysteresis | 15868/16200 | 111.11 | 92.46% | 0.1928 | 0.7873 | 30/30 | 4/30 | 0 | 10/30 |
| Nominal entry + fixed return | 1143/16200 | 133.33 | 91.53% | 0.6459 | 0.8225 | 30/30 | 24/30 | 0 | 30/30 |
| Envelope entry + fixed return | 10789/16200 | 2733.33 | 92.07% | 0.2491 | 0.7873 | 30/30 | 20/30 | 0 | 30/30 |

Source: `local/recovery_v0.6/runs/simulation_001/aggregate.json`.
SHA-256: `103aac9488910a2f103e8d95fd7bda6a9aaf62675a2025d4aa6d6ad138f88dae`.
