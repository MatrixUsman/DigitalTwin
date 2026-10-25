# RAPT baseline admission and independent-recording route

Audit: 19 October 2026. Active project: manufacturing. Read-only source/data-metadata work and one bounded normal-only compatibility pilot. No final observations or original robot measurements were opened by this audit.

## Decision

**Admit the complete released RAPT online detector as an executable recent preprint comparator**, under a declared transferred-data protocol. Prefer its full default architecture rather than an arbitrarily weakened network. Retain its released gates and add a separately named manuscript-formula branch; do not silently equate them. The 60-second compatibility/cost pilot succeeded. Scientific training and final evaluation require their separately frozen common protocol.

The strongest additional evidence route is **the same author's released pretrained G1 velocity model and previously unopened physical G1 recordings**. This can establish execution on original-system data without training a humanoid policy. It does not reproduce the manuscript's entire 78-run campaign, and its unknown intervention times cannot establish physical recovery or detection delay. Keep it a separate episode-classification track.

## Publication identity and primary sources

Humphrey Munn, Brendan Tidd, Peter Böhm, Marcus Gallagher and David Howard, *RAPT: Model-Predictive Out-of-Distribution Detection and Failure Diagnosis for Sim-to-Real Humanoid Deployment*. [arXiv:2602.01515v2](https://arxiv.org/abs/2602.01515v2), submitted 2 February 2026, revised 21 July 2026; DOI `10.48550/arXiv.2602.01515`. **Preprint; peer-reviewed acceptance was not verified.** The [author manuscript](https://arxiv.org/html/2602.01515v2) describes nominal-only recurrent probabilistic modeling, two residual gates and an optional range gate. Its robot evaluation covers four simulated tasks and 78 physical runs. The architecture includes a forward-dynamics variant conditioned on previous observation/action. See §§3.2–3.4,4.1–4.4 and6.

[Author code](https://github.com/csiro-robotics/RAPT), pinned commit `d745668ffdb0e26877b1de4c9b2126af7bda5b03`, identifies itself as the paper release. The BSD-3-Clause license is saved unmodified. Code modules and paper-to-code differences are detailed in `METHOD_MAP.md`. Sixty public source files (803,560 bytes) were downloaded to the project-specific ignored `baselines/vendor/rapt_v020/`; `SOURCE_RECEIPT.json` binds every file. No installation, code edits or external LLM calls occurred.

## Why this comparator is compatible

The forward-dynamics detector consumes numerical state/action sequences, trains without anomaly labels, produces row-aligned scores, and retains recurrent state during online evaluation. Those interfaces can represent the study's four measured joint position/velocity channels plus four protected planned position/velocity channels. This is a complete detector-core transfer, unlike reusing only a calibration formula from a vision-policy method. The original G1 model and task-specific features are not reused on the two-joint simulator.

Our transfer changes task, dimensions, nominal population, split, sampling period and local batch size. Initialization and calibration populations must be common and explicit; copied headline scores are excluded. Its optional semantic diagnosis is outside our evaluated endpoint and needs no API call. An execution here cannot claim that the original G1 result was reproduced or refuted.

## Candidate limitation worth testing

The released forward predictor conditions on observed state at the preceding step; its recurrent state continues updating after anomalous observations. Therefore a sustained motion deviation can become predictable while remaining inconsistent with the authorized trajectory. This is a **testable limitation hypothesis**, not an observed RAPT failure. Detection asks whether a transition is plausible; intent/recovery asks whether it agrees with a protected command reference. The simulator must keep both methods' information access aligned, distinguish legitimate state corrections from model learning, and retain ordinary filters/ARX/control rules as explanatory controls. A protected reference or kinematic filter alone does not establish originality.

## Alternatives screened

| Method | Current decision and reason |
|---|---|
| [FAIL-Detect, RSS2025](https://www.roboticsproceedings.org/rss21/p073.html), DOI10.15607/RSS.2025.XXI.073 | Verified peer-reviewed and code-backed. Its learned policy-observation/action uncertainty and conformal calibration are relevant prior art; moving only its scalar band to our residuals is not a complete detector reproduction. RAPT offers a closer direct numerical-state interface. |
| [Schubert et al., ITSC2024 manuscript](https://arxiv.org/html/2404.16500v2) | Predicts maneuver-level maximum lateral deviation from operating/known degradation conditions; mismatched target/information access. Useful uncertainty-margin prior art, not an online cyberattack comparator. |
| [Xu et al., RCIM2024](https://doi.org/10.1016/j.rcim.2024.102777) | Current/collision residuals require unavailable current/torque information; full implementation still unverified. |
| [Kaisar et al., IEEE OJCOMS2026](https://doi.org/10.1109/OJCOMS.2026.3739185) | Sensor-corruption isolation and active vehicle control/handover differ from passive command-path monitoring. Full matched runnable author system remains unverified. |
| MVT-Flow | Existing separate admission remains an offline full-trajectory fault-detection track. It does not supply causal online recovery evidence. |

## Verified pilot result

Command and bounds are in `PILOT_PLAN.md`; complete receipts are in `local/baseline_admission_v0.20/pilot_001/`. Nine previously admitted synthetic normal Q1/K13 episodes yielded 9,900 observations and 189 separate 50-step windows. The unmodified architecture has 2,613,832 trainable parameters. One epoch at batch32 took 0.803s including training setup (the internal epoch log reports0.4s); total worker/supervisor wall2.447s, CPU1.665s, sampled peak506,871,808 bytes, output13,260 bytes before the final supervisor receipt. Five explicitly synthetic compatibility checks passed; all60 upstream source hashes matched. No fitted checkpoint was retained/admitted, no convergence or detection result was measured. The rough100-epoch planning estimate is80.3s per plant/seed before validation and calibration, not an execution guarantee.

## Source-access and metadata boundaries

`PUBLIC_RELEASE_CONTRACT.md` records licenses, exact revisions, expected hashes, dimensions, archive sizes, conflicts and proposed access gates. Documents/source metadata were fetched publicly; a failed sandbox DNS attempt preceded an approved public-source fetch. No credentials, contact, raw-data redistribution or publishing occurred. Notes are AI-assisted source audit, not a human-read attestation.
