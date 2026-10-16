# Configurations — Smart manufacturing

No executable configurations are frozen yet. Future configuration files should separately define dataset/release identity, preprocessing, chronological splits, calibration, metrics, method settings, seeds and runtime limits.

Keep private paths/credentials in ignored `local/` under the project root. Every run must save a resolved configuration and hash. Defaults imported from a sibling project or an upstream method require explicit review; never inherit its thresholds, test decisions or fitted transforms silently.

Protocol changes after test inspection require disclosure and an appropriate new evaluation design, not repeated tuning on the same held-out attacks.
