# RAPT author-code compatibility and cost pilot

19 October 2026. Authorized by the parent research task before execution. This is a normal-only resource and implementation check, not a detector benchmark.

Run the unmodified released RAPT forward-dynamics architecture at commit `d745668ffdb0e26877b1de4c9b2126af7bda5b03`: width 256, four residual blocks per encoder/decoder, one GRU, 25% bottleneck, sequence length 50, Gaussian NLL training. Feed four honest measured joint position/velocity observations and four protected planned position/velocity commands. Training normalization uses training observations only; commands retain native units as in the released forward-dynamics loader.

Use only the nine saved synthetic Q1/K13 normal episodes from residual-twin v0.13, with the existing 100-row startup removed. No calibration, development selection, attacks, final outcomes, original robot observations or pretrained humanoid weights enter. Non-overlapping windows are made separately inside each episode. The authoritative author code receives those explicit episodes; its random sequence-split CLI is not invoked.

One epoch, batch 32 (reduced from 256 to fit the local bound), seed 17, one CPU thread, default learning rate/optimizer/noise/clip/weight decay. The one-epoch scheduler is a timing pilot and is not used as an experimental fitted artifact. Save no trained checkpoint. On a separate explicitly synthetic 53-row algebraic fixture, verify batch/stream score alignment, first-step zero convention, and exact calibrated gate formulas. Do not treat these tests as benchmark results.

Bounds: 60 seconds wall, 50 seconds CPU, 1 GiB sampled RSS, 5 MiB outputs. Preserve a terminal failure if any limit is reached. Estimate a 100-epoch upper planning cost from measured epoch time; do not launch that training here. Record source/input hashes, platform, package versions, interpreter, command, Git revision/dirty state, limits and final worker usage. No package installation.

Working directory: `manufacturing/`.

```sh
.venv-forecast-v016/bin/python research_cycles/baseline_admission_v0.20/run_pilot.py
```
