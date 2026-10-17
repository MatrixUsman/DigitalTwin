"""Bounded normal-only ordinary-control fitting and development selection.

This module never exposes calibration/final partitions, attack labels, thresholds
or a test-selection objective. Synthetic Study objects support offline tests.
"""
from __future__ import annotations

from array import array
from collections import Counter
from dataclasses import asdict
from decimal import Decimal
import hashlib
import json
import math
from pathlib import Path
import sys
import time

from .contract import ContractError, LoadStats, Study, iter_development_records
from .data import Observation
from .velocity import VelocityDetector, VelocityReference, fit_velocity

CONTROL_PLAN_PATH = "configs/casper_right_arm_controls_v0.1.json"


def state_digest(reference) -> str:
    return hashlib.sha256(json.dumps(reference.to_dict(), sort_keys=True,
                                     allow_nan=False).encode()).hexdigest()


def load_control_plan(root: Path) -> dict:
    """Read an independently versioned plan; test receipt binds its exact hash."""
    plan = json.loads((root / CONTROL_PLAN_PATH).read_text())
    if plan.get("study_id") != "manufacturing-casper-right-arm-controls-v0.1":
        raise ContractError("Unsupported control study version")
    if any(plan["access"].get(key) is not False for key in (
            "calibration_access", "protected_final_access", "labels_available_to_model")):
        raise ContractError("Control study cannot admit calibration/final/label access")
    documentation = (root / plan["documentation"]).resolve()
    if (not documentation.is_relative_to(root.resolve())
            or hashlib.sha256(documentation.read_bytes()).hexdigest() != plan["documentation_sha256"]):
        raise ContractError("Control-study documentation changed before admission")
    for key in ("data_contract", "evaluation_policy"):
        reference = plan[key]
        path = (root / reference["path"]).resolve()
        if (not path.is_relative_to(root.resolve())
                or hashlib.sha256(path.read_bytes()).hexdigest() != reference["sha256"]):
            raise ContractError("Control-study frozen specification mismatch")
    return plan


class TrainingCache:
    """Compact feature-only cache, preserving Decimal dt; no labels/row IDs.

    Structural eligibility remains coordinator metadata rather than an input to
    a prediction. Each iteration constructs ephemeral immutable Observations.
    """
    def __init__(self):
        self.values = array("d")
        self.deltas = []
        self.eligible = bytearray()

    def append(self, observation: Observation, eligible: bool) -> None:
        self.values.extend(observation.q + observation.qdot)
        self.deltas.append(observation.dt)
        self.eligible.append(eligible)

    def __len__(self):
        return len(self.deltas)

    def records(self):
        for index, delta in enumerate(self.deltas):
            start = index * 12
            yield (Observation(tuple(self.values[start:start+6]),
                               tuple(self.values[start+6:start+12]), delta),
                   bool(self.eligible[index]))

    def fit_observations(self):
        return (observation for observation, eligible in self.records() if eligible)

    def first_segment_eligible(self, max_observations):
        started = False
        iterator = iter(self.records())
        for _ in range(max_observations):
            try:
                observation, eligible = next(iterator)
            except StopIteration:
                break
            if started and observation.dt is None:
                break
            started = True
            if eligible:
                yield observation


def candidate_specs(plan: dict) -> list[dict]:
    models = plan["models"]
    result = [{"id": "velocity_zmax", "family": "velocity", "parameters": {}}]
    for order in models["ar"]["orders"]:
        for ridge in models["ar"]["ridges"]:
            result.append({"id": f"ar_p{order}_ridge{ridge:.12g}", "family": "ar",
                           "parameters": {"order": order, "ridge": ridge}})
    for bins in models["template"]["bins"]:
        result.append({"id": f"template_bins{bins}", "family": "template",
                       "parameters": {"bins": bins}})
    if len({item["id"] for item in result}) != len(result):
        raise ContractError("Duplicate candidate IDs")
    if "candidate_order" in plan:
        by_id = {item["id"]: item for item in result}
        if set(plan["candidate_order"]) != set(by_id) or len(plan["candidate_order"]) != len(result):
            raise ContractError("Declared candidate order differs from finite grid")
        result = [by_id[name] for name in plan["candidate_order"]]
    return result


def select_candidates(ledger: list[dict]) -> dict:
    """Select within method only, from complete normal-development candidates."""
    selected = {}
    for family in ("velocity", "ar", "template"):
        complete = [item for item in ledger
                    if item["family"] == family and item["status"] == "completed"]
        if not complete:
            continue
        # No cross-family ranking; velocity has one fixed configuration.
        # Python min retains first item on exact ties: ledger is declared order.
        winner = min(complete, key=lambda item: item["development_mean_score"])
        selected[family] = {"candidate_id": winner["id"],
                            "model_artifact": winner["model_artifact"],
                            "model_state_sha256": winner["model_state_sha256_before"],
                            "score_artifact": winner["score_artifact"],
                            "selection_value": winner["development_mean_score"],
                            "selection_objective": "fixed_no_selection" if family == "velocity" else "mean_standardized_prediction_MSE"}
    return selected


def run_control_study(study: Study, plan: dict, writer, diagnostics: dict) -> None:
    """Fit each declared candidate once and score the common full dev support.

    Model failures are preserved independently; loader/identity/support failures
    stop the whole study. No successful subset is promoted as a completed study.
    """
    from .controls import (ARAccumulator, ARDetector, Standardizer12,
                                  TemplateAccumulator, TemplateDetector,
                                  estimate_period, fit_standardizer, fit_template_seed)
    started = time.perf_counter()
    statistics = {key: LoadStats() for key in ("fit", "check_scores")}
    populations = {}
    ledger = candidate_specs(plan)
    for item in ledger:
        item.update(status="pending", failure=None, score_count=0)
    diagnostics.update(status="running", stage="training_load", candidates=ledger,
                       populations=populations, timing_seconds={})

    def progress():
        writer.append_text("progress.jsonl", json.dumps({
            "stage": diagnostics["stage"], "elapsed_seconds": time.perf_counter()-started,
            "selected_input_rows_parsed": {key: value.selected_rows_parsed for key, value in statistics.items()},
            "candidate_status": {item["id"]: {"status": item["status"], "score_count": item["score_count"]} for item in ledger},
            "coverage_is_last_known_not_terminal": True,
        }, allow_nan=False, separators=(",", ":")) + "\n")

    def records(name):
        scope = plan["access"][name]
        partition = scope["parent_partition"]
        if partition not in {"training", "development"}:
            raise ContractError("Only training and development are admitted")
        spec = study.partition(partition)
        start, stop = scope["rows_half_open"]
        if (start, stop) != (spec.start, spec.end):
            raise ContractError("Full normal partition required; no subset expansion or shrinkage")
        stats = statistics[name]
        summary = populations[name] = {"raw_rows_yielded": 0, "eligible_rows": 0,
                                       "exclusions": {}, "segment_start_rows": [],
                                       "source_checks_completed": False}
        expected = iter(row for a, b in scope["eligible_intervals_half_open"] for row in range(a, b))
        next_eligible = next(expected, None)
        exclusions = Counter()
        stream = iter_development_records(study, partition, stats=stats)
        try:
            for record in stream:
                if record.row != start + summary["raw_rows_yielded"]:
                    raise ContractError("Missing, duplicated or reordered control-study row")
                summary["raw_rows_yielded"] += 1
                if record.eligible != (record.row == next_eligible):
                    raise ContractError("Control-study endpoint mask mismatch")
                if record.eligible:
                    summary["eligible_rows"] += 1
                    next_eligible = next(expected, None)
                else:
                    exclusions[record.exclusion] += 1
                    summary["exclusions"] = dict(exclusions)
                if record.observation is None:
                    raise ContractError("Invalid control-study observation")
                if record.observation.dt is None:
                    summary["segment_start_rows"].append(record.row)
                if summary["raw_rows_yielded"] % 10000 == 0:
                    progress()
                yield record
            if (summary["raw_rows_yielded"] != scope["raw_rows"]
                    or summary["eligible_rows"] != scope["expected_eligible_rows"]
                    or next_eligible is not None or not stats.stream_checks_completed):
                raise ContractError("Incomplete control-study source or support checks")
            summary["source_checks_completed"] = True
        finally:
            stream.close()
            summary["load_stats"] = asdict(stats)

    def failure(item, error, stage):
        item.update(status="failed", failure={"stage": stage,
                    "reason": f"{type(error).__name__}: {error}"})

    references, detectors, score_arrays = {}, {}, {}
    try:
        progress()
        cache = TrainingCache()
        for record in records("fit"):
            cache.append(record.observation, record.eligible)
        diagnostics["training_cache_rows"] = len(cache)
        diagnostics["stage"] = "training_fit"
        progress()
        tick = time.perf_counter()
        velocity_item = ledger[0]
        try:
            references[velocity_item["id"]] = fit_velocity(cache.fit_observations())
        except Exception as error:
            failure(velocity_item, error, "fit")
        scaler = fit_standardizer(cache.fit_observations())
        writer.write_json("training_standardizer.json", {"state": scaler.to_dict(), "state_sha256": state_digest(scaler)})
        ar_accumulators = {order: ARAccumulator(scaler, order) for order in plan["models"]["ar"]["orders"]}
        template_accumulators = {}
        template_config = plan["models"]["template"]
        try:
            period_kwargs = {key: template_config["period_estimation"][key]
                             for key in ("stride", "min_lag", "max_lag", "max_observations")}
            prefix_limit = period_kwargs["max_observations"]
            period = estimate_period(cache.first_segment_eligible(prefix_limit), scaler, **period_kwargs)
            diagnostics["period_estimate"] = period.to_dict()
            for item in ledger:
                if item["family"] == "template":
                    try:
                        seed = fit_template_seed(cache.first_segment_eligible(prefix_limit), scaler,
                                                 period.period_seconds, item["parameters"]["bins"],
                                                 initialization=template_config["initialization"])
                        template_accumulators[item["id"]] = TemplateAccumulator(seed)
                    except Exception as error:
                        failure(item, error, "template_initialization")
        except Exception as error:
            for item in ledger:
                if item["family"] == "template":
                    failure(item, error, "period_estimation")
        for index, (observation, eligible) in enumerate(cache.records()):
            for order, accumulator in list(ar_accumulators.items()):
                try:
                    accumulator.observe(observation, eligible)
                except Exception as error:
                    for item in ledger:
                        if item["family"] == "ar" and item["parameters"]["order"] == order:
                            failure(item, error, "fit")
                    del ar_accumulators[order]
            for name, accumulator in list(template_accumulators.items()):
                try:
                    accumulator.observe(observation, eligible)
                except Exception as error:
                    failure(next(item for item in ledger if item["id"] == name), error, "fit")
                    del template_accumulators[name]
            if index % 10000 == 0:
                progress()
        for item in ledger:
            if item["status"] == "failed":
                continue
            try:
                if item["family"] == "ar":
                    reference = ar_accumulators[item["parameters"]["order"]].finish(item["parameters"]["ridge"])
                    detector = ARDetector(reference)
                elif item["family"] == "template":
                    reference = template_accumulators[item["id"]].finish()
                    detector = TemplateDetector(reference)
                else:
                    reference = references[item["id"]]
                    detector = VelocityDetector(reference)
                if reference.n != plan["access"]["fit"]["expected_eligible_rows"]:
                    raise ContractError("Reference count differs from complete eligible training support")
                references[item["id"]], detectors[item["id"]] = reference, detector
                item.update(status="fitted", fit_count=reference.n,
                            model_artifact=item["id"]+".model.json",
                            model_state_sha256_before=state_digest(reference))
                writer.write_json(item["model_artifact"], {"candidate": item["id"], "family": item["family"],
                                  "designation": "independent_ordinary_control_not_a_digital_twin",
                                  "reference": reference.to_dict(), "state_sha256": state_digest(reference)})
                score_arrays[item["id"]] = array("d")
            except Exception as error:
                failure(item, error, "fit_finalization")
        del cache
        diagnostics["timing_seconds"]["fitting_after_training_load"] = time.perf_counter()-tick
        diagnostics["stage"] = "development_scoring"
        progress()
        writer.write_text("development_index.jsonl", "")
        index_buffer = []
        for record in records("check_scores"):
            observation = record.observation
            if record.eligible:
                index_buffer.append(json.dumps({"row": record.row, "timestamp": str(record.timestamp),
                                               "segment": record.segment}, separators=(",", ":"))+"\n")
            for item in ledger:
                if item["status"] != "fitted":
                    continue
                detector = detectors[item["id"]]
                try:
                    if observation.dt is None:
                        detector.reset()
                    if record.eligible:
                        score = detector.score(observation)
                        if type(score) not in (int, float) or not math.isfinite(score) or score < 0:
                            raise ContractError("Missing, negative or nonfinite development score")
                        score_arrays[item["id"]].append(score)
                        item["score_count"] += 1
                    detector.update(observation)
                except Exception as error:
                    failure(item, error, "development_scoring")
            if len(index_buffer) >= 1000:
                writer.append_text("development_index.jsonl", "".join(index_buffer))
                index_buffer.clear()
        if index_buffer:
            writer.append_text("development_index.jsonl", "".join(index_buffer))
        for item in ledger:
            if item["id"] not in score_arrays:
                continue
            scores = score_arrays[item["id"]]
            item["score_artifact"] = item["id"]+".scores.f64"
            writer.write_bytes(item["score_artifact"], scores.tobytes())
            item["score_sha256"] = hashlib.sha256(scores.tobytes()).hexdigest()
            after = state_digest(references[item["id"]])
            item["model_state_sha256_after"] = after
            item["reference_unchanged"] = after == item["model_state_sha256_before"]
            if item["status"] == "failed":
                continue
            if not item["reference_unchanged"] or len(scores) != plan["access"]["check_scores"]["expected_eligible_rows"]:
                failure(item, ContractError("Changed reference or incomplete development scores"), "validation")
                continue
            item.update(status="completed", development_mean_score=math.fsum(scores)/len(scores),
                        score_min=min(scores), score_max=max(scores))
        selected = select_candidates(ledger)
        complete = all(item["status"] == "completed" for item in ledger)
        writer.write_json("candidate_results.json", {"candidates": ledger, "selection": selected,
                          "scores": {"format": "native_array_d", "bytes_per_score": array("d").itemsize,
                                     "byteorder": sys.byteorder, "alignment": "development_index.jsonl"},
                          "all_candidates_complete": complete})
        writer.write_json("selected_artifacts.json", {"selection": selected,
                          "ready_for_later_calibration": complete and set(selected) == {"velocity", "ar", "template"},
                          "calibrated": False, "final_test_admitted": False,
                          "selection_partition": "development", "refit_on_development": False})
        diagnostics.update(status="completed" if complete else "failed", stage="completed",
                           all_candidates_complete=complete, selected=selected,
                           calibrated_threshold=None, attack_metrics_computed=False,
                           calibration_or_final_observations_parsed=False,
                           failure_reason=None if complete else "One or more declared candidates failed; inspect preserved ledger")
        progress()
    except Exception as error:
        diagnostics.update(status="failed", failure_reason=f"{type(error).__name__}: {error}")
        raise
    finally:
        diagnostics["timing_seconds"]["core_end_to_end"] = time.perf_counter()-started
        diagnostics["load_stats"] = {key: asdict(value) for key, value in statistics.items()}


def validate_control_artifacts(run_dir: Path, plan: dict) -> dict:
    """Independent saved-artifact readback, without opening source observations."""
    from .controls import ARReference, Standardizer12, TemplateReference
    results = json.loads((run_dir / "candidate_results.json").read_text())
    expected_rows = iter(row for a, b in plan["access"]["check_scores"]["eligible_intervals_half_open"] for row in range(a, b))
    count = 0
    with (run_dir / "development_index.jsonl").open() as handle:
        previous_timestamp = None
        for line in handle:
            item = json.loads(line)
            timestamp = Decimal(item["timestamp"])
            if (set(item) != {"row", "timestamp", "segment"}
                    or type(item["row"]) is not int or item["row"] != next(expected_rows, None)
                    or not timestamp.is_finite() or type(item["segment"]) is not int
                    or (previous_timestamp is not None and timestamp <= previous_timestamp)):
                raise ContractError("Invalid, missing, duplicated or reordered saved score index")
            previous_timestamp = timestamp
            count += 1
    if next(expected_rows, None) is not None or count != plan["access"]["check_scores"]["expected_eligible_rows"]:
        raise ContractError("Incomplete saved score index")
    expected_specs = candidate_specs(plan)
    if [item["id"] for item in results["candidates"]] != [item["id"] for item in expected_specs]:
        raise ContractError("Candidate inventory mismatch")
    if (results["scores"]["byteorder"] != sys.byteorder
            or results["scores"]["bytes_per_score"] != array("d").itemsize):
        raise ContractError("Unsupported saved-score representation")
    scaler_saved = json.loads((run_dir / "training_standardizer.json").read_text())
    scaler = Standardizer12.from_dict(scaler_saved["state"])
    if state_digest(scaler) != scaler_saved["state_sha256"] or scaler.n != plan["access"]["fit"]["expected_eligible_rows"]:
        raise ContractError("Saved training standardizer changed")
    for item, expected_spec in zip(results["candidates"], expected_specs):
        if item["family"] != expected_spec["family"] or item["parameters"] != expected_spec["parameters"]:
            raise ContractError("Saved candidate family or parameters differ from the finite grid")
        if item["status"] != "completed":
            raise ContractError("A declared candidate is incomplete")
        saved = json.loads((run_dir / item["model_artifact"]).read_text())
        if item["family"] == "velocity":
            state = saved["reference"]
            reference = VelocityReference(state["n"], tuple(state["mean"]), tuple(state["variance"]), tuple(state["sigma"]))
        else:
            cls = ARReference if item["family"] == "ar" else TemplateReference
            reference = cls.from_dict(saved["reference"])
            if state_digest(reference.scaler) != state_digest(scaler):
                raise ContractError("Candidate does not use the saved training-only standardizer")
            if item["family"] == "ar":
                if reference.order != item["parameters"]["order"] or reference.ridge != item["parameters"]["ridge"]:
                    raise ContractError("Saved AR configuration differs from the declared candidate")
            elif (reference.bins != item["parameters"]["bins"]
                  or reference.initialization != plan["models"]["template"]["initialization"]):
                raise ContractError("Saved template configuration differs from the declared candidate")
        state_hash = state_digest(reference)
        if (reference.n != plan["access"]["fit"]["expected_eligible_rows"]
                or saved["candidate"] != item["id"] or saved["family"] != item["family"]
                or item["reference_unchanged"] is not True
                or state_hash != saved["state_sha256"] or state_hash != item["model_state_sha256_before"]
                or state_hash != item["model_state_sha256_after"]):
            raise ContractError("Saved model identity/count mismatch")
        payload = (run_dir / item["score_artifact"]).read_bytes()
        scores = array("d")
        scores.frombytes(payload)
        if (len(scores) != count or item["score_count"] != count
                or hashlib.sha256(payload).hexdigest() != item["score_sha256"]
                or any(not math.isfinite(value) or value < 0 for value in scores)
                or math.fsum(scores)/len(scores) != item["development_mean_score"]):
            raise ContractError("Saved score checksum/count/statistics mismatch")
    selected = json.loads((run_dir / "selected_artifacts.json").read_text())
    if (selected["selection"] != select_candidates(results["candidates"])
            or selected["selection"] != results["selection"]
            or selected["ready_for_later_calibration"] is not True
            or selected["selection_partition"] != "development" or selected["refit_on_development"] is not False
            or selected["calibrated"] is not False or selected["final_test_admitted"] is not False):
        raise ContractError("Saved selection does not match the declared rule")
    return {"saved_index_rows": count, "complete_candidates": len(results["candidates"]),
            "all_models_immutable": True, "all_scores_finite": True,
            "selection_verified": True, "calibration_or_final_opened": False}
