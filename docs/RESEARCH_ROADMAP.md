# Research roadmap for the three projects

Status: proposed staged work; **no experiments executed**. Updated 2026-10-16.

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
2. **Manufacturing / Haiqa Mushtaq:** validate whether selected leads actually represent a manufacturing process, contain relevant attacks, and support an explicit twin. Audit full papers and usable author code before choosing a baseline.
3. **Smart grids / Muhammad Usman Sanghla:** choose the electrical system and observation type; verify which leads provide attack recordings versus only simulation cases. Audit recent twin-based comparators and their code/protocol.

## Preventing accidental duplication

Water currently investigates adaptation contamination. Manufacturing and grids have distinct provisional domain themes, not approved contributions. Before Stage 6, compare the actual questions, threat models, assumptions, proposed mechanisms, and evidence across projects. If the papers differ only by dataset or title, revise their scope before making three novelty claims.

Shared utility code may later be justified, but it needs a documented interface/version and per-project tests. Share algorithms by explicit design; never share learned transforms, thresholds, hidden test decisions, or results implicitly. All dataset users must be individually covered by provider authorization.

## A session request that keeps context clear

> Work only in `manufacturing/`. Read its instructions, brief and status. Audit the first dataset lead using primary sources, update the evidence register, and stop before downloading or running models.

After each session, the active project's `STATUS.md` should make the next session possible without relying on chat memory.
