# Completed raw RAPT normal-only training

19 October 2026. The single frozen Q1/seed17 run completed all100epochs within its declared resource limits. The full released architecture now has a saved, calibrated checkpoint under our transferred numerical-motion protocol. This closes the executable normal-training step for one plant/seed; it does not establish an attack-detection advantage, originality or full-paper reproduction.

## Recorded outcome

| Item | Result |
|---|---:|
| Architecture | Author RAPT forward dynamics;2,613,832parameters |
| Training rows / complete transition-window targets |9,900 /9,450|
| Normal-development selection targets |9,450|
| Epochs completed |100|
| Selected normal-development checkpoint |Epoch14|
| Selected development Gaussian NLL |0.1660407387|
| Epoch100 development Gaussian NLL |41.9201329549|
| Epoch100 training Gaussian NLL |−2.9056148529|
| Calibration eligible observations |9,900|
| Normal M13 scoring observations |9,900|
| Fixed-calibration model-only / hybrid point alarms |313 /313|
| Total wall / CPU |40.4425s /39.4347s|
| Training call including validation |37.9073s|
| Sampled peak memory |583,467,008bytes (556.44MiB)|
| Complete local output bytes |10,767,269|
| Synthetic software tests |8passed|
| In-worker checks |164passed|
| Separate fresh-process checks |192passed|

The normal-development checkpoint was saved and hashed before L13 calibration opened. All9saved development score arrays reproduce exactly from the saved checkpoint. Calibration was recomputed exactly, and fitted training statistics match the K13-only population. Model-only and hybrid scores/alarms happen to coincide here; no choice between them was made from that outcome.

The313/9,900alarms (3.1616%) describe normal **development** data under a threshold calibrated on a different normal task. They are not an unbiased held-out false-alarm estimate because M13 selected the checkpoint. No attack labels or final outcomes were read. The paper's nominal0.5%episode-FPR ROC result is a different metric/protocol and is not comparable to this point count.

## What the learning curve establishes

The author loop restores its best normal-development model after completing the100-epoch schedule. It correctly chose epoch14 rather than the much poorer epoch100. Thus the result is not a CPU-truncated fit. It also shows that simply training longer does not improve task-separated normal generalization in this particular run.

| Epoch | Training NLL | Development NLL |
|---:|---:|---:|
|1|0.6991|0.6531|
|10|−1.1231|3.4561|
|14|−0.8691|0.1660|
|20|−0.7098|0.6308|
|40|−1.1941|5.0331|
|60|−2.0033|19.1952|
|80|−2.7351|40.0375|
|100|−2.9056|41.9201|

The later training/development divergence is consistent with overfitting or predictive-uncertainty miscalibration under a task shift; this run does not separate those causes. A low training loss is not evidence of a well-calibrated detector. Neither a global optimum nor broadly adequate convergence is certified. The final-epoch weights were not retained by the unchanged author loop; only the selected checkpoint and complete curves are saved. No retrospective architecture, learning-rate, threshold or training-duration change was made.

## Run identity and commands

Working directory: `/Users/matrixusman/CUI/DigitalTwin/manufacturing`.

```sh
.venv-forecast-v016/bin/python -m unittest discover -s research_cycles/rapt_protocol_v0.21 -p 'test_*.py' -v
.venv-forecast-v016/bin/python research_cycles/rapt_protocol_v0.21/run.py
.venv-forecast-v016/bin/python research_cycles/rapt_protocol_v0.21/verify.py
```

One training attempt succeeded. The existing supervisor used an approved monitor-enabled execution because macOS process RSS monitoring is unavailable in the filesystem sandbox. No resource monitor was disabled. Caps were120s wall,90s CPU,1GiB sampled RSS,25MiB output. The run's provenance records interpreter/dependency versions, Git revision/dirty state, hardware/platform, configuration, source/input freeze and command. All source/vendor/data bindings remain unchanged.

Freeze SHA256:`5ba9e79111fddb84587831af91636b87c54509566069a4ec5e90b3b0e11c138a`.

Local artifacts: `local/rapt_protocol_v0.21/raw_Q1_seed17_001/`. Main files are`model.pt`,`config.json`,`obs_stats.json`,`history.json`,`selection.json`,`SELECTION_SEALED.json`,`calibration.json`,`normal_development_scores.npz`,`access.json`,`result.json`,`worker.log`,`supervisor.json`. `VERIFICATION.json` independently binds their completed bytes. All measurements are previously admitted synthetic normal data; original CASPER, voraus-AD and G1 signals/test recordings were not accessed.

## Recommendation

Retain this checkpoint as the raw author-code comparator for bounded normal-development diagnostics. Complete estimator admission using a shared raw prediction target before spending compute on projected variants. Nine raw plant/seed fits would take about6.1minutes at this measured rate; four preprocessing families would be approximately24.3minutes before extra verification, with variation across fits. Those are planning extrapolations and the36-fit matrix remains unexecuted/unadmitted here.

The immediate scientific question is whether an estimator improves task-separated predictive information beyond ordinary filtering, not whether it makes its own smoothed target easier to predict. No additional final experiment is justified until that question and the exact comparator/protected-reference roles are settled.
