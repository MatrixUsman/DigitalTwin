"""Download explicitly listed public research artifacts; never execute their code.

Use from water/: python3 tools/collect_baseline_resources.py
This collector does not obtain SWaT/WADI data or submit access requests.
"""

import concurrent.futures
import hashlib
import json
from pathlib import Path
import sys
from datetime import datetime, timezone
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "baselines/acquisition_sources.json"
OUT = ROOT / "baselines/RESOURCE_MANIFEST.json"
MAX_BYTES = 64 * 1024 * 1024


def now():
    return datetime.now(timezone.utc).isoformat()


def fetch(item, previous):
    result = dict(item, checked_at_utc=now())
    path = (ROOT / item["path"]).resolve()
    if not path.is_relative_to(ROOT / "baselines"):
        raise ValueError("Destination must remain within water/baselines")
    if not item["url"].startswith("https://"):
        raise ValueError("Only explicit public HTTPS sources are supported")
    path.parent.mkdir(parents=True, exist_ok=True)
    partial = path.with_name(path.name + ".partial")
    try:
        if path.exists():
            data = path.read_bytes()
            if previous and previous.get("url") == item["url"] and previous.get("sha256"):
                if hashlib.sha256(data).hexdigest() != previous["sha256"]:
                    raise ValueError("Existing bytes differ from the previous acquisition manifest")
            result["status"] = "present_verified"
        else:
            req = urllib.request.Request(item["url"], headers={"User-Agent": "Research-resource-collection/1.0"})
            with urllib.request.urlopen(req, timeout=35) as response:
                result["resolved_url"] = response.url
                result["content_type"] = response.headers.get("Content-Type")
                length = response.headers.get("Content-Length")
                if length and int(length) > MAX_BYTES:
                    raise ValueError("Artifact exceeds the explicit per-file size limit")
                data = response.read(MAX_BYTES + 1)
                if len(data) > MAX_BYTES:
                    raise ValueError("Artifact exceeds the explicit per-file size limit")
            if item.get("kind") == "pdf" and not data.startswith(b"%PDF-"):
                raise ValueError("Response is not a PDF; not saved")
            if item.get("kind") == "json":
                json.loads(data)
            if item.get("expected_bytes") is not None and len(data) != item["expected_bytes"]:
                raise ValueError("Byte length differs from source metadata")
            if item.get("expected_sha256") and hashlib.sha256(data).hexdigest() != item["expected_sha256"]:
                raise ValueError("SHA-256 differs from audited source")
            if item.get("git_blob_sha1"):
                digest = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
                if digest != item["git_blob_sha1"]:
                    raise ValueError("Downloaded bytes do not match pinned Git blob")
            partial.write_bytes(data)
            partial.replace(path)
            result["status"] = "downloaded"
        if item.get("kind") == "pdf" and not data.startswith(b"%PDF-"):
            raise ValueError("Existing file is not a PDF")
        result["bytes"] = len(data)
        result["sha256"] = hashlib.sha256(data).hexdigest()
        if item.get("git_blob_sha1"):
            blob_hash = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
            if blob_hash != item["git_blob_sha1"]:
                raise ValueError("Downloaded bytes do not match pinned Git blob")
        if item.get("expected_bytes") is not None and len(data) != item["expected_bytes"]:
            raise ValueError("Existing file byte count differs")
        if item.get("expected_sha256") and result["sha256"] != item["expected_sha256"]:
            raise ValueError("Existing file SHA-256 differs")
    except Exception as exc:
        partial.unlink(missing_ok=True)
        result["status"] = "unavailable"
        result["error"] = f"{type(exc).__name__}: {exc}"
    return result


def main():
    spec = json.loads(SPEC.read_text())
    previous = json.loads(OUT.read_text()) if OUT.exists() else {"attempts": []}
    known = {entry["path"]: entry for entry in previous.get("resources", [])}
    entries = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for entry in pool.map(fetch, spec["resources"], [known.get(x["path"]) for x in spec["resources"]]):
            entries.append(entry)
            print(entry["status"], entry["path"], flush=True)
    manifest = {
        "project": "water",
        "purpose": "Published source collection, not our experiments or dataset access",
        "updated_at_utc": now(),
        "python": sys.version,
        "interpreter": sys.executable,
        "collector_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "resources": entries,
        "attempts": previous["attempts"] + [{"at_utc": now(), "resources": entries}],
    }
    OUT.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"available": sum(x["status"] != "unavailable" for x in entries),
                      "unavailable": sum(x["status"] == "unavailable" for x in entries)}))
    if any(x["status"] == "unavailable" for x in entries):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
