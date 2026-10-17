"""Frozen artifact admission, threshold-only calibration and sealed evaluation.

No fitting or configuration selection occurs here. Production entry points
bind this module to a pre-calibration freeze, tested source inventory, exact
source bytes and one-attempt ledger. Pure/synthetic helpers accept test inputs.
"""
from __future__ import annotations

from array import array
from dataclasses import asdict
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import json
import math
from pathlib import Path
import sys
import time

from .campaign_data import delayed_labels, verified_features
from .campaign_models import FrozenRoster, METHODS
from .contract import ContractError, LoadStats
from .metrics import Event, ScoredPoint, calibrate, evaluate

CONFIG = "configs/casper_right_arm_campaign_v0.1.json"
CHOICES = "experiments/MODEL_SELECTION_FREEZE_V0.1.json"
FINAL = "experiments/FINAL_TEST_FREEZE_RECORD.json"


def utc():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def bound(root, relative):
    path = (Path(root) / relative).resolve()
    if not path.is_relative_to(Path(root).resolve()):
        raise ContractError("Campaign reference escapes project")
    return path


def read_ref(root, reference):
    path = bound(root, reference["path"])
    if sha(path) != reference["sha256"]:
        raise ContractError("Frozen reference changed: " + reference["path"])
    return path


def file_ref(root, path):
    path = Path(path).resolve()
    return {"path": str(path.relative_to(Path(root).resolve())), "sha256": sha(path), "bytes": path.stat().st_size}


def verify_choices(root):
    """Metadata/saved artifacts only: neither calibration nor final raw open."""
    freeze = json.loads(bound(root, CHOICES).read_text())
    if (freeze.get("status") != "frozen_before_calibration" or tuple(freeze.get("methods", ())) != METHODS
            or freeze.get("fit_allowed") is not False or freeze.get("calibration_observations_seen") is not False
            or freeze.get("deterministic_runs_each") != 1 or freeze.get("stochastic_runs") != []):
        raise ContractError("Incomplete model-selection freeze")
    for relative, expected in freeze["source_sha256"].items():
        read_ref(root, {"path": relative, "sha256": expected})
    for reference in freeze["inputs"]:
        read_ref(root, reference)
    for reference in freeze["provenance_files"].values():
        read_ref(root, reference)
    config = json.loads(read_ref(root, freeze["configuration"]).read_text())
    if (tuple(config["methods"]) != METHODS or config["calibration"] != {
            "partition": "normal_calibration", "count": 160473, "rank": 158869,
            "quantile": "99/100 nearest rank", "alarm": "score > threshold"}):
        raise ContractError("Unsupported campaign scientific configuration")
    models = {key: json.loads(read_ref(root, ref).read_text()) for key, ref in freeze["fitted_artifacts"].items()}
    roster = FrozenRoster(models)
    if roster.config.initialization != 1528 or roster.reference.n != 536946:
        raise ContractError("Unexpected production model support/history")
    return freeze, config, models


def write_scores(writer, values):
    references = {}
    for name in METHODS:
        scores = values[name]
        if scores.itemsize != 8:
            raise ContractError("binary64 array unavailable")
        payload = array("d", scores)
        if sys.byteorder != "little":
            payload.byteswap()
        path = writer.write_bytes(name + ".scores.f64", payload.tobytes())
        references[name] = {"path": path.name, "sha256": sha(path), "count": len(scores), "bytes": path.stat().st_size}
    return references


def read_scores(directory, reference, expected_count):
    path = read_ref(directory, reference)
    if path.stat().st_size != expected_count * 8 or reference["count"] != expected_count:
        raise ContractError("Score byte/count mismatch")
    values = array("d")
    values.frombytes(path.read_bytes())
    if sys.byteorder != "little":
        values.byteswap()
    if len(values) != expected_count or any(not math.isfinite(v) or v < 0 for v in values):
        raise ContractError("Incomplete/nonfinite/negative score support")
    return values


def read_index(directory, seal, study):
    """Check every raw coordinate, common warmup and observed gap/reset."""
    spec = study.partition(seal["partition"])
    path = read_ref(directory, seal["index"])
    expected = study.expected_eligible_rows(spec.name)
    next_eligible = next(expected, None)
    output = []
    previous, preceding, segment = None, 0, -1
    with path.open() as handle:
        for row, line in enumerate(handle, start=spec.start):
            value = json.loads(line)
            if (len(value) != 4 or type(value[0]) is not int or value[0] != row or row >= spec.end
                    or type(value[2]) is not int or type(value[3]) is not bool):
                raise ContractError("Invalid/reordered/duplicate index coordinate")
            timestamp = Decimal(value[1])
            if not timestamp.is_finite():
                raise ContractError("Nonfinite index time")
            from .data import _native_delta
            dt = None if previous is None else _native_delta(timestamp, previous)
            if dt is None or dt <= 0 or dt > spec.gap_seconds:
                preceding, segment = 0, segment + 1
            eligible = preceding >= spec.warmup
            if value[2] != segment or value[3] != eligible or eligible != (row == next_eligible):
                raise ContractError("Index segment/eligibility differs from independent mask")
            if eligible:
                next_eligible = next(expected, None)
            output.append((row, timestamp, segment, eligible))
            previous, preceding = timestamp, preceding + 1
    if len(output) != spec.expected_rows or next_eligible is not None:
        raise ContractError("Incomplete index")
    return output


def validate_seal(directory, study, *, partition, choice_hash):
    """All declared score streams must be complete before ANY label access."""
    directory = Path(directory)
    seal = json.loads((directory / "score_seal.json").read_text())
    if (seal.get("status") != "complete_all_declared_scores_no_labels"
            or seal.get("partition") != partition or seal.get("model_selection_sha256") != choice_hash
            or seal.get("source_sha256") != study.source_sha256
            or tuple(seal.get("methods", ())) != METHODS or set(seal.get("scores", {})) != set(METHODS)
            or seal.get("format") != "little-endian IEEE754 binary64"
            or seal.get("labels_parsed") is not False):
        raise ContractError("Invalid/incomplete score seal")
    index = read_index(directory, seal, study)
    count = sum(v[3] for v in index)
    if seal["eligible_count"] != count:
        raise ContractError("Sealed count differs from index")
    for name in METHODS:
        read_scores(directory, seal["scores"][name], count)
    return seal, index


def run_scoring(study, models, writer, diagnostics, *, partition, choice_hash):
    """Stream permitted features once; persist every declared stream together."""
    roster = FrozenRoster(models)
    stats = LoadStats()
    diagnostics.update(stage=partition + "_label_free_replay", load_stats={}, fit_calls=0, labels_parsed=False)
    arrays = {name: array("d") for name in METHODS}
    index_buffer = []
    writer.write_text("index.jsonl", "")
    started = time.perf_counter()
    try:
        for record in verified_features(study, partition, stats):
            scores = roster.step(record.observation, record.eligible)
            if (tuple(scores) != (METHODS if record.eligible else ())
                    or any(type(v) not in (int, float) or not math.isfinite(v) or v < 0 for v in scores.values())):
                raise ContractError("Invalid score vector before sealing")
            for name, score in scores.items():
                arrays[name].append(score)
            index_buffer.append(json.dumps([record.row, str(record.timestamp), record.segment, record.eligible], separators=(",", ":")) + "\n")
            if len(index_buffer) >= 1000:
                writer.append_text("index.jsonl", "".join(index_buffer))
                index_buffer.clear()
            if stats.selected_rows_parsed % 10000 == 0:
                writer.append_text("progress.jsonl", json.dumps({"stage": diagnostics["stage"],
                    "parsed": stats.selected_rows_parsed, "eligible": len(arrays[METHODS[0]]),
                    "elapsed_seconds": time.perf_counter() - started}) + "\n")
        if index_buffer:
            writer.append_text("index.jsonl", "".join(index_buffer))
        roster.verify_unchanged()
        count = sum(1 for _ in study.expected_eligible_rows(partition))
        if not stats.stream_checks_completed or any(len(a) != count for a in arrays.values()):
            raise ContractError("Incomplete campaign population")
        scores = write_scores(writer, arrays)
        seal = {"status": "complete_all_declared_scores_no_labels", "created_at_utc": utc(),
            "partition": partition, "model_selection_sha256": choice_hash, "source_sha256": study.source_sha256,
            "methods": list(METHODS), "scores": scores, "eligible_count": count,
            "format": "little-endian IEEE754 binary64", "labels_parsed": False,
            "index": {"path": "index.jsonl", "sha256": sha(writer.output_dir / "index.jsonl")},
            "fitted_parameters_unchanged": True, "fit_calls": 0}
        writer.write_json("score_seal.json", seal)
        if partition == "normal_calibration":
            thresholds = {name: asdict(calibrate(values, expected_m=count)) for name, values in arrays.items()}
            writer.write_json("calibration.json", {"status": "thresholds_only", "model_selection_sha256": choice_hash,
                "score_seal_sha256": sha(writer.output_dir / "score_seal.json"), "created_at_utc": utc(),
                "alarm": "score > threshold", "quantile": "99/100 nearest rank", "thresholds": thresholds,
                "selection_performed": False, "future_false_alarm_guarantee": False})
        diagnostics.update(status="completed", stage="scores_sealed", eligible_count=count,
            fitted_parameters_unchanged=True, final_features_parsed=partition == "final_replay")
    finally:
        diagnostics["load_stats"] = asdict(stats)
        diagnostics["final_features_parsed"] = partition == "final_replay" and stats.selected_rows_parsed > 0


def validate_calibration(directory, study, choice_hash):
    seal, index = validate_seal(directory, study, partition="normal_calibration", choice_hash=choice_hash)
    receipt = json.loads((Path(directory) / "calibration.json").read_text())
    if (receipt.get("status") != "thresholds_only" or receipt.get("model_selection_sha256") != choice_hash
            or receipt.get("score_seal_sha256") != sha(Path(directory) / "score_seal.json")
            or receipt.get("alarm") != "score > threshold" or receipt.get("quantile") != "99/100 nearest rank"
            or receipt.get("selection_performed") is not False
            or set(receipt.get("thresholds", {})) != set(METHODS)):
        raise ContractError("Invalid calibration receipt")
    count = sum(v[3] for v in index)
    for name in METHODS:
        expected = asdict(calibrate(read_scores(directory, seal["scores"][name], count), expected_m=count))
        if receipt["thresholds"][name] != expected:
            raise ContractError("Calibration threshold/rank/count differs from sealed scores")
    return receipt


def accepted_run(root, ref, phase, choice_hash):
    path = read_ref(root, ref)
    run = json.loads(path.read_text())
    if (run.get("accepted") is not True or run.get("phase") != phase
            or run.get("model_selection_sha256") != choice_hash or run.get("status") != "completed"):
        raise ContractError("Run was not completely admitted")
    expected = [{"method": m, "seed": None, "replicate": 1, "status": "completed"} for m in METHODS]
    if run.get("run_matrix") != expected:
        raise ContractError("Accepted run matrix omits or changes a declared method")
    for name, item in run["artifacts"].items():
        read_ref(path.parent, dict(item, path=name))
    return path.parent, run


def verify_final(root, study):
    freeze, config, models = verify_choices(root)
    final = json.loads(bound(root, FINAL).read_text())
    choice_hash = sha(bound(root, CHOICES))
    if (final.get("status") != "ready_for_final_execution_not_executed"
            or final.get("model_selection_record", {}).get("sha256") != choice_hash
            or final.get("campaign_started_at") is not None or final.get("first_outcome_revealed_at") is not None
            or final.get("methods") != list(METHODS)):
        raise ContractError("Final campaign freeze missing or inconsistent")
    read_ref(root, final["model_selection_record"])
    directory, _ = accepted_run(root, final["calibration_run"], "calibrate", choice_hash)
    calibration = validate_calibration(directory, study, choice_hash)
    if any(v["count"] != 160473 or v["rank"] != 158869 for v in calibration["thresholds"].values()):
        raise ContractError("Wrong production calibration population/rank")
    if final.get("thresholds") != calibration["thresholds"]:
        raise ContractError("Final thresholds differ from calibration")
    expected_matrix = [{"method": name, "seed": None, "replicate": 1, "stochastic": False,
                        "calibration_status": "valid", "final_status": "not_started"} for name in METHODS]
    if final.get("declared_run_matrix") != expected_matrix:
        raise ContractError("Incomplete/changed declared run matrix")
    for key in ("fitted_artifacts", "execution_commands", "budgets"):
        if final.get(key) != freeze[key]:
            raise ContractError("Final record differs from selection freeze: " + key)
    if final.get("mask_artifact") != freeze["provenance_files"]["mask.json"]:
        raise ContractError("Final mask binding differs")
    return final, freeze, config, models


def run_evaluation(study, score_dir, thresholds, writer, diagnostics, *, choice_hash, policy, events):
    """Delayed join, after full seal admission; every method, no best-run choice."""
    seal, index = validate_seal(score_dir, study, partition="final_replay", choice_hash=choice_hash)
    if set(thresholds) != set(METHODS) or any(type(v.get("threshold")) not in (int, float)
            or not math.isfinite(v["threshold"]) for v in thresholds.values()):
        raise ContractError("Incomplete frozen thresholds before label join")
    stats = LoadStats()
    diagnostics.update(stage="delayed_label_join", scores_verified_before_labels=True)
    # This is the first operation in this function which can interpret labels.
    writer.append_text("access.jsonl", json.dumps({"time": utc(), "event": "label_join_started",
        "all_score_files_verified": True, "score_seal_sha256": sha(Path(score_dir) / "score_seal.json")}) + "\n")
    try:
        labels = delayed_labels(study, index, stats)
        spec = study.partition("final_replay")
        ranges = {name: tuple(policy["populations"][name]["rows_half_open"])
                  for name in ("held_out_normal", "mixed_final")}
        # Every scheduled-zero inter-event/recovery interval is reported separately.
        cursor = ranges["mixed_final"][0]
        for number, event in enumerate(events, 1):
            if cursor < event.start:
                ranges[f"scheduled_zero_before_event_{number}"] = (cursor, event.start)
            cursor = event.end
        if cursor < spec.end:
            ranges["scheduled_zero_after_last_event"] = (cursor, spec.end)
        if sum(labels) != sum(e.end - e.start for e in events):
            raise ContractError("Final label totals differ from frozen annotation")
        for name in METHODS:
            diagnostics["stage"] = "metrics_" + name
            values = iter(read_scores(score_dir, seal["scores"][name], seal["eligible_count"]))
            points = (ScoredPoint(row, timestamp, label, eligible, next(values) if eligible else None, segment)
                      for (row, timestamp, segment, eligible), label in zip(index, labels, strict=True))
            report = evaluate(points, expected_domain=(spec.start, spec.end),
                expected_eligible_rows=study.expected_eligible_rows("final_replay"),
                threshold=thresholds[name]["threshold"], reporting_ranges=ranges, events=events)
            # No labels/outcomes are printed; run artifacts remain local. The
            # first metrics artifact is nevertheless an outcome exposure record.
            writer.append_text("access.jsonl", json.dumps({"time": utc(), "event": "outcome_artifact_written", "method": name}) + "\n")
            # Episode IDs/coordinates are reconstructible from sealed scores.
            # Keep mandatory counts/censoring/delays without duplicating a
            # potentially row-sized episode table in eleven JSON reports.
            result = {"expected_domain": report.expected_domain, "threshold": report.threshold,
                      "coverage": asdict(report.coverage), "slices": [],
                      "events": asdict(report.events), "global_episode_count": len(report.episodes),
                      "episode_detail": "Reconstruct from sealed index/scores with this frozen metric implementation"}
            for item in report.slices:
                summary = asdict(item)
                del summary["episode_ids"]
                result["slices"].append(summary)
            for event in result["events"]["outcomes"]:
                event["overlapping_episode_count"] = len(event.pop("episode_ids"))
            writer.write_text(name + ".metrics.json", json.dumps(result, default=str, allow_nan=False) + "\n")
            del report
        left = json.loads((writer.output_dir / "O-RC.metrics.json").read_text())
        right = json.loads((writer.output_dir / "O-R.metrics.json").read_text())
        def difference(a, b):
            return None if a is None or b is None else a - b
        writer.write_json("paired_contrast.json", {"contrast": "O-RC minus O-R", "seed": None,
            "mixed_F1_difference": difference(left["slices"][1]["points"]["f1"], right["slices"][1]["points"]["f1"]),
            "normal_point_exceedance_difference": difference(left["slices"][0]["points"]["point_exceedance"], right["slices"][0]["points"]["point_exceedance"]),
            "normal_episodes_per_hour_difference": difference(left["slices"][0]["episodes_per_hour"], right["slices"][0]["episodes_per_hour"]),
            "eligible_coverage_difference": difference(left["coverage"]["eligible_coverage"],right["coverage"]["eligible_coverage"]),
            "interpretation": "Joint descriptive effects; no composite winner or independent-acquisition inference"})
        diagnostics.update(status="completed", stage="all_declared_metrics_complete", labels_joined=len(labels),
                           report_interpretation="single_acquisition_schedule_agreement_not_cyber_generalization")
    finally:
        diagnostics["label_load_stats"] = asdict(stats)
        diagnostics["label_rows_traversed_for_join"] = stats.selected_rows_parsed
