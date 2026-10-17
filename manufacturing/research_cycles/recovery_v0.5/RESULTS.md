# Recovery pilot v0.5 — completed exploratory findings

**The physical pilot is implemented, executed and verified.** Two simulated plants, three paired noise seeds, 18 normal training episodes, 18 separate normal calibration episodes and 48 evaluation episodes produced 528 method–episode outcomes. Every declared method and outcome is retained. No CASPER observations or new real-world test recordings were opened.

The comparator roles are finalized in [COMPARATORS.md](COMPARATORS.md). The executable paper-derived reference remains our independent Edge-2025 architecture implementation in the separate recorded-IMU track. CASPER requires a separate reproduction path; TWINE and CatBoost are outside this normal-only comparison; ModernTCN is a reserved modified transfer. No three-paper faithful reproduction set or published headline score is claimed.

## What was tested

The [frozen plan](PLAN.md) specifies an idealized horizontal two-joint arm, PD servo, Gaussian sensing noise and two mass/friction variants. The monitor receives truthful noisy joint states plus protected approved commands and their validity flag. Unauthorized command changes occur downstream of that protected reference. Authorized changes affect both the approved and executed program. A corrected following observer and an uncorrected command-driven reference predict prospectively; labels never control them.

All fitted transformations, AR/ARX coefficients and error normalizers use synthetic normal training only. Thresholds use 16,200 normal calibration targets, rank 16,038, strict exceedance. There is no parameter search or outcome-selected threshold. Each evaluation episode contributes 900 eligible points; each method has 43,200 points. All scores were sealed before outcome joining.

The candidate triggers on either normalized observer error and clears after ten consecutive valid observations below both low thresholds. The pre-run [algebraic audit](PRIOR_ART.md) established that it is exactly fused-error dwell-time hysteresis. Separate implementations agreed throughout the pilot. This rule is therefore retained as an ordinary control, not an original contribution.

## Complete comparison

“Clean normal” uses the 18 fully benign evaluation episodes: unchanged motion, authorized offset and authorized slowdown, totaling 16,200 eligible observations. Recall/F1 use all 48 episodes and **attack-command interval labels**, with 4,830 corrupted-command points. A physical transient can continue after the command is restored; post-command alarms are therefore reported separately and cannot all be interpreted as erroneous state alarms. This label distinction is essential when reading F1.

| Method | Clean normal alarms | Attack-command recall | Point F1 | Event overlap; fresh start | Post-command alarm points |
|---|---:|---:|---:|---:|---:|
| persistence | 1.01% | 3.85% | 0.064 | 30/30; 30/30 | 640/7,500 |
| ar4 | 1.02% | 3.48% | 0.058 | 30/30; 30/30 | 582/7,500 |
| arx4 | 1.06% | 91.72% | 0.879 | 30/30; 24/30 | 650/7,500 |
| following | 1.07% | 92.05% | 0.885 | 30/30; 24/30 | 594/7,500 |
| following_mean45 | 0.99% | 92.05% | 0.802 | 30/30; 24/30 | 1652/7,500 |
| following_cusum | 1.02% | 87.08% | 0.397 | 24/30; 18/30 | 6000/7,500 |
| command_reference | 1.00% | 92.05% | 0.755 | 30/30; 24/30 | 2339/7,500 |
| fused | 1.00% | 92.05% | 0.755 | 30/30; 24/30 | 2334/7,500 |
| following_hysteresis | 5.52% | 92.05% | 0.735 | 30/30; 24/30 | 1858/7,500 |
| fused_hysteresis | 3.49% | 92.05% | 0.708 | 30/30; 24/30 | 2710/7,500 |
| candidate_recovery | 3.49% | 92.05% | 0.708 | 30/30; 24/30 | 2710/7,500 |

No point adjustment. Unknown decisions count as misses on attack support and never earn true negatives. Context-dependent methods have 360 unknown evaluation points, all during the six declared 60-point context gaps. Their full-support coverage is 99.17%, and their overlap detection delay there is 1.20 s. Fresh-onset counts conservatively require a known previous decision; returning from an uncertain interval is not credited as a fresh onset. Persistence/AR retain 100% context-independent decision coverage.

## Findings and implications

1. **Trusted context supplies the largest detection improvement.** AR(4) has 3.48% command-interval recall; ARX(4), given the same protected commands as the observer, reaches 91.72%. The following observer reaches 92.05%. Physically identical authorized/unauthorized offset observations differ only in their approved context. Motion alone cannot reveal that distinction. These results do not establish that a novel twin is needed.
2. **The ordinary following observer already retains sustained-change evidence here.** It detects all 30 intervention episodes and has no clearing transition during command corruption. Adding the immutable reference or hysteresis gives no recall gain on this matrix. This differs from the earlier CASPER-family measurement-replay behavior; mechanisms and input access differ, so the results should not be pooled.
3. **Recovery is a different objective from command-interval F1.** The declared physical-return diagnostic is the first start of ten consecutive observations for which the true simulated state is within 0.1 training standard deviations of the nominal command reference on every channel. It is evaluator-only and is not a safety certificate. The following observer's first post-command clear precedes that diagnostic in 30/30 events, by 0.84–2.18 s. The fused hysteresis/candidate clears 0.16–0.20 s after it in 30/30. All 30 candidate alarms clear within the five-second evaluation horizon. Ordinary fused hysteresis achieves exactly the same result.
4. **That recovery behavior costs normal alarm time.** The candidate alarms on 565/16,200 benign targets (3.49%), versus 173/16,200 (1.07%) for the following observer. All 565 candidate normal alarm points occur in authorized-offset episodes. The candidate has fewer alarm starts but longer alarms: 21 benign episodes of alarm versus 57 for the following observer across 324 eligible seconds. Rates extrapolated from this short, scripted population are descriptive, not operational guarantees. A shared score percentile does not equalize stateful alarm burden.
5. **CUSUM has a concrete carryover problem under this frozen configuration.** It misses all six 0.10 s command-offset events and fails to clear within 5 s after the 24 longer events. The 45-observation mean detects the brief events here; the earlier v0.4 missed-brief result does not transfer across different sensors, amplitudes, dynamics and calibration.

## Verification, resources and failures

- 24 physics/causality/uncertainty tests passed after one preserved pre-run numerical failure. Four RK4 substeps missed the original one-step tolerance; eight substeps passed without relaxing it. Two additional synthetic tests cover the later serialization repair: **26 passing tests total**.
- **52,582 fresh-process checks** validate sealed identities, training-only fits through independent augmented least squares, rank calibration, complete alignment, decision replay, event/miss/unknown arithmetic, classical equivalence, exact episode regeneration and integration refinement. Another **422 checks** validate physical-return arithmetic, copied score identities and resource accounting. Total **53,004 passing checks**; these are software checks, not statistical evidence units or an independent human review.
- The predeclared full-trajectory refinement check gives maximum absolute errors `[1.62e-8,4.84e-8]` rad for angles and `[1.57e-6,4.69e-6]` rad/s for velocities, comparing eight and sixteen RK4 substeps on the selected episode. This establishes numerical consistency for that check, not hardware fidelity.
- `simulation_001` generated all scores in a 73.353 s supervised attempt (72.422 s CPU; 40.17 MiB worker peak RSS), then failed exporting a NumPy `int64` field. All arrays and the score seal survived. The failed attempt remains intact.
- `reporting_001` verified/copied those sealed bytes and exported the original outcome formulas with native scalar conversion. It completed in 0.393 s supervised wall and 0.379 s CPU, with 42.34 MiB worker peak RSS. No simulation, fitting, threshold or score was rerun or changed. [Failure and recovery record](REPORTING_RECOVERY.md).
- Both jobs obeyed their 600 s wall/300 s CPU/1 GiB RSS/50 MiB per-attempt output bounds. Keeping both attempts uses approximately 50.1 MiB of run artifacts in total, plus verification/source/figure storage. Sampled RSS monitoring is not an instantaneous ceiling.
- The 13-source/337-input scientific freeze and 99-identity export-recovery freeze remain unchanged. Older CASPER campaigns, v0.2–v0.4 artifacts, PDF and environments retain their identities.

Hardware: Apple M5 Pro, 24 GiB RAM, 18 logical CPUs; Python 3.12.15 and NumPy 1.26.4. The unchanged environment and command receipts are retained locally. The plotting job used the existing separate project environment. Matplotlib fell back to a temporary font cache; both figures rendered successfully and were visually inspected. One ad-hoc result-inspection command used system Python without NumPy and was rerun in the existing isolated environment; it changed no scientific artifact.

## Figures and traceability

[All-method comparison](../../output/recovery_v0.5/comparison.png) · [PDF figure](../../output/recovery_v0.5/comparison.pdf) · [Saved timelines](../../output/recovery_v0.5/timelines.png) · [PDF timelines](../../output/recovery_v0.5/timelines.pdf).

[Machine-readable complete aggregates](RESULTS.json) contain every method/condition, misses, delays and clear outcomes. Local `runs/reporting_001/outcomes.json` contains all 528 rows; its original provenance and failure are retained. `summarize.py` and `plot_results.py` generate reporting from saved artifacts. Verification is in local `verification/verify_001/` and `verification/reporting_001/`. `PACKAGE_MANIFEST.json` binds the completed package.

## Scientific decision and next bounded step

The implementation/pilot milestone is complete. The proposed rule **does not qualify as a novel algorithm**; both the algebraic equivalence and close prior art prevent that claim. Its measured physical-return behavior is useful baseline evidence. Retain ARX, following error, mean45, direct reference and fused dwell-time hysteresis in the next comparison.

The next specific problem is **reducing prolonged alarms during legitimate command changes while retaining evidence until physical recovery under model mismatch**. First diagnose the existing authorized-offset residuals and distinguish mismatch-driven error from an inadequate static calibration; that analysis is exploratory on these exposed outcomes. Then specify a mathematically non-equivalent uncertainty/recovery rule and compare it with mode-conditioned calibration, ordinary dwell hysteresis and existing set-consistency/observer approaches. Obtain the closest 2026 recovery manuscript where lawful access becomes available before making fine-grained novelty claims.

Any next confirmation must freeze new task frequencies/geometry/mismatch groups before generation. None of those future groups has been generated in this cycle. Seeds here alter measurement noise on two fixed plants; they are not independent robot acquisitions. The same equation family supplies plant and observer, trusted context is assumed, and no hardware, contact dynamics, adversarial sensor forgery, physical mitigation or broad superiority is established. The original-contribution paper remains the destination; this pilot supplies concrete mechanism evidence and a stronger required control set.
