# Frozen RAPT transfer diagnostic on exposed Q1 simulations

This is an exploratory, no-fit replay of the complete existing Q1 grid. It does not open a fresh holdout, select an improved model, reproduce the humanoid experiments, or establish novelty. RAPT does not claim the physical-recovery guarantee examined by our diagnostic. A mismatch on this task is not itself a flaw in its original claim.

## Fixed detector and population

Use the unmodified author detector at commit `d745668ffdb0e26877b1de4c9b2126af7bda5b03`, selected normal-development epoch 14 from `raw_Q1_seed17_001`. Load its saved configuration, weights, training normalizer and L13 calibration without fitting or changes. Evaluate both released model-only and hybrid range-gate modes; strict normalized risk > 1 is the alarm rule. Reload calibration through the author's `Calibration.from_dict`, which restores numeric arrays as float64. Do not recompute or optimize thresholds.

The fixed input manifest contains all 36 exposed v0.19 Q1 episodes: tasks L19/S19 × simulation seeds 17/42/2026 × normal, authorized_changes, brief_offset, persistent_offset, hold and slow. These contain 129,600 observations, of which 126,000 remain after excluding each episode's first 100 rows. There are 12 benign episodes (70,800 eligible observations) and 24 intervention intervals. Simulation seeds are not independent robots; there is one fitted network seed.

Detector inputs are only noisy honest measured q1/q2/v1/v2, protected desired q1/q2/v1/v2 and validity. Command at t drives the transition to t+1. Feed the complete sequence causally, resetting recurrent state only at the start of an episode. No resets at labels, no truth or counterfactual input, no parameter updates. The first forward score is undefined and returned as zero upstream; it lies inside the excluded warmup.

## Ordering and outcomes

Verify all frozen source/input/checkpoint bindings. Produce both score/alarm series for every episode, preserve per-channel discrepancies, then hash and seal all 36 artifacts before opening evaluator-only truth. After that seal, join existing intervention labels and counterfactual physical trajectories for evaluation. Save every episode, both modes, failures and computational cost.

Report unadjusted pooled and per-task/per-condition precision, recall, F1 and average precision; point alarms, alarm starts per benign eligible hour, coverage, overlap and fresh event detection, missed events, delays with denominators, and the v0.19 physical-return diagnostic. Its tolerance is 0.1 training-scale units with ten consecutive qualifying observations, measured from the first qualifying observation; clearance horizon is 250 observations (5 seconds). This is a diagnostic using simulated counterfactual truth, not detector input or a safety guarantee.

For every intervention report first-quarter and final-quarter risk median/max, alarm occupancy, physical-outside points and inactive-outside counts. Quarter length is max(1,floor(interval length/4)); no post hoc subset. A late reduction in risk alone does not establish failure: interpret it together with detection and physical deviation. No success criterion, preferred mode or subsequent redesign will be chosen from these outcomes.

Older v0.19 controls are not ranked here. Their base ARX artifacts were fitted in v0.9 and loaded by v0.13; RAPT uses K13 training, M13 checkpoint selection and L13 calibration. Shared evaluation inputs do not erase these different training populations. This experiment therefore assesses author-code transfer behavior, not common-training superiority over a published full system.

## Budget and command

One sequential attempt, CPU only, no fitting: 120 seconds wall, 90 CPU, 1 GiB monitored RSS, 50 MiB total output. The completed normal run took 40.44 seconds, including 37.91 seconds training; its remaining work included three nine-episode score passes (32,400 observations). Four times that non-training duration is about 10.2 seconds, a rough estimate rather than a guarantee. Allow 10–20 seconds expected replay and evaluator work; the hard supervisor remains decisive. Do not silently weaken the monitor or retry a failed scientific run.

From `manufacturing/`:

```
.venv-forecast-v016/bin/python -m unittest discover -s research_cycles/rapt_protocol_v0.21/exploratory -p 'test_*.py' -v
.venv-forecast-v016/bin/python research_cycles/rapt_protocol_v0.21/exploratory/run.py
```

Preparation and synthetic tests precede parent review. Execution requires the parent's explicit go-ahead. No training, filtered matrix, original G1 observation access, manuscript change or publication is included.
