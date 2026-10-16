"""Read-only structural audit of the saved baseline collection.

Run from water/: python3 tools/audit_baseline_resources.py
No author code is executed; no pickle or model is loaded. Preview derivatives
and audit reports are written separately from the acquired source material.
"""

import ast
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
import tarfile
import warnings
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "baselines"
OUT = BASE / "artifacts/verification"
OUT.mkdir(parents=True, exist_ok=True)
download = json.loads((BASE / "RESOURCE_MANIFEST.json").read_text())
derived = json.loads((BASE / "DERIVED_ARTIFACTS.json").read_text())
entries = download["resources"] + derived["artifacts"]
checks = []


def command(args):
    result = subprocess.run(args, capture_output=True, text=True, timeout=120)
    if result.returncode:
        raise ValueError(f"{args[0]} exited {result.returncode}: {result.stderr[:1000]}")
    return result.stdout, result.stderr


for entry in entries:
    path = ROOT / entry["path"]
    record = {"path": entry["path"], "checks": [], "warnings": []}
    try:
        data = path.read_bytes()
        if len(data) != entry["bytes"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
            raise ValueError("Acquisition/derivation manifest integrity mismatch")
        record["checks"].append("size_and_sha256_match")
        if entry.get("git_blob_sha1"):
            digest = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
            if digest != entry["git_blob_sha1"]:
                raise ValueError("Git blob mismatch")
            record["checks"].append("pinned_git_blob_matches")
        if entry.get("source"):
            source = ROOT / entry["source"]
            if hashlib.sha256(source.read_bytes()).hexdigest() != entry["source_sha256"]:
                raise ValueError("Derivative source hash mismatch")
            record["checks"].append("derivative_source_hash_matches")
        if path.suffix == ".pdf":
            info, stderr = command(["pdfinfo", str(path)])
            record["pages"] = int(next(x.split(":")[1] for x in info.splitlines() if x.startswith("Pages:")))
            command(["pdftotext", str(path), "-"])
            prefix = OUT / "rendered" / hashlib.sha256(data).hexdigest()[:16] / "page"
            prefix.parent.mkdir(parents=True, exist_ok=True)
            _, stderr = command(["pdftoppm", "-r", "36", "-png", str(path), str(prefix)])
            pages = sorted(prefix.parent.glob("page-*.png"))
            if len(pages) != record["pages"]:
                raise ValueError("PDF render page count mismatch")
            if stderr:
                record["warnings"].append(stderr.strip()[:1200])
            record["checks"].extend(["pdfinfo", "all_pages_text_parse", "all_pages_rasterize"])
        elif path.suffix == ".py":
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                ast.parse(data, filename=str(path))
            record["warnings"] += [str(x.message) for x in caught]
            record["checks"].append("python_ast_parse_only")
        elif path.suffix == ".sh":
            command(["bash", "-n", str(path)])
            record["checks"].append("bash_syntax_only")
        elif path.suffix in (".png", ".jpg"):
            target = OUT / "decoded_images" / (hashlib.sha256(data).hexdigest()[:16] + ".png")
            target.parent.mkdir(exist_ok=True)
            command(["sips", "-s", "format", "png", str(path), "--out", str(target)])
            record["checks"].append("image_decoded_by_sips")
        elif path.suffix == ".json":
            json.loads(data)
            record["checks"].append("json_parse")
        elif path.suffix == ".xml":
            ET.fromstring(data)
            record["checks"].append("xml_parse")
        elif path.suffix == ".source":
            count = 0
            with tarfile.open(path) as archive:
                for member in archive.getmembers():
                    parts = Path(member.name)
                    if parts.is_absolute() or ".." in parts.parts or not (member.isdir() or member.isfile()):
                        raise ValueError("Archive path/type is not a safe regular member")
                    if member.isfile():
                        with archive.extractfile(member) as stream:
                            original = stream.read()
                        extracted = path.parent / "arxiv_v1" / member.name
                        if original != extracted.read_bytes():
                            raise ValueError("Extracted source differs from archive member")
                        count += 1
            record["archive_regular_files"] = count
            record["checks"].append("all_archive_members_match_extracted_bytes")
        elif path.suffix == ".npy":
            if data[:6] != b"\x93NUMPY":
                raise ValueError("Not a NumPy container")
            major = data[6]
            width = 2 if major == 1 else 4
            size = int.from_bytes(data[8:8 + width], "little")
            if size > 65536:
                raise ValueError("Unexpected array header size")
            header = ast.literal_eval(data[8 + width:8 + width + size].decode())
            descriptor = header["descr"]
            if not isinstance(descriptor, str) or "O" in descriptor:
                raise ValueError("Object/structured array not decoded")
            item_size = int(descriptor[2:])
            if len(data) != 8 + width + size + math.prod(header["shape"]) * item_size:
                raise ValueError("Array payload size does not match header")
            record["array_header"] = header
            record["checks"].append("npy_numeric_header_and_payload_size_only")
        elif path.suffix == ".pth":
            if not zipfile.is_zipfile(path):
                record["warnings"].append("Non-ZIP checkpoint: format/content not inspected")
            else:
                with zipfile.ZipFile(path) as archive:
                    bad = archive.testzip()
                    if bad:
                        raise ValueError("Checkpoint ZIP CRC failure: " + bad)
                    record["zip_members"] = archive.namelist()
                record["checks"].append("checkpoint_zip_crc_only_no_deserialization")
        record["status"] = "pass_with_limits" if record["warnings"] else "pass"
    except Exception as exc:
        record.update(status="fail", error=f"{type(exc).__name__}: {exc}")
    checks.append(record)

xml_source = BASE / "dt_ensemble/artifacts/pmc/PMC13402577.1.xml"
xml_tree = ET.parse(xml_source)
semantic_checks = []


def element_structure(node):
    return node.tag, dict(node.attrib), node.text, [(element_structure(child), child.tail) for child in node]


for tag, group in [("table-wrap", "tables"), ("fig", "figures"), ("ref-list", "references")]:
    nodes = xml_tree.findall(".//" + tag)
    matches = []
    for number, node in enumerate(nodes, 1):
        target = BASE / "dt_ensemble/artifacts/extracted" / f"{group}_{number:02d}.xml"
        matches.append(element_structure(node) == element_structure(ET.parse(target).getroot()))
    semantic_checks.append({"group": group, "count": len(nodes), "all_identical": all(matches)})

summary = {
    "scope": "Integrity and format checks, not scientific validation or executable compatibility",
    "at_utc": datetime.now(timezone.utc).isoformat(),
    "python": sys.version,
    "command": "python3 tools/audit_baseline_resources.py",
    "working_directory": str(ROOT),
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "manifest_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in [BASE / "RESOURCE_MANIFEST.json", BASE / "DERIVED_ARTIFACTS.json"]},
    "counts": dict(Counter(x["status"] for x in checks)),
    "xml_semantic_equivalence": {
        "source": str(xml_source.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(xml_source.read_bytes()).hexdigest(),
        "comparisons": semantic_checks,
    },
    "checks": checks,
}
(BASE / "INTEGRITY_AUDIT.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary["counts"]))
for result in checks:
    if result["status"] == "fail":
        print(result["path"], result["error"])
if summary["counts"].get("fail") or not all(x["all_identical"] for x in semantic_checks):
    raise SystemExit(1)
