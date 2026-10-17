"""Explicitly SYNTHETIC observer-run admission, alignment and isolation checks."""
from array import array
from dataclasses import replace
import csv
import hashlib
import importlib.util
import io
import json
import math
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from mfg_twin.contract import ContractError
from mfg_twin.control_study import run_control_study
from mfg_twin.controls import Standardizer12, TemplateReference
from mfg_twin.observer_study import (OBSERVER_PLAN_PATH, MODES, Recurrence, ProspectiveForecasts, Progression,
    load_observer_plan, load_references, run_observer_study, validate_observer_artifacts, template_kinematics, sha)
from mfg_twin.supervisor import BudgetWriter, Limits, SupervisorError
from test_control_study import synthetic_study

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("_synthetic_observer_entry",ROOT/"scripts/run_observer_study.py")
ENTRY = importlib.util.module_from_spec(_spec)
_original = list(sys.path)
try:
    _spec.loader.exec_module(ENTRY)
finally:
    sys.path[:] = _original


def fixture(root, development_offset=0., label="0"):
    root = Path(root)
    study, oldplan = synthetic_study(root, development_offset=development_offset,label=label)
    rows = list(csv.reader((root/"synthetic.csv").read_text().splitlines()))
    for i,row in enumerate(rows[1:105]):
        for j in (1,2):
            row[j] = json.dumps([v + .03*math.sin(i*.31+j+k) for k,v in enumerate(json.loads(row[j]))])
    stream = io.StringIO(newline=""); csv.writer(stream).writerows(rows)
    payload = stream.getvalue().encode(); (root/"synthetic.csv").write_bytes(payload)
    study = replace(study, source_bytes=len(payload),source_sha256=hashlib.sha256(payload).hexdigest())
    previous = root/"previous_synthetic_controls"
    run_control_study(study,oldplan,BudgetWriter(previous,limit_bytes=1000000),{})
    (previous/"run.json").write_text('{"explicitly_synthetic":true}')
    selected = json.loads((previous/"selected_artifacts.json").read_text())["selection"]
    # Fixed SYNTHETIC prior models prevent development selection in the fixture
    # from changing inputs to the new observer-isolation test.
    candidates=json.loads((previous/"candidate_results.json").read_text())["candidates"]
    for family,identifier in (("template","template_bins4"),("ar","ar_p2_ridge0.001")):
        candidate=next(x for x in candidates if x["id"]==identifier)
        selected[family]={"candidate_id":identifier,"model_artifact":candidate["model_artifact"],"model_state_sha256":candidate["model_state_sha256_before"]}
    registry = {"selection_partition":"development","refit_on_development":False,"training_eligible_count":72,
                "development_eligible_count":20,"thresholds":None,"final_test_admitted":False,
                "source_run":previous.name,"run_manifest_sha256":sha(previous/"run.json"),"selected":{}}
    for family,entry in selected.items():
        model = previous/entry["model_artifact"]
        registry["selected"][family] = dict(entry,model_path=str(model.relative_to(root)),model_file_sha256=sha(model))
    registry_path = root/"synthetic_registry.json"; registry_path.write_text(json.dumps(registry))
    plan = {"access":oldplan["access"],"selected_controls":{"path":registry_path.name,"sha256":sha(registry_path)},
            "model":{"initialization":4,"mixing_rate":.02,"temperature_floor":1e-8,"normalizer_floor":0.},
            "diagnostics":{"stride":2,"recurrence_factors":[.5,.9,1.,1.1],"recurrence_tolerance_seconds":.075,
                           "horizons_seconds":[.1,.25],"forecast_tolerance_seconds":.075}}
    return study,plan


class ObserverStudyTests(unittest.TestCase):
    def execute(self, directory, **kwargs):
        study,plan=fixture(directory,**kwargs)
        output=Path(directory)/"synthetic_observer_outputs"; diagnostics={}
        run_observer_study(study,plan,BudgetWriter(output,limit_bytes=2000000),diagnostics)
        return study,plan,output,diagnostics

    def test_complete_support_immutable_references_and_saved_readback(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-observer-") as tmp:
            study,plan,output,diagnostics=self.execute(tmp)
            self.assertEqual(diagnostics["status"],"completed")
            self.assertEqual(diagnostics["score_counts"],dict.fromkeys(("synchronized_residual","synchronized_evidence","unconstrained_residual","free_running_residual"),20))
            self.assertTrue(diagnostics["reference_unchanged"])
            self.assertEqual(diagnostics["fitted_emission_scale"]["nearest_template_MSE"]["n"],72)
            self.assertEqual(diagnostics["load_stats"]["check_scores"]["csv_records_traversed"],104)
            self.assertEqual(validate_observer_artifacts(output,plan)["saved_index_rows"],20)
            results=json.loads((output/"observer_results.json").read_text())
            for partition in results["partitions"].values():
                counts={x["standardized_MSE"]["n"] for x in partition["recurrence"].values()}
                self.assertEqual(len(counts),1)
                for forecast in partition["prospective_forecasts"].values():
                    self.assertEqual(forecast["issued"],forecast["censored"]+forecast["synchronized"]["n"])
            self.assertFalse(diagnostics["calibration_or_final_observations_parsed"])

    def test_development_observations_cannot_change_bandwidth_or_evidence_scales(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-A-") as a,tempfile.TemporaryDirectory(prefix="synthetic-B-") as b:
            _,_,first,_=self.execute(a)
            _,_,second,_=self.execute(b,development_offset=100.)
            self.assertEqual(json.loads((first/"input_references.json").read_text())["template_state_sha256"],json.loads((second/"input_references.json").read_text())["template_state_sha256"])
            self.assertEqual(json.loads((first/"observer.model.json").read_text())["emission_scale_fit"],
                             json.loads((second/"observer.model.json").read_text())["emission_scale_fit"])
            self.assertEqual((first/"observer.model.json").read_bytes(),(second/"observer.model.json").read_bytes())
            self.assertNotEqual((first/"synchronized_residual.scores.f64").read_bytes(),(second/"synchronized_residual.scores.f64").read_bytes())

    def test_changed_labels_do_not_change_observer_models_or_scores(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-A-") as a,tempfile.TemporaryDirectory(prefix="synthetic-B-") as b:
            _,_,first,_=self.execute(a)
            _,_,second,_=self.execute(b,label="1")
            for path in [first/"observer.model.json",*first.glob("*.scores.f64")]:
                self.assertEqual(path.read_bytes(),(second/path.name).read_bytes())

    def test_changed_selected_reference_rejected_before_raw_access(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-reference-") as tmp:
            study,plan=fixture(tmp)
            registry=json.loads((Path(tmp)/plan["selected_controls"]["path"]).read_text())
            path=Path(tmp)/registry["selected"]["template"]["model_path"]
            path.write_text("SYNTHETIC CORRUPTION")
            with self.assertRaisesRegex(ContractError,"file identity"):
                load_references(Path(tmp),plan)

    def test_protected_or_subset_access_rejected(self):
        for change in ("protected","subset"):
            with self.subTest(change=change),tempfile.TemporaryDirectory(prefix="synthetic-scope-") as tmp:
                study,plan=fixture(tmp)
                if change=="protected": plan["access"]["fit"]["parent_partition"]="normal_calibration"
                else: plan["access"]["fit"]["rows_half_open"][1]-=1
                with self.assertRaises(ContractError):
                    run_observer_study(study,plan,BudgetWriter(Path(tmp)/"out",limit_bytes=2000000),{})

    def test_failed_scientific_checks_do_not_masquerade_as_execution_failure_or_twin(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-negative-") as tmp:
            _,_,output,diagnostics=self.execute(tmp,development_offset=50.)
            self.assertEqual(diagnostics["status"],"completed")
            self.assertFalse(diagnostics["validity"]["physical_digital_twin_established"])
            self.assertFalse(diagnostics["validity"]["all_predeclared_checks_pass"])
            self.assertTrue((output/"observer_results.json").exists())

    def test_saved_index_scores_model_criteria_corruption_rejected(self):
        for change in ("index","score","model","criteria"):
            with self.subTest(change=change),tempfile.TemporaryDirectory(prefix="synthetic-readback-") as tmp:
                _,plan,output,_=self.execute(tmp)
                if change=="index":
                    path=output/"development_index.jsonl"; lines=path.read_text().splitlines(); lines[1]=lines[0];path.write_text("\n".join(lines)+"\n")
                elif change=="score":
                    path=output/"synchronized_residual.scores.f64";path.write_bytes(path.read_bytes()[:-8])
                elif change=="model":
                    path=output/"observer.model.json";value=json.loads(path.read_text());value["observer_config"]["temperature"]*=2;path.write_text(json.dumps(value))
                else:
                    path=output/"observer_results.json";value=json.loads(path.read_text());value["validity"]["criteria"][0]["passed"]=not value["validity"]["criteria"][0]["passed"];path.write_text(json.dumps(value))
                with self.assertRaises(ContractError): validate_observer_artifacts(output,plan)

    def test_document_change_rejects_before_raw_access(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-docbinding-") as tmp:
            root=Path(tmp);(root/"configs").mkdir();document=root/"synthetic_plan.md";document.write_text("SYNTHETIC original")
            config={"study_id":"manufacturing-casper-right-arm-observer-v0.1","access":{"calibration_access":False,"protected_final_access":False,"labels_available_to_model":False},"documentation":document.name,"documentation_sha256":sha(document)}
            (root/OBSERVER_PLAN_PATH).write_text(json.dumps(config));document.write_text("SYNTHETIC changed")
            with self.assertRaisesRegex(ContractError,"documentation changed"):load_observer_plan(root)


class DiagnosticTests(unittest.TestCase):
    def test_known_circular_position_derivative_maps_physical_units_and_rejects_wrong_velocity(self):
        bins=8; period=4.; step=period/bins
        means=tuple(10.+j for j in range(12)); sigmas=tuple(1.+j for j in range(12))
        scaler=Standardizer12(16,means,tuple(x*x for x in sigmas),sigmas)
        positions=[[means[j]+(j+1)*math.sin(2*math.pi*k/bins) for j in range(6)] for k in range(bins)]
        velocities=[[(positions[(k+1)%bins][j]-positions[(k-1)%bins][j])/(2*step) for j in range(6)] for k in range(bins)]
        def ref(wrong=False):
            rows=[]
            for k in range(bins):
                physical=positions[k]+[(-v if wrong else v) for v in velocities[k]]
                rows.append(tuple((x-m)/s for x,m,s in zip(physical,means,sigmas)))
            return TemplateReference(scaler,period,bins,4,16,tuple(rows),(2,)*bins)
        exact=template_kinematics(ref())
        self.assertTrue(exact["aggregate_better_than_training_mean"])
        self.assertLess(max(exact["per_joint_MSE"]),1e-25)
        # With a zero training mean velocity, reversing the derivative produces
        # four times the zero-velocity baseline error, independently known.
        wrong_ref=ref(True)
        zero_velocity_scaler=replace(scaler,mean=means[:6]+(0.,)*6)
        physical_rows=[]
        for k in range(bins):
            physical=positions[k]+[-v for v in velocities[k]]
            physical_rows.append(tuple((x-m)/s for x,m,s in zip(physical,zero_velocity_scaler.mean,sigmas)))
        wrong_ref=replace(wrong_ref,scaler=zero_velocity_scaler,means=tuple(physical_rows))
        wrong=template_kinematics(wrong_ref)
        self.assertFalse(wrong["aggregate_better_than_training_mean"])
        for ratio in wrong["per_joint_ratio"]:self.assertAlmostEqual(ratio,4.)

    def test_progression_wraps_forward_and_reset_prevents_cross_gap_comparison(self):
        progression=Progression(32,32.)
        progression.observe(0.,31);progression.observe(1.,0)
        self.assertEqual(progression.displacement.mean,1.)
        self.assertEqual(progression.deviation.mean,0.)
        progression.reset();progression.observe(0.,20)
        self.assertEqual(progression.displacement.n,1)
        progression.observe(1.,19)
        self.assertEqual(progression.to_dict()["backward_fraction"],.5)

    def test_native_recurrence_support_is_paired_even_for_fractional_sample_lags(self):
        recurrence=Recurrence(1.,(.5,.9,1.,1.1),.0251)
        for i in range(200):
            values=(math.sin(i*.05*2*math.pi),)*12
            recurrence.observe(i*.05,values,True,i%20==0)
        counts=[v["standardized_MSE"]["n"] for v in recurrence.to_dict().values()]
        self.assertEqual(len(set(counts)),1);self.assertGreater(counts[0],0)
        self.assertEqual(recurrence.attempted,recurrence.matched+sum(recurrence.unmatched.values()))
        recurrence.reset();recurrence.observe(0.,(0.,)*12,True,True)
        self.assertEqual(len(recurrence.history),1)

    def test_native_recurrence_does_not_bridge_gap_or_ineligible_endpoint(self):
        recurrence=Recurrence(1.,(.5,.9,1.,1.1),.075)
        for i in range(50):recurrence.observe(i*.05,(0.,)*12,False,False)
        recurrence.observe(2.5,(0.,)*12,True,True)
        self.assertEqual(recurrence.matched,0)
        self.assertEqual(recurrence.unmatched["ineligible_past_endpoint"],1)

    def test_forecast_is_saved_at_origin_and_matched_once_at_first_future_time(self):
        class SyntheticForecast:
            prediction=(1.,)*12
        class SyntheticObserver:
            def forecast(self,horizon):return SyntheticForecast()
        forecasts=ProspectiveForecasts((1.,),.075)
        forecasts.issue(0.,(0.,)*12,dict.fromkeys(MODES,SyntheticObserver()))
        forecasts.observe(.95,(100.,)*12,True)
        self.assertEqual(forecasts.stats["1.0"]["synchronized"].n,0)
        forecasts.observe(1.04,(1.,)*12,True)
        forecasts.observe(1.05,(100.,)*12,True)
        self.assertEqual(forecasts.stats["1.0"]["synchronized"].n,1)
        self.assertEqual(forecasts.stats["1.0"]["synchronized"].mean,0)
        self.assertAlmostEqual(forecasts.stats["1.0"]["matching_error_seconds"].mean,.04)
        forecasts.issue(2.,(0.,)*12,dict.fromkeys(MODES,SyntheticObserver()));forecasts.reset()
        self.assertEqual(forecasts.censored["1.0"],1)

    def test_late_or_ineligible_forecast_target_censored_without_changing_scores(self):
        class S:
            def forecast(self,horizon):return type("F",(),{"prediction":(0.,)*12})()
        for elapsed,eligible in ((1.1,True),(1.02,False)):
            forecasts=ProspectiveForecasts((1.,),.075)
            forecasts.issue(0.,(0.,)*12,dict.fromkeys(MODES,S()))
            forecasts.observe(elapsed,(0.,)*12,eligible)
            self.assertEqual(forecasts.censored["1.0"],1)
            self.assertEqual(forecasts.stats["1.0"]["synchronized"].n,0)


class ObserverEntryTests(unittest.TestCase):
    def test_resource_receipt_rejects_missing_or_overrun(self):
        limits=Limits()
        self.assertTrue(ENTRY.resource_receipt_admitted({"process_cpu_seconds":1.,"peak_rss_bytes":123},limits))
        self.assertFalse(ENTRY.resource_receipt_admitted({},limits))
        self.assertFalse(ENTRY.resource_receipt_admitted({"process_cpu_seconds":301.,"peak_rss_bytes":123},limits))

    def test_attempt_cannot_be_replayed(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-attempt-") as tmp:
            writer=BudgetWriter(Path(tmp),limit_bytes=10000)
            ENTRY.claim_worker_start(writer,"a"*64)
            with self.assertRaises(SupervisorError):ENTRY.claim_worker_start(writer,"a"*64)

    def test_inventory_covers_runner_models_config(self):
        names={str(p.relative_to(ROOT)) for p in ENTRY.admission_files()}
        for name in ("scripts/run_observer_study.py","src/mfg_twin/observer_study.py","src/mfg_twin/observer.py","tests/test_observer_study.py","configs/casper_right_arm_observer_v0.1.json"):
            self.assertIn(name,names)


if __name__=="__main__":unittest.main()
