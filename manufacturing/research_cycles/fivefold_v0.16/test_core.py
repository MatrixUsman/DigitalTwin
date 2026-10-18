"""Explicitly synthetic software fixtures, never benchmark measurements."""
import unittest
import numpy as np
from core import arx, bounds, cut, fit_pair, score_pair, metrics

class TemporalTests(unittest.TestCase):
    @staticmethod
    def episode():
        rng=np.random.default_rng(112)
        u=rng.normal(size=(1200,4)); y=np.zeros((1200,4))
        for t in range(1,len(y)):y[t]=.55*y[t-1]+.2*u[t-1]+rng.normal(0,.01,4)
        return arx.Observation(y,u,np.ones(1200,dtype=bool))
    def test_all_folds_and_coverage(self):
        seen=[]
        for k in range(1,6):
            b=bounds(k)
            self.assertEqual(b['train'][1],b['validation'][0])
            self.assertGreaterEqual(b['scored'][0]-b['train'][1],100)
            seen.extend(range(*b['scored']))
        self.assertEqual(len(seen),500)
        self.assertEqual(len(set(seen)),500)
    def test_invalid_folds(self):
        for k in [0,6,True,1.5]:
            with self.assertRaises(ValueError):bounds(k)
    def test_future_cannot_change_fitted_parameters(self):
        e=self.episode(); b=bounds(2)
        y=e.measurements.copy();y[400:]+=1000
        altered=arx.Observation(y,e.commands,e.valid)
        pair=fit_pair([cut(e,b['train'])],'Q1')
        other=fit_pair([cut(altered,b['train'])],'Q1')
        for a,c in zip(pair,other):
            for key in a:np.testing.assert_array_equal(a[key],c[key])
    def test_prediction_alignment_and_future_isolation(self):
        e=self.episode();b=bounds(2);base,head=fit_pair([cut(e,b['train'])],'Q1')
        val=cut(e,b['validation']);native,standard=score_pair(val,base,head)
        self.assertEqual(native.shape,(100,2,4))
        np.testing.assert_allclose(native/base['scale'],standard)
        y=val.measurements.copy();y[100:]+=7
        moved=arx.Observation(y,val.commands,val.valid)
        n2,_=score_pair(moved,base,head)
        np.testing.assert_allclose(n2,native-7,atol=1e-12)
        self.assertEqual(metrics(native,standard)['targets'],100)
    def test_nonfinite_rejected(self):
        e=self.episode();y=e.measurements.copy();y[0,0]=np.nan
        with self.assertRaises(ValueError):arx.Observation(y,e.commands,e.valid)

if __name__=='__main__':unittest.main()
