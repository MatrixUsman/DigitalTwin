# Datasets — Smart manufacturing

**Original CASPER v3 is present locally:** unchanged archive plus five original files under ignored `datasets/raw/casper/v3/`, with CRC checks and SHA-256 hashes. It was acquired from the public author listing under its CC BY-SA 4.0 terms. See the [receipt manifest](manifests/casper_v3_receipt.json), [identity audit](../docs/CASPER_DATASET_IDENTITY.md) and [access checklist](../docs/DATASET_ACCESS_CHECKLIST.md). No newer CASPER 1 & 2 data was acquired. Received bytes do not resolve clock alignment, authentic IMU labels or experimental splits.

The current [identity register](../docs/DATASET_IDENTITY_REGISTER.md), [consolidated JSON](manifests/casper_v3_identity.json) and [SHA-256 file](manifests/casper_v3.sha256) record the exact release, all six fresh hash matches, label inventory and clock limits. Checksum paths are relative to `manufacturing/`. `arms.pcap` is PCAPNG with recorded epoch timestamps; controller clocks are boot-relative, and IMU time/labels are absent. These are separate time bases. No final annotation or split manifest is approved.

For the subsequently selected **right-arm normal-only study**, [contract v0.1](../configs/casper_right_arm_contract_v0.1.json) fixes the recorded schedule convention, exact row splits and permitted inputs for design review. Its [explanation](../docs/ANNOTATION_FEATURE_SPLIT_CONTRACT.md) preserves assumptions and execution gates. This is metadata, not a generated feature/label array or validated training loader; the IMU annotation track is unchanged.

- `datasets/raw/<dataset>/<release>/`: ignored, untouched originals, after authorized acquisition.
- `datasets/processed/<manifest-id>/`: ignored derived outputs, traceable to originals and configurations.
- `datasets/manifests/`: non-sensitive receipt/identity records; split manifests are not yet frozen.
- Private approval records, credentials and external paths belong in `local/`, never tracked files. These paths resolve from the project root.

Before loading, record authorized user(s), source, terms, exact filenames, sizes/hashes, release, schema, timestamps and label definitions. Use the same frozen files across this project's main comparisons. A sibling project's access or data is not automatically available here.

Do not upload dataset contents. A simulator/testbed description or a directory containing synthetic fixtures is not an acquired benchmark. Keep raw files immutable and verify hashes before/after loader checks.
