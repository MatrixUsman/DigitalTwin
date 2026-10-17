"""Bound one cooperative local CPU worker; no retries or dataset access.

This is a resource supervisor, not a security sandbox. The worker must install
its CPU limit and use BudgetWriter for artifacts. RSS is sampled, so transient
peaks between samples are not an instantaneous enforced ceiling.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import math
import os
from pathlib import Path
import resource
import selectors
import signal
import subprocess
import sys
import threading
import time
from typing import Callable


class SupervisorError(ValueError):
    """Invalid settings, unavailable monitoring or an artifact budget violation."""


@dataclass(frozen=True)
class Limits:
    wall_seconds: float = 600
    cpu_seconds: int = 300
    rss_bytes: int = 1073741824
    output_bytes: int = 52428800
    poll_seconds: float = 0.25

    def __post_init__(self) -> None:
        for name in ("wall_seconds", "poll_seconds"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
                raise SupervisorError(f"invalid_{name}")
        if self.poll_seconds > 1:
            raise SupervisorError("poll_interval_exceeds_one_second")
        for name in ("cpu_seconds", "rss_bytes", "output_bytes"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                raise SupervisorError(f"invalid_{name}")
        if self.output_bytes < 16:
            raise SupervisorError("output_budget_too_small")

    @property
    def parent_reserve_bytes(self) -> int:
        return min(1048576, self.output_bytes // 4)


def directory_bytes(directory: Path) -> int:
    """Count actual regular artifact bytes; fail closed on links/special files."""
    directory = Path(directory)
    if directory.is_symlink() or not directory.is_dir():
        raise SupervisorError("invalid_output_directory")
    total = 0
    for root, dirs, files in os.walk(directory, followlinks=False):
        for name in dirs:
            if (Path(root) / name).is_symlink():
                raise SupervisorError("symlink_in_output_directory")
        for name in files:
            path = Path(root) / name
            if path.is_symlink() or not path.is_file():
                raise SupervisorError("nonregular_output_artifact")
            total += path.stat().st_size
    return total


class BudgetWriter:
    """Flat, non-overwriting artifact writer with aggregate pre/post checks.

    Worker usage: reserve the supervisor's metadata allocation. Parent final
    metadata may use reserve_bytes=0, remaining inside the same total limit.
    No arbitrary uncooperative writers or concurrent experiment are supported.
    """

    def __init__(self, output_dir: Path, *, limit_bytes: int,
                 reserve_bytes: int = 0) -> None:
        if (isinstance(limit_bytes, bool) or not isinstance(limit_bytes, int)
                or isinstance(reserve_bytes, bool) or not isinstance(reserve_bytes, int)
                or not 0 <= reserve_bytes < limit_bytes):
            raise SupervisorError("invalid_output_budget")
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.limit_bytes = limit_bytes
        self.reserve_bytes = reserve_bytes
        self.capacity = limit_bytes - reserve_bytes
        if self.bytes_used > self.capacity:
            raise SupervisorError("output_budget_already_exceeded")

    @property
    def bytes_used(self) -> int:
        return directory_bytes(self.output_dir)

    def _path(self, name: str) -> Path:
        if not isinstance(name, str) or not name or name in (".", "..") or Path(name).name != name or "\\" in name:
            raise SupervisorError("artifact_name_must_be_flat")
        path = self.output_dir / name
        if path.is_symlink():
            raise SupervisorError("symlink_output_artifact")
        return path

    def write_bytes(self, name: str, value: bytes, *, append: bool = False) -> Path:
        if not isinstance(value, bytes):
            raise SupervisorError("artifact_payload_must_be_bytes")
        path = self._path(name)
        if not append and path.exists():
            raise SupervisorError("artifact_already_exists")
        if self.bytes_used + len(value) > self.capacity:
            raise SupervisorError("output_budget_exceeded_before_write")
        with path.open("ab" if append else "xb") as stream:
            written = stream.write(value)
            if written != len(value):
                raise SupervisorError("incomplete_artifact_write")
        if self.bytes_used > self.capacity:
            raise SupervisorError("output_budget_exceeded_after_write")
        return path

    def write_text(self, name: str, value: str) -> Path:
        return self.write_bytes(name, value.encode("utf-8"))

    def append_text(self, name: str, value: str) -> Path:
        return self.write_bytes(name, value.encode("utf-8"), append=True)

    def write_json(self, name: str, value: object) -> Path:
        return self.write_text(name, json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n")


def install_worker_limits(limits: Limits) -> dict:
    """Call immediately inside the worker, never in the supervising process."""
    _, previous_hard = resource.getrlimit(resource.RLIMIT_CPU)
    effective = limits.cpu_seconds
    if previous_hard != resource.RLIM_INFINITY:
        effective = min(effective, previous_hard)
    if effective <= 0:
        raise SupervisorError("no_available_cpu_budget")
    resource.setrlimit(resource.RLIMIT_CPU, (effective, effective))
    return {"cpu_soft_seconds": effective, "cpu_hard_seconds": effective,
            "cpu_enforcement": "RLIMIT_CPU_in_worker", "pid": os.getpid()}


def worker_usage() -> dict:
    """Actual RUSAGE_SELF values; macOS ru_maxrss is bytes, Linux is KiB."""
    usage = resource.getrusage(resource.RUSAGE_SELF)
    if sys.platform == "darwin":
        multiplier, unit = 1, "bytes"
    elif sys.platform.startswith("linux"):
        multiplier, unit = 1024, "KiB"
    else:
        raise SupervisorError("unverified_ru_maxrss_platform")
    return {"user_cpu_seconds": usage.ru_utime, "system_cpu_seconds": usage.ru_stime,
            "process_cpu_seconds": usage.ru_utime + usage.ru_stime,
            "peak_rss_bytes": int(usage.ru_maxrss) * multiplier,
            "ru_maxrss_native_unit": unit, "source": "getrusage(RUSAGE_SELF)"}


def read_rss_bytes(pid: int) -> int | None:
    """Read one worker's RSS using ps; None means it exited before sampling.

    Local macOS ps(1), rss keyword: units are 1024 bytes. The local
    getrusage(2) page instead documents ru_maxrss in bytes. These two sources
    must not share an unqualified unit conversion.
    """
    if sys.platform != "darwin" and not sys.platform.startswith("linux"):
        raise SupervisorError("unverified_ps_platform")
    result = subprocess.run(["/bin/ps", "-o", "rss=", "-p", str(pid)],
                            stdin=subprocess.DEVNULL, capture_output=True,
                            text=True, timeout=0.25, check=False)
    value = result.stdout.strip()
    if not value and result.returncode == 1:
        return None
    if result.returncode != 0 or not value.isdecimal():
        raise SupervisorError("rss_monitor_failed")
    return int(value) * 1024


def _kill_group(process: subprocess.Popen) -> None:
    if process.poll() is not None:
        return
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    except PermissionError:
        # A watchdog may already have killed/reaped the same worker before the
        # polling thread reaches this call. Ignore denial only if termination
        # is independently confirmed; a live unkillable worker is an error.
        try:
            process.wait(timeout=.05)
        except subprocess.TimeoutExpired:
            raise


def supervise(command: list[str], *, cwd: Path, output_dir: Path,
              limits: Limits = Limits(), env: dict | None = None,
              rss_reader: Callable[[int], int | None] | None = None) -> dict:
    """Run once, cap captured output, sample RSS and terminate on limit breach.

    A zero exit code is only process success; the caller must validate required
    worker artifacts and scientific checks. Returned timing covers the worker
    launch through termination, not a claimed inference-only measurement.
    """
    if not command or not isinstance(command, list) or any(not isinstance(x, str) or not x for x in command):
        raise SupervisorError("invalid_command")
    cwd, output_dir = Path(cwd), Path(output_dir)
    if not cwd.is_dir():
        raise SupervisorError("invalid_working_directory")
    writer = BudgetWriter(output_dir, limit_bytes=limits.output_bytes)
    if (output_dir / "worker.log").exists():
        raise SupervisorError("worker_log_already_exists_no_retry")
    log_limit = limits.parent_reserve_bytes // 2
    log_bytes = 0
    worker_env = dict(os.environ)
    if env is not None:
        worker_env.update(env)
    for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
        worker_env[key] = "1"
    reader = rss_reader or read_rss_bytes
    start = time.monotonic()
    process = subprocess.Popen(command, cwd=cwd, env=worker_env, stdin=subprocess.DEVNULL,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               start_new_session=True, bufsize=0)
    reason = None
    peak_rss = None
    sample_count = 0
    max_sample_gap = 0.0
    previous_sample_started = start
    selector = selectors.DefaultSelector()
    os.set_blocking(process.stdout.fileno(), False)
    selector.register(process.stdout, selectors.EVENT_READ)
    next_sample = start
    timed_out = threading.Event()

    def deadline_stop() -> None:
        if process.poll() is None:
            timed_out.set()
            _kill_group(process)

    watchdog = threading.Timer(max(0, limits.wall_seconds - (time.monotonic() - start)), deadline_stop)
    watchdog.daemon = True
    watchdog.start()

    def capture() -> None:
        nonlocal log_bytes, reason
        while True:
            try:
                block = os.read(process.stdout.fileno(), 65536)
            except BlockingIOError:
                return
            if not block:
                return
            remaining = log_limit - log_bytes
            if remaining:
                portion = block[:remaining]
                writer.write_bytes("worker.log", portion, append=True)
                log_bytes += len(portion)
            if len(block) > remaining:
                reason = reason or "worker_log_budget_exceeded"
                return

    try:
        while process.poll() is None:
            now = time.monotonic()
            if now - start >= limits.wall_seconds:
                reason = "wall_timeout"
                break
            if now >= next_sample:
                sample_gap = now - previous_sample_started
                max_sample_gap = max(max_sample_gap, sample_gap)
                if sample_gap > 1:
                    reason = "rss_monitor_interval_exceeded"
                    break
                previous_sample_started = now
                rss = reader(process.pid)
                sample_count += 1
                if rss is not None:
                    if isinstance(rss, bool) or not isinstance(rss, int) or rss < 0:
                        raise SupervisorError("invalid_rss_measurement")
                    peak_rss = rss if peak_rss is None else max(peak_rss, rss)
                    if rss > limits.rss_bytes:
                        reason = "rss_limit_exceeded"
                        break
                elif process.poll() is None:
                    raise SupervisorError("rss_unavailable_for_live_worker")
                if writer.bytes_used > limits.output_bytes:
                    reason = "output_budget_exceeded"
                    break
                next_sample = now + limits.poll_seconds
            if reason:
                break
            remaining_wall = limits.wall_seconds - (time.monotonic() - start)
            if remaining_wall <= 0:
                reason = "wall_timeout"
                break
            selector.select(min(limits.poll_seconds, remaining_wall,
                                max(0, next_sample - time.monotonic())))
            capture()
            if reason:
                break
        if reason:
            _kill_group(process)
        process.wait(timeout=2)
        capture()
        if writer.bytes_used > limits.output_bytes:
            reason = reason or "output_budget_exceeded"
    except Exception as exc:
        reason = reason or f"supervision_failure:{type(exc).__name__}:{exc}"
        _kill_group(process)
        process.wait(timeout=2)
    finally:
        watchdog.cancel()
        selector.close()
        process.stdout.close()
        if process.poll() is None:
            _kill_group(process)
            process.wait(timeout=2)
    if timed_out.is_set():
        reason = "wall_timeout"
    if reason is None:
        if process.returncode == 0:
            reason = "completed"
        elif process.returncode == -signal.SIGXCPU:
            reason = "cpu_limit_exceeded"
        else:
            reason = "worker_nonzero_exit"
    try:
        output_bytes = writer.bytes_used
    except (OSError, SupervisorError):
        output_bytes = None
    return {"status": "completed" if reason == "completed" else "failed",
            "reason": reason, "returncode": process.returncode,
            "wall_seconds": time.monotonic() - start,
            "sampled_peak_rss_bytes": peak_rss, "rss_samples": sample_count,
            "maximum_rss_poll_start_gap_seconds": max_sample_gap,
            "rss_source": "injected_test_reader" if rss_reader else "/bin/ps rss (1024-byte units)",
            "rss_is_instantaneous_ceiling": False,
            "worker_log_bytes": log_bytes, "output_bytes": output_bytes,
            "limits": asdict(limits), "parent_reserve_bytes": limits.parent_reserve_bytes,
            "attempts": 1, "worker_usage": None,
            "worker_usage_note": "caller must attach worker getrusage receipt when available"}
