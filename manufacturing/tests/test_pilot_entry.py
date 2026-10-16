"""SYNTHETIC admission/guard fixtures; never execute the pilot or read raw data.

The entry module is imported without main(). Receipt inventories are fake files
inside temporary directories. Audit callbacks are captured and called directly:
no actual socket, child process, raw open, worker, or --execute invocation occurs.
"""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from mfg_twin.supervisor import BudgetWriter, SupervisorError


ENTRY_PATH = Path(__file__).resolve().parents[1] / "scripts" / "run_bounded_pilot.py"
_spec = importlib.util.spec_from_file_location("_synthetic_pilot_entry_under_test", ENTRY_PATH)
ENTRY = importlib.util.module_from_spec(_spec)
_original_path = list(sys.path)
try:
    _spec.loader.exec_module(ENTRY)
finally:
    sys.path[:] = _original_path


class TestReceiptAdmission(unittest.TestCase):
    def setUp(self):
        self.storage = tempfile.TemporaryDirectory(prefix="synthetic-pilot-admission-")
        self.addCleanup(self.storage.cleanup)
        self.root = Path(self.storage.name).resolve()
        fake_sources = {
            "src/mfg_twin/synthetic_control.py": "# SYNTHETIC source fixture\n",
            "tests/test_synthetic.py": "# SYNTHETIC test fixture\n",
            "tests/fixtures/synthetic.json": '{"synthetic": true}\n',
            "scripts/run_synthetic_tests.py": "# SYNTHETIC runner fixture\n",
            "scripts/run_bounded_pilot.py": "# SYNTHETIC entry fixture\n",
            "pyproject.toml": "# SYNTHETIC metadata fixture\n",
            "configs/casper_right_arm_pilot_v0.1.json": '{"synthetic": true}\n',
        }
        for relative, text in fake_sources.items():
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
        for name, value in (("ROOT", self.root),
                            ("__file__", str(self.root / "scripts/run_bounded_pilot.py"))):
            patcher = patch.object(ENTRY, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        self.receipt_path = self.root / "synthetic_receipt.json"
        self.receipt = {
            "kind": "synthetic_software_validation_not_benchmark", "project": "manufacturing",
            "success": True, "failures": 0, "errors": 0, "skips": 0,
            "tests_run": 1, "expected_failures": 0, "unexpected_successes": 0,
            "raw_dataset_opened": False, "trained_models": False,
            "source_changed_during_tests": [], "blocked_access_attempts": [],
            "executable": sys.executable, "python": sys.version,
            "source_sha256_at_start": {
                str(path.relative_to(self.root)): ENTRY.digest(path)
                for path in ENTRY.admission_files()
            },
        }

    def validate(self):
        self.receipt_path.write_text(json.dumps(self.receipt))
        return ENTRY.validate_test_receipt(self.receipt_path)

    def test_synthetic_matching_current_inventory_and_interpreter_admitted(self):
        self.assertEqual(self.validate(), self.receipt)

    def test_synthetic_modified_code_rejected(self):
        (self.root / "src/mfg_twin/synthetic_control.py").write_text("# changed SYNTHETIC source\n")
        with self.assertRaisesRegex(ValueError, "changed implementation"):
            self.validate()

    def test_synthetic_unhashed_new_source_rejected(self):
        (self.root / "src/mfg_twin/unhashed.py").write_text("# new SYNTHETIC source\n")
        with self.assertRaises(ValueError):
            self.validate()

    def test_synthetic_deleted_test_rejected(self):
        (self.root / "tests/test_synthetic.py").unlink()
        with self.assertRaises(ValueError):
            self.validate()

    def test_synthetic_removed_receipt_inventory_entry_rejected(self):
        self.receipt["source_sha256_at_start"].pop("src/mfg_twin/synthetic_control.py")
        with self.assertRaises(ValueError):
            self.validate()

    def test_synthetic_changed_configuration_rejected(self):
        (self.root / "configs/casper_right_arm_pilot_v0.1.json").write_text('{"synthetic": "changed"}\n')
        with self.assertRaises(ValueError):
            self.validate()

    def test_synthetic_failed_skipped_empty_or_expected_failure_receipts_rejected(self):
        invalid = [("success", False), ("failures", 1), ("errors", 1), ("skips", 1),
                   ("tests_run", 0), ("tests_run", True), ("expected_failures", 1),
                   ("unexpected_successes", 1), ("source_changed_during_tests", ["synthetic.py"])]
        for name, value in invalid:
            previous = self.receipt[name]
            self.receipt[name] = value
            try:
                with self.subTest(name=name, value=value), self.assertRaises(ValueError):
                    self.validate()
            finally:
                self.receipt[name] = previous

    def test_synthetic_missing_test_count_rejected(self):
        self.receipt.pop("tests_run")
        with self.assertRaises(ValueError):
            self.validate()

    def test_synthetic_changed_interpreter_or_version_rejected(self):
        for name, value in [("executable", "/synthetic/wrong/python"), ("python", "synthetic wrong version")]:
            previous = self.receipt[name]
            self.receipt[name] = value
            try:
                with self.subTest(name=name), self.assertRaises(ValueError):
                    self.validate()
            finally:
                self.receipt[name] = previous

    def test_synthetic_raw_or_training_scope_receipts_rejected(self):
        for name in ("raw_dataset_opened", "trained_models"):
            self.receipt[name] = True
            try:
                with self.subTest(name=name), self.assertRaises(ValueError):
                    self.validate()
            finally:
                self.receipt[name] = False


class WorkerScopeTests(unittest.TestCase):
    def setUp(self):
        self.storage = tempfile.TemporaryDirectory(prefix="synthetic-worker-guard-")
        self.addCleanup(self.storage.cleanup)
        self.root = Path(self.storage.name).resolve()
        self.source = self.root / "datasets/raw/synthetic_allowed.csv"
        # Only capture the callback. Installing a real audit hook is permanent
        # for a process and would change later tests' scope.
        with patch.object(ENTRY.sys, "addaudithook") as register:
            ENTRY.install_worker_scope(self.source)
        register.assert_called_once()
        self.guard = register.call_args.args[0]

    def test_synthetic_selected_source_read_allowed_without_opening_it(self):
        self.guard("open", (str(self.source), "r", os.O_RDONLY))
        self.guard("open", (os.fsencode(self.source), "rb", os.O_RDONLY))
        self.assertFalse(self.source.exists())

    def test_synthetic_other_raw_member_and_other_project_rejected(self):
        for path in (self.root / "datasets/raw/other.csv",
                     self.root / "water/datasets/raw/synthetic.csv"):
            with self.subTest(path=path), self.assertRaises(PermissionError):
                self.guard("open", (str(path), "r", os.O_RDONLY))

    def test_synthetic_selected_source_write_modes_and_flags_rejected(self):
        for mode in ("w", "a", "x", "r+", "w+b"):
            with self.subTest(mode=mode), self.assertRaises(PermissionError):
                self.guard("open", (str(self.source), mode, os.O_RDONLY))
        for flags in (os.O_WRONLY, os.O_RDWR, os.O_CREAT, os.O_TRUNC):
            with self.subTest(flags=flags), self.assertRaises(PermissionError):
                self.guard("open", (str(self.source), None, flags))

    def test_synthetic_path_alias_cannot_open_other_raw_member(self):
        alias = self.root / "synthetic_alias.csv"
        target = self.root / "datasets/raw/other.csv"
        alias.symlink_to(target)
        with self.assertRaises(PermissionError):
            self.guard("open", (str(alias), "r", os.O_RDONLY))
        self.assertFalse(target.exists())

    def test_synthetic_source_readonly_also_outside_raw_named_directory(self):
        source = self.root / "authorized_external_source.csv"
        with patch.object(ENTRY.sys, "addaudithook") as register:
            ENTRY.install_worker_scope(source)
        guard = register.call_args.args[0]
        guard("open", (str(source), "r", os.O_RDONLY))
        with self.assertRaises(PermissionError):
            guard("open", (str(source), "w", os.O_WRONLY))

    def test_synthetic_network_child_and_exec_events_rejected_without_execution(self):
        events = ("socket.__new__", "socket.connect", "socket.getaddrinfo", "socket.bind",
                  "subprocess.Popen", "os.system", "os.fork", "os.posix_spawn", "os.exec")
        for event in events:
            with self.subTest(event=event), self.assertRaises(PermissionError):
                self.guard(event, ())

    def test_synthetic_ordinary_artifact_open_is_allowed(self):
        path = self.root / "synthetic_artifacts/reference.json"
        self.guard("open", (str(path), "w", os.O_WRONLY | os.O_CREAT))
        self.assertFalse(path.exists())


class WorkerAttemptTests(unittest.TestCase):
    def test_synthetic_worker_start_token_blocks_repeat_and_preserves_first_claim(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-worker-claim-") as temporary:
            directory = Path(temporary)
            writer = BudgetWriter(directory, limit_bytes=10000)
            ENTRY.claim_worker_start(writer, "a" * 64)
            token = directory / "worker_started.json"
            original = token.read_bytes()
            parsed = json.loads(original)
            self.assertEqual(parsed["attempt"], 1)
            self.assertEqual(parsed["resolved_config_sha256"], "a" * 64)
            for digest in ("a" * 64, "b" * 64):
                fresh_writer = BudgetWriter(directory, limit_bytes=10000)
                with self.subTest(digest=digest), self.assertRaises(SupervisorError):
                    ENTRY.claim_worker_start(fresh_writer, digest)
                self.assertEqual(token.read_bytes(), original)
            self.assertEqual([p.name for p in directory.iterdir()], ["worker_started.json"])


if __name__ == "__main__":
    unittest.main()
