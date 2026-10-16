"""SYNTHETIC supervisor tests: only temporary files and toy child processes."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

from mfg_twin.supervisor import (BudgetWriter, Limits, SupervisorError,
                                 directory_bytes, install_worker_limits,
                                 read_rss_bytes, supervise, worker_usage)


class BudgetTests(unittest.TestCase):
    def test_synthetic_aggregate_prewrite_cap_preserves_existing_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            writer = BudgetWriter(Path(tmp), limit_bytes=100, reserve_bytes=20)
            writer.write_text("first.txt", "a" * 60)
            with self.assertRaises(SupervisorError):
                writer.write_text("second.txt", "b" * 21)
            self.assertFalse((Path(tmp) / "second.txt").exists())
            writer.append_text("first.txt", "b" * 20)
            self.assertEqual(writer.bytes_used, 80)
            with self.assertRaises(SupervisorError):
                writer.append_text("first.txt", "x")
            self.assertEqual(writer.bytes_used, 80)
            parent = BudgetWriter(Path(tmp), limit_bytes=100)
            parent.write_text("parent.txt", "p" * 20)
            self.assertEqual(directory_bytes(Path(tmp)), 100)

    def test_synthetic_utf8_count_json_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            writer = BudgetWriter(Path(tmp), limit_bytes=200)
            writer.write_text("unicode.txt", "é")
            self.assertEqual(writer.bytes_used, 2)
            writer.write_json("status.json", {"synthetic": True})
            self.assertEqual(json.loads((Path(tmp) / "status.json").read_text()), {"synthetic": True})
            with self.assertRaises(SupervisorError):
                writer.write_text("unicode.txt", "replacement")
            with self.assertRaises(ValueError):
                writer.write_json("invalid.json", {"x": float("nan")})
            self.assertFalse((Path(tmp) / "invalid.json").exists())

    def test_synthetic_rejects_path_escape_links_and_invalid_budgets(self):
        with tempfile.TemporaryDirectory() as tmp:
            writer = BudgetWriter(Path(tmp), limit_bytes=200)
            for name in ("../outside", "/tmp/outside", "sub/file", "..", ""):
                with self.subTest(name=name), self.assertRaises(SupervisorError):
                    writer.write_text(name, "synthetic")
            (Path(tmp) / "link").symlink_to(Path(tmp) / "absent")
            with self.assertRaises(SupervisorError):
                writer.write_text("link", "synthetic")
            with self.assertRaises(SupervisorError):
                directory_bytes(Path(tmp))
        for total, reserve in ((0, 0), (100, 100), (True, 0), (100, -1)):
            with self.subTest(total=total, reserve=reserve), self.assertRaises(SupervisorError):
                BudgetWriter(Path("unused"), limit_bytes=total, reserve_bytes=reserve)


class SupervisorTests(unittest.TestCase):
    def run_toy(self, source, *, limits=None, rss_reader=None):
        with tempfile.TemporaryDirectory() as tmp:
            result = supervise([sys.executable, "-c", source], cwd=Path(tmp), output_dir=Path(tmp),
                               limits=limits or Limits(wall_seconds=3, poll_seconds=.02),
                               rss_reader=rss_reader)
            text = (Path(tmp) / "worker.log").read_text() if (Path(tmp) / "worker.log").exists() else ""
            return result, text

    def test_synthetic_success_and_nonzero_failure_preserved(self):
        success, text = self.run_toy("print('SYNTHETIC success')")
        self.assertEqual((success["status"], success["returncode"], success["attempts"]), ("completed", 0, 1))
        self.assertIn("SYNTHETIC success", text)
        failed, text = self.run_toy("import sys; print('SYNTHETIC failure'); sys.exit(7)")
        self.assertEqual((failed["status"], failed["reason"], failed["returncode"]), ("failed", "worker_nonzero_exit", 7))
        self.assertIn("SYNTHETIC failure", text)

    def test_synthetic_wall_timeout_terminates_without_retry(self):
        result, _ = self.run_toy("import time; time.sleep(30)",
                                limits=Limits(wall_seconds=.15, poll_seconds=.02))
        self.assertEqual((result["status"], result["reason"], result["attempts"]), ("failed", "wall_timeout", 1))
        self.assertLess(result["wall_seconds"], 2)
        self.assertLess(result["returncode"], 0)

    def test_synthetic_watchdog_kills_worker_while_monitor_is_delayed(self):
        def delayed_reader(pid):
            time.sleep(.3)
            return 100
        result, _ = self.run_toy("import time; time.sleep(30)", rss_reader=delayed_reader,
                                limits=Limits(wall_seconds=.1, poll_seconds=.02))
        self.assertEqual(result["reason"], "wall_timeout")
        self.assertLess(result["returncode"], 0)
        self.assertLess(result["wall_seconds"], 1)

    def test_synthetic_rss_limit_and_monitor_failure(self):
        result, _ = self.run_toy("import time; time.sleep(30)", rss_reader=lambda pid: 1001,
                                limits=Limits(wall_seconds=2, rss_bytes=1000, poll_seconds=.02))
        self.assertEqual(result["reason"], "rss_limit_exceeded")
        self.assertEqual(result["sampled_peak_rss_bytes"], 1001)
        result, _ = self.run_toy("import time; time.sleep(30)", rss_reader=lambda pid: -1)
        self.assertTrue(result["reason"].startswith("supervision_failure:"))
        self.assertEqual(result["status"], "failed")

    def test_synthetic_missed_rss_poll_deadline_is_recorded_and_stops(self):
        def slow_reader(pid):
            time.sleep(1.05)
            return 100
        result, _ = self.run_toy("import time; time.sleep(30)", rss_reader=slow_reader,
                                limits=Limits(wall_seconds=3, poll_seconds=.02))
        self.assertEqual(result["reason"], "rss_monitor_interval_exceeded")
        self.assertGreater(result["maximum_rss_poll_start_gap_seconds"], 1)

    def test_synthetic_log_cap_and_uncooperative_file_cap(self):
        result, text = self.run_toy("print('x' * 10000)",
                                   limits=Limits(wall_seconds=3, output_bytes=4096, poll_seconds=.02))
        self.assertEqual(result["reason"], "worker_log_budget_exceeded")
        self.assertLessEqual(len(text.encode()), 512)
        self.assertLessEqual(result["output_bytes"], 4096)
        result, _ = self.run_toy("from pathlib import Path; Path('too-big').write_bytes(b'x'*5000)",
                                limits=Limits(wall_seconds=3, output_bytes=4096, poll_seconds=.02))
        self.assertEqual(result["reason"], "output_budget_exceeded")
        # Detection of arbitrary direct writes is not prevention. Real worker
        # artifacts must use the separately tested prewrite BudgetWriter.
        self.assertGreater(result["output_bytes"], 4096)

    def test_synthetic_no_retry_into_existing_log(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "worker.log").write_text("old attempt")
            with self.assertRaises(SupervisorError):
                supervise([sys.executable, "-c", "pass"], cwd=Path(tmp), output_dir=Path(tmp))

    def test_synthetic_limits_validate(self):
        for kwargs in ({"poll_seconds": 1.1}, {"wall_seconds": 0}, {"wall_seconds": float("nan")},
                       {"cpu_seconds": True}, {"rss_bytes": -1}, {"output_bytes": 1}):
            with self.subTest(kwargs=kwargs), self.assertRaises(SupervisorError):
                Limits(**kwargs)

    def test_synthetic_cpu_limit_helper_changes_worker_only(self):
        src = Path(__file__).resolve().parents[1] / "src"
        source = ("import json,resource; from mfg_twin.supervisor import Limits,install_worker_limits; "
                  "x=install_worker_limits(Limits(cpu_seconds=2)); "
                  "x['actual']=resource.getrlimit(resource.RLIMIT_CPU); print(json.dumps(x))")
        with tempfile.TemporaryDirectory() as tmp:
            result = supervise([sys.executable, "-c", source], cwd=Path(tmp), output_dir=Path(tmp),
                               limits=Limits(wall_seconds=3, poll_seconds=.02),
                               env={"PYTHONPATH": str(src)})
            self.assertEqual(result["status"], "completed")
            recorded = json.loads((Path(tmp) / "worker.log").read_text())
            self.assertEqual(recorded["actual"], [2, 2])
            self.assertNotEqual(recorded["pid"], os.getpid())

    def test_synthetic_cpu_exhaustion_stops_worker_before_wall_deadline(self):
        src = Path(__file__).resolve().parents[1] / "src"
        source = (
            "from mfg_twin.supervisor import Limits, install_worker_limits\n"
            "install_worker_limits(Limits(cpu_seconds=1))\n"
            "print('SYNTHETIC CPU limit installed', flush=True)\n"
            "while True:\n"
            "    pass\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            result = supervise([sys.executable, "-c", source], cwd=Path(tmp), output_dir=Path(tmp),
                               limits=Limits(wall_seconds=5, cpu_seconds=1, poll_seconds=.02),
                               env={"PYTHONPATH": str(src)})
            self.assertIn("SYNTHETIC CPU limit installed", (Path(tmp) / "worker.log").read_text())
            self.assertEqual(result["status"], "failed")
            self.assertIn(result["reason"], ("cpu_limit_exceeded", "worker_nonzero_exit"))
            self.assertLess(result["returncode"], 0)
            self.assertLess(result["wall_seconds"], 5)
            self.assertEqual(result["attempts"], 1)

    def test_synthetic_ps_units_and_worker_usage(self):
        fake = subprocess.CompletedProcess([], 0, stdout="123\n", stderr="")
        with patch("mfg_twin.supervisor.subprocess.run", return_value=fake):
            self.assertEqual(read_rss_bytes(1234), 123 * 1024)
        fake = subprocess.CompletedProcess([], 1, stdout="", stderr="")
        with patch("mfg_twin.supervisor.subprocess.run", return_value=fake):
            self.assertIsNone(read_rss_bytes(1234))
        actual = worker_usage()
        self.assertGreater(actual["peak_rss_bytes"], 0)
        self.assertGreaterEqual(actual["process_cpu_seconds"], 0)
        self.assertEqual(actual["ru_maxrss_native_unit"], "bytes" if sys.platform == "darwin" else "KiB")


if __name__ == "__main__":
    unittest.main()
