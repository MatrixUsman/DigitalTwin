# SWaT/WADI provider evidence for release identification

Audit date: **2026-10-16**. Scope: bounded read-only verification of public **iTrust/SUTD** pages, using the installed research skill's source-verification guidance. This is provider metadata evidence, not inspection of benchmark files. Access approval, exact received bytes and measured dataset hashes remain unverified. The existing [application record](../DATASET_REQUEST_PREPARATION.md) records submission only; this audit did not submit another request or contact anyone.

## Inspected primary sources

All sources below were opened on the audit date. Locators refer to visible headings and paragraphs; line numbers are the browser's retrieved-text locations on that date, not permanent website anchors.

| ID | Source | Exact locator and use |
|---|---|---|
| P1 | [SWaT characteristics](https://www.sutd.edu.sg/itrust/itrust-labs/datasets/dataset-characteristics/swat/) | Characteristics of dataset, lines 111–115; Updates on dataset, 122–146; December 2023 section, 147–160. Release history and normal-startup revision. |
| P2 | [WADI characteristics](https://www.sutd.edu.sg/itrust/itrust-labs/datasets/dataset-characteristics/wadi/) | Characteristics of dataset, 112–116; update dated 19 Dec 19, 121–122; December 2023 section, 123–136. Revision filenames and explicit numeric label polarity. |
| P3 | [Release summary](https://www.sutd.edu.sg/itrust/itrust-labs/datasets/summary-of-available-datasets/) | Summary of available datasets table, 106–115. Public collection aliases/dates; conflicts with characteristics pages retained below. |
| P4 | [Dataset overview](https://www.sutd.edu.sg/itrust/itrust-labs/datasets/) | Introductory availability, processing and support paragraphs, 102–106. Access route and support limitations. |
| P5 | [Terms](https://www.sutd.edu.sg/itrust/itrust-labs/datasets/terms-of-usage/) | Terms of usage of datasets, 104–109. Sharing restrictions and attribution obligations. |
| P6 | [Request form](https://www.sutd.edu.sg/itrust/request-for-datasets/) | Email field, 71; dataset choices, 81–85; agreement and consent, 104–107. Request mechanism, not an approval record. |

## Public release catalogue, not a file manifest

The table below transcribes the identifiers/date labels in **P3**. Dates are catalogue labels; they do not establish every file's recording start or publication date.

| System | Public identifiers/date labels |
|---|---|
| SWaT | A1 and A2 — Dec 2015; A3 — Jun 2017; A4 and A5 — Jul 2019; A6 — Dec 2019; A7 — Jun 2020; A8 — Jun 2021; A9 — Nov 2022; A10 — Dec 2023; A11 — Feb 2026; A12 — Mar 2026 |
| WADI | A1 — 9 Oct 2017; A2 — 19 Nov 2019; A3 — Dec 2023 |

**The recent-paper window does not select recent data.** A paper published in 2026 can use a 2015 collection. Do not automatically replace a baseline's legacy inputs with the latest provider catalogue entry.

## Release-specific facts supported by the provider

**SWaT, P1:** the December 2015 collection describes 51 sensor/actuator variables, seven normal days and four attack days, with 41 launched attacks. The **24 September 2018** A2 update distinguishes normal versions 0 and 1: v1 removes the initial **30 minutes** of v0, associated with tank drainage and LIT101 behavior. Therefore collection date, update date and normal-file version are separate fields. These statements do not establish actual row counts, exact file extensions or a contiguous time range in our future copy.

**WADI, P2:** A1 describes 123 sensor/actuator variables, 14 normal days, two attack days and 15 launched attacks. The **19 December 2019** A2 update identifies `WADI_14days_new.csv` after removing unstable-operation readings and `WADI_attackdataLABLE.csv` with **attack = −1, no attack = +1**. It also announces an attack table with corrected dates. Retain this original polarity in provenance even if a later evaluator explicitly converts it to attack = 1. Removed intervals may introduce gaps; that consequence must be measured from received timestamps.

For both systems, a count of launched attacks is not yet our evaluator's event denominator. The received attack register, point labels and treatment of simultaneous/overlapping attacks must determine that denominator under a declared rule.

## Conflicts that must remain visible

| Finding | Evidence | Consequence |
|---|---|---|
| WADI A2 has different public date labels | P3: **19 Nov 2019**; P2 update heading: **19 Dec 19** | Record both. They could represent distinct catalogue/update dates; the inspected pages do not explain the difference. Do not silently select one as the collection date. |
| December 2023 SWaT numbering disagrees | P3: **A10 Dec 2023**, with A9 assigned to Nov 2022. P1/P2 December 2023 section: **SWaT.A9_18 Dec 2023** | Preserve the source-specific aliases; do not use the A-number alone as a unique release key. |
| Later shared collection is a different setting | P1/P2: **18–22 Dec 2023**, 105 normal hours, including 100 CrossOver hours; no attacks | It cannot silently substitute for the legacy attack benchmark or establish evidence for our attack-detection comparison. |

The two December 2023 characteristics paragraphs repeat the same provider description; they are not independent corroboration. The catalogue conflicts do not prove that any dataset or paper is fabricated.

## Labels, timestamps and hashes: unresolved file-level fields

| Field | What this audit establishes | What still requires authorized original files/documentation |
|---|---|---|
| SWaT label representation | P1 describes normal/abnormal labelling | Literal column name, string vocabulary, whitespace/typos, missing labels and per-row counts. Do not infer their exact spelling from the prose. |
| WADI label representation | P2 gives A2 numeric polarity and the labelled filename | Exact header and values in the received file; missing/invalid entries; reconciliation to the corrected attack table. A1 must not inherit A2's schema without inspection. |
| Attack register | P1 refers to an attack PDF; P2 refers to a corrected attack table | Exact documents, hashes, event IDs, targets, start/end times, inclusion convention and differences from row labels. The inspected public characteristics pages expose no downloadable event table link. |
| Timestamp storage | No legacy file timestamp schema established by P1–P6 | Whether date/time are split fields, format and locale, precision, AM/PM handling, timezone/offset and provenance. Plant location alone does not prove the logging timezone. |
| Cadence | No legacy SWaT/WADI cadence specification located in P1–P6 | Nominal cadence from release documentation and actual consecutive differences, duplicate times, reversals, missing intervals and episode boundaries. A paper's stated 1 Hz is not a measurement of our files. |
| First/last timestamp | Catalogue dates above are verified as labels | Exact first/last original row and timestamp per file, including startup revisions. Do not derive these from duration multiplied by sample rate. |
| File identity | P2 gives two concrete revised filenames | Original archive/member names, extension, size, export dialect, sheet/header layout and transformations. Matching names alone do not establish identical bytes. |
| Provider checksum | **No provider checksum located on P1–P6** | Any checksum delivered with the authorized download and its trust origin. This bounded result does not assert that no private release manifest exists. |
| Our checksum | No local benchmark bytes inspected by this audit | SHA-256 of each received archive, original data file, readme/schema and attack register; preserve original bytes before parsing. A hash computed locally is a fingerprint, not independent provider authentication. |

## Access and documentation limitations

P4 routes researchers through a free request process and states that clarification support ceased from **1 July 2022**. P5 prohibits recipients from sharing data privately or publicly and requires credit/publication notification. P6 requires a university/organisation email. A published listing, pending application, or university account does not itself establish dataset permission.

No private download location, delivered release readme, original attack table or checksum manifest was available to this audit. The SWaT page mentions a `readme.docx` for its **July 2019** revision; that is not evidence that the same documentation describes December 2015. Provider-linked software examples are not provider signatures for any files they might reference.

## Search coverage and outcomes

In addition to directly opening P1–P6, ordinary web searches used these exact queries:

```text
site.sutd.edu.sg SWaT dataset "second" timestamp
site.sutd.edu.sg WADI dataset "timestamp"
site.sutd.edu.sg "WADI" "2017" "10"
site.sutd.edu.sg "SWaT" "Attack List"
site.sutd.edu.sg "WADI" "SHA256"
site.sutd.edu.sg "SWaT" "checksum"
site.sutd.edu.sg "SWaT" "Timestamp" "2015"
site.sutd.edu.sg "WADI" "time zone"
```

Results included unrelated uses of “SWAT”, third-party papers/repositories, and official descriptions of other collections. None supplied additional verified provider checksums, a legacy timezone specification or an authenticated legacy attack-register download. Search snippets and third-party reproductions were not promoted into official release evidence. Search absence is not proof of nonexistence.

## Completion boundary

**Completed:** official catalogue/revision verification, explicit label-polarity evidence, source conflicts and file-level unknowns. **Not completed:** receipt, exact-release freeze, timestamp/label inspection, file hashes or event reconciliation. The next release-identification pass requires authorized original bytes plus accompanying documentation. Preserve the evidence gaps rather than filling them from plausible filenames or another researcher's processed copy.
