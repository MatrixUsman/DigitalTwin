#!/usr/bin/env python3
"""Static annotation/index audit; does not execute author code or generate labels.

Reads the frozen notebook and previously measured schema profile. Detailed
source-derived intervals stay in ignored local storage, not processed data.
"""
import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import re
import sys

PROJECT = Path(__file__).resolve().parents[1]
NOTEBOOK = PROJECT / "baselines/casper/artifacts/casper.ipynb"
PROFILE = PROJECT / "local/casper_v3_receipt/schema_profile.json"
RECEIPT = PROJECT / "datasets/manifests/casper_v3_receipt.json"
OUTPUT = PROJECT / "local/casper_annotation_study/annotation_lineage.json"
REVISION = "bff03c91d155bf3134f6d801d3a4f4af7ea78adb"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def source(cells, index):
    return "".join(cells[index]["source"])


def intervals_from_cell(code):
    intervals = []
    for node in ast.parse(code).body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if (isinstance(target, ast.Subscript)
                and isinstance(target.value, ast.Name)
                and target.value.id == "nicla_labels"):
            require(isinstance(target.slice, ast.Slice), "Expected a slice")
            require(target.slice.step is None, "Unexpected annotation step")
            require(ast.literal_eval(node.value) == 1, "Unexpected label value")
            intervals.append([ast.literal_eval(target.slice.lower),
                              ast.literal_eval(target.slice.upper)])
    return intervals


def main():
    started = datetime.now(timezone.utc).isoformat()
    cells = json.loads(NOTEBOOK.read_text())["cells"]
    profile = json.loads(PROFILE.read_text())
    receipt = json.loads(RECEIPT.read_text())
    require(digest(NOTEBOOK) == receipt["source_notebook"]["sha256"],
            "Notebook differs from the pinned receipt copy")
    require(receipt["source_notebook"]["revision"] == REVISION, "Revision changed")
    # Refuse to extrapolate if the inspected source operations change.
    expected = {
        2: "skiprows=6", 8: "nicla.iloc[897:]",
        21: "nicla_dropped.rolling(f_window_size).median().dropna().to_numpy()",
        25: "nicla_filtered[:1072450]", 81: "shuffle=False",
        82: "WINDOW_SIZE = 755", 89: "nicla_anol[755:]",
        92: "np.convolve(rmse_per_row, np.ones(window_size), 'valid')",
        95: "> (755 / 2)",
    }
    for index, token in expected.items():
        require(token in source(cells, index), f"Source changed at cell {index}")
    require(re.search(r"f_window_size\s*=\s*20\b", source(cells, 21)),
            "Median width changed")
    require(re.search(r"window_size\s*=\s*755\b", source(cells, 92)),
            "Score width changed")
    imu_profile = profile["files"]["dataset/nicla.csv"]
    for count_key in ("nine_field_nonnumeric_records", "nine_field_nonfinite_records"):
        require(imu_profile[count_key] == 0, "Unexpected invalid IMU values")
    rows = imu_profile["data_records_after_skip"]
    require(imu_profile["record_width_counts"] == {"9": rows},
            "Unexpected IMU row widths; dropna arithmetic would be unsafe")
    trim, median, prediction, aggregation = 897, 20, 755, 755
    offset = trim + median - 1
    filtered_rows = rows - offset
    intervals = intervals_from_cell(source(cells, 23))
    require(len(intervals) == 8, "Expected eight upstream annotation intervals")
    prior_end = 0
    for start, end in intervals:
        require(prior_end <= start < end <= filtered_rows, "Invalid intervals")
        prior_end = end
    split = intervals[0][0]
    require(split == 1072450, "Normal-prefix source boundary changed")
    mixed_rows = filtered_rows - split
    residual_rows = mixed_rows - prediction
    scores_if_executed = residual_rows - aggregation + 1
    filtered_support = prediction + aggregation
    raw_support = filtered_support + median - 1
    # Independent set-union checks on synthetic indices, not sensor samples.
    first_support = set()
    for residual_index in range(aggregation):
        for filtered_index in range(residual_index, residual_index + prediction + 1):
            first_support.update(range(filtered_index, filtered_index + median))
    require(first_support == set(range(raw_support)), "Support derivation failed")
    require(len(first_support) == 1529, "Unexpected complete input support")
    # Derive label-class totals from the eight published slices only. This
    # computes no predictions or accuracy and does not inspect sensor values.
    positive_score_targets = 0
    for j in range(scores_if_executed):
        start = split + prediction + j
        end = start + aggregation
        positives = sum(max(0, min(end, b) - max(start, a)) for a, b in intervals)
        positive_score_targets += positives > aggregation / 2
    arm = profile["files"]["dataset/right_arm.csv"]
    arm_events = [r for r in arm["label_runs_zero_based_half_open"] if str(r["label"]) == "1"]
    require(len(arm_events) == 8, "Unexpected controller event inventory")
    annotations = []
    for ordinal, (start, end) in enumerate(intervals, 1):
        annotations.append({
            "event_ordinal": ordinal,
            "filtered_endpoint_index_half_open": [start, end],
            "raw_numeric_endpoint_index_half_open": [start + offset, end + offset],
            "original_csv_endpoint_record_one_based_half_open": [start + offset + 7, end + offset + 7],
            "raw_numeric_support_union_half_open": [start + trim, end + offset],
            "labelled_filtered_rows": end - start,
            "status": "upstream_retrospective_manual_annotation_not_independent_ground_truth",
        })
    result = {
        "audit_type": "static_index_lineage_not_model_evaluation",
        "started_at_utc": started,
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "command": "python3 manufacturing/scripts/audit_casper_annotation_lineage.py",
        "working_directory": str(PROJECT.parent),
        "python": sys.version, "platform": platform.platform(),
        "script_sha256": digest(Path(__file__)),
        "source_notebook": {"revision": REVISION, "sha256": digest(NOTEBOOK),
                            "url": f"https://github.com/hkayann/1D-CNN-Anomaly-Detection-via-CASPER/blob/{REVISION}/notebooks/casper.ipynb"},
        "input_profile_sha256": digest(PROFILE),
        "input_receipt_sha256": digest(RECEIPT),
        "raw_inputs": [f for f in receipt["files"] if f["archive_member"] in
                       ("dataset/nicla.csv", "dataset/right_arm.csv")],
        "index_convention": "zero-based half-open except explicit CSV record numbers; no physical-time conversion",
        "source_operations": {"startup_csv_records_skipped": 6,
                              "numeric_rows_trimmed": trim, "trailing_median_width": median,
                              "filtered_to_raw_numeric_endpoint_offset": offset},
        "counts_derived_from_source_not_executed_pipeline": {
            "raw_numeric_rows_measured_previously": rows,
            "after_trim": rows - trim, "after_median_dropna": filtered_rows,
            "upstream_normal_prefix": split, "mixed_segment": mixed_rows,
            "manually_positive_filtered_rows": sum(b - a for a, b in intervals),
            "cnn_residuals_if_executed": residual_rows,
            "aggregated_scores_if_executed": scores_if_executed,
            "upstream_majority_positive_targets": positive_score_targets,
            "upstream_majority_negative_targets": scores_if_executed - positive_score_targets},
        "annotations": annotations,
        "clock_alignment": "unresolved; corresponding event ordinal does not establish synchronized rows or onset",
        "paper_code_discrepancy": {"notebook_markdown_final_end": 1716456,
                                   "notebook_executable_slice_final_end": intervals[-1][1],
                                   "difference_samples": 1716456 - intervals[-1][1]},
        "score_support": {"prediction_history_filtered_rows": prediction,
                          "residual_aggregation_rows": aggregation,
                          "complete_filtered_span": filtered_support,
                          "complete_raw_span": raw_support,
                          "first_endpoint_in_mixed_filtered_coordinates": filtered_support - 1,
                          "majority_positive_required": aggregation // 2 + 1,
                          "raw_overlap_across_prefiltered_partition_boundary": median - 1,
                          "checked_with": "synthetic index-set union only"},
        "limits": ["No filters, detector, threshold or upstream notebook executed.",
                   "No new labels or processed training files produced.",
                   "Endpoint lineage is bookkeeping, not evidence that every supporting raw row is anomalous.",
                   "Global prefiltering leaves 19 rows of support overlap at subsequent splits; proposed protocol resets preprocessing.",
                   "Retrospective annotations depend on an observed IMU channel; accuracy and real-time onset are not independently validated."]}
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"output": str(OUTPUT.relative_to(PROJECT)),
                      "sha256": digest(OUTPUT),
                      "derived_counts": result["counts_derived_from_source_not_executed_pipeline"],
                      "raw_support": raw_support,
                      "annotation_intervals": len(annotations)}, indent=2))


if __name__ == "__main__":
    main()
