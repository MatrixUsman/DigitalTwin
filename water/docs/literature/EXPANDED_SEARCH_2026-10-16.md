# Expanded water baseline search — 16 October 2026

This is a targeted search and static evidence audit for selecting papers to study, not an exhaustive systematic review or a reproduction. The predefined [selection criteria](../BASELINE_SELECTION_CRITERIA.md) apply. Search results are leads; the records below distinguish directly retrieved manuscripts, indexed publisher excerpts, repository observations and unresolved facts. No author was contacted. No restricted dataset was acquired or uploaded.

## Search scope and limits

Window: **2023-10-16–2026-10-16**, with preference for 2024–2026. English-language searches combined SWaT/WADI with digital twins, adaptation, contamination, drift, state estimation, physics and anomaly detection. Exact-title, identifier and author-code follow-ups checked identity and implementation availability. Preprint and published versions were treated as one work when the linkage was supported. Abstract-only hits were not promoted to full-method verification.

Sources included primary publisher/proceedings pages, arXiv author manuscripts, institutional author pages and matched GitHub repositories. Search-engine relative dates were not accepted as publication dates. No database export, complete hit count, citation-network census or PRISMA flow was produced. Consequently this report supports a bounded recommendation, not a claim to have found every eligible method or the globally best-performing model. Unavailable full text or code remains a gap, not proof of nonexistence.

Representative exact queries executed by the lead researcher:

```text
"SWaT" "WADI" "digital twin" 2025 2026
"SWaT" "WADI" "adaptive" "digital twin" detection
"SWaT" "WADI" "2024" "2025" anomaly detection code normal validation
"DPDGAD" full text github Liao
"DPDGAD" pdf Liao 2024
"SWaT" "WADI" "physics" "2025" anomaly detection code
"SWaT" "WADI" "state-space" "2024" "2025" detection
"INVARLLM" github journal conference
"A Reality Gap Taxonomy" github
"A Reality Gap Taxonomy" "doi.org"
"SWaT" "WADI" "digital twin" "2024" "2023" LATTICE ATTAIN
"System-aware contextual digital twin for ICS anomaly diagnosis"
"LATTICE" "digital twin" anomaly detection 2023 2024
"3582571" "Published" "2023"
```

Native research workers separately searched recent learned detectors, twin alternatives and CAROTS/CCM-TAD implementation details. Their findings were synthesized with the lead researcher's checks. These are AI-assisted source audits, not independent experimental replications or attestations that a researcher has read the papers.

## Additional process-model and evaluation leads

### INVARLLM — relevant invariant comparator, not an admitted twin baseline

Abshari, Shi, Fu, Sridhar and Du, *INVARLLM: LLM-assisted Physical Invariant Extraction for Cyber-Physical Systems Anomaly Detection*. [arXiv:2411.10918](https://arxiv.org/abs/2411.10918): v1 **17 November 2024**, v2 **2 June 2025**; DOI `10.48550/arXiv.2411.10918`. The [author's institutional page](https://webpages.charlotte.edu/cfu6/) identifies it as a preprint/selected work; peer-reviewed publication was not verified.

[Full v2 manuscript](https://arxiv.org/html/2411.10918v2), §§IV–V, Tables I/VI and appendix, evaluates both datasets. LLM-derived process invariants are filtered statistically, then scored by windowed regression residuals. Exact releases/files remain unresolved. §V-D normalizes residual sums using statistics across windows and describes optimal invariant-specific window sizes without a sufficiently traceable development partition. **Reader-inferred uncertainty:** the temporal availability of normalization statistics and window-selection labels needs resolution before online comparison. No matched implementation/license was located through the manuscript and exact-title/code searches. Extra system documentation and LLM generation must be accounted for in information/cost comparisons. Retain for prior-art study; do not substitute its reported precision for verified performance.

### Reality-gap taxonomy — priority question/evaluation background

Radovanovic et al., *A Reality Gap Taxonomy for Physics-Informed Anomaly Detection in Industrial Control Systems: Cross-Regime Evaluation, Operating-Point and Temporal Distribution Shifts*. *Machine Learning and Knowledge Extraction*, 8(10), 306; DOI `10.3390/make8100306`. [Publisher version notes](https://www.mdpi.com/2504-4990/8/10/306/notes) record the version-of-record upload on **30 September 2026**. Journal article; individual reviews were not inspected. Direct article retrieval returned 429; the following details are from indexed primary-publisher sections, not a complete retrieved-manuscript audit.

[Publisher article](https://www.mdpi.com/2504-4990/8/10/306), §§3.4/4.2 and availability: reports SWaT/WADI and HAI, normal-validation calibration for the water pair, and a separate retrospective recalibration experiment using verified-normal attack-period observations. Code/configurations are offered on request; exact water releases and a public implementation remain unverified. **Reader-inferred relevance:** its documented distinction between operational shifts and threshold calibration directly overlaps our motivating question. That retrospective diagnostic must not be treated as label-free adaptation or imported into our untouched-test protocol. Keep as required novelty/evaluation background, not a ready numerical comparator. Do not infer that its reported shifts establish the exact regimes present in files we have not received.

### LATTICE — relevant twin background outside the date window

Xu, Ali and Yue, *Digital Twin-based Anomaly Detection with Curriculum Learning in Cyber-physical Systems*. *ACM Transactions on Software Engineering and Methodology*, 32(5), article 113; DOI `10.1145/3582571`. [Primary ACM record](https://doi.org/10.1145/3582571) was accessible through indexed publisher text; direct DOI retrieval failed. It records online accepted manuscript **1 February 2023**, publication **22 July 2023**, September 2023 issue. [arXiv:2309.15995](https://arxiv.org/abs/2309.15995) was submitted **27 September 2023**. All precede our cutoff.

Publisher experimental text reports both SWaT and WADI and links a replication package. Full code/protocol/release audit was not performed because it fails the date gate. Keep as background for learning-based twin adaptation; do not relabel it as a recent main baseline or disregard its prior-art relevance because of age.

### DPDGAD — previous hold reconfirmed

The [publisher abstract](https://www.sciencedirect.com/science/article/pii/S1474034624001952) again confirms the title, authors, August 2024 issue, DOI `10.1016/j.aei.2024.102547` and both dataset names. Direct full-text retrieval returned 403. Exact-title/full-text/code searches did not resolve the existing implementation and protocol gaps. Method-level weaknesses beyond the available abstract are **not assessed**. Its earlier [detailed record](DPDGAD_AND_BASELINE.md) remains controlling; do not confuse it with the different 2026 paper named DP-DGAD.

## Additional twin candidates

These records came from the parallel primary-source audit. Unknown release IDs, code licenses and runtime costs remain unknown; a publisher abstract alone does not verify an executable twin.

| Candidate and publication evidence | Dataset/method evidence and decision |
|---|---|
| **SCDT**, Woo, Kim, Heo and Shin, *System-aware contextual digital twin for ICS anomaly diagnosis*. [arXiv:2604.24051v1](https://arxiv.org/abs/2604.24051), **27 April 2026**, DOI `10.48550/arXiv.2604.24051`; preprint only verified | [Full manuscript](https://arxiv.org/html/2604.24051v1), §4.1/Tables 2–3: both datasets. Actuator-context clustering and normal envelopes; §3.5 makes the LLM an arbitrator for ambiguous normal/anomaly decisions, not merely an explanation add-on. §4 uses GPT-5-mini and CUDA/cuML and describes CPU clustering cost. Exact releases, full selection provenance and matched code/license unverified. **Required context/ambiguity prior art; execution hold.** Removing the LLM would change the method; external data transmission is not authorized |
| **ISTFAD**, Li, Lu and Zhang, *Improved spatio-temporal feature fusion-based anomaly detection in industrial digital twins*. [Publisher](https://www.sciencedirect.com/science/article/pii/S1874548226000491), *International Journal of Critical Infrastructure Protection* 54, 100877, **September 2026**; DOI `10.1016/j.ijcip.2026.100877`; journal article, first-online date unverified | Indexed publisher abstract/dataset excerpt reports SWaT/WADI/GP. Full retrieval failed; exact releases, physical twin role, preprocessing, independent calibration, update admission, code/license and compute **unverified**. **Priority full-text reserve**, not a replacement justified by its title. Method weaknesses not assessed from abstract/excerpts |
| **i-SDT**, Homaei et al., *Cyber-Resilient Digital Twins: Discriminating Attacks for Safe Critical Infrastructure Control*. [arXiv:2603.18613v1](https://arxiv.org/abs/2603.18613), **19 March 2026**, DOI `10.48550/arXiv.2603.18613`; preprint only verified | [Manuscript](https://arxiv.org/html/2603.18613v1), §5.1/Tables 3–4: both. Hydraulically constrained predictor, attack discrimination and MPC. §4.3 uses simulated labeled attacks; §5.1.3 includes attack validation. **Different supervision/control task:** related work, not an unchanged normal-only comparator. Exact releases/code unverified; code promised after acceptance |
| *A Digital Twin and Lightweight Blockchain Logging Framework for Real-Time CPS Threat Detection*. [CMC publisher](https://www.techscience.com/cmc/online/detail/28190), DOI `10.32604/cmc.2026.086552`, online **7 September 2026**, accepted 24 August | [Full PDF](https://www.techscience.com/cmc/online/detail/28190/pdf), §5.6/Table 11: both datasets; Algorithm 1 trains supervised GBM/MLP and tunes validation F1. **Different information access**, not an unchanged normal-only comparison. Dataset releases/splits and matched code/license unresolved |
| *Digital-Twin-Enabled, Time-Aware Anomaly Detection for Industrial Cyber-Physical Systems*. [Wiley/IET](https://ietresearch.onlinelibrary.wiley.com/doi/10.1049/dgt2.70016), DOI `10.1049/dgt2.70016`, first published **31 December 2025** | Full publisher §4.1/Table 4 evaluates SWaT/HAI; WADI occurs elsewhere as context. **Excluded from the published-both starting set**. No claim that the algorithm cannot be extended to WADI |
| *Digital Twin-Driven Intrusion Detection for Industrial SCADA: A Cyber-Physical Case Study*. [Sensors](https://www.mdpi.com/1424-8220/25/16/4963), DOI `10.3390/s25164963`, **11 August 2025** | Publisher experiments concern a 72-hour simulated plant; WADI is future work in the conclusion. **Excluded from the shared-pair starting set**, despite keyword matches |
| *A Physics-Informed Digital Twin for Passive Anomaly Detection in Water Treatment and Distribution Systems* — [hydongmeow/dtwater repository](https://github.com/hydongmeow/dtwater) | README lead only: publication identity, manuscript, date, review and license unverified. README describes synthetic fallback when data are missing. **Not an admitted paper**; synthetic fallback would never establish SWaT/WADI access or a reproduction |

Twin search queries included:

```text
"digital twin" "SWaT" "WADI" 2024 2025 2026 anomaly detection
"digital twin" "WADI" adaptive cybersecurity
"SWaT" "WADI" "Kalman" 2024 2025 2026
"digital twin" "SWaT" "WADI" github
"Improved spatio-temporal feature fusion-based anomaly detection" code DOI
"Improved spatio-temporal feature fusion-based" pdf
"ISTFAD" github
"Cyber-Resilient Digital Twins" github code journal
"System-aware contextual digital twin" github publication
"s41598-026-53863-z" github
"Information-Theoretic Digital Twins" github journal
```

The same worker rechecked IT-DT's arXiv v1, the ensemble's publisher methods/availability, and CDT's author v2. No newly verified public implementation removed their existing holds. CDT's December 2025 first-online date remains supported by the earlier published-manuscript audit; the direct publisher fetch failed again. The ensemble publisher confirms 22 May 2026 publication and 27 July version of record. Its alarm gate, state assimilation, threshold updates and parameter updates remain distinct operations.

## Additional learned-detector candidates

These repositories were inspected on mutable branches in this pass; they were not pinned, installed or executed. Any later admission requires commit-qualified reinspection. Static code consequences below are reader inferences from the cited paths, not measured failures.

| Candidate and identity | Both-dataset evidence, protocol and disposition |
|---|---|
| **NPSR**, *Nominality Score Conditioned Time Series Anomaly Detection by Point/Sequential Reconstruction*. [NeurIPS 2023 proceedings](https://papers.neurips.cc/paper_files/paper/2023/hash/f1cf02ce09757f57c3b93c0db83181e0-Abstract-Conference.html), peer-reviewed, DOI `10.52202/075280-3348`. [Preprint](https://arxiv.org/abs/2310.15416) first submitted **24 October 2023**; exact proceedings day unverified | [Full paper](https://papers.neurips.cc/paper_files/paper/2023/file/f1cf02ce09757f57c3b93c0db83181e0-Paper-Conference.pdf), §4.1/Table 1: both. Factor-ten resampling/min–max; Equation 6 uses neighbors on both sides, requiring delay or different causal scoring. Appendix D selects hyperparameters using best F1. [Author code](https://github.com/andrewlai61616/NPSR) names SWaT Dec2015 v1/v0 and WADI2017 files; hashes/license unresolved. `train.py` evaluates test best F1 each epoch but saves the final model; **do not mislabel this as observed best-test checkpoint saving**. Reserve, no first-reproduction advantage established |
| **WRADMts**, *Warping resilient robust anomaly detection for multivariate time series*. [Machine Learning 114, article 29](https://link.springer.com/article/10.1007/s10994-024-06689-7), published **27 January 2025**, accepted 12 December 2024; DOI `10.1007/s10994-024-06689-7`; peer-reviewed | Publisher manuscript evaluates both; ten-sample median features/modal labels. [Linked author code](https://github.com/WRADMts/WRADMts) uses validation-loss checkpoints, but [`evaluate.py`](https://raw.githubusercontent.com/WRADMts/WRADMts/main/evaluate.py) uses full-test error statistics, test-best thresholds and point adjustment; `main.py` constructs windows before forming loaders. Release/license and split independence unresolved. **Robustness reserve**, substantial protocol changes still needed |
| **RoCA**, *Robust Contrastive One-Class Time Series Anomaly Detection With Contaminated Data*. [arXiv:2503.18385](https://arxiv.org/abs/2503.18385), first submitted **24 March 2025**. [Author repository](https://github.com/ruiking04/RoCA) cites TNNLS 2026, DOI `10.1109/TNNLS.2026.3702237`, [IEEE 11575088](https://ieeexplore.ieee.org/document/11575088); primary publisher/date verification incomplete | [Full preprint](https://arxiv.org/html/2503.18385v1), §V-A/Tables II–III: both. MIT author code; loader comments identify SWaT A2 Dec2015/WADI A2 Nov2019, not verified file hashes. [`dataset.py`](https://raw.githubusercontent.com/ruiking04/RoCA/main/dataloader/dataset.py) retains all training windows after selecting a validation subset, creating train/validation overlap. [`data_preprocessing.py`](https://raw.githubusercontent.com/ruiking04/RoCA/main/dataloader/data_preprocessing.py) fills missing test values using full-test means. Revised point-adjusted validation F1/test monitoring require further audit. **Priority contamination reading; not a cleaner execution replacement.** Training-contamination robustness does not establish protection of online twin updates |
| **ECNU-GNN**, *Edge conditional node update graph neural network for multivariate time series anomaly detection*. [Information Sciences 679](https://www.sciencedirect.com/science/article/pii/S0020025524009769), 121062, **September 2024**; DOI `10.1016/j.ins.2024.121062`; [author institution record](https://pure.korea.ac.kr/en/publications/edge-conditional-node-update-graph-neural-network-for-multivariat/). [Preprint](https://arxiv.org/abs/2401.13872), **25 January 2024**; first-online day unverified | [Full preprint](https://arxiv.org/html/2401.13872v1), §4: both and validation-loss stopping. [Publisher-linked repository](https://github.com/hayoung-jo/ECNU-GNN) contains a README promising code; runnable implementation/license not verified. Exact releases/preprocessing/threshold execution unresolved. **Hold for implementation**, not preferred over inspectable CAROTS |

For RoCA, a search-indexed [PubMed record](https://pubmed.ncbi.nlm.nih.gov/42335058/) corroborates 23 June 2026 ahead-of-print publication, but this is secondary metadata. It does not close the primary publisher-verification gap. The unambiguous verified manuscript remains the preprint. SensitiveHUE's additional exact-title/DOI/KDD searches did not resolve its previous full-text hold.

Additional queries:

```text
"SWaT" "WADI" "2024" "code" "anomaly" AAAI
"SWaT" "WADI" "2025" "github" KDD
"NPSR" anomaly detection paper 2023
"Nominality Score Conditioned" github
"RoCA" "anomaly detection" 2025
"SWaT" "WADI" "2024" "TKDE"
"SWaT" "WADI" "2025" "TNNLS"
"Edge conditional node update graph" pdf
"RoCA" "3702237"
"Warping resilient robust anomaly" github
"SensitiveHUE" "3671919" pdf
"RoCA" "11575088" date
"SensitiveHUE" site:kdd2024.kdd.org
"3637528.3671919" ACM
```

## Published-manuscript and pinned-code recheck: CAROTS versus CCM-TAD

The earlier browser PDF failures were overcome with public HTTP reads and in-memory `pdftotext` extraction. **Correction to prior access limits:** published proceedings passages were now checked directly, rather than relying solely on arXiv. This does not claim complete byte-for-byte equivalence between all versions. No PDFs were saved into the project collection.

| Artifact | Observed identifier |
|---|---|
| [CAROTS published PDF](https://raw.githubusercontent.com/mlresearch/v267/main/assets/kim25aa/kim25aa.pdf) | 4,383,503 bytes; SHA-256 `b9c8de2e1f517e0df614ae88bb8f3e1a6b1f065e2952cbfd0cd19c67b4e5b568` |
| [CCM-TAD published PDF](https://raw.githubusercontent.com/mlresearch/v306/main/assets/murad26a/murad26a.pdf) | 5,181,951 bytes; SHA-256 `5832f4246e78629638c80a41d1a4c8cb87ec7f636c45f89d94c5c48ef814ecd7` |
| CAROTS `master` | `63a41f45a2ae680d5cdbb2d5739e7a11264867cb`, committed 2025-08-14T15:28:08Z |
| CCM-TAD `main` | `3a8bc8263b648a707cd0658bf4f06517fb9e52c5`, committed 2026-09-15T21:01:02Z |

**CAROTS:** proceedings §5.1/Table 1 and Appendix A.1 confirm both datasets. Appendix B confirms validation-loss selection, best-F1 reporting, no point-adjusted main F1 and clipping 1.0. The pinned [`config.py`](https://github.com/kimanki/CAROTS/blob/63a41f45a2ae680d5cdbb2d5739e7a11264867cb/config.py#L79) instead defaults to clipping 0.5: a verified paper/code discrepancy to resolve before running. [`trainer_carots.py`](https://github.com/kimanki/CAROTS/blob/63a41f45a2ae680d5cdbb2d5739e7a11264867cb/models/carots/trainer_carots.py#L61) and CUTS+ select validation loss; both forbidden test-threshold/reporting paths remain in the [earlier code audit](CAROTS_AND_INFORMATION_THEORETIC.md). License remains MIT-derived/non-commercial; CUDA portability untested. [Issue #6](https://github.com/kimanki/CAROTS/issues/6) reports 51-versus-49 channels, but its proposed cause is **a user report, not our reproduced defect**. [Issue #4](https://github.com/kimanki/CAROTS/issues/4) discusses clipping; [PR #3](https://github.com/kimanki/CAROTS/pull/3) was open, not merged support. Exact-title correction/erratum searches located no authoritative correction in this bounded pass.

**CCM-TAD:** [ICML 2026/PMLR 306](https://proceedings.mlr.press/v306/murad26a.html), Murad and Yilmaz, *Cluster-Aware Causal Mixer for Online Anomaly Detection in Multivariate Time Series*, 91338–91362; conference **6–11 July 2026**; preprint `2506.00188` first **30 May 2025**, v2 **4 June 2026**. Published §4.1/Tables 1–3 and Appendix C confirm both; appendices describe WADI2017, factor-five preprocessing, normal validation and Optuna. Some comparison numbers are borrowed from prior papers (Appendix F), not rerun under one protocol. MIT code is linked from proceedings; Python3.10/PyTorch2.5.1 guidance is not a tested local environment.

Pinned static findings explain why CCM-TAD does not displace CAROTS:

- [`exp_anomaly.py`](https://github.com/Secure-and-Intelligent-Systems-Lab/CCM-TAD/blob/3a8bc8263b648a707cd0658bf4f06517fb9e52c5/exp/exp_anomaly.py#L133): evaluates test every epoch, saves using test F1 and reports the objective to Optuna.
- [`Dataset_SWAT.py`](https://github.com/Secure-and-Intelligent-Systems-Lab/CCM-TAD/blob/3a8bc8263b648a707cd0658bf4f06517fb9e52c5/data_provider/Dataset_SWAT.py#L102): centered 50-point smoothing uses future measurements relative to a nominal timestamp; the loader assigns original labels after computing resampled labels, creating an alignment risk when downsampling.
- [`downsampling.py`](https://github.com/Secure-and-Intelligent-Systems-Lab/CCM-TAD/blob/3a8bc8263b648a707cd0658bf4f06517fb9e52c5/utils/downsampling.py#L12): minimum binary labels differ from CAROTS median reduction and original event labels.
- [`sequence_based_anomaly_evaluation.py`](https://github.com/Secure-and-Intelligent-Systems-Lab/CCM-TAD/blob/3a8bc8263b648a707cd0658bf4f06517fb9e52c5/utils/ccm_tad_anomaly_evaluation/sequence_based_anomaly_evaluation.py#L36): further test-label parameter/threshold selection. [`pred_anomaly_start_end_update.py`](https://github.com/Secure-and-Intelligent-Systems-Lab/CCM-TAD/blob/3a8bc8263b648a707cd0658bf4f06517fb9e52c5/utils/ccm_tad_anomaly_evaluation/pred_anomaly_start_end_update.py#L12) retrospectively changes boundaries; do not count reconstructed onset as an online alarm's availability time.

These are code-level evidence and reader-inferred risks; no benchmark failure was observed. WADI filename expectations differ from CAROTS A2, while CCM-TAD's processed SWaT arrays lack verified provider equivalence. Neither repository establishes our data permission.

## Read-only source retrieval commands

Working directory: `/Users/matrixusman/CUI/DigitalTwin`. The worker used `python3` from shell `PATH`; the exact interpreter path/version was not captured in that subtask. Existing `/opt/homebrew/bin/pdftotext` was used. Initial sandboxed HTTP attempts failed DNS resolution; the successful public reads used authorized network escalation. These were source reads, not package installation or experiment commands. Both PDF extractions and both commit lookups succeeded. No local PDF/text artifact was created.

Exact PDF command executed:

```sh
python3 - <<'PY'
import urllib.request, subprocess, concurrent.futures, hashlib
urls=[('CAROTS','https://raw.githubusercontent.com/mlresearch/v267/main/assets/kim25aa/kim25aa.pdf'),('CCM-TAD','https://raw.githubusercontent.com/mlresearch/v306/main/assets/murad26a/murad26a.pdf')]
def read(item):
 name,url=item
 try:
  data=urllib.request.urlopen(url,timeout=30).read()
  text=subprocess.run(['/opt/homebrew/bin/pdftotext','-layout','-','-'],input=data,capture_output=True,check=True).stdout.decode()
  lines=text.splitlines()
  keys=['validation','best F1','downsampl','WADI','gradient clipping','Optuna','RTX','A40','tuning']
  indices=set()
  for i,line in enumerate(lines):
   if any(k.lower() in line.lower() for k in keys):
    indices.update(range(max(0,i-1),min(len(lines),i+3)))
  print(name,url,'bytes',len(data),'sha256',hashlib.sha256(data).hexdigest())
  print('\n'.join(f'{i+1}: {lines[i]}' for i in sorted(indices)))
 except Exception as e:print(name,type(e).__name__,str(e))
with concurrent.futures.ThreadPoolExecutor(2) as pool:list(pool.map(read,urls))
PY
```

Exact commit metadata command executed:

```sh
python3 - <<'PY'
import json, urllib.request, concurrent.futures
items=[('kimanki/CAROTS','master'),('Secure-and-Intelligent-Systems-Lab/CCM-TAD','main')]
def read(item):
 repo,branch=item
 url='https://api.github.com/repos/'+repo+'/commits/'+branch
 try:
  r=json.load(urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Research-source-audit'}),timeout=20))
  return {'repo':repo,'sha':r.get('sha'),'url':r.get('html_url'),'date':r.get('commit',{}).get('committer',{}).get('date')}
 except Exception as e:return {'repo':repo,'error':str(e)}
for r in concurrent.futures.ThreadPoolExecutor(2).map(read,items):print(json.dumps(r))
PY
```

## Interpretation

Novelty review must include relevant older papers, preprints and non-twin contamination/shift methods even when the main numerical comparison has a tighter admission rule. Publication date, peer review, usable code and comparable information access are separate properties. A method can be important prior art while remaining unsuitable for our first reproduction.
