"""Execute the single explicitly authorized normal-only pilot, without retries.

From manufacturing: .venv/bin/python scripts/run_bounded_pilot.py --execute
    --test-receipt local/software_validation/<id>/receipt.json
The worker is private to this supervisor; it cannot be run without a matching
attempt ledger and resolved run record. This is procedural, not OS isolation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shlex
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from importlib.metadata import distributions
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mfg_twin.supervisor import BudgetWriter, Limits, install_worker_limits, supervise, worker_usage


def utc():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def admission_files():
    return sorted({*ROOT.joinpath("src").rglob("*.py"),
                   *ROOT.joinpath("tests").rglob("*.py"),
                   *ROOT.joinpath("tests/fixtures").rglob("*.json"),
                   ROOT / "scripts/run_synthetic_tests.py", Path(__file__).resolve(),
                   ROOT / "pyproject.toml",
                   *ROOT.joinpath("configs").glob("casper_right_arm_*.json")})


def validate_test_receipt(path):
    receipt = json.loads(path.read_text())
    if (receipt.get("kind") != "synthetic_software_validation_not_benchmark"
            or receipt.get("success") is not True or receipt.get("failures") != 0
            or receipt.get("errors") != 0 or receipt.get("skips") != 0
            or type(receipt.get("tests_run")) is not int or receipt["tests_run"] <= 0
            or receipt.get("expected_failures") != 0 or receipt.get("unexpected_successes") != 0
            or receipt.get("raw_dataset_opened") is not False or receipt.get("trained_models") is not False
            or receipt.get("source_changed_during_tests") != []
            or receipt.get("executable") != sys.executable
            or receipt.get("python") != sys.version):
        raise ValueError("A successful current-interpreter synthetic test receipt is required")
    files = admission_files()
    if set(receipt["source_sha256_at_start"]) != {str(path.relative_to(ROOT)) for path in files}:
        raise ValueError("Tested implementation inventory differs from current files")
    for path in files:
        relative = str(path.relative_to(ROOT))
        if receipt["source_sha256_at_start"].get(relative) != digest(path):
            raise ValueError(f"Untested or changed implementation: {relative}")
    return receipt


def claim_worker_start(writer, resolved_hash):
    """Exclusive immutable start token: direct private-worker repeats fail too."""
    writer.write_json("worker_started.json", {"attempt": 1, "pid": os.getpid(),
                      "started_at_utc": utc(), "resolved_config_sha256": resolved_hash})


def install_worker_scope(source):
    """Process-local guard; source parsing limits are enforced by the wrapper."""
    allowed = source.resolve()

    def guard(event, args):
        if event.startswith("socket.") or event in {"subprocess.Popen", "os.system", "os.fork", "os.posix_spawn", "os.exec"}:
            raise PermissionError("Pilot worker forbids network and child processes")
        if event == "open" and isinstance(args[0], (str, bytes)):
            path = Path(os.fsdecode(args[0])).resolve()
            if path == allowed or any(a == "datasets" and b == "raw" for a, b in zip(path.parts, path.parts[1:])):
                mode, flags = args[1], args[2]
                if (path != allowed or (mode and any(c in mode for c in "wax+"))
                        or flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC)):
                    raise PermissionError("Pilot raw source is read-only; other members forbidden")
    sys.addaudithook(guard)


def worker(run_dir):
    limits = Limits()
    effective_limits = install_worker_limits(limits)
    writer = BudgetWriter(run_dir, limit_bytes=limits.output_bytes,
                          reserve_bytes=limits.parent_reserve_bytes)
    diagnostics = {"status": "running", "stage": "worker_admission", "effective_cpu_limits": effective_limits}
    started = utc()
    result = 1
    try:
        from mfg_twin.contract import load_study
        from mfg_twin.pilot import PILOT_SHA256, load_pilot_plan, run_pilot
        resolved = json.loads((run_dir / "resolved_config.json").read_text())
        if (sys.executable != resolved["executable"] or sys.version != resolved["python"]
                or sys.prefix != resolved["prefix"] or str(Path.cwd().resolve()) != resolved["cwd"]):
            raise ValueError("Worker interpreter/environment/cwd differs from admitted provenance")
        claim = json.loads((ROOT / "local/pilot_attempts/casper_right_arm_pilot_v0.1.json").read_text())
        if (claim["run_directory"] != str(run_dir)
                or claim["resolved_config_sha256"] != digest(run_dir / "resolved_config.json")
                or resolved["pilot_specification_sha256"] != PILOT_SHA256
                or resolved["attempt"] != 1):
            raise ValueError("Worker attempt/configuration was not admitted")
        for name, expected in resolved["source_sha256"].items():
            if digest(ROOT / name) != expected:
                raise ValueError(f"Implementation changed before worker: {name}")
        claim_worker_start(writer, digest(run_dir / "resolved_config.json"))
        study = load_study(ROOT)
        plan = load_pilot_plan(ROOT)
        install_worker_scope(ROOT / study.source_relative_path)
        print("Starting one normal-only pilot; no calibration or final parsing", flush=True)
        run_pilot(study, plan, writer, diagnostics)
        result = 0
    except Exception as error:
        diagnostics.update(status="failed", failure_reason=f"{type(error).__name__}: {error}")
        print(f"Pilot failed at {diagnostics['stage']}: {type(error).__name__}: {error}", flush=True)
    finally:
        diagnostics.update(worker_started_at_utc=started, worker_completed_at_utc=utc(),
                           worker_resources=worker_usage())
        writer.write_json("diagnostics.json", diagnostics)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--execute", action="store_true")
    group.add_argument("--worker", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--test-receipt", type=Path)
    args = parser.parse_args()
    if args.worker:
        run_dir = args.worker.resolve()
        if not run_dir.is_relative_to((ROOT / "experiments/runs").resolve()):
            parser.error("Worker directory must be inside this project's run storage")
        return worker(run_dir)
    if args.test_receipt is None:
        parser.error("--execute requires --test-receipt")
    if Path.cwd().resolve() != ROOT or Path(sys.prefix).resolve() != (ROOT / ".venv").resolve() or sys.prefix == sys.base_prefix:
        parser.error("Run from manufacturing with its isolated .venv/bin/python")

    from mfg_twin.contract import load_study
    from mfg_twin.pilot import PILOT_PATH, PILOT_SHA256, load_pilot_plan, validate_run_artifacts, last_progress
    started_clock = time.perf_counter()
    started = utc()
    study = load_study(ROOT)  # metadata only
    plan = load_pilot_plan(ROOT)
    validate_test_receipt(args.test_receipt.resolve())
    limits = Limits()
    required_limits = plan["resource_limits"]
    if (limits.wall_seconds != required_limits["wall_timeout_seconds"]
            or limits.cpu_seconds != required_limits["worker_cpu_limit_seconds"]
            or limits.rss_bytes != required_limits["monitored_RSS_abort_bytes"]
            or limits.output_bytes != required_limits["output_limit_bytes"]
            or limits.poll_seconds > required_limits["RSS_poll_interval_seconds_maximum"]):
        raise ValueError("Runner resource limits differ from the immutable pilot plan")
    if shutil.disk_usage(ROOT).free < 2 * limits.output_bytes:
        raise RuntimeError("Insufficient free disk for bounded outputs and safety margin")
    attempts = ROOT / "local/pilot_attempts"
    attempts.mkdir(parents=True, exist_ok=True)
    claim_path = attempts / "casper_right_arm_pilot_v0.1.json"
    if claim_path.exists():
        raise RuntimeError("This specification already has an attempt; automatic retries are forbidden")
    run_id = "velocity_zmax_pilot_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    run_dir = ROOT / "experiments/runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    writer = BudgetWriter(run_dir, limit_bytes=limits.output_bytes, reserve_bytes=0)
    files = admission_files()
    hashes = {str(p.relative_to(ROOT)): digest(p) for p in files}
    writer.write_json("source_snapshot.json", {str(path.relative_to(ROOT)): path.read_text() for path in files})
    writer.write_text("synthetic_test_receipt.json", args.test_receipt.read_text())
    writer.write_text("pilot_specification.json", (ROOT / PILOT_PATH).read_text())
    writer.write_json("specification_snapshot.json", {name: (ROOT / "docs" / name).read_text() for name in (
        "ANNOTATION_FEATURE_SPLIT_CONTRACT.md", "EVALUATION_PROTOCOL.md", "METRIC_DEFINITIONS.md", "FINAL_TEST_PROTECTION.md")})
    git_head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    git_status = subprocess.check_output(["git", "status", "--short", "--", "."], cwd=ROOT, text=True)
    patch = subprocess.check_output(["git", "diff", "HEAD", "--", "."], cwd=ROOT, text=True)
    writer.write_text("tracked_workspace.patch", patch)
    hardware = subprocess.check_output(["/usr/sbin/sysctl", "-n", "hw.model", "hw.memsize", "machdep.cpu.brand_string"], text=True).splitlines()
    worker_command = [sys.executable, str(Path(__file__).resolve()), "--worker", str(run_dir)]
    thread_environment = {name: "1" for name in (
        "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS")}
    environment = dict(os.environ)
    environment.update(thread_environment)
    environment.update(PYTHONDONTWRITEBYTECODE="1", PYTHONNOUSERSITE="1")
    resolved = {
        "run_id": run_id, "kind": "bounded_normal_only_feasibility_not_benchmark",
        "project": "manufacturing", "owner": "Haiqa Mushtaq", "operator": "Codex assistant",
        "authorization": "Latest user explicitly requested implementing/testing the control and runner, then executing the bounded normal-only pilot: 'do these 2 both'.",
        "pilot_specification_sha256": PILOT_SHA256,
        "historical_plan_status_preserved": True, "attempt": 1, "automatic_retry": False,
        "seed": None, "stochastic": False, "started_at_utc": started,
        "command": shlex.join([sys.executable, *sys.argv]), "worker_command": worker_command,
        "cwd": str(ROOT), "run_directory": str(run_dir),
        "python": sys.version, "executable": sys.executable, "prefix": sys.prefix,
        "platform": platform.platform(), "machine": platform.machine(), "hardware_sysctl": hardware,
        "dependency_policy": "Python standard library only",
        "installed_distributions": sorted((d.metadata.get("Name", "unknown"), d.version) for d in distributions()),
        "thread_environment": thread_environment, "device": "cpu", "network_allowed": False,
        "resource_limits": {"wall_seconds": limits.wall_seconds, "cpu_seconds": limits.cpu_seconds,
                            "rss_bytes": limits.rss_bytes, "output_bytes": limits.output_bytes,
                            "poll_seconds": limits.poll_seconds},
        "git_head": git_head, "git_status": git_status, "source_sha256": hashes,
        "patch_sha256": digest(run_dir / "tracked_workspace.patch"),
        "test_receipt_sha256": digest(args.test_receipt),
        "dataset": {"path": study.source_relative_path, "bytes": study.source_bytes, "sha256": study.source_sha256},
        "access": plan["access"], "model": plan["model"],
        "implementation_designation": "independent_ordinary_control_pilot_only",
        "upstream_code_revision": None, "promotion_to_final_checkpoint": False,
    }
    writer.write_json("resolved_config.json", resolved)
    # The exclusive persistent claim consumes this plan's one attempt. It is
    # deliberately not removed on success, crash, interruption or spawn failure.
    claim = {"run_directory": str(run_dir), "claimed_at_utc": utc(), "attempt": 1,
             "resolved_config_sha256": digest(run_dir / "resolved_config.json")}
    with claim_path.open("x") as handle:
        json.dump(claim, handle, indent=2)
        handle.write("\n")
    print(json.dumps({"run_directory": str(run_dir), "status": "launching", "worker_command": worker_command}), flush=True)
    try:
        result = supervise(worker_command, cwd=ROOT, output_dir=run_dir, limits=limits, env=environment)
    except Exception as error:
        result = {"status": "failed", "reason": f"supervisor_start_failure:{type(error).__name__}:{error}",
                  "attempts": 1, "worker_usage": None}
    changed = [name for name, expected in hashes.items() if digest(ROOT / name) != expected]
    diagnostics_path = run_dir / "diagnostics.json"
    diagnostics = json.loads(diagnostics_path.read_text()) if diagnostics_path.exists() else None
    if diagnostics:
        result["worker_usage"] = diagnostics.get("worker_resources")
    accepted = (result.get("status") == "completed" and diagnostics is not None
                and diagnostics.get("status") == "completed" and not changed)
    artifact_validation = None
    if accepted:
        try:
            artifact_validation = validate_run_artifacts(run_dir, plan)
        except Exception as error:
            accepted = False
            artifact_validation = {"status": "failed", "reason": f"{type(error).__name__}: {error}"}
    artifacts = {str(p.relative_to(run_dir)): {"sha256": digest(p), "bytes": p.stat().st_size}
                 for p in sorted(run_dir.rglob("*")) if p.is_file()}
    manifest = {
        "run_id": run_id, "kind": "bounded_normal_only_feasibility_not_benchmark",
        "status": "completed" if accepted else "failed", "accepted": accepted,
        "started_at_utc": started, "completed_at_utc": utc(),
        "entry_end_to_end_seconds_before_receipt": time.perf_counter() - started_clock,
        "supervisor": result, "diagnostics": diagnostics, "source_changes_during_run": changed,
        "last_known_progress": last_progress(run_dir),
        "failure_stage": None if accepted else (diagnostics or last_progress(run_dir) or {}).get("stage", "worker_start_or_admission"),
        "artifact_readback_validation": artifact_validation,
        "artifacts_excluding_this_manifest": artifacts, "total_output_bytes": 0,
        "source_identity": resolved["dataset"], "calibration_access": False,
        "final_feature_access": False, "benchmark_or_twin_claim": False,
        "comparator_admission": "unchanged_pending_for_all_three_learning_papers",
    }
    # Fixed-point byte count includes this manifest, without pretending to embed
    # a self hash. Its SHA-256 is printed and retained in the external summary.
    base_bytes = sum(p.stat().st_size for p in run_dir.rglob("*") if p.is_file())
    for _ in range(8):
        text = json.dumps(manifest, indent=2, allow_nan=False) + "\n"
        total = base_bytes + len(text.encode())
        if manifest["total_output_bytes"] == total:
            break
        manifest["total_output_bytes"] = total
    writer.write_text("run.json", text)
    print(json.dumps({"status": manifest["status"], "accepted": accepted,
                      "run_manifest": str(run_dir / "run.json"), "sha256": digest(run_dir / "run.json"),
                      "output_bytes": manifest["total_output_bytes"]}), flush=True)
    return 0 if accepted else 1


if __name__ == "__main__":
    raise SystemExit(main())
