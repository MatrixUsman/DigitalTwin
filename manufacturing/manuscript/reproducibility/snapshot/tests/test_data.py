"""Offline software checks using SYNTHETIC CSV observations only.

These fixtures do not contain CASPER observations and establish no benchmark
result, physical realism, model quality or production dataset admission.
"""

from __future__ import annotations

import csv
import dataclasses
import io
import json
import tempfile
import unittest
from decimal import Decimal, localcontext
from pathlib import Path

from mfg_twin.data import (
    CASPER_HEADER, DataContractError, EvaluatorRecord, Observation,
    PartitionSpec, causal_windows, iter_csv_partition,
)


def synthetic_rows(count: int) -> list[list[str]]:
    rows = []
    for index in range(count):
        # Deliberately nonnumeric excluded columns demonstrate the allowlist.
        row = ["EXCLUDED_SYNTHETIC_FIELD"] * len(CASPER_HEADER)
        row[0] = str(Decimal("100") + Decimal(index) / 20)
        row[1] = json.dumps([index + axis / 10 for axis in range(6)])
        row[2] = json.dumps([axis + 0.01 for axis in range(6)])
        row[-1] = "0"
        rows.append(row)
    return rows


def synthetic_csv(rows: list[list[str]], header=CASPER_HEADER) -> io.StringIO:
    stream = io.StringIO(newline="")
    writer = csv.writer(stream)
    writer.writerow(header)
    writer.writerows(rows)
    stream.seek(0)
    return stream


class PartitionSpecTests(unittest.TestCase):
    def test_defaults_and_expected_count(self):
        spec = PartitionSpec("synthetic", 12, 15)
        self.assertEqual(spec.expected_rows, 3)
        self.assertEqual(spec.warmup, 1528)
        self.assertEqual(spec.gap_seconds, Decimal("0.075"))

    def test_invalid_partition_specs_fail(self):
        for kwargs in (
            {"name": ""}, {"start": -1}, {"start": 3}, {"end": 0},
            {"warmup": -1}, {"warmup": True}, {"start": 0.0},
            {"gap_seconds": 0.075}, {"gap_seconds": Decimal("0")},
            {"gap_seconds": Decimal("NaN")}, {"gap_seconds": Decimal("Infinity")},
        ):
            values = dict(name="synthetic", start=0, end=3)
            values.update(kwargs)
            with self.subTest(kwargs=kwargs), self.assertRaises((TypeError, ValueError)):
                PartitionSpec(**values)


class LoaderTests(unittest.TestCase):
    def load(self, rows, start=0, end=None, warmup=1):
        spec = PartitionSpec("synthetic", start, len(rows) if end is None else end, warmup)
        return list(iter_csv_partition(synthetic_csv(rows), spec))

    def test_feature_allowlist_and_evaluator_separation(self):
        result = self.load(synthetic_rows(3))
        observation = result[1].observation
        self.assertEqual([field.name for field in dataclasses.fields(Observation)], ["q", "qdot", "dt"])
        self.assertEqual(len(observation.q), 6)
        self.assertEqual(len(observation.qdot), 6)
        self.assertEqual(observation.dt, Decimal("0.05"))
        for forbidden in ("label", "row", "timestamp", "path", "segment", "eligible", "partition"):
            self.assertFalse(hasattr(observation, forbidden))
        with self.assertRaises((AttributeError, TypeError)):
            observation.label = 1
        self.assertEqual(result[1].label, 0)
        self.assertEqual(result[1].row, 1)
        self.assertEqual(result[1].timestamp, Decimal("100.05"))

    def test_exact_half_open_split_and_no_prior_parsing_or_history(self):
        rows = synthetic_rows(6)
        rows[0][0] = "bad timestamp before selected split"
        rows[0][1] = "bad vector before selected split"
        rows[0][-1] = "bad label before selected split"
        records = self.load(rows, start=2, end=5)
        self.assertEqual([record.row for record in records], [2, 3, 4])
        self.assertEqual([record.eligible for record in records], [False, True, True])
        self.assertEqual(records[0].segment, 0)
        self.assertIsNone(records[0].observation.dt)
        self.assertEqual(records[1].observation.dt, Decimal("0.05"))

    def test_suffix_changes_do_not_affect_prefix_outputs(self):
        rows = synthetic_rows(8)
        expected = self.load(rows, end=4)
        rows[4][0], rows[4][1], rows[4][-1] = "INVALID", "INVALID", "INVALID"
        rows[5] = ["wrong row width beyond split"]
        self.assertEqual(self.load(rows, end=4), expected)

    def test_never_requests_record_beyond_end(self):
        class GuardedStream(io.StringIO):
            def __init__(self, text):
                super().__init__(text)
                self.calls = 0

            def __next__(self):
                self.calls += 1
                if self.calls > 4:  # One header and exactly three records.
                    raise AssertionError("read beyond partition end")
                return super().__next__()

        stream = GuardedStream(synthetic_csv(synthetic_rows(10)).getvalue())
        records = list(iter_csv_partition(stream, PartitionSpec("synthetic", 1, 3, 0)))
        self.assertEqual(len(records), 2)
        self.assertEqual(stream.calls, 4)
        self.assertFalse(stream.closed)

    def test_native_decimal_delta_ignores_ambient_rounding(self):
        rows = synthetic_rows(2)
        rows[0][0] = "328538.426"
        rows[1][0] = "328538.47599999997"
        with localcontext() as context:
            context.prec = 6
            records = self.load(rows)
        self.assertEqual(records[1].timestamp, Decimal("328538.47599999997"))
        self.assertEqual(records[1].observation.dt, Decimal("0.04999999997"))

    def test_warmup_requires_preceding_observations_not_inclusive_count(self):
        records = self.load(synthetic_rows(5), warmup=2)
        self.assertEqual([record.eligible for record in records], [False, False, True, True, True])
        self.assertEqual([record.exclusion for record in records], ["warmup", "warmup", None, None, None])

    def test_zero_warmup_makes_valid_segment_start_eligible(self):
        records = self.load(synthetic_rows(2), warmup=0)
        self.assertTrue(records[0].eligible)
        self.assertIsNone(records[0].observation.dt)

    def test_gap_restarts_warmup_and_state(self):
        rows = synthetic_rows(6)
        for index in range(3, 6):
            rows[index][0] = str(Decimal(rows[index][0]) + Decimal("0.05"))
        records = self.load(rows, warmup=2)
        self.assertEqual([record.segment for record in records], [0, 0, 0, 1, 1, 1])
        self.assertEqual([record.eligible for record in records], [False, False, True, False, False, True])
        self.assertIsNone(records[3].observation.dt)

    def test_gap_boundary_exactly_075_is_continuous(self):
        rows = synthetic_rows(3)
        rows[1][0], rows[2][0] = "100.075", "100.1500000000001"
        records = self.load(rows)
        self.assertEqual([record.segment for record in records], [0, 0, 1])
        self.assertEqual(records[1].observation.dt, Decimal("0.075"))
        self.assertIsNone(records[2].observation.dt)

    def test_nonpositive_clock_increment_restarts(self):
        for time in ("100", "99.9"):
            rows = synthetic_rows(3)
            rows[1][0] = time
            rows[2][0] = str(Decimal(time) + Decimal("0.05"))
            with self.subTest(time=time):
                records = self.load(rows)
                self.assertEqual([record.segment for record in records], [0, 1, 1])
                self.assertEqual([record.eligible for record in records], [False, False, True])

    def test_labels_do_not_change_features_continuity_or_windows(self):
        rows = synthetic_rows(8)
        first = self.load(rows)
        for index, row in enumerate(rows):
            row[-1] = str(index % 2)
        second = self.load(rows)
        self.assertEqual([record.observation for record in first], [record.observation for record in second])
        self.assertEqual([record.segment for record in first], [record.segment for record in second])
        self.assertEqual([record.eligible for record in first], [record.eligible for record in second])
        self.assertEqual(list(causal_windows(first, 2)), list(causal_windows(second, 2)))
        self.assertNotEqual([record.label for record in first], [record.label for record in second])

    def test_invalid_vectors_emit_unknown_and_require_fresh_warmup(self):
        invalid = (
            "[]", "[0, 0, 0, 0, 0]", "[0, 0, 0, 0, 0, 0, 0]",
            "[0, 0, 0, 0, 0, true]", '[0, 0, 0, 0, 0, "1"]',
            "[0, 0, 0, 0, 0, null]", "[0, 0, 0, 0, 0, [1]]",
            "[0, 0, 0, 0, 0, NaN]", "[0, 0, 0, 0, 0, Infinity]",
            "[0, 0, 0, 0, 0, 1e999]", "{\"0\": 1}",
            "__import__('os').getcwd()", "(0, 0, 0, 0, 0, 0)",
        )
        for column, reason in ((1, "invalid_joint_positions"), (2, "invalid_joint_velocities")):
            for text in invalid:
                with self.subTest(column=column, text=text):
                    rows = synthetic_rows(6)
                    rows[2][column] = text
                    records = self.load(rows)
                    self.assertIsNone(records[2].observation)
                    self.assertFalse(records[2].eligible)
                    self.assertIsNone(records[2].segment)
                    self.assertEqual(records[2].exclusion, reason)
                    self.assertEqual(records[2].timestamp, Decimal("100.1"))
                    self.assertEqual(records[3].segment, 1)
                    self.assertIsNone(records[3].observation.dt)
                    self.assertFalse(records[3].eligible)
                    self.assertTrue(records[4].eligible)

    def test_bad_labels_fail_closed(self):
        for label in ("", "2", "-1", "0.0", "1.0", "True", " 1", "1 "):
            rows = synthetic_rows(2)
            rows[1][-1] = label
            with self.subTest(label=label), self.assertRaisesRegex(DataContractError, "literal 0/1"):
                self.load(rows)

    def test_bad_native_timestamps_fail_closed(self):
        for timestamp in ("", "not a timestamp", "NaN", "Infinity", "-Infinity"):
            rows = synthetic_rows(2)
            rows[1][0] = timestamp
            with self.subTest(timestamp=timestamp), self.assertRaisesRegex(DataContractError, "invalid timestamp"):
                self.load(rows)

    def test_missing_duplicate_reordered_and_extra_headers_fail(self):
        duplicate = list(CASPER_HEADER)
        duplicate[-1] = duplicate[0]
        reordered = list(CASPER_HEADER)
        reordered[1], reordered[2] = reordered[2], reordered[1]
        for header in (CASPER_HEADER[:-1], duplicate, reordered, (*CASPER_HEADER, "extra")):
            with self.subTest(header=header), self.assertRaises(DataContractError):
                list(iter_csv_partition(synthetic_csv(synthetic_rows(2), header), PartitionSpec("synthetic", 0, 2)))
        with self.assertRaisesRegex(DataContractError, "missing CSV header"):
            list(iter_csv_partition(io.StringIO(""), PartitionSpec("synthetic", 0, 2)))

    def test_wrong_width_and_malformed_csv_fail(self):
        for row in (["one"], [], ["x"] * 21):
            rows = synthetic_rows(2)
            rows[1] = row
            with self.subTest(row=row), self.assertRaisesRegex(DataContractError, "field count"):
                self.load(rows)
        text = synthetic_csv([]).getvalue() + '"unterminated\n'
        with self.assertRaisesRegex(DataContractError, "malformed CSV"):
            list(iter_csv_partition(io.StringIO(text), PartitionSpec("synthetic", 0, 1)))

    def test_short_partition_fails_even_when_valid_prefix_was_yielded(self):
        for start, end, expected in ((0, 4, 3), (2, 5, 1), (5, 6, 0)):
            with self.subTest(start=start), self.assertRaisesRegex(DataContractError, f"observed {expected}"):
                self.load(synthetic_rows(3), start=start, end=end)

    def test_path_read_keeps_synthetic_bytes_unchanged(self):
        payload = synthetic_csv(synthetic_rows(3)).getvalue().encode("utf-8")
        with tempfile.TemporaryDirectory(prefix="synthetic_mfg_loader_") as directory:
            path = Path(directory) / "synthetic_input.txt"
            path.write_bytes(payload)
            records = list(iter_csv_partition(path, PartitionSpec("synthetic", 0, 3, 1)))
            self.assertEqual(len(records), 3)
            self.assertEqual(path.read_bytes(), payload)


class WindowTests(unittest.TestCase):
    def records(self, rows, spec=None):
        return list(iter_csv_partition(synthetic_csv(rows), spec or PartitionSpec("synthetic", 0, len(rows), 2)))

    def test_windows_are_trailing_feature_only_and_endpoint_aligned(self):
        records = self.records(synthetic_rows(6))
        windows = list(causal_windows(records, 3))
        self.assertEqual(len(windows), 4)
        self.assertEqual([[obs.q[0] for obs in window] for window in windows], [
            [0, 1, 2], [1, 2, 3], [2, 3, 4], [3, 4, 5],
        ])
        self.assertTrue(all(isinstance(obs, Observation) for window in windows for obs in window))
        self.assertEqual([window[-1] for window in windows], [record.observation for record in records if record.eligible])

    def test_windows_never_cross_gap_or_invalid_observation(self):
        rows = synthetic_rows(10)
        rows[3][1] = "invalid synthetic vector"
        for index in range(7, 10):
            rows[index][0] = str(Decimal(rows[index][0]) + Decimal("1"))
        windows = list(causal_windows(self.records(rows), 3))
        self.assertEqual([[obs.q[0] for obs in window] for window in windows], [
            [0, 1, 2], [4, 5, 6], [7, 8, 9],
        ])

    def test_suffix_change_cannot_change_earlier_windows(self):
        rows = synthetic_rows(8)
        before = list(causal_windows(self.records(rows), 3))
        rows[5][1] = json.dumps([999] * 6)
        after = list(causal_windows(self.records(rows), 3))
        self.assertEqual(before[:3], after[:3])
        self.assertNotEqual(before[3], after[3])

    def test_insufficient_history_fails_instead_of_dropping_eligible_rows(self):
        with self.assertRaisesRegex(DataContractError, "exceeds history"):
            list(causal_windows(self.records(synthetic_rows(6)), 4))

    def test_chained_partitions_cannot_borrow_history_even_when_ids_repeat(self):
        rows = synthetic_rows(6)
        first = self.records(rows, PartitionSpec("synthetic_first", 0, 3, 2))
        second = self.records(rows, PartitionSpec("synthetic_second", 3, 6, 2))
        self.assertEqual(first[-1].segment, second[0].segment)
        windows = list(causal_windows(first + second, 3))
        self.assertEqual([[obs.q[0] for obs in window] for window in windows], [[0, 1, 2], [3, 4, 5]])
        zero_warmup_second = self.records(rows, PartitionSpec("synthetic_second", 3, 6, 0))
        with self.assertRaisesRegex(DataContractError, "exceeds history"):
            list(causal_windows(first + zero_warmup_second, 3))

    def test_missing_row_resets_even_when_segment_identifier_reused(self):
        records = self.records(synthetic_rows(7))
        with self.assertRaisesRegex(DataContractError, "exceeds history"):
            list(causal_windows(records[:3] + records[4:], 3))

    def test_eligible_missing_observation_fails(self):
        record = EvaluatorRecord(0, Decimal("0"), 0, None, True, None, "invalid_joint_positions")
        with self.assertRaisesRegex(DataContractError, "no observation"):
            list(causal_windows([record], 1))

    def test_invalid_window_length_fails(self):
        for length in (0, -1, True, 1.5):
            with self.subTest(length=length), self.assertRaises(ValueError):
                list(causal_windows([], length))


if __name__ == "__main__":
    unittest.main()
