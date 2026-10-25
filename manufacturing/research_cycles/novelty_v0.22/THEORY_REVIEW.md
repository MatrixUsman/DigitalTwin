# Theory review: sustained deviation and physical return

24 October 2026. Manufacturing only. Scoped parallel AI research review under the academic-research-suite deep-research/assumption-challenger guidance. Read current STATUS, CLAIM_INTENT, the v0.19 implementation, and the existing recovery/representation audits. This is source inspection and analytical reasoning, not a new experiment, independent human peer review, or an originality certificate. No raw/test signals, fitted checkpoints or old artifacts were modified.

## Decision

The most concrete candidate raised during this review is **a command-driven predictor with a provably limited observation correction, plus an uncertainty path that cannot erase the residual floor**. Its potentially useful distinction is a sufficient, pointwise sensitivity statement for a precisely defined sustained displacement, obtained without training on fault labels. This is a research hypothesis, not established novelty. Reverse-Lipschitz algebra is elementary; H-minus fault sensitivity and Lipschitz neural anomaly detection are established. It only earns a contribution if its implementable constrained learning rule improves a worthwhile nominal-monitoring tradeoff beyond a simple linear leaky correction with the same gain bound.

Two alternatives were examined: shared-uncertainty counterfactual effect bounds, and anytime-valid recovery decisions with a physical variation bound. Neither is currently a stronger novelty candidate. Their main value is exposing missing assumptions and preventing a new decorative threshold rule.

## Primary-source findings that constrain the claim

**Ghanipoor, Murguia, Ferrari Trecate and van de Wouw, arXiv:2504.19688v1, 28 April 2025.** [Full author manuscript](https://arxiv.org/html/2504.19688v1); [version history](https://arxiv.org/abs/2504.19688). Inspected §§II–III, Theorem 1, Remark 1, example and conclusion. The bank of robust recurrent equilibrium networks uses healthy trajectories with synthesized additive sensor faults. Eq. 6 bounds the *maximum* residual contrast by a truncated-l2 gain; Remark 1 explicitly calls its parameter choice necessary for sensitivity, while fault-tracking training supplies sensitivity empirically. Eq. 7 bounds response to other sensors' faults. The conclusion identifies a sufficient sensitivity parameterization and process/actuator extensions as future work. The author-linked [code](https://github.com/DecodEPFL/faultDiag) was located but not inspected/executed by this reviewer. Root found a 2026 Automatica successor, DOI 10.1016/j.automatica.2026.113096; this review's direct publisher retrieval returned 403. Do not transfer the v1 gap to that final article until its theorem is checked. The arXiv history showed only v1; speculative v2 retrieval failed.

**Kim, Kwon, Chang and Paik, AISTATS 2020, PMLR 108:2507–2517.** [Proceedings](https://proceedings.mlr.press/v108/kim20c.html), [full paper](https://proceedings.mlr.press/v108/kim20c/kim20c.pdf). Inspected abstract and method/theorem context. Lipschitz constraints and reconstruction-error anomaly discrimination already have theoretical and empirical treatment. Their admissibility concerns average anomaly reconstruction error and a Wasserstein objective. This defeats a broad claim that Lipschitz-constrained neural reconstruction or lower anomaly-score arguments are new. It does not by itself establish the exact causal command/history contract proposed below. Older foundational background, outside the principal comparator window.

**Wang et al., “Fault detection based on zonotopic H_/L∞ observer for Lipschitz nonlinear systems,” Automatica 192, 113159, October 2026.** [Publisher preview](https://www.sciencedirect.com/science/article/pii/S0005109826003432). Abstract, introduction, declared contributions and section snippets inspected; full theorem/code not admitted. The method targets minimum fault sensitivity and bounded-peak disturbances, with a flexible robot arm example. This is exceptionally close to any claim of retaining persistent-fault evidence while controlling nuisance response. Exact first-online date versus our 16 October cutoff remains unresolved. It must be considered for novelty even if ineligible for the frozen main roster. No numerical superiority claim can be made from our different task.

**Qin et al., “H−/L∞ Fault Detection Observer Design for Uncertain Lipschitz Nonlinear Systems,” 2022, DOI 10.1155/2022/6596746.** [Publisher full text](https://onlinelibrary.wiley.com/doi/10.1155/2022/6596746). Problem formulation and design statements inspected. It combines finite-frequency fault sensitivity, bounded-disturbance attenuation, uncertain parameters and dynamic thresholds. It confirms the established nature of the gain tradeoff; a different neural parameterization must supply more than a renamed version of it. Older methodological background.

**Altinses and Schwung, arXiv:2603.25103v1, 26 March 2026.** [Full preprint](https://arxiv.org/html/2603.25103v1). §§3.4, 4.3–4.4 inspected. Layer-specific sensitivity, contrastive separation and contracting correction explicitly address the tension between detecting and correcting faults. The displayed product-of-layer-norm and local perturbation inequalities do not establish the proposed end-to-end recurrent plateau guarantee. This remains an important overlap, not proof that our exact contract is original. Page says submitted to Information Fusion; peer review was not established.

**“Causally-Constrained Probabilistic Forecasting for Time-Series Anomaly Detection,” arXiv:2604.17998v1.** [Full preprint](https://arxiv.org/html/2604.17998v1). Main architecture and §§IV-F, IV-I–K inspected. A causal parent-masked predictor already has a detached shadow residual-correction path, probabilistic scoring and gated blending. Stop-gradient isolates training gradients; it does not certify an inference-time gain cap. Its causality graph is also different from cryptographically/operationally protected command provenance. The broad two-path architecture is therefore unavailable as novelty; the proposed distinction must be the enforced contract and demonstrated tradeoff. Published headline results are not comparable to ours.

**Sandberg and Teixeira, arXiv:1604.05476v1, 19 April 2016; SoSCYPS 2016, DOI 10.1109/SOSCYPS.2016.7580001.** [Full manuscript](https://arxiv.org/pdf/1604.05476), [institution manuscript metadata](https://pure.tudelft.nl/ws/files/8960001/From_Control_System_Security_Indices_to_Attack_Identifiability.pdf). Definitions of persistent attack, disturbance masking and identifiability inspected. If plausible disturbances can produce the same observations as an attack, no passive monitor can distinguish them under that model. This limits cyber attribution and parameter-mismatch rejection. Existing fault-diagnosis disturbance decoupling is not an original mechanism here. Older background.

**Howard et al., “Time-uniform, nonparametric, nonasymptotic confidence sequences.”** Annals of Statistics 49(2), 1055–1080 (2021), DOI 10.1214/20-AOS1991; inspected [arXiv v9](https://arxiv.org/pdf/1810.08240) (6 August 2022), definition and main construction context. Time-uniform uncertainty and validity at stopping times are established. A confidence sequence for a running conditional mean is not automatically a bound on today's physical displacement. **Liu (2003), DOI 10.37920/sasj.2003.37.2.2**, [publisher abstract](https://www.journals.ac.za/sasj/article/view/9056), already tests sequential equivalence against an outside-tolerance null. Neither sequential testing nor “prove return rather than fail to detect departure” alone is new.

**Ingimundarson et al., “Robust fault detection using zonotope-based set-membership consistency test,” DOI 10.1002/acs.1038.** Author-hosted manuscript search result exposed parameter-consistency equations and invariant/bounded/unbounded parameter-variation cases; direct [institution PDF](https://grupo.us.es/gepoc/wp-content/uploads/publications/Ari_Adapt_08.pdf) retrieval failed. Inspection is therefore partial, not full-manuscript verification. The work already tests whether one admissible parameter history can explain a sequence. A joint-parameter consistency test cannot be called new merely because pointwise envelopes are weaker.

**Desai et al., Soter, UCB/EECS-2018-127, 21 August 2018.** [Institution technical report](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2018/Archive/EECS-2018-127.pdf), introduction and runtime-assurance design inspected. Guarded return from a verified controller to an advanced controller and recoverable-state logic predate this project. Recovery-aware monitoring should not be confused with a new control-safety guarantee.

## Candidate A: observation correction with a residual floor

This candidate was proposed by the root during the review. The following derivation is explanatory mathematics, not an original theorem and not a verification of any implementation.

Let a fixed protected-command model produce `b_t=b(u_≤t)`. Let `A_t` be a causal correction driven by past observed residuals and trusted commands, with fixed parameters and the same initialization in paired nominal/deviated trajectories. Define

\[
\mu_t=b_t+A_t(y_{<t}-b_{<t},u_{\le t}),\qquad r_t=y_t-\mu_t.
\]

Assume the *whole causal operator*, including its hidden state, satisfies an incremental peak-gain bound

\[
\|A_t(e+\delta,u)-A_t(e,u)\|_\infty
\le\kappa\max_{s<t}\|\delta_s\|_\infty,\quad 0\le\kappa<1.
\]

For two input streams with the same protected commands, reverse triangle inequality gives

\[
\|r_t^a-r_t^0\|_\infty\ge
\|\delta_t\|_\infty-\kappa\max_{s<t}\|\delta_s\|_\infty.
\]

For a step displacement that is zero before onset and a constant vector `δ` afterward, the lower bound is `(1−κ)||δ||∞` at each post-onset timestamp. More generally it holds whenever the current displacement magnitude equals the historical peak. It is **not** a pointwise lower bound of `(1−κ)||δ_t||` for arbitrary time-varying signals.

If an earlier onset transient is larger than the eventual plateau, the peak-gain statement can become vacuous. A separately proved fading-memory inequality is needed to obtain a nonvacuous late-time result. For example, a state recurrence with state contraction `ρ<1`, input gain `Lx` and output gain `Lo` gives a contribution from a past state discrepancy bounded by `Lo ρ^n ||Δh_0||`, while a constant plateau contributes at most `Lo Lx D/(1−ρ)`. The sufficient design requirement is on that total gain, not merely `ρ<1`. A stable observer can still have unit DC gain and absorb a constant displacement completely.

Turning contrast into an operational alarm additionally needs a nominal residual bound `||r_t^0||∞≤ε_t` and a fixed threshold `h_t`. A sufficient conditional alarm inequality is

\[
(1-\kappa)D>\epsilon_t+h_t.
\]

An empirical normal quantile is not a uniform physical guarantee; its scope must remain explicit. A learned scale/variance head must use trusted context only or have a certified finite upper cap. Otherwise the model can preserve a raw residual while inflating its denominator enough to suppress the score. With `σ_t,j≤σbar`, max standardized-squared-residual is at least `||r_t||∞²/σbar²`. This covers that score, not arbitrary NLL/postprocessing gates.

### Concrete provisional recurrent parameterization

The root subsequently specified a tanh adapter

\[
h_t=\tanh(W_hh_{t-1}+W_zz_{t-1}+W_cc_t+b),\quad
a_t=W_oh_t,
\]

where `z=y−b(u)`, command context `c` and the base prediction are identical in paired streams, and `h_0` is identical. If the actual trained weights enforce induced matrix infinity norms `||W_h||∞≤ρ<1`, `||W_z||∞≤β`, `||W_o||∞≤γ`, then

\[
\|\Delta a_t\|_\infty\le
\gamma\beta\sum_{s=0}^{t-1}\rho^{t-1-s}\|\delta_s\|_\infty,
\quad \kappa=\gamma\beta/(1-\rho)<1.
\]

This yields the preceding peak bound and a useful explicit decaying tail after a larger transient. It relies on tanh's componentwise 1-Lipschitz property and exact norm constraints. It is standard contraction algebra. A training penalty alone is insufficient. Any normalization, skip connection, input-dependent gating, missingness encoding or extra observation path must be included in the actual bound. If `z` is scaled, the physical-to-normalized conversion belongs in the proof. Runtime resets cannot depend on attack labels or silently erase ongoing deviation.

The proposed normal-development selection target

\[
R_{\rm dev}=(E_{\rm dev}+\tau_{\rm dev}s_{\max})/(1-\kappa)
\]

is more relevant than MSE alone because it penalizes the sacrificed sensitivity margin. Compare with the direct-reference `κ=0` case using the same normal selection population and definition. Here `E_dev` and `τ_dev` are empirical development quantities, not deterministic deployment guarantees; a normal-data maximum does not certify every future nominal trajectory. Reserve final calibration, report all finite candidates and use episode-group validation if admitted. This objective can still be optimistic after model selection; a successful value is an admission diagnostic, not a new detection result.

There is an additional ordinary control: tanh makes the adapter amplitude bounded even without the incremental-gain constraint. A clipped/saturated linear leaky correction can likewise preserve large-offset residuals. Include an equal-cap amplitude-bounded adapter, or otherwise demonstrate that the advantage comes from the certified incremental gain rather than saturation alone. Scale capping is also a distinct component; test its contribution separately.

### What might be distinct

The defensible candidate claim is an **implemented normal-only learned correction with an enforced causal gain contract and explicit residual-to-alarm conditions for sustained deviations**, compared with both unprotected prediction and ordinary protected/leaky controls. The contribution cannot be “new Lipschitz theory,” “first protected twin,” or “first fault-sensitive recurrent network.” The final Ghanipoor version and robust H-minus observer literature are mandatory close comparisons. Sensor-fault isolation and command-path physical deviation differ, but changing the threat label is not itself a new method.

### Strongest falsifiers and controls

1. Direct protected reference (`κ=0`) has the strongest nominal sensitivity bound. The correction must reduce genuine normal-model error/alarm cost enough to justify giving up sensitivity.
2. A linear leaky correction `a_t=ρa_(t−1)+(1−ρ)κ e_(t−1)` already has total incremental peak gain `κ` and the same step-floor guarantee. If it matches the learned candidate, the neural contribution fails.
3. Ordinary KF/AR controls, with equal inputs/training/calibration, must remain. A purposely rigid or badly fitted filter is not a valid comparator.
4. Spectral penalties, sample Jacobians, gradient clipping or finite perturbation checks do not certify the whole recurrent input/output gain. If certification is vacuous or not enforced after fitting, reject the guarantee claim.
5. If nominal error needs gain near one, the proposed constraint may worsen benign behavior. Do not change κ after viewing attacks to manufacture success.
6. Distinguish observation differences caused by true motion from corrupted telemetry. Honest observations and protected commands remain assumptions; they are not established by this architecture.
7. Clearing/recovery is a separate inference. This sensitivity bound does not certify physical return, and the old failed v0.19 criterion remains failed.

## Candidate B: coupled counterfactual uncertainty

One alternative is to retain a joint set of actual and authorized-counterfactual trajectories with **the same** uncertain parameters, instead of separately bounding each trajectory and adding widths. For a structural model

\[
x^a_{t+1}=f_\theta(x^a_t,u_t,a_t,w_t),\quad
x^0_{t+1}=f_\theta(x^0_t,u_t,0,w_t),
\]

the target is the range of `x^a−x^0` over joint feasible paths consistent with measurements and a frozen commissioning set. Sharing θ and exogenous noise may avoid duplicated uncertainty. In a linear additive-noise example, common additive disturbance cancels from the difference dynamics; that is algebra, not a novel theorem.

The practical barrier is severe: the sharing model must be scientifically justified. Arbitrary unknown attacks can explain observations without narrowing θ, and legitimate disturbance/attack ambiguity remains. A finite model ensemble is not a guaranteed outer bound. Existing constrained-zonotope, parameter-consistency and relational verification techniques are mandatory controls. **Kill criterion:** if the scheme is simply a standard augmented-state set observer, or its advantage depends on evaluator-only shared noise/true plant parameters, do not advance it as a contribution. This is a secondary design lead, currently less ready than Candidate A.

## Candidate C: recovery decisions with temporal evidence

Suppose `z_t=d_t+η_t` and a sequential method bounds a recent average displacement. It still cannot certify current `d_t` without a temporal model. A declared variation bound `||d_t−d_s||≤L|t−s|` yields

\[
\|d_t\|\le\|\bar d_{t-w+1:t}\|+L(w-1)\Delta t/2.
\]

Adding a valid uncertainty bound for the window mean gives a current-state bound, but its window/physical-rate tradeoff is standard. Repeated overlapping windows require suitable simultaneous validity, not an ordinary fixed-sample interval reused each tick. With velocity/acceleration bounds, the temporal remainder can be refined using established reachability.

**Potential useful task:** quantify when a physical return statement is identifiable and available, rather than treating every low prediction error as recovery. **Kill criterion:** if the final rule is confidence-sequence thresholding plus a standard Lipschitz remainder, there is no established algorithmic novelty. Do not infer instantaneous return from sign-cancelling means, permanent uncertainty from zero alarms, or cyber attribution from bounded displacement. This route may improve rigor but currently does not meet the user's original-method objective.

## Search receipt and limitations

Queries were issued on 24 October 2026 through the web tool; searched combinations included: robot attack recovery/sequential equivalence; time-varying confidence sequences; attack identifiability/disturbance masking; paired counterfactual reachability/shared parameter uncertainty; parameter-consistency fault detection; action-conditioned contrastive anomaly detection; Lipschitz fault sensitivity/H-minus/H-infinity/H-minus/L-infinity; and the exact Ghanipoor title/DOI. Public primary manuscripts/proceedings/publisher pages supplied conclusions. Third-party aggregators and broad generated-looking web summaries were leads only. No external programmatic reference-verification or model APIs were called.

Access failures: the institution Ingimundarson PDF, direct Automatica 113096 article and its DOI resolver, and speculative arXiv v2 for Ghanipoor. The last is not evidence of a missing paper; the accessible arXiv history showed v1 only. The 2026 final Automatica theorem remains an explicit unverified dependency. No exhaustive-search or novelty-proof claim follows.

Next bounded step recommended to root: reconcile Candidate A against the final REN and H-minus manuscripts, write the exact enforced architecture and plain linear control, prove the implemented norm bound, and first test **normal-only feasibility** under a fixed resource budget. A candidate is admitted only if its normal fit remains useful and its distinction survives these comparisons. Any later attack confirmation requires fresh prospectively frozen conditions; the exposed v0.19/v0.21 outcomes can only serve exploratory diagnosis.
