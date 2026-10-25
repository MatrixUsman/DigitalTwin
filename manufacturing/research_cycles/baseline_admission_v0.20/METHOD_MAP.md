# Manuscript-to-released-code mapping

19 October2026. Upstream revision `d745668ffdb0e26877b1de4c9b2126af7bda5b03`; exact downloaded bytes in `SOURCE_RECEIPT.json`. Paths below are relative to `baselines/vendor/rapt_v020/`.

| Component | Manuscript locator | Released implementation | Admission consequence |
|---|---|---|---|
| State/action input | §3.2 forward-dynamics variant | `rapt/model.py:RaptModel`; `rapt/data.py:make_windows` | At time t predict observation t from preceding observed state/action; no future observation enters prediction. |
| Architecture | §3.2,Eq1 | width256;4residual encoder blocks;GRU256;latent192;4decoder blocks;diagonal Gaussian mean/logvariance; clamp logvariance±6 | Use original full architecture unless a separately declared resource constraint changes it. |
| Objective | §3.2 Gaussian NLL | `rapt/model.py:nll_loss`: mean of0.5[(y−mu)^2/exp(logvar)+logvar] | Original author loss is directly executable. |
| Detector score | §3.3 calls score NLL | `rapt/model.py:nll_per_dim`: **(y−mu)^2/exp(logvar)** | Released score omits the logvariance term; retain accurately named standardized squared residual. Do not call it full NLL. |
| Local gate | Eq2: maximum calibration score+5standard deviations | `rapt/detector.py:calibrate`: maximum+2(maximum−median) | A real correspondence difference, not automatically a defect. The latter also appears in original `reproduce/realworld/test_real_world_rapt.py:1176`. |
| Global gate | Eq2 global baseline+3sigma, precise aggregation not stated there | `detector.py:calibrate`: max over time of per-row mean+3std of row means | `scripts/evaluate_paper.py` instead uses mean of per-channel maxima+3std across episode mean-maxima. Keep variants distinct. |
| Range gate | §3.4 optional | `detector.py:Calibration.range_lo/range_hi`: calibration min−range, max+range; logical OR | Evaluate model-only and hybrid without choosing by final outcome. Range is an observation envelope, not a physical safety proof. |
| Preprocessing | §3.1 z normalization | `data.py:NormStats.from_data` uses training rows only; std floor1e−6; action units are untouched | Preserve train-only fit; require channel/unit assertion. |
| Training | implementation supplement | `train.py:train_rapt`:AdamW1e−3,weightdecay1e−2,OneCycleLR,denoising.01,clip1;best normal-validation NLL | Call library with separately supplied populations; never invoke test-dependent selection. |
| Splits/windows | release default | `data.py:SequenceData.split` random by sequence; `make_windows` non-overlapping inside episodes | Main study supplies chronological/task-independent populations first; no windows cross splits. This is a disclosed protocol modification. |
| Streaming | §3.3 online | `detector.py:RaptDetector.step` stores previous input and GRU state; no alarm-based reset or update freeze | Do not reset at intervention labels. First dynamics step has no transition score and must be explicitly ineligible. |
| Batch inference | release convenience | `score_sequence` uses same unidirectional GRU and aligns prediction t−1 with targett | Synthetic batch/stream test passed tolerance; final artifact scoring should also validate causal prefix invariance. |
| Evaluation | §4.4 ROC/SafetyScore | `evaluate_paper.py` supplies episode ROC-derivedTPR at0.5%FPR and notes interpolation/campaign differences | ROC is descriptive only. Main threshold must be fixed on normal calibration, never selected from testROC. |

## Executable interface

From an isolated interpreter whose dependencies are recorded:

```python
import sys
sys.path.insert(0, "baselines/vendor/rapt_v020")
from rapt import RaptConfig, SequenceData, train_rapt, calibrate, RaptDetector
cfg = RaptConfig(obs_dim=4, action_dim=4, train_dynamics=True,
                 dt=0.02, batch_size=32, num_epochs=100, seed=17)
# train_obs/train_cmd and dev_obs/dev_cmd are separate admitted normal episodes.
model, stats, history = train_rapt(
    cfg, SequenceData(train_obs, train_cmd),
    SequenceData(dev_obs, dev_cmd), device="cpu")
cal = calibrate(model, stats, SequenceData(cal_obs, cal_cmd), cfg)
detector = RaptDetector(model, stats, cal, use_range=False)
# Feed one tick at a time; reset only at declared acquisition boundaries.
```

This is an interface example, not the final study configuration or an executed100-epoch run. No direct checkpoint saving into upstream directories is permitted; persist in new local run storage. Preserve seed17,42,2026 roster if stochastic final runs are admitted.

## Specific cautions

The public convenience evaluators contain stale textual protocol labels even when executable defaults changed. `evaluate_paper.py`'s top docstring/output says margin2.2/1.2 while actual default argument is sigma5_3. It also documents correction of historical ROC interpolation and two perturbations reset before application. Treat those as author-disclosed implementation differences, not as our independently reproduced defects. No paper headline metric should be expected byte-for-byte from the smaller public release.

The previous state entering a predictor may explain a sustained shifted trajectory. That does not imply parameter contamination: the weights are fixed. A future experiment must report whether a limitation belongs to inference-state conditioning, calibration, inputs or training adequacy.

Primary executable sources: [model.py](https://github.com/csiro-robotics/RAPT/blob/d745668ffdb0e26877b1de4c9b2126af7bda5b03/rapt/model.py), [detector.py](https://github.com/csiro-robotics/RAPT/blob/d745668ffdb0e26877b1de4c9b2126af7bda5b03/rapt/detector.py), [train.py](https://github.com/csiro-robotics/RAPT/blob/d745668ffdb0e26877b1de4c9b2126af7bda5b03/rapt/train.py), [data.py](https://github.com/csiro-robotics/RAPT/blob/d745668ffdb0e26877b1de4c9b2126af7bda5b03/rapt/data.py), [evaluate_paper.py](https://github.com/csiro-robotics/RAPT/blob/d745668ffdb0e26877b1de4c9b2126af7bda5b03/scripts/evaluate_paper.py).
