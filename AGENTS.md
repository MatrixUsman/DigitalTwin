# Shared research workspace instructions

This workspace contains **three independent academic digital-twin cybersecurity projects**, not a production application:

- `water/` — Muhammad Usman — water treatment and distribution.
- `manufacturing/` — Haiqa Mushtaq — smart manufacturing.
- `smart_grids/` — Muhammad Usman Sanghla — electrical grids.

Read `README.md` and `PROJECT_BRIEF.md`, then the active project's `AGENTS.md`, `PROJECT_BRIEF.md`, and `STATUS.md`. Resolve project-local paths from that project's directory. Root instructions apply to every project; child instructions add sector-specific requirements. Do not let a water-only rule silently constrain manufacturing or grids.

## Scope and task routing

- The user authorized restructuring and scoping these independent projects, followed by staged dataset/baseline work. Current readiness is recorded per project. Manufacturing has completed its explicitly authorized eleven-method protected final campaign and joint analysis: weak absolute detection and mixed control comparisons on one recording. Its holdout is exposed; outcome-informed redesign is exploratory and needs fresh evidence for a new confirmatory claim. No project has reproduced a paper baseline or established a novel general digital twin. Do not transfer manufacturing's completion or findings to the other sectors.
- Default work order is water → manufacturing → smart grids, one bounded milestone at a time. Continue useful independent planning while external access is pending. A user instruction can explicitly select another project.
- For an ambiguous request that could change multiple projects, establish the intended project before project-specific mutations; use session context when clear. Do not automatically replicate changes into sibling projects.
- Never overwrite another project's context. Shared notes are limited to workspace facts, common rules, scheduling, and explicit cross-project decisions.
- Keep each project's environment, configuration, raw data, derived data, fitted transforms, checkpoints, logs, and manuscript separate. Do not create cross-project dataset symlinks or reusable fitted-model state by default.
- Ownership is not final authorship. Record actual contributions and author-order decisions separately. Different sectors/titles alone do not establish distinct publishable contributions.

## Publication ambition, writing and titles

- Apply the user's confirmed preferences in `docs/PUBLICATION_STANDARDS.md` to **all three projects**. Aim for leading, credible, field-appropriate peer-reviewed journals through substantive contributions, demanding comparisons, reproducibility and honest limitations. Journal acceptance is an aspiration, not an assured outcome or a reason to inflate claims.
- Carry the baseline-selection discipline across sectors: distinguish learning papers, eligible candidates and execution-ready baselines; verify recent primary sources, common releases within each project, appropriate information access and clean evaluation. Three papers is an initial learning target, not a substitute for all scientifically necessary comparisons.
- Preserve the user's intended destination: original contributions grounded in demonstrated baseline limitations and justified improvements. A feasibility experiment or honest negative case study may be useful groundwork, but must not silently replace that destination. Distinguish verified code/protocol defects, hypotheses about method limitations, reproduced failure and established new contributions. Before treating a draft as the intended paper, reconcile its contribution with this objective. Manufacturing's post-PDF correction is recorded in `manufacturing/docs/ORIGINAL_CONTRIBUTION_DIRECTION_V0.1.md`; it does not establish completion in any sector.
- Write natural, precise academic prose that the researchers understand and can defend. Avoid generic AI-sounding filler, repeated templates, forced synonyms and unsupported adjectives; use the authors' actual notes and reasoning to develop their voice. Preserve required AI-use disclosure and do not make claims about guaranteed detector classifications or human-only authorship.
- Seek concise, distinctive, memorable titles grounded in the actual problem and supported contribution. Study strong articles' title structure without copying their names or wording. All current titles remain provisional; avoid forced acronyms and unsupported novelty, robustness, safety or superiority claims.
- The user intends possible future use of publications in a U.S. **EB-2** petition. Preserve accurate individual contribution, publication/version and independently verifiable impact records; do not assume all three papers belong to one person, infer a particular petition route, give unsupported eligibility assurances, or reshape results to serve that purpose. Future immigration analysis requires current official sources and a separately scoped request.

## Evidence and research integrity

- Never fabricate citations, access, measurements, results, or uncertainty intervals. Prior chats, snippets, and candidate lists are leads, not verified evidence.
- Default baseline publication window: **2023-10-16 through 2026-10-16**, inclusive; prefer 2024–2026. Dataset age is a different question. Document any justified eligibility changes before comparison. Keep background and preprints separate.
- Verify primary publisher/proceedings/manuscript and author-code evidence. Record dates, identifiers, review status, exact source versions, datasets/releases, preprocessing, evaluation, code revision/license, and limitations. Mark unknown or inaccessible facts explicitly.
- Distinguish paper existence, claim support, code availability, and reproducibility. Absence from search is not proof of nonexistence. Do not claim novelty, superiority, causality, physical fidelity, safety, or live deployment without evidence.
- Within a project's main comparison, freeze consistent releases, eligible inputs, labels, splits, score alignment, and metric rules. Different sectors may need different datasets/protocols; do not pool their scores into one ranking.
- Establish what the twin actually estimates/predicts and how it is coupled to observations. A generic classifier, static network trace, or simulator name does not establish a digital twin. A fault dataset does not automatically contain cyberattacks.
- Before expensive experiments, reconcile each proposed claim with close methodological prior art, the necessary explanatory controls and independent evidence units. A phase variable, synchronization or a renamed score alone does not establish novelty. Narrow unsupported claims; do not count rows/windows/seeds or repackaged releases as independent acquisitions. Separate decision/design completion from implemented comparisons and measured contributions. Manufacturing's completed case study is preliminary evidence; its current goal remains an original contribution. No manufacturing decision or result transfers to other sectors.
- Preserve negative results. Distinguish faithful reproduction, author-code execution under a modified protocol, and our independent reimplementation. Record every deviation.

## Data and evaluation

- Confirm access, authorized users, terms, exact releases, original filenames, hashes, schema, labels, and provider documentation before loading benchmark data. A shared folder or university email does not establish another person's access permission.
- Keep raw data unchanged under the active project's ignored `datasets/raw/` or an authorized external location. Derive outputs in `datasets/processed/`. Put private paths and approval records in that project's ignored `local/` directory.
- Do not upload dataset contents, submit access requests, contact authors/providers, or publish files without explicit authorization. Provider terms still govern redistribution. Ignore rules are a precaution, not publication approval.
- Split before window construction; respect chronology, episode boundaries and gaps. Fit transforms only on designated training/development partitions. Avoid future-looking interpolation and cross-split overlap.
- **Never use held-out test attacks to select thresholds, hyperparameters, checkpoints, preprocessing, architectures, or preferred variants.** Test labels belong only to final scoring. Do not execute upstream oracle-best-F1 selection as our evaluation protocol.
- Use unadjusted main metrics and explicit denominators; report event/delay and false-alarm behavior where meaningful. Never silently substitute point-adjusted scores, published scores, or optimal test thresholds.
- For online replay, score before updating. Gates/adaptation cannot use true test labels or future observations. Distinguish state estimation, parameter learning, residual calibration, and alarm threshold updates.
- Label artificial fixtures and perturbations **synthetic**. Smoke tests are software checks, not benchmark results. Measurement manipulation is not proof of physically valid operational change.

## Experiments and workspace discipline

- Maintain durable session records as part of every substantive task. At the start, read `docs/RESEARCH_PLAYBOOK.md`, the active project's `docs/WORK_LOG.md`, and its `STATUS.md`. At the end (and before a long task handoff), append what was actually done, evidence/artifact paths, checks and outcomes, failures, decisions, and the next bounded action to the project work log; refresh `STATUS.md`. Record shared setup changes in root `docs/WORK_LOG.md` instead of duplicating their details across projects.
- When a completed step teaches a reusable procedure, update `docs/RESEARCH_PLAYBOOK.md` with its prerequisites, instructions, expected artifacts, checks, and limitations. Label it proposed, audited, or executed/validated as supported by evidence. Reuse the procedure in another sector only after checking that sector's data, permissions, and scientific assumptions. Never copy completion status or results between projects.
- Keep logs chronological. Add corrections referencing earlier entries rather than silently rewriting history. Backfilled entries must say they summarize existing records, and must not invent commands, dates, or outcomes. Record exact reproducible commands and working directories when commands matter; keep secrets, personal access details, and restricted output in ignored `local/` or run storage and link only safe metadata.

- Every reported run records project ID, owner/operator, seeds, resolved configuration, dataset/split hashes, preprocessing, dependency versions, interpreter, hardware, exact command and working directory, our revision/dirty state, upstream revision/patches, timestamps, logs, and metric definitions.
- Validate loaders, chronology, feature/label/score alignment, calibration independence, metrics, and provenance before benchmark claims. Synthetic tests must work without private data or network access.
- Use isolated environments inside the active project; record platform-specific locks after validation. Never modify system packages, unrelated projects, or shared base environments. Keep upstream checkouts under that project's ignored `baselines/vendor/`.
- Get approval before paid compute, lengthy training, or publishing. Prepare a concrete run configuration and estimate from an authorized bounded pilot first. Schedule substantial runs sequentially on the shared machine unless resource capacity and user instructions support concurrency.
- Prefer small explicit Python research modules; no app, cloud service, database, deployment, or automatic monitoring is implied.
- At session end, update that project's `STATUS.md` with completed work, evidence paths, unresolved questions, next task, and actual run status. Never convert a proposed task into a completed result.

## Research skill

- Start from root `.agents/skills/academic-research-suite/SKILL.md`; provenance is in `docs/RESEARCH_SKILL_SETUP.md`. Keep the pinned package shared and unmodified. Select only the workflow relevant to the authorized task.
- Skill-generated notes, caches, passports, and run state belong to the active project, never sibling projects. This folder setup is not an executed research-to-paper pipeline.
- Project rules govern skill use: fuzzy title/year matches do not verify a source or its claims; failed searches mean unverified/inaccessible, not fabricated. Do not impose medical evidence rankings or arbitrary source quotas on engineering benchmarks.
- Preserve current model/runtime choices. Optional hooks, cross-provider calls, API verification scripts, scheduled monitoring, and fixed full-team automation remain disabled unless separately authorized.
- Skills are workflow guidance, not enforcement or accuracy guarantees. Bundled skill fixtures are not our datasets or results. Do not mark a paper as human-read on behalf of a researcher.
