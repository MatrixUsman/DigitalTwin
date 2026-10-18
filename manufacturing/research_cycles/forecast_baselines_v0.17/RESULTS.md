# Recent author-code forecasting results

Manufacturing, 18 October 2026. All nine registered outcomes completed once under the approved local budget. The three ICLR 2024 model classes are unchanged author code; the data, history, horizon, preprocessing, optimizer schedule and budget form our modified protocol. These are normal-development prediction measurements, not published-benchmark reproductions or attack-detection results.

| Model | Seed | Completed / selected epochs | Standardized MSE | Standardized MAE | CPU seconds per seed | Stop |
|---|---:|---:|---:|---:|---:|---|
| ModernTCN | 17 | 4 / 4 | 0.013426310 | 0.064299915 | 129.878 | declared_cpu_admission |
| ModernTCN | 42 | 4 / 4 | 0.012207311 | 0.059501380 | 130.281 | declared_cpu_admission |
| ModernTCN | 2026 | 4 / 4 | 0.013542819 | 0.061625821 | 130.415 | declared_cpu_admission |
| iTransformer | 17 | 5 / 4 | 0.023680216 | 0.088321303 | 135.071 | declared_cpu_admission |
| iTransformer | 42 | 5 / 5 | 0.020874676 | 0.082868460 | 135.179 | declared_cpu_admission |
| iTransformer | 2026 | 5 / 5 | 0.020030581 | 0.078749087 | 135.133 | declared_cpu_admission |
| TimeMixer | 17 | 8 / 8 | 0.014041325 | 0.076721760 | 129.984 | declared_cpu_admission |
| TimeMixer | 42 | 8 / 7 | 0.015218045 | 0.074443368 | 129.942 | declared_cpu_admission |
| TimeMixer | 2026 | 8 / 7 | 0.011628560 | 0.065609003 | 141.698 | declared_cpu_admission |

Each outcome covers the identical 2,048 development targets. All seeds are shown. The checkpoint rule uses normal development and the observations were already exposed in the prior study. These measurements therefore characterize the bounded development procedure, not an independent generalization estimate. Different histories and budgets in the earlier independent CNN study remain disclosed. Budget-stopped runs cannot be presented as converged; a favorable seed cannot substitute for the complete roster.

Total campaign wall time: 1208.167 s; summed worker CPU: 1199.209 s; maximum sampled RSS: 521.44 MiB; monitored outputs: 14.48 MiB. Memory is sampled, not an instantaneous ceiling. No paid compute was used.

Three synthetic model tests, 33 pilot arithmetic/seal checks and 294 full-study saved-artifact/checkpoint checks passed. All nine checkpoints exactly reproduce their saved predictions and retain their fitted state during evaluation. No final attacks, calibration thresholds or voraus-AD process signals were accessed.

## Reproducibility

Commands from `/Users/matrixusman/CUI/DigitalTwin/manufacturing`:

```sh
.venv-forecast-v016/bin/python research_cycles/forecast_baselines_v0.17/run.py --phase full
.venv-forecast-v016/bin/python research_cycles/forecast_baselines_v0.17/verify.py --method ModernTCN
.venv-forecast-v016/bin/python research_cycles/forecast_baselines_v0.17/verify.py --method iTransformer
.venv-forecast-v016/bin/python research_cycles/forecast_baselines_v0.17/verify.py --method TimeMixer
.venv-forecast-v016/bin/python research_cycles/forecast_baselines_v0.17/report.py
```

The training command is consumed and intentionally refuses to overwrite its run directory. Do not rerun it automatically. Verification performs inference only. `FREEZE.json`, `RUN_AUTHORIZATION.json`, `HARDWARE.json`, dependency lock, per-method provenance/access logs and output seals retain the full correspondence. The separate package manifest binds the resulting report. Original licenses remain in the ignored vendor checkouts.

## Scientific consequence

These executions resolve whether the three recent forecasting model classes can run on the common IMU task within a measured budget. They do not provide the protected command input or physical-return labels needed for the ARX–RBF simulation track. The prior failed attack-improvement criterion remains unchanged. MVT-Flow and full published robotic detector reproductions remain separate work.
