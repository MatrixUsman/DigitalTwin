# Stage 3: dataset identity, labels, time and byte provenance

Audit date: **16 October 2026**. **Source-level identification is prepared; file-level identification is blocked by non-receipt.** The user reconfirmed: “Still waiting; no files received.” The official application has website submission confirmation, but provider approval and a permitted download route remain pending. No external folder was supplied and no whole-computer search was performed.

The [observed local inventory](../datasets/manifests/LOCAL_INVENTORY_2026-10-16.json) found **zero raw files, zero processed files and zero matches for the six CAROTS expected CSV/XLSX names** in the scoped project search. Eight previously acquired provider/host metadata files still match their saved hashes. Those eight objects are documentation, not SWaT/WADI recordings.

## 1. What a release identity must contain

Keep five different identifiers separate: the physical collection period, provider catalogue alias, revision/update date, original archive/member name, and SHA-256 of the received bytes. A CSV conversion of an XLSX file is a derivative with a different hash, even if its values agree. A matching filename, paper sample count or host checksum alone does not establish provider authorization or the exact copy used by an author.

The [candidate register](../datasets/manifests/RELEASE_CANDIDATES.json) records the following **targets, not frozen releases**:

| Dataset | Candidate for our comparison | Evidence and outstanding identity |
|---|---|---|
| SWaT | December 2015 process data, normal v1 and attack v0 | Provider A2 update dated 24 September 2018 removes the first 30 minutes of normal v0 to obtain v1. CAROTS expects `SWaT_Dataset_Normal_v1` and `SWaT_Dataset_Attack_v0` in CSV or XLSX form. Actual archives, sheets, row ranges and hashes are unknown. |
| WADI | Revised A2 process data | Provider names `WADI_14days_new.csv` and `WADI_attackdataLABLE.csv`, with corrected attack dates. CAROTS expects directory `WADI.A2_19 Nov 2019`. The provider catalogue says 19 November 2019, while its revision notice says 19 December 2019. Preserve both source-specific dates until delivered documentation resolves their meaning. |

Sources and precise locators: [provider evidence](literature/DATASET_PROVIDER_EVIDENCE_2026-10-16.md); [SWaT provider](https://www.sutd.edu.sg/itrust/itrust-labs/datasets/dataset-characteristics/swat/); [WADI provider](https://www.sutd.edu.sg/itrust/itrust-labs/datasets/dataset-characteristics/wadi/); [catalogue](https://www.sutd.edu.sg/itrust/itrust-labs/datasets/summary-of-available-datasets/).

These older collections are compatible with our recent-paper selection rule. The 2023 paired clean collection and later catalogue entries are different datasets; recency alone is not a reason to substitute them. No additional 30-minute removal should be applied to an authenticated SWaT normal v1 merely because an older preprocessing script removed startup from v0. If further startup exclusion is scientifically justified, record it as a separate derived-data decision.

## 2. Labels: provenance before conversion

| Dataset | Source-backed expectation | Proposed internal representation | Required receipt check |
|---|---|---|---|
| SWaT | Provider describes normal/abnormal labels. Pinned CAROTS treats the exact string `Attack` in the last column as positive. | Attack `1`, normal `0`, with an explicit allowed vocabulary established from the received release | Exact column, case, whitespace, missing/unknown values and correspondence with the attack register. Do not treat every string other than `Attack` as normal. |
| WADI A2 | Provider explicitly assigns attack `-1`, no attack `1`. CAROTS expects column `Attack LABLE (1:No Attack, -1:Attack)`. | Raw `-1 → 1`; raw `+1 → 0`; retain the raw label separately | Confirm the exact header and numeric representation. Missing or other values fail validation rather than being silently mapped to normal. |

The internal mapping is an intended evaluator convention, not a conversion already performed. “Normal recording” is provider context, not sufficient reason to ignore an unexpected label in a file. Verify or document absent normal-file labels before constructing an all-zero vector.

Obtain and hash the release-specific attack register as well as the telemetry. Preserve original event IDs, start/end strings, target metadata, overlaps and simultaneous attacks. Reconcile row labels against intervals under an explicit endpoint convention; do not silently overwrite either source. A disagreement should produce an integrity issue with counts and examples retained privately. Provider counts of launched attacks are not automatically the final event denominator. Attacks, labelled intervals and detected events are different units.

CAROTS's median downsampling of labels followed by an any-positive window label changes the evaluation unit. Our proposed interval/OR-labelled common grid is a declared protocol change, not the original provider label sequence. Preserve original labels and timestamps so both transformations remain traceable.

## 3. Timestamps: fields that remain unknown

**No exact timestamp format, timezone, first/last instant, row count or measured cadence can be filled from our current files: there are no recordings to inspect.** The inspected public provider pages do not specify a complete legacy timestamp schema. A paper's sampling claim is recorded as a claim, not as a measurement of our copy. The ensemble's stated 10 Hz needs reconciliation with the actual release; sample counts must not be silently reinterpreted as seconds.

The pinned CAROTS water loader discards time metadata rather than parsing it. Therefore its source does not resolve date order, AM/PM, timezone or gaps. Do not assume UTC, Singapore time or Pakistan time from plant location, researcher location or the application date. Do not let a parser silently choose day-first/month-first interpretation for ambiguous strings.

After authorized receipt, inspect structural metadata in this order:

1. Identify CSV encoding/delimiter/decimal notation or XLSX sheet/header layout, including metadata preambles. Preserve physical row numbers and original timestamp fields. Check both split date/time fields and spreadsheet date types where applicable.
2. Establish explicit date/time formats from the release documentation and unambiguous observations. Record precision, AM/PM and any offset evidence. When timezone is absent, retain a timezone-unknown local timeline; do not invent an offset or compare separate recordings as synchronized UTC.
3. Check parsing coverage, nulls, duplicates and backward steps without sorting, dropping or repairing rows. Distinguish exact duplicate rows from conflicting observations sharing a timestamp. Every exception requires a declared policy.
4. Measure consecutive time differences within each recording. Record first/last timestamp, count, nominal cadence if documented, observed delta distribution and gaps. Do not derive row count as days × 86,400 or assume row adjacency means temporal adjacency.
5. Preserve breaks caused by WADI's removed unstable intervals and any later exclusions. No window or resampling operation may bridge an unobserved interval or independent episode. Record coverage lost to gaps and warm-up.
6. Compare attack-register time representation with telemetry time representation before interval alignment. Decide endpoint inclusion from documentation where available; otherwise declare the assumption before scoring and report conflicts. Never shift labels until model scores look better.

This is necessary annotation/structure auditing, not permission to inspect attack traces or detector failures for model design. Keep inspection commands and scope in the work log; do not plot or tune on held-out attacks during this stage.

## 4. Hashes: what is measured and what is advertised

| Hash category | Current status | Meaning |
|---|---|---|
| Our received raw-file SHA-256 | **Unavailable; zero raw files** | Will identify the exact bytes we possess. No empty-file digest or placeholder string substitutes for it. |
| Provider-issued original checksums | **Not located in inspected public provider pages** | Could authenticate a supplied release if its origin is trustworthy. Private delivery may contain a manifest; this audit cannot rule that out. |
| Mirror-reported SHA-256 | Two SWaT LFS digests preserved from the pinned host listing; WADI listing supplies no verified digest | Remote claims, not our measurements or official provider signatures. See the candidate register and [acquisition record](../baselines/DATASET_ACQUISITION_STATUS.md). |
| Local metadata-file SHA-256 | Eight metadata objects rehashed successfully | Identifies the saved web/listing evidence only. It says nothing about possession of the advertised datasets. |

Do not confuse a Git blob ID, Xet hash, archive hash and extracted-file SHA-256. Each identifies a different object or representation. Matching our later digest to a mirror would show byte agreement with that advertised object, not prove permission or the copy used in a baseline experiment. Differing hashes can arise from conversion or container metadata; investigate with preserved originals rather than declaring scientific inequivalence automatically.

On receipt, stream SHA-256 over each unchanged original archive, extracted data file, readme/schema and attack table. Record bytes, original names, acquisition time/source and archive-member relationships. Verify archive containers before safe extraction; reject HTML error bodies, incomplete downloads and Git LFS pointer stubs. Do not execute archive contents. Keep conversions/caches outside raw storage and record input hashes, commands, tool versions and output hashes. Rehash originals after inspection to confirm no writes.

## 5. Can we establish the same files as all three baselines?

**Not yet.** The [baseline compatibility audit](literature/DATASET_BASELINE_COMPATIBILITY_2026-10-16.md) separates paper claims, pinned loader behavior and our future common protocol. CAROTS gives the strongest filename/revision clues but no verified author raw-file checksum. IT-DT and the ensemble do not provide a reconstructable exact-file manifest in the available materials. Their reported variable counts and calendar-day splits do not establish byte identity.

Further CAROTS receipt risks include SWaT labels extracted before the first feature row is removed, WADI row deletion before time columns are discarded, and independent removal of all-empty columns. The meaning of the first parsed row and actual effects remain unknown without the original files. Check named feature alignment, metadata exclusion, missing values and chronological continuity; never blindly copy positional slices or code-configured feature counts.

The eventual comparison can use one clearly identified common release pair under a declared common protocol. It must not claim exact reproduction of every author's original data preparation unless that evidence becomes available.

## 6. Required record and completion gate

The [manifest guide](../datasets/manifests/README.md) defines the necessary receipt fields. Current observed inventory, candidate metadata and future measured manifests are separate records. Candidate fields remain null when unmeasured; no proposed parser, split or feature list is marked verified.

Stage 3 can close only when both datasets have authorized original recordings and accompanying documentation, local hashes and byte sizes, verified schemas and label mapping, explicit timestamp/timezone handling, reconciled attack intervals, and a documented common-release decision. If an essential field remains unresolved, record its consequence and keep the affected comparison on hold.

**Completed now:** local inventory, provider/version evidence, label expectations, baseline compatibility audit, remote-versus-local hash separation and the receipt specification. **Still blocked:** actual file hashes, timestamp profiles, row/feature/label counts, interval reconciliation and release freeze. No dataset was downloaded, parsed, modified or uploaded, and no model ran.
