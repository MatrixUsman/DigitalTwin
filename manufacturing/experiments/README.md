# Experiments — Smart manufacturing

**No training or benchmark runs/results exist.** The [software test report](SOFTWARE_TEST_REPORT.json) records synthetic correctness tests only; detailed receipts and source snapshots live under ignored `local/software_validation/`. From the project root, future real-data outputs belong under ignored `experiments/runs/<project-id>_<run-id>/`; use project ID `manufacturing`. Do not place data-bearing outputs in tracked documents.

For every reported run record: owner/operator, command and working directory, seeds, resolved config/hash, raw/split/processed hashes, source revisions and dirty patches, upstream method version, dependency lock, hardware/device, timestamps, logs, calibration/metric definitions, scores/alignment metadata, measured runtime/memory, outcome and failures.

Keep proposed plans separate from executed records. Start with correctness checks and an authorized bounded pilot; obtain approval before lengthy training or paid compute. Preserve negative results and failed runs. Summaries may enter tracked Markdown only after checking that no restricted records/private links are exposed.

Training and test evaluation must use this project's frozen protocol; no cross-project score pooling or inherited test-tuned choices.

The [final-test freeze record](FINAL_TEST_FREEZE_RECORD.json) is a **pending template**, with null timestamps/artifact fields and empty model/run lists. It does not establish a fitted model, threshold, approval or completed freeze. The [evaluation plan](../docs/EVALUATION_PROTOCOL.md) and [protection procedure](../docs/FINAL_TEST_PROTECTION.md) require both normal and mixed final slices to stay outside development. Freeze the complete roster before calibration; freeze actual artifacts before final replay; save/hash all campaign scores before label joining and outcome release. Keep a prospective outcome-access ledger, including partial reveals, failures and retries. Prior metadata inspection is disclosed separately.
