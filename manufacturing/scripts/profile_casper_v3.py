#!/usr/bin/env python3
"""Read-only, streaming CASPER schema/clock/label audit. No model or scores.

Outputs contain structural metadata, not sensor/network contents. Label intervals
are annotation inventory only and must never be used to tune the final detector.
"""
import collections
import csv
import hashlib
import itertools
import json
import math
from pathlib import Path
import platform
import sys
from datetime import datetime, timezone

PROJECT = Path(__file__).resolve().parents[1]
RAW = PROJECT / "datasets/raw/casper/v3/original"
OUT = PROJECT / "local/casper_v3_receipt/schema_profile.json"

def finite_number(value):
    try:
        return math.isfinite(float(value))
    except ValueError:
        return False

def preview(path):
    with path.open(newline="", encoding="utf-8-sig") as stream:
        rows = list(itertools.islice(csv.reader(stream), 10))
    return [{"physical_record_1based": i + 1, "fields": len(row),
             "finite_numeric_fields": sum(finite_number(v) for v in row)}
            for i, row in enumerate(rows)]

def arm(path):
    widths, labels, deltas = collections.Counter(), collections.Counter(), collections.Counter()
    invalid_t = invalid_label = negative = duplicate = blank_rows = 0
    previous = first_t = last_t = min_t = max_t = None
    intervals, current = [], None
    with path.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.reader(stream)
        header = next(reader)
        ti, li = header.index("Timestamp"), header.index("Anomaly State")
        for i, row in enumerate(reader):
            widths[len(row)] += 1
            if not row:
                blank_rows += 1
            if len(row) != len(header):
                if current:
                    current["end_row_exclusive"] = i
                    intervals.append(current)
                    current = None
                previous = None
                continue
            label = row[li]
            labels[label] += 1
            if label not in ("0", "1", "0.0", "1.0"):
                invalid_label += 1
            if current is None or current["label"] != label:
                if current:
                    current["end_row_exclusive"] = i
                    intervals.append(current)
                current = {"label": label, "start_row_inclusive": i}
            if finite_number(row[ti]):
                t = float(row[ti])
                first_t = t if first_t is None else first_t
                last_t = t
                min_t = t if min_t is None else min(t, min_t)
                max_t = t if max_t is None else max(t, max_t)
                if previous is not None:
                    delta = t - previous
                    negative += delta < 0
                    duplicate += delta == 0
                    deltas[round(delta, 6)] += 1
                previous = t
            else:
                invalid_t += 1
                previous = None
        n = sum(widths.values())
        if current:
            current["end_row_exclusive"] = n
            intervals.append(current)
    return {"file": str(path.relative_to(PROJECT)), "header": header,
            "header_fields": len(header), "duplicate_header_names": [k for k,v in collections.Counter(header).items() if v>1],
            "data_records_including_malformed": n, "record_width_counts": dict(widths),
            "blank_records": blank_rows, "label_column": "Anomaly State", "label_counts": dict(labels),
            "unrecognized_label_records": invalid_label, "label_runs_zero_based_half_open": intervals,
            "timestamp_column": "Timestamp", "timestamp_first": first_t, "timestamp_last": last_t,
            "timestamp_min": min_t, "timestamp_max": max_t, "invalid_timestamp_records": invalid_t,
            "timestamp_negative_steps": negative, "timestamp_duplicate_steps": duplicate,
            "timestamp_delta_rounded_6dp_counts": {str(k):v for k,v in sorted(deltas.items())},
            "timestamp_units_status": "not inferred from numerical magnitude; reconcile writer/provider documentation",
            "feature_validation_limit": "Only field width, Timestamp and Anomaly State parsed; other feature semantics/finite values not validated."}

def nicla(path, skip_records):
    widths = collections.Counter()
    bad_numeric = nonfinite = 0
    bad_examples = []
    with path.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.reader(stream)
        skipped = list(itertools.islice(reader, skip_records))
        for i, row in enumerate(reader):
            widths[len(row)] += 1
            if len(row) != 9:
                if len(bad_examples) < 10:
                    bad_examples.append(i + skip_records + 1)
                continue
            try:
                values = [float(v) for v in row]
            except ValueError:
                bad_numeric += 1
                if len(bad_examples) < 10:
                    bad_examples.append(i + skip_records + 1)
                continue
            nonfinite += not all(math.isfinite(v) for v in values)
    return {"file": str(path.relative_to(PROJECT)), "skipped_initial_records_for_this_audit": skip_records,
            "skipped_record_widths": [len(r) for r in skipped],
            "header": skipped[0] if skip_records == 1 else None,
            "data_records_after_skip": sum(widths.values()), "record_width_counts": dict(widths),
            "nine_field_nonnumeric_records": bad_numeric, "nine_field_nonfinite_records": nonfinite,
            "first_structurally_invalid_physical_record_numbers": bad_examples,
            "column_mapping_source": "Original author notebook supplies nine names for raw nicla.csv; nicla_fixed.csv has the same names in its received header",
            "timestamp_and_label_columns": "No timestamp or anomaly label included in the nine-field records examined"}

def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    results = {"audit_started_at_utc": datetime.now(timezone.utc).isoformat(),
               "command": "python3 manufacturing/scripts/profile_casper_v3.py",
               "working_directory": ". (repository root)",
               "python": sys.version, "platform": platform.platform(),
               "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               "scope": "Complete streaming CSV structural, clock and label inventory; no signal distributions, models, metrics, threshold selection or PCAP decoding",
               "files": {}}
    for name in ("dataset/left_arm.csv", "dataset/right_arm.csv", "dataset/nicla.csv", "nicla_fixed.csv"):
        p = RAW / name
        print("Profiling " + name, flush=True)
        beginning = preview(p)
        if "arm.csv" in name:
            record = arm(p)
        else:
            # Raw-six-row skip is documented in the pinned author notebook.
            # Corrected-file header was directly inspected before this final audit.
            record = nicla(p, 6 if name == "dataset/nicla.csv" else 1)
        record["first_ten_record_structure"] = beginning
        results["files"][name] = record
        OUT.write_text(json.dumps(results, indent=2) + "\n")
        print("Completed " + name, flush=True)
    results["audit_completed_at_utc"] = datetime.now(timezone.utc).isoformat()
    OUT.write_text(json.dumps(results, indent=2) + "\n")
    print("Read-only schema audit complete.", flush=True)

if __name__ == "__main__":
    main()
