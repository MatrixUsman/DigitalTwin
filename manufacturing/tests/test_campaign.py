"""Explicitly SYNTHETIC frozen-campaign tests. No CASPER observations used."""
from array import array
from copy import deepcopy
from dataclasses import replace
from decimal import Decimal
import csv
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from mfg_twin.campaign import (METHODS, accepted_run, file_ref, read_index, read_scores,
    run_evaluation, run_scoring, sha, validate_calibration, validate_seal, verify_choices, verify_final)
from mfg_twin.campaign_data import delayed_labels, feature_rows, verified_features
from mfg_twin.campaign_models import FrozenRoster
from mfg_twin.contract import ContractError, LoadStats
from mfg_twin.data import PartitionSpec, Observation
from mfg_twin.metrics import Event, calibrate
from mfg_twin.observer_study import run_observer_study
from mfg_twin.observer import PhaseObserver, prepare_observation
from mfg_twin.supervisor import BudgetWriter, SupervisorError
from test_observer_study import fixture as old_fixture

ROOT = Path(__file__).resolve().parents[1]
_path = list(sys.path)
try:
    sys.path.insert(0, str(ROOT / "scripts"))
    _spec = importlib.util.spec_from_file_location("_synthetic_campaign_entry", ROOT / "scripts/run_campaign.py")
    ENTRY = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(ENTRY)
finally:
    sys.path[:] = _path


def fixture(root):
    """Build only synthetic old models, normal calibration and held-out stream."""
    root = Path(root)
    study, plan = old_fixture(root)
    old = root / "synthetic_old_observer"
    run_observer_study(study, plan, BudgetWriter(old, limit_bytes=2000000), {})
    registry = json.loads((root / "synthetic_registry.json").read_text())
    models = {name: json.loads((root / value["model_path"]).read_text()) for name, value in registry["selected"].items()}
    models["observer"] = json.loads((old / "observer.model.json").read_text())
    rows = list(csv.reader((root / "synthetic.csv").read_text().splitlines()))[:105]
    final = deepcopy(rows[81:105])
    for i, row in enumerate(final):
        row[0] = str(Decimal("6.2") + Decimal("0.05") * i)
        row[-1] = "1" if 8 <= i < 14 else "0"
    rows.extend(final)
    # Poison labels throughout calibration. A label-free reader must succeed.
    for row in rows[81:105]:
        row[-1] = "SYNTHETIC_LABEL_MUST_NOT_BE_INTERPRETED"
    # Poison trailing observations. Neither scoring phase can request them.
    trailing = ["SYNTHETIC_PROTECTED"] * 20
    rows.append(trailing)
    text = io.StringIO(newline=""); csv.writer(text).writerows(rows)
    payload = text.getvalue().encode(); (root / "synthetic.csv").write_bytes(payload)
    study = replace(study, source_bytes=len(payload), source_sha256=sha(root / "synthetic.csv"),
        partitions=study.partitions + (PartitionSpec("normal_calibration",80,104,warmup=4),
                                      PartitionSpec("final_replay",104,128,warmup=4)),
        eligible_intervals=study.eligible_intervals + (("normal_calibration",((84,104),)), ("final_replay",((108,128),))))
    return study, models


def replay(root, study, models, partition="normal_calibration", name="calibration"):
    writer = BudgetWriter(Path(root) / name, limit_bytes=2000000)
    diagnostics = {}
    run_scoring(study, models, writer, diagnostics, partition=partition, choice_hash="SYNTHETIC_CHOICE")
    return writer.output_dir, diagnostics


class CampaignTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="synthetic-campaign-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.study, self.models = fixture(self.root)

    def test_all_eleven_complete_and_no_fit_or_label_parse(self):
        before = deepcopy(self.models)
        output, diagnostics = replay(self.root, self.study, self.models)
        receipt = validate_calibration(output, self.study, "SYNTHETIC_CHOICE")
        self.assertEqual(set(receipt["thresholds"]), set(METHODS))
        self.assertTrue(all(v["count"] == 20 and v["rank"] == 20 for v in receipt["thresholds"].values()))
        self.assertEqual(diagnostics["load_stats"]["selected_rows_parsed"], 24)
        self.assertEqual(diagnostics["load_stats"]["csv_records_traversed"], 104)
        self.assertEqual(diagnostics["load_stats"]["hash_scans_completed"], 2)
        self.assertFalse(diagnostics["labels_parsed"])
        self.assertEqual(diagnostics["fit_calls"], 0)
        self.assertEqual(before, self.models)

    def test_no_fitting_functions_called(self):
        with patch("mfg_twin.velocity.fit_velocity", side_effect=AssertionError("forbidden fit")), \
             patch("mfg_twin.controls.fit_standardizer", side_effect=AssertionError("forbidden fit")), \
             patch("mfg_twin.control_study.run_control_study", side_effect=AssertionError("forbidden fit")):
            replay(self.root, self.study, self.models)

    def test_exact_old_api_parity_for_all_controls_and_observer_modes(self):
        output, _ = replay(self.root, self.study, self.models)
        seal, _ = validate_seal(output, self.study, partition="normal_calibration", choice_hash="SYNTHETIC_CHOICE")
        roster = FrozenRoster(self.models)
        observers = {m: PhaseObserver(roster.reference, roster.config, m) for m in roster.observers}
        expected = {m: [] for m in METHODS}
        from mfg_twin.observer_scores import score_observer_proposal
        for record in verified_features(self.study, "normal_calibration", LoadStats()):
            obs = record.observation
            prep = prepare_observation(roster.reference, obs)
            proposals = {m: o.propose(prep) for m,o in observers.items()}
            if obs.dt is None:
                for control in roster.controls.values(): control.reset()
            if record.eligible:
                scores = score_observer_proposal(proposals["synchronized"], prep, roster.config, roster.scales).to_dict()
                scores.update({"O-Follow": roster.scales.scores(proposals["unconstrained"])[0],
                               "O-Free": roster.scales.scores(proposals["free_running"])[0]})
                scores.update({m: c.score(obs) for m,c in roster.controls.items()})
                for m in METHODS: expected[m].append(scores[m])
            for m,o in observers.items(): o.commit(proposals[m])
            for c in roster.controls.values(): c.update(obs)
        for name in METHODS:
            self.assertEqual(list(read_scores(output, seal["scores"][name],20)), expected[name])
        # Exact original historical same-state outputs on the same synthetic data.
        old = self.root / "synthetic_old_observer"
        self.assertEqual((output/"O-R.scores.f64").read_bytes(), (old/"synchronized_residual.scores.f64").read_bytes())

    def test_invalid_or_flipped_labels_cannot_change_features_or_scores(self):
        first, _ = replay(self.root, self.study, self.models)
        path = self.root / "synthetic.csv"
        text = path.read_text().replace("SYNTHETIC_LABEL_MUST_NOT_BE_INTERPRETED", "1")
        path.write_text(text)
        study = replace(self.study, source_bytes=path.stat().st_size, source_sha256=sha(path))
        second, _ = replay(self.root, study, self.models, name="second_synthetic")
        for name in METHODS:
            self.assertEqual((first/(name+".scores.f64")).read_bytes(), (second/(name+".scores.f64")).read_bytes())

    def test_feature_records_have_no_labels_or_detector_coordinates(self):
        record = next(verified_features(self.study, "normal_calibration", LoadStats()))
        self.assertFalse(hasattr(record, "label"))
        self.assertEqual(record.observation.__slots__, ("q", "qdot", "dt"))

    def test_rejects_wrong_partition_before_raw_open(self):
        with patch("pathlib.Path.open", side_effect=AssertionError("raw open")):
            with self.assertRaises(ContractError):
                next(verified_features(self.study, "training", LoadStats()))

    def test_source_hash_failure_preserves_no_seal(self):
        study = replace(self.study, source_sha256="0"*64)
        with self.assertRaises(ContractError): replay(self.root, study, self.models)
        self.assertFalse((self.root/"calibration/score_seal.json").exists())

    def test_incomplete_mask_fails_no_threshold(self):
        study = replace(self.study, eligible_intervals=tuple((k, ((85,104),) if k == "normal_calibration" else v) for k,v in self.study.eligible_intervals))
        with self.assertRaises(ContractError): replay(self.root, study, self.models)
        self.assertFalse((self.root/"calibration/calibration.json").exists())

    def test_nonfinite_or_missing_method_fails_without_seal(self):
        for kind in ("nan", "missing"):
            with self.subTest(kind=kind):
                writer = BudgetWriter(self.root/kind, limit_bytes=2000000)
                bad = {m: 1. for m in METHODS}
                if kind == "nan": bad["O-C"] = float("nan")
                else: del bad["O-C"]
                with patch.object(FrozenRoster, "step", return_value=bad):
                    with self.assertRaises((ContractError, ValueError)):
                        run_scoring(self.study,self.models,writer,{},partition="normal_calibration",choice_hash="SYNTHETIC_CHOICE")
                self.assertFalse((writer.output_dir/"calibration.json").exists())

    def test_tied_quantile_and_real_population_rank_are_exact(self):
        result = calibrate([1.] * 160473, expected_m=160473)
        self.assertEqual((result.rank, result.threshold, result.exceedances), (158869,1.,0))
        result = calibrate(range(160473), expected_m=160473)
        self.assertEqual((result.rank,result.threshold,result.exceedances),(158869,158868.,1604))

    def test_wrong_threshold_rank_and_missing_threshold_rejected(self):
        output,_ = replay(self.root,self.study,self.models)
        path=output/"calibration.json"; original=path.read_text()
        for mutation in ("rank", "threshold", "missing"):
            value=json.loads(original)
            if mutation == "missing": del value["thresholds"]["O-C"]
            else: value["thresholds"]["O-C"][mutation] += 1
            path.write_text(json.dumps(value))
            with self.subTest(mutation=mutation), self.assertRaises(ContractError):
                validate_calibration(output,self.study,"SYNTHETIC_CHOICE")

    def test_changed_scores_or_index_fail_seal_validation(self):
        output,_=replay(self.root,self.study,self.models)
        for name in ("O-C.scores.f64","index.jsonl"):
            path=output/name; old=path.read_bytes();path.write_bytes(old+b"x")
            with self.subTest(name=name),self.assertRaises(ContractError):
                validate_seal(output,self.study,partition="normal_calibration",choice_hash="SYNTHETIC_CHOICE")
            path.write_bytes(old)

    def test_wrong_or_partial_seal_rejected(self):
        output,_=replay(self.root,self.study,self.models)
        path=output/"score_seal.json";old=path.read_text()
        for field,value in (("partition","final_replay"),("model_selection_sha256","other"),("methods",list(METHODS[:-1])),("labels_parsed",True)):
            seal=json.loads(old);seal[field]=value;path.write_text(json.dumps(seal))
            with self.subTest(field=field),self.assertRaises(ContractError):
                validate_seal(output,self.study,partition="normal_calibration",choice_hash="SYNTHETIC_CHOICE")

    def test_reordered_index_rejected_even_with_rehashed_index(self):
        output,_=replay(self.root,self.study,self.models)
        path=output/"index.jsonl";lines=path.read_text().splitlines(True)
        lines[5],lines[6]=lines[6],lines[5];path.write_text(''.join(lines))
        seal=json.loads((output/"score_seal.json").read_text());seal["index"]["sha256"]=sha(path)
        with self.assertRaises(ContractError): read_index(output,seal,self.study)

    def test_label_access_blocked_until_every_score_stream_valid(self):
        output,_=replay(self.root,self.study,self.models,"final_replay","final")
        (output/"AR-4.scores.f64").unlink()
        with patch("mfg_twin.campaign.delayed_labels", side_effect=AssertionError("labels must stay closed")) as labels:
            with self.assertRaises((ContractError,FileNotFoundError)):
                run_evaluation(self.study,output,{},BudgetWriter(self.root/"metrics",limit_bytes=2000000),{},
                               choice_hash="SYNTHETIC_CHOICE",policy={},events=[])
            labels.assert_not_called()

    def test_full_synthetic_calibration_score_seal_delayed_join_and_metrics(self):
        calibration,_=replay(self.root,self.study,self.models)
        thresholds=validate_calibration(calibration,self.study,"SYNTHETIC_CHOICE")["thresholds"]
        final,diagnostics=replay(self.root,self.study,self.models,"final_replay","final")
        self.assertFalse((final/"calibration.json").exists())
        writer=BudgetWriter(self.root/"metrics",limit_bytes=2000000)
        info={}
        policy={"populations":{"held_out_normal":{"rows_half_open":[104,112]},"mixed_final":{"rows_half_open":[112,128]}}}
        run_evaluation(self.study,final,thresholds,writer,info,choice_hash="SYNTHETIC_CHOICE",policy=policy,events=[Event("1",112,118)])
        self.assertEqual(info["status"],"completed")
        self.assertEqual(info["labels_joined"],24)
        self.assertEqual(info["label_load_stats"]["valid_observations"],0)
        for name in METHODS:
            report=json.loads((writer.output_dir/(name+".metrics.json")).read_text())
            self.assertEqual(report["coverage"]["eligible_rows"],20)
            self.assertEqual(report["events"]["denominator"],1)
            self.assertEqual(report["slices"][1]["coverage"]["eligible_rows"],16)
        _, index=validate_seal(final,self.study,partition="final_replay",choice_hash="SYNTHETIC_CHOICE")
        self.assertEqual({v[2] for v in index},{0})  # no reset at report/label boundary
        access=(writer.output_dir/"access.jsonl").read_text().splitlines()
        self.assertEqual(json.loads(access[0])["event"],"label_join_started")

    def test_join_rejects_coordinate_mismatch(self):
        final,_=replay(self.root,self.study,self.models,"final_replay","final")
        _,index=validate_seal(final,self.study,partition="final_replay",choice_hash="SYNTHETIC_CHOICE")
        index[0]=(index[0][0],Decimal("999"),0,False)
        with self.assertRaises(ContractError): delayed_labels(self.study,index,LoadStats())

    def test_join_checks_annotation_intervals_not_just_counts(self):
        cal,_=replay(self.root,self.study,self.models)
        threshold=validate_calibration(cal,self.study,"SYNTHETIC_CHOICE")["thresholds"]
        final,_=replay(self.root,self.study,self.models,"final_replay","final")
        policy={"populations":{"held_out_normal":{"rows_half_open":[104,112]},"mixed_final":{"rows_half_open":[112,128]}}}
        with self.assertRaises(ValueError):
            run_evaluation(self.study,final,threshold,BudgetWriter(self.root/"metrics",limit_bytes=2000000),{},
                choice_hash="SYNTHETIC_CHOICE",policy=policy,events=[Event("1",113,119)])

    def test_failed_run_or_hash_mismatch_not_accepted(self):
        path=self.root/"run.json";path.write_text(json.dumps({"accepted":False,"status":"failed","phase":"score-final","model_selection_sha256":"SYNTHETIC_CHOICE"}))
        with self.assertRaises(ContractError): accepted_run(self.root,file_ref(self.root,path),"score-final","SYNTHETIC_CHOICE")
        with self.assertRaises(ContractError): accepted_run(self.root,{"path":"run.json","sha256":"0"*64},"score-final","SYNTHETIC_CHOICE")

    def test_attempt_cannot_be_reused_after_failure(self):
        path=self.root/"attempt.json"
        ENTRY.claim_attempt(path,{"status":"failed"})
        with self.assertRaises(FileExistsError): ENTRY.claim_attempt(path,{"status":"retry"})
        self.assertEqual(json.loads(path.read_text())["status"],"failed")

    def test_budget_failure_preserves_partial_outputs_without_threshold(self):
        writer=BudgetWriter(self.root/"too_small",limit_bytes=800)
        with self.assertRaises(SupervisorError):
            run_scoring(self.study,self.models,writer,{},partition="normal_calibration",choice_hash="SYNTHETIC_CHOICE")
        self.assertTrue(writer.output_dir.exists())
        self.assertFalse((writer.output_dir/"calibration.json").exists())

    def test_production_admission_rejects_empty_freeze_before_source_access(self):
        path=self.root/"experiments/MODEL_SELECTION_FREEZE_V0.1.json";path.parent.mkdir()
        path.write_text('{}')
        with self.assertRaises(ContractError): verify_choices(self.root)

    def test_fitted_changes_detected(self):
        roster=FrozenRoster(self.models)
        roster.fitted_before["controls"]["V-Z"]["mean"][0]+=1
        with self.assertRaises(ContractError): roster.verify_unchanged()

    def test_changed_model_or_source_binding_rejected_before_raw_access(self):
        from mfg_twin.campaign import CHOICES
        path=self.root/CHOICES;path.parent.mkdir()
        model=self.root/"synthetic_model.json";model.write_text('{}')
        freeze={"status":"frozen_before_calibration","methods":list(METHODS),"fit_allowed":False,
            "calibration_observations_seen":False,"deterministic_runs_each":1,"stochastic_runs":[],
            "source_sha256":{},"inputs":[file_ref(self.root,model)]}
        path.write_text(json.dumps(freeze));model.write_text('{"changed":true}')
        with self.assertRaises(ContractError): verify_choices(self.root)
        freeze["inputs"]=[];freeze["source_sha256"]={"synthetic_model.json":"0"*64}
        path.write_text(json.dumps(freeze))
        with self.assertRaises(ContractError): verify_choices(self.root)

    def test_accepted_flag_cannot_hide_incomplete_run_matrix(self):
        path=self.root/"run.json"
        path.write_text(json.dumps({"accepted":True,"status":"completed","phase":"score-final",
            "model_selection_sha256":"SYNTHETIC_CHOICE","run_matrix":[]}))
        with self.assertRaises(ContractError):
            accepted_run(self.root,file_ref(self.root,path),"score-final","SYNTHETIC_CHOICE")

    def test_worker_calibration_admission_and_failure_receipt(self):
        """Exercise entry wiring with synthetic roots; don't install process limits."""
        from mfg_twin.campaign import CHOICES
        from dataclasses import asdict
        from mfg_twin.supervisor import Limits
        choice=self.root/CHOICES;choice.parent.mkdir();choice.write_text('{}')
        limits=asdict(Limits())
        for mismatch in (False,True):
            name="entry_failure" if mismatch else "entry_success"
            run=self.root/name;run.mkdir()
            resolved={"phase":"calibrate","limits":limits,"model_selection_sha256":sha(choice)}
            (run/"resolved.json").write_text(json.dumps(resolved))
            claim=self.root/"local/campaign_v0.1/calibrate.attempt.json";claim.parent.mkdir(parents=True,exist_ok=True)
            claim.write_text(json.dumps({"run_directory":str(run),"resolved_sha256":"bad" if mismatch else sha(run/"resolved.json")}))
            with patch.object(ENTRY,"ROOT",self.root),patch.object(ENTRY,"install_worker_limits",return_value={}), \
                 patch.object(ENTRY,"load_study",return_value=self.study), \
                 patch.object(ENTRY,"verify_choices",return_value=({}, {"phase_budgets":{"calibrate":limits}}, self.models)), \
                 patch.object(ENTRY,"verify_environment"),patch.object(ENTRY,"install_worker_scope"):
                result=ENTRY.worker(run)
            self.assertEqual(result,1 if mismatch else 0)
            diagnostic=json.loads((run/"diagnostics.json").read_text())
            self.assertEqual(diagnostic["status"],"failed" if mismatch else "completed")
            if mismatch:self.assertFalse((run/"score_seal.json").exists())

    def test_empty_final_record_rejected_without_raw_source(self):
        from mfg_twin.campaign import FINAL,CHOICES
        path=self.root/FINAL;path.parent.mkdir();path.write_text('{}')
        (self.root/CHOICES).write_text('{}')
        with patch("mfg_twin.campaign.verify_choices",return_value=({}, {}, self.models)):
            with self.assertRaises(ContractError):verify_final(self.root,self.study)

    def test_incomplete_threshold_roster_cannot_open_labels(self):
        output,_=replay(self.root,self.study,self.models,"final_replay","final")
        with patch("mfg_twin.campaign.delayed_labels") as labels:
            with self.assertRaises(ContractError):
                run_evaluation(self.study,output,{},BudgetWriter(self.root/"metrics",limit_bytes=2000000),{},
                    choice_hash="SYNTHETIC_CHOICE",policy={},events=[])
            labels.assert_not_called()

    def test_early_eligible_endpoint_rejected(self):
        roster=FrozenRoster(self.models)
        record=next(verified_features(self.study,"normal_calibration",LoadStats()))
        with self.assertRaises(ContractError): roster.step(record.observation,True)


if __name__ == "__main__":
    unittest.main()
