"""Entirely SYNTHETIC loader→causal coordinator→metrics tests, not CASPER results."""
import csv
import io
import json
import unittest
from dataclasses import replace
from decimal import Decimal

from mfg_twin.data import CASPER_HEADER, PartitionSpec, iter_csv_partition
from mfg_twin.metrics import Event, MetricError, calibrate, evaluate
from mfg_twin.replay import ReplayError, score_stream


def synthetic_csv(values, labels=None):
    stream = io.StringIO(newline="")
    writer = csv.writer(stream); writer.writerow(CASPER_HEADER)
    for row, value in enumerate(values):
        fields = ["SYNTHETIC_UNUSED"]*20
        fields[0] = str(Decimal(row)*Decimal(".05"))
        fields[1] = json.dumps([float(value)]*6)
        fields[2] = json.dumps([float(value)]*6)
        fields[-1] = str(labels[row] if labels is not None else 0)
        writer.writerow(fields)
    stream.seek(0)
    return stream


class SyntheticSpy:
    """Artificial state checker; no trained parameters or scientific detector."""
    def __init__(self):
        self.calls = []
        self.seen = 0

    def reset(self):
        self.seen = 0
        self.calls.append(("reset",))

    def score(self, observation):
        self.calls.append(("score", self.seen, observation.q[0]))
        assert set(observation.__slots__) == {"q", "qdot", "dt"}
        return observation.qdot[0]

    def update(self, observation):
        self.calls.append(("update", self.seen, observation.q[0]))
        self.seen += 1


class IntegrationTests(unittest.TestCase):
    def records(self, values, labels=None, *, start=0, end=None, warmup=2):
        return list(iter_csv_partition(synthetic_csv(values, labels),
                                      PartitionSpec("SYNTHETIC",start,len(values) if end is None else end,warmup=warmup)))

    def test_score_before_update_and_feature_only_interface(self):
        spy = SyntheticSpy()
        result = list(score_stream(self.records([0,1,2,3]), spy))
        self.assertEqual(spy.calls, [("reset",),("update",0,0),("update",1,1),
                                    ("score",2,2),("update",2,2),("score",3,3),("update",3,3)])
        self.assertEqual([x.score for x in result], [None,None,2,3])

    def test_changing_labels_never_changes_detector_calls(self):
        a,b = SyntheticSpy(),SyntheticSpy()
        points_a = list(score_stream(self.records([0,1,2,3]),a))
        points_b = list(score_stream(self.records([0,1,2,3],[1,0,1,1]),b))
        self.assertEqual(a.calls,b.calls)
        self.assertEqual([p.score for p in points_a],[p.score for p in points_b])
        self.assertNotEqual([p.label for p in points_a],[p.label for p in points_b])

    def test_future_change_never_changes_prefix(self):
        a=list(score_stream(self.records([0,1,2,3,4]),SyntheticSpy()))
        b=list(score_stream(self.records([0,1,2,90,80]),SyntheticSpy()))
        self.assertEqual(a[:3],b[:3])

    def test_small_synthetic_calibration_and_event_report(self):
        # Separate artificial streams, each reset/warmup independently.
        calibration_points=list(score_stream(self.records([0,0,1,2]),SyntheticSpy()))
        calibration=calibrate([p.score for p in calibration_points if p.eligible],expected_m=2)
        self.assertEqual(calibration.threshold,2)
        points=list(score_stream(self.records([0,0,0,1,3,3,0,0],[0,0,0,0,1,1,0,0]),SyntheticSpy()))
        report=evaluate(points,expected_domain=(0,8),expected_eligible_rows=range(2,8),threshold=calibration.threshold,
                        reporting_ranges={"normal":(0,4),"mixed":(4,8)},events=[Event("SYNTHETIC_EVENT",4,6)])
        normal,mixed=report.slices
        self.assertEqual(normal.exposure_seconds,Decimal(".05"))
        self.assertEqual(normal.points.alarm_rows,0)
        self.assertEqual((mixed.points.tp,mixed.points.fp,mixed.points.fn,mixed.points.tn),(2,0,0,2))
        self.assertEqual(report.events.outcomes[0].fresh_onset_delay_seconds,Decimal(0))
        self.assertEqual(report.events.denominator,1)

    def test_split_starts_new_state_without_preceding_history(self):
        spy = SyntheticSpy()
        result=list(score_stream(self.records([50,60,70,80,1,2,3,4],start=4,warmup=2),spy))
        self.assertEqual([p.score for p in result],[None,None,3,4])
        self.assertEqual(spy.calls[0],("reset",))
        self.assertEqual(spy.calls[1],("update",0,1))

    def test_broken_row_sequence_fails(self):
        records=self.records([0,1,2,3])
        with self.assertRaises(ReplayError):
            list(score_stream([records[0],records[2]],SyntheticSpy()))

    def test_nonfinite_or_nonnumeric_model_output_fails(self):
        for value in (float("nan"),float("inf"),True,"1",None):
            with self.subTest(value=value):
                spy=SyntheticSpy();spy.score=lambda _: value
                with self.assertRaises(ReplayError):
                    list(score_stream(self.records([0,1,2]),spy))

    def test_invalid_feature_keeps_unknown_and_resets(self):
        records=self.records([0,1,2,3,4,5],warmup=1)
        records[2]=replace(records[2],observation=None,eligible=False,segment=None,exclusion="synthetic_invalid")
        records[3]=replace(records[3],observation=replace(records[3].observation,dt=None),eligible=False,segment=1)
        records[4]=replace(records[4],segment=1);records[5]=replace(records[5],segment=1)
        spy=SyntheticSpy();points=list(score_stream(records,spy))
        self.assertEqual(sum(c[0]=="reset" for c in spy.calls),2)
        self.assertIsNone(points[2].score)
        report=evaluate(points,expected_domain=(0,6),expected_eligible_rows=[1,4,5],threshold=2,
                        reporting_ranges={"synthetic":(0,6)},events=[])
        self.assertEqual(report.coverage.scored_rows,3)

    def test_omitted_score_rejected_at_report_admission(self):
        points=list(score_stream(self.records([0,1,2,3]),SyntheticSpy()))
        points[3]=replace(points[3],score=None)
        with self.assertRaisesRegex(MetricError,"incomplete_score_coverage"):
            evaluate(points,expected_domain=(0,4),expected_eligible_rows=range(2,4),threshold=1,
                     reporting_ranges={"synthetic":(0,4)},events=[])


if __name__ == "__main__":
    unittest.main()
