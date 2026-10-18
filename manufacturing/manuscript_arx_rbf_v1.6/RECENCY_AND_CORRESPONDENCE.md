# Recent comparisons and what was executed

18 October 2026. Same-assistant source review, not independent replication or a claim that the researchers have read each paper. The selection window remains 16 October 2023–16 October 2026. Dates below identify cited publication versions; a conference paper may have an older preprint.

| Method | Verified cited publication | Primary source | Executed role in this revision |
|---|---|---|---|
| CASPER | ACM Transactions on Internet of Things, 2024; DOI 10.1145/3670414 | https://dl.acm.org/doi/10.1145/3670414 ; author repository https://github.com/hkayann/1D-CNN-Anomaly-Detection-via-CASPER | Preserved independent CNN results from v0.11; not a complete author-code attack-detector reproduction |
| Edge CNN | IEEE Internet of Things Journal 12(15), 29696–29712, 2025; DOI 10.1109/JIOT.2025.3569780 | https://orca.cardiff.ac.uk/178905 ; https://ieeexplore.ieee.org/document/11004009/ | Preserved independent compact CNN results; normal forecasting, not the paper's complete task |
| ModernTCN | ICLR 2024 | https://openreview.net/forum?id=vpJMJerXHU ; https://github.com/luodhhh/ModernTCN | Official model class; fixed transferred configuration, normal CASPER IMU forecasting |
| iTransformer | ICLR 2024 | https://openreview.net/forum?id=JePfAI8fah ; https://github.com/thuml/iTransformer | Official model class; same normal targets and training procedure |
| TimeMixer | ICLR 2024 | https://openreview.net/forum?id=7oLshfEIC2 ; https://github.com/kwuking/TimeMixer | Official model class; same normal targets and training procedure |
| MVT-Flow / voraus-AD | IEEE Transactions on Robotics, volume 40, 2024; preprint 8 November 2023 | https://arxiv.org/abs/2311.04765v1 ; https://www.tnt.uni-hannover.de/project/anomaly/?publ=2 | Source/metadata audit only; no original signal or test outcome access in this task |

The publisher refresh for CASPER returned HTTP 403; IEEE's Edge page presented a browser challenge. The existing full CASPER audit and author repository remain available; Cardiff's primary institutional record confirms the Edge publication metadata but does not supply a full manuscript there. MVT-Flow's issue year and preprint date are distinguishable from its institution's November 2023 online listing; the exact publisher first-online day was not newly verified. These limitations are not evidence that the papers are invalid.

The bibliography is unchanged at 20 references. Eighteen cited versions are dated 2024–2026 (90%). The 2010 interval-observer paper and 2021 confidence-sequence paper are mathematical background. AR, persistence, rolling mean and CUSUM remain necessary explanatory controls even though their foundations are older. Recency does not establish state of the art, and an unexecuted discussion is not a measured comparator.

## Author-code correspondence

| Method | Frozen revision | License | Loaded class |
|---|---|---|---|
| ModernTCN | `56a9a2c018385cd5acef015378cae7f084d1b11c` | MIT | `ModernTCN-Long-term-forecasting/models/ModernTCN.py:Model` |
| iTransformer | `c2426e68ca13f74aaec08045c5c724d8ad328124` | MIT | `model/iTransformer.py:Model` |
| TimeMixer | `e24610583b36fdd8c76cc17a8df4e65759a5f460` | Apache-2.0 | `models/TimeMixer.py:Model` |

The model sources are unpatched. The wrapper changes the task to nine channels, history 96 and horizon one; it omits future time features. Training-only outer scaling and causal median preprocessing are inherited from the sealed common-input study. The models' input-window normalization is retained. The selected author ETTh1 architectural configurations and learning rates are recorded in `research_cycles/forecast_baselines_v0.17/adapter.py` and `FREEZE.json`; all dependency and upstream source identities are bound there.

All three models run three fresh seeds under the same per-seed CPU admission and normal-development selection rule. Different epoch counts under this constraint are reported, not concealed as equal convergence. Older CNNs used different histories and training budgets. Neither comparison estimates the proposed command-driven model's attack performance on real IMU data, because that task lacks its protected commands and evaluator-only physical return. There is no joint attack ranking across these incompatible tracks.

## Five-fold meaning

Five expanding chronological train/validation folds refit both references from prior observations on nine existing synthetic commissioning episodes. No random row mixing or cross-boundary windows is used. Hyperparameters were already chosen during earlier development, so these folds assess temporal stability; they cannot retroactively supply independent confirmation or unbiased model selection. The original attack audit and failed primary criterion remain unchanged.
