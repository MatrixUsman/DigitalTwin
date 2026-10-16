# Water project instructions

This project belongs to **Muhammad Usman** and concerns cybersecurity of water-treatment and water-distribution industrial control systems. It inherits `../AGENTS.md`; these local instructions retain the original water requirements. Read `PROJECT_BRIEF.md`, `STATUS.md`, `docs/LITERATURE_EVIDENCE.md`, and `docs/REPRODUCTION_PLAN.md` before experimental work. All local paths below resolve from `water/`. Ownership is not a final authorship decision.

Keep data under local `datasets/raw/` and `datasets/processed/`, author-code checkouts under `baselines/vendor/`, runs under `experiments/runs/`, and environments under local `.venv/` or `.venv-<method>/`. Do not use manufacturing or grid data/state, or propagate the SWaT/WADI requirement into those projects. Shared skill/machine records remain in `../docs/`.

## Scope and current state

- The title, trust-gating mechanism, and novelty are provisional. No baseline has been reproduced and no benchmark results exist as of the initial audit, 2026-10-16.
- Initial authorization is **audit and setup only**: documents, read-only inspection, literature verification, and a proposed experiment structure. Stop before substantial implementation or training. A later user instruction can authorize the next phase.
- Treat conversation notes and candidate lists as leads. Verify claims against primary sources; mark unavailable material and unresolved discrepancies explicitly. Absence from a search does not prove that code or a paper does not exist.
- Baseline publication window: 2023-10-16 through 2026-10-16 inclusive; prefer 2024–2026. Main comparisons must support both SWaT and WADI. Keep background, out-of-window work, and preprints clearly distinguished.

## Data and evaluation

- Do not assume dataset access. Confirm authorization, exact release, original filenames, hashes, schema, labels, and provider documentation before loading benchmark data.
- Keep raw datasets unchanged and out of Git. Store raw data, processed copies, checkpoints, scores, and potentially sensitive logs in ignored local locations. `.gitignore` is a precaution, not proof that a file is safe to publish.
- Do not upload dataset contents, submit access requests, contact authors, or publish files without explicit authorization. Respect provider terms; user approval alone does not grant redistribution rights.
- Freeze consistent releases, eligible inputs, label semantics, chronological splits, score alignment, and evaluation rules across compared methods. Document every method-specific preprocessing exception.
- Split before constructing windows. Fit scalers, imputers, feature selection, model selection, and calibration on their designated development partitions only. Avoid future-looking interpolation and cross-split window leakage.
- **Never tune thresholds, hyperparameters, checkpoints, preprocessing, or model choices using held-out test attacks.** Test labels belong only to the final evaluator. Never execute an upstream oracle-best-F1 selection path as our evaluation protocol.
- Report unadjusted metrics as the main results. Never silently substitute point-adjusted F1, optimal test thresholds, or published headline numbers. Label any protocol modification explicitly.
- During online replay, score before updating; adaptation cannot access true attack labels or future samples. Distinguish state estimation, model-parameter learning, and residual/threshold calibration.
- Label all artificial fixtures and perturbations as **synthetic**. Smoke tests are software checks, never benchmark results. Measurement-level changes do not establish physically valid operational changes.

## Reproducibility and claims

- Every reported experiment must record seeds, resolved configuration, dataset and split hashes, preprocessing, dependency versions, interpreter, hardware/device, exact commands, our code revision and dirty state, upstream code revision and patches, timestamps, and logs.
- Classify work accurately: faithful reproduction, author-code run under a modified protocol, or our independent reimplementation. A faithful algorithm implementation can still have a modified evaluation protocol.
- Preserve failures and negative results. Do not fabricate citations, dataset access, measurements, results, or uncertainty intervals.
- Do not claim novelty, superiority, causality, physical fidelity, or live deployment without supporting evidence. Benchmark success is not evidence of operational safety or a full APT-defense capability.
- Get approval before paid compute, lengthy training, or publishing. Before proposing a long run, give a concrete configuration and measured resource estimate from an authorized bounded pilot.

## Workspace discipline

- Do not change unrelated files, system packages, or existing shared environments. Use a project-local isolated environment when implementation is authorized; keep upstream methods isolated where dependencies conflict.
- Prefer small, explicit Python modules and configuration files over application infrastructure. No web app, cloud service, database, or deployment work is in scope.
- Add meaningful tests for loading, chronological isolation, label/score alignment, calibration independence, metrics, and provenance before any benchmark claim. Synthetic tests must run without private data or network access.
- Keep source URLs, access dates, manuscript versions, paper sections, and code permalinks with literature evidence. Recheck unresolved facts before promoting a candidate into a main comparison.

## Installed research skill

- Use the shared root `academic-research-suite` (ARS-Codex), starting with `../.agents/skills/academic-research-suite/SKILL.md`. Installation provenance and usage are in `../docs/RESEARCH_SKILL_SETUP.md`. Load only the workflow relevant to the current authorized task; keep generated notes/state inside `water/`.
- For the present audit, use bounded source verification / `deep-research` `fact-check` mode. Installing the suite does not authorize experiments, manuscript results, or a full research-to-paper pipeline.
- These project research rules govern skill use. Approximate title/year matches establish neither exact paper identity nor support for a claim. Check primary metadata and the actual passage, table, or code; separate paper existence, claim support, implementation availability, and reproduction readiness.
- Failed searches or inaccessible sources mean **unverified/inaccessible**, not fabricated. Never classify a source as fabricated solely because lookups fail. Do not use arbitrary citation quotas or medical-study evidence rankings to decide ICS benchmark quality.
- Keep the current model/runtime choices. Optional hooks, cross-provider model calls, API-based verification scripts, scheduled monitoring, and full-team automation are not enabled by this installation. Use ordinary primary-source browsing for the audit.
- The suite provides workflow guidance, not a technical guarantee of citation accuracy or enforcement. Preserve its original files and license notices; record any future version or local modification before use. Its bundled example/test data are third-party skill fixtures, not SWaT/WADI access or our research results.
