# SWaT/WADI request preparation

Prepared **16 October 2026, Asia/Karachi**. **Not submitted; no approval or dataset receipt.** The user explicitly requested Stage 1 access work and downloads. The official form is open in a dedicated Safari tab, with the known fields filled. The missing email and any prior submission must be resolved before proceeding.

## Concrete application draft

Official form: https://www.sutd.edu.sg/itrust/request-for-datasets/

| Field | Prepared value / status |
|---|---|
| Full name | Muhammad Usman, from the confirmed project-owner mapping |
| University | COMSATS University Islamabad, Sahiwal Campus, from the user's reported affiliation |
| University email | **Missing; not inferred**. Requested privately in the conversation; never store the address in tracked files |
| Dataset choices | SWaT and WADI checked; other datasets unchecked |
| Organisation category | Academia/research |
| Region | Pakistan |
| Date | Form default **17/10/2026**, preserved; the clock check was 2026-10-16 16:09:15 UTC, already 17 October in Singapore and still 16 October in Pakistan. Recheck at submission |
| Terms acceptance | Unchecked; action-time confirmation pending |
| Personal-information consent | Unchecked; confirmation pending |
| Submission | **Not performed**; no receipt or request identifier exists |

The browser state was read back after correcting transient field-entry problems. Name, university, both dataset selections, category and Pakistan were visibly verified. No email was entered, neither consent box was selected, and Submit was not clicked. An in-app browser was unavailable; native Safari worked. This preparation does not assert that the user's own earlier request was or was not submitted.

## What submission would agree to

The [provider terms](https://www.sutd.edu.sg/itrust/itrust-labs/datasets/terms-of-usage/) require publishing the requester/organisation names and request date, giving iTrust credit, notifying iTrust of resulting publications, and not sharing the datasets privately or publicly. Additional users must request access separately. The [form](https://www.sutd.edu.sg/itrust/request-for-datasets/) also requires consent for SUTD to process the supplied personal information and share it with authorised third parties for processing/communication purposes. The form states processing may take up to three working days; this is not a guaranteed approval date.

The computer-use tool requires confirmation at the time of accepting binding terms. The current request authorizes application preparation and the access task, but that tool requirement still applies before checking agreement and submitting. A CAPTCHA, if presented, has its own action-time confirmation requirement; none was solved.

## Files needed after approval

Target the process/historian recordings and release documentation, not the large network packet captures:

- SWaT December 2015 corrected normal v1 and attack v0, matching CAROTS's expected filenames where the provider supplies them.
- WADI A2-style normal and attack recordings (`WADI_14days_new.csv`, `WADI_attackdataLABLE.csv`), subject to provider documentation and label verification.
- Dataset README/schema and attack-interval documentation for each exact release.

The request form selects dataset families, not exact releases. A family request does not establish receipt of these files. Provider WADI A2 date labels remain inconsistent across pages; preserve supplied names and documentation. IT-DT and the ensemble's exact release equivalence remains unresolved.

## Current local and alternative-source checks

Read-only inventory found **zero files** in `water/datasets/raw/`, `water/datasets/processed/` and `water/local/`. Available workspace filesystem capacity was **254,771,200,000 bytes free (237.27 GiB)** at inspection. Free capacity can change; no extraction requirement was inferred from it.

The earlier public mirrors remain leads: [THUML SWaT](https://huggingface.co/datasets/thuml/Time-Series-Library) and [Kaggle WADI](https://www.kaggle.com/datasets/giovannimonco/wadi-data). A bounded fresh search found no provider endorsement establishing permission for those mirrors. Their uploader license labels are not verified iTrust permission, and original-release equivalence remains unproven. No inference is made that a particular mirror lacks a separate agreement; none was located here.

The official [SWaT characteristics page](https://www.sutd.edu.sg/itrust/itrust-labs/datasets/dataset-characteristics/swat/) links an [anomaly-detection implementation](https://github.com/ngoclesydney/Anomaly-Detection-with-Swat-Dataset). The inspected repository root/README contains notebooks and implementation material, with no original dataset download route. The provider's implementation link does not solve dataset access.

## Resume this task

1. Obtain the user's exact active university email and whether a prior request already exists. Avoid duplicating an existing pending request without a reason.
2. Reinspect the live form, correct any user-supplied identity details, and verify all visible fields before submission.
3. Obtain the required action-time agreement/consent confirmation with the concrete request and provider conditions visible. If the researcher prefers, they can complete these controls themselves.
4. Submit only after those prerequisites are met; record the actual confirmation, time and any request reference in ignored `water/local/`. Submission is not approval.
5. On receipt of an authorized download route, save unchanged originals under ignored `water/datasets/raw/`, hash each file, and complete the [receipt checklist](DATASET_ACCESS_CHECKLIST.md). Do not treat public mirror metadata as measured local data.

No datasets were downloaded, no approval was verified, and no model or experiment ran in this preparation task.
