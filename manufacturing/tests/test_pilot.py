"""Entirely synthetic CSV/pilot fixtures; no CASPER observations or training."""
import csv
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from mfg_twin.contract import ContractError, LoadStats, Study, iter_development_records
from mfg_twin.data import CASPER_HEADER, PartitionSpec
from mfg_twin.pilot import PILOT_PATH, last_progress, load_pilot_plan, run_pilot, validate_run_artifacts
from mfg_twin.supervisor import BudgetWriter
from mfg_twin.velocity import VelocityError

ROOT = Path(__file__).resolve().parents[1]


def synthetic_study(root, *, constant=False, development_offset=0, label="0", invalid_at=None):
    stream = io.StringIO(newline="")
    writer = csv.writer(stream)
    writer.writerow(CASPER_HEADER)
    for row in range(18):
        values = ["SYNTHETIC_UNUSED"] * 20
        values[0] = str(row * 0.05)
        values[1] = json.dumps([float(row)] * 6)
        base = 1000000 if row in (0, 1, 8, 9) else row
        values[2] = json.dumps([float(j if constant else base * (j+1) + j + (development_offset if row >= 8 else 0)) for j in range(6)])
        values[-1] = label
        if row in (6, 7) or row >= 14:
            values[0] = "SYNTHETIC_NOT_A_TIMESTAMP"
            values[1] = values[2] = "SYNTHETIC_INVALID_FEATURES"
        if row == invalid_at:
            values[1] = "SYNTHETIC_INVALID_FEATURES"
        writer.writerow(values)
    payload = stream.getvalue().encode()
    path = Path(root) / "synthetic_only.csv"
    path.write_bytes(payload)
    study = Study(Path(root), path.name, len(payload), hashlib.sha256(payload).hexdigest(),
                  (PartitionSpec("training", 0, 8, warmup=2), PartitionSpec("development", 8, 16, warmup=2)),
                  (("training", ((2, 8),)), ("development", ((10, 16),))))
    plan = {"model": {"id": "SYNTHETIC_velocity_only"}, "access": {
        "fit": {"parent_partition": "training", "rows_half_open": [0, 6], "raw_rows": 6,
                "eligible_intervals_half_open": [[2, 6]], "expected_eligible_rows": 4},
        "check_scores": {"parent_partition": "development", "rows_half_open": [8, 14], "raw_rows": 6,
                         "eligible_intervals_half_open": [[10, 14]], "expected_eligible_rows": 4}}}
    return study, plan


class PilotTests(unittest.TestCase):
    def execute_synthetic(self, root, **kwargs):
        study, plan = synthetic_study(root, **kwargs)
        output = Path(root) / "synthetic_outputs"
        diagnostics = {}
        run_pilot(study, plan, BudgetWriter(output, limit_bytes=1000000), diagnostics)
        return study, plan, output, diagnostics

    def test_exact_subset_fit_scores_and_roundtrip_with_invalid_unparsed_suffix(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-pilot-") as tmp:
            study, plan, output, diagnostics = self.execute_synthetic(tmp)
            self.assertEqual(diagnostics["status"], "completed")
            self.assertEqual(diagnostics["fit_count"], 4)
            self.assertEqual(diagnostics["score_count"], 4)
            self.assertTrue(diagnostics["reference_unchanged"])
            reference = json.loads((output / "reference.json").read_text())["reference"]
            self.assertEqual(reference["mean"], [3.5*(j+1)+j for j in range(6)])
            scores = [json.loads(line) for line in (output / "development_scores.jsonl").read_text().splitlines()]
            self.assertEqual([x["row"] for x in scores], [10, 11, 12, 13])
            self.assertTrue(all(set(x) == {"row", "timestamp", "segment", "score"} for x in scores))
            self.assertEqual(validate_run_artifacts(output, plan)["saved_score_count"], 4)
            self.assertEqual(diagnostics["populations"]["fit"]["exclusions"], {"warmup": 2})
            self.assertEqual(diagnostics["populations"]["check_scores"]["exclusions"], {"warmup": 2})
            for name, traversal in (("fit", 6), ("check_scores", 14)):
                stats = diagnostics["load_stats"][name]
                self.assertEqual(stats["csv_records_traversed"], traversal)
                self.assertEqual(stats["selected_rows_parsed"], 6)
                self.assertEqual(stats["valid_observations"], 6)
                self.assertEqual(stats["hash_bytes"], study.source_bytes)
                self.assertEqual(stats["hash_scans_completed"], 1)
                self.assertTrue(stats["source_verified"])
                self.assertTrue(stats["stream_checks_completed"])

    def test_development_cannot_change_fit(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-A-") as one, tempfile.TemporaryDirectory(prefix="synthetic-B-") as two:
            _, _, output_a, _ = self.execute_synthetic(one)
            _, _, output_b, _ = self.execute_synthetic(two, development_offset=500)
            self.assertEqual((output_a / "reference.json").read_bytes(), (output_b / "reference.json").read_bytes())
            self.assertNotEqual((output_a / "development_scores.jsonl").read_bytes(), (output_b / "development_scores.jsonl").read_bytes())

    def test_labels_cannot_change_fit_or_scores(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-A-") as one, tempfile.TemporaryDirectory(prefix="synthetic-B-") as two:
            _, _, output_a, _ = self.execute_synthetic(one)
            _, _, output_b, _ = self.execute_synthetic(two, label="1")
            for artifact in ("reference.json", "development_scores.jsonl"):
                self.assertEqual((output_a / artifact).read_bytes(), (output_b / artifact).read_bytes())

    def test_constant_channel_fails_before_development_no_fallback(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-constant-") as tmp:
            study, plan = synthetic_study(tmp, constant=True)
            diagnostics = {}
            output = Path(tmp) / "outputs"
            with self.assertRaisesRegex(VelocityError, "nonpositive_variance"):
                run_pilot(study, plan, BudgetWriter(output, limit_bytes=100000), diagnostics)
            self.assertEqual(diagnostics["status"], "failed")
            self.assertEqual(diagnostics["stage"], "fit")
            self.assertEqual(diagnostics["load_stats"]["check_scores"]["hash_bytes"], 0)
            self.assertFalse((output / "reference.json").exists())

    def test_invalid_selected_input_fails_no_mask_revision(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-invalid-") as tmp:
            study, plan = synthetic_study(tmp, invalid_at=11)
            diagnostics = {}
            output = Path(tmp) / "outputs"
            with self.assertRaises(ContractError):
                run_pilot(study, plan, BudgetWriter(output, limit_bytes=100000), diagnostics)
            self.assertEqual(diagnostics["status"], "failed")
            self.assertEqual(diagnostics["stage"], "development_scoring")
            self.assertEqual(diagnostics["score_count"], 1)
            self.assertFalse(diagnostics["load_stats"]["check_scores"]["stream_checks_completed"])

    def test_declared_fit_count_mismatch_fails_after_exhaustion(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-count-") as tmp:
            study, plan = synthetic_study(tmp)
            plan["access"]["fit"]["expected_eligible_rows"] = 3
            with self.assertRaisesRegex(ContractError, "Incomplete pilot support"):
                run_pilot(study, plan, BudgetWriter(Path(tmp)/"outputs", limit_bytes=100000), {})

    def test_plan_hash_fails_before_source_access(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-plan-") as tmp:
            root = Path(tmp)
            (root / "configs").mkdir()
            (root / PILOT_PATH).write_text('{"changed":true}')
            with self.assertRaisesRegex(ContractError, "specification changed"):
                load_pilot_plan(root)

    def test_frozen_plan_metadata_only(self):
        self.assertEqual(load_pilot_plan(ROOT)["access"]["check_scores"]["rows_half_open"], [540002,560002])

    def test_partial_loader_does_not_claim_completed_integrity(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-partial-") as tmp:
            study, _ = synthetic_study(tmp)
            stats = LoadStats()
            stream = iter_development_records(study, "training", stop=6, stats=stats)
            next(stream)
            stream.close()
            self.assertTrue(stats.source_verified)
            self.assertFalse(stats.stream_checks_completed)
            self.assertEqual(stats.csv_records_traversed, 1)

    def test_readback_rejects_missing_duplicate_reordered_and_nonfinite_scores(self):
        for corruption in ("missing", "duplicate", "reordered", "nonfinite"):
            with self.subTest(corruption=corruption), tempfile.TemporaryDirectory(prefix="synthetic-readback-") as tmp:
                _, plan, output, _ = self.execute_synthetic(tmp)
                path = output / "development_scores.jsonl"
                lines = path.read_text().splitlines()
                if corruption == "missing":
                    lines.pop()
                elif corruption == "duplicate":
                    lines[1] = lines[0]
                elif corruption == "reordered":
                    lines.reverse()
                else:
                    row = json.loads(lines[0]); row["score"] = float("inf"); lines[0] = json.dumps(row)
                path.write_text("\n".join(lines)+"\n")
                with self.assertRaises(ContractError):
                    validate_run_artifacts(output, plan)

    def test_readback_rejects_changed_reference(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-reference-") as tmp:
            _, plan, output, _ = self.execute_synthetic(tmp)
            path = output / "reference.json"
            saved = json.loads(path.read_text())
            saved["reference"]["mean"][0] += 1
            path.write_text(json.dumps(saved))
            with self.assertRaises(ContractError):
                validate_run_artifacts(output, plan)

    def test_progress_survives_abrupt_abort_and_partial_last_write(self):
        class AbruptWriter(BudgetWriter):
            def write_json(self, name, value):
                if name == "reference.json":
                    raise KeyboardInterrupt("SYNTHETIC abrupt interruption")
                return super().write_json(name, value)
        with tempfile.TemporaryDirectory(prefix="synthetic-progress-") as tmp:
            study, plan = synthetic_study(tmp)
            output = Path(tmp) / "outputs"
            with self.assertRaises(KeyboardInterrupt):
                run_pilot(study, plan, AbruptWriter(output, limit_bytes=100000), {})
            recovered = last_progress(output)
            self.assertEqual(recovered["stage"], "fit")
            self.assertTrue(recovered["coverage_is_last_known_not_terminal"])
            with (output / "progress.jsonl").open("a") as handle:
                handle.write('{"partial":')
            self.assertEqual(last_progress(output), recovered)


if __name__ == "__main__":
    unittest.main()
