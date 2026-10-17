# Recovery study v0.8: measured results

Frozen primary criterion: **failed**.

| Method | Benign alarms | F1 | Overlap / fresh | Premature clear | Cleared / returned detected |
|---|---:|---:|---:|---:|---:|
| persistence | 878/89100 | 0.0573 | 127/127 | 127 | 127/127 |
| arx_one_step | 792/89100 | 0.8034 | 108/108 | 108 | 108/108 |
| following_point | 794/89100 | 0.8076 | 108/108 | 108 | 108/108 |
| following_hysteresis | 993/89100 | 0.7848 | 108/108 | 108 | 108/108 |
| nominal_hysteresis | 789/89100 | 0.7128 | 108/108 | 45 | 108/108 |
| nominal_fixed_return | 621/89100 | 0.6569 | 108/108 | 0 | 108/108 |
| learned_point | 819/89100 | 0.6999 | 108/108 | 18 | 108/108 |
| learned_hysteresis | 792/89100 | 0.6827 | 108/108 | 0 | 108/108 |
| learned_fixed_return | 827/89100 | 0.6899 | 108/108 | 0 | 108/108 |
| learned_uncertainty_return | 309/89100 | 0.4463 | 108/104 | 0 | 36/108 |
| functional_cp_constant_band | 0/89100 | 0.7443 | 108/108 | 75 | 108/108 |
| matched_no_allowance | 140/89100 | 0.7090 | 108/108 | 0 | 108/108 |
| matched_no_dwell | 20/89100 | 0.4526 | 108/108 | 0 | 36/108 |

## Declared criterion
{
  "benign_reduction_fraction": 0.5024154589371981,
  "passed": false,
  "tests": {
    "benign_reduction": true,
    "commissioning_control_cost": true,
    "misses": true,
    "premature": true,
    "timely_return": false
  }
}

## Commissioning and uncertainty

- Q1: reference spectral radius 0.955950; empirical allowance 0.070880; return tolerance 0.1.
- Q2: reference spectral radius 0.966903; empirical allowance 0.191489; return tolerance 0.1.
- Q3: reference spectral radius 0.971475; empirical allowance 0.209284; return tolerance 0.1.

Paired-plant versus nominal-model return differs in 21/135 intervention episodes. This is a comparison of definitions, not a retroactive change to v0.7.
The reference-error envelope covers the entire eligible counterfactual trajectory in 189/216 episodes. This is measured test coverage, not a distribution-free guarantee.

## Scope and computation
The completed run has 216 synthetic episodes, 13 methods and 2808 outcomes. 9610 verification checks passed. All three noise seeds are retained; they are dependent replicates of the same physical conditions.
Worker elapsed time: 229.077 s. Full costs and supervisor memory/CPU/output measurements are in the saved run. The prior launch failed before the worker began because /bin/ps was blocked; the unchanged experiment then ran under scoped monitoring permission.
The functional-CP row uses a separate episode-level threshold. The two matched ablations reuse the candidate entry threshold; neither is presented as an equal-calibration-budget competitor. Missing command context remains unknown for the rest of an episode. Missed events and absent fresh onsets stay in all denominators.
This study does not reproduce a complete recent paper experiment. The references and comparator adaptations are described in PRIOR_ART.md. It establishes neither physical robot validation nor algorithmic novelty by itself. No outcomes may be reused as fresh confirmation for a redesigned mechanism.
