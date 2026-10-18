# Five-fold temporal validation results

## Material Passport
Manufacturing; 18 October 2026. Retrospective normal-only diagnostic on existing synthetic commissioning episodes. Five expanding-window folds, three plants, three episodes per plant. No attack evaluation, new hyperparameter selection or raw dataset access.

All 15 plant-fold fits completed; both references scored 4,500 eligible observations. Five synthetic software tests and 109 saved-artifact checks passed. The initial sandbox-denied resource-monitor attempt remains preserved; unchanged scientific code completed after process-monitor permission. The original freeze and the separate infrastructure repair are retained.

| Fold | Training rows per episode | Scored rows per episode | Targets per method | ARX standardized RMSE | ARX–RBF standardized RMSE |
|---|---|---|---:|---:|---:|
| 1 | [0,200) | [300,400) | 900 | 0.224180764 | 0.224551350 |
| 2 | [0,400) | [500,600) | 900 | 0.011500530 | 0.011521208 |
| 3 | [0,600) | [700,800) | 900 | 0.012051899 | 0.012074569 |
| 4 | [0,800) | [900,1000) | 900 | 0.011103480 | 0.011086374 |
| 5 | [0,1000) | [1100,1200) | 900 | 0.010940371 | 0.010937394 |

The RBF correction improves pooled RMSE in folds 4 and 5, and in 5/15 individual plant-fold cases. Effects are small and inconsistent; these results do not establish a predictive advantage. The first fold uses a much shorter commissioning prefix. Fold-specific scaling, changing trajectory segments and training length all affect across-fold errors; the rows are not an isolated training-size causal experiment. Each reference is initialized from 100 normal observations inside the validation block, then forecasts the following 100 without measurement correction.

Settings were selected in earlier development, so this is not nested validation or unbiased independent confirmation. Training prefixes overlap between folds; no standard-error, significance or independent-robot claim is made. Existing attack findings and frozen model choices remain unchanged. Full per-channel native-unit errors, all fitted coefficients, row alignment and plant-fold outcomes are in the run artifacts.

Actual supervised wall time: 0.485 s; worker CPU: 0.297 s; sampled RSS: 38.97 MiB; getrusage peak RSS: 50.77 MiB; monitored output: 806,804 bytes. All are within the declared limits. RSS sampling is not an instantaneous ceiling.

Commands from manufacturing: `.venv-reproduction-v02/bin/python research_cycles/fivefold_v0.16/resume.py` (with required process monitoring permission), then `.venv-reproduction-v02/bin/python research_cycles/fivefold_v0.16/verify.py`. No new scientific fit ran during verification.
