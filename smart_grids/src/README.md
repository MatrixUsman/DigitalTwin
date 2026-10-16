# Implementation — Smart grids

No model, loader, evaluator or package is implemented. The [reproduction plan](../docs/REPRODUCTION_PLAN.md) proposes the next stage.

When authorized, use small Python modules for loading/manifests, splits, preprocessing, calibration, metrics, baseline adapters and provenance. Establish a local isolated environment, then lock validated dependencies. Do not modify system packages or share mutable runtime state with another project.

Data transformations must preserve chronological and label alignment. No test labels may reach fitting, model selection, threshold calibration or online update gates.
