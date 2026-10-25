"""Consolidate completed source reviews; does not perform network verification."""
from pathlib import Path
import datetime
import hashlib
import json

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
ROOT = PROJECT.parent
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
intake = json.loads((HERE / "INTAKE.json").read_text())
local = json.loads((HERE / "LOCAL_CHECKS.json").read_text())
rows = []
for group in "ABC":
    path = HERE / f"GROUP_{group}.json"
    report = json.loads(path.read_text())
    for item in report.get("references", report.get("records", [])):
        fields = item.get("verified_fields", item.get("verified"))
        rows.append({
            "number": item["number"], "key": item["key"],
            "existence": item.get("existence_status", item.get("existence_verdict")),
            "metadata": item.get("metadata_status", item.get("metadata_verdict")),
            "verified_fields": fields, "sources": item["sources"],
            "details_file": path.name, "details_sha256": sha(path),
        })
rows.sort(key=lambda x: x["number"])
assert len(rows) == 28 and [x["number"] for x in rows] == list(range(1, 29))
assert len({x["key"] for x in rows}) == 28
assert all(x["existence"] == "verified_real" for x in rows)
assert [(x["number"], x["key"]) for x in rows] == [(x["number"], x["key"]) for x in intake["references"]]
assert all(sha(ROOT / path) == digest for path, digest in intake["sources_sha256"].items())
old = json.loads((PROJECT / "manuscript_arx_rbf_v1.8/PACKAGE_MANIFEST.json").read_text())
assert all(sha(PROJECT / path) == info["sha256"] for path, info in old["bindings"].items())
record = {
    "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "scope": "Fresh source existence and bibliographic metadata audit; not full claim-support/retraction/replication review",
    "numbered_sources_verified_real": 28, "unverified_existence": 0,
    "fabricated_or_nonexistent_identified": 0, "required_substantive_metadata_corrections_identified": 0,
    "extra_prose_final_ren_doi_verified_real": True,
    "qualification": "Existence is complete; metadata access limitations and optional version updates remain explicit in per-reference reports.",
    "preserved_v18_bindings": len(old["bindings"]), "all_preserved": True,
    "missing_citations": local["missing_numbered_refs"], "unused_references": local["unused_numbered_refs"],
    "citation_occurrences": local["citation_occurrences"], "references": rows,
}
(HERE / "RESULTS.json").write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n")

notes = {
    3: "Corrected version exists; original 2024 citation remains valid.",
    5: "Conference article published in the 2024 Procedia volume.",
    9: "2023 early-online versus supported 2024 volume citation; direct IEEE date field blocked.",
    10: "Exact arXiv v5; workshop acceptance is author-reported, not ICML main-conference status.",
    14: "Verified through fresh indexed primary metadata; direct pages blocked.",
    18: "Exact arXiv v1 preprint; no peer-reviewed venue established.",
    19: "Verified through fresh indexed publisher and author-institution metadata.",
    20: "Cited arXiv v2 is real; a final ITSC conference record is also verified.",
    21: "Core metadata verified; original-source page-range export inaccessible.",
    23: "Exact arXiv v2 preprint; no peer-reviewed venue established.",
    24: "Cited arXiv v2 is real; final ICRA record now verified. Final DOI/pages remain secondary-only here.",
    25: "Exact 2025 preprint; later Automatica article has different title/author order.",
    28: "Exact arXiv v1; ICDM acceptance remains author-reported in this audit.",
}
head = """# Manufacturing manuscript v1.8: reference verification

Verified on 24 October 2026 against fresh online publisher, official proceedings, versioned arXiv and author-institution records.

**All 28 numbered references correspond to real papers. No fabricated or nonexistent reference was identified.** The additional Automatica DOI embedded in the prose also identifies a real article. No substantive factual correction to the intentionally cited source versions was established. This does not mean every field was directly accessible: precise qualifications appear below and in the group reports.

The bibliography and compiled manuscript contain the same 28 keys, all cited, with 40 citation occurrences. There are no missing or unused references. All 108 sealed v1.8 package bindings remain unchanged. The audit does not rewrite the delivered PDF or replace a cited preprint silently.

## Reference-by-reference result

Each source link below supports identity; additional primary URLs, full verified metadata, exact access method and limitations are recorded in the linked group reports. An inaccessible publisher page was not treated as evidence that a paper is fake.

| Ref. | Paper | Existence | Note |
|---|---|---|---|
"""
lines = [head]
for row in rows:
    sources = row["sources"]
    # Prefer an actually opened primary source over an inaccessible publisher route.
    chosen = next((x for x in sources if x.get("access") == "opened"), sources[0])
    title = row["verified_fields"]["title"].replace("|", "\\|")
    lines.append(f'| {row["number"]} | [{title}]({chosen["url"]}) | Real | {notes.get(row["number"], "Cited metadata match the inspected records.")} |\n')
lines.append("""
## Version notes and remaining editorial items

- **CASPER, ref. 3:** the author-hosted version of record is marked corrected V1.1, published 5 February 2025. Its bibliographic citation remains volume 5, issue 3, Article 18, August 2024. A correction notice is not a retraction.
- **voraus-AD, ref. 9:** author-institution records differ in date treatment: Hannover records 2023 early-online publication, while the coauthor's Linköping list cites volume 40, pages 438–451 in 2024. Preserve 2024 for this volume citation; the direct IEEE date fields were blocked. No mismatch in paper identity or DOI was found.
- **Motion-conformal, ref. 20:** the existing reference deliberately identifies arXiv v2 dated 29 July 2024. A final IEEE ITSC 2024 record is now verified, DOI [10.1109/ITSC58415.2024.10920241](https://doi.org/10.1109/ITSC58415.2024.10920241); its addition to IEEE in March 2025 does not change the conference year. Final pages 1778–1785 are supported by the author-institution list. Adding this final-publication information is optional enrichment, not repair of a fake citation.
- **Robot active defence, ref. 24:** the cited arXiv v2 is real. The [IEEE ICRA 2026 publication record](https://ieeexplore.ieee.org/abstract/document/11697152) now independently supports proceedings publication. Final DOI/pages were only observed in secondary DBLP during this audit and should not be promoted to primary-verified fields. The previous equation-level inspection scope remains the arXiv version.
- **TSB-AD, ref. 21:** official NeurIPS confirms the title, authors, volume, year and DOI. Its original BibTeX export was inaccessible. The printed range 108231–108261 is corroborated in a later official proceedings bibliography, but was not freshly verified from the original bibliographic export. No contrary range was found.
- **Number order:** if adopting the IEEE first-citation-order convention, the final four entries should be iResNet, Lipschitz autoencoders, DiffInt, then the REN preprint. The current list puts REN before those three. All citations resolve correctly; this is an ordering issue, not a nonexistent source. No target journal is selected.

Seven entries deliberately identify arXiv versions: 10, 18, 20, 23, 24, 25 and 28. They must not all be described as published journal articles. Some have independently verified final conference records; others retain preprint or author-reported acceptance status. The additional [Automatica 2026 article](https://www.sciencedirect.com/science/article/pii/S0005109826002803) is real, but differs from ref. 25 in title and author order; bibliographic verification does not resolve access to its final equations.

## Audit limits and evidence

This is an existence/metadata check, not a fresh full-text audit of whether every source supports every manuscript claim. It does not establish reproducibility, novelty, journal readiness, human reading or a complete retraction clearance. A narrow four-query Retraction Watch site search found no matching notice, but was not a complete database check and supplies no no-retraction certificate. No external model or programmatic bibliographic-resolver API was used. Three AI workers divided the list, sharing project context; root reconciled all records and independently checked selected recent sources.

- [References 1–9: source evidence and date/correction qualifications](GROUP_A.md)
- [References 10–18: source evidence and access limits](GROUP_B.md)
- [References 19–28 and the extra final REN DOI](GROUP_C.md)
- [Structured consolidated results](RESULTS.json)
- [Local cross-reference checks](LOCAL_CHECKS.json)
- [Root cross-checks and access limits](ROOT_CROSSCHECK.json)

The prior failed scientific criteria and journal-submission hold remain unchanged. No model training, dataset access, manuscript rebuild, external contact, upload or submission was performed for this audit.
""")
(HERE / "REPORT.md").write_text("".join(lines))
print(json.dumps({k: v for k, v in record.items() if k != "references"}, indent=2))
