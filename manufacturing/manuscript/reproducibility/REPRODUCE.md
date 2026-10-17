# Reproduction instructions and remaining dependencies

## 1. Verify this presentation package without dataset access

Use Python 3.15.0 for parity with the recorded environment; the manuscript tools use only the standard library. No package installation or network is needed. From `manufacturing/`:

```sh
.venv/bin/python manuscript/tools/build_assets.py --check
.venv/bin/python manuscript/tools/verify_package.py --receipt local/manuscript_v0.1/package_check.json
```

These checks reject raw-dataset opens and network connections in their Python processes. They verify hashes, roster/support, aggregate point/event arithmetic, claim-span identities, citation keys, input files and elementary LaTeX syntax, then compare regenerated asset bytes. This is process-local instrumentation, not an operating-system isolation guarantee. The output receipt states the unperformed checks, including model replay, new software-test execution and PDF rendering.

The generator reads the seven JSON inputs, not protected trajectories or labels. Mean-normalizer/model numbers come from the saved normal-development summaries; final outcomes come from the completed campaign summary. The reference register generates both bibliography forms. Do not edit generated tables to improve a reported outcome.

## 2. Understand the exact experimental dependency chain

Historical order: synthetic validation → bounded velocity pilot → full normal-only controls → normal observer → four-score extension → actual selection freeze → normal threshold-only calibration → final scoring seal → delayed joint evaluation. Reports and local receipts retain intermediate failures and attempts. All eleven final methods are deterministic; the policy seeds 17, 42 and 2026 were not instantiated because no stochastic model was admitted.

`inputs/MODEL_SELECTION_FREEZE_V0.1.json` binds scientific choices and fitted artifacts. `inputs/FINAL_TEST_FREEZE_RECORD.json` binds actual calibration/thresholds and the pre-execution run matrix. `inputs/FINAL_CAMPAIGN_V0.1_RECORD.json` records completion, resources, exposure and run artifacts separately. Original run folders and consumed attempts must remain intact.

Historical final commands, from the original manufacturing directory, were:

```sh
.venv/bin/python scripts/run_campaign.py --check-final
.venv/bin/python scripts/run_campaign.py --score-final
.venv/bin/python scripts/run_campaign.py --evaluate-final --score-run experiments/runs/campaign_v0.1_score-final_2026-10-17T062117.703085_0000
```

These document completed commands; **do not run them in place or delete attempt ledgers to make them run again**. The accepted evaluation directory was `campaign_v0.1_evaluate-final_2026-10-17T062627.210253_0000`. Whole-worker caps/measurements and source seals are in the completion record. No per-method latency data exist.

## 3. A future independent computation requires a separate workspace

1. Obtain the lawful original raw file and validate its byte identity using the data-access guide. Do not substitute a new CASPER release.
2. Prepare a separate research directory and isolated environment. Copy the exact `snapshot/` tree; preserve source hashes and original records as references. Do not point output paths at original experiment storage.
3. Inventory the 133 dependencies and all final-completion references. The package excludes model files, row-level scores, manifests/resource logs and the complete original receipt/attempt chain. Retrieve these only from authorized local archives for saved-artifact verification, or generate **new** development/calibration artifacts through a separately versioned replication plan. Missing provenance must not be filled with fabricated receipts.
4. Test the copied synthetic suite and supervisor on the new host before real data. Original scripts expect project-relative metadata and Git/provenance context; their portability outside the original workspace has not been validated. Record necessary adapter changes and their new hashes rather than silently claiming an exact execution. Operating-system process monitoring needs an explicitly working local implementation.
5. Freeze the same scientific protocol and compare fitted artifacts/scores under documented numeric tolerance, retaining divergent outputs and every failure. New receipts describe computational replication of a known result, not fresh hypothesis confirmation.
6. Only an independently reserved acquisition can confirm a model redesigned after these outcomes. A fresh directory, seed or data reshuffle does not provide that evidence.

This guide intentionally distinguishes a runnable, verified **presentation** command from an **unvalidated full-study replay**. The latter is not completed or authorized by writing this package. No automatic download, dependency installation, training, robot operation, public upload or paid compute is part of these commands.
