# Bounded CASPER receipt and identity utilities

These standard-library scripts supported the authorized 16 October 2026 data audit. They are not model implementations, benchmark loaders or general dataset tools. Run locations and exact outcomes are in [the identity report](../docs/CASPER_DATASET_IDENTITY.md); raw inputs remain ignored and read-only.

| Utility | Scope |
|---|---|
| `acquire_casper_v3.py` | Original author Kaggle collection only; check v3/file inventory/license/storage, collect archive, verify safe members/CRC/SHA-256 and preserve originals. Uses the latest endpoint bracketed by version checks, not a guaranteed version-specific URL. |
| `profile_casper_v3.py` | Read-only full CSV structural, native timestamp and label-run inventory; bounded nested-field inspection. Writes profiles to ignored local audit storage. |
| `inspect_casper_alignment.py` | Full numeric original/fixed IMU comparison and cross-arm label/native-clock correspondence; no inferred synchronization or detector fitting. |
| `audit_casper_controller_schema.py` | Complete nested-vector/scalar parsing and concurrent hash confirmation for both controller CSVs. |
| `audit_casper_annotation_lineage.py` | Static notebook-slice extraction, index/support and label-class arithmetic; no sensor processing or model execution. |
| `verify_casper_release.py` | Fresh hash/size/immutable-storage checks of archive and all members; passive PCAPNG framing, interface-resolution and packet timestamp audit without payload decoding. Writes a separate later audit receipt. |

The commands in the report record what was run. Do not automatically rerun acquisition: a repeated invocation refreshes provider metadata and the receipt. Preserve the completed receipt and attached profile provenance before any separately scoped re-acquisition or revision. Future changes must retain executed-script hashes and distinguish old outputs from new checks.

No upstream notebooks, pickle/checkpoint loading, packet replay, model training or cloud SDKs belong in this audit. Profile counts are dataset facts, not benchmark performance. The [comparison protocol](../docs/COMPARISON_PROTOCOL.md) lists the separate readiness gates.

Later full-schema and index checks have their own [schema manifest](../datasets/manifests/casper_controller_schema_audit.json) and ignored `local/casper_annotation_study/annotation_lineage.json`. They preserve the original receipt. See [sensor semantics](../docs/CASPER_SENSOR_SCHEMA.md) and [annotation lineage](../docs/CASPER_ANNOTATION_LINEAGE.md) for commands, checks and limitations.

The [release/clock register](../docs/DATASET_IDENTITY_REGISTER.md) consolidates the newest verification. Run `verify_casper_release.py` with ordinary Python (not `python -O`, since its validation uses assertions). Its current output location is fixed: preserve this completed integrity receipt and ignored profiles before a later rerun. Supplemental source-review and synthetic-check fields in the receipt were added after the raw verification command; the work log distinguishes those stages. Valid container framing is not proof of lossless capture, clock accuracy or synchronized sensors.
