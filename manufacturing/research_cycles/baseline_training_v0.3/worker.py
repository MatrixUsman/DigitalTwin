"""Execute all fixed controls/seeds on the permitted nominal prefix only."""
import argparse
from datetime import datetime, timezone
import gc
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import time
import traceback

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
sys.path.insert(0, str(PROJECT / "src"))
from mfg_twin.supervisor import BudgetWriter, Limits, install_worker_limits, worker_usage


def main(output):
    config = json.loads((HERE / "config.json").read_text())
    limits = Limits(**config["limits"])
    install_worker_limits(limits)
    writer = BudgetWriter(output, limit_bytes=limits.output_bytes, reserve_bytes=limits.parent_reserve_bytes)
    start, wall_start = datetime.now(timezone.utc).isoformat(), time.monotonic()
    import numpy as np
    import tensorflow as tf
    from core import prepare, batches, score_predictions, fit_ar, predict_ar, EarlyStop
    from model import make_model, predict, weights_bytes, load_weights_artifact
    from io_utils import sha256, array_hash, npz_bytes, load_prefix, verify_frozen
    freeze = json.loads((HERE / "FREEZE.json").read_text()); verify_frozen(PROJECT, freeze)
    provenance = {"study_id": config["study_id"], "start_utc": start, "command": sys.argv,
                  "cwd": str(Path.cwd()), "owner": "Haiqa Mushtaq", "operator": "Codex",
                  "interpreter": sys.version, "platform": platform.platform(),
                  "tensorflow": tf.__version__, "numpy": np.__version__, "configuration": config,
                  "freeze_sha256": sha256(HERE / "FREEZE.json"), "source_sha256": freeze["source_sha256"],
                  "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
                  "git_status": subprocess.check_output(["git", "status", "--porcelain"], text=True),
                  "threads": {"tensorflow_intra": 1, "tensorflow_inter": 1, "blas": 1},
                  "hardware_receipt": "local/contribution_v0.2/hardware_snapshot_authorized.json",
                  "hardware_receipt_sha256": sha256(PROJECT / "local/contribution_v0.2/hardware_snapshot_authorized.json")}
    writer.write_json("provenance.json", provenance)
    writer.write_json("data_access.json", {"utc": datetime.now(timezone.utc).isoformat(),
                                          "path": config["data_path"], "identity_hash_reads_whole_nominal_file": True,
                                          "maximum_parsed_numeric_rows": config["development_raw_stop"],
                                          "selected_rows": [config["raw_start"], config["development_raw_stop"]],
                                          "attack_files": [], "calibration_access": False, "final_access": False})
    frame = load_prefix(PROJECT / config["data_path"], config["data_sha256"], config["development_raw_stop"], config["columns"])
    frame = frame.iloc[config["raw_start"]:config["development_raw_stop"]]
    data = prepare(frame[config["columns"]].to_numpy(), frame["time"].to_numpy(),
                   config["training_raw_stop"] - config["raw_start"], config["history"],
                   config["gap_multiple"], config["minimum_coverage"])
    del frame
    train, dev = data["training"], data["development"]
    ti, di, scaler = data["training_indices"], data["development_indices"], data["scaler"]
    target = dev[di]
    scaler_digest = array_hash(scaler.mean) + array_hash(scaler.scale)
    writer.write_bytes("prepared_development.npz", npz_bytes(values=dev, indices=di, raw_indices=di + config["training_raw_stop"], mean=scaler.mean, scale=scaler.scale))
    writer.write_json("population.json", {"training": data["training_coverage"], "development": data["development_coverage"],
                                         "training_indices_sha256": array_hash(ti + config["raw_start"]),
                                         "development_indices_sha256": array_hash(di + config["training_raw_stop"]),
                                         "training_values_sha256": array_hash(train), "development_values_sha256": array_hash(dev),
                                         "median_training_increment_native": data["median_training_increment"],
                                         "maximum_gap_native": data["maximum_gap"], "clock_unit": "unresolved"})
    model_results = []

    def retain_result(name, predictions, cost, extra=None):
        score, native_score, metrics = score_predictions(predictions, target, scaler.scale)
        filename = name + "_scores.npz"
        writer.write_bytes(filename, npz_bytes(predictions=predictions, scores=score, native_scores=native_score,
                                              raw_indices=di + config["training_raw_stop"]))
        record = {"model": name, **metrics, **cost, "score_artifact": filename,
                  "score_artifact_sha256": sha256(output / filename), **(extra or {})}
        model_results.append(record)
        writer.write_json(name + "_record.json", record)
        return record

    for name in ["mean", "persistence"]:
        clock, cpu = time.monotonic(), time.process_time()
        predictions = np.zeros_like(target) if name == "mean" else dev[di - 1].copy()
        retain_result(name, predictions, {"fit_wall_seconds": 0.0, "score_wall_seconds": time.monotonic() - clock,
                                         "score_cpu_seconds": time.process_time() - cpu}, {"seed": None})
    clock, cpu = time.monotonic(), time.process_time()
    coefficients = fit_ar(train, ti, config["ar"]["order"], config["ar"]["ridge"], config["cnn"]["batch_size"])
    fit_wall, fit_cpu = time.monotonic() - clock, time.process_time() - cpu
    writer.write_bytes("ar_coefficients.npz", npz_bytes(coefficients=coefficients))
    clock, cpu = time.monotonic(), time.process_time()
    predictions = predict_ar(dev, di, coefficients, config["ar"]["order"], config["cnn"]["batch_size"])
    retain_result("ar4", predictions, {"fit_wall_seconds": fit_wall, "fit_cpu_seconds": fit_cpu,
                                      "score_wall_seconds": time.monotonic() - clock, "score_cpu_seconds": time.process_time() - cpu},
                  {"seed": None, "coefficient_sha256": sha256(output / "ar_coefficients.npz")})

    writer.write_text("learning_curves.csv", "seed,epoch,training_mse,development_mse,accepted_checkpoint,epoch_wall_seconds,epoch_cpu_seconds\n")
    cnn = config["cnn"]
    for seed in config["seeds"]:
        tf.keras.backend.clear_session(); gc.collect()
        model = make_model(config, seed)
        selection = EarlyStop(cnn["early_stopping_patience"], cnn["minimum_improvement"])
        best_weights, history = None, []
        fit_start, cpu_start = time.monotonic(), time.process_time()
        train_prediction = predict(model, train, ti, config["history"], cnn["batch_size"])
        dev_prediction = predict(model, dev, di, config["history"], cnn["batch_size"])
        train_loss = score_predictions(train_prediction, train[ti], scaler.scale)[2]["standardized_mse"]
        dev_loss = score_predictions(dev_prediction, target, scaler.scale)[2]["standardized_mse"]
        writer.append_text("learning_curves.csv", f"{seed},0,{train_loss:.17g},{dev_loss:.17g},0,0,0\n")
        del train_prediction, dev_prediction
        for epoch in range(1, cnn["maximum_epochs"] + 1):
            epoch_start, epoch_cpu = time.monotonic(), time.process_time()
            model.reset_metrics()
            for x, y in batches(train, ti, config["history"], cnn["batch_size"]):
                model.train_on_batch(x, y[:, None, :])
            weight_hash_before = hashlib.sha256(b"".join(w.tobytes() for w in model.get_weights())).hexdigest()
            train_prediction = predict(model, train, ti, config["history"], cnn["batch_size"])
            dev_prediction = predict(model, dev, di, config["history"], cnn["batch_size"])
            train_loss = score_predictions(train_prediction, train[ti], scaler.scale)[2]["standardized_mse"]
            dev_loss = score_predictions(dev_prediction, target, scaler.scale)[2]["standardized_mse"]
            weight_hash_after = hashlib.sha256(b"".join(w.tobytes() for w in model.get_weights())).hexdigest()
            if weight_hash_before != weight_hash_after: raise ValueError("Evaluation mutated fitted weights")
            accepted, stop = selection.observe(epoch, dev_loss)
            if accepted: best_weights = [w.copy() for w in model.get_weights()]
            row = {"epoch": epoch, "training_mse": train_loss, "development_mse": dev_loss,
                   "accepted_checkpoint": accepted, "wall_seconds": time.monotonic() - epoch_start,
                   "cpu_seconds": time.process_time() - epoch_cpu}
            history.append(row)
            writer.append_text("learning_curves.csv", f"{seed},{epoch},{train_loss:.17g},{dev_loss:.17g},{int(accepted)},{row['wall_seconds']:.9f},{row['cpu_seconds']:.9f}\n")
            if epoch == 1 or epoch % 5 == 0 or stop:
                print(f"seed={seed} epoch={epoch} train_mse={train_loss:.6f} dev_mse={dev_loss:.6f} best_epoch={selection.best_epoch}", flush=True)
            del train_prediction, dev_prediction
            if stop: break
        fit_wall, fit_cpu = time.monotonic() - fit_start, time.process_time() - cpu_start
        if best_weights is None: raise ValueError("No selected checkpoint")
        model.set_weights(best_weights)
        name = f"cnn_seed{seed}"
        weight_filename = name + "_weights.npz"
        writer.write_bytes(weight_filename, weights_bytes(model))
        clock, cpu = time.monotonic(), time.process_time()
        prediction = predict(model, dev, di, config["history"], cnn["batch_size"])
        score_wall, score_cpu = time.monotonic() - clock, time.process_time() - cpu
        restored = load_weights_artifact(config, output / weight_filename)
        restored_prediction = predict(restored, dev, di, config["history"], cnn["batch_size"])
        if not np.array_equal(prediction, restored_prediction): raise ValueError("Saved checkpoint inference parity failed")
        record = retain_result(name, prediction, {"fit_wall_seconds": fit_wall, "fit_cpu_seconds": fit_cpu,
                                                  "score_wall_seconds": score_wall, "score_cpu_seconds": score_cpu},
                               {"seed": seed, "epochs_completed": len(history), "selected_epoch": selection.best_epoch,
                                "parameters": model.count_params(), "stopping_reason": "normal_development_patience" if stop else "maximum_epochs",
                                "weight_artifact": weight_filename, "weight_artifact_sha256": sha256(output / weight_filename),
                                "saved_model_inference_parity": True, "history": history})
        if abs(record["standardized_mse"] - selection.best_loss) > 1e-12: raise ValueError("Selected loss mismatch")
        print(f"completed {name}: epoch={selection.best_epoch} dev_mse={record['standardized_mse']:.6f}", flush=True)
        del model, restored, prediction, restored_prediction, best_weights
        gc.collect()

    if scaler_digest != array_hash(scaler.mean) + array_hash(scaler.scale): raise ValueError("Scaler changed")
    verify_frozen(PROJECT, freeze)
    summary = {"study_id": config["study_id"], "status": "completed", "data_sha256": config["data_sha256"],
               "training_targets": len(ti), "development_targets": len(di), "models": model_results,
               "scaler_unchanged": True, "attack_metrics": None, "thresholds": None, "final_access": False,
               "start_utc": start, "end_utc": datetime.now(timezone.utc).isoformat(),
               "worker_wall_seconds": time.monotonic() - wall_start, "usage": worker_usage(),
               "interpretation": "Normal-development baseline training; independent implementation and all seeds retained"}
    writer.write_json("summary.json", summary)
    print("Complete: all three CNN seeds and three deterministic controls saved.", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    expected_parent = (PROJECT / "local/baseline_training_v0.3/runs").resolve()
    if args.output.resolve().parent != expected_parent or not args.output.is_dir():
        raise ValueError("Output must be a launcher-created attempt directory")
    try:
        main(args.output)
    except Exception:
        # Supervisor also preserves stderr/exit status. Keep a structured failure if space allows.
        try:
            config = json.loads((HERE / "config.json").read_text())
            BudgetWriter(args.output, limit_bytes=config["limits"]["output_bytes"], reserve_bytes=1048576).write_json(
                "failure.json", {"utc": datetime.now(timezone.utc).isoformat(), "traceback": traceback.format_exc()})
        except Exception:
            pass
        raise
