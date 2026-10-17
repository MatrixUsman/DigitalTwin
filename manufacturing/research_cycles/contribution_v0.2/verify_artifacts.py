"""Read back saved v0.2 evidence; do not train or parse raw observations."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
LOCAL = PROJECT / "local/contribution_v0.2"


def digest(path):
    result = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1024 * 1024):
            result.update(block)
    return result.hexdigest()


def read(path):
    return json.loads(path.read_text())


def main():
    checks = []

    def check(name, condition):
        checks.append({"name": name, "passed": bool(condition)})

    guards = read(PROJECT / "local/manuscript_v0.1/starting_guardrails.json")
    for name, expected in guards["frozen_source"].items():
        check("old_source:" + name, digest(PROJECT / name) == expected)
    for item in guards["frozen_inputs"]:
        path = PROJECT / item["path"]
        if "datasets/raw" in str(path):
            raise ValueError("Old raw data is outside this verification scope")
        check("old_input:" + item["path"], digest(path) == item["sha256"])
    for filename, key in [
        ("MODEL_SELECTION_FREEZE_V0.1.json", "selection_sha256"),
        ("FINAL_TEST_FREEZE_RECORD.json", "final_freeze_sha256"),
        ("FINAL_CAMPAIGN_V0.1_RECORD.json", "final_record_sha256"),
    ]:
        check(filename, digest(PROJECT / "experiments" / filename) == guards[key])
    check("old_pdf_unchanged", digest(PROJECT / "output/pdf/correction-evidence-casper-study.pdf") ==
          "c849f75b14b913646b1f756e5f73cf211163dc590216db693cd0d7cb72a4bd6f")

    diagnostic = read(LOCAL / "runs/diagnostics_003/diagnostics.json")
    pilot = read(LOCAL / "runs/normal_pilot_001/pilot_summary.json")
    for record in [diagnostic["provenance"], pilot]:
        for name, expected in record["source_sha256"].items():
            check("run_source:" + name, digest(PROJECT / name) == expected)
    for item in read(LOCAL / "sources/retrievals.json"):
        check("source_download:" + item["name"], digest(LOCAL / "sources" / item["name"]) == item["sha256"])
    nominal = read(LOCAL / "nominal_receipt.json")
    raw = PROJECT / nominal["file"]
    check("nominal_file_sha256", digest(raw) == nominal["sha256"])
    check("nominal_file_size", raw.stat().st_size == nominal["bytes"])
    check("nominal_read_only", raw.stat().st_mode & 0o222 == 0)
    check("nominal_archive_sha256", digest(raw.with_suffix(".download")) == nominal["payload_sha256"])

    run = LOCAL / "runs/normal_pilot_001"
    check("pilot_model_sha256", digest(run / "pilot_cnn.keras") == pilot["model_file_sha256"])
    with np.load(run / "pilot_artifacts.npz", allow_pickle=False) as arrays:
        check("pilot_indices", np.array_equal(arrays["indices"], np.arange(8501, 10549)))
        check("pilot_scores_finite", arrays["scores"].shape == (2048,) and np.isfinite(arrays["scores"]).all())
        check("pilot_scores_nonnegative", np.all(arrays["scores"] >= 0))
        check("pilot_score_mse_agrees", np.isclose(np.mean(arrays["scores"] ** 2), pilot["dev_standardized_mse"], rtol=2e-7))
        check("pilot_scaler_valid", arrays["mean"].shape == (9,) and arrays["scale"].shape == (9,)
              and np.isfinite(arrays["mean"]).all() and np.isfinite(arrays["scale"]).all()
              and np.all(arrays["scale"] > 0))
    check("pilot_no_threshold_or_attack_metric", pilot["threshold"] is None and pilot["attack_metrics"] is None)
    check("pilot_no_final_access", pilot["final_test_opened"] is False)
    check("pilot_internal_fit_immutability", pilot["weights_unchanged_during_development"] and pilot["scaler_unchanged_during_development"])
    # This checks the saved worker assertions; no development data or model is rerun.
    for name, worker in [("diagnostics_003", diagnostic["provenance"]), ("normal_pilot_001", pilot)]:
        supervisor = read(LOCAL / "runs" / name / "supervisor.json")
        limits = supervisor["limits"]
        check(name + ":completed", supervisor["status"] == "completed")
        check(name + ":wall_cap", supervisor["wall_seconds"] < limits["wall_seconds"])
        check(name + ":cpu_cap", worker["usage"]["process_cpu_seconds"] < limits["cpu_seconds"])
        check(name + ":sampled_memory_cap", supervisor["sampled_peak_rss_bytes"] < limits["rss_bytes"])
        actual_bytes = sum(p.stat().st_size for p in (LOCAL / "runs" / name).iterdir() if p.is_file())
        check(name + ":actual_output_cap", actual_bytes < limits["output_bytes"])
    tests_log = (LOCAL / "synthetic_tests_v2.log").read_text()
    check("recorded_18_synthetic_tests_passed", "Ran 18 tests" in tests_log and tests_log.rstrip().endswith("OK"))
    check("all_failed_attempts_preserved", (LOCAL / "runs/diagnostics_001/failure_record.json").is_file()
          and read(LOCAL / "runs/diagnostics_002/supervisor.json")["status"] == "failed")

    paths = set(p for p in HERE.iterdir() if p.is_file() and p.name != "EVIDENCE_MANIFEST.json")
    paths.update(p for p in LOCAL.rglob("*") if p.is_file() and p.suffix != ".pyc")
    paths.add(PROJECT / "docs/BASELINE_LIMITATION_DOSSIER_V0.2.md")
    paths.add(PROJECT / "docs/CONTRIBUTION_DESIGN_V0.2.md")
    paths.add(PROJECT / "docs/literature/RECOVERY_PRIOR_ART_ADDENDUM_2026-10-17.md")
    paths.add(PROJECT / "datasets/manifests/casper12_v2_nominal_receipt.json")
    manifest = {
        "schema": "manufacturing-contribution-evidence-v0.2",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "record_type": "post-run artifact readback, not preregistration or independent reviewer",
        "command": [sys.executable, str(Path(__file__).resolve())],
        "checks": checks,
        "passed": sum(c["passed"] for c in checks),
        "total": len(checks),
        "checks_all_passed": all(c["passed"] for c in checks),
        "artifact_sha256": {str(p.relative_to(PROJECT)): digest(p) for p in sorted(paths)},
        "data_receipt": nominal,
        "synthetic_diagnostics": {k: v for k, v in diagnostic.items() if k != "provenance"},
        "normal_pilot": {k: v for k, v in pilot.items() if k not in ["git_status", "source_sha256"]},
        "pipeline_state": {
            "baseline_source_audit": "bounded completed; table/run lineage remains unresolved",
            "limitation_reproduction": "specific source defects and model-state behavior reproduced; method-level cyber weakness not demonstrated",
            "improvement": "candidate equations/design only; not implemented or admitted as novel",
            "fair_test": "synthetic software checks and one normal feasibility pilot completed; full comparison not run",
            "writing": "research notes only; contribution results and final title/venue not established",
            "physical_testbed_access": False,
            "permitted_future_evidence": ["public datasets after admission", "clearly labelled simulation"],
        },
        "boundaries": [
            "No raw observations parsed during this readback; only new nominal bytes hashed",
            "Saved fit-immutability fields are checked, not independently replayed",
            "RSS is monitored, not an instantaneous ceiling",
            "No claim of paper reproduction, novelty, physical generalization or journal readiness",
        ],
    }
    (HERE / "EVIDENCE_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"passed": manifest["passed"], "total": manifest["total"],
                      "failed": [c["name"] for c in checks if not c["passed"]],
                      "artifacts_hashed": len(paths)}, indent=2))
    return 0 if manifest["checks_all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
