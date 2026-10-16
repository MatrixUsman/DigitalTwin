# Smart-grid project instructions

Inherit the shared research and workspace rules in [../AGENTS.md](../AGENTS.md). These instructions apply only inside `smart_grids/`; do not edit another project's files as part of this project.

- Owner: **Muhammad Usman Sanghla**. This designation does not assign authorship. Read `PROJECT_BRIEF.md` and `STATUS.md` before work.
- Current authorization is setup/scoping and bounded source verification only. Full audits proceed water, then manufacturing, then smart grids. No implementation, installation, simulation campaign, training, data download, contact, or publication is implied by folder creation.
- Use the root-installed research skill selectively through `../.agents/skills/academic-research-suite/SKILL.md`. Keep its installation and runtime choices unchanged. Do not run the full research-to-paper pipeline.
- Preserve the distinct topology/electrical-state consistency direction as provisional. Do not import the water project's gate, datasets, results, or baseline decisions as grid evidence.
- Separate observed laboratory/field attack recordings, simulated attack trajectories, network logs, and static electrical cases. A simulator or IEEE bus case is not an observed attack dataset. Label synthetic data and software fixtures explicitly.
- Distinguish authorized switching/load changes, physical faults, equipment/sensor faults, and cyberattacks. Preserve scenario provenance and ground-truth event intervals. Do not infer attack labels from electrical deviation alone.
- Record topology revisions, breaker-status source and trust, bus/branch identity, units, phase/reference conventions, operating point, sensor placement, observability, and missing-data handling. Do not assume measured breaker status is authenticated.
- Before future comparisons, freeze common grid releases/scenarios, accessible inputs, chronological and scenario-group splits, metrics, and calibration rules. Never tune thresholds, hyperparameters, checkpoints, preprocessing, or model choices using held-out test attacks. Keep adjacent windows and the same simulated trajectory out of different splits.
- A randomized or subsampled classification table must not silently become a chronological replay. If event ordering is unavailable, limit the task accordingly or find a suitable source.
- During replay, expose only information available at that time. Separate oracle simulator truth from detector inputs and score before any adaptation. Report attacks that are unidentifiable under the stated assumptions.
- Keep originals and restricted artifacts unchanged and out of Git under the project's `datasets/` storage policy. Verify permissions, manifests, and hashes before use. Do not upload dataset contents or publish project files without approval.
- Every later reported experiment must log seeds, configurations, commands, dependency/environment versions, simulator and case revisions, raw/split hashes, our and upstream code revisions, patches, hardware, timestamps, and outcomes. Distinguish reproduction, modified-protocol author-code evaluation, and independent reimplementation.
- Main comparative papers: 2023-10-16–2026-10-16 inclusive, preferably 2024–2026. Keep older background separate. Unknown or inaccessible sources are not fabricated sources. No novelty, superiority, operational safety, or live-deployment claim without evidence.
- Obtain approval before paid compute, lengthy runs, or publishing. Use an isolated project environment only when implementation is authorized; no system-package changes.
