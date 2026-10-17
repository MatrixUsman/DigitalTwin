"""Fresh-process readback with independent score and selection arithmetic."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys
import time

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
sys.path.insert(0, str(PROJECT / "src"))
from mfg_twin.supervisor import BudgetWriter, Limits, supervise, install_worker_limits, worker_usage

LIMITS = Limits(wall_seconds=120, cpu_seconds=90, rss_bytes=1073741824, output_bytes=10485760)


def worker(run, output):
    install_worker_limits(LIMITS)
    import numpy as np
    import tensorflow as tf
    from io_utils import sha256, array_hash, verify_frozen
    from model import load_weights_artifact, predict
    start = time.monotonic()
    checks = []

    def check(name, value): checks.append({"name": name, "passed": bool(value)})

    freeze = json.loads((HERE / "FREEZE.json").read_text())
    verify_frozen(PROJECT, freeze)
    config = freeze["configuration"]
    summary = json.loads((run / "summary.json").read_text())
    supervisor = json.loads((run / "supervisor.json").read_text())
    population = json.loads((run / "population.json").read_text())
    check("supervised_completion", summary["status"] == "completed" and supervisor["status"] == "completed")
    check("full_declared_roster", [x["model"] for x in summary["models"]] == ["mean", "persistence", "ar4", "cnn_seed17", "cnn_seed42", "cnn_seed2026"])
    for key, actual in [("wall_seconds", supervisor["wall_seconds"]), ("cpu_seconds", summary["usage"]["process_cpu_seconds"]), ("rss_bytes", supervisor["sampled_peak_rss_bytes"])]:
        check("resource:" + key, actual < config["limits"][key])
    check("actual_output_cap", sum(p.stat().st_size for p in run.iterdir() if p.is_file()) < config["limits"]["output_bytes"])
    check("no_threshold_or_attack_metric", summary["thresholds"] is None and summary["attack_metrics"] is None and not summary["final_access"])
    with np.load(run / "prepared_development.npz", allow_pickle=False) as arrays:
        values, indices, raw_indices = arrays["values"], arrays["indices"], arrays["raw_indices"]
        mean, scale = arrays["mean"], arrays["scale"]
    check("development_population_size", len(values) == config["development_raw_stop"] - config["training_raw_stop"])
    check("coordinates", np.array_equal(raw_indices, indices + config["training_raw_stop"]))
    potential = np.arange(config["history"], len(values))
    excluded = population["development"]["excluded_local_endpoints"]
    check("coverage_and_exclusions", np.array_equal(indices, np.setdiff1d(potential, excluded)))
    check("development_array_hash", array_hash(values) == population["development_values_sha256"])
    check("development_index_hash", array_hash(raw_indices) == population["development_indices_sha256"])
    check("finite_transform", np.isfinite(values).all() and np.isfinite(mean).all() and np.isfinite(scale).all() and np.all(scale > 0))
    targets = values[indices].astype(np.float64)
    with np.load(run / "ar_coefficients.npz", allow_pickle=False) as arrays:
        ar = arrays["coefficients"]
    # Independent dense design assembly, unlike the streaming fit/predict code.
    ar_design = np.column_stack([np.stack([values[i - 4:i].reshape(-1) for i in indices]).astype(np.float64), np.ones(len(indices))])
    for record in summary["models"]:
        name = record["model"]
        artifact = run / record["score_artifact"]
        check(name + ":score_hash", sha256(artifact) == record["score_artifact_sha256"])
        with np.load(artifact, allow_pickle=False) as arrays:
            predictions, scores, native = arrays["predictions"], arrays["scores"], arrays["native_scores"]
            check(name + ":same_support", np.array_equal(arrays["raw_indices"], raw_indices))
        check(name + ":shape_finite", predictions.shape == targets.shape and np.isfinite(predictions).all() and np.isfinite(scores).all())
        errors = predictions.astype(np.float64) - targets
        squared = errors * errors
        native_squared = squared * scale * scale
        check(name + ":point_scores", np.allclose(scores ** 2, np.sum(squared, axis=1) / 9, rtol=1e-12, atol=1e-14))
        check(name + ":native_scores", np.allclose(native ** 2, np.sum(native_squared, axis=1) / 9, rtol=1e-12, atol=1e-10))
        check(name + ":mse", np.isclose(record["standardized_mse"], np.sum(squared) / targets.size, rtol=1e-12, atol=1e-14))
        check(name + ":channel_mse", np.allclose(record["channel_standardized_mse"], np.sum(squared, axis=0) / len(indices), rtol=1e-12, atol=1e-14))
        if name == "mean": check(name + ":semantics", np.array_equal(predictions, np.zeros_like(targets)))
        elif name == "persistence": check(name + ":semantics", np.array_equal(predictions, values[indices - 1]))
        elif name == "ar4": check(name + ":semantics", np.allclose(predictions, ar_design @ ar, rtol=1e-10, atol=1e-10))
        else:
            path = run / record["weight_artifact"]
            check(name + ":weight_hash", sha256(path) == record["weight_artifact_sha256"])
            best, selected, stale, stop_at = float("inf"), 0, 0, None
            for epoch, row in enumerate(record["history"], 1):
                accepted = row["development_mse"] < best - config["cnn"]["minimum_improvement"]
                check(name + f":epoch{epoch}_choice", row["epoch"] == epoch and row["accepted_checkpoint"] == accepted)
                if accepted: best, selected, stale = row["development_mse"], epoch, 0
                else: stale += 1
                if stale >= config["cnn"]["early_stopping_patience"]:
                    stop_at = epoch
                    break
            check(name + ":selected_checkpoint", selected == record["selected_epoch"] and abs(best - record["standardized_mse"]) < 1e-12)
            check(name + ":stopping", record["epochs_completed"] == (stop_at or config["cnn"]["maximum_epochs"]))
            model = load_weights_artifact(config, path)
            replay = predict(model, values, indices, config["history"], config["cnn"]["batch_size"])
            check(name + ":fresh_process_inference", np.array_equal(predictions, replay))
            del model
            tf.keras.backend.clear_session()
    guards = json.loads((PROJECT / "local/baseline_training_v0.3/starting_guard.json").read_text())
    old = guards["old_campaign"]
    for path, expected in old["frozen_source"].items(): check("old_source:" + path, sha256(PROJECT / path) == expected)
    for item in old["frozen_inputs"]:
        if "datasets/raw" in item["path"]: raise ValueError("Old raw observations outside verification scope")
        check("old_input:" + item["path"], sha256(PROJECT / item["path"]) == item["sha256"])
    for filename, key in [("MODEL_SELECTION_FREEZE_V0.1.json", "selection_sha256"), ("FINAL_TEST_FREEZE_RECORD.json", "final_freeze_sha256"), ("FINAL_CAMPAIGN_V0.1_RECORD.json", "final_record_sha256")]:
        check("old_freeze:" + filename, sha256(PROJECT / "experiments" / filename) == old[key])
    check("old_pdf", sha256(PROJECT / "output/pdf/correction-evidence-casper-study.pdf") == "c849f75b14b913646b1f756e5f73cf211163dc590216db693cd0d7cb72a4bd6f")
    check("v02_manifest", sha256(PROJECT / "research_cycles/contribution_v0.2/EVIDENCE_MANIFEST.json") == guards["v02_manifest_sha256"])
    for path, expected in guards["v02_files"].items(): check("v02:" + path, sha256(PROJECT / path) == expected)
    result = {"status": "passed" if all(c["passed"] for c in checks) else "failed", "checks": checks,
              "passed": sum(c["passed"] for c in checks), "total": len(checks),
              "utc": datetime.now(timezone.utc).isoformat(), "command": sys.argv,
              "wall_seconds": time.monotonic() - start, "usage": worker_usage(),
              "verification_source_sha256": sha256(Path(__file__)), "freeze_sha256": sha256(HERE / "FREEZE.json"),
              "run_artifact_sha256": {p.name: sha256(p) for p in sorted(run.iterdir()) if p.is_file()},
              "scope": "fresh-process inference, independent score/selection arithmetic and immutable-history checks; no fitting or raw parse"}
    BudgetWriter(output, limit_bytes=LIMITS.output_bytes, reserve_bytes=LIMITS.parent_reserve_bytes).write_json("verification.json", result)
    print(json.dumps({k: result[k] for k in ["status", "passed", "total", "wall_seconds"]}, indent=2))
    if result["status"] != "passed":
        print([c for c in checks if not c["passed"]])
        raise SystemExit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("--run", required=True); parser.add_argument("--attempt", required=True)
    parser.add_argument("--worker", action="store_true")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_]+", args.run) or not re.fullmatch(r"[A-Za-z0-9_]+", args.attempt): raise ValueError("Invalid identifier")
    run = PROJECT / "local/baseline_training_v0.3/runs" / args.run
    output = PROJECT / "local/baseline_training_v0.3/verification" / args.attempt
    if args.worker:
        worker(run, output)
    else:
        output.mkdir(parents=True, exist_ok=False)
        command = [sys.executable, str(Path(__file__).resolve()), "--run", args.run, "--attempt", args.attempt, "--worker"]
        outcome = supervise(command, cwd=PROJECT, output_dir=output, limits=LIMITS,
                            env={"TF_NUM_INTRAOP_THREADS": "1", "TF_NUM_INTEROP_THREADS": "1", "TF_CPP_MIN_LOG_LEVEL": "2",
                                 "CUDA_VISIBLE_DEVICES": "-1", "OPENBLAS_NUM_THREADS": "1", "OMP_NUM_THREADS": "1"})
        BudgetWriter(output, limit_bytes=LIMITS.output_bytes).write_json("supervisor.json", outcome)
        print(json.dumps(outcome, indent=2))
        raise SystemExit(0 if outcome["status"] == "completed" else 1)
