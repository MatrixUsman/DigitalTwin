"""Synthetic helper tests plus optional extracted-package identity verification."""
from pathlib import Path
import argparse, importlib.util, json, tempfile, unittest

HERE = Path(__file__).resolve().parent

def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    result = importlib.util.module_from_spec(spec); spec.loader.exec_module(result)
    return result

replay = module('reviewer_replay', 'replay_tables.py')
pack = module('reviewer_pack', 'build_package.py')
portable = module('reviewer_portable', 'portable_replay.py')

class SyntheticPackageTests(unittest.TestCase):
    def test_missing_and_censored_values_remain_visible(self):
        d = replay.describe([None, .02, .06, None])
        self.assertEqual((d['n'], d['missing']), (2, 2))
        self.assertAlmostEqual(d['median'], .04)
        self.assertAlmostEqual(d['p95'], .058)

    def test_empty_and_nonfinite_outcomes(self):
        self.assertIsNone(replay.describe([None])['median'])
        with self.assertRaises(ValueError):
            replay.describe([float('nan')])

    def test_no_raw_or_traversal_paths(self):
        for value in ['/private/file', '../file', 'local/private/key', 'datasets/raw/a.csv', 'baselines/vendor/upstream.py', '.venv/bin/python', 'local\\file']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                pack.safe_path(value)

    def test_symlinks_are_not_admitted(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'real').write_text('synthetic')
            (root / 'link').symlink_to(root / 'real')
            with self.assertRaises(ValueError):
                pack.safe_path('link', root)

    def test_adapter_fails_on_unexpected_provenance(self):
        with self.assertRaises(ValueError):
            portable.adapt('print("synthetic unrelated worker")', 18)

    def test_final_adapter_keeps_declared_storage_policy(self):
        with tempfile.TemporaryDirectory() as temp:
            cycle = Path(temp)
            freeze = cycle / 'FINAL_FREEZE.json'
            freeze.write_text(json.dumps({'worker': 'worker_compact.py'}))
            self.assertEqual(portable.selected_wrapper(cycle, 19, 'final'), cycle / 'worker_compact.py')
            self.assertIsNone(portable.selected_wrapper(cycle, 19, 'development'))
            freeze.write_text(json.dumps({'worker': 'synthetic_unexpected.py'}))
            with self.assertRaises(ValueError):
                portable.selected_wrapper(cycle, 19, 'final')

    def test_compact_binding_rejects_an_unrecognized_loader(self):
        with self.assertRaises(ValueError):
            portable.adapt_compact_loader('worker = synthetic_different_loader()')

    def test_exposure_denominator_is_not_all_rows(self):
        base = dict(method='synthetic', plant='S', task='fixture', condition='fixture', plant_group='fixture',
                    benign=True, event=False, eligible=100, alarm_points=2, alarm_episodes=1,
                    tp=0, fp=2, fn=0, alarm_durations_seconds=[.04], overlap=False, fresh=False,
                    outside_inactive=0, outside_points=0, joint=False, clear_timely=False,
                    already_clear_at_return=False, return_missing=False, returned_detected=False,
                    detection_delay=None, fresh_delay=None, clear_delay=None)
        attack = dict(base, benign=False, event=True, eligible=200, alarm_points=0, alarm_episodes=0,
                      fp=0, fn=10, alarm_durations_seconds=[], outside_inactive=10, outside_points=10)
        row = replay.aggregate([base, attack], 19)[0]
        self.assertEqual(row['benign_points'], 100)
        self.assertEqual(row['occupancy'], .02)
        self.assertEqual(row['events'], 1)
        self.assertEqual(row['misses'], 1)
        self.assertEqual(row['detection_delay']['missing'], 1)
        self.assertEqual(row['outside_inactive'], 10)

def verify(root):
    allow = root / 'reproducibility_v1.7/ALLOWLIST.json'
    data = json.loads(allow.read_text())
    checks = 0
    for record in data['files']:
        p = pack.safe_path(record['path'], root)
        if not p.is_file() or p.stat().st_size != record['bytes'] or pack.digest(p) != record['sha256']:
            raise AssertionError('Package binding failed: ' + record['path'])
        checks += 1
    return checks

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-root', type=Path)
    args = parser.parse_args()
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(SyntheticPackageTests))
    if not result.wasSuccessful():
        raise SystemExit(1)
    if args.verify_root:
        print(json.dumps({'status': 'passed', 'package_bindings': verify(args.verify_root.resolve()),
                          'synthetic_tests': result.testsRun, 'raw_dataset_access': False}))
