"""Seal the local versioned manuscript and its validation receipts."""
from pathlib import Path
import datetime
import hashlib
import json

here = Path(__file__).resolve().parent
project = here.parent
manifest = here / "PACKAGE_MANIFEST.json"
assert not manifest.exists(), "Preserve an existing package seal"
paths = [p for p in here.rglob("*") if p.is_file() and p != manifest and "__pycache__" not in p.parts]
paths += [project / name for name in (
    "output/pdf/ARX-RBF-Muhammad-Usman-v1.8.pdf",
    "output/ARX-RBF-Muhammad-Usman-v1.8-latex.zip",
    "research_cycles/gain_limited_v0.23/PACKAGE_MANIFEST.json",
    "research_cycles/novelty_v0.22/PACKAGE_MANIFEST.json",
    "local/manuscript_arx_rbf_v1.8/pdf_build/attempt_006/receipt.json",
    "local/manuscript_arx_rbf_v1.8/pdf_build/attempt_006/stdout.log",
    "local/manuscript_arx_rbf_v1.8/source_archive_build.log",
    "local/manuscript_arx_rbf_v1.8/source_archive_build_002.log",
    "local/manuscript_arx_rbf_v1.8/manuscript.txt",
    "local/manuscript_arx_rbf_v1.8/abstract.md",
)]
paths += sorted((project / "local/manuscript_arx_rbf_v1.8/render_006").glob("page-*.png"))
assert len(set(paths)) == len(paths)
bindings = {str(p.relative_to(project)): {"sha256": hashlib.sha256(p.read_bytes()).hexdigest(), "bytes": p.stat().st_size} for p in sorted(paths)}
record = {"utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "project": "manufacturing", "version": "manuscript_arx_rbf_v1.8", "path_base": "manufacturing", "file_count": len(bindings), "bindings": bindings, "scientific_status": "Candidate failed; original-method journal readiness not established", "scope": "Local manuscript/evidence seal; not publication approval or portable scientific replication"}
manifest.write_text(json.dumps(record, indent=2) + "\n")
assert all(hashlib.sha256((project / p).read_bytes()).hexdigest() == item["sha256"] for p, item in bindings.items())
print(json.dumps({"file_count": len(bindings), "manifest_sha256": hashlib.sha256(manifest.read_bytes()).hexdigest(), "passed": True}))
