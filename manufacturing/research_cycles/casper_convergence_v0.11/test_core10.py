import unittest
import numpy as np
from core import batches,score_predictions,EarlyStop
from model10 import prepare_raw,make_model,predict,pack_weights,restore,aggregate,admit_epoch
import tempfile
from pathlib import Path

class SyntheticChecks(unittest.TestCase):
    def setUp(self):
        self.c=dict(median_width=20,common_history=755,raw_start=219,training_raw_stop=2219,gap_multiple=5.,fit_cpu_seconds_per_model=30,next_epoch_cost_factor=1.25)
        self.y=np.random.default_rng(17).normal(size=(4000,9));self.t=np.arange(4000,dtype=np.int64)*100
    def test_lineage(self):
        d=prepare_raw(self.y,self.t,2000,self.c)
        self.assertEqual(d['training_raw_indices'][0],993);self.assertEqual(d['development_raw_indices'][0],2993)
        self.assertEqual(d['training_raw_indices'][-1],2218)
    def test_development_cannot_change_training(self):
        a=prepare_raw(self.y,self.t,2000,self.c);self.y[2000:]+=1000;b=prepare_raw(self.y,self.t,2000,self.c)
        for key in ['mean','scale','training']:np.testing.assert_array_equal(a[key],b[key])
    def test_trailing_causality(self):
        a=prepare_raw(self.y,self.t,2000,self.c);self.y[1500:2000]+=999;b=prepare_raw(self.y,self.t,2000,self.c)
        # Undo changed training scaler before comparing the unaffected causal filter.
        x=a['training']*a['scale']+a['mean'];y=b['training']*b['scale']+b['mean']
        np.testing.assert_allclose(x[:1481],y[:1481],atol=5e-5)
    def test_gap_rejected(self):
        self.t[3000:]+=10000
        with self.assertRaises(ValueError):prepare_raw(self.y,self.t,2000,self.c)
    def test_nonpositive_clock_rejected(self):
        self.t[100]=self.t[99]
        with self.assertRaises(ValueError):prepare_raw(self.y,self.t,2000,self.c)
    def test_constant_training_rejected(self):
        self.y[:2000,2]=3.
        with self.assertRaises(ValueError):prepare_raw(self.y,self.t,2000,self.c)
    def test_nonfinite_rejected(self):
        self.y[3,0]=np.nan
        with self.assertRaises(ValueError):prepare_raw(self.y,self.t,2000,self.c)
    def test_batch_target_after_history(self):
        y=np.arange(2000*9).reshape(2000,9);ep=np.array([755,756,1000])
        xx,yy=next(batches(y,ep,755,3));np.testing.assert_array_equal(xx[0],y[:755]);np.testing.assert_array_equal(yy,y[ep])
    def test_aggregation_and_support(self):
        s=np.arange(2048,dtype=float);a=aggregate(s)
        self.assertEqual(len(a),1294);self.assertEqual(a[0],sum(s[:755]));self.assertEqual(a[-1],sum(s[-755:]))
    def test_nonfinite_score_rejected(self):
        s=np.ones(800);s[4]=np.nan
        with self.assertRaises(ValueError):aggregate(s)
    def test_native_score_formula(self):
        a,b,m=score_predictions(np.ones((2,9)),np.zeros((2,9)),np.arange(1,10))
        np.testing.assert_array_equal(a,[1,1]);np.testing.assert_allclose(b,np.sqrt(np.mean(np.arange(1,10)**2)))
    def test_budget_admission(self):
        self.assertTrue(admit_epoch(0,None,self.c));self.assertTrue(admit_epoch(5,4,self.c));self.assertFalse(admit_epoch(27,4,self.c))
    def test_earliest_checkpoint_and_patience(self):
        s=EarlyStop(2,1e-6);self.assertEqual(s.observe(1,1.),(True,False));self.assertEqual(s.observe(2,1.),(False,False));self.assertEqual(s.observe(3,1.1),(False,True));self.assertEqual(s.best_epoch,1)
    def test_architectures_and_weight_parity(self):
        import tensorflow as tf
        for kind,history,parameters in [('casper_cnn',755,39977),('edge_cnn',45,1369)]:
            tf.keras.backend.clear_session();model=make_model(kind,17);self.assertEqual(model.count_params(),parameters)
            x=np.random.default_rng(42).normal(size=(2,history,9)).astype('float32');y=np.ones((2,1,9),dtype='float32')
            model.train_on_batch(x,y);expected=model(x,training=False).numpy();self.assertEqual(expected.shape,(2,1,9));self.assertTrue(np.isfinite(expected).all())
            with tempfile.TemporaryDirectory() as d:
                p=Path(d)/'weights.npz';p.write_bytes(pack_weights(model));actual=restore(kind,p)(x,training=False).numpy()
                np.testing.assert_array_equal(expected,actual)

if __name__=='__main__':unittest.main()
