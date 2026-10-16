# Implementation — Smart manufacturing

The `mfg_twin` package now implements a read-only loader, frozen-metadata development wrapper, causal score/update coordinator and metric primitives. [Software validation](../docs/SOFTWARE_VALIDATION.md) records 83 passing synthetic tests. No model, trained reference or production final-evaluation runner exists.

Use the manufacturing-local [environment](../docs/ENVIRONMENT.md). The current package uses only the standard library and is tested with Python 3.15.0. Future preprocessing, baseline adapters and runtime supervision require their own scoped implementation/tests. Do not modify system packages or share mutable runtime state with another project.

Data transformations must preserve chronological and label alignment. No test labels may reach fitting, model selection, threshold calibration or online update gates.

`contract.load_study` verifies the registered data/evaluation metadata without raw access. `iter_development_records` permits only training/development, validates source byte identity before parsing, and can cap a declared prefix. Calibration/final access is deliberately unavailable. `data.iter_csv_partition` is a lower-level parser, not an access-control mechanism. Detectors receive only `Observation`; `EvaluatorRecord` and `ScoredPoint` remain evaluator-only. Pure metric functions require independently verified coordinates and masks.
