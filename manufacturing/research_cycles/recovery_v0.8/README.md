# Manufacturing contribution study v0.8

This separately versioned cycle follows the user's request for a precise contribution, worthwhile advantage and fair fresh confirmation. [Protocol](PLAN.md), [prior-art and comparator decisions](PRIOR_ART.md), [analytical results](ANALYSIS.md), and `FREEZE.json` define its scientific scope. All previous studies remain immutable.

The experiment fits command-driven references on clean commissioning observations, compares thirteen specified detectors/clearance rules, and evaluates recovery against an independent same-plant uncorrupted trajectory. It is entirely synthetic. Detection computations use only measurements, approved commands and availability. The worker passes a wider episode dictionary; three restricted-input replays verified identical outputs, but no enforced interface boundary is claimed. This is not a faithful rerun of CASPER, its successor or full FAIL-Detect.

Commands from workspace root:

```sh
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/recovery_v0.8/freeze.py
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/recovery_v0.8/run.py
```

The first launch was terminated before the worker started because sandboxed `/bin/ps` access prevented resource monitoring. Its receipts are preserved in `local/recovery_v0.8/runs/confirmation_001/`. The separate `launch_retry.py` checks that pre-worker failure and launches the unchanged frozen worker into `confirmation_002` with authorized process-monitor access. No scientific choice changed and no outcomes existed before the retry.

**Completed:** 216 episodes, thirteen methods and 2,808 outcomes, with fourteen pre-run synthetic tests and 9,610 post-run checks. [Results](RESULTS.md) and [review decision](REVIEW_AND_DECISION.md) reject the candidate as the intended original contribution: its benign alarm count fell from 621 to 309, but only 36/108 detected-returned events cleared on time. Removing the uncertainty allowance gave 140 benign alarms and 108/108 timely clearances at the same entry threshold. All 27 context-gap misses remain visible. The entire matrix is now exposed.

[Manuscript and PDF](../../manuscript_recovery_v0.8/README.md), [source access](SOURCE_ACCESS.json), [analytical explanation](ANALYSIS.md), [information-flow qualification](INFORMATION_FLOW_CHECK.json), and [normal-only admission diagnostic](NORMAL_ADMISSION.json) preserve what is established and what remains unresolved. No physical equipment is required. The stronger simple control is not automatically a novel replacement.

To verify existing artifacts without running a new experiment:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/recovery_v0.8/verify.py --run manufacturing/local/recovery_v0.8/runs/confirmation_002
```

The initial verifier attempt used different BLAS threading and failed exact coefficient replay; its diagnostic is preserved. The unchanged verifier passed with the worker's single-thread settings. No tolerance was relaxed. Current readiness and the next normal-only feasibility step are in `REVIEW_AND_DECISION.md`. No manuscript was submitted, no files published, and author declarations remain pending where unconfirmed.
