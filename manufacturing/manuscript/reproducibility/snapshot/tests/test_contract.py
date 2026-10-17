"""Contract metadata and explicitly synthetic byte-stream tests; no raw reads."""
import hashlib
import io
import csv
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from mfg_twin.contract import (
    CONTRACT_PATH, POLICY_PATH, ContractError, ProtectedPartitionError, Study,
    iter_development_records, load_study, verify_source,
)
from mfg_twin.data import CASPER_HEADER, PartitionSpec

ROOT = Path(__file__).resolve().parents[1]


class ContractTests(unittest.TestCase):
    def synthetic_study(self, root, *, invalid_at=None, intervals=((2, 8),)):
        """Entirely invented bytes; deliberately not the production CASPER receipt."""
        path = Path(root)/"synthetic.csv"
        stream = io.StringIO(newline="")
        writer = csv.writer(stream);writer.writerow(CASPER_HEADER)
        for row in range(8):
            values = ["UNUSED_SYNTHETIC"]*20
            values[0] = str(row/20)
            values[1] = json.dumps([float(row)]*6) if row != invalid_at else "[1]"
            values[2] = json.dumps([float(row+1)]*6)
            values[-1] = "0"
            writer.writerow(values)
        payload = stream.getvalue().encode();path.write_bytes(payload)
        return Study(Path(root), path.name, len(payload), hashlib.sha256(payload).hexdigest(),
                     (PartitionSpec("training", 0, 8, warmup=2),), (("training", intervals),))

    def test_frozen_populations_and_support(self):
        study = load_study(ROOT)
        expected = {"training":536946, "development":160472, "normal_calibration":160473,
                    "held_out_normal":214473, "mixed_final":682646, "final_replay":897119}
        for name, count in expected.items():
            with self.subTest(name=name):
                self.assertEqual(sum(1 for _ in study.expected_eligible_rows(name)), count)
        self.assertEqual(study.partition("training").start, 0)
        self.assertEqual(study.partition("final_replay").start, 864003)
        for name in ("held_out_normal", "mixed_final"):
            with self.assertRaises(ContractError):
                study.partition(name)  # Reporting slices must not restart state.

    def test_successful_synthetic_wrapper_full_and_prefix(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-source-") as tmp:
            study = self.synthetic_study(tmp)
            path = Path(tmp)/study.source_relative_path
            before = path.read_bytes()
            full = list(iter_development_records(study, "training"))
            prefix = list(iter_development_records(study, "training", stop=5))
            self.assertEqual(prefix, full[:5])
            self.assertEqual([p.row for p in full if p.eligible], list(range(2,8)))
            self.assertEqual(path.read_bytes(), before)

    def test_synthetic_mask_disagreement_fails(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-source-") as tmp:
            study = self.synthetic_study(tmp, intervals=((3,8),))
            with self.assertRaises(ContractError):
                list(iter_development_records(study, "training"))

    def test_invalid_observation_even_inside_capped_warmup_fails(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-source-") as tmp:
            study = self.synthetic_study(tmp, invalid_at=0)
            with self.assertRaisesRegex(ContractError, "invalid observation"):
                list(iter_development_records(study, "training", stop=1))

    def test_changed_synthetic_source_rejected(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-source-") as tmp:
            study = self.synthetic_study(tmp)
            path = Path(tmp)/study.source_relative_path
            path.write_bytes(path.read_bytes().replace(b"UNUSED", b"CHANGED",1))
            with self.assertRaises(ContractError):
                list(iter_development_records(study, "training"))

    def test_protected_access_rejected_before_open(self):
        study = load_study(ROOT)
        with patch.object(Path, "open", side_effect=AssertionError("must not open a source")):
            for name in ("normal_calibration", "held_out_normal", "mixed_final", "final_replay", "arbitrary"):
                with self.subTest(name=name), self.assertRaises(ProtectedPartitionError):
                    list(iter_development_records(study, name))

    def test_prefix_cannot_cross_partition_or_move_start(self):
        study = load_study(ROOT)
        with patch.object(Path, "open", side_effect=AssertionError("must not open a source")):
            for end in (540002, 702003, True, 0, 540002.5):
                with self.subTest(end=end), self.assertRaises(ContractError):
                    list(iter_development_records(study, "development", stop=end))

    def test_changed_policy_rejected(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-contract-") as tmp:
            root = Path(tmp); (root/"configs").mkdir()
            (root/CONTRACT_PATH).write_bytes((ROOT/CONTRACT_PATH).read_bytes())
            policy = json.loads((ROOT/POLICY_PATH).read_text())
            policy["calibration"]["quantile_numerator"] = 50
            (root/POLICY_PATH).write_text(json.dumps(policy))
            with self.assertRaisesRegex(ContractError, "hash mismatch"):
                load_study(root)

    def test_synthetic_fingerprint_and_rewind(self):
        payload = b"SYNTHETIC fixture only\n"
        stream = io.BytesIO(payload)
        verify_source(stream, expected_bytes=len(payload), expected_sha256=hashlib.sha256(payload).hexdigest())
        self.assertEqual(stream.tell(), 0)
        for size, digest in [(1, hashlib.sha256(payload).hexdigest()), (len(payload), "0"*64)]:
            with self.assertRaises(ContractError):
                verify_source(stream, expected_bytes=size, expected_sha256=digest)


if __name__ == "__main__":
    unittest.main()
