"""Label-free replay and delayed annotation I/O for the frozen campaign.

These are procedural interfaces, not OS isolation. CSV positioning tokenizes
earlier records; byte identity scans cover the entire source without parsing it.
Only the requested partition's permitted features are interpreted. The label
column is never indexed in the feature reader, including for validation.
"""
from __future__ import annotations

import csv
import io
import os
from dataclasses import dataclass
from decimal import Decimal

from .contract import ContractError, verify_source
from .data import CASPER_HEADER, Observation, _joint_vector, _native_delta


@dataclass(frozen=True, slots=True)
class FeatureRecord:
    row: int
    timestamp: Decimal
    observation: Observation
    eligible: bool
    segment: int


def csv_rows(text, spec, stats=None):
    """Position without interpreting skipped cells; never request row end."""
    reader = csv.reader(text, strict=True)
    if tuple(next(reader, ())) != CASPER_HEADER:
        raise ContractError("Campaign source header mismatch")
    for row in range(spec.end):
        values = next(reader, None)
        if values is None or len(values) != len(CASPER_HEADER):
            raise ContractError(f"Short or malformed campaign source at {row}")
        if stats is not None:
            stats.csv_records_traversed += 1
        if row >= spec.start:
            if stats is not None:
                stats.selected_rows_parsed += 1
            yield row, values


def feature_rows(text, spec, stats=None):
    previous, preceding, segment = None, 0, -1
    for row, values in csv_rows(text, spec, stats):
        timestamp = Decimal(values[0])
        if not timestamp.is_finite():
            raise ContractError("Nonfinite campaign timestamp")
        q, qdot = _joint_vector(values[1]), _joint_vector(values[2])
        dt = None if previous is None else _native_delta(timestamp, previous)
        if dt is None or dt <= 0 or dt > spec.gap_seconds:
            preceding, segment, dt = 0, segment + 1, None
        observation = Observation(q, qdot, dt)
        if stats is not None:
            stats.valid_observations += 1
        yield FeatureRecord(row, timestamp, observation, preceding >= spec.warmup, segment)
        previous, preceding = timestamp, preceding + 1


def verified_features(study, partition, stats):
    """Drain to check the exact mask and pre/post source identity. No labels."""
    if partition not in {"normal_calibration", "final_replay"}:
        raise ContractError("Campaign exposes only its declared calibration/final partitions")
    spec = study.partition(partition)
    path = (study.project_root / study.source_relative_path).resolve()
    if not path.is_relative_to(study.project_root.resolve()):
        raise ContractError("Source escapes project")
    expected = study.expected_eligible_rows(partition)
    next_row = next(expected, None)
    starts = {a - spec.warmup for name, intervals in study.eligible_intervals
              if name == partition for a, _ in intervals}
    with path.open("rb") as binary:
        before = os.fstat(binary.fileno())
        verify_source(binary, expected_bytes=study.source_bytes, expected_sha256=study.source_sha256, stats=stats)
        text = io.TextIOWrapper(binary, encoding="utf-8-sig", newline="")
        try:
            for record in feature_rows(text, spec, stats):
                if (record.observation.dt is None) != (record.row in starts):
                    raise ContractError("Campaign reset disagrees with frozen mask")
                if record.eligible != (record.row == next_row):
                    raise ContractError("Campaign eligibility disagrees with frozen mask")
                if record.eligible:
                    next_row = next(expected, None)
                yield record
            if next_row is not None:
                raise ContractError("Incomplete campaign support")
            after = os.fstat(binary.fileno())
            if (before.st_ino, before.st_size, before.st_mtime_ns) != (after.st_ino, after.st_size, after.st_mtime_ns):
                raise ContractError("Campaign source changed during replay")
            text.detach()
            verify_source(binary, expected_bytes=study.source_bytes, expected_sha256=study.source_sha256, stats=stats)
            stats.stream_checks_completed = True
        finally:
            # detach may already have occurred; no generator may silently skip
            # the postcheck and still receive a successful terminal receipt.
            try:
                text.detach()
            except ValueError:
                pass


def delayed_labels(study, sealed_index, stats):
    """Evaluator-only join. Caller must verify the entire sealed campaign first.

    Parses timestamps and literal binary labels only; never joint features.
    Coordinates must match every raw final row, including unscored warmup.
    """
    spec = study.partition("final_replay")
    path = (study.project_root / study.source_relative_path).resolve()
    if not path.is_relative_to(study.project_root.resolve()):
        raise ContractError("Source escapes project")
    labels = bytearray()
    with path.open("rb") as binary:
        verify_source(binary, expected_bytes=study.source_bytes, expected_sha256=study.source_sha256, stats=stats)
        text = io.TextIOWrapper(binary, encoding="utf-8-sig", newline="")
        try:
            for (row, values), coordinate in zip(csv_rows(text, spec, stats), sealed_index, strict=True):
                if row != coordinate[0] or Decimal(values[0]) != coordinate[1]:
                    raise ContractError("Label/score coordinate mismatch")
                if values[-1] not in ("0", "1"):
                    raise ContractError("Invalid final literal label")
                labels.append(int(values[-1]))
            text.detach()
            verify_source(binary, expected_bytes=study.source_bytes, expected_sha256=study.source_sha256, stats=stats)
            stats.stream_checks_completed = True
        finally:
            try:
                text.detach()
            except ValueError:
                pass
    return labels
