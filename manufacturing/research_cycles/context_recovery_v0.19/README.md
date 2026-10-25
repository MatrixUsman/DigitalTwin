# Bounded contextual recovery study v0.19

All data in this cycle are synthetic. See PLAN.md, RESOURCE_DECISION.md, RESULTS.md, REPORTING.json and VERIFICATION.json. The original-contribution objective remains open; the candidate failed its prospectively declared composite criterion.

`INDEPENDENT_REVIEW.md` records a separate AI-assisted read-back: 29,381 arithmetic checks, all 11 prospective clauses, and an explicitly post-evaluation diagnosis of initial delay and missed re-entry. It is technical verification, not human peer review. Of 679 candidate outside-tolerance inactive points, 299 precede initial detection and 380 follow it; 678 lie in the rule's uncertainty band. No final condition was retuned after this diagnosis.

Commands executed from `manufacturing/`, using the existing isolated `.venv-reproduction-v02`:

```sh
.venv-reproduction-v02/bin/python -m unittest discover -s research_cycles/context_recovery_v0.19 -p 'test_*.py' -v
.venv-reproduction-v02/bin/python research_cycles/context_recovery_v0.19/freeze.py development
.venv-reproduction-v02/bin/python research_cycles/context_recovery_v0.19/run.py development
.venv-reproduction-v02/bin/python research_cycles/context_recovery_v0.19/freeze.py pilot
.venv-reproduction-v02/bin/python research_cycles/context_recovery_v0.19/run.py pilot
.venv-reproduction-v02/bin/python research_cycles/context_recovery_v0.19/admit_final.py
.venv-reproduction-v02/bin/python research_cycles/context_recovery_v0.19/admit_compact.py
.venv-reproduction-v02/bin/python research_cycles/context_recovery_v0.19/run_final.py
.venv-reproduction-v02/bin/python research_cycles/context_recovery_v0.19/verify_compact.py
.venv-reproduction-v02/bin/python research_cycles/context_recovery_v0.19/report.py
```

The pilot failed conservative cost admission; admit_final.py failed its storage gate. These are preserved attempts, not successful commands. admit_compact.py initially had an import probe failure before its run directory existed; explicit source loading corrected it before final freeze. Its subsequent successful export check changed no scientific calculation. FINAL_FREEZE.json records the admitted wrapper.

Scientific launch commands refuse overwriting their consumed output directories. Do not run a frozen final campaign again in place. For lightweight independent descriptive replay use `reproducibility_v1.7/replay_tables.py --output <fresh-directory>`; that reconstructs tables from outcomes without training, physics or external data. The local reviewer package documents portable isolated reproduction and which historical real-data evidence requires separate access. Full fresh retraining/simulation is separate from saved-result replay.

Compact score archives retain all observations/commands/scores/alarms and the three references used by the11 declared methods, with explicit role indices. verify_compact.py independently reconstructs the other intermediate references from unchanged models and requires exact agreement for saved predictions/scores. Truth is stored separately and joined only after all final scores are sealed.
