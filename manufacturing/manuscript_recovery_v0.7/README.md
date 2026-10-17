# Recovery manuscript and reproducibility package

**Title:** *When Should a Digital-Twin Alarm Clear? Recovery Evidence under Motion-Model Mismatch.*

This is the complete LaTeX author-review draft for the measured v0.7 virtual experiment, with methods, related work, threat model, all-method results, matched-entry ablations, costs, limitations, conclusion and pending declarations. The primary improvement criterion failed. The draft is not an admitted original-algorithm contribution or a submission-ready paper. The user's intended original-contribution destination remains active.

- [Main LaTeX source](main.tex), `sections/`, and [references](references.tex).
- [Claim ledger](CLAIM_LEDGER.md), source/reference manifest and review record.
- `generated/` tables and all-outcome CSV, `figures/` PDF/PNG data plots, all derived from saved results.
- [Experiment protocol and complete results](../research_cycles/recovery_v0.7/README.md).
- Final PDF: `manufacturing/output/pdf/alarm-recovery-model-mismatch.pdf`.

From repository root, rebuild assets with the existing `manufacturing/.venv-plots-v03/bin/python manufacturing/research_cycles/recovery_v0.7/present.py`, then compile with `manufacturing/.venv-reproduction-v02/bin/python manufacturing/manuscript_recovery_v0.7/build_pdf.py`. The latter uses the existing verified Tectonic 0.17.0 binary and a separate local cache; compilation is offline by default. Every attempt, including failures, remains under `manufacturing/local/recovery_v0.7/pdf_build/`. `--allow-resource-downloads` permits missing compiler resource/font retrieval only; it does not upload the manuscript. No system package installation is needed.

Author order supplied: Muhammad Usman, Haiqa Mushtaq. Muhammad Usman's affiliation is recorded from the prior supplied context as COMSATS University Islamabad, Sahiwal Campus, Pakistan. Haiqa's affiliation, actual individual roles, funding/conflicts and both authors' review remain unconfirmed. The user asked the assistant to draft these declarations; that does not establish unknown personal facts. No public release/submission occurred. **ISA Transactions is a conditional scope-fit target**, not an acceptance promise; source limitations and the unmet original-contribution gate are recorded in the source/admission report. Hardware is not a prerequisite for the next virtual research cycle.

This directory is separate from `manufacturing/manuscript/` and its preserved earlier CASPER PDF. Neither historical source nor frozen score artifacts were edited to fit this account.
