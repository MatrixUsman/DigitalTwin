# Dataset identity records

These files contain safe provenance and status metadata, never telemetry, private download URLs or approval-email contents.

- [LOCAL_INVENTORY_2026-10-16.json](LOCAL_INVENTORY_2026-10-16.json): observed scoped inventory. Empty file arrays mean no files received; they are not empty benchmark datasets.
- [RELEASE_CANDIDATES.json](RELEASE_CANDIDATES.json): source-backed target versions, expected names, label rules and explicitly remote host metadata. Not a received/frozen dataset manifest.
- [Stage 3 audit](../../docs/DATASET_IDENTITY_AUDIT.md): evidence, conflicts, timestamp/label checks and completion gate.

## Receipt manifest contract — not populated yet

After authorized receipt, create a separate versioned manifest per dataset/release. Keep raw bytes ignored and unchanged. A complete manifest must record:

| Group | Required fields |
|---|---|
| Status and authority | Dataset/project ID; receipt and verification state; safe source reference; applicable terms; authorized-user scope verified privately; acquisition time. No private links or email addresses. |
| Release identity | Provider alias exactly as delivered; collection period; revision date; ambiguity notes and documentary evidence; our separately named manifest ID. |
| Original objects | Original archive/member names; relative raw paths; observed bytes and SHA-256; provider digest and algorithm if supplied; comparison outcome and source. Include readme, schema and attack register. |
| Storage/schema | File format; CSV dialect/encoding or sheet selection; metadata/header rows; ordered original columns and roles; units and unknowns; feature schema digest. |
| Time | Original time fields; explicit parser; timezone status and evidence; first/last time; row count; cadence/delta summary; duplicate/reversal/gap counts and policies; recording boundaries. |
| Labels/events | Original label column/vocabulary; explicit normal/attack mapping; missing/invalid counts; event-register identity; endpoint convention; overlaps and reconciliation outcome. |
| Derivations | Separate startup/filtering exclusions; row-ID mapping; transformations and software versions; source/output hashes; conversion/caching paths outside raw storage. A derived manifest cannot replace the original one. |
| Audit/freeze | Inspection command, revision, interpreter/time, limitations, original hashes rechecked; common-release decision and unresolved blockers. Split/calibration manifests follow separately. |

Use JSON `null` for an unmeasured value with a reason/status; use zero only for an observed zero. Do not copy paper counts or remote sizes/hashes into measured fields. Preserve earlier manifests when evidence changes. Hashing authenticates byte consistency, not dataset labels, permissions or scientific validity.

Any checksum command shown in research notes is proposed until run on an actual file. No file-level SWaT/WADI receipt manifest exists at this stage.
