"""Independent saved-array audit; no imports from decomposition implementation."""
from pathlib import Path
import hashlib
import json
import math
import platform
import sys
from datetime import datetime, timezone

import numpy as np

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
RUN = PROJECT / "local/novelty_v0.22/decomposition_001"
checks = 0
scalar_parities = 0
maximum_log_error = 0.0
maximum_score_relative_error = 0.0
total_zero_scores = 0
read_arrays = []


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def insist(value, description):
    global checks
    checks += 1
    if not value:
        raise AssertionError(description)


def close(actual, expected, description, tolerance=1e-12):
    if expected is None:
        insist(actual is None, description)
    else:
        insist(math.isclose(actual, expected, rel_tol=tolerance, abs_tol=tolerance),
               f"{description}: {actual!r} != {expected!r}")


def mean(values):
    # A separate reduction from the implementation's ndarray.mean.
    return math.fsum(float(v) for v in values) / len(values)


manifest_path = HERE / "INPUT_MANIFEST.json"
freeze_path = HERE / "FREEZE.json"
summary_path = RUN / "episode_summary.json"
sealed_path = RUN / "DECOMPOSITION_SEALED.json"
manifest = json.loads(manifest_path.read_text())
freeze = json.loads(freeze_path.read_text())
claimed = json.loads(summary_path.read_text())
sealed = json.loads(sealed_path.read_text())
config_path = PROJECT / "research_cycles/context_recovery_v0.19/config.json"
tasks = {r["id"]: r for r in json.loads(config_path.read_text())["tasks"]}
claimed_by_id = {r["id"]: r for r in claimed}
episodes = manifest["episodes"]
insist(len(episodes) == len(claimed) == len(claimed_by_id) == 36, "complete 36-episode population")
expected_ids = {f"{task}_Q1_{seed}_{condition}" for task in ("L19", "S19")
                for seed in (17, 42, 2026)
                for condition in ("normal", "authorized_changes", "brief_offset", "persistent_offset", "hold", "slow")}
insist({r["id"] for r in episodes} == expected_ids == set(claimed_by_id), "full factorial identities")
for path, expected in freeze["bindings"].items():
    insist(digest(PROJECT / path) == expected, "frozen input identity: " + path)
for name, expected in sealed["bindings"].items():
    insist(digest(RUN / name) == expected, "sealed output identity: " + name)

rows = 0
eligible_rows = 0
recomputed = []
for episode in episodes:
    name = episode["id"]
    supplied = claimed_by_id[name]
    count = 6000 if episode["condition"] in ("normal", "authorized_changes") else 2400
    output_path = RUN / ("decomposition_" + name + ".npz")
    old_path = PROJECT / episode["prior_rapt_score_path"]
    with np.load(output_path, allow_pickle=False) as archive:
        insist(set(archive.files) == {"mean", "logvar", "squared_error", "loss", "defined", "eligible"}, name + " members")
        values = {k: archive[k].copy() for k in archive.files}
    with np.load(old_path, allow_pickle=False) as archive:
        old_loss = archive["loss"]
    read_arrays.extend([{"path": str(output_path.relative_to(PROJECT)), "members": sorted(values)},
                        {"path": str(old_path.relative_to(PROJECT)), "members": ["loss"]}])
    for key in ("mean", "logvar", "squared_error", "loss"):
        insist(values[key].shape == (count, 4), name + " shape " + key)
        insist(values[key].dtype == np.float32, name + " dtype " + key)
        insist(np.isfinite(values[key]).all(), name + " finite " + key)
        insist(np.all(values[key][0] == 0), name + " undefined padding " + key)
    insist(values["defined"].dtype == np.bool_ and np.array_equal(values["defined"], np.arange(count) > 0), name + " score-defined mask")
    insist(values["eligible"].dtype == np.bool_ and np.array_equal(values["eligible"], np.arange(count) >= 100), name + " eligibility mask")
    insist(old_loss.dtype == values["loss"].dtype and old_loss.shape == values["loss"].shape, name + " original shape/type")
    insist(old_loss.tobytes() == values["loss"].tobytes(), name + " byte-exact original score parity")
    scalar_parities += old_loss.size
    rows += count
    eligible_rows += int(values["eligible"].sum())
    insist(np.all(values["squared_error"] >= 0) and np.all(values["loss"] >= 0), name + " nonnegative values")
    insist(np.all(np.abs(values["logvar"][1:]) <= 6), name + " released variance clamp")
    calc = values["squared_error"][1:].astype(float) / np.exp(values["logvar"][1:].astype(float))
    supplied_score = values["loss"][1:].astype(float)
    denominator = np.maximum(np.abs(calc), np.finfo(float).tiny)
    err = float(np.max(np.abs(calc - supplied_score) / denominator))
    maximum_score_relative_error = max(maximum_score_relative_error, err)
    insist(np.allclose(calc, supplied_score, rtol=3e-7, atol=0), name + " released score algebra")
    total_zero_scores += int(np.count_nonzero(values["loss"][100:] == 0))
    if episode["condition"] in ("normal", "authorized_changes"):
        beginning, end = 100, count
        expected_definition = "full eligible benign episode"
    else:
        schedule = tasks[episode["task"]]
        beginning = schedule["onset"]
        end = beginning + schedule["brief" if episode["condition"] == "brief_offset" else "duration"]
        expected_definition = "frozen v0.19 command-intervention schedule"
    quarter = (end - beginning) // 4
    regions = {"eligible_all": (100, count), "first": (beginning, beginning + quarter), "last": (end - quarter, end)}
    insist(supplied["interval_definition"] == expected_definition, name + " interval definition")
    local = {"id": name, "task": episode["task"], "condition": episode["condition"], "seed": episode["seed"]}
    for label, (lo, hi) in regions.items():
        region = supplied[label]
        insist((region["lo"], region["hi"], region["points"]) == (lo, hi, hi - lo), name + " " + label + " boundaries")
        insist(len(region["channels"]) == 4, name + " " + label + " channel count")
        local[label] = []
        for channel in range(4):
            row = region["channels"][channel]
            insist(row["channel"] == channel and row["points"] == hi - lo, name + " channel identity/count")
            prediction, lv, se, loss = [values[k][lo:hi, channel].astype(float) for k in ("mean", "logvar", "squared_error", "loss")]
            computed = {"mean_prediction": mean(prediction), "mean_log_variance": mean(lv),
                        "mean_variance": mean(np.exp(lv)), "mean_squared_error": mean(se), "mean_score": mean(loss)}
            for key, number in computed.items():
                close(row[key], number, f"{name}/{label}/{channel}/{key}")
            positive = (se > 0) & (loss > 0)
            npositive = int(positive.sum())
            logs = row["log_decomposition"]
            insist(logs["points"] == npositive and logs["excluded_zero"] == len(positive) - npositive, name + " positive log support")
            if npositive:
                log_loss, log_se, log_var = np.log(loss[positive]), np.log(se[positive]), lv[positive]
                rounding = float(np.max(np.abs(log_loss - log_se + log_var)))
                maximum_log_error = max(maximum_log_error, rounding)
                insist(rounding <= 2e-5, name + " per-element log identity")
                log_values = {"mean_log_score": mean(log_loss), "mean_log_squared_error": mean(log_se),
                              "mean_log_variance": mean(log_var), "max_identity_roundoff": rounding}
            else:
                log_values = {k: None for k in ("mean_log_score", "mean_log_squared_error", "mean_log_variance", "max_identity_roundoff")}
            for key, number in log_values.items():
                close(logs[key], number, f"{name}/{label}/{channel}/log/{key}")
            computed["log"] = log_values
            computed["positive"] = npositive
            local[label].append(computed)
    local["deltas"] = []
    for channel, change in enumerate(supplied["log_changes"]):
        first, last = local["first"][channel], local["last"][channel]
        insist(change["channel"] == channel and change["first_positive"] == first["positive"] and change["last_positive"] == last["positive"], name + " difference support")
        delta = {}
        for key in ("mean_log_score", "mean_log_squared_error", "mean_log_variance"):
            number = last["log"][key] - first["log"][key] if first["positive"] and last["positive"] else None
            close(change["delta_" + key], number, name + " difference " + key)
            delta[key] = number
        if first["positive"] and last["positive"]:
            close(delta["mean_log_score"], delta["mean_log_squared_error"] - delta["mean_log_variance"], name + " difference log identity", tolerance=4e-5)
        local["deltas"].append(delta)
    recomputed.append(local)

insist(rows == 129600 and eligible_rows == 126000 and scalar_parities == 518400, "population totals")
result = json.loads((RUN / "result.json").read_text())
for key, expected in {"episodes": 36, "rows": rows, "eligible_rows": eligible_rows, "original_loss_scalar_parity": scalar_parities}.items():
    insist(result[key] == expected, "result " + key)
insist(result["status"] == "completed" and not result["training"] and not result["fresh_confirmation"] and not result["novelty_established"], "result interpretation flags")
supervisor = json.loads((RUN / "supervisor.json").read_text())
insist(supervisor["status"] == "completed" and supervisor["attempts"] == 1 and supervisor["returncode"] == 0, "supervisor completion")
insist(supervisor["wall_seconds"] <= 60 and result["usage"]["process_cpu_seconds"] <= 45 and supervisor["sampled_peak_rss_bytes"] <= 2**30 and supervisor["output_bytes"] <= 25*2**20, "resource bounds")
insist(supervisor["rss_samples"] > 0, "active memory monitoring")

table = []
for task in ("L19", "S19"):
    group = [r for r in recomputed if r["task"] == task and r["condition"] == "persistent_offset"]
    insist(len(group) == 3, "persistent case count " + task)
    for channel in range(4):
        row = {"task": task, "channel": channel, "episodes": len(group)}
        for key in ("mean_log_score", "mean_log_squared_error", "mean_log_variance"):
            v = [r["deltas"][channel][key] for r in group]
            row["median_delta_" + key] = float(np.median(v))
            row["negative_count_" + key] = sum(x < 0 for x in v)
        # Medians of the three components are descriptive and need not add exactly.
        table.append(row)

bindings = {str(p.relative_to(PROJECT)): digest(p) for p in [Path(__file__), manifest_path, freeze_path, summary_path, sealed_path, config_path, RUN/"result.json", RUN/"supervisor.json"]}
receipt = {"utc": datetime.now(timezone.utc).isoformat(), "status": "passed", "checks": checks,
           "episodes": 36, "rows": rows, "eligible_rows": eligible_rows, "byte_exact_original_loss_values": scalar_parities,
           "maximum_log_identity_error": maximum_log_error, "maximum_score_relative_error": maximum_score_relative_error,
           "eligible_zero_score_values": total_zero_scores, "persistent_offset_descriptive_table": table,
           "interpreter": sys.executable, "python": sys.version, "numpy": np.__version__, "platform": platform.platform(),
           "cwd": str(PROJECT), "command": "PYTHONDONTWRITEBYTECODE=1 .venv-analysis-v022/bin/python research_cycles/novelty_v0.22/decomposition/reviewer_verify.py",
           "source_imports": ["Python standard library", "numpy"], "decomposition_core_imported": False,
           "learned_model_inference": False, "truth_arrays_opened": False, "new_observations": False,
           "scope": "saved array/parity/summary audit; no independent neural prediction reconstruction or physical-truth audit",
           "frozen_input_bindings": len(freeze["bindings"]), "sealed_array_bindings": len(sealed["bindings"]),
           "bindings": bindings, "array_access": read_arrays}
destination = HERE / "REVIEWER_VERIFICATION.json"
with destination.open("x") as stream:
    json.dump(receipt, stream, indent=2, allow_nan=False)
    stream.write("\n")
print(json.dumps({k: receipt[k] for k in ("status", "checks", "byte_exact_original_loss_values", "maximum_log_identity_error", "eligible_zero_score_values", "persistent_offset_descriptive_table")}, indent=2))
