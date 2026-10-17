"""Use the preserved supervisor for separately identified v0.2 attempts."""
import argparse
import json
import os
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
sys.path.insert(0, str(PROJECT / "src"))
from mfg_twin.supervisor import BudgetWriter, Limits, supervise

LIMITS = Limits(wall_seconds=300, cpu_seconds=180, rss_bytes=1073741824,
                output_bytes=52428800)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("worker", choices=["run_diagnostics.py", "run_normal_pilot.py", "run_mechanism_test.py"])
    parser.add_argument("--attempt", required=True)
    args = parser.parse_args()
    if not args.attempt.replace("_", "").isalnum():
        raise ValueError("Invalid attempt name")
    output = PROJECT / "local/contribution_v0.2/runs" / args.attempt
    output.mkdir(parents=True, exist_ok=False)
    command = [sys.executable, str(HERE/args.worker), "--output", str(output)]
    outcome = supervise(command, cwd=PROJECT, output_dir=output, limits=LIMITS,
                        env={"TF_NUM_INTRAOP_THREADS":"1", "TF_NUM_INTEROP_THREADS":"1",
                             "TF_CPP_MIN_LOG_LEVEL":"2", "CUDA_VISIBLE_DEVICES":"-1"})
    BudgetWriter(output, limit_bytes=LIMITS.output_bytes).write_bytes(
        "supervisor.json", (json.dumps(outcome, indent=2)+"\n").encode())
    print(json.dumps(outcome, indent=2))
    sys.exit(0 if outcome.get("status") == "completed" else 1)
