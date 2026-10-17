"""Explicitly SYNTHETIC score-extension fixtures; no CASPER observations."""
from array import array
from copy import deepcopy
from dataclasses import replace
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from mfg_twin.contract import ContractError
from mfg_twin.observer_study import run_observer_study, sha
from mfg_twin.score_extension import (PLAN_PATH, SCORES, load_score_extension_plan, load_inputs,
    unchanged_inputs, run_score_extension, validate_score_extension_artifacts)
from mfg_twin.supervisor import BudgetWriter, Limits, SupervisorError
from test_observer_study import fixture as observer_fixture

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("_synthetic_score_extension_entry", ROOT / "scripts/run_score_extension.py")
ENTRY = importlib.util.module_from_spec(_spec)
_original = list(sys.path)
try:
    _spec.loader.exec_module(ENTRY)
finally:
    sys.path[:] = _original


def fixture(directory, label="0"):
    """Build prior fitted SYNTHETIC artifacts, then expose only development."""
    root = Path(directory)
    study, oldplan = observer_fixture(root, label=label)
    old = root / "previous_synthetic_observer"
    run_observer_study(study, oldplan, BudgetWriter(old, limit_bytes=2000000), {})
    artifacts = {p.name: {"sha256": sha(p), "bytes": p.stat().st_size} for p in old.iterdir() if p.is_file()}
    (old / "run.json").write_text(json.dumps({"accepted": True, "status": "completed", "artifacts_excluding_this_manifest": artifacts}))
    oldconfig = root / "synthetic_observer_config.json"
    oldconfig.write_text(json.dumps(oldplan))
    results = json.loads((old / "observer_results.json").read_text())
    model = old / "observer.model.json"
    registry = {"source_run": old.name, "run_manifest_sha256": sha(old / "run.json"),
                "configuration_sha256": sha(oldconfig), "model_path": str(model.relative_to(root)), "model_file_sha256": sha(model),
                "input_reference_registry": oldplan["selected_controls"]["path"],
                "input_reference_registry_sha256": oldplan["selected_controls"]["sha256"],
                "training_eligible_count": 72, "development_eligible_count": 20,
                "reference_refit": False, "development_refit": False, "thresholds": None,
                "final_test_admitted": False, "principal_pair_shared_state": True,
                "saved_scores": {k: dict(v, path=str((old / v["path"]).relative_to(root))) for k,v in results["scores"].items()}}
    regpath = root / "synthetic_observer_registry.json"; regpath.write_text(json.dumps(registry))
    plan = {"observer_registry": {"path": regpath.name, "sha256": sha(regpath)},
            "observer_configuration": {"path": oldconfig.name, "sha256": sha(oldconfig)},
            "scores": list(SCORES),
            "access": {"check_scores": deepcopy(oldplan["access"]["check_scores"]), "training_access": False,
                       "fitting_allowed": False, "calibration_access": False, "protected_final_access": False,
                       "labels_available_to_model": False}}
    return study, plan


class ScoreExtensionTests(unittest.TestCase):
    def execute(self, directory, **kwargs):
        study, plan = fixture(directory, **kwargs)
        output = Path(directory) / "synthetic_score_extension"
        diagnostics = {}
        run_score_extension(study, plan, BudgetWriter(output, limit_bytes=2000000), diagnostics)
        return study, plan, output, diagnostics

    def test_full_support_exact_old_score_coordinate_parity_and_no_fitting(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-score-extension-") as tmp:
            study, plan, output, diagnostics = self.execute(tmp)
            self.assertEqual(diagnostics["status"], "completed")
            self.assertEqual(diagnostics["score_counts"], dict.fromkeys(SCORES, 20))
            self.assertEqual(diagnostics["fit_calls"], 0)
            self.assertEqual(diagnostics["training_rows_parsed"], 0)
            self.assertEqual(diagnostics["load_stats"]["selected_rows_parsed"], 24)
            self.assertEqual(diagnostics["load_stats"]["csv_records_traversed"], 104)
            self.assertEqual(diagnostics["load_stats"]["hash_scans_completed"], 2)
            self.assertEqual(diagnostics["load_stats"]["hash_bytes"], 2 * study.source_bytes)
            self.assertEqual(validate_score_extension_artifacts(output, plan, Path(tmp))["saved_index_rows"], 20)
            old = Path(tmp) / "previous_synthetic_observer"
            self.assertEqual((output/"O-R.scores.f64").read_bytes(), (old/"synchronized_residual.scores.f64").read_bytes())
            self.assertEqual((output/"O-RC.scores.f64").read_bytes(), (old/"synchronized_evidence.scores.f64").read_bytes())
            self.assertEqual((output/"development_index.jsonl").read_bytes(), (old/"development_index.jsonl").read_bytes())

    def test_labels_do_not_change_any_score(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-label-A-") as a, tempfile.TemporaryDirectory(prefix="synthetic-label-B-") as b:
            _, _, first, _ = self.execute(a)
            _, _, second, _ = self.execute(b, label="1")
            for name in SCORES:
                self.assertEqual((first/(name+".scores.f64")).read_bytes(), (second/(name+".scores.f64")).read_bytes())

    def test_runner_does_not_call_any_fitting_path(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-no-fit-") as tmp:
            study, plan = fixture(tmp)
            with patch("mfg_twin.observer_study.run_observer_study", side_effect=AssertionError("fitting called")), patch("mfg_twin.control_study.run_control_study", side_effect=AssertionError("fitting called")):
                run_score_extension(study, plan, BudgetWriter(Path(tmp)/"out", limit_bytes=2000000), {})

    def test_changed_model_rejected_before_raw_access(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-model-corruption-") as tmp:
            study, plan = fixture(tmp)
            (Path(tmp)/"previous_synthetic_observer/observer.model.json").write_text("SYNTHETIC corruption")
            with patch("mfg_twin.score_extension.records", side_effect=AssertionError("raw opened")):
                with self.assertRaisesRegex(ContractError, "identity changed"):
                    run_score_extension(study, plan, BudgetWriter(Path(tmp)/"out", limit_bytes=2000000), {})

    def test_wrong_partition_or_subset_rejected_before_loading(self):
        for field in ("partition", "subset", "warmup"):
            with self.subTest(field=field), tempfile.TemporaryDirectory(prefix="synthetic-scope-") as tmp:
                study, plan = fixture(tmp)
                if field == "partition": plan["access"]["check_scores"]["parent_partition"] = "normal_calibration"
                elif field == "subset": plan["access"]["check_scores"]["rows_half_open"][1] -= 1
                else:
                    partitions = tuple(replace(p, warmup=p.warmup+1) if p.name == "development" else p for p in study.partitions)
                    study = replace(study, partitions=partitions)
                with self.assertRaises(ContractError):
                    run_score_extension(study, plan, BudgetWriter(Path(tmp)/"out", limit_bytes=2000000), {})

    def test_changed_prior_score_file_rejected_before_replay(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-parity-source-") as tmp:
            study, plan = fixture(tmp)
            (Path(tmp)/"previous_synthetic_observer/synchronized_residual.scores.f64").write_bytes(b"bad")
            with self.assertRaisesRegex(ContractError, "identity changed"):
                load_inputs(Path(tmp), plan)

    def test_missing_or_nonfinite_or_rehashed_inconsistent_saved_scores_fail(self):
        for change in ("short", "nan", "correction_formula", "velocity_bound", "coordinate", "snapshot", "scope"):
            with self.subTest(change=change), tempfile.TemporaryDirectory(prefix="synthetic-readback-") as tmp:
                _, plan, output, _ = self.execute(tmp)
                results_path = output / "score_extension_results.json"
                results = json.loads(results_path.read_text())
                if change in ("short", "nan", "correction_formula", "velocity_bound"):
                    name = "O-Rv" if change == "velocity_bound" else "O-C"
                    path = output / (name+".scores.f64")
                    values = array("d"); values.frombytes(path.read_bytes())
                    if change == "short": values.pop()
                    elif change == "nan": values[0] = math.nan
                    elif change == "correction_formula": values[0] = .5
                    else: values[0] = 1e9
                    path.write_bytes(values.tobytes())
                    if change in ("correction_formula", "velocity_bound"):
                        item = results["scores"][name]
                        item.update(sha256=sha(path), mean=math.fsum(values)/len(values), min=min(values), max=max(values))
                        results_path.write_text(json.dumps(results))
                elif change == "coordinate":
                    path=output/"development_index.jsonl"; lines=path.read_text().splitlines(); lines[1]=lines[0]; path.write_text("\n".join(lines)+"\n")
                elif change == "snapshot":
                    path=output/"immutable_model_snapshot.json"; value=json.loads(path.read_text());value["config"]["temperature"]*=2;path.write_text(json.dumps(value))
                else:
                    results["fit_calls"] = 1; results_path.write_text(json.dumps(results))
                with self.assertRaises(ContractError):
                    validate_score_extension_artifacts(output, plan, Path(tmp))

    def test_failed_parity_preserves_diagnostics_and_does_not_adjust_scores(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-failed-parity-") as tmp:
            study, plan = fixture(tmp)
            from mfg_twin.observer_scores import score_observer_proposal
            class WrongScores:
                def __init__(self, values): self.values=values
                def to_dict(self): return self.values
            def altered(*args):
                values=score_observer_proposal(*args).to_dict();values["O-R"]+=.01
                return WrongScores(values)
            diagnostics={}
            with patch("mfg_twin.observer_scores.score_observer_proposal", side_effect=altered):
                with self.assertRaisesRegex(ContractError,"historical score parity"):
                    run_score_extension(study, plan, BudgetWriter(Path(tmp)/"out", limit_bytes=2000000), diagnostics)
            self.assertEqual(diagnostics["status"], "failed")
            self.assertEqual(diagnostics["stage"], "exact_parity_and_artifact_write")
            self.assertTrue((Path(tmp)/"out/progress.jsonl").exists())

    def test_source_immutable_postcheck_detects_change(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-immutability-") as tmp:
            root=Path(tmp); path=root/"reference.json";path.write_text("synthetic")
            hashes={path.name:sha(path)}; self.assertTrue(unchanged_inputs(root,hashes))
            path.write_text("changed")
            with self.assertRaisesRegex(ContractError,"changed during"):
                unchanged_inputs(root,hashes)

    def test_plan_refuses_training_or_final_and_changed_document(self):
        for change in ("training", "final", "document"):
            with self.subTest(change=change), tempfile.TemporaryDirectory(prefix="synthetic-plan-") as tmp:
                root=Path(tmp);(root/"configs").mkdir();document=root/"synthetic-plan.md";document.write_text("SYNTHETIC")
                access={"check_scores":{"parent_partition":"development"},"training_access":False,"fitting_allowed":False,"calibration_access":False,"protected_final_access":False,"labels_available_to_model":False}
                plan={"study_id":"manufacturing-casper-right-arm-score-extension-v0.1","access":access,"scores":list(SCORES),"documentation":document.name,"documentation_sha256":sha(document)}
                if change == "training": access["training_access"]=True
                elif change == "final": access["protected_final_access"]=True
                else: document.write_text("SYNTHETIC changed")
                (root/PLAN_PATH).write_text(json.dumps(plan))
                with self.assertRaises(ContractError): load_score_extension_plan(root)

    def test_declared_numerics_and_all_prior_dependency_bindings_are_enforced(self):
        from mfg_twin.observer_scores import MASS_ABS_TOL, CONSISTENCY_REL_TOL, CONSISTENCY_ABS_TOL, NONNEGATIVE_ABS_TOL
        for change in ("numerics", "prior_dependency", "prior_source", "warmup", "retry"):
            with self.subTest(change=change), tempfile.TemporaryDirectory(prefix="synthetic-bindings-") as tmp:
                root=Path(tmp);(root/"configs").mkdir()
                document=root/"synthetic-plan.md";document.write_text("SYNTHETIC plan")
                source=root/"synthetic-source.py";source.write_text("# SYNTHETIC source")
                dependency=root/"synthetic-prior.json";dependency.write_text('{"synthetic":true}')
                binding={"path":dependency.name,"sha256":sha(dependency)}
                plan={"study_id":"manufacturing-casper-right-arm-score-extension-v0.1", "documentation":document.name,"documentation_sha256":sha(document),
                      "access":{"check_scores":{"parent_partition":"development"},"training_access":False,"fitting_allowed":False,"calibration_access":False,"protected_final_access":False,"labels_available_to_model":False},
                      "scores":list(SCORES),"preserved_source_sha256":{source.name:sha(source)},"preserved_dependencies_sha256":{dependency.name:sha(dependency)},
                      "numerics":{"probability_mass_absolute_tolerance":MASS_ABS_TOL,"consistency_relative_tolerance":CONSISTENCY_REL_TOL,"consistency_absolute_tolerance":CONSISTENCY_ABS_TOL,"negative_roundoff_absolute_tolerance":NONNEGATIVE_ABS_TOL,"historical_score_and_coordinate_parity":"exact_byte_hash_not_tolerance"},
                      "continuity":{"warmup":1528,"gap_seconds":.075,"subset_expansion":False,"consume_record_at_stop":False},
                      "execution":{"attempts":1,"automatic_retry":False,"fit_calls":0,"score_selection":False}}
                for key in ("data_contract","evaluation_policy","observer_registry","observer_configuration","pending_final_freeze"):
                    plan[key]=dict(binding)
                config=root/PLAN_PATH;config.write_text(json.dumps(plan))
                self.assertEqual(load_score_extension_plan(root)["study_id"],plan["study_id"])
                if change=="numerics":plan["numerics"]["probability_mass_absolute_tolerance"]*=10
                elif change=="prior_dependency":dependency.write_text("SYNTHETIC changed")
                elif change=="prior_source":source.write_text("# SYNTHETIC changed")
                elif change=="warmup":plan["continuity"]["warmup"]-=1
                else:plan["execution"]["automatic_retry"]=True
                config.write_text(json.dumps(plan))
                with self.assertRaises(ContractError):load_score_extension_plan(root)

    def test_output_budget_failure_is_preserved(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-budget-") as tmp:
            study, plan=fixture(tmp);diagnostics={}
            with self.assertRaises(SupervisorError):
                run_score_extension(study,plan,BudgetWriter(Path(tmp)/"out",limit_bytes=100),diagnostics)
            self.assertEqual(diagnostics["status"],"failed")


class ScoreExtensionEntryTests(unittest.TestCase):
    def test_worker_start_is_exclusive(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-attempt-") as tmp:
            writer=BudgetWriter(Path(tmp),limit_bytes=10000)
            ENTRY.claim_worker_start(writer,"synthetic-sha")
            with self.assertRaises(SupervisorError): ENTRY.claim_worker_start(writer,"synthetic-sha")
            self.assertEqual(json.loads((Path(tmp)/"worker_started.json").read_text())["attempt"],1)

    def test_terminal_resource_receipts_fail_closed(self):
        limits=Limits()
        self.assertTrue(ENTRY.resource_receipt_admitted({"process_cpu_seconds":1.,"peak_rss_bytes":10},limits))
        for usage in ({},{"process_cpu_seconds":301,"peak_rss_bytes":10},{"process_cpu_seconds":1,"peak_rss_bytes":2**30+1},{"process_cpu_seconds":math.nan,"peak_rss_bytes":10}):
            self.assertFalse(ENTRY.resource_receipt_admitted(usage,limits))

    def test_stale_or_uncovered_receipt_rejected(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-receipt-") as tmp:
            root=Path(tmp); source=root/"source.py";source.write_text("# synthetic\n")
            receipt={"kind":"synthetic_software_validation_not_benchmark","success":True,"failures":0,"errors":0,"skips":0,"tests_run":1,"expected_failures":0,"unexpected_successes":0,"raw_dataset_opened":False,"trained_models":False,"source_changed_during_tests":[],"executable":sys.executable,"python":sys.version,"source_sha256_at_start":{"source.py":sha(source)}}
            path=root/"receipt.json";path.write_text(json.dumps(receipt))
            with patch.object(ENTRY,"ROOT",root),patch.object(ENTRY,"admission_files",return_value=[source]):
                self.assertEqual(ENTRY.validate_test_receipt(path)["tests_run"],1)
                source.write_text("# changed\n")
                with self.assertRaisesRegex(ValueError,"changed implementation"):
                    ENTRY.validate_test_receipt(path)
                receipt["source_sha256_at_start"]={};path.write_text(json.dumps(receipt))
                with self.assertRaisesRegex(ValueError,"inventory differs"):
                    ENTRY.validate_test_receipt(path)


if __name__ == "__main__":
    unittest.main()
