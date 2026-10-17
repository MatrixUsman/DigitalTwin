# Noise-aware return control: measured normal feasibility

17 October 2026. The standard control is implemented and numerically verified. **The full normal-feasibility gate failed: 20 of 36 constructed traces passed.** This narrows the next mechanism problem to handling temporal correlation and current-state variation under useful, justified uncertainty bounds.

## Material passport

Manufacturing; owner Haiqa Mushtaq; operator Codex. Synthetic residual-level diagnostic, not robot dynamics, CASPER observations, cyberattack evaluation or a new detector. Sources/configuration were frozen before generation. All six declared controls and all seeds are retained. [Plan and derivation](PLAN.md), [prior art](PRIOR_ART.md), [verification](VERIFICATION.json).

## What ran

Four noise settings × three within-tolerance deviation profiles × seeds 17,42,2026 = 36 traces and 216 method/trace outcomes. Each method has the same 1,000 eligible endpoints per trace. Registered valid controls use windows 1,41,201 and their simultaneous upper-bound envelope. Two additional controls deliberately ignore temporal correlation; they are invalid under the correlated conditions even if their normal certificate rates appear favorable.

The run completed once, with no experiment failure or retry. Actual wall time was **0.565s**, worker CPU **0.459s**, sampled peak RSS **39.81 MiB**, worker lifetime peak RSS **39.91 MiB**, and final run artifacts **11.07 MiB**. Limits were 120s wall/60s CPU/512MiB sampled memory/20MiB output. Aggregate six-control scoring CPU was 0.020899s; this is neither per-model latency nor a CASPER speed comparison.

Twenty synthetic software tests passed. A first test attempt had one overly strict floating-point assertion; its 2.78e-17 discrepancy, source, log and corrected tolerance are preserved in [test development](TEST_DEVELOPMENT.md). The independent post-run verifier passed **2,665 checks**, recomputing window means through convolution and Gaussian variance through covariance sums, checking all 216 records and preserving 301+64+71+24 prior-package file bindings.

## Normal-feasibility result

The registered criterion required at least 95% of endpoints certified on **every** trace. The following ranges cover the three declared seeds, with passes counted separately. A group mean above 95% cannot hide a failed seed.

| Noise setting | Within-tolerance profile | Multiwindow certificate fraction, seed range | Traces meeting 95% |
|---|---|---:|---:|
| iid_low | settled | 100.0%–100.0% | 3/3 |
| iid_low | slow_within_tolerance | 100.0%–100.0% | 3/3 |
| iid_low | faster_within_tolerance | 100.0%–100.0% | 3/3 |
| iid_high | settled | 100.0%–100.0% | 3/3 |
| iid_high | slow_within_tolerance | 100.0%–100.0% | 3/3 |
| iid_high | faster_within_tolerance | 17.2%–25.6% | 0/3 |
| ar08_low | settled | 100.0%–100.0% | 3/3 |
| ar08_low | slow_within_tolerance | 85.8%–100.0% | 2/3 |
| ar08_low | faster_within_tolerance | 0.0%–0.0% | 0/3 |
| ar095_high | settled | 0.0%–0.0% | 0/3 |
| ar095_high | slow_within_tolerance | 0.0%–0.0% | 0/3 |
| ar095_high | faster_within_tolerance | 0.0%–0.0% | 0/3 |

Noise settings are dimensionless: iid_low sigma=.03/rho=0; iid_high .06/0; ar08_low .03/.8; ar095_high .06/.95, with the frozen channel multipliers. See [configuration](config.json) for every value. “Certified” means the upper bounds fit within tolerance; absence of a certificate is uncertainty, not a declared cyberalarm. These are not false-alarm rates or measured recovery delays.

The instantaneous error-controlled comparator certified no common endpoints. Averaging enabled ordinary return certification in several settings. For low independent noise with the faster within-tolerance profile, the 41-sample window certified every endpoint while the 201-sample window certified none: the latter's current-state drift penalty consumed its noise benefit. For correlated low noise and the slower profile, the envelope certified 100%, 85.8%, 100% for seeds17/42/2026, so that condition fails the all-traces rule despite its 95.27% mean.

With rho=.95 and sigma=.06, the valid controls certified no endpoints, even for the settled profile. Ignoring correlation with the 201-sample control would certify 91.53% on average in that settled condition, but removes the stated uncertainty justification. This is an assumption audit, not evidence that it produced unsafe decisions here. Every generated deviation was small and within tolerance.

No bound-coverage violations were observed in these normal traces. That limited check does not validate a 5% unsafe-clearing probability, performance near the tolerance boundary or behavior during attacks. The mathematical coverage statement remains conditional on the known Gaussian covariance, bias and drift contract.

## Interpretation and next scientific decision

The useful result is a tested comparator and an explicit trade-off: longer windows suppress noise but make a bound on **current** motion less informative. The conservative registered window set fails under strong correlation; this does not show that every window set or every observer must fail. No windows, bounds, percentiles or thresholds were changed after inspecting these outcomes.

The next bounded step is to establish which uncertainty quantities can be estimated from clean, command-matched commissioning observations, using the existing virtual plant and reserved normal conditions. Repeated command trajectories can support a measurement-noise model only if the repeatability assumptions are checked; reference bias must be separated from that noise, and current-deviation bounds need a defensible dynamics assumption. Keep simulator truth evaluator-only. Compare any replacement with this control and an ordinary state observer under the same information access. An operationally unavailable bound must be reported as an unavailable assumption, rather than filled with true simulator values.

This is standard Gaussian variance/concentration accounting. A new method-level distinction from close interval/recovery prior art remains unresolved, including the inaccessible Kaisar full method. Neither CASPER superiority nor journal readiness follows. The existing trained references and consolidated manuscript are preserved; no attack experiment, neural training, PDF rewrite or publication occurred.

## Dependence and wording correction

The pre-run plan's phrase “new independent trace” was too strong. Traces sharing a seed use paired innovations across conditions; there are three independent noise draws, not 36 independent acquisitions. The construction was fixed in the frozen generator before execution. Each trace's bound is a separate marginal error contract; independence between traces is not needed for that statement. There is no joint 95% guarantee across the study. Repeated alarm resets within a trace remain prohibited. No inferential test or standard error treats endpoints, windows, seeds or these traces as independent robot experiments.

All signal values, noise/bias/drift bounds and reference decompositions are synthetic and oracle-informed. No physical simulation or commissioning estimator is validated by this study. The 0.1 tolerance is a diagnostic choice, not a robot safety requirement. These outcomes are now exposed development evidence.

## Traceability

- [Frozen configuration and identities](FREEZE.json); all outcomes in [JSON](ALL_OUTCOMES.json) and [CSV](all_outcomes.csv).
- Local arrays, receipts, provenance, access record and supervisor log: `manufacturing/local/return_bound_v0.12/runs/diagnostic_001/`.
- Successful commands: `freeze.py --test-attempt test_002`, `run.py`, `verify.py`, then post-run `report.py`, all through `manufacturing/.venv-reproduction-v02/bin/python` from the workspace root.
- Freeze SHA256 `b22b229e5d919882302296e3f1de1e8ba3460c66a69c8de70d254148a24d146c`; saved summary SHA256 `33b6352f5a33f96359121898b8ef5394f84ebec9e7257dcd7d0414433b88ba51`.
