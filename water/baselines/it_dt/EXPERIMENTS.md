# IT-DT experimental specification audit

**No experiments have been run.** This file separates the authors' description from the work needed for a future, independently implemented comparison. See [resource provenance](../RESOURCE_MANIFEST.json), [data gaps](DATASETS.md) and the [common reproduction proposal](../../docs/REPRODUCTION_PLAN.md).

**Execution hold after verification:** [VERIFICATION_REPORT.md](VERIFICATION_REPORT.md) records a figure/threshold inconsistency, an F1 arithmetic/aggregation question, conflicting descriptions of the statistical endpoint and missing validation-label provenance. The mathematical method can be studied, but its published numerical claims are not validated. The quadratic runtime claim also needs an explicit method for updating the changing covariance log determinant; no such implementation is supplied.

## Authors' described method

| Component | Published specification | Reproduction gap |
|---|---|---|
| Identification | N4SID on normal recordings; state orders SWaT 12, WADI 25; noise covariances estimated from training | Input/output mapping, N4SID implementation/options, block size, fitted matrices and initialization absent |
| Synchronization | Steady-state Kalman prediction and measurement correction; innovation residual scored | Initial state/covariance, gain calculation and reset rules incomplete |
| Score | Gaussian KL divergence between a residual-window estimate and a normal reference | Reference-estimation procedure, rank/numerical handling and all executable details unverified |
| Window/regularization | `W=60`; candidates `{30,60,120,240}`; diagonal regularizer `1e-4` | Sensitivity text uses validation F1; provenance of positive validation labels unresolved |
| Threshold | Attack-free validation 99th percentile, nominal false-alarm target 0.01 | Exact calibration interval/sample count, quantile convention and independence from fitting unresolved |
| Statistical analysis | Ten chronological non-overlapping test subsets; Wilcoxon comparison to TranAD | Original subset boundaries, per-subset predictions and uncertainty inputs absent |
| Delay example | SWaT Attack #41; IT-DT threshold bootstrap versus neural initialization variability | Attack mapping, bootstrap details and comparability of uncertainty estimates unresolved |
| Timing | CPU Intel i9-14900K reported; comparison includes CPU and GPU latency | Executable dependencies, profiling code, warm-up/repetitions and GPU details incomplete |

Source: [arXiv v1](https://arxiv.org/html/2603.01621v1), Sections III–VI, Algorithm 1 and Tables I–III. The downloaded TeX and figure PDFs preserve the reported presentation; they do not supply its computational pipeline.

## Scientific distinctions to preserve

The Kalman filter's current state changes as measurements arrive. That does not establish online learning of the system matrices, residual reference or alarm threshold. Algorithm 1 computes the innovation before state correction and makes the alarm decision afterward. It does not specify a trust gate that rejects suspicious measurements from state correction. Reproduce this ordering accurately if later authorized; any change to it is an explicit algorithmic change.

The manuscript discusses Gaussian approximations and false alarms during operational transitions. These motivate questions, but do not prove our proposed adaptation mechanism is novel or effective. Dataset attack detection and a delay plot do not demonstrate mitigation or prevented physical damage.

## Required work before a pilot

1. Resolve the missing dataset, identification, calibration and window-selection details from authoritative artifacts; record remaining assumptions. Author outreach needs explicit authorization.
2. Decide whether the available specification supports a useful reimplementation. No matched author code, software license, checkpoints or original logs are verified.
3. Freeze a clean chronological development/calibration protocol. Never optimize `W`, model order, preprocessing, checkpoint, architecture or threshold on held-out test attacks. Predeclare allowed model-selection evidence.
4. Define common unadjusted metrics, false alarms on held-out normal data, event recall, missed attacks and delay with explicit units/denominators. State whether PR area is average precision or trapezoidal integration. Do not silently use point adjustment.
5. Write synthetic unit checks for state/residual equations, KL numerical behavior, data/window separation, score-label alignment and calibration independence. Label these as software tests, not benchmark results.
6. Only after authorized implementation, use an isolated water environment, pin dependencies and record a small pilot configuration. Record seeds, raw/split hashes, software/hardware, revisions, command, working directory and logs. Obtain approval for paid or lengthy runs.

Final attack evaluation occurs after all baseline and proposed-method development is frozen. Any redesign prompted by those outcomes becomes exploratory and needs fresh confirmatory evidence.
