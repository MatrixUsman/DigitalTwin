# Proposed reproduction plan

Status: **proposal only**, 2026-10-16. Author materials and a pinned CAROTS source snapshot have been [collected](../baselines/README.md); no model implementation by us, scientific environment, experiment, benchmark score, or training run has been produced. Acquisition utilities are not model implementations. This document does not authorize lengthy runs.

Project: `water`, owner Muhammad Usman. After the three-project reorganization, all relative runtime paths resolve from `water/`. Source/checkpoint/environment isolation is governed by the [shared instructions](../../AGENTS.md) and [local status](../STATUS.md).

The [detailed water roadmap](RESEARCH_ROADMAP.md) breaks this proposal into numbered tasks and completion criteria. The sequencing clarification below reserves final held-out scoring until baseline and proposed-method development are complete.

## 1. First baseline and admission criteria

**Start with CAROTS and CAROTS-dagger (contrastive score without the forecasting-error ensemble).** It has an ICML 2025 publication, both target datasets, and inspectable author code. See [evidence and code permalinks](literature/CAROTS_AND_INFORMATION_THEORETIC.md). Select both variants in advance; do not choose the weaker variant or select the winner after looking at test labels.

This is conditional, not a claim that the repository runs on this machine. Resolve before training:

1. Authorized SWaT/WADI release manifests and file/label alignment.
2. Upstream commit and actual modified non-commercial license; exact dependencies and any portability patch.
3. Hardcoded CUDA paths on the available Apple hardware. CPU first for correctness; MPS only after compatibility/determinism checks. Remote or paid compute is not authorized.
4. Test-label threshold optimization **and** the separate oracle-best-F1 reporting path. Disable both; calibration and report generation must use the frozen project protocol.
5. Potential SWaT first-row alignment issue, writes into input directories, downsampling/label aggregation, and gap handling. Static concerns are not yet confirmed runtime defects.
6. Published Appendix B specifies gradient clipping 1.0, while pinned code defaults to 0.5. Resolve and predeclare the intended setting without test-based selection. The 51/49-feature repository issue remains an unconfirmed user report. See the [expanded pinned-code audit](literature/EXPANDED_SEARCH_2026-10-16.md).
7. The [deeper CAROTS audit](../baselines/carots/VERIFICATION_REPORT.md) identifies broken ratio-threshold wiring, config-clone misuse for inference loaders, fresh/cached causal-checkpoint differences and a conditional singleton-batch shape issue. Simply changing the threshold setting is insufficient. Resolve each in a declared adapter with meaningful synthetic tests before real-data runs.
8. The [method-to-code study](../baselines/carots/METHOD_TO_CODE.md) additionally finds CPA noise outside the forecaster's input history and global-pair SOC weighting instead of the paper's per-anchor average. It also records configured-but-unused graph grouping/temperature settings and dataset-specific configuration overrides. Specify the intended behavior before implementation; use small synthetic dependency/unequal-partner fixtures to check the consequential differences. No runtime effect has been measured.

Call evaluation-only changes **author-code CAROTS under a modified evaluation protocol**, with an explicit deviation ledger. Corrections to CPA, SOC or discoverer semantics introduce additional algorithmic differences; identify those separately and never label them an unchanged author-code run. Published best-F1 values are reference claims, not targets we may reach by tuning on the test set. If faithful reported-score reproduction requires violating the held-out-label rule, do not perform that part.

IT-DT is a later compact twin-method candidate, currently a preprint without verified author code or complete protocol. A manuscript-based implementation would be **our reimplementation**. CDT and the ensemble need matched code and clarification; DPDGAD needs accessible full text and code evidence. Do not make the first milestone depend on these unresolved artifacts.

The [current learning selection](BASELINE_SELECTION_REPORT.md) retains CAROTS, IT-DT and the ensemble. New contamination/context/shift references inform question refinement, but do not expand this proposed implementation scope or authorize additional runs.

The later [verification report](BASELINE_VERIFICATION_REPORT.md) adds material IT-DT/ensemble figure, mathematical, protocol and bibliography concerns. Preserve them as critical-reading sources; do not treat their displayed scores or formal guarantees as validated targets for a reimplementation.

## 2. Minimal structure to create in the next phase

Documentation and folder-purpose READMEs exist now; the shared `.gitignore` and skill live at the workspace root. The following functional code/data files are **proposed**, not implemented:

```text
DigitalTwin/water/
  PROJECT_BRIEF.md
  AGENTS.md
  STATUS.md                     # current evidence, blockers and handoff
  README.md
  docs/                         # evidence, protocol, decisions, deviations
  pyproject.toml                # research package + explicit dependency groups
  requirements/                # validated, hashed platform/method locks
  configs/
    datasets/                  # release/schema and label rules, no private URLs
    protocols/                 # splits, score cadence, calibration, metrics
    methods/                   # CAROTS, CAROTS-dagger, later twins
  src/water_twin/
    data/                      # schemas, read-only loaders, manifests
    splits.py                  # chronological boundaries and window eligibility
    preprocessing.py           # fitted training-only transforms
    calibration.py             # normal-calibration thresholds
    metrics.py                 # point/event metrics and explicit denominators
    baselines/                 # thin, traceable method adapters
    experiment.py              # config validation, provenance, local logging
  tests/
    fixtures/synthetic/        # tiny authored fixtures, clearly labelled
    test_loading.py
    test_splits.py
    test_calibration.py
    test_metrics.py
    test_provenance.py
  baselines/vendor/            # ignored, pinned upstream checkouts
  datasets/raw/                # ignored, immutable authorized originals
  datasets/processed/          # ignored, derived files keyed by hashes/config
  experiments/runs/<run_id>/   # ignored logs/config/metrics/scores/checkpoints
  local/                       # ignored access records and private paths
  .venv/                       # ignored harness environment
  .venv-carots/                # optional separate method environment
```

Use a small package plus command-line entry points; no UI, database, deployment service, or experiment SaaS. Raw files may instead live on an authorized external volume. Private paths belong in ignored local configuration. Do not materialize all overlapping windows in RAM. Upstream code should never receive writable raw-data paths for conversion caches.

## 3. Isolated environment proposal

Use the already available **Python 3.11.17** for the initial harness, subject to a dependency resolution check. Avoid modifying Homebrew, Miniconda base, or other projects. Python's `venv` provides package isolation; do not enable system-site packages. [Official venv documentation](https://docs.python.org/3.11/library/venv.html)

Interpreter and machine observations come from the initial audit; recheck them, free disk and available memory before acquisition or installation. No dependency/device compatibility has been established by this proposal.

After implementation is authorized, the proposed creation command is:

```sh
/opt/homebrew/bin/python3.11 -m venv .venv
```

Not executed in this audit. Proposed minimal dependencies: NumPy, pandas, scikit-learn, pytest; add openpyxl only for received XLSX files. Add SciPy or PyTorch only when the chosen implementation requires them. Avoid unnecessary plotting/notebook/experiment-server packages initially. Exact versions are **not yet validated or locked**; an untested version list would give false reproducibility confidence.

Audit upstream imports and documented versions, resolve compatible ARM/macOS wheels in the isolated environment, then record the complete installed dependency graph and hashes. Keep a separate baseline environment if it needs a different interpreter or conflicting versions. A Linux/CUDA lock, if eventually required and authorized, must be separate from a macOS lock. Check the [official PyTorch platform guidance](https://pytorch.org/get-started/locally/) when selecting its version; no GPU acceleration or runtime is promised.

## 4. Freeze the common protocol before test evaluation

The values below are proposed defaults to be confirmed from actual release metadata, then frozen before test scores are inspected.

| Decision | Proposed rule |
|---|---|
| Release | Same authorized SWaT files and same authorized WADI files for every main comparison; choose after manifest verification. |
| Model scope | Fit a separate model per dataset. Evaluation on both datasets is not cross-dataset transfer. |
| Inputs | Same eligible telemetry and time coverage. Remove labels, IDs and timestamps from predictive features; retain timestamps/IDs separately for alignment. Any verified physical metadata used by twins is recorded as extra information. |
| Normal chronology | Split normal recordings by elapsed timeline into 60% fit, 15% model-selection validation, 15% threshold calibration, 10% held-out normal evaluation. Resolve exact timestamps, gaps and startup exclusions before freezing. |
| Attack test | Keep the selected official attack recording untouched. Its labels are available only to the final scorer, never the model/gate/calibrator. |
| Preprocessing | Fit scalers, imputers and feature eligibility on the fit partition only. Apply frozen parameters elsewhere. Train-only constant/all-missing features and release-required exclusions are logged. No backfill or interpolation using future samples. |
| Window isolation | Split first; every input/target window must lie in one contiguous partition. Exclude any window whose lookback/horizon/filter support touches another partition or a gap. Record discarded rows and scoring coverage. |
| Selection | Predeclare hyperparameters or select using normal-only validation objectives. No anomaly-F1 selection without independently designated development attacks; none are currently available. No repeated adaptation after inspecting test performance. |
| Threshold | Fit once using the designated normal calibration scores. Initial proposal: empirical 99.5th percentile with a declared quantile method and strict `score > threshold` decision. The nominal 0.5% calibration exceedance is **not** a guarantee of held-out point or event false-alarm rates, especially under dependence or distribution shift. |
| Main score grid | Shared causal five-second bins, subject to release cadence verification. Aggregate only completed bins; timestamp the score at the bin end. Every method must emit one aligned score per eligible bin after warmup. |
| Labels on common grid | A bin is positive if it overlaps a documented attack interval; preserve original labels/intervals. Never median labels. Exclude incomplete bins consistently and document missing/overlapping labels. |
| CAROTS compatibility | Retain its published factor-five feature aggregation where applicable, but audit feature types and exact cadence. Common endpoint alignment and OR/interval labels are explicit deviations from any upstream median-label/window-label protocol. |
| Real-time interpretation | A score assigned to a bin or trailing window becomes available only at its end. Never credit a retrospective window score as an earlier alarm. Detection delay uses timestamps, including aggregation latency. |
| Seeds | Proposed fixed seeds: 0, 1, 2 for eventual repeated training. A bounded pilot uses 0 only and is not a full benchmark result. Record all randomness sources and device determinism settings. |

Before observing scores, derive a **common evaluation mask** from the maximum declared lookback/horizon/filter support across methods, timestamp availability, release gaps and bin completeness. Use that same mask for main point-metric denominators and normal-time exposure. Report each method's additional usable coverage separately; never mask observations based on scores or errors. Adding a later method with longer warmup requires a newly versioned mask and rescoring all comparisons, not selective removal of difficult intervals.

The 60/15/15/10 split changes upstream training coverage. It protects a separate clean calibration and normal-evaluation segment; report it as a protocol deviation and use it consistently. If raw data make these splits unsuitable, revise once using metadata/development data, record why, and freeze again before test access. Do not substitute test data for missing validation.

Separate two records: (a) a paper-to-code fidelity checklist of the original method and (b) our common evaluation configuration. Do not blend original published scores, original window-level oracle scores, and common-grid operational scores in one ranking.

## 5. Metrics and test specifications

Main comparison: **event recall at the predeclared calibration rule**, accompanied by observed alarm-onset frequency on held-out normal data. Report missed-event counts and delays jointly. Also report unadjusted point precision/recall/F1, average precision (AP), actual point FPR `FP/(FP+TN)`, and optional ROC-AUC where both classes exist. AP and trapezoidal PR-AUC are different; name the implementation and version. No point adjustment or optimal-test threshold in the main report.

Define an event from provider attack annotations, not by merging arbitrary positive samples after seeing scores. Proposed detection is the first newly raised alarm within the event interval; a pre-existing alarm is not a new detection. Report persistent-alarm coverage separately. No post-event grace period by default. Alarm episodes are contiguous positive decisions; any hysteresis, cooldown or merging rule must be chosen in advance on development data. False alarms/hour count alarm onsets during eligible normal time divided by actual eligible normal duration; exclude gaps. Report normal point exceedance too, so one long alarm cannot look harmless by episode count alone. Overlapping attacks and zero-duration intervals require an explicit manifest policy before scoring.

An attack that ends before the first eligible bin-end score has **zero detection opportunities** under this strict deadline. Retain it in the primary all-event denominator as undetected and report the zero-opportunity count/reason separately; do not silently exclude it or add retrospective grace. Also list events affected by warmup or gaps so temporal resolution is visible. Any secondary opportunity-conditioned recall must have its own denominator and label.

At an independent recording/partition boundary or an unobserved gap, terminate the previous alarm episode. Reset detector history as specified by the frozen method adapter, reacquire warmup, and initialize alarm state to clear at the first eligible decision. A positive first decision creates a new episode. Never bridge an episode across missing observation time. This conservative counting rule and all resets must be identical across compared runs.

For detected events, delay = first eligible alarm time minus event start. Report misses separately and denominator totals; never replace missed-event delays with zero. Initial compute metrics: wall time, peak memory, and latency on the actual local device, separating preprocessing, training, inference and any adaptation.

| Proposed test | Acceptance condition |
|---|---|
| Synthetic fixtures | Hand-authored data carry `synthetic=true`; tests do not require private files or network. No fixture scores enter benchmark tables. |
| Loaders | Known synthetic CSV/XLSX schemas parse correctly; metadata/labels excluded from features; WADI sign mapping and SWaT string mapping tested; unknown labels fail clearly. Raw byte hashes remain unchanged. |
| Time integrity | Declared timestamp parsing handles date ambiguity; duplicates, regressions and gaps are rejected or handled by an explicit policy; no silent sort/drop/interpolation. |
| Label alignment | Timestamp IDs remain paired through header removal, startup trimming, missing rows, downsampling and windows; a one-sample synthetic attack survives common-bin OR labeling. This catches the CAROTS first-row concern. |
| Chronological isolation | Train, validation, calibration and test row IDs are disjoint and ordered; no input/target/filter window crosses a boundary or gap, including horizon/lookback edge cases. |
| Leakage resistance | Changing held-out values/labels leaves **offline** fitted transforms, feature selection, selected checkpoint and initial calibration threshold identical. Test-label arrays are rejected by training/calibration interfaces. Future authorized online adaptation may respond to past unlabeled observations under its frozen rule; test it separately for causality and label independence. |
| Causal operation | Perturbing future samples cannot change an earlier score. Prediction precedes update. A synthetic attack label cannot influence the gate. |
| Calibration | Tied-score quantiles and strict-threshold behavior are deterministic; the threshold is fixed before scoring; all-normal calibration requires no attack labels. |
| Point metrics | For synthetic `y=[0,0,1,1]`, predictions `[0,1,1,0]`: TP=FP=FN=TN=1; precision=recall=F1=FPR=0.5. Test all-normal/all-attack, no alarms, ties, masks, and empty inputs. Undefined metrics return explicit N/A with counts, not misleading perfect values. |
| Event metrics | Synthetic annotated intervals exercise exact boundaries, overlaps, late alarms, persistent alarms, misses and gaps. Verify no double counting and delay in seconds rather than row index. |
| Ranking metrics | Check small known rankings against the named reference library; AP and trapezoidal PR-AUC have different keys. Never compute max-F1 as operational F1. |
| Provenance | A run without dataset/split hashes, config, seeds or code revision is marked incomplete; changing preprocessing changes its identity. |

These are **test specifications**, not tests already written or passed. Later integration tests using authorized data should be opt-in and local. Do not broaden testing into training until these invariants hold.

## 6. Staged execution and stop conditions

1. **Resolve inputs:** authorized access and exact manifests; missing original literature/code details; common protocol and deviation ledger.
2. **Authorize minimal implementation:** isolated environments, loaders, manifests, evaluator and synthetic tests; pin upstream source. No model claim from synthetic data.
3. **Authorize bounded pilot:** proposed ceiling is one seed, one small normal-data subset, one epoch, CPU, at most 10 wall-clock minutes, with an explicit stop timer and logged resource use. This is a proposal for a later instruction, not permission to run it now. Stop on data leakage, mismatched labels, raw writes, excessive RAM or unsupported device operations.
4. **Budget full baseline:** use pilot measurements to propose exact datasets, variants, three-seed configurations, time/memory estimates and storage before any lengthy or paid run. Obtain approval. Do not invent runtime estimates from hardware specifications.
5. **Develop comparisons before final-test access:** establish baseline fidelity on fit/development data and synthetic software checks. Define trusted inputs and the protected update type, then develop the fixed twin, ungated adaptive twin, guarded twin and relevant ablations using permitted development evidence. Keep unchanged benchmarks separate from synthetic corruption/measurement-shift tests; resolve the evidence for legitimate physical changes early. Neither baseline test failures nor proposed-method test scores may guide this design.
6. **Freeze all variants, then evaluate:** complete method, selection, mask, calibration and analysis decisions before scoring held-out normal and attack sets. Preserve outputs locally with full provenance and report every predeclared variant/seed, including failures. If final-test outcomes inform a subsequent redesign, label it exploratory and obtain independent confirmation evidence for confirmatory claims; rerunning on the same attacks or changing seeds does not restore an untouched test set.

Every reported run should retain: run ID; seeds; exact command; resolved config/hash; raw/split/preprocessing hashes; our revision and dirty patch; upstream commit and patches; interpreter and dependency lock; OS/device/thread settings; timestamps; stdout/stderr; score/label alignment metadata; calibration rule; metrics with denominators; timing/memory; and outcome/failure reason. Logs must not expose raw records or private links. The workspace now has a private Git repository; no implementation or experiment revision exists yet. Use the actual code revision and dirty patch when later experiments are authorized.

## 7. Blockers at audit close

| Blocker | What resolves it |
|---|---|
| No dataset files or confirmed access | Authorized official files plus release/readme/attack-table manifests |
| Request submitted; provider approval and authorized download pending | The user supplied a student university address and explicit agreement/consent. The assistant submitted once and observed website confirmation on 2026-10-16; see the [request record](DATASET_REQUEST_PREPARATION.md). Inbox delivery, approval and download access remain unverified |
| Researcher reading and some implementation specifications unresolved | All three selected full texts are collected and [assistant study guides](PAPER_STUDY_GUIDE.md) are prepared. Researcher reading remains unconfirmed; the original background architecture attachment is still unavailable and needed only if that separate paper is audited |
| CAROTS forbidden metric paths, possible alignment issue, CUDA assumption | Static review followed by meaningful synthetic/integration tests and recorded patches after implementation authorization |
| Other comparators lack full text, author code or sufficient protocol | Verified matched artifacts/clarifications; author contact only if explicitly authorized |
| No evidence that benchmark shifts represent legitimate change | Documented regime annotations or separately validated simulation; otherwise limit claims to detection and labelled stress tests |
| Limited free disk and unknown runtime/MPS compatibility | Measure authorized pilot and actual data sizes before allocating long runs |
| Novelty overlaps prior gated/adaptive work | Mechanism-by-mechanism prior-art comparison and a testable distinguishing claim, after baseline reproduction |

**Current stopping point:** collection, source audits and assistant method-to-code studies are prepared; no substantial implementation or training. Next: researcher-owned CAROTS explanation and a concrete correction/deviation specification, while awaiting authorized dataset receipt. No novel model or results section is ready for approval.
