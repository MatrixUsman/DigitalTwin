"""Run offline synthetic correctness tests and preserve a local receipt.

No training, calibration of CASPER, benchmark scoring or raw dataset access.
Run from manufacturing: .venv/bin/python scripts/run_synthetic_tests.py
"""
from __future__ import annotations

import hashlib
import io
import json
import platform
import shlex
import shutil
import subprocess
import sys
import time
import unittest
from datetime import datetime, timezone
from importlib.metadata import distributions
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    started = datetime.now(timezone.utc)
    output = ROOT / "local/software_validation" / started.strftime("%Y%m%dT%H%M%S_%fZ")
    output.mkdir(parents=True, exist_ok=False)
    files = [*ROOT.joinpath("src").rglob("*.py"), *ROOT.joinpath("tests").rglob("*.py"),
             *ROOT.joinpath("tests/fixtures").rglob("*.json"),
             *ROOT.joinpath("scripts").glob("*.py"), ROOT/"pyproject.toml",
             *ROOT.joinpath("configs").glob("casper_right_arm_*.json")]
    files = sorted(set(files))
    fingerprints = {}
    for source in files:
        relative = source.relative_to(ROOT)
        fingerprints[str(relative)] = digest(source)
        target = output / "source_snapshot" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    dirty = subprocess.check_output(["git", "status", "--short", "--", "."], cwd=ROOT, text=True)
    patch = subprocess.check_output(["git", "diff", "HEAD", "--", "."], cwd=ROOT)
    (output/"tracked_workspace.patch").write_bytes(patch)
    blocked_accesses = []

    def protect_test_scope(event, args):
        if event == "open" and isinstance(args[0], (str, bytes)):
            path = Path(args[0].decode() if isinstance(args[0], bytes) else args[0]).resolve()
            # Reject every project's raw-data directory, even through symlinks.
            if any(a == "datasets" and b == "raw" for a, b in zip(path.parts, path.parts[1:])):
                blocked_accesses.append({"event": event, "path": str(path)})
                raise PermissionError("Synthetic test runner forbids raw dataset access")
        if event in {"socket.connect", "socket.getaddrinfo", "socket.bind"}:
            blocked_accesses.append({"event": event})
            raise PermissionError("Synthetic test runner is offline")

    # Process-local guard, installed before test discovery/imports. This is not
    # an OS sandbox and does not claim to constrain arbitrary native extensions.
    sys.addaudithook(protect_test_scope)
    stream = io.StringIO()
    suite = unittest.defaultTestLoader.discover(str(ROOT/"tests"), pattern="test_*.py")
    start_clock = time.monotonic()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    elapsed = time.monotonic() - start_clock
    log = stream.getvalue()
    (output/"test_output.txt").write_text(log)
    changed = [path for path, value in fingerprints.items() if digest(ROOT/path) != value]
    receipt = {
        "kind": "synthetic_software_validation_not_benchmark", "project": "manufacturing",
        "operator": "Codex assistant", "started_at_utc": started.isoformat(),
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "command": shlex.join([sys.executable, *sys.argv]), "cwd": str(Path.cwd()),
        "python": sys.version, "executable": sys.executable,
        "platform": platform.platform(), "machine": platform.machine(),
        "isolated_environment": sys.prefix != sys.base_prefix,
        "installed_distributions": sorted((d.metadata.get("Name", "unknown"), d.version) for d in distributions()),
        "git_head": head, "git_status_at_start": dirty,
        "source_sha256_at_start": fingerprints,
        "tracked_patch_sha256": digest(output/"tracked_workspace.patch"),
        "source_changed_during_tests": changed,
        "random_seeds": "deterministic synthetic cases; no randomized fitting",
        "tests_run": result.testsRun, "failures": len(result.failures),
        "errors": len(result.errors), "skips": len(result.skipped),
        "expected_failures": len(result.expectedFailures),
        "unexpected_successes": len(result.unexpectedSuccesses),
        "duration_seconds": elapsed,
        "success": result.wasSuccessful() and not changed,
        "raw_dataset_opened": False, "trained_models": False,
        "test_scope_guard": "process-local Python audit hook; raw-path/network opens rejected",
        "blocked_access_attempts": blocked_accesses,
        "scope_limit": "Tests and metadata references only; not validation on CASPER observations, a comparator reproduction or final-release admission",
    }
    (output/"receipt.json").write_text(json.dumps(receipt, indent=2)+"\n")
    if not receipt["success"]:
        print(log)
    print(json.dumps({"tests":result.testsRun,"failures":len(result.failures),"errors":len(result.errors),
                      "skips":len(result.skipped),"success":receipt["success"],"receipt":str(output/"receipt.json")}))
    return 0 if receipt["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
