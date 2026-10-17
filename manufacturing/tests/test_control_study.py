"""Explicitly SYNTHETIC normal-only control study and entry admission tests."""
import csv
import hashlib
import importlib.util
import io
import json
import math
from pathlib import Path
from decimal import Decimal
import sys
import tempfile
import unittest
from unittest.mock import patch

from mfg_twin.contract import ContractError, Study
from mfg_twin.control_study import (CONTROL_PLAN_PATH, TrainingCache, candidate_specs, load_control_plan, run_control_study,
                                    select_candidates, validate_control_artifacts)
from mfg_twin.data import CASPER_HEADER, Observation, PartitionSpec
from mfg_twin.supervisor import BudgetWriter, Limits, SupervisorError

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("_synthetic_control_entry", ROOT / "scripts/run_control_study.py")
ENTRY = importlib.util.module_from_spec(_spec)
_original_path = list(sys.path)
try:
    _spec.loader.exec_module(ENTRY)
finally:
    sys.path[:] = _original_path


def synthetic_study(root, *, development_offset=0, label="0", constant=False):
    stream = io.StringIO(newline="")
    writer = csv.writer(stream)
    writer.writerow(CASPER_HEADER)
    for row in range(108):
        values = ["SYNTHETIC_UNUSED"] * 20
        values[0] = str(row * .05 + (1 if row >= 40 else 0))
        wave = 0 if constant else math.sin(row * math.pi / 2)
        offset = development_offset if row >= 80 else 0
        values[1] = json.dumps([wave * (j+1) + j + offset for j in range(6)])
        values[2] = json.dumps([wave * (j+2) - j + offset for j in range(6)])
        values[-1] = label
        if row >= 104:
            values[0] = "SYNTHETIC_PROTECTED_INVALID_TIMESTAMP"
            values[1] = values[2] = "SYNTHETIC_PROTECTED_INVALID_FEATURES"
        writer.writerow(values)
    payload = stream.getvalue().encode()
    path = Path(root) / "synthetic.csv"
    path.write_bytes(payload)
    study = Study(Path(root), path.name, len(payload), hashlib.sha256(payload).hexdigest(),
                  (PartitionSpec("training", 0, 80, warmup=4), PartitionSpec("development", 80, 104, warmup=4)),
                  (("training", ((4, 40), (44, 80))), ("development", ((84, 104),))))
    plan = {"access": {
        "fit": {"parent_partition": "training", "rows_half_open": [0, 80], "raw_rows": 80,
                "eligible_intervals_half_open": [[4, 40], [44, 80]], "expected_eligible_rows": 72},
        "check_scores": {"parent_partition": "development", "rows_half_open": [80, 104], "raw_rows": 24,
                         "eligible_intervals_half_open": [[84, 104]], "expected_eligible_rows": 20}},
        "models": {"velocity": {"id": "velocity_zmax"},
                   "ar": {"orders": [1, 2], "ridges": [.001, .1]},
                   "template": {"bins": [2, 4], "initialization": 4,
                                "period_estimation": {"stride": 1, "min_lag": 2, "max_lag": 4, "max_observations": 32}}}}
    return study, plan


class ControlStudyTests(unittest.TestCase):
    def execute(self, directory, **kwargs):
        study, plan = synthetic_study(directory, **kwargs)
        output = Path(directory) / "synthetic_outputs"
        diagnostics = {}
        run_control_study(study, plan, BudgetWriter(output, limit_bytes=1000000), diagnostics)
        return study, plan, output, diagnostics

    def test_complete_synthetic_support_models_scores_and_readback(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-controls-") as tmp:
            study, plan, output, diagnostics = self.execute(tmp)
            self.assertEqual(diagnostics["status"], "completed")
            self.assertEqual(diagnostics["populations"]["fit"]["segment_start_rows"], [0, 40])
            self.assertEqual(diagnostics["populations"]["check_scores"]["segment_start_rows"], [80])
            for item in diagnostics["candidates"]:
                self.assertEqual(item["fit_count"], 72)
                self.assertEqual(item["score_count"], 20)
                self.assertTrue(item["reference_unchanged"])
            readback = validate_control_artifacts(output, plan)
            self.assertEqual(readback["complete_candidates"], 7)
            self.assertEqual(readback["saved_index_rows"], 20)
            self.assertEqual(diagnostics["load_stats"]["fit"]["csv_records_traversed"], 80)
            self.assertEqual(diagnostics["load_stats"]["check_scores"]["csv_records_traversed"], 104)
            self.assertEqual(sum(x["hash_bytes"] for x in diagnostics["load_stats"].values()), 2*study.source_bytes)
            self.assertFalse(diagnostics["calibration_or_final_observations_parsed"])

    def test_development_changes_cannot_change_any_fitted_model_or_scaler(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-A-") as a, tempfile.TemporaryDirectory(prefix="synthetic-B-") as b:
            _, _, first, _ = self.execute(a)
            _, _, second, _ = self.execute(b, development_offset=100)
            for file in [*first.glob("*.model.json"), first / "training_standardizer.json"]:
                self.assertEqual(file.read_bytes(), (second / file.name).read_bytes())
            self.assertNotEqual((first/"velocity_zmax.scores.f64").read_bytes(), (second/"velocity_zmax.scores.f64").read_bytes())

    def test_labels_do_not_change_models_or_scores(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-A-") as a, tempfile.TemporaryDirectory(prefix="synthetic-B-") as b:
            _, _, first, _ = self.execute(a)
            _, _, second, _ = self.execute(b, label="1")
            for file in [*first.glob("*.model.json"), *first.glob("*.scores.f64")]:
                self.assertEqual(file.read_bytes(), (second / file.name).read_bytes())

    def test_selection_is_within_family_and_exact_ties_follow_declared_order(self):
        def item(identifier, family, value):
            return {"id": identifier, "family": family, "status": "completed", "development_mean_score": value,
                    "model_artifact": identifier+".json", "model_state_sha256_before": "a"*64,
                    "score_artifact": identifier+".f64"}
        ledger = [item("z", "ar", 2), item("a", "ar", 2), item("t", "template", 100), item("v", "velocity", 1)]
        self.assertEqual(select_candidates(ledger)["ar"]["candidate_id"], "z")
        self.assertEqual(set(select_candidates(ledger)), {"ar", "template", "velocity"})

    def test_failed_template_is_preserved_and_no_partial_suite_admitted(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-failure-") as tmp:
            study, plan = synthetic_study(tmp)
            plan["models"]["template"]["period_estimation"]["max_observations"] = 5
            output = Path(tmp)/"outputs"
            diagnostics = {}
            run_control_study(study, plan, BudgetWriter(output, limit_bytes=1000000), diagnostics)
            self.assertEqual(diagnostics["status"], "failed")
            self.assertEqual(len(diagnostics["candidates"]), 7)
            templates = [item for item in diagnostics["candidates"] if item["family"] == "template"]
            self.assertTrue(all(item["status"] == "failed" for item in templates))
            self.assertTrue(all(item["failure"]["stage"] == "period_estimation" for item in templates))
            self.assertFalse(json.loads((output/"selected_artifacts.json").read_text())["ready_for_later_calibration"])
            with self.assertRaises(ContractError):
                validate_control_artifacts(output, plan)

    def test_refuses_subset_plan_and_protected_partition_before_read(self):
        for change in ("subset", "protected"):
            with self.subTest(change=change), tempfile.TemporaryDirectory(prefix="synthetic-scope-") as tmp:
                study, plan = synthetic_study(tmp)
                if change == "subset":
                    plan["access"]["fit"]["rows_half_open"][1] = 79
                else:
                    plan["access"]["fit"]["parent_partition"] = "normal_calibration"
                with self.assertRaises(ContractError):
                    run_control_study(study, plan, BudgetWriter(Path(tmp)/"outputs", limit_bytes=1000000), {})

    def test_readback_rejects_index_score_model_and_selection_corruption(self):
        for corruption in ("index", "score", "model", "selection"):
            with self.subTest(corruption=corruption), tempfile.TemporaryDirectory(prefix="synthetic-corruption-") as tmp:
                _, plan, output, _ = self.execute(tmp)
                if corruption == "index":
                    path = output/"development_index.jsonl"
                    lines = path.read_text().splitlines(); lines[1] = lines[0]
                    path.write_text("\n".join(lines)+"\n")
                elif corruption == "score":
                    path = output/"velocity_zmax.scores.f64"
                    path.write_bytes(path.read_bytes()[:-8])
                elif corruption == "model":
                    path = output/"velocity_zmax.model.json"
                    value = json.loads(path.read_text()); value["reference"]["mean"][0] += 1
                    path.write_text(json.dumps(value))
                else:
                    path = output/"selected_artifacts.json"
                    value = json.loads(path.read_text()); value["selection"].pop("ar")
                    path.write_text(json.dumps(value))
                with self.assertRaises(ContractError):
                    validate_control_artifacts(output, plan)

    def test_candidate_grid_duplicate_rejected(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-grid-") as tmp:
            _, plan = synthetic_study(tmp)
            plan["models"]["ar"]["orders"] = [1, 1]
            with self.assertRaises(ContractError):
                candidate_specs(plan)

    def test_period_prefix_caps_raw_valid_count_before_filtering_and_stops_at_gap(self):
        cache = TrainingCache()
        for index in range(12):
            cache.append(Observation((float(index),)*6, (float(index),)*6,
                                     None if index in (0, 8) else Decimal(".05")), index >= 4)
        self.assertEqual([o.q[0] for o in cache.first_segment_eligible(6)], [4., 5.])
        self.assertEqual([o.q[0] for o in cache.first_segment_eligible(12)], [4., 5., 6., 7.])

    def test_readback_rejects_changed_candidate_configuration_and_refit_flag(self):
        for corruption in ("parameters", "refit"):
            with self.subTest(corruption=corruption), tempfile.TemporaryDirectory(prefix="synthetic-identity-") as tmp:
                _, plan, output, _ = self.execute(tmp)
                if corruption == "parameters":
                    path = output/"candidate_results.json"
                    value = json.loads(path.read_text())
                    next(item for item in value["candidates"] if item["family"] == "ar")["parameters"]["order"] = 99
                else:
                    path = output/"selected_artifacts.json"
                    value = json.loads(path.read_text()); value["refit_on_development"] = True
                path.write_text(json.dumps(value))
                with self.assertRaises(ContractError):
                    validate_control_artifacts(output, plan)

    def test_constant_training_fails_before_development_source_is_read(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-constant-") as tmp:
            study, plan = synthetic_study(tmp, constant=True)
            diagnostics = {}
            with self.assertRaises(ValueError):
                run_control_study(study, plan, BudgetWriter(Path(tmp)/"outputs", limit_bytes=1000000), diagnostics)
            self.assertEqual(diagnostics["status"], "failed")
            self.assertEqual(diagnostics["load_stats"]["check_scores"]["hash_bytes"], 0)

    def test_document_change_rejects_plan_before_raw_access(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-docbinding-") as tmp:
            root = Path(tmp)
            (root/"configs").mkdir()
            document = root/"synthetic_plan.md"; document.write_text("SYNTHETIC original")
            config = {"study_id": "manufacturing-casper-right-arm-controls-v0.1",
                      "access": {"calibration_access": False, "protected_final_access": False,
                                 "labels_available_to_model": False},
                      "documentation": document.name,
                      "documentation_sha256": hashlib.sha256(document.read_bytes()).hexdigest()}
            (root/CONTROL_PLAN_PATH).write_text(json.dumps(config))
            document.write_text("SYNTHETIC changed")
            with self.assertRaisesRegex(ContractError, "documentation changed"):
                load_control_plan(root)


class ControlEntryTests(unittest.TestCase):
    def test_terminal_resource_overrun_or_missing_receipt_rejected(self):
        limits = Limits()
        valid = {"process_cpu_seconds": 10., "peak_rss_bytes": 100000}
        self.assertTrue(ENTRY.resource_receipt_admitted(valid, limits))
        self.assertFalse(ENTRY.resource_receipt_admitted({}, limits))
        self.assertFalse(ENTRY.resource_receipt_admitted(dict(valid, process_cpu_seconds=301.), limits))
        self.assertFalse(ENTRY.resource_receipt_admitted(dict(valid, peak_rss_bytes=limits.rss_bytes+1), limits))
        self.assertFalse(ENTRY.resource_receipt_admitted(dict(valid, process_cpu_seconds=float("nan")), limits))

    def test_inventory_covers_every_current_python_script_and_control_config(self):
        inventory = {str(path.relative_to(ROOT)) for path in ENTRY.admission_files()}
        self.assertIn("scripts/run_control_study.py", inventory)
        self.assertIn("configs/casper_right_arm_controls_v0.1.json", inventory)
        self.assertIn("src/mfg_twin/control_study.py", inventory)
        self.assertIn("tests/test_control_study.py", inventory)

    def test_matching_synthetic_receipt_then_changed_config_or_interpreter_rejected(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-admission-") as tmp:
            root = Path(tmp)
            path = root/"configs/casper_right_arm_controls_v0.1.json"
            path.parent.mkdir(); path.write_text('{"synthetic":true}')
            receipt = {"kind": "synthetic_software_validation_not_benchmark", "success": True,
                       "failures": 0, "errors": 0, "skips": 0, "tests_run": 1,
                       "expected_failures": 0, "unexpected_successes": 0,
                       "raw_dataset_opened": False, "trained_models": False,
                       "source_changed_during_tests": [], "executable": sys.executable, "python": sys.version,
                       "source_sha256_at_start": {str(path.relative_to(root)): ENTRY.digest(path)}}
            receipt_path = root/"receipt.json"
            receipt_path.write_text(json.dumps(receipt))
            with patch.object(ENTRY, "ROOT", root), patch.object(ENTRY, "admission_files", return_value=[path]):
                ENTRY.validate_test_receipt(receipt_path)
                path.write_text('{"synthetic":"changed"}')
                with self.assertRaises(ValueError):
                    ENTRY.validate_test_receipt(receipt_path)
                receipt["executable"] = "/synthetic/incorrect/python"
                receipt_path.write_text(json.dumps(receipt))
                with self.assertRaises(ValueError):
                    ENTRY.validate_test_receipt(receipt_path)

    def test_new_worker_start_token_preserves_failed_or_completed_attempt(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-attempt-") as tmp:
            writer = BudgetWriter(Path(tmp), limit_bytes=10000)
            ENTRY.claim_worker_start(writer, "a"*64)
            original = (Path(tmp)/"worker_started.json").read_bytes()
            with self.assertRaises(SupervisorError):
                ENTRY.claim_worker_start(writer, "a"*64)
            self.assertEqual((Path(tmp)/"worker_started.json").read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
