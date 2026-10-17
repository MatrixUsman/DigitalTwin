# Research roadmap for the three projects

Status: staged portfolio plan. Manufacturing has completed **254 synthetic tests, preserved pilot/control studies and bounded normal-only empirical motion-observer validation**. No paper baseline reproduction, attack benchmark or validated twin exists. Updated 2026-10-17.

## Working order

Cycle through **water → manufacturing → smart grids** for evidence and data feasibility first. A project waiting for provider approval can remain pending while another receives its audit. Once a project satisfies its own prerequisites, implement and run its baseline in a bounded session. Do not launch all three training jobs together on the shared machine.

| Stage | What we do for each project | Evidence required to finish |
|---|---|---|
| 0. Workspace and ownership | Separate contexts and storage; preserve previous work | Project brief, owner, instructions, status, and folders |
| 1. Feasibility and reading | Audit recent sector-appropriate papers and dataset access | Primary sources; exact known/unknown facts; candidate method/data compatibility |
| 2. Select question and comparisons | Narrow the threat model, twin role, and main baseline(s) | A question that the available observations can answer; common data within this project's comparison |
| 3. Acquire and identify data | Obtain authorized files; preserve originals and inspect metadata | Access record, file hashes, release/schema/label manifest, storage estimate |
| 4. Freeze evaluation and prepare software | Specify chronological splits, development calibration, metrics, versions | Protocol/configuration record; loader/split/metric/provenance tests; isolated environment |
| 5. Reproduce a baseline | Begin with a bounded pilot, then approved full runs | Run records and measured results; deviations and failures disclosed |
| 6. Test the research hypothesis | Specify and test a meaningful change against appropriate controls | Fair comparisons, repeated runs where needed, ablations, failure cases and limitations |
| 7. Develop the paper | Write from source notes, methods and measured evidence | Traceable claims, figures/tables, related-work comparison, contribution/authorship records |
| 8. Review and submit | Choose an appropriate venue and follow its actual instructions | Reviewed manuscript, dataset/publication obligations, explicit publication approval |

Writing notes starts in Stage 1. Results sections and superiority claims require Stage 5/6 evidence. Stage 0 is complete only after the folder/link/ignore checks; the rest is not implied by this scaffold. Timelines depend on access, learning needs, code availability, and measured runtime; no publication date is promised.

## Immediate next tasks

1. **Water / Muhammad Usman:** use the COMSATS student-email route for an authorized SWaT/WADI request, then identify releases. In parallel, read CAROTS and audit remaining preprocessing/device issues. The assistant has not submitted a request.
2. **Manufacturing / Haiqa Mushtaq:** use the [complete paper roadmap](../manufacturing/docs/PAPER_ROADMAP.md). The right-arm question/data/evaluation definitions, 254 synthetic tests, prior bounded pilot/control selection and empirical motion-observer validation are complete within their recorded scope. Velocity, a 32-bin template and AR(4) artifacts are ready for later calibration. The observer checks support a narrow empirical-state interpretation; ordinary AR remains stronger at one-step prediction. The [scope decision](../manufacturing/docs/CONTRIBUTION_AND_EVIDENCE_SCOPE.md) selects a narrow single-acquisition case study; next implement/test the bounded C/K/L/Rv score extension and admit the executable roster before calibration. Independent voraus-AD/NIST sources remain screened fault/benign candidates, not admitted cyber evidence. The [comparator audit](../manufacturing/docs/COMPARATOR_ADMISSION.md) excludes TWINE/CatBoost from Group D, records two original full manuscripts, and selects a conditional ModernTCN transfer. Neural adapter/configuration admission, CatBoost full text, physical-twin claims, novelty, calibration and final execution remain unresolved.
3. **Smart grids / Muhammad Usman Sanghla:** choose the electrical system and observation type; verify which leads provide attack recordings versus only simulation cases. Audit recent twin-based comparators and their code/protocol.

## Preventing accidental duplication

Water currently investigates adaptation contamination. Manufacturing now studies state synchronization against a fixed nominal progression reference under truthful monitoring telemetry; grids remain at a provisional domain theme. These are selected directions, not validated distinct contributions. Before Stage 6, compare the actual questions, threat models, assumptions, mechanisms and evidence. If the papers differ only by dataset or title, revise their scope before making three novelty claims.

Shared utility code may later be justified, but it needs a documented interface/version and per-project tests. Share algorithms by explicit design; never share learned transforms, thresholds, hidden test decisions, or results implicitly. All dataset users must be individually covered by provider authorization.

## A session request that keeps context clear

> Work only in `manufacturing/`. Read its instructions, brief and status. Audit the first dataset lead using primary sources, update the evidence register, and stop before downloading or running models.

After each session, the active project's `STATUS.md` should make the next session possible without relying on chat memory.
