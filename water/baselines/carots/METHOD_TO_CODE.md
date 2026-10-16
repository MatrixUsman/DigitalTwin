# CAROTS: reading the method through its implementation

Study date: **16 October 2026**. This walkthrough connects the [ICML 2025 paper](artifacts/papers/CAROTS_ICML2025.pdf), [official proceedings record](https://proceedings.mlr.press/v267/kim25aa.html), [arXiv source](artifacts/source/arxiv_v1/main.tex) and the author snapshot at commit `63a41f45a2ae680d5cdbb2d5739e7a11264867cb`. Page numbers below are PDF pages. **Paper** identifies the authors' description; **Code** identifies inspected behavior; **Proposed** means unimplemented work; **Unknown** means evidence remains insufficient. No code was executed, imported or altered, and no weights or datasets were loaded. Researcher reading status remains **unknown**.

## 1. What the detector learns

**Paper, Sections 3–4:** CAROTS learns normal relationships between multiple observed variables, creates synthetic variations using those relationships, and learns an embedding that separates normal-looking variations from deliberately disturbed ones. At inference it combines embedding distance with forecasting error. Its clean-training assumption matters: the normal relationships are assumed stable over time. This is a useful non-twin comparator for our project, but it does not implement trustworthy online adaptation or establish a hydraulic digital twin.

Let `N` denote variables, `w` window length and `B` original batch size. A window `X_t` has shape `[w,N]`, ending at time `t`. The paper's adjacency `A[i,j]=1` means variable `i` helps predict variable `j`; rows are causes and columns effects. This is learned predictive/Granger structure. Observational predictive links are not automatically verified physical causes.

**Code, water defaults:** input batches are `[B,10,N]`, with `N=51` for SWaT and `N=123` for WADI. CUTS+ consumes the first nine steps and predicts the tenth. Its output is `[B,N,1]`, transposed by callers to `[B,1,N]`. These are configured expectations, not schemas validated against received data. The default LSTM maps each window to 512 features; a projection network maps `512 → 1024 → 512`. Both training and scoring use the projected representation, rather than discarding the projection head after contrastive training.

## 2. Follow one complete run without running it

The shipped [SWaT script](vendor/author_code/scripts/SWaT.sh) selects learning rate `0.0003`, weight decay `0.001` and downsampling five; [WADI](vendor/author_code/scripts/WADI.sh) selects `0.001`, `0.0` and five. They call `python main.py` with configuration pairs. These are upstream commands to understand, **not approved commands for execution**: the default evaluation uses test labels for optimization.

The call chain is:

```text
scripts/SWaT.sh or WADI.sh
  → main.main → parse_args → load_config
  → save config; set_seeds; build_model → CAROTS
  → build_trainer → CAROTSTrainer → Trainer.__init__
      → get_*_dataloader → construct_loader → build_dataset
          → SWaTSegLoader/WADISegLoader → split → downsample → scale
          → TSDataset.__getitem__ → [B,w,N] and [B] window labels
  → CAROTSTrainer.train
      → load CUTS+ checkpoint, otherwise CUTS_PLUS_Trainer.train
      → attach forecaster to CPA; freeze discoverer; contrastive training
      → validation loss → save selected CAROTS checkpoint
  → load_best_model → Predictor → Scorer.init_centroid
      → CL scores → CD scores → training-based normalization → sum
      → Thresholder → get_results → test.txt and score arrays
```

**Code configuration precedence:** defaults are cloned, an optional YAML file is merged, then command-line pairs are merged, **then dataset-specific assignments overwrite several values**. Both water datasets force downsampling five; WADI forces cosine scoring; variable counts and output paths are assigned afterward. Thus a command-line downsampling value other than five will not survive this parser for water. Inspect the final configuration, not just the shell command. `main.py` writes `config.txt` before later trainer mutations, including the similarity schedule, so that initial file is not a complete record of all subsequent state.

**Code data path:** normal records are split chronologically at `floor(0.8 × length)` before windowing; train/validation/test are downsampled separately. StandardScaler is fitted on training and applied to the others. Each label returned by `__getitem__` is one if **any retained point in that window** is anomalous. Consequently these are window-level outputs, not automatically per-second predictions. Median-of-five label aggregation happens earlier and can remove a short attack before window labels are formed. WADI row deletion can introduce gaps; SWaT has a feature/label row-removal discrepancy. The [verification report](VERIFICATION_REPORT.md) gives exact existing findings. **Unknown:** exact releases, timestamps, retained coverage and graph feature ordering.

## 3. Stage one: the forecasting causal discoverer

**Paper, Equation 1:** fit a forecaster while encouraging sparse edges, schematically `prediction MSE + λ × graph L1 norm`. CUTS+ is the chosen causal-discovery component. The graph expresses which variables provide useful past information for forecasting another variable; it does not encode an authenticated control channel or a guaranteed plant law.

**Code:** `CUTS_Plus_Net` stores unconstrained graph parameters `GT[N,N]`; `sigmoid(GT)` supplies edge scores. Its message-passing block multiplies each source-variable input by the corresponding source-to-target graph entry, combines messages, and updates GRU-style hidden states. Defaults use one recurrent layer, 32 hidden channels per node and a separate decoder per node. The function's local dimension names are confusing, but its callers pass `[B,9,N]`; its initial rearrangement produces `[B,N,9]` internally.

Training alternates two passes each epoch. `latent_data_pred` samples a Bernoulli graph and updates forecasting parameters using MSE. `graph_discov` uses a hard Gumbel-softmax sample and updates graph parameters using MSE plus `λ × ||Graph||₁/N²`. Defaults provide 50 discoverer epochs, distinct from the 30 contrastive epochs. Validation uses the continuous edge scores, whereas later augmentation and residual scoring threshold them at `>0.5`.

Do not equate the adapted implementation with every feature of the original CUTS+ method. The executed path visible in source sets its grouping matrix `G` to identity each epoch; a configured group policy is not applied there. A Gumbel-temperature schedule is updated, but the sampling call omits that temperature and uses the helper's default. The helper supplies `[p,1-p]` as softmax logits, unlike the Bernoulli sampling in the forecasting pass. These are **code observations**, not measured performance failures. **Unknown:** whether these choices match the configurations that produced the published CAROTS results; the original CUTS+ manuscript and upstream implementation need a separate detailed comparison.

After fitting/loading, CAROTS freezes the discoverer's parameters. Forecasting hidden states still evolve within each window; freezing parameters does not mean predicting a constant. There is no test-time parameter adaptation in this path. Fresh discovery hands over the final model, while cached discovery loads a best-validation checkpoint; their selection difference is already recorded in the audit.

## 4. Stage two: create four groups of windows

**Paper, Equation 3:** the causality-preserving augmentor (CPA) perturbs past values of selected causes with Gaussian noise, predicts affected variables using the perturbed history, and replaces their current values. It intends to create plausible normal variation according to the learned predictor.

**Code:** CPA selects one starting variable, shared across the batch, and finds its outgoing neighbors from the thresholded graph. Noise magnitude defaults to `0.1` in standardized units. A substantive discrepancy appears at lines 23–28: noise is added at index `INPUT_STEP`, but forecasting receives `x_pos[:, :INPUT_STEP]`. With the water defaults, noise changes time index **9**, while the forecaster consumes **0–8**. Thus that injected noise does **not** enter the forecast used to replace effects. A self-edge can also cause the noisy target value to be overwritten. This differs from perturbing past causes in Equation 3; no experiment is needed to observe the slicing difference, but its numerical consequences remain unmeasured.

**Proposed:** a synthetic dependency fixture should first demonstrate which timestamps enter the forecaster and which outputs change. Specify the intended history perturbation explicitly before choosing a paper-faithful correction. Preserve the original path as an identified upstream variant if later compared; do not silently correct it and claim unchanged author-code reproduction.

**Paper:** the causality-disturbing augmentor (CDA) traverses the graph and injects biases into connected variables to construct negative examples. **Code:** it chooses one root and traverses outgoing edges with cutoff probability `0.1`. A failed continuation breaks the current neighbor loop. One selected subgraph is shared across the batch. `AddBias` chooses half the window positions by default, then samples biases from `±0.1,…,±0.5` for each selected sample/time/variable. There is no model-based propagation of these biases to preserve downstream behavior.

An original batch `G1[B,10,N]` produces CPA batch `G2`, then CDA operates on their concatenation to produce `G3` and `G4`. `CAROTS.forward` returns embeddings in the order `[G1,G2,G3,G4]`, shape `[4B,512]` under defaults. The first `2B` are positive examples and the remaining `2B` synthetic negatives. These training labels come from augmentation, not real attack annotations. **A synthetic negative is not necessarily a feasible cyberattack or physical fault**, and the CPA label does not certify physically legitimate operation.

## 5. Stage three: learn the embedding

The LSTM reads each entire window and returns its final hidden state. With one layer this is `[4B,512]`; the projector applies linear, batch-normalization, GELU and linear layers. The contrastive objective operates on normalized projected vectors, so its pairwise cosine-similarity matrix is `[4B,4B]`.

**Paper, Equation 6:** each of the `2B` positive examples is an anchor. Keep positive partners whose cosine similarity meets threshold `α`; retain their corresponding disturbed negatives at an index offset of `2B`. A pair's loss compares its positive exponential similarity against that term plus the selected negative exponential similarities, using temperature `τ=0.1`. The paper averages eligible pairs **within each anchor**, then averages anchors. Similarity filtering is intended to avoid forcing all normal patterns together immediately.

**Code:** `loss_fn` performs this paired masking and removes diagonal self-positive contributions. However, line 36 divides the total eligible-pair loss by the **total number of non-self eligible pairs**, rather than averaging within each anchor first. Anchors with more selected partners therefore receive greater weight; this is not generally Equation 6 when partner counts differ. `sim_mtx_pos` is a view of the original cosine matrix: the in-place masking changes that view, but rebinding `sim_mtx` to exponentials does not. Final eligibility therefore uses masked cosine values, not exponentials. The code explicitly excludes self-positive pairs, while the displayed equation does not state that exclusion. If no non-self positives qualify, the denominator can be zero; actual occurrence is unknown.

The schedule raises `α` from `0.5` to `0.9` over 30 epochs. At fixed similarities this is stricter, not looser. The authors' explanation of increasing inclusion depends on embeddings becoming more similar during training; the schedule alone cannot demonstrate that behavior. Both training and validation generate stochastic augmentations and evaluate SOC loss. Validation selects among evaluated checkpoints every five contrastive epochs, using normal-validation loss rather than attack detection F1. Default seed is zero; the scripts do not themselves loop over the paper's three seeds.

## 6. Stage four: score a new window

`Scorer.init_centroid` runs training windows through the model with augmentations, keeps only the positive half and averages their projected embeddings. SWaT uses raw-embedding Euclidean distance. WADI averages normalized embeddings, normalizes that centroid again, and uses `(1−cosine)/2`. New test windows are embedded **without augmentation**. The separate CD score is mean squared prediction error across variables for the final window step.

**Paper, Equation 7 / Code:** calculate each component's mean and standard deviation on training scores, z-normalize train/test scores using those statistics, then sum CL and CD equally. This is a continuous anomaly score, not an attack probability. The predictor lacks a zero-standard-deviation guard. Its scoring loaders also retain original shuffle/drop-last settings because cloned inference flags are not passed into construction; see the prior audit before interpreting training-score coverage.

**CAROTS-dagger** removes the CD score from final detection; it still needs the causal discoverer for training augmentation. It is not “CAROTS without causality.” The pinned predictor unconditionally computes and adds both scores, so a declared CL-only inference path is needed. Do not pick full versus dagger using held-out attacks.

Final evaluation currently chooses the best threshold using test labels and independently reports maximum F1 from the test precision–recall curve. AUPRC is trapezoidal PR integration. Point-adjusted metrics are enabled in the code despite exclusion in the paper. Our future protocol requires independent calibration, fixed-threshold metrics, explicit window-to-time alignment and unadjusted main metrics. That would be **author-code execution with declared protocol changes**; CPA/loss corrections would introduce additional algorithmic differences requiring separate records.

## Evidence map

Local paths below are relative to this folder. Every online code link is pinned to the audited commit; ranges identify the inspected implementation. Paper-to-code correspondence does not imply exact equivalence.

| Paper location / stage | Local implementation and exact lines | Pinned code |
|---|---|---|
| §5.1 p.6, Appendix B p.16; launch/config | [main.py](vendor/author_code/main.py), `main` 8–32; [utils/parser.py](vendor/author_code/utils/parser.py), `load_config` 34–89 | [main](https://github.com/kimanki/CAROTS/blob/63a41f45a2ae680d5cdbb2d5739e7a11264867cb/main.py#L8-L32), [parser](https://github.com/kimanki/CAROTS/blob/63a41f45a2ae680d5cdbb2d5739e7a11264867cb/utils/parser.py#L34-L89) |
| §5.1; split, scale, window label | [datasets/build.py](vendor/author_code/datasets/build.py), `TSDataset` 50–105; water loaders 198–292 | [loader](https://github.com/kimanki/CAROTS/blob/63a41f45a2ae680d5cdbb2d5739e7a11264867cb/datasets/build.py#L50-L105) |
| Appendix B; median aggregation | [datasets/util.py](vendor/author_code/datasets/util.py), `downsample` 4–15 | [resampling](https://github.com/kimanki/CAROTS/blob/63a41f45a2ae680d5cdbb2d5739e7a11264867cb/datasets/util.py#L4-L15) |
| Eq.1 pp.3–4; graph and forecast | [modeling_cuts_plus.py](vendor/author_code/models/carots/modeling_cuts_plus.py), `MPNN.forward` 38–50; `CUTS_Plus_Net` 71–161 | [model](https://github.com/kimanki/CAROTS/blob/63a41f45a2ae680d5cdbb2d5739e7a11264867cb/models/carots/modeling_cuts_plus.py#L38-L161) |
| Eq.1; alternating optimization | [trainer_cuts_plus.py](vendor/author_code/models/carots/trainer_cuts_plus.py), `latent_data_pred` 231–262, `graph_discov` 264–294, `train` 296–390 | [training](https://github.com/kimanki/CAROTS/blob/63a41f45a2ae680d5cdbb2d5739e7a11264867cb/models/carots/trainer_cuts_plus.py#L231-L390) |
| Eq.3 p.4, Fig.2 p.5; CPA | [modeling_positive_augmentor.py](vendor/author_code/models/carots/modeling_positive_augmentor.py), `forward` 17–30 | [CPA including discrepancy](https://github.com/kimanki/CAROTS/blob/63a41f45a2ae680d5cdbb2d5739e7a11264867cb/models/carots/modeling_positive_augmentor.py#L17-L30) |
| §4.1 p.4; CDA | [modeling_negative_augmentor.py](vendor/author_code/models/carots/modeling_negative_augmentor.py), 16–58; [transform_layer.py](vendor/author_code/models/carots/transform_layer.py), `AddBias.forward` 13–21 | [traversal](https://github.com/kimanki/CAROTS/blob/63a41f45a2ae680d5cdbb2d5739e7a11264867cb/models/carots/modeling_negative_augmentor.py#L16-L58), [bias](https://github.com/kimanki/CAROTS/blob/63a41f45a2ae680d5cdbb2d5739e7a11264867cb/models/carots/transform_layer.py#L13-L21) |
| Eqs.4–5 pp.4–5; groups/encoder | [modeling_carots.py](vendor/author_code/models/carots/modeling_carots.py), `forward` 66–90, projector 36–45; [encoder.py](vendor/author_code/models/carots/encoder.py), `LSTM_ENC` 100–120 | [groups](https://github.com/kimanki/CAROTS/blob/63a41f45a2ae680d5cdbb2d5739e7a11264867cb/models/carots/modeling_carots.py#L66-L90), [LSTM](https://github.com/kimanki/CAROTS/blob/63a41f45a2ae680d5cdbb2d5739e7a11264867cb/models/carots/encoder.py#L100-L120) |
| Eq.6 p.5; SOC | [loss.py](vendor/author_code/models/carots/loss.py), `loss_fn` 5–38 | [loss including weighting difference](https://github.com/kimanki/CAROTS/blob/63a41f45a2ae680d5cdbb2d5739e7a11264867cb/models/carots/loss.py#L5-L38) |
| §5.1/Appendix B; freezing/checkpoints | [trainer_carots.py](vendor/author_code/models/carots/trainer_carots.py), `train` 40–83, `load_best_model` 123–139 | [selection](https://github.com/kimanki/CAROTS/blob/63a41f45a2ae680d5cdbb2d5739e7a11264867cb/models/carots/trainer_carots.py#L40-L139) |
| Eq.7 pp.5–6; centroid/components | [scorer_carots.py](vendor/author_code/models/carots/scorer_carots.py), `init_centroid` 16–42, `get_anomaly_scores` 45–73 | [scorer](https://github.com/kimanki/CAROTS/blob/63a41f45a2ae680d5cdbb2d5739e7a11264867cb/models/carots/scorer_carots.py#L16-L73) |
| Eq.7 / §5.2; full versus dagger | [predictor.py](vendor/author_code/models/carots/predictor.py), `predict` 32–78 | [unconditional ensemble](https://github.com/kimanki/CAROTS/blob/63a41f45a2ae680d5cdbb2d5739e7a11264867cb/models/carots/predictor.py#L32-L78) |
| §5.1/Appendix B; final metrics | `predictor.py::get_results` 140–170; [threshold.py](vendor/author_code/threshold.py), 28–43 | [metrics](https://github.com/kimanki/CAROTS/blob/63a41f45a2ae680d5cdbb2d5739e7a11264867cb/models/carots/predictor.py#L140-L170), [threshold](https://github.com/kimanki/CAROTS/blob/63a41f45a2ae680d5cdbb2d5739e7a11264867cb/threshold.py#L28-L43) |

## Reading exercises and next decisions

1. Draw `G1–G4` for a **synthetic** three-variable example. Mark what the paper intends to perturb and what the current CPA actually changes.
2. Trace one `[B,10,51]` tensor through the forecaster, augmentors, LSTM, projector and scores. Explain why a window label and final-step residual describe different temporal scopes.
3. Hand-calculate SOC for anchors with unequal partner counts; compare Equation 6 with global-pair weighting. Specify empty-positive behavior before implementing a test.
4. Explain why dagger still requires causal discovery, and why a good anomaly score does not supply an operational threshold.
5. List the trusted information available to our proposed adaptation mechanism. CAROTS's frozen clean-training assumption supplies a comparator, not proof that such information remains trustworthy online.

**Priority before implementation:** settle CPA semantics and SOC weighting; preserve chronology/labels; resolve discoverer selection and sampling settings; specify full/dagger scoring and calibration. Exact-release permission, environment portability and expected runtime remain unresolved. None requires tuning on final attacks.

**Actual assistant reading coverage:** this pass read the published method text and Equations 1–7 (pp.3–6), Figure 1–2 captions, §5.1 and Appendix B, and their source TeX; statically followed the default water path through scripts, parser/config, model factory, base/water loaders, training loops, CUTS+ network/optimization, both augmentors, LSTM/projector, SOC, scorer, predictor, thresholds and metric writing. Alternate encoder internals and dependency libraries were not comprehensively audited; the separate CUTS+ paper was not fully studied here. The earlier [verification report](VERIFICATION_REPORT.md) covers identity, references and numerical consistency. This is assistant study coverage, not a human-read attestation or a completed reproduction.
