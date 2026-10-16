# Datasets — Smart manufacturing

**No benchmark data is present.** Public retrieval without institutional approval was verified for original CASPER and several alternatives; response bodies were not read. See the [access checklist](../docs/DATASET_ACCESS_CHECKLIST.md) for release, license and receipt prerequisites. Preferred candidate: original CASPER v3, CC BY-SA 4.0; do not silently substitute the newer CASPER 1 & 2 listing.

- `datasets/raw/<dataset>/<release>/`: ignored, untouched originals, after authorized acquisition.
- `datasets/processed/<manifest-id>/`: ignored derived outputs, traceable to originals and configurations.
- `datasets/manifests/`: future non-sensitive release/schema/split records; no manifests are populated yet.
- Private approval records, credentials and external paths belong in `local/`, never tracked files. These paths resolve from the project root.

Before loading, record authorized user(s), source, terms, exact filenames, sizes/hashes, release, schema, timestamps and label definitions. Use the same frozen files across this project's main comparisons. A sibling project's access or data is not automatically available here.

Do not upload dataset contents. A simulator/testbed description or a directory containing synthetic fixtures is not an acquired benchmark. Keep raw files immutable and verify hashes before/after loader checks.
