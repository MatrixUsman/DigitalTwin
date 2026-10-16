"""Small causal coordinator, tested with synthetic spies rather than models.

No fit/calibration API and no dataset paths are passed into the detector. Final
campaign authorization, artifact freezing and output release are not implemented.
"""
from __future__ import annotations

import math
from typing import Iterable, Iterator, Protocol

from .data import EvaluatorRecord, Observation
from .metrics import ScoredPoint


class ReplayError(ValueError):
    """Invalid sequence or detector output; do not silently trim the row."""


class Detector(Protocol):
    def reset(self) -> None: ...
    def score(self, observation: Observation) -> float: ...
    def update(self, observation: Observation) -> None: ...


def score_stream(records: Iterable[EvaluatorRecord], detector: Detector) -> Iterator[ScoredPoint]:
    """Score each eligible observation before state correction, then align labels.

    Warmup observations update state without an output score. Invalid features
    stay unknown; the next valid observation must explicitly reset the stream.
    A score function may inspect current features to compute a residual, but its
    predictor must use past state. This coordinator cannot inspect model internals
    or prove a future detector is causal; every model still needs its own tests.
    """
    previous_row = None
    previous_segment = None
    needs_reset = True
    for record in records:
        if previous_row is not None and record.row != previous_row + 1:
            raise ReplayError("Missing, duplicate or reordered input row")
        previous_row = record.row
        if record.timestamp is None or not record.timestamp.is_finite():
            raise ReplayError("A native timestamp is required")
        observation = record.observation
        score = None
        if observation is None:
            if record.eligible:
                raise ReplayError("Eligible row has no observation")
            needs_reset = True
        else:
            if observation.dt is None:
                detector.reset()
                needs_reset = False
            elif needs_reset or record.segment != previous_segment:
                raise ReplayError("Stream start/break lacks explicit state reset")
            if record.eligible:
                value = detector.score(observation)
                if type(value) not in (int, float):
                    raise ReplayError("Detector score must be a finite number")
                try:
                    score = float(value)
                except OverflowError as error:
                    raise ReplayError("Detector score overflow") from error
                if not math.isfinite(score):
                    raise ReplayError("Detector score is nonfinite")
            detector.update(observation)
        previous_segment = record.segment
        yield ScoredPoint(record.row, record.timestamp, record.label, record.eligible, score, record.segment)
