# Matched no-dwell and reporting replay v0.18

## Material Passport
19 October 2026; manufacturing; operator Codex at the user's explicit execution request. Exposed synthetic v0.14 traces only. No training, simulation generation, original dataset access, threshold selection or fresh confirmation.

## Frozen question and comparison
Does the already reported no-dwell occupancy reduction depend on the RBF correction? Add only `base_dual_nodwell`: the saved base score, threshold and residual, windows (5,41), tolerance 0.1, one qualifying non-exceedance to clear, with entry priority. RBF no-dwell is reconstructed using the identical rule. Both use original train-fitted scales and original rank-5445/5500 normal-calibration thresholds. The original 17 streams must replay bit-for-bit; all old outcomes must agree exactly. Original 10% primary failure remains unchanged.

All 189 exposed traces (3 tasks, 3 plants, 3 paired noise seeds, 7 conditions) are replayed. Warmup 100; 1100 eligible observations per episode; 50 Hz. No label is used by alarm calculation. Scoring starts at 100; dual-window readiness starts at 140; dwell 1 can clear then; dwell 10 can first clear at 149. Truth joins only in the evaluator.

## Reporting and diagnostic rules, specified before replay
For all 18 methods save episode-level original metrics plus: eligible alarm-run lengths, start frequency, detection/fresh/clearance delay distributions (median, 90th/95th percentile, maximum and observed/missing counts), physical-outside-tolerance inactive points before/after first detection, episodes with such inactivity, pre-return gaps, and literal inactive-by-return+5s counts. Delays remain conditional on success; misses and absent/censored returns remain explicit. Summarize pooled, plant, task, condition and plant-by-condition; no p-values or independent-robot inference. Do not relabel already-inactive-at-return as successful retention.

For base/RBF point and dual/no-dwell only, partition benign alarm points into current score exceedances, retained points with clearance evidence true, and retained points with evidence false. Report deterministic reference-error-only exceedances versus noisy observed exceedances and shared occurrences, plus calibration and evaluation occupancy separately. These diagnostics characterize interactions, not causal intervention estimates or automatic model-selection rules. Native physical tolerance is 0.1 times each training scale.

## Bounds and artifacts
One supervised replay attempt, <=300 s wall, <=180 s CPU, <=1 GiB sampled RSS, <=100 MiB output; all attempts preserved. Existing shared supervisor; no system packages. Synthetic tests cover entry priority, strict ties, dwell, invalid observations, window readiness, start counting, fragmentation, outside-tolerance counting, misses and conditional clearance. Freeze input/source hashes before execution. Outputs: all episode outcomes, descriptive stratified summary, matched alarms, diagnostics, provenance, resource receipt and separate verification receipt. Save each source/model/input identity; verify originals before and after. Any software correction and rerun needs a separately recorded repair, never overwrite an attempt.
