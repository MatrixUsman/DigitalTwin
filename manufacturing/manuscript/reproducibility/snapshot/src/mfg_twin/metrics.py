"""Pure metrics for the frozen CASPER comparison; no data or model I/O.

``evaluate`` is the admission boundary: callers supply the complete expected
row domain and its independently constructed structural eligibility mask.
All time arithmetic uses the supplied Decimal controller timestamps.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction
import math
from typing import Iterable, Mapping, Sequence


class MetricError(ValueError):
    """Invalid inputs or incomplete comparative admission, with safe diagnostics."""

    def __init__(self, reason: str, **details: object) -> None:
        self.reason = reason
        self.details = details
        super().__init__(f"{reason}: {details}" if details else reason)


@dataclass(frozen=True)
class ScoredPoint:
    row: int
    time: Decimal
    label: int
    eligible: bool
    score: float | None
    segment: int | None


@dataclass(frozen=True)
class Event:
    event_id: str
    start: int
    end: int


@dataclass(frozen=True)
class Calibration:
    count: int
    rank: int
    threshold: float
    exceedances: int


@dataclass(frozen=True)
class Coverage:
    raw_rows: int
    eligible_rows: int
    scored_rows: int
    excluded_rows: int
    raw_coverage: float | None
    eligible_coverage: float | None


@dataclass(frozen=True)
class PointMetrics:
    tp: int
    fp: int
    fn: int
    tn: int
    precision: float | None
    recall: float | None
    f1: float | None
    average_precision: float | None
    positive_rows: int
    negative_rows: int
    alarm_rows: int
    point_exceedance: float | None
    scheduled_zero_exceedance: float | None


@dataclass(frozen=True)
class Episode:
    episode_id: int
    start_row: int
    end_row_exclusive: int
    first_time: Decimal
    last_time: Decimal
    left_censored: bool
    right_censored: bool


@dataclass(frozen=True)
class SliceMetrics:
    name: str
    bounds: tuple[int, int]
    coverage: Coverage
    points: PointMetrics
    exposure_seconds: Decimal
    episode_ids: tuple[int, ...]
    episode_count: int
    left_censored_count: int
    right_censored_count: int
    crosses_start_count: int
    crosses_end_count: int
    episodes_per_hour: float | None


@dataclass(frozen=True)
class EventOutcome:
    event_id: str
    start: int
    end: int
    first_positive_time: Decimal
    eligible_rows: int
    scored_rows: int
    excluded_rows: int
    interval_overlap_hit: bool
    first_overlap_row: int | None
    first_overlap_time: Decimal | None
    overlap_delay_seconds: Decimal | None
    overlap_delay_reason: str | None
    pre_existing_alarm: bool | None
    first_fresh_onset_row: int | None
    first_fresh_onset_time: Decimal | None
    fresh_onset_delay_seconds: Decimal | None
    fresh_onset_delay_reason: str | None
    episode_ids: tuple[int, ...]


@dataclass(frozen=True)
class EventMetrics:
    outcomes: tuple[EventOutcome, ...]
    denominator: int
    overlap_hits: int
    overlap_recall: float | None
    fresh_onset_events: int
    fresh_onset_recall: float | None
    coverage_failure_events: int


@dataclass(frozen=True)
class EvaluationReport:
    expected_domain: tuple[int, int]
    threshold: float
    coverage: Coverage
    episodes: tuple[Episode, ...]
    slices: tuple[SliceMetrics, ...]
    events: EventMetrics


def _finite_number(value: object, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise MetricError("non_numeric_value", field=field, value_type=type(value).__name__)
    try:
        result = float(value)
    except (OverflowError, ValueError) as exc:
        raise MetricError("nonfinite_value", field=field) from exc
    if not math.isfinite(result):
        raise MetricError("nonfinite_value", field=field)
    return result


def _integer(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _bounds(value: object, field: str) -> tuple[int, int]:
    if not isinstance(value, (tuple, list)) or len(value) != 2:
        raise MetricError("invalid_range", field=field)
    start, end = value
    if not _integer(start) or not _integer(end) or start < 0 or end < start:
        raise MetricError("invalid_range", field=field)
    return start, end


def _ratio(numerator: int, denominator: int) -> float | None:
    return numerator / denominator if denominator else None


def _exact_decimal(value: Fraction) -> Decimal:
    """Convert a terminating rational without consulting the Decimal context.

    Differences/sums of finite Decimal timestamps terminate in base ten. Build
    the Decimal tuple directly so ambient precision, rounding and traps cannot
    round native exposure or schedule delay. No global context is changed.
    """
    denominator = value.denominator
    twos = fives = 0
    while denominator % 2 == 0:
        denominator //= 2
        twos += 1
    while denominator % 5 == 0:
        denominator //= 5
        fives += 1
    if denominator != 1:
        raise MetricError("nonterminating_native_time_fraction")
    scale = max(twos, fives)
    coefficient = abs(value.numerator) * 2 ** (scale - twos) * 5 ** (scale - fives)
    # Decimal(int) and Decimal(tuple) construction are exact, including under
    # low-precision contexts with Inexact/Rounded traps enabled.
    digits = Decimal(coefficient).as_tuple().digits
    return Decimal((int(value.numerator < 0), digits, -scale))


def calibrate(scores: Iterable[float], *, expected_m: int | None = None) -> Calibration:
    """Nearest-rank 99th percentile; strict greater-than is the alarm rule.

    The caller must already have verified row identity and the complete mask.
    ``expected_m`` additionally guards against an omitted calibration score.
    """
    values = [_finite_number(x, "calibration_score") for x in scores]
    if expected_m is not None:
        if not _integer(expected_m) or expected_m < 0:
            raise MetricError("invalid_expected_calibration_count")
        if len(values) != expected_m:
            raise MetricError("calibration_count_mismatch", expected=expected_m, observed=len(values))
    if not values:
        raise MetricError("empty_calibration")
    values.sort()
    rank = (99 * len(values) + 99) // 100
    threshold = values[rank - 1]
    return Calibration(len(values), rank, threshold, sum(x > threshold for x in values))


def average_precision(labels: Sequence[int], scores: Sequence[float]) -> float | None:
    """Noninterpolated binary AP, including entire equal-score groups together.

    This arithmetic primitive does not validate dataset identity. Use evaluate
    for a comparative report with domain/mask admission.
    """
    if len(labels) != len(scores):
        raise MetricError("label_score_length_mismatch")
    if any(not _integer(y) or y not in (0, 1) for y in labels):
        raise MetricError("invalid_binary_label")
    values = [_finite_number(x, "score") for x in scores]
    positives = sum(labels)
    if not positives:
        return None
    ranked = sorted(zip(values, labels), key=lambda pair: pair[0], reverse=True)
    cumulative_true = 0
    cumulative_count = 0
    terms = []
    index = 0
    while index < len(ranked):
        stop = index + 1
        while stop < len(ranked) and ranked[stop][0] == ranked[index][0]:
            stop += 1
        group_true = sum(label for _, label in ranked[index:stop])
        cumulative_true += group_true
        cumulative_count += stop - index
        terms.append((group_true / positives) * (cumulative_true / cumulative_count))
        index = stop
    return math.fsum(terms)


def _coverage(points: Sequence[ScoredPoint]) -> Coverage:
    eligible = sum(p.eligible for p in points)
    scored = sum(p.eligible and p.score is not None for p in points)
    return Coverage(len(points), eligible, scored, len(points) - eligible,
                    _ratio(scored, len(points)), _ratio(scored, eligible))


def _validate_points(
    points: tuple[ScoredPoint, ...],
    domain: tuple[int, int],
    expected_eligible_rows: Iterable[int],
) -> None:
    start, end = domain
    rows = list(expected_eligible_rows)
    if any(not _integer(row) or not start <= row < end for row in rows):
        raise MetricError("invalid_expected_eligible_row")
    expected = set(rows)
    if len(expected) != len(rows):
        raise MetricError("duplicate_expected_eligible_row")
    if len(points) != end - start:
        raise MetricError("incomplete_domain", expected_rows=end - start, observed_rows=len(points))
    failures = []
    previous = None
    last_segment = None
    for expected_row, point in zip(range(start, end), points):
        if not isinstance(point, ScoredPoint):
            raise MetricError("invalid_point_type", row=expected_row)
        if not _integer(point.row) or point.row != expected_row:
            raise MetricError("row_alignment_mismatch", expected=expected_row, observed=point.row)
        if not isinstance(point.time, Decimal) or not point.time.is_finite():
            raise MetricError("invalid_timestamp", row=point.row)
        if not _integer(point.label) or point.label not in (0, 1):
            raise MetricError("invalid_binary_label", row=point.row)
        if not isinstance(point.eligible, bool) or point.eligible != (point.row in expected):
            raise MetricError("eligibility_mask_mismatch", row=point.row)
        if point.segment is None:
            if point.eligible:
                raise MetricError("eligible_point_without_segment", row=point.row)
        elif not _integer(point.segment) or point.segment < 0:
            raise MetricError("invalid_segment", row=point.row)
        elif last_segment is not None and point.segment < last_segment:
            raise MetricError("segment_reuse_or_reordering", row=point.row)
        if previous is not None:
            if (point.segment is not None and point.segment == previous.segment
                    and point.time <= previous.time):
                raise MetricError("nonincreasing_segment_time", row=point.row)
        if point.segment is not None:
            last_segment = point.segment
        if point.eligible:
            if point.score is None:
                failures.append((point.row, "missing_score"))
            else:
                try:
                    _finite_number(point.score, "score")
                except MetricError as exc:
                    failures.append((point.row, exc.reason))
        elif point.score is not None:
            raise MetricError("score_outside_eligible_support", row=point.row)
        previous = point
    if failures:
        raise MetricError("incomplete_score_coverage", expected_eligible_rows=len(expected),
                          finite_scored_rows=len(expected) - len(failures),
                          failures=tuple(failures))


def _decision(point: ScoredPoint, threshold: float) -> bool | None:
    return float(point.score) > threshold if point.eligible and point.score is not None else None


def _point_metrics(points: Sequence[ScoredPoint], threshold: float) -> PointMetrics:
    selected = [p for p in points if p.eligible]
    tp = fp = fn = tn = 0
    for point in selected:
        alarm = _decision(point, threshold)
        if point.label:
            if alarm:
                tp += 1
            else:
                fn += 1
        elif alarm:
            fp += 1
        else:
            tn += 1
    ap = average_precision([p.label for p in selected], [p.score for p in selected])
    return PointMetrics(tp, fp, fn, tn, _ratio(tp, tp + fp), _ratio(tp, tp + fn),
                        _ratio(2 * tp, 2 * tp + fp + fn), ap, tp + fn, fp + tn,
                        tp + fp, _ratio(tp + fp, len(selected)), _ratio(fp, fp + tn))


def _episodes(points: Sequence[ScoredPoint], threshold: float) -> tuple[Episode, ...]:
    output = []
    start = None
    left_censored = False
    for index, point in enumerate(points):
        previous = points[index - 1] if index else None
        continuous = (previous is not None and point.segment is not None
                      and point.segment == previous.segment)
        decision = _decision(point, threshold)
        if start is not None and (decision is not True or not continuous):
            first, last = points[start], points[index - 1]
            output.append(Episode(len(output) + 1, first.row, last.row + 1,
                                  first.time, last.time, left_censored,
                                  not (continuous and decision is False)))
            start = None
        if decision is True and start is None:
            start = index
            left_censored = not (continuous and _decision(previous, threshold) is not None)
    if start is not None:
        first, last = points[start], points[-1]
        output.append(Episode(len(output) + 1, first.row, last.row + 1,
                              first.time, last.time, left_censored, True))
    return tuple(output)


def _slice_metrics(name: str, bounds: tuple[int, int], all_points: tuple[ScoredPoint, ...],
                   domain: tuple[int, int], threshold: float,
                   episodes: tuple[Episode, ...]) -> SliceMetrics:
    start, end = bounds
    selected = all_points[start - domain[0]:end - domain[0]]
    exposure_fraction = sum((Fraction(right.time) - Fraction(left.time)
                    for left, right in zip(selected, selected[1:])
                    if left.eligible and right.eligible and left.segment == right.segment),
                   Fraction(0))
    exposure = _exact_decimal(exposure_fraction)
    overlapping = [e for e in episodes if max(start, e.start_row) < min(end, e.end_row_exclusive)]
    rate = None
    if exposure_fraction:
        try:
            rate = float(Fraction(len(overlapping) * 3600) / exposure_fraction)
        except OverflowError as exc:
            raise MetricError("episode_rate_not_representable") from exc
    return SliceMetrics(name, bounds, _coverage(selected), _point_metrics(selected, threshold),
                        exposure, tuple(e.episode_id for e in overlapping), len(overlapping),
                        sum(e.left_censored for e in overlapping),
                        sum(e.right_censored for e in overlapping),
                        sum(e.start_row < start for e in overlapping),
                        sum(e.end_row_exclusive > end for e in overlapping), rate)


def _validate_events(events: tuple[Event, ...], points: tuple[ScoredPoint, ...],
                     domain: tuple[int, int]) -> None:
    declared = []
    ids = set()
    for event in events:
        if not isinstance(event, Event) or not isinstance(event.event_id, str) or not event.event_id:
            raise MetricError("invalid_event")
        if event.event_id in ids:
            raise MetricError("duplicate_event_id", event_id=event.event_id)
        ids.add(event.event_id)
        start, end = _bounds((event.start, event.end), "event")
        if start == end or start < domain[0] or end > domain[1]:
            raise MetricError("event_outside_domain", event_id=event.event_id)
        declared.append((start, end))
    observed = []
    start = None
    for point in points:
        if point.label and start is None:
            start = point.row
        if not point.label and start is not None:
            observed.append((start, point.row))
            start = None
    if start is not None:
        observed.append((start, domain[1]))
    if declared != observed:
        raise MetricError("event_annotation_mismatch", declared=tuple(declared), observed=tuple(observed))


def _delay(points: tuple[ScoredPoint, ...], start_index: int,
           target_index: int | None, absent_reason: str) -> tuple[Decimal | None, str | None]:
    if target_index is None:
        return None, absent_reason
    for index in range(start_index + 1, target_index + 1):
        if points[index].time <= points[index - 1].time:
            return None, "clock_discontinuity"
    return _exact_decimal(Fraction(points[target_index].time) - Fraction(points[start_index].time)), None


def _event_metrics(events: tuple[Event, ...], points: tuple[ScoredPoint, ...],
                   domain: tuple[int, int], threshold: float,
                   episodes: tuple[Episode, ...]) -> EventMetrics:
    outcomes = []
    for event in events:
        start_index, end_index = event.start - domain[0], event.end - domain[0]
        selected = points[start_index:end_index]
        overlap = fresh = None
        for index in range(start_index, end_index):
            point = points[index]
            if _decision(point, threshold) is True:
                if overlap is None:
                    overlap = index
                if (fresh is None and index > 0 and points[index - 1].segment == point.segment
                        and _decision(points[index - 1], threshold) is False):
                    fresh = index
        first = points[start_index]
        previous = points[start_index - 1] if start_index else None
        pre_existing = None
        if (previous is not None and previous.segment == first.segment
                and _decision(previous, threshold) is not None
                and _decision(first, threshold) is not None):
            pre_existing = _decision(previous, threshold) is True and _decision(first, threshold) is True
        overlap_delay, overlap_reason = _delay(points, start_index, overlap, "no_overlap_alarm")
        fresh_delay, fresh_reason = _delay(points, start_index, fresh, "no_new_onset")
        coverage = _coverage(selected)
        ids = tuple(e.episode_id for e in episodes
                    if max(event.start, e.start_row) < min(event.end, e.end_row_exclusive))
        outcomes.append(EventOutcome(event.event_id, event.start, event.end, first.time,
                                     coverage.eligible_rows, coverage.scored_rows, coverage.excluded_rows,
                                     overlap is not None,
                                     points[overlap].row if overlap is not None else None,
                                     points[overlap].time if overlap is not None else None,
                                     overlap_delay, overlap_reason, pre_existing,
                                     points[fresh].row if fresh is not None else None,
                                     points[fresh].time if fresh is not None else None,
                                     fresh_delay, fresh_reason, ids))
    hits = sum(e.interval_overlap_hit for e in outcomes)
    fresh = sum(e.first_fresh_onset_row is not None for e in outcomes)
    return EventMetrics(tuple(outcomes), len(events), hits, _ratio(hits, len(events)),
                        fresh, _ratio(fresh, len(events)),
                        sum(e.eligible_rows == 0 for e in outcomes))


def evaluate(
    points: Iterable[ScoredPoint],
    *,
    expected_domain: tuple[int, int],
    expected_eligible_rows: Iterable[int],
    threshold: float,
    reporting_ranges: Mapping[str, tuple[int, int]],
    events: Sequence[Event],
) -> EvaluationReport:
    """Validate complete support, then compute explicitly scoped metrics.

    All recorded positive runs in the domain must be declared, in order, as
    events. Timestamp deltas must be positive within each segment. The loader
    owns the gap threshold and warmup policy; this generic arithmetic layer
    respects its explicit mask/segments rather than guessing a sampling rate.
    A structural unknown may have segment=None only when it is ineligible.
    Numeric scores/thresholds are interpreted as finite Python binary64 floats.
    Labels never alter the global episode stream. No files are read/written.
    """
    domain = _bounds(expected_domain, "expected_domain")
    tau = _finite_number(threshold, "threshold")
    records = tuple(points)
    _validate_points(records, domain, expected_eligible_rows)
    event_tuple = tuple(events)
    _validate_events(event_tuple, records, domain)
    ranges = []
    for name, value in reporting_ranges.items():
        if not isinstance(name, str) or not name:
            raise MetricError("invalid_reporting_name")
        bounds = _bounds(value, f"reporting_range:{name}")
        if bounds[0] < domain[0] or bounds[1] > domain[1]:
            raise MetricError("reporting_range_outside_domain", name=name)
        ranges.append((name, bounds))
    if not ranges:
        raise MetricError("no_reporting_ranges")
    episodes = _episodes(records, tau)
    slices = tuple(_slice_metrics(name, bounds, records, domain, tau, episodes)
                   for name, bounds in ranges)
    return EvaluationReport(domain, tau, _coverage(records), episodes, slices,
                            _event_metrics(event_tuple, records, domain, tau, episodes))
