"""Synthetic unit fixtures only."""
import unittest
import numpy as np
from observers import *

class Synthetic(unittest.TestCase):
    def setUp(self):
        self.fit={'variance':[1e-5]*4,'jerk_density':[.01,.02]}
    def test_polynomial_endpoint_and_prediction(self):
        t=np.arange(100)*DT;y=np.column_stack([t*t,.1+t+.5*t*t,2*t,1+t])
        for family in ('coupled','uncoupled'):
            for w in (5,9):
                out,pred=estimate(y,self.fit,family,w)
                np.testing.assert_allclose(out[w:],y[w:],atol=1e-10)
                np.testing.assert_allclose(pred[w:-1],y[w+1:],atol=1e-10)
    def test_future_noninterference_all(self):
        y=np.random.default_rng(17).normal(size=(100,4));z=y.copy();z[60:]+=100
        for fam,settings in GRID.items():
            for s in settings:
                a,b=estimate(y,self.fit,fam,s);c,d=estimate(z,self.fit,fam,s)
                np.testing.assert_array_equal(a[:60],c[:60]);np.testing.assert_array_equal(b[:60],d[:60])
    def test_training_weights_immutable(self):
        y=np.random.default_rng(42).normal(size=(1000,4));f=fit_noise([y]);before=repr(f)
        for fam,ss in GRID.items():estimate(y*100,f,fam,ss[0])
        self.assertEqual(before,repr(f))
    def test_invalid(self):
        for y in (np.zeros((0,4)),np.zeros((10,3)),np.full((10,4),np.nan)):
            with self.assertRaises(ValueError):estimate(y,self.fit,'raw',0)
        with self.assertRaises(ValueError):fit_noise([np.zeros((20,4))])
    def test_coupling_control(self):
        y=np.zeros((20,4));y[-5:,2]=1
        a,_=estimate(y,self.fit,'coupled',5);b,_=estimate(y,self.fit,'uncoupled',5)
        self.assertGreater(abs(a[-1,0]),.001);self.assertEqual(b[-1,0],0.)
    def test_backward_mean(self):
        y=np.arange(80.).reshape(20,4);a,_=estimate(y,self.fit,'mean',5)
        np.testing.assert_allclose(a[4:],np.stack([y[i-4:i+1].mean(0) for i in range(4,20)]))

if __name__=='__main__':unittest.main()
