"""Development-only replay of four explanatory scores; no fitting or selection.

All six outputs use one immutable synchronized observer. Prior R/RC arrays and
coordinates are byte-identical acceptance controls, not tuning targets.
"""
from __future__ import annotations

from array import array
from dataclasses import asdict
import hashlib
import json
import math
from pathlib import Path
import sys
import time

from .contract import ContractError, LoadStats, verify_source
from .control_study import state_digest
from .controls import TemplateReference
from .observer import EvidenceScale, ObserverConfig, PhaseObserver, prepare_observation
from .observer_study import bound_path, records, sha

PLAN_PATH = "configs/casper_right_arm_score_extension_v0.1.json"
SCORES = ("O-R", "O-RC", "O-C", "O-K", "O-L", "O-Rv")
OLD_NAMES = {"O-R": "synchronized_residual", "O-RC": "synchronized_evidence"}


def load_score_extension_plan(root):
    plan = json.loads((root / PLAN_PATH).read_text())
    if plan.get("study_id") != "manufacturing-casper-right-arm-score-extension-v0.1":
        raise ContractError("Unsupported score-extension version")
    access = plan["access"]
    if (set(access) != {"check_scores", "calibration_access", "protected_final_access", "labels_available_to_model", "training_access", "fitting_allowed"}
            or any(access[key] is not False for key in access if key != "check_scores")
            or access["check_scores"]["parent_partition"] != "development"
            or tuple(plan["scores"]) != SCORES):
        raise ContractError("Score extension admits only development replay, without fitting")
    document = bound_path(root, plan["documentation"])
    if sha(document) != plan["documentation_sha256"]:
        raise ContractError("Score-extension documentation changed")
    for key in ("data_contract", "evaluation_policy", "observer_registry", "observer_configuration", "pending_final_freeze"):
        item = plan[key]
        if sha(bound_path(root, item["path"])) != item["sha256"]:
            raise ContractError("Score-extension frozen dependency mismatch: " + key)
    from .observer_scores import MASS_ABS_TOL, CONSISTENCY_REL_TOL, CONSISTENCY_ABS_TOL, NONNEGATIVE_ABS_TOL
    expected_numerics = {"probability_mass_absolute_tolerance": MASS_ABS_TOL, "consistency_relative_tolerance": CONSISTENCY_REL_TOL, "consistency_absolute_tolerance": CONSISTENCY_ABS_TOL, "negative_roundoff_absolute_tolerance": NONNEGATIVE_ABS_TOL, "historical_score_and_coordinate_parity": "exact_byte_hash_not_tolerance"}
    if plan["numerics"] != expected_numerics:
        raise ContractError("Declared numerical policy differs from score helper")
    if (plan["continuity"]["warmup"] != 1528 or plan["continuity"]["gap_seconds"] != .075
            or plan["continuity"]["subset_expansion"] is not False or plan["continuity"]["consume_record_at_stop"] is not False
            or plan["execution"]["attempts"] != 1 or plan["execution"]["automatic_retry"] is not False
            or plan["execution"]["fit_calls"] != 0 or plan["execution"]["score_selection"] is not False):
        raise ContractError("Declared continuity or execution policy changed")
    for name, expected in plan["preserved_dependencies_sha256"].items():
        if sha(bound_path(root, name)) != expected:
            raise ContractError("Historical immutable dependency changed: " + name)
    for name, expected in plan["preserved_source_sha256"].items():
        if sha(bound_path(root, name)) != expected:
            raise ContractError("Historical observer dependency changed: " + name)
    return plan


def load_inputs(root, plan):
    """Verify fitted artifact provenance and saved parity targets; never open raw."""
    hashes = {}

    def admit(relative, expected):
        path = bound_path(root, relative)
        actual = sha(path)
        if actual != expected:
            raise ContractError("Frozen observer input identity changed: " + relative)
        hashes[relative] = actual
        return path

    for name, expected in plan.get("preserved_dependencies_sha256", {}).items():
        admit(name, expected)
    for name in (PLAN_PATH, plan.get("documentation")):
        if name and (root / name).is_file():
            hashes[name] = sha(root / name)
    binding = plan["observer_registry"]
    registry = json.loads(admit(binding["path"], binding["sha256"]).read_text())
    if (registry["reference_refit"] is not False or registry["development_refit"] is not False
            or registry["thresholds"] is not None or registry["final_test_admitted"] is not False
            or registry["principal_pair_shared_state"] is not True
            or registry["development_eligible_count"] != plan["access"]["check_scores"]["expected_eligible_rows"]):
        raise ContractError("Observer registry incompatible with score-only development")
    admit(registry["input_reference_registry"], registry["input_reference_registry_sha256"])
    configuration = plan["observer_configuration"]
    admit(configuration["path"], configuration["sha256"])
    if configuration["sha256"] != registry["configuration_sha256"]:
        raise ContractError("Observer configuration binding differs from registry")
    prior_run = registry["source_run"]
    manifest = json.loads(admit(prior_run + "/run.json", registry["run_manifest_sha256"]).read_text())
    if manifest["accepted"] is not True or manifest["status"] != "completed":
        raise ContractError("Observer source run was not accepted")
    model = json.loads(admit(registry["model_path"], registry["model_file_sha256"]).read_text())
    reference = TemplateReference.from_dict(model["template"])
    config = ObserverConfig.from_dict(model["observer_config"])
    n = registry["training_eligible_count"]
    if (model["training_eligible_count"] != n or reference.n != n
            or model["template_state_sha256"] != state_digest(reference)
            or model["development_refitting"] is not False
            or model["paired_ablation_same_state"] is not True
            or set(model["normalizers"]) != {"residual", "correction_js"}
            or any(v["n"] != n for v in model["normalizers"].values())
            or model["emission_scale_fit"]["n"] != n):
        raise ContractError("Observer fitted state provenance mismatch")
    scales = EvidenceScale(n, model["normalizers"]["residual"]["mean"], model["normalizers"]["correction_js"]["mean"])
    prior_config = json.loads((root / configuration["path"]).read_text())
    if (config.initialization != prior_config["model"]["initialization"]
            or config.mixing_rate != prior_config["model"]["mixing_rate"]
            or config.temperature != max(model["emission_scale_fit"]["mean"], prior_config["model"]["temperature_floor"])
            or plan["access"]["check_scores"] != prior_config["access"]["check_scores"]):
        raise ContractError("Immutable observer parameters or development scope changed")
    saved = {}
    for name, old in OLD_NAMES.items():
        item = registry["saved_scores"][old]
        path = admit(item["path"], item["sha256"])
        if item["n"] != registry["development_eligible_count"] or path.stat().st_size != item["n"] * 8:
            raise ContractError("Prior score support mismatch")
        saved[name] = {"path": item["path"], "sha256": item["sha256"], "n": item["n"]}
    index_name = "development_index.jsonl"
    index_item = manifest["artifacts_excluding_this_manifest"][index_name]
    index_path = admit(prior_run + "/" + index_name, index_item["sha256"])
    if index_path.stat().st_size != index_item["bytes"]:
        raise ContractError("Prior coordinate bytes mismatch")
    result_item = manifest["artifacts_excluding_this_manifest"]["observer_results.json"]
    results = json.loads(admit(prior_run + "/observer_results.json", result_item["sha256"]).read_text())
    if results["score_format"] != {"bytes_per_score": array("d").itemsize, "byteorder": sys.byteorder}:
        raise ContractError("Prior score format does not match current interpreter")
    return reference, config, scales, {
        "input_sha256": hashes, "model_file_sha256": registry["model_file_sha256"],
        "template_state_sha256": state_digest(reference), "old_scores": saved,
        "old_index": {"path": str(index_path.relative_to(root.resolve())), "sha256": index_item["sha256"]},
        "training_eligible_count": n,
    }


def unchanged_inputs(root, hashes):
    changed = [name for name, expected in hashes.items() if not (root / name).is_file() or sha(root / name) != expected]
    if changed:
        raise ContractError("Frozen inputs changed during score extension: " + ", ".join(changed))
    return True


def run_score_extension(study, plan, writer, diagnostics):
    from .observer_scores import score_observer_proposal
    started = time.perf_counter()
    stats, population = LoadStats(), {}
    diagnostics.update(status="running", stage="input_admission", population=population)
    try:
        reference, config, scales, provenance = load_inputs(study.project_root, plan)
        if study.partition("development").warmup != config.initialization:
            raise ContractError("Observer initialization differs from common warmup")
        writer.write_json("input_provenance.json", provenance)
        writer.write_json("immutable_model_snapshot.json", {"reference": reference.to_dict(), "config": config.to_dict(),
                          "scale": asdict(scales), "state_sha256": state_digest(reference)})
        arrays = {name: array("d") for name in SCORES}
        writer.write_text("development_index.jsonl", "")
        index_buffer = []
        observer = PhaseObserver(reference, config, mode="synchronized")
        fitted_before = (reference.to_dict(), config.to_dict(), asdict(scales))

        def progress():
            writer.append_text("progress.jsonl", json.dumps({"stage": diagnostics["stage"],
                "elapsed_seconds": time.perf_counter() - started,
                "selected_input_rows_parsed": stats.selected_rows_parsed,
                "scores_emitted": len(arrays["O-R"]), "coverage_is_last_known_not_terminal": True}) + "\n")

        diagnostics["stage"] = "development_only_replay"
        progress()
        for record in records(study, plan, "check_scores", stats, population, progress):
            prepared = prepare_observation(reference, record.observation)
            proposal = observer.propose(prepared)
            if record.eligible:
                if not proposal.ready:
                    raise ContractError("Observer uninitialized on eligible support")
                scores = score_observer_proposal(proposal, prepared, config, scales).to_dict()
                if tuple(scores) != SCORES or any(not math.isfinite(v) or v < 0 for v in scores.values()):
                    raise ContractError("Incomplete or invalid score proposal")
                for name, value in scores.items():
                    arrays[name].append(value)
                index_buffer.append(json.dumps({"row": record.row, "timestamp": str(record.timestamp),
                                                "segment": record.segment}, separators=(",", ":")) + "\n")
            # The current observation may affect correction evidence, but state
            # changes only after all six scores have been emitted.
            observer.commit(proposal)
            if len(index_buffer) >= 1000:
                writer.append_text("development_index.jsonl", "".join(index_buffer)); index_buffer.clear()
        if index_buffer:
            writer.append_text("development_index.jsonl", "".join(index_buffer))
        if fitted_before != (reference.to_dict(), config.to_dict(), asdict(scales)):
            raise ContractError("Pinned fitted reference changed during development")
        diagnostics["stage"] = "source_identity_postcheck"
        with (study.project_root / study.source_relative_path).open("rb") as source:
            verify_source(source, expected_bytes=study.source_bytes, expected_sha256=study.source_sha256, stats=stats)
        unchanged_inputs(study.project_root, provenance["input_sha256"])
        diagnostics["stage"] = "exact_parity_and_artifact_write"
        if sha(writer.output_dir / "development_index.jsonl") != provenance["old_index"]["sha256"]:
            raise ContractError("Development coordinates differ from original observer run")
        score_manifest = {}
        for name, values in arrays.items():
            if len(values) != plan["access"]["check_scores"]["expected_eligible_rows"]:
                raise ContractError("Score support incomplete")
            payload = values.tobytes()
            fingerprint = hashlib.sha256(payload).hexdigest()
            # No tolerance or post-hoc adjustment is allowed for historical parity.
            if name in OLD_NAMES and fingerprint != provenance["old_scores"][name]["sha256"]:
                raise ContractError("Exact historical score parity failed: " + name)
            filename = name + ".scores.f64"
            writer.write_bytes(filename, payload)
            score_manifest[name] = {"path": filename, "sha256": fingerprint, "n": len(values),
                                    "mean": math.fsum(values)/len(values), "min": min(values), "max": max(values)}
        results = {"kind": "normal_only_frozen_observer_score_extension_not_benchmark", "scores": score_manifest,
                   "score_format": {"bytes_per_score": array("d").itemsize, "byteorder": sys.byteorder},
                   "index_sha256": sha(writer.output_dir / "development_index.jsonl"),
                   "same_state_trajectory": True, "exact_historical_score_parity": dict.fromkeys(OLD_NAMES, True),
                   "immutable_fitted_parameters": True, "input_hashes_unchanged": True,
                   "fit_calls": 0, "training_rows_parsed": 0, "calibrated_threshold": None,
                   "attack_metrics_computed": False, "calibration_or_final_observations_parsed": False,
                   "score_selection_performed": False, "normal_development_reuse": True}
        writer.write_json("score_extension_results.json", results)
        diagnostics.update(status="completed", stage="completed", score_counts={k: len(v) for k,v in arrays.items()},
                           reference_unchanged=True, fit_calls=0, training_rows_parsed=0,
                           exact_historical_score_parity=dict.fromkeys(OLD_NAMES, True),
                           calibrated_threshold=None, attack_metrics_computed=False,
                           calibration_or_final_observations_parsed=False)
        progress()
    except Exception as error:
        diagnostics.update(status="failed", failure_reason=f"{type(error).__name__}: {error}")
        raise
    finally:
        diagnostics["core_elapsed_seconds"] = time.perf_counter() - started
        diagnostics["load_stats"] = asdict(stats)


def validate_score_extension_artifacts(run_dir, plan, root):
    """Full saved-score/index integrity readback; no raw observation access."""
    from decimal import Decimal
    results = json.loads((run_dir / "score_extension_results.json").read_text())
    provenance = json.loads((run_dir / "input_provenance.json").read_text())
    unchanged_inputs(root, provenance["input_sha256"])
    reference, config, scales, actual_provenance = load_inputs(root, plan)
    snapshot = json.loads((run_dir / "immutable_model_snapshot.json").read_text())
    expected_snapshot = {"reference": reference.to_dict(), "config": config.to_dict(), "scale": asdict(scales), "state_sha256": state_digest(reference)}
    if snapshot != expected_snapshot:
        raise ContractError("Saved immutable model snapshot differs from input artifact")
    if provenance != actual_provenance:
        raise ContractError("Saved input provenance differs from admitted dependencies")
    scope = plan["access"]["check_scores"]
    expected = iter(row for a,b in scope["eligible_intervals_half_open"] for row in range(a,b))
    previous, count = None, 0
    index = run_dir / "development_index.jsonl"
    with index.open() as handle:
        for line in handle:
            item = json.loads(line)
            timestamp = Decimal(item["timestamp"])
            if (set(item) != {"row", "timestamp", "segment"} or type(item["row"]) is not int
                    or item["row"] != next(expected, None) or not timestamp.is_finite()
                    or type(item["segment"]) is not int or (previous is not None and timestamp <= previous)):
                raise ContractError("Invalid saved extension coordinate")
            previous, count = timestamp, count + 1
    if (count != scope["expected_eligible_rows"] or next(expected, None) is not None
            or sha(index) != provenance["old_index"]["sha256"] or sha(index) != results["index_sha256"]):
        raise ContractError("Saved extension coordinates lack exact original parity")
    if (set(results["scores"]) != set(SCORES)
            or results["score_format"] != {"bytes_per_score": array("d").itemsize, "byteorder": sys.byteorder}):
        raise ContractError("Saved extension score inventory or encoding mismatch")
    arrays = {}
    for name, item in results["scores"].items():
        if item["path"] != name + ".scores.f64":
            raise ContractError("Invalid score artifact filename")
        payload = (run_dir / item["path"]).read_bytes()
        if len(payload) != count * 8:
            raise ContractError("Saved extension score length mismatch")
        values = array("d"); values.frombytes(payload)
        if (item["n"] != count or hashlib.sha256(payload).hexdigest() != item["sha256"]
                or any(not math.isfinite(x) or x < 0 for x in values)
                or item["mean"] != math.fsum(values)/count or item["min"] != min(values) or item["max"] != max(values)
                or (name in OLD_NAMES and item["sha256"] != provenance["old_scores"][name]["sha256"])):
            raise ContractError("Saved extension score integrity or parity mismatch")
        arrays[name] = values
    for r, rc, c, rv in zip(arrays["O-R"], arrays["O-RC"], arrays["O-C"], arrays["O-Rv"]):
        if rc != r + c / scales.mean_correction or c > math.log(2) + 1e-14:
            raise ContractError("Saved correction score violates exact RC formula or JS bound")
        upper = 2 * scales.mean_residual * r
        if rv > upper and not math.isclose(rv, upper, rel_tol=1e-12, abs_tol=1e-14):
            raise ContractError("Velocity subset residual exceeds full residual bound")
    if (results["same_state_trajectory"] is not True or results["immutable_fitted_parameters"] is not True
            or results["input_hashes_unchanged"] is not True or results["fit_calls"] != 0
            or results["training_rows_parsed"] != 0 or results["calibrated_threshold"] is not None
            or results["attack_metrics_computed"] is not False or results["calibration_or_final_observations_parsed"] is not False
            or results["score_selection_performed"] is not False
            or results["exact_historical_score_parity"] != dict.fromkeys(OLD_NAMES, True)):
        raise ContractError("Saved extension scope/immutability claims inconsistent")
    return {"saved_index_rows": count, "score_variants": len(SCORES), "all_scores_finite": True,
            "exact_historical_score_parity": dict.fromkeys(OLD_NAMES, True), "exact_coordinate_parity": True,
            "input_hashes_unchanged": True, "fit_calls": 0, "calibration_or_final_opened": False}
