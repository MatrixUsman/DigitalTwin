import unittest
import numpy as np
from pilot_data import prepare_prefix


class PilotIsolationTests(unittest.TestCase):
    def fixture(self):return np.random.default_rng(17).normal(size=(28,9))
    def test_development_cannot_change_fit_or_training(self):
        v=self.fixture();a=prepare_prefix(v,history=4,train_targets=12,dev_targets=8)
        v[16:]+=10000;b=prepare_prefix(v,history=4,train_targets=12,dev_targets=8)
        for k in ['mean','scale','train_x','train_y']:np.testing.assert_array_equal(a[k],b[k])
    def test_windows_do_not_cross_split(self):
        v=self.fixture();p=prepare_prefix(v,history=4,train_targets=12,dev_targets=8)
        np.testing.assert_allclose(p['dev_x'][0],((v[16:20]-p['mean'])/p['scale']).astype(np.float32))
        self.assertEqual(p['train_target_indices'][-1],15);self.assertEqual(p['dev_target_indices'][0],20)
    def test_future_changes_do_not_change_earlier_inputs(self):
        v=self.fixture();a=prepare_prefix(v,history=4,train_targets=12,dev_targets=8)
        v[24:]=-1234;b=prepare_prefix(v,history=4,train_targets=12,dev_targets=8)
        np.testing.assert_array_equal(a['dev_x'][:5],b['dev_x'][:5])
    def test_constant_channel_rejected(self):
        v=self.fixture();v[:16,0]=1
        with self.assertRaises(ValueError):prepare_prefix(v,history=4,train_targets=12,dev_targets=8)
    def test_nonfinite_rejected(self):
        v=self.fixture();v[0,0]=np.inf
        with self.assertRaises(ValueError):prepare_prefix(v,history=4,train_targets=12,dev_targets=8)

if __name__=='__main__':unittest.main()
