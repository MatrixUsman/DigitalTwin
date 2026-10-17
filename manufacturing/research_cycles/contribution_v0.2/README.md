# Contribution investigation v0.2

This separate cycle advances the original-contribution objective without changing the completed CASPER experiment. It is **exploratory research and partial baseline reproduction**, not a finished contribution paper.

- [Execution scope](PLAN.md)
- [Measured findings, resources and failures](RESULTS.md)
- [Source claim/test dossier](../../docs/BASELINE_LIMITATION_DOSSIER_V0.2.md)
- [Candidate mechanism and fair comparison design](../../docs/CONTRIBUTION_DESIGN_V0.2.md)
- [Close recovery prior art](../../docs/literature/RECOVERY_PRIOR_ART_ADDENDUM_2026-10-17.md)
- [Concrete next study and independent-evidence gates](NEXT_STUDY.md)
- [Source-backed LaTeX research notes](research_notes.tex)
- [Actual state and artifact manifest](EVIDENCE_MANIFEST.json)
- [Single nominal-file identity and access record](../../datasets/manifests/casper12_v2_nominal_receipt.json)

Code is independent except for the identified MIT-licensed successor snippets extracted from a verified local notebook; see [NOTICE.md](NOTICE.md). Public manuscripts, upstream files, models, data and run outputs remain in ignored local storage. This package does not redistribute the dataset or claim the historical paper environment is reconstructed.

## Commands already executed

Working directory: `/Users/matrixusman/CUI/DigitalTwin`.

```sh
manufacturing/.venv-reproduction-v02/bin/python -m unittest discover -s manufacturing/research_cycles/contribution_v0.2 -p 'test_*.py' -v
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/contribution_v0.2/bounded_run.py run_diagnostics.py --attempt diagnostics_003
manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/contribution_v0.2/bounded_run.py run_normal_pilot.py --attempt normal_pilot_001
```

Do not rerun consumed attempts: the launcher refuses existing output directories. The launcher lists a future `run_mechanism_test.py` choice, but that worker **does not exist and has not run**. Only the two workers above are implemented; preserve the run-bound launcher bytes rather than retroactively editing a receipt. Environment versions are recorded in [the platform lock](requirements-macos-arm64.lock.txt), not assumed portable to every OS.

The final readback command is `manufacturing/.venv-reproduction-v02/bin/python manufacturing/research_cycles/contribution_v0.2/verify_artifacts.py`. It hashes stored bytes and checks saved arrays; it does not train or parse raw observations. It requires the local artifacts and should not be described as a standalone public reproduction package. The LaTeX notes have not been compiled or visually checked as a PDF in this cycle.

## Next gate

Resolve close-prior-art equations and full baseline training/preprocessing/state-policy correspondence, then demonstrate a method-level limitation under a predeclared exploratory protocol. The current proposed observer has not passed novelty admission. No full training campaign, attack evaluation, new simulator, protected test or original-contribution manuscript is complete. The user has explicitly selected public data and clearly labelled simulation because no physical testbed is available.
