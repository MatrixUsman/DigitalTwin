"""One fixed normal-only feasibility pilot; no calibration or final runner.

The public entry point binds the exact pilot plan. ``run_pilot`` also accepts
explicitly synthetic studies for offline integration tests. It is not an access
control boundary against arbitrary Python code or direct filesystem access.
"""
from __future__ import annotations

import hashlib
import json
import math
import time
from collections import Counter
from dataclasses import asdict
from decimal import Decimal
from pathlib import Path

from .contract import ContractError, LoadStats, Study, iter_development_records
from .velocity import VelocityDetector, VelocityReference, fit_velocity

PILOT_PATH = "configs/casper_right_arm_pilot_v0.1.json"
PILOT_SHA256 = "5df7c1e6f279aebe482099fe9dfeaeba1eb241df47ce9a93137fbfcbb95870dc"


def load_pilot_plan(root: Path) -> dict:
    payload = (root / PILOT_PATH).read_bytes()
    if hashlib.sha256(payload).hexdigest() != PILOT_SHA256:
        raise ContractError("Pilot specification changed; no implicit admission")
    return json.loads(payload)


def reference_digest(reference) -> str:
    return hashlib.sha256(json.dumps(reference.to_dict(), sort_keys=True,
                                     allow_nan=False).encode()).hexdigest()


def last_progress(run_dir: Path) -> dict | None:
    """Recover only complete count-only records after abrupt worker termination."""
    path = run_dir / "progress.jsonl"
    if not path.exists():
        return None
    last = None
    with path.open() as handle:
        for line in handle:
            try:
                last = json.loads(line)
            except json.JSONDecodeError:
                break
    return last


def validate_run_artifacts(run_dir: Path, plan: dict) -> dict:
    """Independently read back saved normal-only artifacts, never the raw CSV."""
    saved = json.loads((run_dir / "reference.json").read_text())
    state = saved["reference"]
    reference = VelocityReference(state["n"], tuple(state["mean"]),
                                  tuple(state["variance"]), tuple(state["sigma"]))
    if (reference.n != plan["access"]["fit"]["expected_eligible_rows"]
            or reference_digest(reference) != saved["state_sha256"]):
        raise ContractError("Saved reference identity/count mismatch")
    expected = iter(row for a, b in plan["access"]["check_scores"]["eligible_intervals_half_open"]
                    for row in range(a, b))
    count = 0
    with (run_dir / "development_scores.jsonl").open() as handle:
        for line in handle:
            item = json.loads(line)
            row = next(expected, None)
            if (set(item) != {"row", "timestamp", "segment", "score"}
                    or type(item["row"]) is not int or item["row"] != row
                    or type(item["score"]) not in (int, float) or not math.isfinite(item["score"])
                    or not Decimal(item["timestamp"]).is_finite()):
                raise ContractError("Invalid, missing, duplicated or reordered saved score")
            count += 1
    if next(expected, None) is not None or count != plan["access"]["check_scores"]["expected_eligible_rows"]:
        raise ContractError("Incomplete saved scores")
    return {"saved_reference_valid": True, "saved_score_count": count,
            "missing": 0, "duplicate_or_reordered": 0, "nonfinite": 0}


def run_pilot(study: Study, plan: dict, writer, diagnostics: dict) -> None:
    """Fit once and score once, fully exhausting both declared prefix streams.

    Only ``Observation`` reaches the control. Alignment and mask checks are
    outside the model. No labels, threshold, score ranking or attack metrics are
    consumed here. On failure the caller persists this partially filled ledger.
    """
    started = time.perf_counter()
    load_stats = {name: LoadStats() for name in ("fit", "check_scores")}
    populations = {}
    diagnostics.update(status="running", stage="fit", populations=populations,
                       timing_seconds={}, reference_unchanged=None)

    def progress():
        writer.append_text("progress.jsonl", json.dumps({
            "stage": diagnostics["stage"], "elapsed_seconds": time.perf_counter()-started,
            "last_completed_score_writes": diagnostics.get("score_count", 0),
            "completed_fit_count": diagnostics.get("fit_count"),
            "selected_input_rows_parsed": {name: stats.selected_rows_parsed for name, stats in load_stats.items()},
            "eligible_input_rows_offered": {name: values["eligible_rows"] for name, values in populations.items()},
            "coverage_is_last_known_not_terminal": True,
        }, allow_nan=False, separators=(",", ":")) + "\n")

    def records(name):
        scope = plan["access"][name]
        partition = scope["parent_partition"]
        start, stop = scope["rows_half_open"]
        if start != study.partition(partition).start:
            raise ContractError("Pilot cannot move the parent partition start")
        stats = load_stats[name]
        summary = populations[name] = {
            "raw_rows_yielded": 0, "eligible_rows": 0, "exclusions": {},
            "segment_start_rows": [], "loader_advance_seconds": 0.0,
            "source_checks_completed": False,
        }
        expected_rows = iter(row for a, b in scope["eligible_intervals_half_open"]
                             for row in range(a, b))
        expected_eligible = next(expected_rows, None)
        exclusions = Counter()
        stream = iter(iter_development_records(study, partition, stop=stop, stats=stats))
        try:
            while True:
                tick = time.perf_counter()
                try:
                    record = next(stream)
                except StopIteration:
                    break
                finally:
                    summary["loader_advance_seconds"] += time.perf_counter() - tick
                if record.row != start + summary["raw_rows_yielded"]:
                    raise ContractError("Missing, duplicate or reordered pilot row")
                summary["raw_rows_yielded"] += 1
                if record.eligible != (record.row == expected_eligible):
                    raise ContractError("Pilot endpoint mask mismatch")
                if record.eligible:
                    summary["eligible_rows"] += 1
                    expected_eligible = next(expected_rows, None)
                else:
                    exclusions[record.exclusion] += 1
                    summary["exclusions"] = dict(exclusions)
                if record.observation is None:
                    raise ContractError("Invalid pilot observation")
                if record.observation.dt is None:
                    summary["segment_start_rows"].append(record.row)
                if summary["raw_rows_yielded"] % 1000 == 0:
                    progress()
                yield record
            if (summary["raw_rows_yielded"] != scope["raw_rows"]
                    or summary["eligible_rows"] != scope["expected_eligible_rows"]
                    or expected_eligible is not None):
                raise ContractError("Incomplete pilot support")
            if not stats.stream_checks_completed:
                raise ContractError("Loader did not complete source checks")
            summary["source_checks_completed"] = True
        finally:
            stream.close()
            summary["load_stats"] = asdict(stats)
            summary["csv_loading_seconds_excluding_hash"] = (
                summary["loader_advance_seconds"] - stats.hash_seconds)

    try:
        progress()
        tick = time.perf_counter()
        fit_stream = records("fit")
        try:
            reference = fit_velocity(r.observation for r in fit_stream if r.eligible)
        finally:
            fit_stream.close()
        fit_wall = time.perf_counter() - tick
        if reference.n != plan["access"]["fit"]["expected_eligible_rows"]:
            raise ContractError("Fitted count differs from declared support")
        diagnostics["fit_count"] = reference.n
        diagnostics["finite_positive_variance_channels"] = sum(
            math.isfinite(v) and v > 0 for v in reference.variance)
        diagnostics["timing_seconds"]["fit_stage_including_loading"] = fit_wall
        diagnostics["timing_seconds"]["fit_accumulation_and_coordination_excluding_loading"] = (
            fit_wall - populations["fit"]["loader_advance_seconds"])
        before = reference_digest(reference)
        writer.write_json("reference.json", {
            "designation": "independent_ordinary_control_pilot_only_not_a_twin",
            "model_id": plan["model"]["id"], "seed": None,
            "reference": reference.to_dict(), "state_sha256": before,
            "promotion_to_final_checkpoint": False,
        })
        diagnostics["reference_state_sha256_before"] = before
        diagnostics["stage"] = "development_scoring"
        progress()
        print("Fit completed; starting declared development prefix", flush=True)
        detector = VelocityDetector(reference)
        count = 0
        score_seconds = 0.0
        output_seconds = 0.0
        tick = time.perf_counter()
        development_stream = records("check_scores")
        writer.write_text("development_scores.jsonl", "")
        try:
            for record in development_stream:
                observation = record.observation
                if observation.dt is None:
                    detector.reset()
                if record.eligible:
                    score_start = time.perf_counter()
                    score = detector.score(observation)
                    score_seconds += time.perf_counter() - score_start
                    if type(score) not in (int, float) or not math.isfinite(score):
                        raise ContractError("Missing or nonfinite pilot score")
                    output_start = time.perf_counter()
                    writer.append_text("development_scores.jsonl", json.dumps({
                        "row": record.row, "timestamp": str(record.timestamp),
                        "segment": record.segment, "score": score,
                    }, allow_nan=False, separators=(",", ":")) + "\n")
                    output_seconds += time.perf_counter() - output_start
                    count += 1
                    diagnostics["score_count"] = count
                detector.update(observation)
        finally:
            development_stream.close()
        diagnostics["timing_seconds"].update(
            development_stage_including_loading_and_output=time.perf_counter()-tick,
            score_function_calls=score_seconds, score_serialization_and_output=output_seconds)
        if count != plan["access"]["check_scores"]["expected_eligible_rows"]:
            raise ContractError("Incomplete pilot score artifact")
        after = reference_digest(reference)
        diagnostics["reference_state_sha256_after"] = after
        diagnostics["reference_unchanged"] = before == after
        if before != after:
            raise ContractError("Fitted reference changed during scoring")
        diagnostics.update(status="completed", stage="completed", failure_reason=None,
                           score_alignment="complete_declared_support_no_duplicates_or_missing",
                           calibrated_threshold=None, attack_metrics_computed=False,
                           calibration_or_final_observations_parsed=False)
        progress()
    except Exception as error:
        diagnostics.update(status="failed", failure_reason=f"{type(error).__name__}: {error}")
        raise
    finally:
        diagnostics["timing_seconds"]["core_end_to_end"] = time.perf_counter() - started
        diagnostics["load_stats"] = {k: asdict(v) for k, v in load_stats.items()}
