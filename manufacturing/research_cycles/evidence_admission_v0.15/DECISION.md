# Independent-recording and published-comparator admission

18 October 2026. Completed before the new manuscript revision. This is a source/data/code admission audit, not a trained baseline or new detection experiment.

## Original voraus-AD recording: received and identified

The author-linked 100 Hz Parquet file is now stored unchanged under `manufacturing/datasets/raw/voraus_ad/`. It contains 2,321,690 rows and 137 fields. Reading only episode IDs, relative time and labels confirms **2,122 executions: 948 original normal training executions, 419 normal test executions and 755 anomalous test executions**. All original training executions have normal labels; metadata is constant within each execution. No process signal column was opened.

- Original URL: https://media.vorausrobotik.com/voraus-ad-dataset-100hz.parquet
- Bytes: 1,115,942,833. SHA-256: `c90ab1c78af52651b954d41787f7e89d750f0a128b57600b0e5ceec22621f704`.
- Data license: CC BY-NC-SA 4.0, stated by the [author repository](https://github.com/vorausrobotik/voraus-ad-dataset). Code has a separate MIT license.
- Paper: Brockmann, Rudolph, Rosenhahn and Wandt, *The voraus-AD Dataset for Anomaly Detection in Robot Applications*, IEEE Transactions on Robotics 40 (2024), 438–451, DOI [10.1109/TRO.2023.3332224](https://doi.org/10.1109/TRO.2023.3332224). Public manuscript [arXiv:2311.04765v1](https://arxiv.org/abs/2311.04765v1), submitted 8 November 2023, is saved locally. Publisher-deposited metadata confirms journal identity; the exact first-online day was not supplied in that metadata.
- Independence: the paper describes a different six-axis collaborative robot, experiment and collection from CASPER. This supports a separate source/acquisition, not 2,122 independent robots. FactoryNet's repackaged voraus subset would not add another independent source.
- Labels: physical/process anomalies, including load, friction, collision and handling failures. Malicious origin and attack onset/recovery labels are not established. Do not relabel them cyberattacks.
- Clocks: time resets to zero each execution. Positive within-execution steps range from 0.00845194 to 0.01211095 seconds; nominal 100 Hz is not an exact uniform clock. Absolute acquisition/session timestamps are absent from the inspected schema. The paper documents training collected before testing, but sample ID order alone does not prove finer chronology.

**Decision:** admit the original release and provenance for a separate real-robot fault-detection/reference-validation study. The 1,174 original test executions remain closed to signal inspection and model selection. Dataset identity, grouping and label metadata have been inspected and are disclosed; this is not complete blinding. Any further within-training split needs a source-specific contract and must not claim unverified chronological ordering.

## MVT-Flow: eligible published baseline, execution conditional

Pinned author revision: `a91a86a642d23df58833b792a53de01edfd81abe`. The complete paper, nine relevant author files, licenses and download receipts are retained in `local/evidence_admission_v0.15/sources/`. Static examination connects the paper's multivariate normalizing flow to `NormalizingFlow`, `CouplingBlock`, `InternalNetwork` and the training/loader paths.

| Aspect | Verified correspondence and consequence |
|---|---|
| Information and fitting | Normal-only original training partition; target and measured machine channels; metadata excluded from the machine feature group. StandardScaler fits training observations only. |
| Architecture/configuration | Four coupling blocks; clamp 1.2; width scale 2; Adam 0.0008; batch 32; 70 epochs; learning-rate factor 0.1 at epochs 11 and 61; seed 177 in the released script. Channel permutations and temporal convolutions implement the flow. |
| Time and score | Complete variable-duration executions, padded to a training-derived length, and a negative-log-likelihood-style episode score. Symmetric convolutions inspect neighboring future positions within an execution. This is an offline episode comparator, not an online delay/recovery monitor. |
| Test exposure | `train.py` evaluates test AUROC every epoch. The released loop uses a fixed epoch count and saves the final model; test evaluation alone does not prove checkpoint tuning. Our runner must suppress those intermediate test outcomes. |
| Objective mismatch | Paper Eq. (8) and `get_loss_per_sample` use `0.5*sum(z**2)-jac`; `get_loss` uses `sum(z**2)-jac` before dimension normalization. The quadratic/Jacobian relative weights differ. This is a verified source discrepancy, not proof that published benchmark results used this exact revision or were invalid. |
| Padding edge case | `load_pandas_dataframes` assigns a truncated test frame and then overwrites it using the original frame plus padding. Synthetic longer-than-training inputs expose the behavior. No original test episode in the metadata audit exceeds the training maximum of 1,164 rows, so this does not establish a defect affecting this release's reported score. |
| Layer count | The manuscript describes three temporal convolution layers. Released `nHiddenLayers=0` gives two convolutions in each internal network; the middle-layer settings are inactive. Resolve this when deciding paper-faithful versus released-code execution. |
| Environment | Original requirements target Python 3.9, PyTorch and FrEIA. No upstream training or package setup was executed here. A separately isolated compatibility pilot is required. |

**Designation:** candidate for author-code execution under a documented modified protocol. A faithful paper reproduction remains conditional on the objective/layer correspondence. A corrected objective is a disclosed implementation variant, not automatically a novel detector. Any comparison with our model must use the same declared signals and complete-episode outputs; online recovery requires a separately justified causal implementation and compatible truth.

## FactoryNet: useful lead with concrete restrictions

The current primary manuscript is [arXiv:2605.09081v5](https://arxiv.org/abs/2605.09081v5), 8 October 2026. The pinned public dataset revision is `3bea3cfc10545d898604f93170108576fd46d518`; the API reports `gated=false`. Its [data card](https://huggingface.co/datasets/Forgis/FactoryNet/blob/3bea3cfc10545d898604f93170108576fd46d518/README.md) distinguishes original laboratory recordings from adapted voraus-AD, AURSAD and CNC data. Those adapted subsets are not independent replications of their sources. The card explicitly says the advertised newer synthetic campaign is not yet in that snapshot. The repository revision `651f066d97b704f0824687f1086eeb8f0422a8f3` contains an older description and code-license notice; it must not be treated as an exact implementation of every v5 experiment.

Licenses are subset-specific: the card assigns MIT to laboratory/synthetic data and retains the source licenses for adapted recordings. The source repository itself carries CC BY-NC-SA 4.0. Recording context can predict fault labels, some commanded/measured channels are absent, and context includes fault labels. Whole-table feature use would risk leakage. A setpoint column is not evidence of an authenticated independent command channel.

**Decision:** metadata-screened additional source, not yet admitted for a numerical comparison or recovery claim. No FactoryNet observations were downloaded. Before use, choose an original laboratory subset, resolve session grouping, deny outcome-derived context features, verify exact files and units, and separate fault classification from cyberattack/recovery evaluation. Do not download the entire corpus merely to inflate dataset count.

## Consequence for the manuscript

The independent-evidence check is complete at the stated level. The revised paper can identify a verified public recording and a concrete published comparator, explain their fit and limitations, and report the existing measured studies. It cannot report MVT-Flow or FactoryNet scores, completed cross-robot confirmation, successful novelty, or an attack advantage that has not been measured. The new manuscript must retain those boundaries.
