# Command-anchored recovery: comparator decision and bounded physical pilot

## Material Passport

Manufacturing / Haiqa Mushtaq; Codex under the user's explicit implementation and pilot instruction, 17 October 2026. Academic-research-suite source-check and bounded-experiment guidance applied inline. New exploratory cycle informed by exposed v0.4 results; no external preregistration or confirmatory test. Preserve all earlier model/data/experiment bytes.

## Scope and threat

Test immediate detection, sustained alarm evidence and clearing after return to an approved trajectory in a simulated horizontal two-joint arm. The attacker changes the desired joint command **after** a protected planner. The independent monitor receives truthful noisy joint positions/velocities and a protected copy of approved position/velocity commands. The monitor does not receive executed corrupted commands, intervention labels, true plant state or mass values. These trust assumptions are explicit simulation inputs, not established CASPER capabilities.

Authorized program changes modify both approved and executed commands. Unauthorized changes modify only executed commands. They can produce identical physical observations with different protected context. Without that context, intent is not identifiable. All context-aware controls receive exactly the same approved command and validity flag; ARX is included to test whether ordinary context-aware prediction suffices. No mitigating control is applied by any detector.

This pilot uses four joint-state channels, rather than CASPER's nine IMU channels. Existing CASPER-family CNN weights are not meaningfully transferable across that interface; they remain in the separate recorded-data track. AR and ARX are fitted afresh on synthetic normal data. The simulation is an independently coded idealized planar mechanism, not a calibrated UR3e twin or new robot experiment.

## Physical equations and numerical validation

State `x=(q1,q2,v1,v2)`, point masses at link ends, horizontal plane (gravity has no joint torque), rigid links, viscous friction, fully actuated joints. The source-backed manipulator form is `M(q) vdot + c(q,v) + b*v = tau`. Set `a=m2*l1*l2`:

```
M11=(m1+m2)*l1²+m2*l2²+2*a*cos(q2)
M12=M21=m2*l2²+a*cos(q2); M22=m2*l2²
c1=-a*sin(q2)*(2*v1*v2+v2²); c2=a*sin(q2)*v1²
tau=clip(kp*(qcmd-q)+kd*(vcmd-v), -20,20) Nm
```

The [MIT multibody notes](https://underactuated.mit.edu/multibody.html) provide the underlying point-mass inertia/Coriolis model. Our horizontal-plane specialization, damping, servo gains, sensing and scenarios are fully specified here and in config. Independently test mass symmetry/positivity, inverse-dynamics consistency, kinetic-energy balance, free-motion energy conservation, equilibrium, torque saturation and integration convergence. RK4 uses eight internal steps per 0.02s observation interval; command values are held over an interval and the servo is evaluated at each RK stage. End-effector coordinates are saved for geometry checks. No contact, gearbox elasticity, temperature, gravity loading, real hardware or certified bounds are modeled.

The two plants have masses ±10% and different damping around the observer's fixed nominal parameters. This avoids identical plant/observer parameters but does not establish broad model robustness. Noise is independent Gaussian measurement noise of declared magnitude; no deterministic noise bound is claimed. Each episode starts at known commissioning position, zero velocity; no intervention-boundary reset.

## Explicit recovery mechanism

Maintain a corrected following observer `x_f`, an uncorrected approved-command reference `x_r`, alarm bit `A` and consecutive-agreement counter `k`. Both predict prospectively using nominal dynamics and the preceding approved command. After scoring, update only the following state by fixed gain `L` times its innovation. Reference parameters/state never learn an observed deviation. Missing context holds the last approved command and marks context-aware decisions uncertain.

For observed `y_t`, training-normal channel scales `sigma`, define

`e_f=mean(((y_t-x_f^-)/sigma)^2)`, `e_r=mean(((y_t-x_r)/sigma)^2)`.

Training-normal means `m_f,m_r` give `z_f=e_f/m_f`, `z_r=e_r/m_r`, and `s=max(z_f,z_r)`. Calibration fixes the 99th percentile threshold `h` for `s`. Candidate behavior:

- With valid context, enter alarm immediately if `z_f>h` or `z_r>h`.
- While alarmed, clear only after ten consecutive valid observations with both `z_f<=0.5*h` and `z_r<=0.5*h`.
- On disagreement, reset the agreement count. During context loss, retain the latch, reset the agreement count and emit uncertainty; do not silently declare recovery.
- Correct the following state after scoring irrespective of labels. The command reference stays separate. No model-parameter adaptation is attempted.

**Algebraic admission decision:** this rule is exactly ordinary two-threshold, dwell-time hysteresis on `max(z_f,z_r)` with a validity guard. Separate implementations must agree bit-for-bit in tests and replay. A two-state description does not make it novel. Its value in this pilot is to test the needed information and recovery trade-off; it is not admitted as an original algorithm. If a claimed benefit is identical to ordinary hysteresis, report that equivalence rather than crediting a new twin mechanism. Close prior art is documented in [PRIOR_ART.md](PRIOR_ART.md).

## Roster, splits and thresholds

Eight score controls: persistence, multivariate AR(4), ARX(4) with the previous approved command, following-observer error, its rolling mean45 and CUSUM, command-reference error, and fused maximum. Three stateful decisions: following-only hysteresis (reference ablation), fused ordinary hysteresis, and separately implemented candidate. Context-free methods use the same observations, while context-aware methods also use the common permitted context. No method gets true event labels during scoring.

Training and normal calibration each contain two plants × seeds 17/42/2026 × three benign conditions (normal, authorized offset, authorized slowdown): 18 independently generated noise streams per role. These are synthetic repetitions of two specified plants, not independent physical replications. No parameter search. Means/scales and ridge AR/ARX coefficients fit only training. Normal calibration sets thresholds only, with ascending rank `ceil(.99*N)`, strict exceedance and no label-based adjustment. Each episode has 1,000 observations; the first 100 are shared warmup, giving **16,200 calibration targets**, rank **16,038**. Episode boundaries reset all methods equally; event boundaries never reset them.

Evaluation has two plants × three seeds × eight conditions = **48 episodes**, 43,200 eligible observations per method. Conditions: unchanged operation; authorized offset/slowdown; unauthorized brief offset (5 observations), persistent offset, held command, slowdown, and offset with missing approved-context access. Longer interventions are steps `[300,500)`; context gap is `[300,360)`. All conditions/parameters are fixed before evaluation. Base noise-seed offsets are 10000/20000/30000 for train/calibration/evaluation; each paired condition within a role/plant/seed uses the same noise stream. Conditions are dependent paired comparisons. All observed outcomes remain exploratory; new task frequencies, geometry and stronger mismatch remain **ungenerated future evidence**, requiring a separate freeze before use.

## Output, checks and stopping

Save states, measurements, approved/executed commands, validity, physical intervention masks, predictions, scores, decisions and uncertainty locally as explicitly synthetic. Fit/threshold artifacts are fixed before evaluation. Seal all evaluation output arrays before a separate label-joining pass. Unknown decisions cannot earn true negatives or detections: report their coverage and count unknown attack targets as misses in full-support recall. For known-normal targets report alarm burden with both full and known-decision denominators. Distinguish attack-command duration from physical return dynamics; post-command alarms can reflect genuine residual motion. Report actual state-return time (diagnostic ground truth only), first clear, false clear while command corruption continues, event misses, delays, point precision/recall/F1 and uncertain coverage.

Pilot limits: 600s wall,300s CPU,1GiB sampled RSS,50MiB output. Use existing isolated Python/NumPy environment and supervisor. No new packages, raw data, paid compute, device connections, publishing or external communication. Run synthetic physics/state-machine tests before freezing sources; preserve failures. Verify fitted/calibration identities, recompute metrics and numerical convergence, check exact candidate/hysteresis equivalence and preserve all earlier artifacts. A bounded pilot validates an implementation and tests a hypothesis under its explicit model; it is not final evidence of physical cybersecurity or publishable novelty.

## Pre-freeze numerical correction

Synthetic test attempt `tests_001` failed the declared one-step integration tolerance: four RK4 substeps differed from the 32-substep reference by 1.8988061374612307e-5, exceeding 1e-5. Before generating any pilot observations, increase the fixed integrator to eight substeps; retain the original tolerance and the failed test receipt. This is a numerical implementation correction, not outcome-based method selection. A restored valid-context flag does not create a fresh alarm onset; missed events cannot receive a recovery time.
