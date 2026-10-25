from pathlib import Path
import sys
import unittest
from types import SimpleNamespace
import numpy as np
import torch
H=Path(__file__).resolve().parent;P=H.parents[2]
sys.path.insert(0,str(P/'baselines/vendor/rapt_v020'))
from core import decompose,region_stats,interval
from rapt.detector import score_sequence

class Stats:
    def normalize(self,x):return (x-2.)/3.

class FakeModel:
    cfg=SimpleNamespace(train_dynamics=True,obs_dim=2)
    def eval(self):return self
    def to(self,device):return self
    def __call__(self,x):
        # Known preceding observation and preceding action; cumulative history
        # is causal and makes future/prefix errors observable in the fixture.
        mean=.4*x[...,:2]+.2*x[...,2:]+.01*torch.cumsum(x[...,:2],dim=1)
        return mean,torch.zeros_like(mean)+.7,None

class SyntheticTests(unittest.TestCase):
    def setUp(self):
        self.y=np.arange(240,dtype=np.float32).reshape(120,2)/11
        self.u=np.arange(240,dtype=np.float32).reshape(120,2)/31
    def test_exact_upstream_score_parity(self):
        a=decompose(FakeModel(),Stats(),self.y,self.u)
        np.testing.assert_array_equal(a['loss'],score_sequence(FakeModel(),Stats(),self.y,self.u))
    def test_transition_alignment_and_padding(self):
        a=decompose(FakeModel(),Stats(),self.y,self.u)
        z=Stats().normalize(self.y)
        np.testing.assert_allclose(a['mean'][1],.41*z[0]+.2*self.u[0],rtol=1e-6)
        self.assertFalse(a['defined'][0]);self.assertTrue(a['defined'][1]);self.assertEqual(int(a['eligible'].sum()),20)
    def test_causal_prefix(self):
        a=decompose(FakeModel(),Stats(),self.y,self.u)
        yy=self.y.copy();yy[60:]+=100
        b=decompose(FakeModel(),Stats(),yy,self.u)
        np.testing.assert_array_equal(a['mean'][:61],b['mean'][:61])
        np.testing.assert_array_equal(a['loss'][:60],b['loss'][:60])
    def test_log_decomposition(self):
        a=decompose(FakeModel(),Stats(),self.y,self.u)
        s=region_stats(a,100,120)
        for c in s['channels']:
            d=c['log_decomposition'];self.assertLess(abs(d['mean_log_score']-d['mean_log_squared_error']+d['mean_log_variance']),2e-5)
    def test_zero_error_reporting(self):
        a={k:np.zeros((120,2),np.float32) for k in ['mean','logvar','squared_error','loss']}
        self.assertEqual(region_stats(a,100,120)['channels'][0]['log_decomposition']['excluded_zero'],20)
    def test_all_condition_intervals(self):
        tasks={'L':dict(onset=503,brief=12,duration=530)}
        for c,end in [('brief_offset',515),('persistent_offset',1033),('hold',1033),('slow',1033)]:
            self.assertEqual(interval(dict(task='L',condition=c),tasks,2400)[:2],(503,end))
        self.assertEqual(interval(dict(task='L',condition='normal'),tasks,6000)[:2],(100,6000))

if __name__=='__main__':unittest.main()
