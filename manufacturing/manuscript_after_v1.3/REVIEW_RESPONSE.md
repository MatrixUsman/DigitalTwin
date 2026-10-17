# Response to the supplied teacher comments

This is an editorial/evidence response, not a claim of teacher approval or completed original-method publication readiness.

| Comment | Revision and evidence | Status |
|---|---|---|
| Short conclusion; move supporting detail | Main conclusion is one short paragraph. Conditional proofs, simulator details, older diagnostics, full IMU study, extra metrics and source audit are in a separate supplement. | Addressed |
| 20–25 valid references; at least 75% recent | 20 cited works; 18 cited versions dated 2024–2026. Primary-source scope, preprint status and inaccessible full text are explicit in REFERENCE_AUDIT.md. | Addressed at stated verification levels |
| Longer introduction and related work | Operational problem, reference semantics and three supported contributions in Section 1; robot monitoring, identification, forecasting, uncertainty and evaluation in Section 2. | Addressed |
| Weak points at the end of related work | The final paragraph identifies input/task incompatibility, code correspondence and missing recovery annotations. It does not invent blanket weaknesses in other papers. | Addressed |
| Main paper at most 15 pages | Main PDF has 11 pages including references; separate supplementary PDF has 12 pages. | Addressed for main article |
| Proposed model missing | Section 3 gives state, threat assumptions, ARX recurrence, RBF objective, frozen correction, residual score, return gate and state machine; Figure 1 shows information flow. | Specified, implemented and tested; efficacy criterion failed |
| Experiments/datasets/splitting absent | Section 4 separates synthetic physical simulation, nominal real IMU prediction, and newly admitted metadata-only public data. Normal train/development/calibration and fresh conditions are explicit. | Addressed |
| Baselines listed separately | Section 4.3 separates executed controls, modified CNN implementations and unexecuted literature comparators. Table 3 includes all 17 audit variants. | Addressed; faithful recent paper reproductions remain incomplete |
| Evaluation matrix/metrics | Table 1 maps five studies; Section 4.4 defines support, point/event metrics, physical return, the primary criterion and denominator limits. Supplement S3 gives remaining metrics. | Addressed |
| Optimization procedures and optimal parameters | Finite normal-only development search and tie breaks are stated; Table 2 reports selected settings. CNN optimizer, stopping and caps are explicit. | Addressed; no global optimality claim |
| Machine/deep learning or transformer approach | Actual shallow RBF correction and independent CNN study described. Recent convolution/transformer/mixing work is discussed with citations. | Addressed without inventing an unrun transformer experiment |
| Ablation/evolution study | Reference protection, linear/nonlinear correction, windows, dwell and ordinary controls compared; all negative outcomes retained. Five studies are linked development stages, not five independent acquisitions. | Addressed |
| Computational cost and discussion | Section 5.4 reports measured shared-pipeline wall/CPU/memory; Supplement S5 adds failures and limits. Section 6 discusses information access and external validity. | Addressed; no per-model latency benchmark invented |
| Find a strong baseline and extend it | Original voraus-AD plus MVT-Flow admitted as a separate offline comparator candidate, with code discrepancies documented. FactoryNet remains partially admitted. | Source verification complete; reproduction/extension not complete |
| Distinct contribution and worthwhile improvement | The candidate failed both relevant gates; ordinary protected reference accounts for its main benefit. | Scientifically unresolved; prose cannot complete this item |
| Natural prose | Rewritten around concrete decisions and measured results; no detector-evasion claim, no invented human-only authorship, factual AI assistance retained. | Editorially addressed |

## Submission decisions still required

The user selected Muhammad Usman as the sole byline, COMSATS University Islamabad, Sahiwal Campus as affiliation, no funding/conflicts, and neutral formatting. These instructions are reflected. Actual human contributions, any necessary prior-contributor agreement and final author approval have not been invented. No journal has been selected, no manuscript uploaded and no public release made.

The intended goal remains a defensible original contribution. This revision is a complete presentation of the available evidence, including failed improvement tests. It should be reviewed with the supervisor before being described as the intended original-method submission. The next scientific step is a frozen feature/split/implementation contract for the admitted voraus-AD/MVT-Flow track, followed by a bounded compatibility pilot; it is not another outcome-selected component added to the exposed simulation.
