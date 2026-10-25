# Paired analysis and portable addendum, v0.21

This local additive package completes episode-paired reporting for the **already exposed synthetic v0.19** study. It preserves v1.7 and its failed scientific criterion. Start with [REPORT.md](REPORT.md). This is not a new detector experiment, submission or publication.

The earlier v1.7 reviewer archive already passed clean extraction and table replay. Its receipt is retained under `inputs/CLEAN_EXTRACTION_RECEIPT.json`; this addendum does not replace that archive. Its prior verification covers saved tables and synthetic fixtures, not a fresh installation or complete retraining.

## Replay

Python 3.12 or later, standard library only. No installation, network, GPU or raw dataset is required. From this directory after extracting the addendum:

```sh
python3 -I test_analysis.py
python3 -I analyze.py --output replay_new
```

`replay_new` must not already exist. Compare its `paired.json`, `paired_effects.csv`, `episode_pairs.csv` and `REPLAY.json` with `results_002/`. Verification does not run `inputs/evaluation.py` or `inputs/mechanism19.py`; these are original metric-definition snapshots for inspection. Model fitting, simulation generation and score-stream replay belong to the original v1.7 package.

The workspace commands were run from `/Users/matrixusman/CUI/DigitalTwin/manufacturing`:

```sh
python3 -I research_cycles/paired_analysis_v0.21/test_analysis.py
python3 -I research_cycles/paired_analysis_v0.21/analyze.py --output research_cycles/paired_analysis_v0.21/results_002
python3 -I research_cycles/paired_analysis_v0.21/make_report.py
python3 -I research_cycles/paired_analysis_v0.21/package.py
```

`package.py` writes an explicit allowlisted ZIP and validates a clean extraction with tests and exact table replay. It refuses to overwrite an existing ZIP or validation directory. The ZIP contains only the seven specified original summary/source files, this addendum's code/report, generated descriptive tables and receipts. No raw physical data, vendor checkout, environment or personal approval record is included. It remains local; sharing/publishing still needs approval.

## Files and interpretation

- `INPUT_MANIFEST.json`: exact original paths, byte lengths and SHA-256 identities.
- `inputs/outcomes.json`: all 2,376 original synthetic method–episode summaries, unchanged.
- `inputs/results.json` and `catalog.json`: original totals, failed criterion and episode definitions.
- `results_002/paired.json`: three contrasts, all episode pairs, full missingness and group tables.
- `results_002/paired_effects.csv`: signed candidate-minus-comparator effects and wins/ties/losses.
- `results_002/episode_pairs.csv`: inspectable pair-level scalar values and metadata.
- `ATTEMPT_HISTORY.json`: initial reporting-schema failure and subsequent correction.
- `PROVENANCE.json`: actual analysis environment and source state.
- `PACKAGE_MANIFEST.json`, `BUILD_AND_REPLAY_RECEIPT.json`: exact identities and clean-extraction checks.

Main comparison names are `context_set` versus `base_dual`, `context_hysteresis` and `global_set`. The analysis unit is an episode pair on a finite reused simulator grid; three seeds are not three robots. The original overall result remains **failed**. Conditional delay improvements do not erase missed fresh detections, loss of physical support or already-inactive alarms.
