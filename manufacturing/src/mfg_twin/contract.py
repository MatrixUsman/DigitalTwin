"""Bind development loading to the reviewed CASPER metadata.

This wrapper intentionally exposes only training/development. Calibration and
final execution need a future artifact-freeze runner. These interfaces prevent
accidental misuse, not access by someone who can directly open the public CSV.
"""
from __future__ import annotations

import hashlib
import io
import json
import os
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import BinaryIO, Iterator

from .data import EvaluatorRecord, PartitionSpec, iter_csv_partition

CONTRACT_PATH = "configs/casper_right_arm_contract_v0.1.json"
POLICY_PATH = "configs/casper_right_arm_evaluation_v0.1.json"
CONTRACT_SHA256 = "3e88c87761b16aa808af188b8419fa48c3ef938a68441c70d1ba05467a779a25"
POLICY_SHA256 = "f7cc91ce98701bfe02725e57684db6850ee15696f22de6507328abb9ba9041f0"


class ContractError(ValueError):
    """The received metadata/source does not match this supported contract."""


class ProtectedPartitionError(ContractError):
    """This milestone does not expose calibration or final observations."""


@dataclass(frozen=True, slots=True)
class Study:
    project_root: Path
    source_relative_path: str
    source_bytes: int
    source_sha256: str
    partitions: tuple[PartitionSpec, ...]
    eligible_intervals: tuple[tuple[str, tuple[tuple[int, int], ...]], ...]

    def partition(self, name: str) -> PartitionSpec:
        """Return an actual stream, not a reporting-only final slice."""
        for item in self.partitions:
            if item.name == name:
                return item
        raise ContractError(f"Unknown partition: {name!r}")

    def expected_eligible_rows(self, name: str) -> Iterator[int]:
        for key, intervals in self.eligible_intervals:
            if key == name:
                for start, end in intervals:
                    yield from range(start, end)
                return
        raise ContractError(f"Unknown eligibility population: {name!r}")


def _json_bound(path: Path, expected_sha256: str) -> dict:
    payload = path.read_bytes()
    if hashlib.sha256(payload).hexdigest() != expected_sha256:
        raise ContractError(f"Reviewed metadata hash mismatch: {path.name}")
    return json.loads(payload)


def load_study(project_root: str | Path) -> Study:
    """Read small immutable specifications only; never opens raw data."""
    root = Path(project_root).resolve()
    contract = _json_bound(root / CONTRACT_PATH, CONTRACT_SHA256)
    policy = _json_bound(root / POLICY_PATH, POLICY_SHA256)
    for ref in [policy["data_contract"], *policy["documentation"]]:
        path = (root / ref["path"]).resolve()
        if not path.is_relative_to(root):
            raise ContractError("Reference escapes manufacturing project")
        if hashlib.sha256(path.read_bytes()).hexdigest() != ref["sha256"]:
            raise ContractError(f"Referenced specification changed: {ref['path']}")
    if policy["dataset"] != contract["dataset"]:
        raise ContractError("Policy and data contract disagree")
    source = contract["dataset"]
    warmup = contract["stream_policy"]["common_warmup_preceding_observations"]
    gap = Decimal(contract["stream_policy"]["gap_threshold_seconds"])
    partitions = tuple(
        PartitionSpec(name, *population["rows_half_open"], warmup=warmup, gap_seconds=gap)
        for name, population in policy["populations"].items()
        if name not in {"held_out_normal", "mixed_final"}
    )
    eligible = tuple(
        (name, tuple(tuple(bounds) for bounds in population["expected_eligible_intervals_half_open"]))
        for name, population in policy["populations"].items()
    )
    return Study(root, source["source_file"], source["source_bytes"], source["source_sha256"], partitions, eligible)


def verify_source(stream: BinaryIO, *, expected_bytes: int, expected_sha256: str) -> None:
    """Hash a seekable binary stream, then rewind; does not parse observations."""
    stream.seek(0)
    digest = hashlib.sha256()
    count = 0
    for chunk in iter(lambda: stream.read(1024 * 1024), b""):
        count += len(chunk)
        digest.update(chunk)
    stream.seek(0)
    if count != expected_bytes or digest.hexdigest() != expected_sha256:
        raise ContractError("Source size or SHA-256 differs from the immutable receipt")


def iter_development_records(study: Study, partition: str, *, stop: int | None = None) -> Iterator[EvaluatorRecord]:
    """Read a training/development prefix from verified bytes.

    `stop` may cap the end for a declared bounded pilot. It cannot move the start,
    borrow history across a partition, or extend into calibration/final data.
    Exhaust the iterator before treating its source/mask checks as complete.
    A prefix is not the full frozen partition and must be recorded as such.
    """
    if partition not in {"training", "development"}:
        raise ProtectedPartitionError("Only training/development are exposed; calibration/final runner is not admitted")
    spec = study.partition(partition)
    end = spec.end if stop is None else stop
    if type(end) is not int or not spec.start < end <= spec.end:
        raise ContractError("Pilot stop must be inside the selected partition")
    bounded = PartitionSpec(spec.name, spec.start, end, warmup=spec.warmup, gap_seconds=spec.gap_seconds)
    source_path = (study.project_root / study.source_relative_path).resolve()
    if not source_path.is_relative_to(study.project_root.resolve()):
        raise ContractError("Source path escapes manufacturing project")
    expected = iter(row for row in study.expected_eligible_rows(partition) if row < end)
    next_eligible = next(expected, None)
    starts = {a - spec.warmup for key, intervals in study.eligible_intervals
              if key == partition for a, _ in intervals}
    with source_path.open("rb") as binary:
        before = os.fstat(binary.fileno())
        if before.st_size != study.source_bytes:
            raise ContractError("Source byte count mismatch")
        verify_source(binary, expected_bytes=study.source_bytes, expected_sha256=study.source_sha256)
        with io.TextIOWrapper(binary, encoding="utf-8-sig", newline="") as text:
            for record in iter_csv_partition(text, bounded):
                if record.observation is None:
                    raise ContractError(f"Unexpected invalid observation at row {record.row}")
                if (record.observation.dt is None) != (record.row in starts):
                    raise ContractError(f"Observed segment reset disagrees with frozen mask at row {record.row}")
                is_expected = record.row == next_eligible
                if record.eligible != is_expected:
                    raise ContractError(f"Observed support disagrees with frozen mask at row {record.row}")
                if is_expected:
                    next_eligible = next(expected, None)
                yield record
            if next_eligible is not None:
                raise ContractError("Source ended before expected support")
            after = os.fstat(binary.fileno())
            if (before.st_size, before.st_mtime_ns, before.st_ino) != (after.st_size, after.st_mtime_ns, after.st_ino):
                raise ContractError("Source metadata changed while loading")
