#!/usr/bin/env python3
"""Fully validate nested CASPER controller fields without training or features.

Standard-library streaming JSON/number parsing only; never eval or execute cells.
Raw files and the earlier acquisition receipt are read-only inputs. Outputs are
aggregate audit metadata under ignored local storage, not a processed dataset.
"""
import collections
import csv
import hashlib
import json
import math
from pathlib import Path
import platform
import sys
import time
from datetime import datetime, timezone

PROJECT = Path(__file__).resolve().parents[1]
OUT = PROJECT / "local/casper_controller_schema_audit"
EXPECTED = {
    "Timestamp": 1, "Actual Joint Positions": 6, "Actual Joint Velocities": 6,
    "Actual Joint Currents": 6, "Actual Cartesian Coordinates": 6,
    "Actual Tool Speed": 6, "Generalized Forces": 6,
    "Temperature of Each Joint": 6, "Execution Time": 1, "Safety Status": 1,
    "Tool Acceleration": 3, "Norm of Cartesion Linear Momentum": 1,
    "Robot Current": 1, "Joint Voltages": 6, "Elbow Position": 3,
    "Elbow Velocity": 3, "Tool Current": 1, "Tool Temperature": 1,
    "TCP Force": 1, "Anomaly State": 1,
}

def stamp():
    return datetime.now(timezone.utc).isoformat()

def scan(path, expected_hash):
    started = time.monotonic()
    sha = hashlib.sha256()
    fields = {k: {"expected_width": n, "parsed_records": 0,
                   "shape_counts": collections.Counter(), "parse_errors": 0,
                   "empty_cells": 0, "non_numeric_elements": 0,
                   "nonfinite_elements": 0, "numeric_elements": 0,
                   "non_integral_scalar_records": 0,
                   "error_row_indices_first_10": []} for k,n in EXPECTED.items()}
    record_widths = collections.Counter()
    rows = 0
    with path.open("rb") as stream:
        def lines():
            for line in stream:
                sha.update(line)
                yield line.decode("utf-8")
        reader = csv.reader(lines())
        header = next(reader)
        assert header == list(EXPECTED), "Unexpected header"
        for row_index, row in enumerate(reader):
            rows += 1
            record_widths[len(row)] += 1
            if len(row) != len(header):
                continue
            for key, raw in zip(header, row):
                f = fields[key]
                if not raw.strip():
                    f["empty_cells"] += 1
                try:
                    value = json.loads(raw) if f["expected_width"] > 1 else float(raw)
                except (ValueError, json.JSONDecodeError):
                    f["parse_errors"] += 1
                    if len(f["error_row_indices_first_10"]) < 10:
                        f["error_row_indices_first_10"].append(row_index)
                    continue
                f["parsed_records"] += 1
                if f["expected_width"] > 1:
                    shape = "list:" + str(len(value)) if isinstance(value, list) else type(value).__name__
                    vals = value if isinstance(value, list) else [value]
                else:
                    shape, vals = "scalar", [value]
                    if math.isfinite(value) and not value.is_integer():
                        f["non_integral_scalar_records"] += 1
                f["shape_counts"][shape] += 1
                for value in vals:
                    if isinstance(value, bool) or not isinstance(value, (int, float)):
                        f["non_numeric_elements"] += 1
                    else:
                        f["numeric_elements"] += 1
                        f["nonfinite_elements"] += not math.isfinite(value)
            if rows % 200000 == 0:
                elapsed = time.monotonic() - started
                print(f"{path.name}: {rows} rows validated in {elapsed:.1f}s", flush=True)
    actual_hash = sha.hexdigest()
    assert actual_hash == expected_hash, "Received-byte hash changed from original receipt"
    issues = []
    if dict(record_widths) != {20:rows}:
        issues.append("record_width")
    for key, f in fields.items():
        expected_shape = "list:" + str(f["expected_width"]) if f["expected_width"] > 1 else "scalar"
        if dict(f["shape_counts"]) != {expected_shape:rows}:
            issues.append(key + ":shape")
        for metric in ("parse_errors", "empty_cells", "non_numeric_elements", "nonfinite_elements"):
            if f[metric]:
                issues.append(key + ":" + metric)
    return {"local_path":str(path.relative_to(PROJECT)), "bytes":path.stat().st_size,
            "sha256":actual_hash, "receipt_sha256_match":True, "rows":rows,
            "record_width_counts":dict(record_widths), "fields":fields,
            "structural_numeric_issues":issues, "elapsed_seconds":time.monotonic()-started}

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    receipt_path = PROJECT / "datasets/manifests/casper_v3_receipt.json"
    receipt_bytes = receipt_path.read_bytes()
    receipt = json.loads(receipt_bytes)
    result = {"audit_started_at_utc":stamp(),
              "command":"python3 manufacturing/scripts/audit_casper_controller_schema.py",
              "working_directory":". (repository root)", "python":sys.version,
              "platform":platform.platform(), "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "input_receipt_sha256":hashlib.sha256(receipt_bytes).hexdigest(),
              "scope":"Complete both-arm nested shape, numeric type, finiteness, byte identity; no model, plots, signal distribution or feature selection",
              "files":[]}
    for name in ("dataset/left_arm.csv", "dataset/right_arm.csv"):
        entry = next(f for f in receipt["files"] if f["archive_member"] == name)
        result["files"].append(scan(PROJECT / entry["local_path"], entry["sha256"]))
        (OUT / "controller_schema_profile.json").write_text(json.dumps(result,indent=2)+"\n")
    result["audit_completed_at_utc"] = stamp()
    (OUT / "controller_schema_profile.json").write_text(json.dumps(result,indent=2)+"\n")
    print("Full nested schema audit completed; original receipt and raw files unchanged.",flush=True)

if __name__ == "__main__":
    main()
