# Common-input normal convergence study, v0.11

Prepared17October2026. Manufacturing / Haiqa Mushtaq, operator Codex. **Execution awaits approval for the stated longer local run.** The user's standing rule requires approval before lengthy training. Preparation and synthetic checks do not authorize execution.

## Exact purpose and changes

Continue the CASPER comparison adequacy work after [v0.10](../casper_comparison_v0.10/RESULTS.md). All three larger CNN fits stopped after three epochs; compact fits were still improving at epoch30. That is insufficient evidence of adequate training for a superiority claim. This version changes only the maximum epochs from30 to100, per-fit CPU admission budget from30 to240seconds, and total wall/CPU ceilings. Model architecture, zero-output initialization, loss, optimizer, minibatch ordering, raw normal prefix, causal preprocessing, gap rejection, scaler, seeds, score formulas and support remain identical. Our implementation files are copied unchanged. All models start afresh because v0.10 did not save optimizer state.

No learning-rate, architecture, filtering or scoring search. Three seeds17/42/2026 for both CNNs and three deterministic controls; retain all nine outcomes and every failure. Earliest normal-development improvement greater than1e-6 selects the checkpoint; patience5, no attack-label use. Per-fit budget admission uses the previous full epoch cost with1.25factor and1second reserve. First complete epoch always admitted; total limits are authoritative.

Same received provider-v2 nominal file and raw `[219,9185)` training / `[9185,12007)` development rows. At most12,007 numeric rows parsed; no new data release, attack, label, calibration or final access. Training8,192targets, development2,048targets, aggregate1,294targets. These are reused normal development, not independent confirmation. Lower development loss is not a security outcome.

## Resource contract and concrete command

One successful attempt allowed after user approval. **At most1,200seconds elapsed wall time,900seconds worker CPU,1GiB monitored RSS,50MiB outputs**, single CPU thread, existing isolated environment, no paid compute/package installation/network request. Expected duration is uncertain; the prior run measured approximately7.8CPU seconds per full larger-model epoch. A240second per-fit admission budget permits approximately30 such epochs, not a promise of100. Early stopping can end sooner. No automatic budget extension or retry; preserve and diagnose failures separately. RSS is sampled, not an instantaneous hard ceiling.

```sh
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/casper_convergence_v0.11/run.py
```

Before execution, an actual user response must be recorded in `RUN_AUTHORIZATION.json` with the matching frozen configuration digest and limits. `run.py` rejects pending or mismatched approval before creating a run directory. The existing process monitor needs `/bin/ps`; request scoped execution permission when running after user authorization, rather than knowingly repeating the prior sandbox-monitor failure.

## Readiness and outcome rule

Pass synthetic shape/causality/split/score/weight tests and approval-record checks, then bind all source/configuration files and predecessor identities before any real run. After execution, reload each saved model in a fresh process and independently verify predictions, metrics, support and checkpoint selection. This is a bounded adequacy check, not permission to open attacks.

Report stopping reasons by seed. If a CNN stops at the epoch/CPU cap while improving, it remains training-limited; do not rank it as an adequately converged CASPER comparator. If patience ends training, describe it as convergence under this local normal-development stopping rule, not proof of a global optimum or full-paper reproduction. Prefix representativeness and original publication-run correspondence remain separate limitations. No scientific choices will be made from attack outcomes, and no new PDF or novelty claim follows from this run.
