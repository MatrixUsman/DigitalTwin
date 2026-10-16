# CASPER annotation and score-index study

Audited 16 October 2026, manufacturing / Haiqa Mushtaq. This is a static study of the pinned author notebook and previously measured file structure. **No model, preprocessing pipeline or upstream notebook was executed. No new ground-truth labels or training data were produced.**

Sources: [corrected CASPER paper](https://ngcharithperera.gitlab.io/publications/pdfs/Kayan2024a.pdf), especially Tables 10–11, §6.4, Figure 11 and Algorithm 1; [author notebook at the frozen revision](https://github.com/hkayann/1D-CNN-Anomaly-Detection-via-CASPER/blob/bff03c91d155bf3134f6d801d3a4f4af7ea78adb/notebooks/casper.ipynb); our [received-file identity](CASPER_DATASET_IDENTITY.md). Notebook cells below are **zero-based**. Paper claims, source-code operations and our bookkeeping deductions are kept separate.

## How an IMU row acquires a label

The raw motion-sensor file has neither time nor anomaly-label columns. The notebook does not obtain a label by joining a sensor timestamp to the controller clock. Instead, it observes the GyroX channel and manually identifies eight changed-motion intervals. It explains that the sensors start/stop at different times and have variable acquisition rates. Its claimed annotation error below 1% has not been independently verified.

| Stage | Source | Meaning and index consequence |
|---|---|---|
| Read nine IMU channels | Cell 2 | Skip six startup CSV records; 1,751,682 numeric rows in our received file. Numeric row `r=0` is CSV record 7. |
| Remove initial idle observations | Cell 8 | Drop 897 numeric rows, resetting the index. This is an upstream selected cut, not a fresh estimate made here. |
| Trailing median | Cell 21 | Width 20, then drop initial incomplete windows. A filtered row `f` uses numeric input rows `[f+897, f+917)` and ends at numeric row `f+916`. |
| Assign motion-deviation intervals | Cell 23 | Eight half-open slices are marked positive in **filtered coordinates**, not raw CSV coordinates. |
| Form upstream normal and mixed segments | Cell 25 | The first 1,072,450 filtered rows are assigned to the normal segment; the rest include both labelled motion changes and intervening zero-labelled periods. |

For example, a filtered endpoint index `f` maps to original CSV record `f+923` (one-based). The complete support of that filtered value spans twenty numeric inputs. **This map does not prove that every supporting input is anomalous**, and it is not an estimate of physical onset time. Copying the filtered index directly onto raw IMU rows would shift the label association by 916 numeric rows.

The final interval's executable slice ends at 1,716,450, whereas notebook prose says 1,716,456. Preserve the six-sample disagreement; do not silently choose whichever improves a score. The audit records the executable slice as source-code behavior, not as independently correct truth.

Detailed upstream slices and their coordinate translations are retained in ignored `manufacturing/local/casper_annotation_study/annotation_lineage.json`. They are evidence for later annotation review, **not an approved benchmark annotation manifest**. A chronological match between eight controller flags and eight IMU intervals does not establish clock synchronization.

## Counts and what they can establish

The following are arithmetic deductions from the received row count and static source operations. They are not generated prediction arrays or performance results.

| Quantity | Count |
|---|---:|
| Numeric IMU rows after the six startup records | 1,751,682 |
| After dropping 897 | 1,750,785 |
| After the width-20 median's 19 incomplete positions | 1,750,766 |
| Upstream normal prefix | 1,072,450 |
| Upstream mixed segment | 678,316 |
| Positive filtered rows in the eight manual slices | 342,740 |
| Residual positions after a 755-step predictor | 677,561 |
| Eligible 755-residual aggregation positions | 676,807 |
| Positive / negative targets under upstream majority-window labels | 341,608 / 335,199 |

Figure 11(c)'s published confusion matrix sums to 676,807 observations, with the same positive and negative target totals. This is a useful consistency check between our received length, the available notebook's annotation procedure and the paper's denominator. **It does not reproduce predictions, accuracy, selected thresholds, checkpoint provenance or exact byte identity of the authors' experiment.**

Table 11 instead lists 1,750,932 IMU points—750 fewer than our received numeric rows. That difference is not explained by dropping 897 idle observations or 19 median warmup positions. Record it as an unresolved table/release/count-definition discrepancy. The figure-denominator agreement is evidence worth retaining, not permission to ignore the conflicting table.

## What one CNN score actually uses

The notebook's CNN predicts the next nine-channel measurement from 755 filtered observations (cells 81–89). It computes the residual after observing the target and then sums 755 consecutive residuals (cell 92). Each aggregated score therefore depends on:

- **1,510 filtered observations**, including the predicted targets;
- **1,529 original numeric observations**, including the median's preceding 19 inputs.

For score index `j` in a mixed segment beginning at filtered row `S`, the filtered support is `[S+j, S+j+1510)`. The endpoint is `S+j+1509`. The original numeric support is `[S+j+897, S+j+2426)`. These ranges describe the inspected upstream operations; a proposed implementation that resets filtering at each partition has its own warmup and index convention.

The score is only available at its final observation. Plotting it at the start of its support would make detection look artificially early. No conversion to seconds is justified for this untimestamped IMU sequence merely by dividing by a nominal frequency.

Cell 95 labels a score positive if **at least 378 of its 755 target positions** are positive. This is majority-window evaluation, which differs from judging the endpoint or detecting any part of an event. It can change apparent onset and duration. Our [proposed comparison protocol](COMPARISON_PROTOCOL.md) uses a separately specified common target rule; it will not silently mix these conventions.

## Consequences for a future reproduction

The upstream median is applied before the later partitioning. Adjacent partitions can therefore share 19 underlying input observations even though their filtered-row indices differ. The trailing filter does not look into the future, but that alone does not establish isolated partitions. The proposed protocol resets preprocessing within each partition and reports its warmup/exclusions.

Manual labels based on a channel observed by the detector introduce annotation dependence. Keep the upstream annotation unchanged for a disclosed reproduction analysis; any revised annotation requires independent evidence, a frozen version and a documented rationale before inspecting detector results. Do not derive supposedly independent truth from the detector's own scores.

The notebook then chooses a threshold using evaluated attack labels (cell 97). This remains ineligible for our operational comparison. Changes to calibration, partitioning or target convention mean **modified-protocol author-code execution**, or an independent implementation if we write the method ourselves; neither can be presented as an unchanged reproduction of published F1.

## Reproducible audit

From the repository root:

```sh
python3 manufacturing/scripts/audit_casper_annotation_lineage.py
```

The standard-library [audit utility](../scripts/audit_casper_annotation_lineage.py) checks the notebook hash against the original receipt, extracts the literal eight intervals using Python's syntax tree without executing them, derives row counts/class totals, and checks complete support by a **synthetic index-set union**. It reads no sensor values and fits no model. Its local JSON records source/profile/receipt/script hashes, interpreter/platform, command and timestamps. Re-running replaces only that audit output; preserve a copy before changing source assumptions.

Unresolved: independent IMU event onset/clock alignment; annotation uncertainty; exact published input bytes and checkpoint; the table's row-count difference; final feature, split and target manifests. See [the protocol](COMPARISON_PROTOCOL.md) for admission gates.
