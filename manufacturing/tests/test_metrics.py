"""SYNTHETIC metric acceptance fixtures: no CASPER data, network or training."""

from dataclasses import FrozenInstanceError, replace
from decimal import Decimal, Inexact, ROUND_DOWN, ROUND_UP, Rounded, getcontext, localcontext
import math
import unittest

from mfg_twin.metrics import Event, MetricError, ScoredPoint, average_precision, calibrate, evaluate


def synthetic_points(labels, scores, *, eligible=None, times=None, segments=None, start=0):
    n = len(labels)
    if eligible is None:
        eligible = [True] * n
    if times is None:
        times = [Decimal(i) * Decimal("0.05") for i in range(n)]
    if segments is None:
        segments = [0] * n
    return [ScoredPoint(start + i, times[i], labels[i], eligible[i], scores[i], segments[i])
            for i in range(n)]


def synthetic_events(labels, start=0):
    result = []
    begin = None
    for index, label in enumerate(labels):
        if label and begin is None:
            begin = start + index
        if not label and begin is not None:
            result.append(Event(f"synthetic-{len(result) + 1}", begin, start + index))
            begin = None
    if begin is not None:
        result.append(Event(f"synthetic-{len(result) + 1}", begin, start + len(labels)))
    return result


def synthetic_report(points, *, threshold=0.5, ranges=None, events=None):
    start = points[0].row if points else 0
    end = start + len(points)
    if ranges is None:
        ranges = {"synthetic": (start, end)}
    if events is None:
        events = synthetic_events([p.label for p in points], start)
    return evaluate(points, expected_domain=(start, end),
                    expected_eligible_rows=[p.row for p in points if p.eligible],
                    threshold=threshold, reporting_ranges=ranges, events=events)


class CalibrationTests(unittest.TestCase):
    def test_synthetic_small_sample_and_strict_equality(self):
        result = calibrate([1, 1, 2, 3], expected_m=4)
        self.assertEqual((result.count, result.rank, result.threshold, result.exceedances), (4, 4, 3, 0))
        report = synthetic_report(synthetic_points([0, 1], [3, 4]), threshold=result.threshold)
        self.assertEqual((report.slices[0].points.tn, report.slices[0].points.tp), (1, 1))

    def test_synthetic_interior_rank(self):
        result = calibrate(range(1, 101), expected_m=100)
        self.assertEqual((result.rank, result.threshold, result.exceedances), (99, 99, 1))

    def test_synthetic_contract_sized_count_arithmetic(self):
        result = calibrate([0.0] * 160473, expected_m=160473)
        self.assertEqual((result.rank, result.threshold, result.exceedances), (158869, 0, 0))

    def test_synthetic_rejects_empty_missing_count_and_invalid_expected_count(self):
        for values, count in [([], None), ([1], 2), ([1], True), ([1], -1)]:
            with self.subTest(values=values, count=count), self.assertRaises(MetricError):
                calibrate(values, expected_m=count)

    def test_synthetic_rejects_nonfinite_boolean_and_nonnumeric(self):
        for value in [None, True, "1", math.nan, math.inf, -math.inf]:
            with self.subTest(value=value), self.assertRaises(MetricError):
                calibrate([0, value])


class PointMetricTests(unittest.TestCase):
    def test_synthetic_confusion_counts(self):
        metric = synthetic_report(synthetic_points([1, 0, 1, 0], [1, 1, 0, 0])).slices[0].points
        self.assertEqual((metric.tp, metric.fp, metric.fn, metric.tn), (1, 1, 1, 1))
        self.assertEqual((metric.precision, metric.recall, metric.f1), (0.5, 0.5, 0.5))
        self.assertEqual(metric.point_exceedance, 0.5)
        self.assertEqual(metric.scheduled_zero_exceedance, 0.5)

    def test_synthetic_no_alarms_positive_labels(self):
        metric = synthetic_report(synthetic_points([1, 0], [0, 0])).slices[0].points
        self.assertIsNone(metric.precision)
        self.assertEqual((metric.recall, metric.f1), (0, 0))

    def test_synthetic_no_positive_labels_one_alarm(self):
        metric = synthetic_report(synthetic_points([0, 0], [1, 0])).slices[0].points
        self.assertEqual((metric.precision, metric.f1), (0, 0))
        self.assertIsNone(metric.recall)
        self.assertIsNone(metric.average_precision)
        self.assertEqual(metric.point_exceedance, 0.5)

    def test_synthetic_no_positive_labels_no_alarms(self):
        metric = synthetic_report(synthetic_points([0, 0], [0, 0])).slices[0].points
        self.assertIsNone(metric.precision)
        self.assertIsNone(metric.recall)
        self.assertIsNone(metric.f1)
        self.assertIsNone(metric.average_precision)
        self.assertEqual(metric.point_exceedance, 0)

    def test_synthetic_ap_ties_and_permutation(self):
        self.assertAlmostEqual(average_precision([1, 0, 1], [0.9, 0.9, 0.2]), 7 / 12)
        self.assertAlmostEqual(average_precision([0, 1, 1], [0.9, 0.9, 0.2]), 7 / 12)
        self.assertEqual(average_precision([1, 0, 1, 0], [2, 2, 2, 2]), 0.5)

    def test_synthetic_ap_perfect_reverse_and_all_positive(self):
        self.assertEqual(average_precision([1, 0], [2, 1]), 1)
        self.assertEqual(average_precision([1, 0], [1, 2]), 0.5)
        self.assertEqual(average_precision([1, 1], [1, 2]), 1)
        self.assertIsNone(average_precision([], []))

    def test_synthetic_ap_rejects_invalid_inputs(self):
        for labels, scores in [([1], []), ([2], [1]), ([True], [1]), ([0], [math.nan])]:
            with self.subTest(labels=labels, scores=scores), self.assertRaises(MetricError):
                average_precision(labels, scores)

    def test_synthetic_separate_reporting_populations(self):
        points = synthetic_points([0, 0, 1, 0], [1, 0, 1, 0])
        normal, mixed = synthetic_report(points, ranges={"normal": (0, 2), "mixed": (2, 4)}).slices
        self.assertEqual((normal.points.fp, mixed.points.fp, mixed.points.tp), (1, 0, 1))
        self.assertEqual(mixed.points.precision, 1)
        self.assertEqual(normal.exposure_seconds, Decimal("0.05"))
        self.assertEqual(mixed.exposure_seconds, Decimal("0.05"))

    def test_synthetic_empty_and_fully_excluded_populations(self):
        empty = synthetic_report([])
        self.assertEqual(empty.coverage.raw_rows, 0)
        self.assertIsNone(empty.coverage.raw_coverage)
        self.assertIsNone(empty.events.overlap_recall)
        excluded = synthetic_report(synthetic_points([0, 0], [None, None], eligible=[False, False]))
        self.assertEqual(excluded.coverage.raw_coverage, 0)
        self.assertIsNone(excluded.coverage.eligible_coverage)
        self.assertIsNone(excluded.slices[0].points.f1)


class EpisodeEventTests(unittest.TestCase):
    def test_synthetic_preexisting_episode_is_not_fresh_onset(self):
        report = synthetic_report(synthetic_points([0, 0, 1, 1, 0], [0, 1, 1, 1, 0]))
        self.assertEqual(len(report.episodes), 1)
        self.assertFalse(report.episodes[0].left_censored)
        self.assertFalse(report.episodes[0].right_censored)
        event = report.events.outcomes[0]
        self.assertTrue(event.interval_overlap_hit)
        self.assertTrue(event.pre_existing_alarm)
        self.assertEqual(event.overlap_delay_seconds, Decimal(0))
        self.assertIsNone(event.first_fresh_onset_row)
        self.assertEqual(event.fresh_onset_delay_reason, "no_new_onset")
        self.assertEqual(report.slices[0].exposure_seconds, Decimal("0.20"))

    def test_synthetic_fresh_event_onset_and_miss(self):
        report = synthetic_report(synthetic_points([0, 1, 1, 0, 1, 0], [0, 0, 1, 0, 0, 0]))
        first, second = report.events.outcomes
        self.assertEqual((first.first_overlap_row, first.first_fresh_onset_row), (2, 2))
        self.assertEqual(first.fresh_onset_delay_seconds, Decimal("0.05"))
        self.assertFalse(first.pre_existing_alarm)
        self.assertFalse(second.interval_overlap_hit)
        self.assertEqual(second.overlap_delay_reason, "no_overlap_alarm")
        self.assertEqual((report.events.denominator, report.events.overlap_recall), (2, 0.5))

    def test_synthetic_unknown_breaks_observation_and_exposure(self):
        points = synthetic_points([0, 0, 1, 1, 0], [0, 1, None, 1, 0],
                                  eligible=[True, True, False, True, True])
        report = synthetic_report(points)
        first, second = report.episodes
        self.assertTrue(first.right_censored)
        self.assertTrue(second.left_censored)
        self.assertFalse(first.left_censored)
        self.assertFalse(second.right_censored)
        self.assertEqual(report.slices[0].exposure_seconds, Decimal("0.10"))
        self.assertEqual(report.slices[0].episodes_per_hour, 72000)
        self.assertIsNone(report.events.outcomes[0].first_fresh_onset_row)
        self.assertIsNone(report.events.outcomes[0].pre_existing_alarm)

    def test_synthetic_segment_boundary_breaks_episodes_without_false_onset(self):
        points = synthetic_points([0, 1, 1, 0], [1, 1, 1, 0], segments=[0, 0, 1, 1])
        report = synthetic_report(points)
        self.assertEqual(len(report.episodes), 2)
        self.assertTrue(report.episodes[0].left_censored)
        self.assertTrue(report.episodes[0].right_censored)
        self.assertTrue(report.episodes[1].left_censored)
        self.assertEqual(report.slices[0].exposure_seconds, Decimal("0.10"))
        self.assertIsNone(report.events.outcomes[0].first_fresh_onset_row)

    def test_synthetic_unknown_without_segment_is_allowed_only_when_excluded(self):
        points = synthetic_points([0, 1, 1, 1, 0], [0, 1, None, 1, 0],
                                  eligible=[True, True, False, True, True],
                                  segments=[0, 0, None, 1, 1])
        report = synthetic_report(points)
        self.assertEqual(len(report.episodes), 2)
        self.assertTrue(report.episodes[0].right_censored)
        self.assertTrue(report.episodes[1].left_censored)
        self.assertEqual(report.slices[0].exposure_seconds, Decimal("0.10"))
        points[1] = replace(points[1], segment=None)
        with self.assertRaises(MetricError) as caught:
            synthetic_report(points)
        self.assertEqual(caught.exception.reason, "eligible_point_without_segment")

    def test_synthetic_reporting_and_event_boundaries_do_not_reset_episode(self):
        points = synthetic_points([0, 0, 1, 1, 0], [0, 1, 1, 1, 0])
        report = synthetic_report(points, ranges={"normal": (0, 2), "mixed": (2, 5)})
        normal, mixed = report.slices
        self.assertEqual(normal.episode_ids, mixed.episode_ids)
        self.assertEqual((normal.crosses_end_count, mixed.crosses_start_count), (1, 1))
        self.assertEqual((normal.right_censored_count, mixed.left_censored_count), (0, 0))
        self.assertEqual(normal.episodes_per_hour, 72000)

    def test_synthetic_unscored_event_stays_in_denominator(self):
        points = synthetic_points([0, 1, 1, 0], [0, None, None, 0], eligible=[True, False, False, True])
        report = synthetic_report(points)
        self.assertEqual(report.events.denominator, 1)
        self.assertEqual(report.events.overlap_recall, 0)
        self.assertEqual(report.events.coverage_failure_events, 1)
        self.assertEqual(report.events.outcomes[0].excluded_rows, 2)

    def test_synthetic_single_positive_has_censored_onset_and_zero_exposure(self):
        report = synthetic_report(synthetic_points([1], [1]))
        self.assertTrue(report.episodes[0].left_censored)
        self.assertTrue(report.episodes[0].right_censored)
        self.assertEqual(report.slices[0].exposure_seconds, 0)
        self.assertIsNone(report.slices[0].episodes_per_hour)
        self.assertIsNone(report.events.outcomes[0].pre_existing_alarm)
        self.assertIsNone(report.events.outcomes[0].first_fresh_onset_row)

    def test_synthetic_clock_restart_censors_delay(self):
        points = synthetic_points([0, 1, 1, 1, 0], [0, 0, 0, 1, 0], segments=[0, 0, 1, 1, 1],
                                  times=[Decimal("10"), Decimal("10.05"), Decimal("0"),
                                         Decimal("0.05"), Decimal("0.10")])
        event = synthetic_report(points).events.outcomes[0]
        self.assertTrue(event.interval_overlap_hit)
        self.assertIsNone(event.overlap_delay_seconds)
        self.assertEqual(event.overlap_delay_reason, "clock_discontinuity")
        self.assertEqual(event.first_fresh_onset_row, 3)
        self.assertIsNone(event.fresh_onset_delay_seconds)

    def test_synthetic_nonzero_domain_start(self):
        report = synthetic_report(synthetic_points([0, 1, 0], [0, 1, 0], start=50))
        self.assertEqual(report.expected_domain, (50, 53))
        self.assertEqual(report.events.outcomes[0].first_overlap_row, 51)

    def test_synthetic_eight_events_one_preexisting_sustained_alarm(self):
        labels = [0, 0]
        for _ in range(8):
            labels.extend([1, 1, 0])
        scores = [0] + [1] * (len(labels) - 1)
        report = synthetic_report(synthetic_points(labels, scores))
        self.assertEqual(len(report.episodes), 1)
        self.assertEqual(report.events.denominator, 8)
        self.assertEqual(report.events.overlap_hits, 8)
        self.assertEqual(report.events.overlap_recall, 1)
        self.assertEqual(report.events.fresh_onset_events, 0)
        self.assertEqual(report.events.fresh_onset_recall, 0)
        self.assertTrue(all(e.pre_existing_alarm is True for e in report.events.outcomes))
        self.assertTrue(all(e.overlap_delay_seconds == 0 for e in report.events.outcomes))
        self.assertTrue(all(e.first_fresh_onset_row is None for e in report.events.outcomes))
        self.assertTrue(all(e.episode_ids == (1,) for e in report.events.outcomes))

    def test_synthetic_native_time_independent_of_ambient_decimal_context(self):
        # Construct fixtures outside the hostile ambient context. The labels
        # start at .05 seconds and the first alarm occurs at 49.95 seconds.
        times = [Decimal(i) / Decimal(20) for i in range(1001)]
        labels = [0] + [1] * 1000
        scores = [0] * 999 + [1, 1]
        points = synthetic_points(labels, scores, times=times)
        expected = synthetic_report(points)
        self.assertEqual(expected.slices[0].exposure_seconds, Decimal("50"))
        self.assertEqual(expected.slices[0].episodes_per_hour, 72)
        self.assertEqual(expected.events.outcomes[0].overlap_delay_seconds, Decimal("49.90"))
        self.assertEqual(expected.events.outcomes[0].fresh_onset_delay_seconds, Decimal("49.90"))
        original = getcontext().copy()
        for rounding in (ROUND_DOWN, ROUND_UP):
            with self.subTest(rounding=rounding), localcontext() as ctx:
                ctx.prec = 2
                ctx.rounding = rounding
                ctx.traps[Inexact] = True
                ctx.traps[Rounded] = True
                ctx.clear_flags()
                actual = synthetic_report(points)
                self.assertEqual(actual, expected)
                self.assertEqual(ctx.prec, 2)
                self.assertEqual(ctx.rounding, rounding)
                self.assertTrue(ctx.traps[Inexact])
                self.assertTrue(ctx.traps[Rounded])
                self.assertFalse(any(ctx.flags.values()))
        self.assertEqual(getcontext().prec, original.prec)
        self.assertEqual(getcontext().rounding, original.rounding)
        self.assertEqual(getcontext().traps, original.traps)
        self.assertEqual(getcontext().flags, original.flags)

    def test_synthetic_nonterminating_episode_rate_ignores_decimal_traps(self):
        # 3600 / .15 terminates; 3600 / .35 does not. Both rates are binary64
        # outputs computed from exact rational exposure, not Decimal division.
        times = [Decimal(i) / Decimal(20) for i in range(8)]
        points = synthetic_points([0] * 8, [0, 1, 1, 0, 0, 0, 0, 0], times=times)
        expected = synthetic_report(points)
        self.assertEqual(expected.slices[0].exposure_seconds, Decimal(".35"))
        self.assertEqual(expected.slices[0].episodes_per_hour, 72000 / 7)
        with localcontext() as ctx:
            ctx.prec = 2
            ctx.traps[Inexact] = True
            ctx.traps[Rounded] = True
            ctx.clear_flags()
            self.assertEqual(synthetic_report(points), expected)
            self.assertFalse(any(ctx.flags.values()))


class AdmissionTests(unittest.TestCase):
    def setUp(self):
        self.points = synthetic_points([0, 1, 0], [0, 1, 0])
        self.kwargs = dict(expected_domain=(0, 3), expected_eligible_rows=[0, 1, 2],
                           threshold=0.5, reporting_ranges={"synthetic": (0, 3)},
                           events=[Event("synthetic-1", 1, 2)])

    def test_synthetic_omitted_duplicate_out_of_order_rows_rejected(self):
        variants = [self.points[:2], self.points + [self.points[-1]],
                    [self.points[0], self.points[0], self.points[2]], list(reversed(self.points))]
        for points in variants:
            with self.subTest(rows=[p.row for p in points]), self.assertRaises(MetricError):
                evaluate(points, **self.kwargs)

    def test_synthetic_missing_nonfinite_boolean_scores_fail_admission(self):
        for value in [None, math.nan, math.inf, True]:
            points = list(self.points)
            points[1] = replace(points[1], score=value)
            with self.subTest(value=value), self.assertRaises(MetricError) as caught:
                evaluate(points, **self.kwargs)
            self.assertEqual(caught.exception.reason, "incomplete_score_coverage")
            self.assertEqual(caught.exception.details["finite_scored_rows"], 2)

    def test_synthetic_mask_mismatch_and_invalid_expected_rows(self):
        for mask in [[0, 2], [0, 1, 1, 2], [0, 1, 2, 3], [False, 1, 2]]:
            with self.subTest(mask=mask), self.assertRaises(MetricError):
                evaluate(self.points, **{**self.kwargs, "expected_eligible_rows": mask})

    def test_synthetic_score_on_excluded_row_rejected(self):
        points = [replace(self.points[0], eligible=False), *self.points[1:]]
        with self.assertRaises(MetricError) as caught:
            evaluate(points, **{**self.kwargs, "expected_eligible_rows": [1, 2]})
        self.assertEqual(caught.exception.reason, "score_outside_eligible_support")

    def test_synthetic_invalid_thresholds(self):
        for threshold in [True, None, "0.5", math.nan, math.inf]:
            with self.subTest(threshold=threshold), self.assertRaises(MetricError):
                evaluate(self.points, **{**self.kwargs, "threshold": threshold})

    def test_synthetic_invalid_time_label_segment_and_row_types(self):
        mutations = [dict(time=0.05), dict(time=Decimal("NaN")), dict(time=Decimal("Infinity")),
                     dict(time=Decimal(0)), dict(label=2), dict(label=True), dict(segment=-1),
                     dict(segment=True), dict(row=True), dict(eligible=1)]
        for mutation in mutations:
            points = list(self.points)
            points[1] = replace(points[1], **mutation)
            with self.subTest(mutation=mutation), self.assertRaises(MetricError):
                evaluate(points, **self.kwargs)

    def test_synthetic_segment_reuse_rejected(self):
        points = [replace(p, segment=s) for p, s in zip(self.points, [0, 1, 0])]
        with self.assertRaises(MetricError):
            evaluate(points, **self.kwargs)

    def test_synthetic_omitted_shifted_duplicate_events_rejected(self):
        for events in [[], [Event("x", 0, 2)], [Event("x", 1, 2), Event("x", 1, 2)],
                       [Event("x", 1, 4)], [Event("x", 1, 1)]]:
            with self.subTest(events=events), self.assertRaises(MetricError):
                evaluate(self.points, **{**self.kwargs, "events": events})

    def test_synthetic_invalid_ranges_rejected(self):
        for ranges in [{}, {"x": (-1, 2)}, {"x": (0, 4)}, {"x": (2, 1)}, {"": (0, 3)}]:
            with self.subTest(ranges=ranges), self.assertRaises(MetricError):
                evaluate(self.points, **{**self.kwargs, "reporting_ranges": ranges})

    def test_synthetic_points_and_results_are_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            self.points[0].row = 1
        report = evaluate(self.points, **self.kwargs)
        with self.assertRaises(FrozenInstanceError):
            report.threshold = 2


if __name__ == "__main__":
    unittest.main()
