"""Single-attempt supervisor for the frozen normal-only study."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from io_utils import sha256, verify_frozen

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
sys.path.insert(0, str(PROJECT / "src"))
from mfg_twin.supervisor import BudgetWriter, Limits, supervise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("--attempt", required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_]+", args.attempt): raise ValueError("Invalid attempt")
    freeze = json.loads((HERE / "FREEZE.json").read_text()); verify_frozen(PROJECT, freeze)
    limits = Limits(**freeze["configuration"]["limits"])
    output = PROJECT / "local/baseline_training_v0.3/runs" / args.attempt
    output.mkdir(parents=True, exist_ok=False)
    writer = BudgetWriter(output, limit_bytes=limits.output_bytes)
    command = [sys.executable, str(HERE / "worker.py"), "--output", str(output)]
    writer.write_json("launch.json", {"utc": datetime.now(timezone.utc).isoformat(), "command": command,
                                     "cwd": str(PROJECT), "freeze_sha256": sha256(HERE / "FREEZE.json"),
                                     "attempt": args.attempt, "owner": "Haiqa Mushtaq", "operator": "Codex"})
    outcome = supervise(command, cwd=PROJECT, output_dir=output, limits=limits,
                        env={"TF_NUM_INTRAOP_THREADS": "1", "TF_NUM_INTEROP_THREADS": "1",
                             "TF_CPP_MIN_LOG_LEVEL": "2", "CUDA_VISIBLE_DEVICES": "-1",
                             "OPENBLAS_NUM_THREADS": "1", "OMP_NUM_THREADS": "1"})
    writer.write_json("supervisor.json", outcome)
    print(json.dumps(outcome, indent=2))
    raise SystemExit(0 if outcome.get("status") == "completed" else 1)
