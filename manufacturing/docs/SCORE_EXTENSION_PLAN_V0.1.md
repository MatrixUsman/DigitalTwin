# Bounded normal-only observer score extension, v0.1

## Material Passport

- Project/owner: manufacturing / Haiqa Mushtaq. Declared 17 October 2026, Asia/Karachi, before real extension replay.
- User authorization: implement and test the four explanatory scores through a separately versioned bounded normal-only extension. This scope includes one guarded normal-development replay after passing synthetic/preflight checks; no fitting, calibration, final tests or additional data acquisition.
- Skill: shared academic-research-suite experiment-agent run/verification guidance, bounded to this implementation. The explicit coding/resource request governs script creation and enforced resource stops. No redundant confirmation, automatic pipeline or external model calls.
- Status at declaration: plan, not a completed experiment. Preserve this document/configuration once execution starts; report actual results separately.
- Input evidence: [scope decision](CONTRIBUTION_AND_EVIDENCE_SCOPE.md), [eleven-variant roster](COMPARISON_ROSTER_DECISION.md), frozen original-CASPER data/evaluation contracts, selected controls and observer v0.1 artifact registry.

## Question and exact scope

Can the four explanatory scores C/K/L/Rv be computed causally, finitely and reproducibly over the entire permitted normal-development support using the **unchanged fitted observer**, with exact preservation of the original R/RC outputs? This tests software, alignment and bounded execution. It does not select a best score, tune a threshold, measure attack performance or establish a contribution.

The existing reference, scaler, period, 32 bins, transition/diffusion, warmup, training-fitted bandwidth and positive R/C scales stay immutable. No parameters or thresholds are fitted in this extension. Previously selected template bins already used this development partition; this replay is further **developmental reuse**, not independent validation or a new holdout.

## Inputs and access boundary

Load the model identified by `experiments/OBSERVER_ARTIFACTS_V0.1.json`, pinned configuration, source-run manifest and selected-control registry. Verify all file/state identities required by the runner before use and again at completion. The new configuration binds this document and the frozen dependencies by SHA-256. Preserve old source/configuration bytes, models, plans and consumed attempt records.

Only the original right-arm file may be read, read-only. Parse the development raw-row interval **[540002,702002)**: **162,000** observations, yielding exactly **160,472** scored endpoints **[541530,702002)**. Zero-based data rows exclude the CSV header; intervals are half-open. The first 1,528 observations initialize state only. The reader may traverse the preceding CSV records for positioning but must not parse, retain, fit or summarize their features. Source-byte identity hashes may scan the whole file without feature parsing; record hashing, traversal and selected parsing separately. Do not consume the record at exclusive stop 702002.

The frozen gap rule remains `dt<=0 or dt>0.075 seconds`; unexpected gaps or support changes fail this fixed-support extension instead of trimming the denominator. No attack-boundary or label resets. Models receive only `Observation(q,qdot,dt)`; coordinates/timestamps remain evaluator metadata. Calibration [702002,864003) and both final slices [864003,1762650) stay closed. No other CASPER member or new dataset is allowed.

## Scoring and causality

For each selected observation, prepare standardized features and template distances once. The existing synchronized `PhaseObserver` creates one immutable proposal: propagate past state with actual dt, predict before the current target, and propose a posterior without state mutation. Compute every admitted score from that same proposal/prepared observation, emit aligned scores, then commit the proposal once. Warmup commits observations without emitting scored endpoints. A score exporter must never alter the reference, proposal or state transition.

Let `p` be predicted phase weights, `u` proposed corrected weights, `m_k` standardized 12-channel templates, `z` the current observation, `D_k=||z-m_k||²/12`, and `τ` the pinned bandwidth. The weights obey `u_k ∝ p_k exp(-D_k/(2τ))`. The six outputs are:

| ID | Definition | Role |
|---|---|---|
| O-R | Existing `R/a`, `R=||z-Σp_km_k||²/12` | Historical principal reference; exact arithmetic preserved |
| O-RC | Existing `R/a+C/b` | Historical principal alternative; exact arithmetic preserved |
| O-C | `C=JSD(p,u)` using natural logarithms | Correction-only explanatory control |
| O-K | `K=Σ u_k[log(u_k)-log(p_k)]` | Classical posterior-to-prior KL surprise |
| O-L | `L=-log Σ p_k exp(-D_k/(2τ))` | Predictive mixture energy, not a calibrated observation probability |
| O-Rv | `mean_velocity_j (z_j-Σp_km_kj)²`, six velocity channels | Prospective velocity mismatch using the same full-input state |

Existing positive training-only means `a,b` are loaded, not recomputed. New singleton C/K/L/Rv scores remain unscaled; later calibration, if admitted, will follow the same frozen rule for each. No score weighting, bandwidth, phase count, threshold, persistence or feature search occurs.

The frozen historical protocol's “progression-aware/omitted” labels map to O-RC/O-R. Both retain nominal progression and correction in state evolution; only the additional score term differs. Record this terminology-only mapping in the versioned execution manifest without editing the hashed historical protocol.

Rv can reveal direct velocity evidence. It does not independently identify alignment's causal effect or prove post-alignment residual suppression. C/K can be small for a poorly fitting but uninformative measurement, and large for a valid informative observation. None is attack probability or malicious intent. All claims remain within the [scope decision](CONTRIBUTION_AND_EVIDENCE_SCOPE.md).

## Numerical and synthetic validation

Compute L with stable log-sum-exp, not exponentiation of raw large negative energies. K uses differences of logarithms to avoid ratio overflow; zero posterior terms contribute zero. Reject nonfinite or negative energies, invalid shapes, unnormalized probability inputs or **any nonpositive prior support**. Do not add smoothing to make an invalid prior pass. Reject inconsistent prepared observations/proposals rather than scoring another model/update silently. All accepted scores must be finite and nonnegative, allowing only explicitly bounded floating-point roundoff handling documented in the implementation/configuration before admission.

Numerical constants: prior/posterior mass must differ from one by at most `1e-12`, without renormalization in the score helper. Prepared transform/distances, prior prediction/physical prediction, residual, synchronized posterior and JS consistency checks use `rel_tol=1e-12`, `abs_tol=1e-14`. A computed nonnegative quantity in `[-1e-14,0)` may be rounded to zero; more-negative or nonfinite results fail. Stable emission log weights preserve the existing `-.5*D/τ` arithmetic. The pure helper validates mathematical correspondence but has no mutable observer owner/generation access; the caller's existing propose/commit protocol rejects foreign/stale commits. These validation tolerances do not relax the **exact** historical R/RC and coordinate parity requirement.

Meaningful synthetic checks must cover independently calculated C/K/L/Rv arithmetic, KL orientation and zero terms, equal-distribution behavior, extreme energies and tiny positive prior weights, nonfinite/overflow/support rejection, and the identity `L=K+Σu_kD_k/(2τ)` within declared floating tolerance. Also check `Σp_kD_k=R+Σp_k||m_k-Σp_jm_j||²/12`, velocity indexing and a clearly labelled synthetic position-aligned speed-amplitude example. These artificial examples are software cases, not physical cyberattack simulations or benchmark evidence.

Integration tests must verify same-state score generation, exact R/RC parity, score-before-commit ordering, unchanged references, label/future-suffix independence, resets/warmup, split/gap isolation and no development fitting. Runner tests use synthetic artifact fixtures only: documentation/config/reference/score corruption, wrong populations, incomplete/nonfinite arrays, stale receipts, resource failures and exclusive attempt admission must fail visibly. The full test receipt must cover every current source/configuration file and the same isolated interpreter used for execution. Tests reject raw-data/network access.

No code/configuration change after a passing full receipt is eligible for real execution until necessary tests rerun and a new matching receipt is saved. Ordinary software fixes before first real execution are not retries of the real study.

## Resource bounds and reproducibility

One deterministic CPU worker attempt: **600 seconds wall**, **300 seconds worker CPU**, **1 GiB monitored RSS**, **50 MiB total run outputs**, one computational thread, no network, GPU/MPS or child computation. Sample RSS at intervals no greater than one second and check terminal peak RSS/CPU as well; sampled monitoring is not an instantaneous kernel memory ceiling. Enforce all limits with the existing tested supervisor. No automatic retries, budget extension or silent subset change. Preserve partial logs/artifacts and the consumed new attempt token after any real failure.

The previous 169.945-second observer study fitted bandwidth/scales and processed training plus development across multiple variants/diagnostics. This extension replays only development with one synchronized observer and six scores. That supports a bounded feasibility estimate, not a measured runtime promise. Before launching, test score cost with explicitly synthetic fixtures if needed and check local disk capacity. Do not install dependencies: use manufacturing's standard-library Python environment.

Proposed command, **not run at declaration**, cwd `manufacturing/`:

```sh
.venv/bin/python scripts/run_score_extension.py --execute --test-receipt local/software_validation/<matching-id>/receipt.json
```

Save configuration/documentation/contracts, exact code inventory and snapshots, dirty Git revision/patch, interpreter/dependency/platform/hardware facts, deterministic seed `null`, command/cwd, start/end times, logs/progress/resource samples, source/reference pre/post hashes and scope counts. Save six finite score arrays with one common coordinate array, score definitions and no-fit declaration. Preserve a readback validation and a separate internal saved-artifact audit. Row-level arrays and local receipts stay ignored; public-safe summaries must not embed dataset observations or score traces.

## Predeclared acceptance and reporting

Accept only if all of the following hold:

1. Every current implementation/configuration file matches a successful synthetic receipt and the configuration binds this plan and all required immutable inputs.
2. Exactly 162,000 selected normal observations are parsed and all **160,472** fixed eligible endpoints appear exactly once in order; no support masking, unexplained reset or protected observation access.
3. All six score arrays are finite, with documented numerical bounds; they share the same state trajectory by construction/tests. Fitted parameters and old model/run/plan identities remain unchanged.
4. O-R and O-RC match their prior saved development arrays **exactly at every endpoint**, and coordinates match the prior index. A tolerance-based match does not pass the historical-parity gate.
5. Readback matches hashes, lengths, coordinates and aggregate summaries. The manifest retains any failures; all actual resources and output size meet caps.

Report actual count, coverage/parity, descriptive score ranges/means, runtime/memory/storage and verification status, including negative findings. Means across differently defined scores are not performance rankings. Do not create hypotheses from their normal distribution, select a preferred score or compute final false alarms/attack metrics. Success completes score implementation and normal replay within the narrow study; it is not calibration admission, a paper reproduction, a validated physical twin or demonstrated security benefit. The next gate is complete executable-roster and calibration-runner admission under a separate scoped task.
