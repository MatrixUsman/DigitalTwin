from pathlib import Path
import sys,unittest
import numpy as np
H=Path(__file__).resolve().parent;P=H.parents[1]
sys.path[:0]=[str(H),str(P/'baselines/vendor/rapt_v020')]
from protocol21 import calibrate_eligible,curve_summary,stage_paths
from rapt import RaptConfig,SequenceData,NormStats,RaptModel,score_sequence
from rapt.data import make_windows
from rapt.detector import evaluate_step,Calibration
import torch
torch.set_num_threads(1)

class SyntheticProtocolTests(unittest.TestCase):
    def test_partition_requires_nine_unique(self):
        with self.assertRaises(ValueError):stage_paths({'files':[]},'Q1','fit')
    def test_duplicate_episode_rejected(self):
        rows=[dict(plant='Q1',role='fit',path='same') for _ in range(9)]
        with self.assertRaises(ValueError):stage_paths({'files':rows},'Q1','fit')
    def test_window_alignment_no_boundary_crossing(self):
        y=np.arange(4400,dtype=np.float32).reshape(1100,4);u=y+10000
        d=SequenceData([y,y+5000],[u,u+5000]);s=NormStats.from_data(d);x,z=make_windows(d,50,s,True)
        self.assertEqual(x.shape,(42,50,8));np.testing.assert_allclose(z[0,0],s.normalize(y)[1]);np.testing.assert_array_equal(x[0,0,4:],u[0]);np.testing.assert_array_equal(x[21,0,4:],u[0]+5000)
    def test_calibration_warmup_excluded(self):
        y=np.arange(480,dtype=float).reshape(120,4);loss=y.copy();loss[:100]=1e20
        c=calibrate_eligible([loss],[y],RaptConfig(obs_dim=4))
        np.testing.assert_array_equal(c.per_dim_max,loss[100:].max(0));self.assertEqual(c.mean_max,float(loss[100:].mean(1).max()))
    def test_strict_released_threshold(self):
        c=Calibration(np.zeros(4),np.ones(4),np.full(4,10.),1.,1.,10.,-np.ones(4),np.ones(4))
        self.assertFalse(evaluate_step(np.full(4,10.),np.zeros(4),c,use_range=False).is_anomaly)
        self.assertTrue(evaluate_step(np.full(4,10.+1e-6),np.zeros(4),c,use_range=False).is_anomaly)
    def test_checkpoint_selection_first_tie(self):
        v=[2.]*100;v[4]=v[8]=1.;s=curve_summary({'train_nll':[3.]*100,'val_nll':v});self.assertEqual(s['selected_epoch'],5);self.assertFalse(s['convergence_certified'])
    def test_incomplete_curve_rejected(self):
        with self.assertRaises(ValueError):curve_summary({'train_nll':[1.],'val_nll':[1.]})
    def test_causal_prefix_no_future(self):
        cfg=RaptConfig(obs_dim=4,action_dim=4,train_dynamics=True,embed_dim=8,num_blocks=1)
        m=RaptModel(cfg).eval();rng=np.random.default_rng(17);y=rng.normal(size=(35,4)).astype(np.float32);u=rng.normal(size=(35,4)).astype(np.float32)
        s=NormStats.from_data(SequenceData([y]));full=score_sequence(m,s,y,u);prefix=score_sequence(m,s,y[:20],u[:20]);np.testing.assert_allclose(full[:20],prefix,rtol=2e-5,atol=2e-6)

if __name__=='__main__':unittest.main()
