"""Read-only CASPER right-arm parsing and causal windows.

This low-level module is not an access-control boundary. Production callers must
use the project admission wrapper, check the declared dataset identity and drain
the iterator to verify partition length. No benchmark file is read at import.
Labels and native coordinates belong only to ``EvaluatorRecord``; a detector
receives ``Observation`` objects, including warmup observations, and resets its
dynamic state whenever ``dt is None``. Score-before-update is the caller's duty.
"""

from __future__ import annotations

import csv
import json
import math
import os
from collections import deque
from contextlib import nullcontext
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, localcontext
from typing import Iterable, Iterator, TextIO


CASPER_HEADER = (
    "Timestamp", "Actual Joint Positions", "Actual Joint Velocities",
    "Actual Joint Currents", "Actual Cartesian Coordinates", "Actual Tool Speed",
    "Generalized Forces", "Temperature of Each Joint", "Execution Time",
    "Safety Status", "Tool Acceleration", "Norm of Cartesion Linear Momentum",
    "Robot Current", "Joint Voltages", "Elbow Position", "Elbow Velocity",
    "Tool Current", "Tool Temperature", "TCP Force", "Anomaly State",
)


class DataContractError(ValueError):
    """Malformed structure, annotation, or incomplete requested partition."""


@dataclass(frozen=True, slots=True)
class PartitionSpec:
    """A zero-based, half-open data-row range, excluding the CSV header."""

    name: str
    start: int
    end: int
    warmup: int = 1528
    gap_seconds: Decimal = Decimal("0.075")

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name:
            raise ValueError("partition name must be nonempty")
        if any(type(value) is not int for value in (self.start, self.end, self.warmup)):
            raise TypeError("partition bounds and warmup must be integers")
        if self.start < 0 or self.end <= self.start or self.warmup < 0:
            raise ValueError("require 0 <= start < end and warmup >= 0")
        if not isinstance(self.gap_seconds, Decimal):
            raise TypeError("gap_seconds must be Decimal")
        if not self.gap_seconds.is_finite() or self.gap_seconds <= 0:
            raise ValueError("gap_seconds must be finite and positive")

    @property
    def expected_rows(self) -> int:
        return self.end - self.start


@dataclass(frozen=True, slots=True)
class Observation:
    """Detector-only features: six q, six qdot, and relative native seconds."""

    q: tuple[float, ...]
    qdot: tuple[float, ...]
    dt: Decimal | None

    def __post_init__(self) -> None:
        for values in (self.q, self.qdot):
            if not isinstance(values, tuple) or len(values) != 6:
                raise ValueError("joint vectors must be tuples of six finite numbers")
            if any(type(value) not in (int, float) or not math.isfinite(value) for value in values):
                raise ValueError("joint vectors must contain six finite numbers")
        if self.dt is not None:
            if not isinstance(self.dt, Decimal) or not self.dt.is_finite() or self.dt <= 0:
                raise ValueError("relative time must be a finite positive Decimal or None")


@dataclass(frozen=True, slots=True)
class EvaluatorRecord:
    """Alignment/annotation metadata; never pass this object to a detector."""

    row: int
    timestamp: Decimal | None
    label: int
    observation: Observation | None
    eligible: bool
    segment: int | None
    exclusion: str | None


def _joint_vector(text: str) -> tuple[float, ...]:
    value = json.loads(text)
    if not isinstance(value, list) or len(value) != 6:
        raise ValueError("expected six-element JSON numeric vector")
    if any(type(element) not in (int, float) for element in value):
        raise ValueError("vector elements must be JSON numbers")
    result = tuple(float(element) for element in value)
    if not all(math.isfinite(element) for element in result):
        raise ValueError("vector contains nonfinite numbers")
    return result


def _native_delta(current: Decimal, previous: Decimal) -> Decimal:
    # Avoid the ambient Decimal precision rounding the provider's native strings.
    digits = max(len(current.as_tuple().digits), len(previous.as_tuple().digits))
    exponent_span = abs(current.as_tuple().exponent - previous.as_tuple().exponent)
    with localcontext() as context:
        context.prec = max(28, digits + exponent_span + 2)
        return current - previous


def iter_csv_partition(
    source: str | os.PathLike[str] | TextIO, spec: PartitionSpec,
) -> Iterator[EvaluatorRecord]:
    """Yield exactly ``end-start`` records when fully consumed, or raise.

    Open paths read-only. A caller-owned text stream must be positioned at the
    header and is not closed. Prior rows are CSV-tokenized to reach ``start`` but
    their labels/features/timestamps are not interpreted or retained. The reader
    never requests a CSV record at or beyond ``end``. Ordinary file buffering may
    read ahead in bytes, so this does not provide OS-level isolation.

    Header/width/label/timestamp errors fail closed. Invalid selected features
    produce an explicit unscored unknown and break continuity. The next valid row
    starts a fresh segment/warmup. Nonpositive or >gap time increments start a
    fresh segment at the current valid observation. Labels never reset state.
    """
    manager = (
        open(source, "r", encoding="utf-8", newline="")
        if isinstance(source, (str, os.PathLike)) else nullcontext(source)
    )
    with manager as handle:
        reader = csv.reader(handle, strict=True)
        try:
            header = next(reader)
        except StopIteration as error:
            raise DataContractError("missing CSV header") from error
        except csv.Error as error:
            raise DataContractError("malformed CSV header") from error
        if len(header) != len(set(header)):
            raise DataContractError("duplicate CSV header names")
        if tuple(header) != CASPER_HEADER:
            raise DataContractError("header does not match the original CASPER controller schema")

        previous_time: Decimal | None = None
        preceding = 0
        segment = -1
        for row_index in range(spec.end):
            try:
                values = next(reader)
            except StopIteration as error:
                observed = max(0, row_index - spec.start)
                raise DataContractError(
                    f"short partition {spec.name!r}: expected {spec.expected_rows} rows, observed {observed}"
                ) from error
            except csv.Error as error:
                raise DataContractError(f"malformed CSV at data row {row_index}") from error
            if len(values) != len(CASPER_HEADER):
                raise DataContractError(f"wrong CSV field count at data row {row_index}")
            if row_index < spec.start:
                continue
            if values[-1] not in ("0", "1"):
                raise DataContractError(f"label is not literal 0/1 at data row {row_index}")
            label = int(values[-1])

            timestamp: Decimal | None = None
            exclusion: str | None = None
            try:
                timestamp = Decimal(values[0])
                if not timestamp.is_finite():
                    raise ValueError("nonfinite timestamp")
            except (InvalidOperation, ValueError) as error:
                raise DataContractError(f"invalid timestamp at data row {row_index}") from error
            try:
                q = _joint_vector(values[1])
            except (ValueError, TypeError, OverflowError, RecursionError):
                exclusion = exclusion or "invalid_joint_positions"
            try:
                qdot = _joint_vector(values[2])
            except (ValueError, TypeError, OverflowError, RecursionError):
                exclusion = exclusion or "invalid_joint_velocities"
            if exclusion is not None:
                previous_time = None
                preceding = 0
                yield EvaluatorRecord(row_index, timestamp, label, None, False, None, exclusion)
                continue

            assert timestamp is not None
            dt = None if previous_time is None else _native_delta(timestamp, previous_time)
            if dt is None or dt <= 0 or dt > spec.gap_seconds:
                segment += 1
                preceding = 0
                dt = None
            observation = Observation(q=q, qdot=qdot, dt=dt)
            eligible = preceding >= spec.warmup
            yield EvaluatorRecord(
                row_index, timestamp, label, observation, eligible, segment,
                None if eligible else "warmup",
            )
            preceding += 1
            previous_time = timestamp


def causal_windows(
    records: Iterable[EvaluatorRecord], length: int,
) -> Iterator[tuple[Observation, ...]]:
    """Yield trailing feature-only windows at every eligible endpoint.

    Warmup observations build history. A window includes its current endpoint;
    one-step prediction must use only its preceding observations before scoring
    the current one. A requested history longer than the common warmup permits
    fails rather than silently dropping eligible endpoints. Coordinates remain
    in the caller's evaluator stream, never in the returned window.
    """
    if type(length) is not int or length <= 0:
        raise ValueError("window length must be a positive integer")
    history: deque[Observation] = deque(maxlen=length)
    previous_row: int | None = None
    previous_segment: int | None = None
    for record in records:
        observation = record.observation
        discontinuity = (
            previous_row is None or record.row != previous_row + 1
            or record.segment != previous_segment
            or observation is None or observation.dt is None
        )
        if discontinuity:
            history.clear()
        previous_row, previous_segment = record.row, record.segment
        if observation is None:
            if record.eligible:
                raise DataContractError("eligible record has no observation")
            continue
        history.append(observation)
        if record.eligible:
            if len(history) != length:
                raise DataContractError("requested window exceeds history at an eligible endpoint")
            yield tuple(history)
