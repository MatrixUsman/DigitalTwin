"""One-attempt calibration and separately invoked final scoring/evaluation.

Run from manufacturing using .venv/bin/python. --freeze and --prepare-final
write real artifact records. --check-final opens saved metadata/artifacts only.
Final scoring and label evaluation are distinct explicit commands; neither is
implied or launched by calibration/preparation. No automatic retry exists.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
import json
import os
from pathlib import Path
import platform
import shlex
import shutil
import subprocess
import sys
import time
from importlib.metadata import distributions

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from mfg_twin.campaign import (CONFIG, CHOICES, FINAL, METHODS, accepted_run, bound, file_ref,
    read_ref, run_evaluation, run_scoring, sha, utc, validate_calibration, validate_seal,
    verify_choices, verify_final)
from mfg_twin.contract import load_study
from mfg_twin.metrics import Event
from mfg_twin.supervisor import BudgetWriter, Limits, install_worker_limits, supervise, worker_usage
from run_score_extension import (admission_files, validate_test_receipt, install_worker_scope,
                                 resource_receipt_admitted)


def write_new(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x") as handle:
        json.dump(value, handle, indent=2, allow_nan=False)
        handle.write("\n")


def environment():
    return {"executable": sys.executable, "python": sys.version, "prefix": sys.prefix,
        "platform": platform.platform(), "machine": platform.machine(),
        "installed_distributions": sorted((d.metadata.get("Name", "unknown"), d.version) for d in distributions()),
        "hardware_sysctl": subprocess.check_output(["/usr/sbin/sysctl", "-n", "hw.model", "hw.memsize", "machdep.cpu.brand_string"], text=True).splitlines(),
        "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "git_status": subprocess.check_output(["git", "status", "--short", "--", "."], cwd=ROOT, text=True),
        "cwd": str(ROOT), "dependency_policy": "standard_library_only", "device": "cpu", "workers": 1,
        "thread_environment": dict.fromkeys(("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"), "1")}


def verify_environment(freeze):
    recorded = freeze["environment"]
    for key, actual in (("executable", sys.executable), ("python", sys.version), ("prefix", sys.prefix)):
        if recorded[key] != actual:
            raise ValueError("Frozen interpreter differs: " + key)
    actual = sorted([d.metadata.get("Name", "unknown"), d.version] for d in distributions())
    if recorded["installed_distributions"] != actual:
        raise ValueError("Frozen dependencies differ")
    files = {str(p.relative_to(ROOT)): sha(p) for p in admission_files()}
    if files != freeze["source_sha256"]:
        raise ValueError("Frozen tested source inventory differs")


def ledger(event, **details):
    """Logical append-only hash chain; no OS tamper-proof claim."""
    path = ROOT / "local/campaign_v0.1/access.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    previous = sha(path) if path.exists() else None
    with path.open("a") as handle:
        handle.write(json.dumps({"time": utc(), "actor": "Codex assistant/operator", "event": event,
                                "previous_file_sha256": previous, **details}, allow_nan=False) + "\n")


def freeze_models(test_receipt):
    if (ROOT / CHOICES).exists():
        raise ValueError("Selection freeze already exists; no overwrite/reselection")
    validate_test_receipt(test_receipt)
    study = load_study(ROOT)
    from mfg_twin.score_extension import load_inputs, load_score_extension_plan
    _, _, _, old = load_inputs(ROOT, load_score_extension_plan(ROOT))
    config = json.loads((ROOT / CONFIG).read_text())
    if config["methods"] != list(METHODS):
        raise ValueError("Incomplete roster")
    controls = json.loads((ROOT / "experiments/SELECTED_CONTROLS_V0.1.json").read_text())
    observer = json.loads((ROOT / "experiments/OBSERVER_ARTIFACTS_V0.1.json").read_text())
    extension = json.loads((ROOT / "experiments/SCORE_EXTENSION_ARTIFACTS_V0.1.json").read_text())
    selected = {name: {"path": x["model_path"], "sha256": x["model_file_sha256"]}
                for name, x in controls["selected"].items()}
    selected["observer"] = {"path": observer["model_path"], "sha256": observer["model_file_sha256"]}
    for ref in selected.values():
        read_ref(ROOT, ref)
    # Bind every artifact from all three completed source studies, including
    # candidates not selected. No candidate/failure is removed from provenance.
    refs = {name: {"path": name, "sha256": digest} for name, digest in old["input_sha256"].items() if name != FINAL}
    for registry in (controls, observer, extension):
        run_path = registry["source_run"] + "/run.json"
        run_ref = {"path": run_path, "sha256": registry["run_manifest_sha256"]}
        run = json.loads(read_ref(ROOT, run_ref).read_text())
        if run.get("accepted") is not True:
            raise ValueError("Source study not accepted")
        refs[run_path] = run_ref
        for name, artifact in run["artifacts_excluding_this_manifest"].items():
            relative = registry["source_run"] + "/" + name
            ref = {"path": relative, "sha256": artifact["sha256"]}
            read_ref(ROOT, ref)
            refs[relative] = ref
    for relative in (CONFIG, config["documentation"], "experiments/SELECTED_CONTROLS_V0.1.json",
                     "experiments/OBSERVER_ARTIFACTS_V0.1.json", "experiments/SCORE_EXTENSION_ARTIFACTS_V0.1.json"):
        refs[relative] = file_ref(ROOT, ROOT / relative)
    files = admission_files()
    env = environment()
    folder = ROOT / "local/campaign_v0.1/selection_freeze"
    folder.mkdir(parents=True, exist_ok=False)
    writer = BudgetWriter(folder, limit_bytes=10 * 1024 * 1024)
    writer.write_text("prior_empty_final_freeze.json", (ROOT / FINAL).read_text())
    writer.write_text("test_receipt.json", test_receipt.read_text())
    writer.write_json("source_snapshot.json", {str(p.relative_to(ROOT)): p.read_text() for p in files})
    writer.write_json("environment.json", env)
    writer.write_json("fitted_model_snapshots.json", {k: json.loads(read_ref(ROOT, v).read_text()) for k, v in selected.items()})
    writer.write_text("tracked_workspace.patch", subprocess.check_output(["git", "diff", "HEAD", "--", "."], cwd=ROOT, text=True))
    writer.write_json("mask.json", {"source_sha256": study.source_sha256,
        "partitions": [{"name": p.name, "start": p.start, "end": p.end, "warmup": p.warmup, "gap_seconds": str(p.gap_seconds)} for p in study.partitions],
        "eligible_intervals": dict(study.eligible_intervals)})
    value = {"kind": "actual_model_selection_freeze", "status": "frozen_before_calibration", "created_at_utc": utc(),
        "project": "manufacturing", "owner": "Haiqa Mushtaq", "operator": "Codex assistant", "reviewer": "internal software/artifact checks; no independent human custodian",
        "methods": list(METHODS), "roster": [dict(item, fitted_artifact=selected[item["artifact_key"]]) for item in config["roster"]], "deterministic_runs_each": 1,
        "declared_stochastic_seeds": [17, 42, 2026], "stochastic_runs": [], "fit_allowed": False,
        "calibration_observations_seen": False, "final_observations_used_for_selection": False,
        "configuration": file_ref(ROOT, ROOT / CONFIG), "fitted_artifacts": selected,
        "inputs": list(refs.values()), "source_sha256": {str(p.relative_to(ROOT)): sha(p) for p in files},
        "environment": env, "provenance_files": {p.name: file_ref(ROOT, p) for p in folder.iterdir()},
        "selection": config["normal_selection"], "transformations": config["preprocessing"],
        "initialization": config["initialization"], "primary_contrast": config["primary_contrast"],
        "reporting": config["reporting"], "budgets": config["phase_budgets"],
        "command": shlex.join([sys.executable, *sys.argv]),
        "execution_commands": {
            "calibrate": ".venv/bin/python scripts/run_campaign.py --calibrate",
            "score_final": ".venv/bin/python scripts/run_campaign.py --score-final",
            "evaluate_final": ".venv/bin/python scripts/run_campaign.py --evaluate-final --score-run <accepted score-final run directory>"},
        "run_matrix": [{"method": name, "seed": None, "replicate": 1, "stochastic": False,
                        "calibration_status": "not_started", "final_status": "not_started"} for name in METHODS],
        "historical_exposure": json.loads((ROOT / FINAL).read_text())["historical_exposure_disclosure"]}
    write_new(ROOT / CHOICES, value)
    verify_choices(ROOT)
    ledger("model_choices_frozen", record=file_ref(ROOT, ROOT / CHOICES), raw_source_opened=False)
    return {"status": "model_choices_frozen", "record": file_ref(ROOT, ROOT / CHOICES), "methods": len(METHODS)}


def claim_attempt(path, record):
    write_new(path, record)  # Exclusive creation survives success, failure, crash.


def worker(run_dir):
    resolved = json.loads((run_dir / "resolved.json").read_text())
    phase = resolved["phase"]
    limits = Limits(**resolved["limits"])
    effective = install_worker_limits(limits)
    writer = BudgetWriter(run_dir, limit_bytes=limits.output_bytes, reserve_bytes=limits.parent_reserve_bytes)
    diagnostics = {"status": "running", "stage": "worker_admission", "effective_cpu_limits": effective,
                   "started_at_utc": utc()}
    result = 1
    try:
        claim = json.loads((ROOT / f"local/campaign_v0.1/{phase}.attempt.json").read_text())
        if claim["run_directory"] != str(run_dir) or claim["resolved_sha256"] != sha(run_dir / "resolved.json"):
            raise ValueError("Unadmitted private worker")
        writer.write_json("worker_started.json", {"time": utc(), "pid": os.getpid(), "resolved_sha256": sha(run_dir / "resolved.json")})
        study = load_study(ROOT)
        freeze, config, models = verify_choices(ROOT)
        verify_environment(freeze)
        choice_hash = sha(ROOT / CHOICES)
        if choice_hash != resolved["model_selection_sha256"] or asdict(limits) != config["phase_budgets"][phase]:
            raise ValueError("Worker freeze/budgets differ")
        if phase != "calibrate":
            final, _, _, _ = verify_final(ROOT, study)
            if sha(ROOT / FINAL) != resolved["final_freeze_sha256"]:
                raise ValueError("Final freeze changed")
        install_worker_scope(ROOT / study.source_relative_path)
        writer.append_text("access.jsonl", json.dumps({"time": utc(), "event": "feature_replay_started" if phase != "evaluate-final" else "evaluator_admission",
            "phase": phase, "model_selection_sha256": choice_hash}) + "\n")
        print("Starting " + phase + "; frozen methods; one attempt", flush=True)
        if phase in {"calibrate", "score-final"}:
            run_scoring(study, models, writer, diagnostics,
                        partition="normal_calibration" if phase == "calibrate" else "final_replay", choice_hash=choice_hash)
        else:
            score_dir, _ = accepted_run(ROOT, resolved["score_run"], "score-final", choice_hash)
            contract = json.loads((ROOT / "configs/casper_right_arm_contract_v0.1.json").read_text())
            policy = json.loads((ROOT / "configs/casper_right_arm_evaluation_v0.1.json").read_text())
            events = [Event(str(v["event_ordinal_by_recorded_flag"]), *v["row_index_half_open"])
                      for v in contract["annotations"]["positive_events"]]
            run_evaluation(study, score_dir, final["thresholds"], writer, diagnostics,
                           choice_hash=choice_hash, policy=policy, events=events)
        verify_choices(ROOT)
        result = 0
    except Exception as error:
        diagnostics.update(status="failed", failure=f"{type(error).__name__}: {error}")
        print(diagnostics["failure"], flush=True)
    finally:
        diagnostics.update(completed_at_utc=utc(), worker_resources=worker_usage())
        writer.write_json("diagnostics.json", diagnostics)
    return result


def execute(phase, score_run=None):
    study = load_study(ROOT)
    freeze, config, _ = verify_choices(ROOT)
    verify_environment(freeze)
    choice_hash = sha(ROOT / CHOICES)
    if phase != "calibrate":
        verify_final(ROOT, study)
    score_ref = None
    if phase == "evaluate-final":
        if score_run is None:
            raise ValueError("Evaluation requires --score-run")
        score_ref = file_ref(ROOT, score_run / "run.json")
        score_dir, _ = accepted_run(ROOT, score_ref, "score-final", choice_hash)
        validate_seal(score_dir, study, partition="final_replay", choice_hash=choice_hash)
    claim_path = ROOT / f"local/campaign_v0.1/{phase}.attempt.json"
    if claim_path.exists():
        raise ValueError("Phase attempt consumed; preserve failure, no automatic retry")
    limits = Limits(**config["phase_budgets"][phase])
    if shutil.disk_usage(ROOT).free < 2 * limits.output_bytes:
        raise ValueError("Insufficient free output capacity")
    run_dir = ROOT / "experiments/runs" / ("campaign_v0.1_" + phase + "_" + utc().replace(":", "").replace("+", "_"))
    run_dir.mkdir(parents=True, exist_ok=False)
    writer = BudgetWriter(run_dir, limit_bytes=limits.output_bytes)
    resolved = {"phase": phase, "project": "manufacturing", "owner": "Haiqa Mushtaq", "operator": "Codex assistant",
        "created_at_utc": utc(), "model_selection_sha256": choice_hash,
        "final_freeze_sha256": sha(ROOT / FINAL) if phase != "calibrate" else None,
        "command": shlex.join([sys.executable, *sys.argv]), "cwd": str(ROOT),
        "environment": environment(), "limits": asdict(limits), "seed": None, "stochastic": False,
        "methods": list(METHODS), "attempt": 1, "automatic_retry": False, "score_run": score_ref,
        "authorization": "Current user requested freeze, threshold-only calibration and final machinery preparation; final phases require a subsequent explicit execution instruction."}
    writer.write_json("resolved.json", resolved)
    writer.write_text("model_selection_snapshot.json", (ROOT / CHOICES).read_text())
    if phase != "calibrate":
        writer.write_text("final_freeze_snapshot.json", (ROOT / FINAL).read_text())
    claim_attempt(claim_path, {"run_directory": str(run_dir), "claimed_at_utc": utc(), "phase": phase,
                              "resolved_sha256": sha(run_dir / "resolved.json"), "attempt": 1})
    ledger("phase_attempt_claimed", phase=phase, run_directory=str(run_dir.relative_to(ROOT)), choice_hash=choice_hash)
    print(json.dumps({"phase": phase, "run_directory": str(run_dir), "status": "launching"}), flush=True)
    command = [sys.executable, str(Path(__file__).resolve()), "--worker", str(run_dir)]
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONNOUSERSITE="1")
    env.update(freeze["environment"]["thread_environment"])
    try:
        result = supervise(command, cwd=ROOT, output_dir=run_dir, limits=limits, env=env)
    except Exception as error:
        result = {"status": "failed", "reason": f"{type(error).__name__}: {error}"}
    diagnostic_path = run_dir / "diagnostics.json"
    diagnostics = json.loads(diagnostic_path.read_text()) if diagnostic_path.exists() else {}
    accepted = (result.get("status") == "completed" and diagnostics.get("status") == "completed"
                and resource_receipt_admitted(diagnostics.get("worker_resources", {}), limits))
    validation = None
    try:
        verify_choices(ROOT)
        verify_environment(freeze)
        if accepted and phase == "calibrate":
            receipt = validate_calibration(run_dir, study, choice_hash)
            if any(v["count"] != 160473 or v["rank"] != 158869 for v in receipt["thresholds"].values()):
                raise ValueError("Wrong production calibration count/rank")
            validation = "All eleven thresholds independently reconstructed from saved aligned finite scores"
        elif accepted and phase == "score-final":
            validate_seal(run_dir, study, partition="final_replay", choice_hash=choice_hash)
            validation = "All eleven final score streams sealed before any label join"
        elif accepted:
            for name in METHODS:
                report = json.loads((run_dir / (name + ".metrics.json")).read_text())
                if report["coverage"]["eligible_rows"] != 897119 or report["events"]["denominator"] != 8:
                    raise ValueError("Incomplete final report")
            validation = "Every declared report complete"
    except Exception as error:
        accepted, validation = False, f"{type(error).__name__}: {error}"
    artifacts = {p.name: {"sha256": sha(p), "bytes": p.stat().st_size} for p in run_dir.iterdir() if p.is_file()}
    manifest = {"phase": phase, "status": "completed" if accepted else "failed", "accepted": accepted,
        "model_selection_sha256": choice_hash, "created_at_utc": resolved["created_at_utc"], "completed_at_utc": utc(),
        "supervisor": result, "diagnostics": diagnostics, "validation": validation, "artifacts": artifacts,
        "run_matrix": [{"method": m, "seed": None, "replicate": 1, "status": "completed" if accepted else "failed_campaign_admission"} for m in METHODS],
        "final_features_parsed": diagnostics.get("final_features_parsed", "unknown_after_worker_failure" if phase == "score-final" else False),
        "labels_joined": diagnostics.get("labels_joined", "unknown_or_incomplete" if phase == "evaluate-final" else 0), "automatic_retry": False}
    writer.write_json("run.json", manifest)
    ledger("phase_terminal", phase=phase, status=manifest["status"], run=file_ref(ROOT, run_dir / "run.json"),
           actual_resources=diagnostics.get("worker_resources"), outcomes_written=phase == "evaluate-final")
    print(json.dumps({"status": manifest["status"], "run_manifest": str(run_dir / "run.json"), "sha256": sha(run_dir / "run.json")}), flush=True)
    return 0 if accepted else 1


def prepare_final(calibration_run):
    study = load_study(ROOT)
    freeze, config, _ = verify_choices(ROOT)
    verify_environment(freeze)
    if calibration_run is None:
        raise ValueError("--prepare-final requires --calibration-run")
    old = json.loads((ROOT / FINAL).read_text())
    if old["status"] != "pending_prerequisites_not_frozen":
        raise ValueError("Final freeze already populated; no overwrite")
    ref = file_ref(ROOT, calibration_run / "run.json")
    directory, run = accepted_run(ROOT, ref, "calibrate", sha(ROOT / CHOICES))
    calibration = validate_calibration(directory, study, sha(ROOT / CHOICES))
    final = {"schema_version": "2.0", "status": "ready_for_final_execution_not_executed", "project": "manufacturing",
        "owner": "Haiqa Mushtaq", "operator": "Codex assistant", "methods": list(METHODS),
        "model_selection_frozen_at": freeze["created_at_utc"], "calibration_completed_at": run["completed_at_utc"],
        "final_freeze_at": utc(), "campaign_started_at": None, "first_outcome_revealed_at": None,
        "campaign_completed_at": None, "model_selection_record": file_ref(ROOT, ROOT / CHOICES),
        "fitted_artifacts": freeze["fitted_artifacts"], "calibration_run": ref,
        "calibration_receipt": file_ref(ROOT, directory / "calibration.json"), "thresholds": calibration["thresholds"],
        "mask_artifact": freeze["provenance_files"]["mask.json"],
        "passing_synthetic_implementation_test_receipt": freeze["provenance_files"]["test_receipt.json"],
        "source_snapshot": freeze["provenance_files"]["source_snapshot.json"],
        "actual_code_revision_and_dirty_patch": {"git_head": freeze["environment"]["git_head"], "patch": freeze["provenance_files"]["tracked_workspace.patch"]},
        "actual_environment_lock_and_hardware": freeze["provenance_files"]["environment.json"],
        "execution_commands": freeze["execution_commands"], "cwd": str(ROOT), "budgets": config["phase_budgets"],
        "declared_run_matrix": [{"method": name, "seed": None, "replicate": 1, "stochastic": False,
                                "calibration_status": "valid", "final_status": "not_started"} for name in METHODS],
        "declared_stochastic_seeds": [17,42,2026], "stochastic_runs": [],
        "protected_rows_half_open": [864003,1762650], "expected_final_eligible": 897119,
        "historical_exposure_disclosure": freeze["historical_exposure"],
        "protection_enforcement": "tested procedural admission and label-free scorer; logical access chain; no OS blinding",
        "final_execution_authorized_by_this_step": False, "no_further_scientific_selection": True,
        "access_ledger": "local/campaign_v0.1/access.jsonl", "completed_final_runs": [],
        "deviations_and_retries": [], "final_report_artifact": None}
    # Only the previously empty template is replaced. The old bytes are bound in
    # the immutable selection snapshot. All future execution state is external.
    temporary = ROOT / "experiments/.final-freeze-prepared.json"
    write_new(temporary, final)
    temporary.replace(ROOT / FINAL)
    verify_final(ROOT, study)
    ledger("final_freeze_prepared", record=file_ref(ROOT, ROOT / FINAL), final_raw_opened=False)
    return {"status": final["status"], "record": file_ref(ROOT, ROOT / FINAL), "final_raw_opened": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    for option in ("freeze", "calibrate", "prepare-final", "check-final", "score-final", "evaluate-final"):
        group.add_argument("--" + option, action="store_true")
    group.add_argument("--worker", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--test-receipt", type=Path)
    parser.add_argument("--calibration-run", type=Path)
    parser.add_argument("--score-run", type=Path)
    args = parser.parse_args()
    if Path.cwd().resolve() != ROOT or Path(sys.prefix).resolve() != (ROOT / ".venv").resolve() or sys.prefix == sys.base_prefix:
        parser.error("Use manufacturing/.venv from manufacturing project directory")
    if args.worker:
        run_dir = args.worker.resolve()
        if not run_dir.is_relative_to((ROOT / "experiments/runs").resolve()):
            parser.error("Worker path outside run storage")
        return worker(run_dir)
    if args.freeze:
        if args.test_receipt is None:
            parser.error("--freeze needs --test-receipt")
        print(json.dumps(freeze_models(args.test_receipt.resolve())))
    elif args.prepare_final:
        print(json.dumps(prepare_final(args.calibration_run.resolve() if args.calibration_run else None)))
    elif args.check_final:
        final, freeze, _, _ = verify_final(ROOT, load_study(ROOT))
        verify_environment(freeze)
        print(json.dumps({"status": "final_preflight_passed", "methods": len(final["methods"]), "raw_source_opened": False}))
    else:
        phase = "calibrate" if args.calibrate else "score-final" if args.score_final else "evaluate-final"
        return execute(phase, args.score_run.resolve() if args.score_run else None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
