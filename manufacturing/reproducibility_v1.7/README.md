# Local reviewer reproducibility package for working revision 1.7

This directory assembles a local reviewer package. It is not a public release, a journal submission, a separately submitted manuscript supplement, or evidence of author approval. The main paper remains a single manuscript. No raw CASPER/voraus-AD files, prepared real observations, third-party vendor checkouts, compiler binaries, credentials or provider approval records are distributed.

The archive is built only after the final study and manuscript seals are confirmed. `ALLOWLIST.json` records exact relative paths, byte sizes, roles and SHA-256 identities. `BUILD_RECEIPT.json` identifies the archive. A final clean-extraction receipt is required before claiming that the package was tested. Current inventory alone does not establish that the final archive exists.

## Three different reproduction levels

1. **Lightweight result replay:** standard-library Python recomputes pooled and stratified v0.18/v0.19 counts, rates, delay distributions and conditional denominators from saved episode outcomes, checking them against saved summaries. This performs no fitting, simulation, new test exposure or dataset access.
2. **Scientific synthetic replay:** the included source, frozen configuration, normal synthetic commissioning inputs, fitted reference artifacts and saved synthetic traces support v0.18 alarm replay and v0.19 code inspection/re-execution. NumPy is required. Historical frozen attempts remain unchanged; fresh attempts need fresh destinations. Re-execution is not fresh confirmation because these conditions are exposed.
3. **Historical real-IMU training:** reports, source/configuration and dependency records are included, but original/prepared CASPER observations and real-data checkpoints are excluded. Reproduction requires separately lawful dataset access, source correspondence and pinned upstream repositories. This package does not claim that those historical fits can execute from the archive alone. Nominal forecasting is a different task from synthetic cyberattack recovery.

The original v1.6 and original failed RBF criterion remain historical evidence. v0.18 is an exposed-data diagnostic replay; v0.19's status and criterion are recorded in its own freeze and terminal result. The package does not turn either result into a novelty claim.

## Run the lightweight checks after extraction

From the extracted `manufacturing/` directory, with Python 3.11 or later:

```sh
python3 -I reproducibility_v1.7/test_package.py --verify-root .
python3 -I reproducibility_v1.7/replay_tables.py --output reviewer_replay_001
```

The second command refuses to overwrite an existing directory. It produces JSON/TSV tables and `REPLAY_RECEIPT.json`, with the exact saved inputs and number of numerical comparisons. All observed misses and absent clearance values remain explicit. Benign rates use wholly benign eligible exposure; they are not deployment-frequency estimates. The replay script uses paths relative to its extracted location, never the developer's absolute workspace.

Before the final study exists, maintainers may run the explicitly partial diagnostic command with `--allow-pending-v019`; such a receipt has `complete_requested_studies: false` and must not be presented as a complete package check.

## Inspect or re-execute the synthetic methods

The relevant executable sources are:

- `research_cycles/review_extension_v0.18/reproduce.py`: exact exposed synthetic replay in a fresh named attempt, under the original resource limits.
- `research_cycles/context_recovery_v0.19/mechanism19.py`: context, empirical envelope, alarm logic, metrics and declared criterion.
- `research_cycles/context_recovery_v0.19/sim19.py`: new virtual trajectories and attack/authorized-command transforms.
- `research_cycles/context_recovery_v0.19/worker.py`: development, numerical/resource pilot and final campaign stages.
- Historical import dependencies under `research_cycles/` and `src/mfg_twin/`; these remain at their original relative locations.

Consult each cycle's `PLAN.md`, freeze, verification and results before running it. The archived original environment used Python 3.12 and NumPy 1.26.4; exact actual versions are in run provenance. Do not install packages into a shared/system interpreter. The lightweight table replay above has no NumPy dependency. Method-level tests need the isolated study interpreter; for example, from extracted `manufacturing/`:

```sh
/path/to/isolated/python research_cycles/review_extension_v0.18/test_replay.py
```

The resource supervisor needs local process-monitor access. If the sandbox denies that access, preserve its failure; do not silently disable the bound. Historical provenance contains the original operator paths and commands as evidence. Those strings are not executable path dependencies.

The original workers also query Git and pip for provenance. A bare archive has no Git checkout. `portable_replay.py` makes exactly three checked provenance substitutions: current Git revision/status become `null`, and dependencies report the actually installed NumPy version. It records original/effective worker hashes, exact substitutions and the adapter hash, then executes the unchanged scientific calculation under its original limits. The original source, freeze and attempt receipts remain byte-for-byte intact. This is explicitly a **provenance-adapted execution**. For example:

```sh
/path/to/isolated/python reproducibility_v1.7/portable_replay.py --study 18 --output reviewer_alarm_replay_001
```

The same adapter supports `--study 19 --phase development|pilot|final`, using the included frozen inputs. Its final path respects the frozen `worker_compact.py` storage policy: reference roles 0/2/3 are retained, and the compact loader is explicitly rebound to the provenance-adapted worker. That loader substitution and both original/effective wrapper hashes are recorded. These are actual computations requiring their declared resource budget; the full scientific portable paths have not been executed in package validation. The lightweight table command does not run them. Repeating already exposed final conditions does not create new confirmatory evidence. All output destinations must be new.

## Manuscript and figures

`manuscript_arx_rbf_v1.7/` contains LaTeX, references, generated tables and scientific figure PDFs; the compiled working PDF is under `output/pdf/`. Existing build receipts record the tested Tectonic 0.17.0 environment. The original `build_pdf.py` uses that local cached compiler and is retained for provenance, not advertised as a portable binary installer. A reviewer with Tectonic can compile `main.tex` in the manuscript directory using their own compiler/cache. No manuscript content is uploaded by this package.

`integrate_review.py` regenerates the v0.18 diagnostic figure/tables from bound saved summaries and requires NumPy/Matplotlib. Run regeneration only in a working copy: generated figure PDF metadata can change and invalidate seals. Earlier figures are included with their source-value/report records; the bundle does not claim that every earlier training/input pipeline is self-contained.

The historical manuscript integrity audit also depends on the full original workspace and prior sealed revisions. It is retained as provenance, not claimed to run from this archive alone. `test_package.py` verifies this archive's explicit file closure; `replay_tables.py` independently checks the two new studies' saved numerical tables. The supplied LaTeX source archive contains the complete current paper, figures and references.

## Maintainer packaging commands

```sh
python3 reproducibility_v1.7/build_package.py inventory
# After final study and manuscript seals are confirmed, refresh the explicit list:
python3 reproducibility_v1.7/build_package.py inventory --refresh
python3 reproducibility_v1.7/build_package.py build --confirmed-final-seals
python3 reproducibility_v1.7/validate_archive.py \
  --archive reproducibility_v1.7/manufacturing-reviewer-v1.7.zip \
  --output local/reviewer_package_v1.7/clean_extract_001 \
  --science-python .venv-reproduction-v02/bin/python
```

The last command uses a new extraction directory, verifies archive identities and the two new scientific closures, runs eight package helper tests and both twelve-test synthetic suites, and recomputes the saved result tables. Its receipt records the actual existing interpreter; it is not a fresh dependency installation or a full scientific rerun. A failed attempt stays on disk and requires a new output name after a documented repair.

The local disk input cap is 350 MiB, approved for this package task. Every included file must match the inventory at build time. Symlinks, traversal, raw-data paths, environments and non-allowlisted `local/` folders fail closed. Previous inventories are preserved by hash. Do not publicly post or send the archive without the user's publication/sharing authorization and a final permissions review appropriate to the recipient.
