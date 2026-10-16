# Research skill installation and use

Installed **2026-10-16**, following the user's instruction to install and use the recommended research skill. This is a project-local installation, not a global environment change.

Following the three-project reorganization, this installation is shared from the workspace root by `water/`, `manufacturing/`, and `smart_grids/`. It remains pinned and unmodified. Research outputs and any workflow state must stay in the active project's folder; the first verification report linked below concerns water only.

## Installed package

- Package: **ARS-Codex / academic-research-suite 3.23.1**, the maintainer's Codex adapter for the recommended `Imbad0202/academic-research-skills` suite.
- Source: [academic-research-skills-codex](https://github.com/Imbad0202/academic-research-skills-codex).
- Pinned adapter revision: [`71528d9349bcdacfbe94111f06d9e2d82215a44d`](https://github.com/Imbad0202/academic-research-skills-codex/commit/71528d9349bcdacfbe94111f06d9e2d82215a44d).
- Entry point: [SKILL.md](../.agents/skills/academic-research-suite/SKILL.md).
- Installed manifest identifies upstream ARS version 3.23.1 at `4c5449017f46eb64d112a301d4817d22c7c9f3d9`, and experiment-agent source at `e291e7dc7ca268b2de7e1a9cf23bc2eef5dc0651`.
- ARS attribution: Cheng-I Wu (Imbad0202), 2026. Its included license is **CC BY-NC 4.0**; original notices and component licenses remain in the installed tree. No license text was modified.

The official local skill-installer helper completed successfully using download mode. It copied the skill; no upstream setup script, hook, experiment, or test suite was executed. No Python dependencies were installed.

```sh
python3 /Users/matrixusman/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo Imbad0202/academic-research-skills-codex \
  --ref 71528d9349bcdacfbe94111f06d9e2d82215a44d \
  --path skills/academic-research-suite \
  --dest /Users/matrixusman/CUI/DigitalTwin/.agents/skills \
  --method download
```

Local inspection found 2,639 files totalling 38,418,357 bytes. The manifest parses and agrees with the entry-point version. The router, selected workflow, source-verification role, runtime policy, agent interface, and attribution files are present. Observed SHA-256 values:

| File | SHA-256 |
|---|---|
| `SKILL.md` | `5922ab7d20f251f4568694b4ebefbe89e04eecf42e332a0a22fd371b719ba38a` |
| `manifest.json` | `f0d04430ac291cf6549a2f343e8bb98a7eed91dde9b615b33a6c62c0dd3996c5` |

These are local provenance checks, not a full security audit or evidence that the skill improves research quality. The vendored directory is ignored by the project's `.gitignore`; this record permits reinstalling the pinned package. No Git repository existed at installation time; the later private-repository setup is recorded in [the shared work log](WORK_LOG.md).

## How it is used here

The first application is `deep-research` **fact-check** mode: a bounded, claim-by-claim recheck of baseline readiness and source support. It is not a systematic review, manuscript draft, or experiment run. Read the [first verification report](../water/docs/RESEARCH_READINESS_REVIEW.md) for findings and limits.

The shared [root AGENTS.md](../AGENTS.md) records the controlling requirements for all three projects: exact primary-source checks, inaccessible sources marked honestly, no test-attack tuning, no assumed dataset access, and the current task's scope. The [water instructions](../water/AGENTS.md) additionally governed the first water-specific verification; their dataset/baseline constraints do not apply to manufacturing or grids. Approximate metadata matching is not sufficient verification. Medical evidence hierarchies and automatic fabrication labels from failed searches are inappropriate for this task.

No optional hooks, paid services, cross-provider review, automatic monitoring, or full-team pipeline were enabled. These are instructions guiding the work, not runtime enforcement. The upstream skill files remain unmodified.

The skill is installed and available in the workspace skill catalog. Its instructions were read directly and applied during the installation turn, and it became discoverable on the following turn. Future use should name the active project, for example: `Work in water/. Use $academic-research-suite to fact-check the evidence supporting this baseline.`
