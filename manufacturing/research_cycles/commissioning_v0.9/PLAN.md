# Normal-only reference adequacy study v0.9

## Material Passport

Manufacturing / Haiqa Mushtaq; operator Codex; 17 October 2026. User authorized clean commissioning model improvement and normal-only recovery feasibility before another attack experiment. This is a bounded model-development study, not a new attack campaign or journal-admission decision. AFTER remains a proposed title, not author-finalized.

## Question and known limitation

Can a stable linear reference with a longer command/state history, or an ordinary command-only finite impulse response (FIR) model, predict normal operation accurately enough that the fixed recovery inequality can be satisfied? v0.8 is exposed and motivates this experiment. Its uncertainty-addition candidate failed; simply increasing history or fitting an FIR model is established system identification, not a new contribution.

## Inputs and partitioning

Use the existing synthetic v0.8 commissioning files: three training episodes per Q1/Q2/Q3 plant. Read only `measurements`, `available` approved commands and `valid` from explicitly enumerated normal files. Arrays are copied read-only into a restricted observation type. Actual plant parameters, true states, intervention labels, prior attack scores/outcomes and counterfactual trajectories do not enter fitting, prediction or model selection.

For each plant, the archived nineteen normal calibration episodes are reassigned *for this new development study*: indices 0–8 select models; 9–13 estimate an empirical discrepancy allowance; 14–18 provide an archived normal check. They are not retrospectively new holdouts. Old files/protocols/results remain unchanged. No cross-episode windows. Means/scales and coefficients use the three training episodes only, eligible targets t>=100.

Every reference gets the same 100-observation initial prefix. A free ARX reference uses its final p observations from that prefix, then only its own predictions and past approved commands. This differs from v0.8's four-observation initialization. The ordinary ARX(4) control receives the same 100-observation prefix, isolating history/model changes from initialization changes. Its fitted coefficients/scales must equal the original fit. FIR sees only past commands after initialization; one-step ARX is a diagnostic following control, not a free reference.

## Finite model bank and selection

Independently implemented ridge least squares: ARX orders 4,8,16,32 and FIR orders 16,32,64; ridge values 1e-7,1e-5,1e-3, unpenalized intercept, mean normal equations. All use training-only state standardization and raw commands. ARX homogeneous recursion must have spectral radius <1; failed fits/unstable models remain in records. No tuning after the bank is declared.

Choose per plant using only nine development episodes: minimize the worst episode's 99th percentile of the maximum absolute standardized channel error, then mean standardized RMSE, parameter count and model identifier. Record every candidate. Save best ARX, best FIR and overall selected reference. These can coincide; duplicate roles are not independent evidence. Keep original ARX(4), ridge1e-7; its one-step following version; and approved-command-as-state as controls. No neural training or physically fitted parameter claims.

## Allowance and clearance feasibility

For each role, b is the maximum scalar discrepancy on the five designated allowance episodes. Test `error+b <= delta`, delta=0.1, over a dwell of ten observations. This empirical allowance includes measurement noise and model discrepancy; it is not a deterministic physical or conformal guarantee.

Necessary algebraic admission: b<delta (strict inequality reserves nonzero observed-discrepancy space). Report the fraction of eligible normal points satisfying the inequality. At indices 100,320,620,900, force a diagnostic active latch and find the first ten consecutive eligible samples satisfying the condition within 250 samples (five seconds). No entry threshold is calibrated, and no attack/return event is fabricated: these are **normal clearance opportunities**, not attack recovery success or detection metrics. Entry-score priority is deliberately absent in this diagnostic; a future complete alarm machine still needs evaluation.

## Fresh normal check

After selection and allowance artifacts are sealed, generate three previously unused tasks H/I/J, three existing plants, three seeds (17,42,2026), and only normal/authorized-offset/authorized-slow conditions: 81 new synthetic episodes. Same simulator, prior-known plants and dependent seeds; not independent real-world acquisitions or cross-plant transfer. Configuration declares all trajectories before generation. Strip simulator truth before model calls. No attacks are generated. Save every role's predictions/errors and diagnose state channels, transients, normal error maxima/quantiles and opportunities.

A selected reference is admitted only to a later alarm-design step if, on every plant, b<0.1, at least 95% of fresh eligible normal samples satisfy the inequality and at least 95% of diagnostic starts clear within five seconds. Report error improvements versus matched ARX(4) even if admission fails. Passing does not establish attack sensitivity, trustworthy physical recovery, novelty or publication readiness. Failure does not authorize another search on the new check.

## Budget, provenance and verification

Single CPU worker, 600 s wall, 300 s CPU, 1 GiB monitored RSS, 200 MiB outputs; existing isolated environment, single BLAS thread. Preserve failures; no automatic scientific retries. Record exact commands, source/config/input hashes, dependency/platform/revision/dirty state, splits, every fitted model and selection/allowance seal before fresh generation. Synthetic tests cover fitting isolation, order/causality, restricted inputs, recurrence, failures and exact clearance arithmetic. Post-run verification independently recalculates metrics/selection/admission and replays saved predictions. Preserve earlier frozen packages and PDF/title artifacts; mutable handoffs get archival snapshots before edits. No data publication, paid compute, author contact or invented author approval.
