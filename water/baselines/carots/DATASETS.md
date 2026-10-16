# CAROTS dataset requirements

Status **16 October 2026:** no SWaT/WADI files or provider access approval have been received. Expected filenames below come from the pinned [author loader](vendor/author_code/datasets/build.py); they do not establish release identity or access.

| Dataset | Expected upstream files beneath its data directory | Still to establish |
|---|---|---|
| SWaT | `SWaT_Dataset_Normal_v1.csv` / `.xlsx`; `SWaT_Dataset_Attack_v0.csv` / `.xlsx` | Official release mapping, original bytes/hashes, header and first-row handling, startup exclusions, timestamps, feature set and annotation semantics. |
| WADI | `WADI.A2_19 Nov 2019/WADI_14days_new.csv`; `WADI.A2_19 Nov 2019/WADI_attackdataLABLE.csv` | A2 release/version equivalence, original bytes/hashes, annotations, unstable-period handling, schema and missing-data treatment. Preserve the source spelling `LABLE`. |

The paper evaluates both datasets, but provides no provider file checksums. Its dataset names and sequence counts alone cannot prove a mirror or another method used identical data. The [acquisition status](../DATASET_ACQUISITION_STATUS.md) records the present official/mirror findings; the [access checklist](../../docs/DATASET_ACCESS_CHECKLIST.md) governs receipt. Official access starts at the [iTrust request form](https://www.sutd.edu.sg/itrust/request-for-datasets/). No request was submitted by this acquisition task.

## Loading differences to resolve before execution

- The loader reserves the later normal portion as validation and fits scaling on training. `TRAIN_RATIO >= 1` instead reuses test data as validation; forbid that branch.
- The SWaT code extracts test labels before removing a feature row. Confirm actual timestamp/row alignment against received files; the suspected defect has not been runtime-tested.
- WADI independently drops wholly missing columns and rows containing missing values in normal/test data, drops three metadata columns and maps `-1` labels to attacks. Check the ordered feature sets explicitly. Deleted rows may create temporal gaps; windows must not silently bridge them.
- SWaT/WADI scripts request factor-five downsampling. The utility applies block medians to labels as well as features and drops incomplete trailing blocks. This can remove short attacks; later any-anomaly window labels do not restore them.
- Upstream conversion and caching write into the data directory. Preserve original data unchanged under `water/datasets/raw/`; redirect derived data to `water/datasets/processed/` in the eventual adapter.
- Cached filenames encode downsampling rate but omit original hashes, split ratio and preprocessing revision. Existing caches can therefore survive changes to those inputs. Bind future processed caches to an explicit provenance manifest.

Do not place separate raw copies in each baseline folder. Each baseline should reference the same approved water-project manifest and frozen files. We cannot yet assert exact release compatibility with IT-DT or the ensemble paper. Document method-specific preprocessing explicitly and use common score/label coverage rules for our eventual comparison.

The downloaded author repository includes dataset-loading code, not SWaT/WADI observations. Its retained `Graph.npy` files are author-derived causal graph artifacts, not raw dataset substitutes.

See [findings C-03–C-05](VERIFICATION_REPORT.md) for exact code locations and limits of this static audit. None of these observations substitutes for testing the authorized original release.
