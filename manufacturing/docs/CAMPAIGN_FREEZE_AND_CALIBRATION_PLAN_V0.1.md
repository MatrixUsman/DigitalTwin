# Model freeze, calibration and final pipeline — v0.1

## Material Passport

Manufacturing / Haiqa Mushtaq; 17 October 2026; academic-research-suite bounded experiment run/validation guidance. This is a pre-calibration execution specification. Actual success, hashes and resources belong in the subsequent report. Current user authorization covers model-choice freezing, fixed normal calibration and preparation/testing of final evaluation; final observations are not opened by this task.

## Scientific freeze

The [campaign configuration](../configs/casper_right_arm_campaign_v0.1.json) enumerates eleven deterministic methods, formulas, initialization, transformations, original finite search, failure rules and budgets. All selected training references already exist. No additional fitting, search, changes to score arithmetic or score selection are allowed. Each deterministic method runs once with seed `null`; seeds 17, 42 and 2026 remain the declared rule for stochastic methods, of which none is admitted. The principal contrast is O-RC minus O-R: both retain progression, differing only by the correction-score term. This supersedes the old policy's progression-omitted terminology, following the already recorded observer/scope decision.

Before opening calibration, the freeze command creates a non-overwriting actual selection record, source/configuration inventory, source snapshots, git revision/dirty patch, exact interpreter/dependencies/hardware, tested receipt, historical candidate outcomes and fitted-artifact hashes. It preserves the former empty final-freeze template as a historical local artifact. That empty template is intentionally replaced only after calibration; earlier consumed studies retain their original snapshots and receipts. Source-only additive modules leave old fitted artifacts, metrics, scores and consumed plans unchanged.

## Calibration

One attempt replays only `[702002,864003)`. After 1,528 warmup observations, each method must emit exactly 160,473 finite nonnegative scores at `[703530,864003)`. All eleven score streams are sealed before thresholds are computed. For each, sort ascending, choose rank 158,869, alarm strictly above it. Ties remain non-alarms. No interpolation, alternate percentile, persistence, fusion or seed choice is permitted. The saved scores independently reconstruct every threshold. The result is an empirical calibration quantile, not a guarantee of a future 1% false-alarm rate. Calibration parses no labels and neither fits parameters nor updates normalizers.

Limits: 600 seconds supervised wall, 300 seconds worker CPU, 1 GiB monitored RSS, 50 MiB outputs, polling every 0.25 seconds. Hardware monitoring is required. Failure consumes the attempt and retains logs, partial outputs and per-method failure status. No automatic retry or support trimming. Source SHA-256 scans cover whole bytes before and after replay; earlier CSV records are tokenized for positioning but their observations are not interpreted. No record at or beyond calibration end is requested. This is procedural protection, not a byte-read OS boundary.

## Final machinery prepared now, executed later

The final freeze contains actual model, calibration, source, dependency, mask and validation identities, eleven explicit run-matrix rows and exact commands. `--check-final` validates metadata and saved calibration artifacts without opening the raw source. Future feature scoring continuously replays `[864003,1762650)`, excluding only the common initial warmup, for 897,119 eligible endpoints. The held-out-normal/mixed boundary never resets state. Scores use explicit little-endian binary64; the separate coordinate stream includes all raw rows, including warmup. Labels, native absolute coordinates and event boundaries never enter a detector.

Future `--score-final` writes and hashes the entire declared roster before its accepted supervisor manifest exists. A distinct `--evaluate-final` verifies that manifest, every score stream, index, frozen threshold and the complete run matrix before opening labels. It joins only timestamps/flags, checks exact coordinates and annotation intervals, then uses the existing tested metric implementation. All eleven methods, all eight events and zero-labelled recovery intervals are reported. Complete campaign scores precede any label join or outcome release. Local outcome writes themselves count as exposure and receive ledger entries. Partial/failing evaluations remain failures, not success-only aggregates.

Final scoring is prospectively capped at 900 s wall / 600 s CPU / 1 GiB RSS / 256 MiB output; evaluation at 1,800 s wall / 1,200 s CPU / 1 GiB RSS / 256 MiB output. These are conservative abort ceilings, not measured runtimes or approval to execute in this task. Eleven full binary score streams alone need 78,946,472 bytes (about 75.3 MiB), so the earlier 50 MiB pilot output budget cannot hold this campaign. Single worker, standard library, no network/packages/GPU. No final run is triggered by freezing, calibration or preflight.

## Required verification

Synthetic tests must cover label-invariant features/scores (including deliberately invalid label strings), gap/warmup/partition isolation, exact parity with original control and observer APIs, immutable references, full-mask admission, tied quantiles, missing/nonfinite/reordered/altered scores, incomplete seals, altered references, model/threshold changes, label access blocked until all scores seal, continuous report-boundary replay, failure retention and one-attempt claims. Tests and preflight must not open real final observations. Saved normal calibration scores are re-read to independently verify thresholds and hashes. Frozen selection input identities are rechecked after execution.

This completes preparation for a narrow single-acquisition comparison if all gates pass. It establishes no attack performance, superiority, novelty, validated physical twin, generalization or paper reproduction. Calibration findings cannot reopen scientific choices. Any technical correction receives a visible record and new version when required; final outcomes never become development data.
