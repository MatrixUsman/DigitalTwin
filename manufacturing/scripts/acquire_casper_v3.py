#!/usr/bin/env python3
"""Acquire the explicitly authorized original CASPER release; never run models.

Standard library only. Original bytes remain under ignored raw storage. Public
metadata is retained locally; the safe receipt contains no signed download URLs.
The latest API route is bracketed by release checks because a version-specific
archive route has not been established. Existing completed artifacts are checked,
not overwritten. Partial archives can resume using an HTTP Range request.
"""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import platform
import shutil
import stat
import subprocess
import sys
import time
from datetime import datetime, timezone
import urllib.request
import zipfile

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT / "datasets/raw/casper/v3"
META = PROJECT / "local/casper_v3_receipt"
RECEIPT = PROJECT / "datasets/manifests/casper_v3_receipt.json"
SLUG = "hkayan/industrial-robotic-arm-anomaly-detection"
BASE = "https://www.kaggle.com/api/v1/datasets/"
DOWNLOAD = BASE + "download/" + SLUG
EXPECTED = {
    "dataset/arms.pcap": 3703911932,
    "dataset/left_arm.csv": 1965113819,
    "dataset/nicla.csv": 138908648,
    "dataset/right_arm.csv": 1978193094,
    "nicla_fixed.csv": 113184581,
}

def now():
    return datetime.now(timezone.utc).isoformat()

def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def metadata(endpoint, suffix):
    url = BASE + endpoint + "/" + SLUG
    with urllib.request.urlopen(url, timeout=60) as response:
        body = response.read()
    target = META / (endpoint + "_" + suffix + ".json")
    target.write_bytes(body)
    return json.loads(body), {"url": url, "retrieved_at_utc": now(),
                             "local_path": str(target.relative_to(PROJECT)),
                             "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}

def atomic_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".json.partial")
    tmp.write_text(json.dumps(data, indent=2) + "\n")
    tmp.replace(path)

def main():
    for path in (ROOT, META, RECEIPT.parent):
        path.mkdir(parents=True, exist_ok=True)
    assert subprocess.run(["git", "check-ignore", "-q", str(ROOT / "archive.zip")],
                          cwd=PROJECT).returncode == 0, "Raw storage must be ignored"
    assert shutil.disk_usage(ROOT).free > 15_000_000_000, "Need 15 GB free reserve"
    before, before_rec = metadata("view", "before")
    listing, list_rec = metadata("list", "before")
    assert before["currentVersionNumber"] == 3
    assert before["licenseName"] == "CC BY-SA 4.0"
    assert {f["name"]: f["totalBytes"] for f in listing["datasetFiles"]} == EXPECTED
    assert not listing.get("nextPageToken"), "Listing is not complete"
    receipt = {
        "schema_version": 1, "project": "manufacturing", "owner": "Haiqa Mushtaq",
        "operator": "Codex acquisition audit; no experiment", "started_at_utc": now(),
        "dataset": {"provider": "Hakan Kayan / Kaggle", "slug": SLUG,
                    "title": before["title"], "version": 3,
                    "version_timestamp": before["lastUpdated"],
                    "license": before["licenseName"],
                    "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
                    "landing_url": "https://www.kaggle.com/datasets/" + SLUG,
                    "archive_url": DOWNLOAD,
                    "archive_route": "latest, bracketed by version 3 metadata checks",
                    "provider_total_uncompressed_bytes": sum(EXPECTED.values())},
        "environment": {"python": sys.version, "platform": platform.platform()},
        "command": "python3 manufacturing/scripts/acquire_casper_v3.py",
        "working_directory": ". (repository root)",
        "metadata": [before_rec, list_rec], "status": "acquiring", "files": [],
        "limitations": ["Provider supplies no authoritative SHA-256 checksums in the inspected metadata.",
                        "CRC and local hashes verify consistency of received bytes, not scientific label validity.",
                        "Public access and license do not grant publication approval for this workspace."]}
    atomic_json(RECEIPT, receipt)
    archive = ROOT / "original_casper_v3.zip"
    partial = archive.with_suffix(".zip.partial")
    started = time.monotonic()
    if not archive.exists():
        offset = partial.stat().st_size if partial.exists() else 0
        headers = {"User-Agent": "Kaggle/1.7.4"}
        if offset:
            headers["Range"] = "bytes=" + str(offset) + "-"
        req = urllib.request.Request(DOWNLOAD, headers=headers)
        with urllib.request.urlopen(req, timeout=120) as response:
            code = response.status
            assert code in (200, 206), f"Unexpected HTTP status {code}"
            if offset and code == 206:
                assert response.headers.get("Content-Range", "").startswith("bytes " + str(offset) + "-")
                mode = "ab"
            else:
                mode, offset = "wb", 0
            length = int(response.headers["Content-Length"])
            total = length + offset
            assert total == 2824019108, f"Unexpected archive length {total}"
            receipt["archive_http"] = {"status": code, "content_type": response.headers.get("Content-Type"),
                                       "expected_bytes": total, "resume_offset": offset,
                                       "response_received_at_utc": now()}
            atomic_json(RECEIPT, receipt)
            done, last = offset, time.monotonic()
            print(f"Download started: {total} bytes; resume offset {offset}", flush=True)
            with partial.open(mode) as output:
                for block in iter(lambda: response.read(8 * 1024 * 1024), b""):
                    output.write(block)
                    done += len(block)
                    if time.monotonic() - last >= 20:
                        elapsed = time.monotonic() - started
                        rate = (done - offset) / max(elapsed, 0.01)
                        print(f"Received {done}/{total} bytes; {rate / 1e6:.2f} MB/s; estimated {(total-done)/max(rate,1):.0f} seconds remaining", flush=True)
                        last = time.monotonic()
            assert partial.stat().st_size == total
        partial.replace(archive)
    receipt["archive"] = {"local_path": str(archive.relative_to(PROJECT)),
                          "bytes": archive.stat().st_size, "sha256": digest(archive),
                          "received_at_utc": now()}
    receipt["status"] = "archive_received_extraction_pending"
    atomic_json(RECEIPT, receipt)
    after, after_rec = metadata("view", "after")
    receipt["metadata"].append(after_rec)
    assert after["currentVersionNumber"] == 3 and after["lastUpdated"] == before["lastUpdated"]
    assert after["licenseName"] == before["licenseName"]
    with zipfile.ZipFile(archive) as z:
        items = z.infolist()
        assert len(items) == len(EXPECTED) and len({i.filename for i in items}) == len(items)
        assert {i.filename: i.file_size for i in items} == EXPECTED
        for info in items:
            rel = PurePosixPath(info.filename)
            assert not rel.is_absolute() and ".." not in rel.parts and "\\" not in info.filename
            assert not stat.S_ISLNK(info.external_attr >> 16), "No archive symlinks permitted"
            assert not info.flag_bits & 1, "No encrypted members permitted"
            target = ROOT / "original" / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            part = target.with_suffix(target.suffix + ".partial")
            h, count = hashlib.sha256(), 0
            # Reading every member to EOF validates its ZIP CRC. Never execute it.
            with z.open(info) as source:
                output = part.open("wb") if not target.exists() else None
                try:
                    for block in iter(lambda: source.read(8 * 1024 * 1024), b""):
                        h.update(block)
                        count += len(block)
                        if output:
                            output.write(block)
                finally:
                    if output:
                        output.close()
            assert count == info.file_size
            if target.exists():
                assert target.stat().st_size == count and digest(target) == h.hexdigest()
            else:
                part.replace(target)
                os.chmod(target, 0o444)
            receipt["files"].append({"archive_member": info.filename,
                "local_path": str(target.relative_to(PROJECT)), "bytes": count,
                "sha256": h.hexdigest(), "zip_crc32": format(info.CRC, "08x"),
                "zip_crc_validation": "passed by complete decompression",
                "archive_stored_datetime_no_timezone": list(info.date_time),
                "profile_status": "not_yet_profiled"})
            atomic_json(RECEIPT, receipt)
            print(f"Validated and preserved {info.filename}: {count} bytes", flush=True)
    os.chmod(archive, 0o444)
    receipt["status"] = "received_integrity_verified"
    receipt["completed_at_utc"] = now()
    atomic_json(RECEIPT, receipt)
    print("CASPER receipt complete; no models or benchmark evaluation executed.", flush=True)

if __name__ == "__main__":
    main()
