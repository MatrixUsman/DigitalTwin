# SWaT/WADI request preparation

Prepared and submitted **16 October 2026, Asia/Karachi**. **Submission confirmed on the website; provider approval and dataset receipt remain pending.** During the subsequent paper-study task, the user supplied the university email and explicitly agreed to submission with the stated terms/privacy consent. The completed request selected SWaT and WADI. The provider displayed a successful contact confirmation; no request identifier or download link was displayed. The private record is in ignored `water/local/itrust_request_2026-10-16.json`.

## Submitted application

Official form: https://www.sutd.edu.sg/itrust/request-for-datasets/

| Field | Prepared value / status |
|---|---|
| Full name | Muhammad Usman, from the confirmed project-owner mapping |
| University | COMSATS University Islamabad, Sahiwal Campus, from the user's reported affiliation |
| University email | Supplied by the user and entered; exact address retained only in the ignored private record |
| Dataset choices | SWaT and WADI checked; other datasets unchecked |
| Organisation category | Academia/research |
| Region | Pakistan |
| Date | Form default **17/10/2026**, preserved; preparation and post-submission clock checks were already 17 October in Singapore and still 16 October in Pakistan |
| Terms acceptance | Checked after explicit user confirmation |
| Personal-information consent | Checked after explicit user confirmation |
| Submission | **Website confirmation observed**; no request identifier displayed |

The browser state was read back after correcting transient field-entry problems. Name, university, email, both dataset selections, category and Pakistan were visibly verified. After user agreement, both consent boxes were checked and Submit was clicked once. Native Safari displayed the success message. A post-submission clock check returned **2026-10-16 16:15:51 UTC**; this is the observation bound, not an exact server timestamp. No CAPTCHA challenge was solved. The user's own earlier-submission status remains unknown; no prior receipt was available. The current submission was explicitly authorized.

## Accepted terms and consent

The [provider terms](https://www.sutd.edu.sg/itrust/itrust-labs/datasets/terms-of-usage/) require publishing the requester/organisation names and request date, giving iTrust credit, notifying iTrust of resulting publications, and not sharing the datasets privately or publicly. Additional users must request access separately. The [form](https://www.sutd.edu.sg/itrust/request-for-datasets/) also requires consent for SUTD to process the supplied personal information and share it with authorised third parties for processing/communication purposes. The form states processing may take up to three working days; this is not a guaranteed approval date.

The computer-use tool required confirmation at the time of accepting binding terms. The user provided that confirmation before the agreement boxes were selected and the form submitted. No further submission is currently needed.

## Files needed after approval

Target the process/historian recordings and release documentation, not the large network packet captures:

- SWaT December 2015 corrected normal v1 and attack v0, matching CAROTS's expected filenames where the provider supplies them.
- WADI A2-style normal and attack recordings (`WADI_14days_new.csv`, `WADI_attackdataLABLE.csv`), subject to provider documentation and label verification.
- Dataset README/schema and attack-interval documentation for each exact release.

The request form selects dataset families, not exact releases. A family request does not establish receipt of these files. Provider WADI A2 date labels remain inconsistent across pages; preserve supplied names and documentation. IT-DT and the ensemble's exact release equivalence remains unresolved.

## Current local and alternative-source checks

The pre-submission inventory found **zero files** in `water/datasets/raw/`, `water/datasets/processed/` and `water/local/`. The private submission record has since been added to `local/`; no benchmark file was acquired. Available workspace filesystem capacity was **254,771,200,000 bytes free (237.27 GiB)** at that inspection. Free capacity can change; no extraction requirement was inferred from it.

The earlier public mirrors remain leads: [THUML SWaT](https://huggingface.co/datasets/thuml/Time-Series-Library) and [Kaggle WADI](https://www.kaggle.com/datasets/giovannimonco/wadi-data). A bounded fresh search found no provider endorsement establishing permission for those mirrors. Their uploader license labels are not verified iTrust permission, and original-release equivalence remains unproven. No inference is made that a particular mirror lacks a separate agreement; none was located here.

The official [SWaT characteristics page](https://www.sutd.edu.sg/itrust/itrust-labs/datasets/dataset-characteristics/swat/) links an [anomaly-detection implementation](https://github.com/ngoclesydney/Anomaly-Detection-with-Swat-Dataset). The inspected repository root/README contains notebooks and implementation material, with no original dataset download route. The provider's implementation link does not solve dataset access.

## Resume this task

1. Wait for the provider's response to the supplied university inbox; no mailbox access or background monitoring was authorized or performed. Do not submit a duplicate merely because approval is pending.
2. Record any approval, conditions and authorized download information privately. Website submission does not verify email delivery or approval.
3. On receipt of an authorized download route, save unchanged originals under ignored `water/datasets/raw/`, hash each file, and complete the [receipt checklist](DATASET_ACCESS_CHECKLIST.md). Do not treat public mirror metadata as measured local data.

No datasets were downloaded, no approval was verified, and no model or experiment ran during application preparation/submission.
