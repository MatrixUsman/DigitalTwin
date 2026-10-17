# Recovery identifiability and the limits of nominal-reference evaluation

These derivations are part of our analysis, not a claim that triangle inequalities or interval observers are new. They distinguish the proposed recovery target from anomaly-score thresholding. Empirical results remain separate.

Let x_t be the perturbed plant state, x_t^0 the same plant's state under its approved command history without corruption, r_t a nominal or learned reference, and y_t=x_t+n_t a truthful noisy measurement. Use a fixed positive diagonal scaling S learned only during clean commissioning and the norm ||v||_S=max_j |v_j|/S_j. Define attack-induced motion discrepancy d_t=||x_t-x_t^0||_S and reference discrepancy c_t=||y_t-r_t||_S.

## 1. Nominal-reference proximity does not identify physical recovery

Even with noise absent, c_t=0 does not imply d_t=0: choose x_t=r_t while x_t^0 differs from r_t because of model mismatch. Conversely, d_t=0 does not imply c_t=0: a recovered mismatched plant can equal its own counterfactual while both differ from the nominal reference. These are algebraic counterexamples, not statements about the observed frequency of either case. A separate paired simulation is needed to measure that frequency.

## 2. Conditional discrepancy bounds

If ||x_t^0-r_t||_S<=b_t and ||n_t||_S<=eta_t, then

    max(0,c_t-b_t-eta_t) <= d_t <= c_t+b_t+eta_t.

Proof: x_t-x_t^0=(y_t-r_t)-n_t-(x_t^0-r_t). Apply the triangle inequality for the upper bound and its reverse form for the lower bound. Both bounds can be attained in one dimension by aligned errors, so they cannot generally be tightened using only these scalar bounds.

Thus rejecting the normal-reference hypothesis using c_t-b_t-eta_t>delta and certifying return using c_t+b_t+eta_t<=delta are different decisions. The region between them is unresolved. Reusing an out-of-distribution threshold as a recovery threshold does not supply this implication.

## 3. Uncertainty can make any certified clearance impossible

Suppose the counterfactual state is only known to belong to a coordinate box centered at r_t with half-width vector b_t and measurement noise to a box of half-width eta_t. Certifying ||x_t-x_t^0||_S<=delta for every admissible pair is equivalent to

    max_j (|y_t,j-r_t,j| + b_t,j + eta_t,j)/S_j <= delta.

For each coordinate, the extreme counterfactual and sensor errors align against the observed deviation, proving necessity as well as sufficiency. If b_t,j+eta_t,j>delta*S_j for any coordinate, no measurement can certify return at that time. Widening uncertainty to reduce nuisance detection can therefore eliminate the possibility of clearance. This is a design trade-off, not evidence of a successful algorithm.

A ten-sample dwell preserves a valid per-sample bound over those ten samples but cannot turn an invalid uncertainty model into a valid one. It also does not prove future safety after the window. A finite-sample probability statement additionally requires justified joint coverage over the chosen stopping time/window.

## 4. Statistical limits of the proposed experiment

The implemented allowance is an empirical maximum of normal reference errors over 19 fixed calibration episodes. It is not a certified parameter/noise enclosure. For 19 exchangeable independent episode scores, the rank ceil(20*.95)=19 is the standard split-conformal 95% rank. Our fixed scenario design and new task families do not establish that assumption. Test error-envelope coverage must be measured; neither the elementary bound nor the FAIL-Detect framing licenses a distribution-free guarantee here.

The clean ARX reference is an explicit model adaptation before monitoring. It cannot absorb post-initialization attack measurements because its free-running state uses only approved command history after four commissioning observations. This immunity is by construction, but it trades away synchronization with unmodeled benign disturbances. Ordinary learned-reference hysteresis is required to separate the value of fitting from the value of the proposed clearance rule.

## Potential contribution and remaining originality test

The evidence package can establish the consequence of separating attack termination, reference proximity and paired-plant recovery; compare commissioning against fixed nominal models; and quantify the cost of uncertainty-aware clearance. It cannot establish original algorithms merely by introducing these names. Close interval/recovery work and RESCUE remain required discussion. Journal submission must match the demonstrated contribution rather than the initial aspiration.
