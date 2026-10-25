# Local package attempt history

19 October 2026. The initial 1,447-member archive passed its own byte checks but failed the stronger clean-extraction check before any test execution: the v0.18 package manifest also binds its cycle's `.gitignore`, which the suffix-only inventory had omitted. All 400 v0.18 scientific freeze bindings had already passed. No result or scientific source changed.

The initial archive is preserved as `attempt_history/archive_001.zip`, SHA-256 `949f30983aa7264bc572e8d52f294b143852a5ff2b62354752677e44a882b200`, 323,167,849 bytes. Its build receipt and the failed `local/reviewer_package_v1.7/clean_extract_001/CLEAN_EXTRACTION_RECEIPT.json` remain preserved. The original receipt's archive path identifies the former location; this entry records the archival move.

The inventory policy now includes top-level research-cycle `.gitignore` files, closing that documented metadata dependency. It still rejects raw/processed dataset paths, vendor trees, environments, symlinks and unrelated local files. A fresh inventory, archive and extraction are required after this repair. The eventual external `CLEAN_EXTRACTION_RECEIPT.json` records their actual outcome; this repair note does not claim a test passed before it ran.
