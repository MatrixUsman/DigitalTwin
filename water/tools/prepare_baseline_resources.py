"""Extract reading material from downloaded papers without executing author code.

Run from water/: python3 tools/prepare_baseline_resources.py
Requires the already installed Poppler tools; installs nothing.
"""

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import tarfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "baselines"
derived = []


def record(path, source, operation):
    derived.append({
        "path": str(path.relative_to(ROOT)),
        "bytes": path.stat().st_size,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "source": str(source.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "operation": operation,
    })


def extract_source(baseline, name):
    archive = BASE / baseline / "artifacts/source" / name
    destination = archive.parent / "arxiv_v1"
    with tarfile.open(archive) as tar:
        members = tar.getmembers()
        if sum(m.size for m in members) > 64 * 1024 * 1024:
            raise ValueError("Unexpected source archive size")
        for member in members:
            relative = PurePosixPath(member.name)
            if relative.is_absolute() or ".." in relative.parts:
                raise ValueError("Unsafe archive path")
            path = destination / relative
            if not path.resolve().is_relative_to(destination.resolve()):
                raise ValueError("Archive target leaves destination")
            if member.isdir():
                path.mkdir(parents=True, exist_ok=True)
            elif member.isfile():
                path.parent.mkdir(parents=True, exist_ok=True)
                with tar.extractfile(member) as source:
                    path.write_bytes(source.read())
                record(path, archive, "Safe regular-file extraction; no TeX compilation")
            else:
                raise ValueError("Archive links/special files are not permitted")


extract_source("carots", "arxiv_2506.03964v1.source")
extract_source("it_dt", "arxiv_2603.01621v1.source")

for baseline in ("carots", "it_dt", "dt_ensemble"):
    papers = BASE / baseline / "artifacts/papers"
    for paper in sorted(papers.glob("*.pdf")):
        target = paper.with_suffix(".txt")
        subprocess.run(["pdftotext", "-layout", str(paper), str(target)], check=True)
        record(target, paper, "pdftotext -layout; reading aid, PDF remains authoritative")
        info = paper.with_suffix(".pdfinfo.txt")
        info.write_bytes(subprocess.check_output(["pdfinfo", str(paper)]))
        record(info, paper, "pdfinfo")
    main = {"carots": "CAROTS_ICML2025.pdf", "it_dt": "IT_DT_arxiv_2603.01621v1.pdf",
            "dt_ensemble": "Ensemble_ScientificReports_VOR.pdf"}[baseline]
    paper = papers / main
    previews = papers.parent / "previews"
    previews.mkdir(exist_ok=True)
    stem = previews / "first_page"
    subprocess.run(["pdftoppm", "-f", "1", "-singlefile", "-scale-to", "1200", "-png", str(paper), str(stem)], check=True)
    record(stem.with_suffix(".png"), paper, "pdftoppm first page, 1200px preview")

xml = BASE / "dt_ensemble/artifacts/pmc/PMC13402577.1.xml"
tree = ET.parse(xml)
out = xml.parent.parent / "extracted"
out.mkdir(exist_ok=True)
index = {"source": str(xml.relative_to(ROOT)), "tables": [], "figures": [], "references": []}
for tag, group in [("table-wrap", "tables"), ("fig", "figures"), ("ref-list", "references")]:
    for number, node in enumerate(tree.findall(".//" + tag), 1):
        target = out / f"{group}_{number:02d}.xml"
        ET.ElementTree(node).write(target, encoding="utf-8", xml_declaration=True)
        record(target, xml, "ElementTree extraction; XML serialization may differ, content retained")
        text_path = target.with_suffix(".txt")
        text_path.write_text(" ".join("".join(node.itertext()).split()) + "\n")
        record(text_path, xml, "Plain text from XML element; formatting lost, not numerical experiment data")
        index[group].append({"source_id": node.get("id"), "xml": target.name, "text": text_path.name})
index["reference_count"] = len(tree.findall(".//ref-list/ref"))
index["supplementary_material_nodes"] = len(tree.findall(".//supplementary-material"))
target = out / "INDEX.json"
target.write_text(json.dumps(index, indent=2) + "\n")
record(target, xml, "XML element inventory")

manifest = {"purpose": "Local reading derivatives, never benchmark results",
            "updated_at_utc": datetime.now(timezone.utc).isoformat(),
            "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "tool_versions": {}, "artifacts": derived}
for tool in ["pdftotext", "pdfinfo", "pdftoppm"]:
    result = subprocess.run([tool, "-v"], text=True, capture_output=True, check=True)
    manifest["tool_versions"][tool] = (result.stdout + result.stderr).splitlines()[0]
(BASE / "DERIVED_ARTIFACTS.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(json.dumps({"derived_files": len(derived), "ensemble_tables": len(index["tables"]),
                  "ensemble_references": index["reference_count"], "supplement_nodes": index["supplementary_material_nodes"]}))
