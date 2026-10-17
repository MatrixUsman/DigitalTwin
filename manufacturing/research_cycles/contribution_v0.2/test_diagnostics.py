import unittest
from pathlib import Path
import numpy as np
from diagnostics import aligned_rmse, prediction_target_indices, cells_from_verified_notebook, source_diagnostics

PROJECT = Path(__file__).resolve().parents[2]


class AlignmentTests(unittest.TestCase):
    def test_next_point_is_outside_history(self):
        np.testing.assert_array_equal(prediction_target_indices(8, 3, 1).ravel(), [3,4,5,6,7])

    def test_multistep_targets(self):
        np.testing.assert_array_equal(prediction_target_indices(8, 3, 2), [[3,4],[4,5],[5,6],[6,7]])

    def test_perfect_future_forecast_has_zero_error(self):
        x=np.arange(120,dtype=float).reshape(40,3)
        idx=prediction_target_indices(40,8,4)
        np.testing.assert_array_equal(aligned_rmse(x[idx],x,idx),np.zeros((29,4)))

    def test_predictions_are_not_scored_against_inputs(self):
        x=np.arange(90,dtype=float)[:,None]
        idx=prediction_target_indices(90,45,45)
        self.assertEqual(float(aligned_rmse(x[:45][None,:,:],x,idx).mean()),45.)

    def test_future_outside_target_does_not_change_score(self):
        x=np.arange(100,dtype=float)[:,None]; idx=np.array([[45,46]])
        pred=x[idx].copy(); first=aligned_rmse(pred,x,idx)
        x[47:]=-1e9
        np.testing.assert_array_equal(first,aligned_rmse(pred,x,idx))

    def test_nonfinite_rejected(self):
        with self.assertRaises(ValueError):aligned_rmse(np.array([[[np.nan]]]),np.zeros((3,1)),np.array([[2]]))

    def test_negative_indices_rejected(self):
        with self.assertRaises(ValueError):aligned_rmse(np.zeros((1,1,1)),np.zeros((3,1)),np.array([[-1]]))

    def test_wrong_shapes_rejected(self):
        with self.assertRaises(ValueError):aligned_rmse(np.zeros((2,1,1)),np.zeros((3,1)),np.array([[2]]))

    def test_short_stream_rejected(self):
        with self.assertRaises(ValueError):prediction_target_indices(10,45,1)


class PinnedSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        notebook=PROJECT/'local/comparator_admission_20261017/replacements/edge_main.ipynb'
        cls.result=source_diagnostics(cells_from_verified_notebook(notebook))

    def test_saved_cnn_path_shape_failure(self):
        self.assertEqual(self.result['D1']['observed'],'ValueError')
        self.assertEqual(self.result['D1']['predictions']-self.result['D1']['hardcoded_targets'],15)

    def test_perfect_forecast_gets_wrong_source_score(self):
        r=self.result['D2']
        self.assertAlmostEqual(r['upstream_l2_window_score_min'],45*np.sqrt(45*9))
        self.assertEqual(r['correct_future_rmse_max'],0.)

    def test_lstm_scores_do_not_feed_saved_aggregation(self):
        self.assertTrue(self.result['D3']['score_unchanged_when_lstm_window_scores_change'])
        self.assertTrue(set(self.result['D3']['reads']).isdisjoint(self.result['D3']['cell281_writes']))

    def test_norms_reverse_order(self):
        r=self.result['D4']
        self.assertGreater(r['a_notebook_rmse'],r['b_notebook_rmse'])
        self.assertLess(r['a_embedded_sum_abs'],r['b_embedded_sum_abs'])


if __name__=='__main__':unittest.main()
