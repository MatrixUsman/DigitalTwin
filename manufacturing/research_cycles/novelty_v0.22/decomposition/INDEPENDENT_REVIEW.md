# Independent saved-array review

24 October 2026. Manufacturing. A separately executing AI reviewer read the protocol, freeze/worker interfaces, original v0.19 schedule and completed saved outputs. The reviewer did **not** import `core.py`, the worker's report helpers or the primary verifier, and did not run learned-model inference. This is independent arithmetic/code-path review within a shared-context AI team, not independent human peer review.

## Outcome

**Passed: 7,364 assertions/checks and 518,400 byte-identical original score values.** These are software/arithmetic checks, not independent experiments. All 36 episodes, 129,600 rows, 126,000 eligible rows and 36 sealed decomposition arrays were accounted for. The original frozen input bindings also match. Detailed identities and access inventory are in `REVIEWER_VERIFICATION.json`.

Executed once from `/Users/matrixusman/CUI/DigitalTwin/manufacturing`:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv-analysis-v022/bin/python research_cycles/novelty_v0.22/decomposition/reviewer_verify.py
```

The verifier uses only Python's standard library and NumPy. It reads each new decomposition array and only the `loss` member of each old RAPT score archive. Other frozen files are hashed, not interpreted as signals. It opens no truth arrays or new raw observations, and performs no fitting or checkpoint inference. Its own source and the exact checked summary/run documents are hashed in the receipt.

## Checks performed

- Reconstructed the complete two-task × three-seed × six-condition population from the declared design, including benign episodes.
- Checked every floating array's type, shape, finite values, nonnegativity where applicable, row-zero padding, defined-score mask, warmup eligibility and released log-variance clamp.
- Compared every saved per-channel loss byte with the corresponding original v0.21 loss array.
- Recomputed standardized error from saved squared error and log variance; floating-point differences fit the declared tolerance. Recomputed every episode/region/channel mean using a separate `math.fsum` reduction.
- Reconstructed all first/last quarters from the frozen schedule, using `floor(duration/4)`: 132 rows for each persistent L19 quarter and 117 for each persistent S19 quarter. Benign quarters span 1,475 rows and do not provide matched motion-phase controls for intervention quarters.
- Recomputed all positive-support logarithmic summaries, excluded-zero counts, first/last differences and their identities. No eligible score value was zero. The largest checked elementwise log-identity error was **1.262×10⁻⁷**, below the protocol's 2×10⁻⁵ limit.
- Checked completion, single-attempt status, resource limits and active RSS sampling. Reported run cost was 4.824 s wall, 3.890 CPU seconds, 410,664,960 sampled peak RSS bytes and 7,933,849 output bytes, within all four caps. Sampled RSS is not a continuous instantaneous bound.

## What the decomposition supports

The persistent-offset cases show **different channel behavior**, not universal error collapse. Across all three seeds, L19 channels 1 and 2 decline in mean log score while channels 0 and 3 increase. In S19, channels 0 and 3 decline in every seed; channel 2 increases, and channel 1 is mixed.

The following values are medians of the three descriptive first-to-last-quarter changes. Each channel-wise episode identity was independently checked before this aggregation. Medians of separate components need not add exactly.

| Task / channel | Δ mean log squared error | Δ mean log variance | Δ mean log score |
|---|---:|---:|---:|
| L19 / 0 | +2.0073 | −0.0735 | +2.0814 |
| L19 / 1 | −1.1096 | −0.0567 | −1.0529 |
| L19 / 2 | −3.2040 | +0.1428 | −3.3468 |
| L19 / 3 | +1.0364 | −0.1174 | +1.1537 |
| S19 / 0 | −3.4928 | −0.2896 | −3.2028 |
| S19 / 1 | +0.0331 | +0.0095 | +0.0242 |
| S19 / 2 | −0.0493 | −0.1795 | +0.1308 |
| S19 / 3 | −2.2084 | +0.6446 | −2.8533 |

For the consistently declining channels, reduced squared prediction error supplies the larger-magnitude log change. Increased predicted variance additionally depresses L19/channel 2 and S19/channel 3 scores. In L19/channel 1 and S19/channel 0, variance instead decreases and partially offsets the numerator-driven decline. Thus a blanket **variance-inflation-only** explanation is contradicted by these saved arrays. Nor do all channels show decreasing prediction error.

These statements explain arithmetic changes in the **released per-channel standardized squared errors**. They do not isolate the causal effects of recurrence, training, task shift, calibration or adaptation. The original pooled risk is a maximum over different channel/gate ratios. Its change cannot be obtained by summing these log-component summaries. Likewise, mean log score describes a geometric-average change, not the change in arithmetic mean score.

The earlier physical-outside/inactive finding remains a previously verified v0.21 result; this review did not reopen its truth arrays. It therefore does not independently recertify physical deviation or attribute it to a particular channel. In particular, the three S19 persistent cases were missed from the start in the earlier replay; they must not all be described as alarms that later cleared.

## Limits and disposition

No arithmetic, population or original-score-parity defect was found. Saved means and variances were not independently reconstructed from neural weights, so this review relies on the primary no-fit inference path for their provenance. Exact old-score parity and reconstructed score algebra are strong consistency checks, not proof of every model intermediate. No full-paper reproduction, causal diagnosis, new detection benefit, generalization or novelty follows.

The results justify keeping both mean-response preservation and uncertainty normalization in the next mechanism audit. They do not authorize choosing a favorable channel, changing thresholds or fitting the proposed candidate to these exposed outcomes. Proceed only with the separately stated normal-only software/feasibility gates.
