#!/usr/bin/env python3
"""Audit file correspondence without producing aligned training data or scores."""
import ast
import collections
import csv
import hashlib
import itertools
import json
from pathlib import Path
import struct
from datetime import datetime, timezone

PROJECT = Path(__file__).resolve().parents[1]
RAW = PROJECT / "datasets/raw/casper/v3/original"
OUT = PROJECT / "local/casper_v3_receipt/alignment_profile.json"

def main():
    result = {"started_at_utc": datetime.now(timezone.utc).isoformat(),
              "command": "python3 manufacturing/scripts/inspect_casper_alignment.py",
              "working_directory": ". (repository root)",
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "interpretation_limit": "Positional equality is not synchronized physical-time or causality evidence; no label alignment or model fitted."}
    with (RAW / "dataset/nicla.csv").open(newline="") as a, (RAW / "nicla_fixed.csv").open(newline="") as b:
        ra, rb = csv.reader(a), csv.reader(b)
        initial = list(itertools.islice(ra, 6))
        header = next(rb)
        assert header == ["AccX", "AccY", "AccZ", "GyroX", "GyroY", "GyroZ", "MagX", "MagY", "MagZ"]
        differences = text_differences = count = 0
        ah, bh = hashlib.sha256(), hashlib.sha256()
        for count, (r1, r2) in enumerate(itertools.zip_longest(ra, rb), 1):
            assert r1 is not None and r2 is not None, "Different numeric-row counts"
            assert len(r1) == len(r2) == 9
            f1, f2 = tuple(map(float, r1)), tuple(map(float, r2))
            differences += f1 != f2
            text_differences += r1 != r2
            ah.update(struct.pack("<9d", *f1))
            bh.update(struct.pack("<9d", *f2))
        result["nicla_correspondence"] = {
            "raw_initial_records_skipped": 6, "corrected_header": header,
            "numeric_rows_compared": count, "numeric_row_mismatches": differences,
            "textual_field_row_mismatches": text_differences,
            "canonicalization": "9 IEEE754 binary64 little-endian numbers per row; original row order; no values emitted",
            "raw_numeric_canonical_sha256": ah.hexdigest(), "corrected_numeric_canonical_sha256": bh.hexdigest(),
            "limit": "Establishes the measured correspondence of these received files, not the provider's undocumented generation history."}
    print("Nicla correspondence audit complete.", flush=True)
    offsets, label_mismatch, timestamps = collections.Counter(), 0, 0
    structures = collections.defaultdict(collections.Counter)
    with (RAW / "dataset/left_arm.csv").open(newline="") as a, (RAW / "dataset/right_arm.csv").open(newline="") as b:
        ra, rb = csv.reader(a), csv.reader(b)
        ha, hb = next(ra), next(rb)
        assert ha == hb
        ti, li = ha.index("Timestamp"), ha.index("Anomaly State")
        for count, (r1, r2) in enumerate(itertools.zip_longest(ra, rb), 1):
            assert r1 is not None and r2 is not None
            label_mismatch += r1[li] != r2[li]
            offsets[round(float(r2[ti]) - float(r1[ti]), 6)] += 1
            timestamps += 1
            if count <= 1000:
                for column, value in zip(ha, r2):
                    try:
                        item = ast.literal_eval(value)
                        key = type(item).__name__ + (":" + str(len(item)) if isinstance(item, (list, tuple)) else "")
                    except (ValueError, SyntaxError):
                        key = "unparsed"
                    structures[column][key] += 1
        result["arm_correspondence"] = {"rows_compared": timestamps,
            "positional_label_mismatch_count": label_mismatch,
            "right_minus_left_timestamp_rounded_6dp_counts": {str(k):v for k,v in sorted(offsets.items())},
            "right_arm_first_1000_record_field_shapes": {k:dict(v) for k,v in structures.items()},
            "limit": "Equal labels at equal row numbers do not establish clock synchronization. Bounded shape check does not validate all vector fields."}
    result["completed_at_utc"] = datetime.now(timezone.utc).isoformat()
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print("Arm clock/label correspondence audit complete.", flush=True)

if __name__ == "__main__":
    main()
