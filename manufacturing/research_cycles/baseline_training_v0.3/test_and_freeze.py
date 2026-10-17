"""Record synthetic checks and bind passing source/configuration before data access."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import time
from io_utils import sha256

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("--attempt", required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_]+", args.attempt): raise ValueError("Invalid attempt")
    freeze_path = HERE / "FREEZE.json"
    if freeze_path.exists(): raise ValueError("Existing freeze must be preserved")
    output = PROJECT / "local/baseline_training_v0.3/tests" / args.attempt
    output.mkdir(parents=True, exist_ok=False)
    paths = sorted(p for p in HERE.iterdir() if p.suffix in [".py", ".json"] or p.name == "PLAN.md")
    paths += [PROJECT / "src/mfg_twin/supervisor.py", PROJECT / "research_cycles/contribution_v0.2/requirements-macos-arm64.lock.txt"]
    source = {str(p.relative_to(PROJECT)): sha256(p) for p in paths}
    command = [sys.executable, "-m", "unittest", "discover", "-s", str(HERE), "-p", "test_*.py", "-v"]
    env = dict(os.environ, TF_NUM_INTRAOP_THREADS="1", TF_NUM_INTEROP_THREADS="1", TF_CPP_MIN_LOG_LEVEL="2", CUDA_VISIBLE_DEVICES="-1", OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1")
    start = datetime.now(timezone.utc).isoformat(); clock = time.monotonic()
    with (output / "tests.log").open("w") as log:
        try:
            process = subprocess.run(command, cwd=PROJECT, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=120)
            code = process.returncode
        except subprocess.TimeoutExpired:
            code = 124
    content = (output / "tests.log").read_text()
    count = re.search(r"Ran (\d+) tests", content)
    unchanged = all(sha256(PROJECT / name) == expected for name, expected in source.items())
    receipt = {"synthetic": True, "benchmark_data_opened": False, "command": command, "cwd": str(PROJECT),
               "start_utc": start, "end_utc": datetime.now(timezone.utc).isoformat(),
               "wall_seconds": time.monotonic() - clock, "returncode": code,
               "tests_run": int(count.group(1)) if count else None,
               "source_unchanged": unchanged, "source_sha256": source,
               "interpreter": sys.version, "platform": platform.platform(), "log_sha256": sha256(output / "tests.log")}
    receipt_path = output / "receipt.json"; receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
    print(content[-4500:])
    if code != 0 or not unchanged: raise SystemExit(1)
    environment = subprocess.check_output([sys.executable, "-m", "pip", "freeze"], text=True)
    lock = PROJECT / "research_cycles/contribution_v0.2/requirements-macos-arm64.lock.txt"
    if environment.strip() != lock.read_text().strip(): raise ValueError("Training environment differs from validated lock")
    freeze = {"study_id": "manufacturing-baseline-training-v0.3", "frozen_utc": datetime.now(timezone.utc).isoformat(),
              "source_sha256": source, "test_receipt": str(receipt_path.relative_to(PROJECT)),
              "test_receipt_sha256": sha256(receipt_path), "raw_observations_read": False,
              "configuration": json.loads((HERE / "config.json").read_text()),
              "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
              "git_status": subprocess.check_output(["git", "status", "--porcelain"], text=True),
              "interpretation": "Pre-execution local specification; no external preregistration"}
    freeze_path.write_text(json.dumps(freeze, indent=2) + "\n")
    print(f"Froze {len(source)} source/configuration identities after {receipt['tests_run']} passing synthetic tests.")
