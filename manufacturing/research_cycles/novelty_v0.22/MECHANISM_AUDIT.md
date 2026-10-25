# Independent mechanism and evidence-feasibility audit

24 October 2026. Manufacturing only. AI-assisted local code/algebra review by the `mechanism_audit` child agent, applying the academic research skill's assumption-challenger guidance. This is not human peer review, a fresh literature search, a benchmark execution or a novelty certificate. The root owns the literature synthesis and scientific decision. No raw real-world signals, fresh synthetic campaign, protected tests, training checkpoints or vendor files were opened or changed by this audit.

## Decision in brief

**Do not admit “subtract the protected reference, then retrain RAPT” as the original mechanism.** Reference subtraction can improve an inductive bias, but it is an invertible coordinate change when the reference remains known. It does not remove observation-conditioned prediction, learned variance or recurrent-state absorption. The exact unchanged-score counterexample below disproves any general guarantee based only on that transformation.

The observed RAPT behavior remains a useful research lead. Its explanation is not isolated: conditional mean, conditional variance, extreme-value calibration, task shift and training adequacy all remain viable contributors. A short, no-fit diagnostic on already exposed episodes could separate them, but has not been run here. Broad novelty for protected prediction or a contractive residual adapter is not established; the latter has a very strong simple leaky-AR control.

## Evidence inspected

- Released RAPT `rapt/model.py` and `rapt/detector.py`, pinned revision `d745668ffdb0e26877b1de4c9b2126af7bda5b03`, already admitted under `../baseline_admission_v0.20/`. The complete selected files were read. [Author model source](https://github.com/csiro-robotics/RAPT/blob/d745668ffdb0e26877b1de4c9b2126af7bda5b03/rapt/model.py), [detector source](https://github.com/csiro-robotics/RAPT/blob/d745668ffdb0e26877b1de4c9b2126af7bda5b03/rapt/detector.py). This review used the local pinned bytes; it did not independently refresh the repository online.
- `../rapt_protocol_v0.21/config.json`, `protocol21.py`, `RESULTS.md` and `exploratory/{PROTOCOL,RESULTS}.md`. These are saved protocol/results, not new measurement access.
- `../context_recovery_v0.19/{sim19.py,mechanism19.py,config.json}` and the import/generation path in `io19.py`/`worker.py`.
- Metadata decisions only: `../evidence_admission_v0.15/DECISION.md`, `../baseline_admission_v0.20/PUBLIC_RELEASE_CONTRACT.md` and `../../docs/DATASET_IDENTITY_REGISTER.md`.

## What the released model can absorb

In forward mode, the released detector predicts observation at t using the previous measured observation and protected action at t−1, plus a GRU state. `RaptDetector.step` updates its stored preceding observation each tick and passes the returned GRU state to the next call. Model weights remain fixed. Calling this “online training absorbed the attack” would be incorrect: these are inference-state and input-conditioning changes.

The same network produces both a mean and diagonal log variance, with log variance clamped to [−6,6]. Its released per-channel score is

\[
s_{t,j}=(y_{t,j}-\mu_{t,j})^2\exp(-\ell_{t,j}).
\]

The training loss is half the mean of this standardized square **plus** log variance; the deployed score omits the latter. This is an established paper/code correspondence difference, not a demonstrated bug or a new algorithm merely waiting to be renamed. Both mean and variance depend on measured history. A declining score could therefore arise from a shrinking prediction discrepancy, an increasing predicted variance, or both. Saved standardized squares alone do not identify these effects.

The local threshold is calibration maximum plus twice its maximum-minus-median spread; global threshold is maximum row-mean score plus three row-mean standard deviations. These are not a prospective pointwise false-alarm-rate guarantee. A task-dependent large calibration error can widen a threshold, while another task can still have false alarms. The optional range gate uses a buffered coordinatewise calibration box, which can miss a motion value that is plausible somewhere in the task but wrong for the present command/phase. In the completed replay, that gate added no detections.

The 100-epoch training run selected epoch 14 on normal development; later training loss improved while development loss deteriorated markedly. Completing all epochs resolves a CPU-truncation concern but does not establish adequate generalization, calibrated variance or a representative training population. Q1 has one fitted seed; L19 and S19 outcomes cannot establish an architectural defect on the original humanoid application.

## Algebraic counterexample: reference subtraction is insufficient

Let r_t be a protected reference derived without current untrusted observations, and define z_t=y_t−r_t. Given any original predictor with mean μ_t=f(y_history,u_history) and variance Σ_t, define a transformed predictor

\[
g(z_{history},u_{history},r_{history})
=f(z_{history}+r_{history},u_{history})-r_t.
\]

Then z_t−g=y_t−f exactly. With the same transformed variance, the standardized square and Gaussian likelihood are unchanged. Translation has unit Jacobian. This is an equivalence/existence argument, not a claim that independently trained neural networks converge to identical weights. A finite network trained on residuals may be easier to optimize or transfer, which is an empirical hypothesis. It does not receive a general non-absorption property from the coordinate change.

If the model does not receive enough reference/command context to invert the transformation, the transformation may discard information. That still does not establish a new source of security evidence. A residual GRU can learn “predict the next residual from the previous residual,” preserving a constant unauthorized offset as an ordinary predictable level.

For a fitted linear conditional model y_t=A y_(t−1)+B u_(t−1), a constant displacement δ produces prediction-error contrast (I−A)δ. Components in the null space of I−A are invisible to that one-step innovation; nearly integrating directions attenuate the contrast. The ordinary direct protected-reference difference retains δ. This explains a possible mechanism but does not prove RAPT's fitted nonlinear gain is near one. A local Jacobian approximation gives the corresponding first-order relation; finite offsets require finite-difference or full nonlinear tests.

## The contractive residual-adapter candidate

The root proposed a command-only nominal b_t plus an observation-residual adapter A with certified sequence infinity-norm gain κ<1. For e_t=y_t−b_t, prediction is b_t+A(e_history,u_history). Under the same commands and a paired constant residual displacement δ, the adapter difference is bounded by κ||δ||, so the innovation contrast is at least (1−κ)||δ||. This is a coherent conditional bound.

Three qualifications are essential:

1. It bounds the **difference of two innovations**. Absolute attacked innovation obeys only a bound such as `(1−κ)||δ||−||innovation_normal||`; alarm detection additionally needs normal mismatch, noise, threshold and uncertainty assumptions. A nominal bias can cancel the attack effect. A variance head depending freely on attacked history can erase the score implication even if the mean contrast is bounded.
2. The gain must cover the complete history-to-output map, its initialization and norm/scaling. Spectral normalization of individual linear layers does not by itself certify a recurrent GRU with gates, layer normalization, residual blocks and infinite history. Finite horizons and reset boundaries need explicit treatment. A time-varying attack gives a term resembling `||δ_t||−κ max_history ||δ_s||`, which can be negative during recovery; constant-offset results must not be advertised as universal transient guarantees.
3. **A scalar leaky residual predictor already realizes this property exactly:** `prediction=b_t+κ(y_(t−1)−b_(t−1))`. Its innovation is `e_t−κe_(t−1)`, with DC gain `1−κ`. This ordinary residual AR filter interpolates between a direct reference (κ=0) and differencing (κ=1). A constrained multivariate AR correction, normal-selected fixed-gain/KF reference and the command-only model are indispensable controls.

Consequently a possible contribution is a carefully justified, operationally useful restriction on adaptation with measurable benefit, not the generic inequality or the existence of protected prediction. A neural version must beat the simple constrained residual controls on the declared benefit at the same tolerated costs. If a leaky AR matches it, complexity has not earned a method contribution. The root's primary-source prior-art review must decide overlap with fault-sensitive/robust observer design and Lipschitz-constrained predictors before admission.

## Most discriminating next diagnostic — proposed, not run

Use the already fixed checkpoint and exposed Q1 population, preserving both released modes. Do not tune or rank a new winner on these outcomes. Save means and log variances, which are currently confounded inside scores. Keep one actual-history branch and a second **protected-reference-history** branch. The reference must come from an admitted normal-trained model or operational command path; simulator counterfactual truth cannot become a detector input.

For each timestep, evaluate a 2×2 factorial diagnostic on the same actual target:

| Prior observation input | Incoming recurrent state | Interpretation |
|---|---|---|
| Actual preceding observation | Actual-history state | Released prediction. |
| Protected preceding reference | Actual-history state | Effect of immediate observation conditioning, conditional on real history. |
| Actual preceding observation | Protected-history state | Effect of recurrent history, conditional on real preceding observation. |
| Protected preceding reference | Protected-history state | Combined removal of observed-history conditioning. |

Maintain the two recurrent states from episode start. Intermediate crossed calls must not update either persistent branch. Never reset at known intervention onset/offset. Crossed states/inputs can be outside the model's training support, so this is a mechanistic intervention diagnostic, not a fair detector comparison or automatically an improved architecture.

For each branch preserve raw squared errors, log variances, standardized squares and released gate ratios separately. Score the same mean with (a) its own variance and (b) a frozen normal-derived per-channel scale for diagnosis. Differences between these readouts reveal variance suppression; they do not license selecting the more favorable final score. Also report command/phase strata and normal versus authorized-change episodes, including every miss. The existing older ARX reference has a different training history from RAPT; using it here can be exploratory, but a main comparison requires refitting everything under one common normal contract.

Essential falsifiers:

- If protected-history means remain inaccurate or low-risk because the model is poorly calibrated on the task, recurrent absorption is not isolated as the primary cause.
- If raw error remains large but score drops as variance increases, a history-only explanation is incomplete.
- If direct reference or ordinary normal-selected constrained AR/KF achieves the same detection/benign tradeoff, an elaborate neural branch is unnecessary.
- If improvement comes only from adding a trustworthy command/reference unavailable to the baseline, report an information-access advantage, not a method advantage.
- If authorized transitions fail because the command-conditioned reference is wrong, a successful offset fixture cannot establish a usable monitor.

## Additional identifiability and evaluation limitations

The simulator's attacker changes executed desired motion while the monitor receives the untouched approved trajectory. Measurements remain truthful. Authorized changes update both executed and approved commands. This supplies a useful protected-intent distinction by design, but it is not established for every public recording. The q/v command channels are desired state, not measured actuator torque or necessarily RAPT's original policy action. A model failure under this transferred action semantics does not contradict its original benchmark result.

The same physical deviation can be produced by a fault, load change or malicious command modification. Without independent command provenance or attack evidence, a state discrepancy can support a departure-from-intent claim but cannot attribute malicious causation. If both trusted intent and independent observations can be spoofed identically, no discrepancy-only algorithm restores identifiability. This must be a threat-model boundary, not an untested promise of “cyber resilience.”

Recovery must distinguish ending the injected command corruption, first entering the physical tolerance, staying inside it for a specified period, and permanent convergence. No finite history can certify permanent future recovery without assumptions about future disturbance and plant behavior. The existing physical-return diagnostic is an evaluator definition, not a detector guarantee.

## Independent-evidence feasibility from existing metadata

| Source | Useful support | What remains unavailable/unproven |
|---|---|---|
| Original CASPER | Real manufacturing acquisition and documented changed-operation intervals; earlier study exists. | Main held-out recording is already exposed; clocks differ, IMU lacks exact timestamps, labels are schedules rather than independently measured recovery truth. This is not fresh confirmation of a redesigned method. |
| Original voraus-AD | Separate six-axis robot acquisition; measured/target channel schema and normal/fault executions; original test signals still closed. Can support normal reference adequacy or a separate fault-detection comparison after a feature/split contract. | Physical/process faults are not cyberattack labels; protected command provenance, attack onset and physical-return truth are not established. MVT-Flow is offline and cannot be treated as an online recovery comparator without a disclosed redesign. |
| Original FactoryNet subsets | Potential command/measurement/context schema and an additional laboratory source. | Only metadata admitted; no observations downloaded. Some subsets repackage voraus-AD/AURSAD, some channels are missing, fault labels can leak through context, newer synthetic campaign absent from the pinned snapshot. No authenticated command channel or recovery truth is established. |
| RAPT G1 release | Potential original-system detector replay, with author code and metadata contract. | Humanoid faults/OOD are not industrial-arm cyber recovery; real onsets are unknown and some cases are extremely short. Current metadata do not admit the desired recovery claim. |

A new synthetic mechanism study can falsify a candidate and test stated assumptions cheaply. It does not solve the independent real-world cybersecurity/recovery evidence gap. Keep separate evidence tracks and do not pool their scores or reinterpret fault labels to create a desired benchmark.

## Executed tiny algebra checks

`mechanism_algebra.py` uses Python's standard library and deterministic scalar examples only. It checks exact score invariance under a conjugate protected-coordinate transformation, attenuation `(1−A)δ`, variance-driven score suppression, and a value lying inside a global box while displaced from present intent. Seven assertions passed. These are mathematical/software counterexamples, **not RAPT inference, robot simulation or benchmark performance**.

Command and working directory:

```sh
# cwd: /Users/matrixusman/CUI/DigitalTwin/manufacturing
python3 research_cycles/novelty_v0.22/mechanism_algebra.py
```

`mechanism_algebra_receipt.json` records the script hash, deterministic settings, interpreter/platform, Git revision/dirty state, timestamps, runtime and values. An initial receipt incorrectly counted eight assertions although the seven assertions all passed; it is preserved as `mechanism_algebra_attempt_001.json`. The count was corrected and the same arithmetic rerun. No substantive formula or result changed. No external dependencies, data access, random seeds, fitting, raw outputs or new final observations were involved. This subsecond software demonstration was not a monitored research campaign and supplies no resource extrapolation for neural training.

## Strongest reviewer objection

“The proposed detector is a familiar protected-reference or residual-filter construction evaluated on a simulator that supplies perfect trusted intent and evaluator-only counterfactual truth. Its apparent benefit over a conditional predictor may reflect extra information, different training populations, variance/calibration choices or an ill-suited action interface. Where is the contribution beyond a normally tuned constrained AR/KF reference?”

The research design must answer that objection before another final campaign. The current audit supports a precise mechanism-discrimination step and rejects an unsupported coordinate-change novelty claim; it does not admit a new superior detector.
