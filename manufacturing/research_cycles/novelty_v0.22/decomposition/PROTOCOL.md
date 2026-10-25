# Proposed no-fit decomposition of exposed RAPT scores

24 October 2026. Root authorized one monitored attempt after six synthetic tests and the freeze succeed. Manufacturing; no training, model modification, new threshold, new reference, mode selection, protected test access or new simulation is authorized by this protocol. The target is the exact Q1/seed17 epoch14 checkpoint and all 36 previously exposed Q1 episodes from v0.21. It is exploratory and cannot confirm a new contribution.

## Inputs and scoring

Inherit and verify every v0.21 replay freeze binding. Bind this protocol/source, the exact checkpoint/config/normalizer, input catalog and every original saved score file. No input signal is opened during preparation; file hashing is byte identity only. During execution read only existing `measurements`, `commands`, `valid` and saved RAPT `loss`. No truth/state/counterfactual/attack arrays are opened. Quarter boundaries use the already frozen v0.19 task schedule, not newly inferred labels.

Mirror the released `score_sequence` forward path exactly: training-normalized observation t−1 concatenated with unnormalized protected action t−1 predicts normalized observation t in one causal GRU pass. Same fixed model, one CPU thread, no new seeds. Preserve mean, log variance, squared prediction error **before predicted-variance division, in training-normalized units**, released standardized squared error, defined-score mask and warmup eligibility. Row zero is undefined and padded with zeros solely for alignment, as in the released score; it is excluded from all summaries. Require byte-identical numeric per-channel score arrays against every v0.21 saved `loss` array before interpreting decomposition.

All 129,600 input rows and 126,000 eligible rows remain. Report every episode and channel, not only persistent offsets. For interventions, first/last quarter definitions match the frozen schedule (brief duration for brief offset; task duration for persistent/hold/slow). For normal and authorized-change episodes, summarize the full eligible interval and its first/last quarters. These longer benign quarters are not identical-phase controls for intervention quarters and will not be presented as such.

For each region report arithmetic means of prediction, log variance, variance, squared error and released score. On explicitly counted rows with positive squared error and positive released score, report the identity `mean(log score)=mean(log squared_error)−mean(log variance)` up to declared float32 roundoff (2e−5 maximum per-element discrepancy). Report excluded zeros; do not add an epsilon or hide them. First/last differences use their respective positive supports and show both counts. Differences describe the arithmetic origin of score changes, not the causal role of recurrence, adaptation, task shift or training. Risk is a maximum of several channel/gate ratios; per-channel log means must not be described as an additive causal decomposition of pooled risk.

## Verification and budget

Six synthetic tests exercise exact parity with upstream scoring using a known causal fake model, preceding-input alignment, undefined-row handling, future-prefix independence, log identity/zero reporting and schedule interval semantics. These fixtures load no learned checkpoint or benchmark data. They must pass before freeze.

One supervised attempt with 60 seconds wall, 45 CPU seconds, 1 GiB sampled RSS and 25 MiB total output. Previous full Q1 replay took 4.023 seconds wall; approximately 5–10 seconds is expected for this simpler no-fit pass plus output, not guaranteed. The existing supervisor, CPU limit and BudgetWriter are retained. No silent retry or disabled memory monitoring; if macOS `/bin/ps` needs permission, obtain monitor-enabled execution. Output is `local/novelty_v0.22/decomposition_001/`; earlier runs and sources are read-only.

Working directory `/Users/matrixusman/CUI/DigitalTwin/manufacturing`:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv-analysis-v022/bin/python -m unittest discover -s research_cycles/novelty_v0.22/decomposition -p 'test_*.py' -v
python3 research_cycles/novelty_v0.22/decomposition/freeze.py
# ROOT GO REQUIRED before the next command:
PYTHONDONTWRITEBYTECODE=1 .venv-analysis-v022/bin/python research_cycles/novelty_v0.22/decomposition/run.py
PYTHONDONTWRITEBYTECODE=1 .venv-analysis-v022/bin/python research_cycles/novelty_v0.22/decomposition/verify.py
```

The worker records actual environment, dependencies, Git revision/dirty state, model seed, selected checkpoint, source/input freeze, access list, score parity, timestamps, timings and resource outcome. The inherited hashes document the previous split/normalizer/threshold provenance. An independent saved-array verification must check shape/support, unchanged score identity and summary arithmetic before reporting findings. This preparation does not claim execution or successful parity.

## Runtime bridge

The historical forecast interpreter symlink points to removed Homebrew Cellar `python@3.12/3.12.15`; the installed stable opt path resolves to `3.12.15_1`, still reporting Python 3.12.15. Root explicitly authorized creating `.venv-analysis-v022` with that installed interpreter and `-m venv --without-pip`, then adding one `.pth` in the new environment pointing to the same project's existing forecast site-packages. No package install, network access, old-environment mutation or system package change occurred. Imports and synthetic tests must pass before inference. `RUNTIME_BRIDGE.json` records actual versions/build and package inventory. This preserves old artifacts and is an exploratory compatibility bridge, not a fresh independent environment installation or portability proof.
