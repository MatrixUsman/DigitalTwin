"""Synthetic software checks, not benchmark observations or results."""
from pathlib import Path
import sys,unittest
import numpy as np
H=Path(__file__).resolve().parent;P=H.parents[2]
sys.path[:0]=[str(H),str(P/'research_cycles/attack_audit_v0.14'),str(P/'baselines/vendor/rapt_v020')]
from replay21 import decisions,validate_population,quarters
from evaluation import evaluate,average_precision

class SyntheticChecks(unittest.TestCase):
    def test_complete_population(self):
        rows=[dict(id=f'{t}_{s}_{c}',plant='Q1',task=t,seed=s,condition=c) for t in ['L19','S19'] for s in [17,42,2026] for c in ['normal','authorized_changes','brief_offset','persistent_offset','hold','slow']]
        validate_population(rows)
        with self.assertRaises(ValueError):validate_population(rows[:-1]+[rows[0]])
    def test_strict_threshold_and_warmup(self):
        np.testing.assert_array_equal(decisions([2.,1.,1.0001,.9],start=1),[False,False,True,False])
        with self.assertRaises(ValueError):decisions([np.nan])
    def test_miss_not_clearance_success(self):
        a=np.zeros(300,bool);y=a.copy();y[110:120]=True;s=np.zeros((300,4))
        r=evaluate(a,y,s,s,np.ones(4),dict(warmup=100,return_tolerance=.1,dwell=10,recovery_horizon=250))
        self.assertFalse(r['overlap']);self.assertFalse(r['clear_timely']);self.assertIsNone(r['detection_delay'])
    def test_sustained_alarm_not_fresh(self):
        a=np.ones(300,bool);a[:100]=False;y=np.zeros(300,bool);y[110:120]=True;s=np.zeros((300,4))
        r=evaluate(a,y,s,s,np.ones(4),dict(warmup=100,return_tolerance=.1,dwell=10,recovery_horizon=250))
        self.assertTrue(r['overlap']);self.assertFalse(r['fresh'])
    def test_quarters_and_ap(self):
        y=np.array([False,True,True,True,True,False]);s=np.ones((6,4));z=np.zeros_like(s)
        r=quarters(np.arange(6.),np.arange(6)>2,y,s,z,np.ones(4))
        self.assertEqual(r['quarter_points'],1);self.assertEqual(r['first']['outside_inactive'],1);self.assertEqual(r['last']['outside_inactive'],0)
        self.assertEqual(average_precision([1,0],[.2,.2]),.5)
    def test_author_forward_prefix_is_causal(self):
        import torch
        from rapt import RaptConfig,RaptModel,NormStats,SequenceData,score_sequence
        torch.set_num_threads(1);torch.manual_seed(17)
        cfg=RaptConfig(obs_dim=4,action_dim=4,train_dynamics=True,embed_dim=16,num_blocks=1,compression_ratio=.25)
        m=RaptModel(cfg);y=np.random.default_rng(17).normal(size=(30,4)).astype(np.float32);u=np.zeros_like(y)
        st=NormStats.from_data(SequenceData([y],[u]));a=score_sequence(m,st,y,u);b=score_sequence(m,st,y[:20],u[:20])
        np.testing.assert_allclose(a[:20],b,rtol=1e-6,atol=1e-6)

if __name__=='__main__':unittest.main()
