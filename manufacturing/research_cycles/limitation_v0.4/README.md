# Frozen-model limitation experiment

**Completed 17 October 2026.** Read [RESULTS.md](RESULTS.md) for measured findings and [duration trade-offs](../../output/limitation_v0.4/duration_tradeoff.png) for the principal figure. This is a separately versioned exploratory measurement-replay study; v0.3 trained artifacts and all older experiments remain unchanged.

The study ran 189 synthetic cases through six saved predictors and four causal scoring rules, then evaluated all 4,536 model/score/case combinations together. All 22 synthetic tests passed after one documented float32 assertion correction; fresh-process verification passed 26,374 checks. No retraining, new raw observation parsing, new held-out exposure or dependency installation occurred.

## What was tested

Hold blends, slow playback and sensor offsets of duration 5,45,450 observations test prediction-history conditioning. Point error, 45/450-observation rolling means and a CUSUM-style accumulator share the same normal calibration population. The clean-history counterfactual is a diagnostic oracle, excluded from the detector ranking. These edits are not a physical simulator or independently recorded attacks.

Long-event CNN point recall rose from 25.12% to 53.33% with a 45-point mean and to 66.91% with accumulation. Mean case F1 was 0.2778,0.5127,0.2364 respectively: accumulation's long post-event alarms offset its coverage gain. The rolling mean also misses brief events. All families, severities, seeds, normal alarms and controls are retained in [216 aggregate rows](aggregate_outcomes.csv) and [structured results](RESULTS.json).

## Exact completed commands

Working directory `/Users/matrixusman/CUI/DigitalTwin`:

```sh
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/limitation_v0.4/freeze.py --attempt tests_001
# One synthetic float32 assertion failed. The failed log is preserved.
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/limitation_v0.4/freeze.py --attempt tests_002
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/limitation_v0.4/run.py --attempt replay_001
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/limitation_v0.4/verify.py --run replay_001 --attempt verify_001
manufacturing/.venv-plots-v03/bin/python manufacturing/research_cycles/limitation_v0.4/report.py
```

Consumed attempts and the freeze cannot be overwritten. For synthetic-only verification, run `python -m unittest -v test_mechanism` from this directory in the existing isolated training environment. It needs no dataset or fitted model. Scientific changes require a new version and explicit outcome-informed status. Report regeneration performs no training; it checks the sealed run before generating presentation artifacts.

## Files and provenance

- [PLAN.md](PLAN.md), [config.json](config.json), [FREEZE.json](FREEZE.json): exact hypothesis, population, interventions, scores, resource caps, 10 source and 260 input identities frozen before replay.
- [mechanism.py](mechanism.py), [test_mechanism.py](test_mechanism.py): independent measurement transformations, scores, calibration and event definitions with synthetic checks.
- [common.py](common.py), [worker.py](worker.py), [run.py](run.py), [freeze.py](freeze.py): source admission, frozen-artifact inference, supervision and execution receipts.
- [verify.py](verify.py): independently written arithmetic, full-versus-optimized inference, analytic controls, immutable-source and resource checks.
- [report.py](report.py): post-execution descriptive aggregation and plotting; source hash is recorded separately from the earlier freeze.
- [Training environment lock](../contribution_v0.2/requirements-macos-arm64.lock.txt), [plotting lock](../baseline_training_v0.3/requirements-plot-macos-arm64.lock.txt): existing environments reused unchanged.
- [Local run](../../local/limitation_v0.4/runs/replay_001/): all affected predictions, residuals, counterfactual errors, original normal scores, thresholds, complete case outcomes, provenance and resource receipts.
- [Local verification](../../local/limitation_v0.4/verification/verify_001/verification.json), [tests](../../local/limitation_v0.4/tests/), [post-execution package manifest](PACKAGE_MANIFEST.json).

`*_overrides.npz` stores, for every case, changed predictions, energy and oracle energy from target `onset` through `onset+duration+45` (exclusive). Start from the complete `energy` array in `*_normal.npz`, replace that slice, then call `mechanism.score_streams` with the saved `normal_mean` and frozen config. This reconstructs the full causal score time course without opening raw files. `raw_indices` map targets to original numeric rows. The stored energy is MSE across standardized channels; the point threshold is equivalent to an RMSE threshold after square root.

Calibration and all prediction/error files were hashed in `SCORES_SEALED.json` before joint outcomes were computed. One first-onset/middle-severity example per family and duration was selected in advance for figures. No threshold, model, seed or scenario was selected using the intervention outcomes.

## Research handoff

Keep the rolling mean as a strong ordinary control; retain accumulation to expose its persistence/recovery trade-off. The hypothesis of universal CNN residual collapse is not supported. The next mechanism should address sustained-change evidence, brief-event sensitivity and justified recovery jointly, under a physically specified simulation with equal access to any trusted context. That next design is informed by this exploratory result and needs fresh, predeclared evidence for confirmation. CUSUM and rolling means are established methods, not novelty claims.
