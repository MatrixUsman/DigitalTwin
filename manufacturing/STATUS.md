# Manufacturing status

As of **16 October 2026**. Owner: **Haiqa Mushtaq**. The user explicitly activated manufacturing while water waits for iTrust. Read the [selection report](docs/BASELINE_SELECTION_REPORT.md) first.

| Item | Actual state |
|---|---|
| Stage | Bounded literature, author-code and public-data feasibility audit completed with explicit gaps |
| Recommended setting | Industrial robotic arms; original CASPER pick-and-place collection |
| Title / question | Provisional; broad process/sequence question not validated against these data |
| Learning set | CASPER 2024, TWINE 2026, CatBoost on CASPER 2026; source/admission notes under `baselines/` |
| Shared-data evidence | Author-code links to original filenames; exact byte-identical release, common labels/inputs and published run correspondence not frozen |
| Public data access | Original CASPER v3 listing/terms and unauthenticated archive response verified; no institutional approval needed in that check |
| Local benchmark data | **Zero files** in manufacturing raw storage; no archive or CSV body acquired |
| First reproduction | CASPER conditional on code-use terms, label alignment and corrected calibration; none execution-ready |
| Other open routes | MIT synthetic machining/assembly; CMU TEP manipulations; no verified recent three-paper intersection |
| Environment / implementation / training | None |
| Benchmark results / novelty evidence | None |

## Important limits

- Original CASPER and CASPER 1 & 2 are distinct provider listings with different versions/terms. Some filenames and advertised sizes overlap; that does not establish identical bytes. `nicla_fixed.csv` provenance remains unresolved.
- CASPER's inspected threshold selection uses anomaly labels. TWINE uses random row splits and has inconsistent feature/model/demo paths. CatBoost's available script creates synthetic outlier labels, stacks incompatible sensor features as rows and scales before splitting. No such workflow is approved as our evaluation.
- CASPER observes external IMU; TWINE uses controller telemetry; supervised and normal-only training differ. Common collection does not automatically mean fair information access or a common detection task.
- TWINE and CatBoost full manuscripts remain inaccessible in this audit. Available code is not established as the exact code behind every published result. Original CASPER and CatBoost code licenses are unresolved; TWINE MIT license is verified.
- Motion deviations and environmental faults do not by themselves establish malicious intent. Digital-twin labels/cloud state storage do not prove predictive physical fidelity or novelty. The CASPER+ programme already describes closely related research ideas.

## Next bounded action

Prepare original-CASPER acquisition and exact-file identification, and finish the missing manuscript/run audit. Recheck storage, retain original provider terms, preserve received bytes, compute hashes and inspect clock/label/cycle alignment before selecting partitions. Resolve or transparently replace unsuitable comparator implementations. **Do not start training or an Azure/Factory I/O deployment.**

The three-paper list is for critical study; final comparative admission remains pending. If a clean shared-data comparison requires independent implementations or different features, record those changes before execution. No change has been made to water or grid research status.

## Evidence and persistent records

- [Admission rules](docs/BASELINE_SELECTION_CRITERIA.md), [selection decision](docs/BASELINE_SELECTION_REPORT.md), [literature register](docs/LITERATURE_EVIDENCE.md).
- [Open data](docs/literature/OPEN_DATASET_SCREEN_2026-10-16.md), [comparator manuscripts/code](docs/literature/COMPARATOR_SCREEN_2026-10-16.md), [twin methods](docs/literature/TWIN_METHOD_SCREEN_2026-10-16.md).
- [Access/receipt checklist](docs/DATASET_ACCESS_CHECKLIST.md), [proposed reproduction plan](docs/REPRODUCTION_PLAN.md), [work log](docs/WORK_LOG.md).
- [Shared publication standards](../docs/PUBLICATION_STANDARDS.md) and [repeatable playbook](../docs/RESEARCH_PLAYBOOK.md) remain in force. No title, venue, authorship or publication outcome is finalized.
