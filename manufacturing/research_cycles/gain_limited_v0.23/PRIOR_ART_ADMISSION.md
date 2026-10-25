# Prior-art admission: gain-limited monitoring

2026-10-24; manufacturing; project owner Haiqa Mushtaq; operator Codex source-review agent. New bounded source audit, preserving sealed v0.22. This applies the academic-research-suite bibliography/source-verification guidance under project rules: exact primary versions, no medical hierarchy, no bibliographic-verification APIs, no inference of originality from search absence. No experiment, clone, installation, contact or dataset access occurred in this source task. Root owns experimental status and session logs.

## Admission decision

**Do not admit a theorem-led original-method claim.** Identity minus a contraction has an established lower Lipschitz bound. Normal-only Lipschitz-constrained reconstruction for anomaly detection, including lower anomaly-score guarantees, also has direct prior art. The stronger claim that our method first prevents learned reconstruction from erasing anomaly evidence is therefore rejected.

The proposed complete monitor remains a **task-specific design hypothesis**: a command-only reference, causal measurement correction with a hard sequence-gain budget, bounded trusted-context score scale, and an explicit sustained-deviation alarm condition. No inspected source establishes that this exact complete contract is identical; that does not establish originality. A combination of existing components, a change of application or use of the term digital twin is insufficient. Independent measured value and a substantive method-level distinction are necessary. Even a successful normal pilot would establish feasibility only.

The two recent Automatica papers' final equations remain inaccessible. This is an unresolved comparison dependency, not an open scientific gap. The rejection of broad mathematical novelty above does **not** depend on those missing texts.

## Exact primary-source findings

### 1. Behrmann et al., ICML 2019 — direct mathematical overlap

Jens Behrmann, Will Grathwohl, Ricky T. Q. Chen, David Duvenaud and Joern-Henrik Jacobsen. *Invertible Residual Networks*. ICML, PMLR97:573–582, 9–15 June2019. [Proceedings record](https://proceedings.mlr.press/v97/behrmann19a.html), [final paper](https://proceedings.mlr.press/v97/behrmann19a/behrmann19a.pdf), [supplement](https://proceedings.mlr.press/v97/behrmann19a/behrmann19a-supp.pdf). Peer-reviewed proceedings; foundational background outside the recent baseline window.

Inspected §2, Theorem1, Lemma2 and its supplementary proof. For `F=I+g`, `Lip(g)=L<1`, Lemma2 bounds the inverse Lipschitz constant by `1/(1−L)`. The proof explicitly derives `||F(x)−F(y)||≥(1−L)||x−y||` by reverse triangle. Substituting `g=−A` is the candidate residual construction. Extending a contractive causal adapter to finite sequence space and adding a nominal-error allowance are our deductions, not new results claimed by this paper. Sequence-level separation alone is not an arbitrary pointwise-in-time guarantee; the candidate's plateau/history assumptions still matter.

Paper-linked [author repository](https://github.com/jhjacobsen/invertible-resnet), master [`630e886bcd50cc21dee0769d1a5b35100d3ff569`](https://github.com/jhjacobsen/invertible-resnet/tree/630e886bcd50cc21dee0769d1a5b35100d3ff569), 25August2020; pinned LICENSE inspected: MIT. No implementation execution/correspondence audit.

### 2. Kim et al., AISTATS 2020 — reconstruction sensitivity is already the objective

Young-geun Kim, Yongchan Kwon, Hyunwoong Chang and Myunghee Cho Paik. *Lipschitz Continuous Autoencoders in Application to Anomaly Detection*. AISTATS, PMLR108:2507–2517, 26–28August2020. [Record](https://proceedings.mlr.press/v108/kim20c.html), [final paper](https://proceedings.mlr.press/v108/kim20c/kim20c.pdf). Peer-reviewed proceedings; foundational background.

Inspected Definition2, Theorems1–2, Proposition4, Lemma3, §3.4 and Algorithm1. Theorem1 uses `K<1` and a sufficiently small normal reconstruction discrepancy to lower-bound contaminated-distribution discrepancy. Theorem2 provides pointwise score ordering under explicit distribution-distance margins. Lemma3 connects ordinary Lipschitz maps to Wasserstein contraction. Thus the overlap is stronger than an average-only abstract summary suggests. Algorithm1 uses a sampled pairwise penalty; that is distinct from our proposed hard induced-norm certificate, but replacing a soft penalty with a familiar hard norm constraint does not alone establish originality.

Paper-linked [code](https://github.com/kyg0910/Lipschitz-Continuous-Autoencoders-in-Application-to-Anomaly-Detection), master `8138e68e173d7df5ef8590686917ceec42309d4d`, 27March2024. Repository license metadata is null; actual reuse permission unresolved. No source execution audit.

### 3. Diop and Plantevit, DiffInt v1 — explicit pointwise lower score bound

Lamine Diop and Marc Plantevit. *Differentiable Interval Bottlenecks for Interpretable Anomaly Detection in Numerical Data*, [arXiv:2609.03878v1](https://arxiv.org/html/2609.03878v1), 3September2026. [Current primary metadata](https://arxiv.org/abs/2609.03878) reports acceptance at ICDM2026; final proceedings identity not inspected. This updates v0.22's preprint-only status without changing its sealed record.

Inspected §§III–IV, Theorem1, discussion and AppendixA proof. Under the theorem's strong coordinate-support violation and a Lipschitz-certified decoder, reconstruction MAE is lower-bounded by distance to a collapsed reconstruction minus bounded decoder slack. The proof uses reverse triangle. Partial violations receive a suppression result, not that score guarantee; the default accuracy configuration is not the certified decoder. This directly blocks broad novelty claims for deterministic pointwise reconstruction-error lower bounds. It is not a temporal command-reference monitor; differing support assumptions must be compared rather than declared inferior.

Paper-linked [code](https://github.com/DiffInt/diffint), main `ee6284e3ddb562077b903eff95ae1a2eff8bc3ba`, 28September2026. Pinned LICENSE inspected: MIT (GitHub metadata classified it Other/NOASSERTION). No execution or theorem-to-code audit.

### 4. Ghanipoor et al., Automatica 2026 — final comparison unresolved

*Provably robust data-driven sensor fault diagnosis using incrementally stable recurrent equilibrium networks*. Authors in final order: Farhad Ghanipoor, Giancarlo Ferrari Trecate, Nathan van de Wouw, Carlos Murguia. Automatica191, September2026, 113096; [DOI10.1016/j.automatica.2026.113096](https://doi.org/10.1016/j.automatica.2026.113096). [Publisher preview](https://www.sciencedirect.com/science/article/pii/S0005109826002803) verifies a published open-access Brief Paper. [EPFL discovery](https://graphsearch.epfl.ch/en/publication/64388483-db0e-4b11-ae49-ebd0ba9075b2) corroborates identity. Direct publisher open again returned403; [Infoscience](https://infoscience.epfl.ch/entities/publication/64388483-db0e-4b11-ae49-ebd0ba9075b2) was inaccessible. Browser fallback reported no available browser. No final proof obtained.

The inspected [2025v1](https://arxiv.org/html/2504.19688v1) remains a different exact citation: its title and author order differ. Its Eq6/Remark1/conclusion limitation, documented in [v0.22](../novelty_v0.22/FINAL_VERSION_CHECK.md), is not attributed to the journal article. The preprint-linked [faultDiag code](https://github.com/DecodEPFL/faultDiag) still reports last push25March2025 and license null; prior pinned main is `6a4e0a81051fe2d8025b58cb3b21db6f6efc57f9`. Final correspondence, source license and implementation admission remain unresolved.

### 5. Wang et al., Automatica 2026 — robust sensitivity comparator

Zi-Yun Wang, Si-Yu Li, Yuan Gao, Yan Wang, Ju H. Park and Zhen-Hua Wang. *Fault detection based on zonotopic H_/L∞ observer for Lipschitz nonlinear systems*. Automatica192, October2026, 113159; [publisher record](https://www.sciencedirect.com/science/article/pii/S0005109826003432), DOI10.1016/j.automatica.2026.113159. Published Brief Paper; precise first-online date and default-window eligibility unresolved.

Publisher abstract/section preview describes bounded disturbances, Lipschitz nonlinear dynamics, sensitivity/robustness observer design via LMIs and fault-free residual sets; flexible-arm simulation. Direct full opening returned403. Exact H-minus norm/frequency assumptions, full theorem, code and license remain unverified. It is strong close prior art for sensitivity plus noise allowances; no claim that it proves or lacks the candidate's particular pointwise floor is admitted.

### 6. Gualandi and Papadopoulos v2 — protect the reset/covariance comparison

Gabriele Gualandi and Alessandro V. Papadopoulos. *From Passive Monitoring to Active Defence: Resilient Control of Manipulators Under Cyberattacks*, [arXiv:2603.13003v2](https://arxiv.org/html/2603.13003v2), 26May2026; first posted13March. [Metadata](https://arxiv.org/abs/2603.13003) reports ICRA2026 acceptance; final-proceedings byte identity unverified.

Rechecked Assumption2, §III-A, Eq14–24. A measurement-free actuation predictor is initialized/reset from the KF. Residual covariance is propagated through a joint recursion, then used for a Mahalanobis discrepancy. Their attack model permits sensor injection only. The candidate differs in protected authorized-command conditioning and a hard incremental correction budget, but must compare fairly with the actual joint-covariance/reset mechanism, not merely a bare KF.

**Correction to the earlier bounded search:** §V/reference16 identifies author MATLAB archive *ManipulatorsGainScaling*, v1.0.1, [DOI10.5281/zenodo.18813337](https://doi.org/10.5281/zenodo.18813337), also visible in the [institutional manuscript](https://www.es.mdu.se/pdf_publications/7340.pdf). DOI/Zenodo retrieval failed here. Archive files, license and executable correspondence remain unverified; no claim of absent code.

## What would support or reject a contribution

1. Treat contraction/reverse-triangle and scale composition as credited supporting analysis. Do not present a known inequality or renamed hard constraint as a new theorem.
2. Specify the genuinely additional algorithmic problem: which nominal mismatch needs nonlinear memory; how trusted commands/phase, resets, initialization and scale are jointly controlled; and why ordinary gain-matched filters fail there. The no-fit RAPT diagnostic does not by itself answer this causal question.
3. Compare direct reference, constrained AR/FIR, amplitude-matched saturated linear correction and the same unconstrained network with identical information and normal-data selection. Include the actual protected reset/covariance method after a disclosed compatibility decision, plus an admitted recent robust-neural comparator. The source papers' incompatible task labels or sensors cannot be converted into an unfair numerical ranking.
4. Separate hard sequence-gain correctness from pointwise plateau conditions and empirical calibration. A development maximum is not a bound on every future nominal residual. A bounded scale does not give a population false-alarm guarantee. Resetting measurement-derived state can violate a certificate unless included in its information path.
5. Reject the nonlinear original-method route if ordinary controls match its useful normal-error/sensitivity tradeoff, the certified operating region is vacuous, the only advantage is privileged commands or scale choices, or a close method already supplies the same complete contract. A failed pilot does not justify changing the success criterion afterward.
6. If a specific new mechanism survives, confirm it on prospectively frozen independent evidence and report delay, benign alarms and return failures. Synthetic outcomes do not establish real-world cyber-recovery generalization. Measured application benefit may support a substantive applied contribution, but does not automatically repair a missing methodological distinction.

## Journal fit: conditional only

No venue is selected or submission recommended. [IFAC's official publication descriptions](https://ifac-control.org/publications/) place Control Engineering Practice at the application of control to automation; [IEEE IES's official publications page](https://www.ieee-ies.org/pubs?highlight=WyJpIiwiaSdkIiwiaW4iXQ%3D%3D) places industrial robotics, AI and process security within IEEE Transactions on Industrial Informatics. These are topical fit examples, not a readiness or acceptance assessment. Our judgment: an applied industrial-monitoring paper needs convincing industrial evidence and meaningful method value; a theory-led control paper needs more than the established bound. Current evidence does not warrant a particular journal recommendation, prestige claim or acceptance promise.

## Search, access and provenance

Date:24October2026. Primary publisher, proceedings, arXiv, author/institution and author-code routes only for technical conclusions. Exact searches included: `"113096" "Ghanipoor" pdf`; `"Ghanipoor" "113096" filetype:pdf`; exact final title with `site:epfl.ch`, `site:tue.nl`, `site:nathanvandewouw.nl`, or `pdf`; `"Ghanipoor" "recurrent" site:infoscience.epfl.ch`; exact zonotopic title plus `pdf`; `"Invertible Residual Networks" "1" "Lipschitz" lower bound`; `"ManipulatorsGainScaling" Gualandi`; `"ManipulatorsGainScaling" github`; `"18813337" Gualandi`; `"Lipschitz" "anomaly detection" "contractive" "lower bound"`; `"Lipschitz" "anomaly" "pointwise" contractive reconstruction`; official journal-scope queries.

Kim/DiffInt were followed from their exact primary records. Search-only synthetic synthesis sites, unrelated results and request-only records were not technical evidence. GitHub connector reads covered repo metadata, pinned commits and identified LICENSE files; no cloning/execution. Browser fallback was unavailable. No access workaround or contact was attempted. Source descriptions are compact and do not reproduce extended prose. Bibliography additions are in `REFERENCES_NEW.bib` and `REFERENCES_NEW.tex`; they cite inspected versions rather than silently substituting later final titles.
