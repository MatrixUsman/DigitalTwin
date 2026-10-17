# Decision on CASPER comparison and the original contribution

17 October 2026. This responds to the request to demonstrate a defensible improvement and establish an original detector. Those remain research objectives. The completed pilot supplies a previously missing executable CASPER architecture; it does not supply either conclusion.

## What is now admitted

The corrected CASPER manuscript's Figure 11 and Algorithm 1 support an independently written four-convolution predictor with 755-observation history, trailing median preprocessing and aggregated prediction error. The Edge-2025 architecture supplies the compact 45-observation predictor. Both now run on the same nine external IMU channels and identical target observations, alongside mean, persistence and AR(4). All three declared seeds remain visible. See [results](RESULTS.md), [frozen protocol](PLAN.md) and [verification](VERIFICATION.json).

Designation: **independent architectural implementations under a modified normal-only protocol**. Original paper-run equivalence remains unresolved: exact released checkpoint, original-recording identity/label alignment and original code-use grant are not recovered. The provider-v2 nominal file is not silently substituted for the original paper's data. Our CNNs are also not converged: the larger architecture completed three epochs per seed under its CPU admission budget; the smaller reached the 30-epoch cap while improving. A favorable comparison against these artifacts alone would not establish superiority over adequately trained CASPER.

## Two comparisons with different information access

| Scientific question | Common information and needed evidence | Current state |
|---|---|---|
| Does a proposed detector improve on CASPER-style IMU anomaly detection? | Same nine IMU channels, causal filtering, chronological partitions, normal calibration, exact event/support definitions, adequate training, every seed and strong AR/persistence controls. | Predictor execution and alignment verified. Detection thresholds, full comparator training and attack evaluation remain outstanding. |
| Can a twin distinguish authorized changes and clear an alarm after physical return? | Same state measurements, approved-command context, availability flags, commissioning budget and initialization for the candidate and command-aware ARX/observer controls. Physical truth is evaluator-only. | Earlier simulation established failed candidate rules and useful controls. A replacement mechanism has not passed novelty or feasibility admission. |

Do not join the two into one ranking by giving only our method approved commands or true joint states. If an IMU-only detector is evaluated in the command-aware study, label its weaker information access and report a separate matched-context variant. Authorized and unauthorized actions with identical observed motion cannot be distinguished from that motion alone. This is an information limitation, not a demonstrated CASPER implementation defect.

## A specific mechanism problem worth solving

The current target is a causal decision about **physical return despite sensor noise and reference-model error**, while preserving evidence during a persistent deviation. v0.9 shows why simply adding the largest noisy commissioning residual to each current residual can make return impossible. Replacing that maximum with an arbitrary smaller percentile would change the error contract; it would not by itself establish an original method.

A useful mathematical specification is:

`e[t,j] = y[t,j] - r[t,j] = delta[t,j] + b[t,j] + noise[t,j]`,

where `r` is the clean-data command-driven reference, `delta` is deviation from the nominal physical response, and `b` is reference bias. Only `y`, approved commands and the fitted reference are detector inputs. The simulator's nominal counterfactual and true `delta` belong exclusively to evaluation.

As a **standard statistical control**, consider a fixed trailing window of length `m`, justified bounds `|b[t,j]| <= B[j]`, conditional zero-mean sub-Gaussian measurement noise with proxy `sigma[j]^2`, and a valid physical-deviation increment bound `|delta[t,j]-delta[t-1,j]| <= L[j]`. For `d` channels and an overall error allocation `alpha`, set `alpha_t = 6*alpha/(pi^2*t^2)` using a global clock that never restarts after an alarm. A conservative current-deviation upper bound is

`U[t,j] = |mean_window(e[:,j])| + B[j] + sigma[j]*sqrt(2*log(2*d/alpha_t)/m) + L[j]*(m-1)/2`.

The noise term follows a sub-Gaussian tail bound and a union bound over channels and all prospective times; overlap between windows does not require independence for that union bound. The drift term connects the window's average deviation to its current value. If every `U[t,j] <= tolerance[j]`, the stated assumptions support a simultaneous error-controlled return decision. Selecting among windows or restarting the error budget needs additional accounting. Unverified model/noise/drift bounds do not become guarantees because the formula is implemented. A noisy empirical maximum is not automatically a bias bound.

**This construction is not admitted as our novelty.** It combines established concentration, bounded-error propagation and equivalence reasoning. It is a demanding control that any proposed mechanism should improve on, for example by providing a less conservative valid treatment of command-dependent bias and motion without discarding the error contract. Ordinary averages, covariance-aware observers, fixed-return hysteresis and calibrated episode bands remain essential controls. [Howard et al.](https://arxiv.org/abs/1810.08240) establish much stronger general time-uniform inference tools; a generic confidence-sequence claim would not be new.

## What must happen before a contribution claim

1. **Comparator adequacy:** run a separately bounded normal-only convergence study; retain all seeds and budgets. Keep prefix feasibility distinct from a representative full-data reproduction. No attack exposure to choose training length, architecture or score convention.
2. **Mechanism admission:** state the proposed operation, assumptions and exact distinction from the closest available recovery/interval methods. Resolve the closely related Kaisar full-method lead; lack of access cannot establish absence of overlap. Test whether the rule reduces algebraically to an existing control before investing in another attack campaign.
3. **Normal feasibility:** using new reserved simulation conditions, verify that the proposed uncertainty treatment admits ordinary recovery and authorized changes under correlated noise, bias and mismatch. All bounds must have an operational source. Simulator-provided true uncertainty is an explicitly oracle-informed diagnostic, not a deployable estimate.
4. **Frozen comparative evaluation:** declare a meaningful advantage and acceptable detection/recovery trade-off, all methods/ablations, normal-only calibration, common eligible observations, uncertainty analysis and failure reporting before opening fresh outcomes. Same-model seeds are computational repetitions; independent task/plant conditions are the relevant evidence units. Synthetic motion edits remain separate from physically generated scenarios.
5. **Claim admission:** claim superiority only for the measured task, information access and conditions. Originality requires a supported method-level distinction; a renamed gate, better threshold, lower normal MSE or a polished PDF does not establish it. An unfavorable result remains visible and does not trigger retuning on the same final scenarios.

The next executable milestone is adequate common-input normal training. The next scientific design milestone is an identifiable, noise-aware return mechanism with a justified distinction from ordinary uncertainty controls. Neither requires physical equipment. Lengthy training still needs the user's standing resource-approval rule; no long run, new attack campaign or publication is authorized by this report alone.
