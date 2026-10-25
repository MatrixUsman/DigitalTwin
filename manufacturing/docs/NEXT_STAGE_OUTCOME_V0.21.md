# Next-stage outcome: paired evidence, representation and RAPT

19 October 2026. Manufacturing. Journal submission remains on hold at the user's direction. The v1.7 manuscript, its original failed requirements and its completed reviewer package remain unchanged. The original-contribution objective remains active.

## Completed work

| Task | Actual outcome |
|---|---|
| Complete episode-paired analyses | Completed for all 216 exposed v0.19 episodes against three controls, including missing-delay denominators and fine strata. |
| Make the analysis easily replayable | New 254 KB standard-library addendum passes clean extraction and byte-identical table replay. The existing 308 MiB reviewer archive was already verified and is preserved. |
| Identify a change beyond alarm threshold/dwell adjustments | Examined causal position/velocity estimation before the fixed reference/readout. Prior art establishes its mathematics; an original algorithm was not claimed. |
| Test that candidate prospectively | Completed 54 fresh normal-only synthetic episodes, five estimator families and three sensing regimes. Coupling failed its frozen gate against ordinary KF; no attack campaign was launched for it. |
| Execute a recent complete detector component | RAPT author code completed 100 normal-training epochs for one plant/seed, selected epoch14 on normal development, then calibrated on separate normal records. |
| Test an actual baseline limitation | Completed a frozen no-fit replay on all 36 previously exposed Q1 episodes, with both released gating modes retained. Persistent-deviation insensitivity is observed in this transferred setting; no new-confirmation or full-paper reproduction claim is made. |

## What the paired analyses add

Relative to contextual hysteresis, the existing recovery component reduces outside-inactive time in 98 of 144 intervention episodes, ties in 46 and worsens in none. Joint success improves in 50 and worsens in none. Costs remain visible: more benign occupancy in 16 of 72 episodes and later clearance in 139 of 144 events. Against base dual, all 72 benign episodes improve, but 82 of 144 intervention episodes lose joint support. The original overall criterion therefore remains failed.

[Paired report](../research_cycles/paired_analysis_v0.21/REPORT.md) · [Portable analysis ZIP](../research_cycles/paired_analysis_v0.21/manufacturing-paired-analysis-v0.21.zip)

## Why the proposed filtering extension stops here

K13 normal observations fitted measurement weights; M13 normal prospective targets selected the finite settings; L13 calibrated widths only after selections were sealed. The experiment used fresh normal trajectories, shifted plant parameters and independent, temporally correlated and encoder-derived sensing. It did not use attack outcomes for selection.

The coupled estimator's pooled standardized state RMSE is 0.057659, compared with 0.049746 for the ordinary constant-acceleration KF. KF also wins separately in every sensing regime. A small benefit over uncoupled fitting under independent/AR(1) noise is insufficient to justify the proposed coupling against this stronger ordinary control. The combined encoder shift changes correlation, noise amplitude, quantization and velocity timing; no single-cause explanation is inferred.

The mean filter's zero alarms coincide with permanent uncertainty under the fixed readout. That is a concrete reason to evaluate state error and uncertainty alongside alarm counts. The result does not establish attack-detection or recovery performance. The frozen normal gate fails, so this candidate is not advanced to fresh attacks or a 36-fit neural preprocessing matrix.

[Prospective plan](../research_cycles/observer_feasibility_v0.21/PLAN.md) · [Results](../research_cycles/observer_feasibility_v0.21/RESULTS.md) · [Independent review](../research_cycles/observer_feasibility_v0.21/INDEPENDENT_REVIEW.md)

## The newly measured RAPT behavior

The selected author-code model completed its full 100-epoch schedule; epoch 14 had the best normal-development loss. The retained weights and all thresholds were fixed before the diagnostic replay. Both released model-only and hybrid modes produce the same outcomes here: 9/24 fresh detections, 15 misses, and 5,175/70,800 benign alarm points (7.31%). These counts concern the transferred synthetic task and one fitted seed, not the original humanoid benchmark.

In all six persistent-offset cases, every final-quarter risk is below the alarm threshold while all 747 final-quarter physical-outside observations are inactive. In the three L19 cases, first-quarter median risk is above threshold and final-quarter risk is below it; the three S19 cases were missed throughout. This is consistent with predictive surprise declining even though motion remains displaced from authorized motion. Architecture alone does not prove the cause, and this replay does not isolate recurrence, task shift, calibration or predictive variance as its sole explanation. Network parameters do not adapt online; recurrent inference state does.

The detector does not claim the physical-recovery guarantee used in our diagnostic. Older ARX controls have different training histories, so this replay does not establish a fair common-training superiority ranking. Its value is a concrete, source-linked behavior on which to base a narrowly specified comparison.

[Normal training](../research_cycles/rapt_protocol_v0.21/RESULTS.md) · [Exploratory protocol](../research_cycles/rapt_protocol_v0.21/exploratory/PROTOCOL.md) · [Exploratory results](../research_cycles/rapt_protocol_v0.21/exploratory/RESULTS.md)

## Decision for subsequent work

Keep the existing paper as the documented outcome and preserve both failed gates. Do not promote the rejected coupled estimator or turn this exploratory RAPT result into a claim against its original paper.

The next specific question is whether a protected-command-relative representation retains evidence of sustained physical deviation beyond observation-conditioned prediction **under matched normal training, calibration and information access**. That comparison must include the ordinary KF and direct protected-reference readouts, and distinguish the contribution of the reference from that of a recurrent network. Close prior art already covers protected predictions, so a broad claim that they are new is unavailable. A convincing baseline-specific distinction and worthwhile tradeoff still need to be established before fresh attack confirmation. No additional candidate, success threshold or fresh campaign was silently selected from the outcomes reported here.

All new simulation and author-code runs were local and bounded. No physical setup, paid compute, raw real-data test access, external contact, upload, manuscript publication or Git push occurred. The small addendum is available locally; public release still requires authorization.
