# Reference audit v0.24 — Group C (references 19–28)

Checked UTC: 2026-10-24T08:46:35.973257+00:00

All ten numbered references are real. No hard factual error was identified in the cited versions. This is an existence and metadata audit, not a claim-support audit. The draft can update the publication status for motionconformal and robotactive while preserving the exact manuscripts inspected. One original-source page-range check remains incomplete for tsbad.

## Per-reference findings

### 19. `inputthreshold`

**Existence:** verified. **Metadata:** `cited_fields_verified_across_publisher_search_record_and_author_institution`.

Publisher and author institution independently identify the same paper. No metadata contradiction found.

**Current vs verified:** See exact current printed/BibTeX entries and verified fields in `GROUP_C.json`. Title, author identity/order and cited source/version match; the verified status and dates are recorded there.

**Correction:** No factual correction identified for the explicitly cited source version.

**Primary observations:**
- [Publisher search result](https://www.sciencedirect.com/science/article/abs/pii/S1474667016380089): Title, journal, volume38, issue1, pages211–216, year2005 and DOI visible; direct opening returned403.
- [Author institutional publications list, search result](https://www.dcsc.tudelft.nl/~tkeviczky/publications.html): Entry C8 identifies same title, four authors in cited order,16thIFAC World Congress, Prague,4–8July2005.

**Limits:** DOI resolver failed and direct ScienceDirect page returned403. Publisher-indexed search text, rather than an opened full page, supplied venue/pages/DOI. Full text not needed or re-reviewed for this audit.

### 20. `motionconformal`

**Existence:** verified. **Metadata:** `cited_fields_verified_publication_status_enrichment_available`.

The existing version-specific citation is accurate. It is now possible to distinguish the inspected arXivv2 from the already published proceedings record.

**Current vs verified:** See exact current printed/BibTeX entries and verified fields in `GROUP_C.json`. Title, author identity/order and cited source/version match; the verified status and dates are recorded there.

**Correction:** Optional bibliographic enrichment: add the final IEEE DOI and publication status while retaining consulted arXivv2 and its29July2024date. Do not silently claim final full text was inspected.

**Primary observations:**
- [Opened arXiv record](https://arxiv.org/abs/2404.16500v2): Exact title, all five authors, v1/v2 dates, arXivDOI and acceptance comment.
- [Publisher IEEE indexed record](https://doi.org/10.1109/ITSC58415.2024.10920241): Title, ITSC2024, conference24–27September2024, added20March2025 and finalDOI.
- [Author institutional publications page, search result](https://www.tu-braunschweig.de/en/ifr/institute/staff/translate-to-english-m-sc-marvin-loba): Five-author order and final ITSC2024 citation with pages1778–1785 and sameDOI.

**Limits:** Final pages confirmed on author institutional list; IEEE extracted record did not display page range. No final-paper claim audit undertaken.

### 21. `tsbad`

**Existence:** verified. **Metadata:** `existence_core_metadata_verified_original_page_range_export_inaccessible`.

The exact work and DOI are verified. Its original BibTeX link could not be fetched, so the existing page range is retained as corroborated rather than fully reverified.

**Current vs verified:** See exact current printed/BibTeX entries and verified fields in `GROUP_C.json`. Title, author identity/order and cited source/version match; the original proceedings page range could not be reverified directly.

**Correction:** No factual correction identified for the explicitly cited source version.

**Primary observations:**
- [Opened official proceedings record](https://proceedings.neurips.cc/paper_files/paper/2024/hash/c3f3c690b7a99fba16d0efd35cb83b2c-Abstract-Datasets_and_Benchmarks_Track.html): Exact title, two authors, NeurIPS37/2024, track and DOI.
- [Later official proceedings paper, citation only](https://proceedings.neurips.cc/paper_files/paper/2025/file/4b52b3c50110fc10f6a1a86055682ea2-Paper-Conference.pdf): Search extraction cites the current108231–108261range; corroboration only, not original bibliographic authority.

**Limits:** Official BibTeX link returned an internal error. Two attempted BibTeX URL forms were also inaccessible. This audit does not mark original-source page-range verification complete.

### 22. `vus`

**Existence:** verified. **Metadata:** `cited_fields_verified`.

The printed abbreviated author list and complete BibTeX list agree with publisher metadata.

**Current vs verified:** See exact current printed/BibTeX entries and verified fields in `GROUP_C.json`. Title, author identity/order and cited source/version match; the verified status and dates are recorded there.

**Correction:** No factual correction identified for the explicitly cited source version.

**Primary observations:**
- [Opened publisher article record](https://link.springer.com/article/10.1007/s00778-025-00907-x): All ten authors, title, volume34, article32, DOI, acceptance and version-of-record dates.
- [Opened publisher issue contents](https://link.springer.com/journal/778/volumes-and-issues/34-3): Lists VUS in volume34, issue3 as article32.

**Limits:** Publisher full article is subscription content. Public metadata were sufficient for this audit.

### 23. `rapt`

**Existence:** verified. **Metadata:** `cited_fields_verified`.

Current citation precisely identifies v2. Limited acceptance-status search did not establish a venue; that is not proof that no other publication exists.

**Current vs verified:** See exact current printed/BibTeX entries and verified fields in `GROUP_C.json`. Title, author identity/order and cited source/version match; the verified status and dates are recorded there.

**Correction:** No factual correction identified for the explicitly cited source version.

**Primary observations:**
- [Opened arXiv record](https://arxiv.org/abs/2602.01515v2): Exact v2 title, five authors, dates and arXiv-issuedDOI; no journal-reference or acceptance field displayed.

**Limits:** No peer-reviewed venue independently established. No full-text claims re-reviewed.

### 24. `robotactive`

**Existence:** verified. **Metadata:** `cited_fields_verified_publication_status_enrichment_available`.

Acceptance remains accurately reported as author metadata in the cited arXivv2, but the present audit found stronger publisher evidence that proceedings publication exists.

**Current vs verified:** See exact current printed/BibTeX entries and verified fields in `GROUP_C.json`. Title, author identity/order and cited source/version match; the verified status and dates are recorded there.

**Correction:** Optional status enrichment: acknowledge verified IEEE ICRA2026 proceedings record while retaining inspected arXivv2. Confirm finalDOI/pages from primary export before adding those fields; do not infer final full-text identity.

**Primary observations:**
- [Opened arXiv record](https://arxiv.org/abs/2603.13003v2): Exact title, authors, v1/v2 dates, arXivDOI and v2 acceptance comment.
- [Publisher indexed search result](https://ieeexplore.ieee.org/abstract/document/11697152): Exact title, published-in ICRA2026, conference1–5June2026 and added30September2026.
- [Secondary bibliographic lead only](https://dblp.uni-trier.de/rec/conf/icra/GualandiP26.html): Supplies finalDOI and17525–17532pages, not promoted to primary-verified fields.

**Limits:** Direct IEEE page returned418; DOI resolver was inaccessible. FinalDOI and pages were visible only in secondaryDBLP. Final proceedings equations not inspected.

### 25. `renpreprint`

**Existence:** verified. **Metadata:** `cited_fields_verified`.

The current deliberate preprint citation matches its record. The final2026title and author order differ, so merging their metadata would be incorrect.

**Current vs verified:** See exact current printed/BibTeX entries and verified fields in `GROUP_C.json`. Title, author identity/order and cited source/version match; the verified status and dates are recorded there.

**Correction:** No factual correction identified for the explicitly cited source version.

**Primary observations:**
- [Opened arXiv record](https://arxiv.org/abs/2504.19688v1): Exact title, author order, v1date and arXivDOI; onlyv1 displayed in submission history.

**Limits:** No inference about final2026equations or guarantees follows from this bibliographic verification.

### 26. `iresnet`

**Existence:** verified. **Metadata:** `cited_fields_verified`.

The current printed citation and BibTeX metadata agree with PMLR. DOI absence is not a defect when the official source gives a stable proceedingsURL.

**Current vs verified:** See exact current printed/BibTeX entries and verified fields in `GROUP_C.json`. Title, author identity/order and cited source/version match; the verified status and dates are recorded there.

**Correction:** No factual correction identified for the explicitly cited source version.

**Primary observations:**
- [Opened official PMLR record and embedded BibTeX](https://proceedings.mlr.press/v97/behrmann19a.html): Title, five authors, conference, series, volume, pages, year and9–15June dates.

**Limits:** This fresh audit checked metadata, not the historic note that a supplementary proof had been inspected.

### 27. `lipschitzauto`

**Existence:** verified. **Metadata:** `cited_fields_verified`.

The current citation matches official proceedings metadata, including spelling and date.

**Current vs verified:** See exact current printed/BibTeX entries and verified fields in `GROUP_C.json`. Title, author identity/order and cited source/version match; the verified status and dates are recorded there.

**Correction:** No factual correction identified for the explicitly cited source version.

**Primary observations:**
- [Opened official PMLR record and embedded BibTeX](https://proceedings.mlr.press/v108/kim20c.html): Title, four authors, conference, series, volume, pages, year and26–28August dates.

**Limits:** This fresh audit checked metadata, not the historic full-text-inspection note.

### 28. `diffint`

**Existence:** verified. **Metadata:** `cited_fields_verified_acceptance_independence_limited`.

Current wording correctly limits acceptance evidence to the author-reported arXiv comment. A limited exact-title conference-domain search supplied no independent final record.

**Current vs verified:** See exact current printed/BibTeX entries and verified fields in `GROUP_C.json`. Title, author identity/order and cited source/version match; the verified status and dates are recorded there.

**Correction:** No factual correction identified for the explicitly cited source version.

**Primary observations:**
- [Opened arXiv record](https://arxiv.org/abs/2609.03878v1): Exact title, two authors, v1date, arXivDOI and ICDM2026acceptance comment.

**Limits:** Final conference proceedings, DOI and page range not independently verified. Search nonreturn is not evidence of nonexistence.

## Extra unnumbered final REN article

**Existence:** verified. Real final article; title and author order differ from renpreprint. Bibliographic existence does not resolve prior full-equation access limitation.

Verified final metadata: Farhad Ghanipoor; Giancarlo Ferrari Trecate; Nathan van de Wouw; Carlos Murguia. *Provably robust data-driven sensor fault diagnosis using incrementally stable recurrent equilibrium networks*. Automatica191,113096, September2026. DOI10.1016/j.automatica.2026.113096.

- [Publisher indexed search result](https://www.sciencedirect.com/science/article/pii/S0005109826002803): Exact final title, altered author order, Automatica191, September2026,113096 andDOI.
- [Author lab institutional publication list, search result](https://www.epfl.ch/labs/decode/dependable-control-and-decision-group/publications/): Corroborates title, altered author order, journal, volume, year andDOI.

No final-equation access or preprint/final equivalence is asserted.

## Provenance and boundaries

The audit bound inputs to the unchanged hashes in INTAKE.json; GROUP_C.json records those hashes, exact current entries, verified fields, sourceURLs, actual access outcomes and querylog. Only GROUP_C.json and GROUP_C.md were written. No sealed manuscript/source was modified.

Primary records were freshly browsed. Search-indexed publisher extracts are identified as such. DOI presence does not itself establish peer review; arXiv records are distinguished from proceedings and journal publication. The absence of a final record in a limited search is not evidence of nonexistence.
