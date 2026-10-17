# Return-bound control v0.12

[Measured results](RESULTS.md): 20/36 synthetic normal traces meet the registered feasibility criterion; the overall gate fails. Twenty software tests and 2,665 saved-artifact checks pass. One small experiment attempt completed. This is a standard comparison control with known generator uncertainty, not a proposed novel detector or a CASPER attack benchmark.

- [Prospective plan and formulas](PLAN.md)
- [Prior-art/admission record](PRIOR_ART.md)
- [Frozen design](FREEZE.json)
- [Implementation](control.py), [synthetic generator/evaluation](study.py)
- [All 216 outcomes](ALL_OUTCOMES.json), [verification](VERIFICATION.json)
- [Preserved pre-freeze software failure/correction](TEST_DEVELOPMENT.md)

The frozen run is consumed; do not rerun it or alter its scientific inputs. New conditions or controls require a separate version. Existing CASPER training artifacts and the AFTER manuscript remain unchanged. The result report corrects the plan's overly strong “independent trace” wording: scenarios share paired innovations across the three seeds; inference is conditional per trace, not a joint guarantee across the study.

Next: operationally justify noise, bias and motion bounds using clean commissioning observations in the virtual plant, with equally informed ordinary observer controls. Close-prior-art comparison and contribution admission remain necessary before a new attack campaign.
