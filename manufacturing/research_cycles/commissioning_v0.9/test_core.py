import unittest
from unittest.mock import patch
from types import SimpleNamespace
import numpy as np
from common9 import bank,config,normal_catalog
from models import Observation,fit,predict,select,design
from metrics9 import errors,opportunities
from normal_io import NormalReader


def fixture(seed=2,n=220):
    rng=np.random.default_rng(seed);u=rng.normal(size=(n,4));y=np.zeros_like(u)
    for t in range(1,n):y[t]=.75*y[t-1]+.2*u[t-1]+rng.normal(scale=.001,size=4)
    return Observation(y,u,np.ones(n,bool))

class Tests(unittest.TestCase):
    def setUp(self):self.e=fixture();self.spec=dict(kind='arx',order=4,ridge=1e-7);self.f=fit([self.e],self.spec,100)
    def test_original_fit_parity(self):
        from mechanism import fit_reference
        old=fit_reference([dict(measurements=self.e.measurements,available=self.e.commands)],4,1e-7,100)
        for key in ['mean','scale','beta','radius']:np.testing.assert_array_equal(self.f[key],old[key])
    def test_train_only_scaler(self):
        np.testing.assert_array_equal(self.f['mean'],self.e.measurements[100:].mean(0));np.testing.assert_array_equal(self.f['scale'],self.e.measurements[100:].std(0))
    def test_prediction_cannot_mutate_fit(self):
        before={k:v.copy() for k,v in self.f.items()};predict(fixture(8),self.f,100)
        for k,v in before.items():np.testing.assert_array_equal(v,self.f[k])
    def test_no_postprefix_measurement_effect(self):
        y=self.e.measurements.copy();y[100:]+=1000;other=Observation(y,self.e.commands,self.e.valid)
        np.testing.assert_array_equal(predict(self.e,self.f,100),predict(other,self.f,100))
    def test_future_command_causality(self):
        u=self.e.commands.copy();u[170:]+=100;other=Observation(self.e.measurements,u,self.e.valid)
        np.testing.assert_array_equal(predict(self.e,self.f,100)[:171],predict(other,self.f,100)[:171])
    def test_fir_no_measurement_feedback(self):
        f=fit([self.e],dict(kind='fir',order=16,ridge=1e-5),100);y=self.e.measurements.copy();y[100:]-=200
        np.testing.assert_array_equal(predict(self.e,f,100)[100:],predict(Observation(y,self.e.commands,self.e.valid),f,100)[100:])
    def test_fir_causal(self):
        f=fit([self.e],dict(kind='fir',order=16,ridge=1e-5),100);u=self.e.commands.copy();u[160:]=1e4
        np.testing.assert_array_equal(predict(self.e,f,100)[:161],predict(Observation(self.e.measurements,u,self.e.valid),f,100)[:161])
    def test_lag_order(self):
        y=np.arange(24.).reshape(6,4);u=-y;x,t=design(y,u,'arx',2,2)
        np.testing.assert_array_equal(x[0],np.r_[y[:2].ravel(),u[:2].ravel(),1]);np.testing.assert_array_equal(t[0],y[2])
    def test_episode_boundaries(self):
        a=fixture(1);b=fixture(2);f=fit([a,b],self.spec,100);self.assertEqual(int(f['training_targets']),240)
    def test_restricted_observation(self):
        with self.assertRaises((AttributeError,TypeError)):self.e.true_state=np.zeros((220,4))
        self.assertFalse(hasattr(self.e,'true_state'))
        with self.assertRaises(ValueError):self.e.measurements[0,0]=1
    def test_nonfinite(self):
        y=self.e.measurements.copy();y[0,0]=np.nan
        with self.assertRaises(ValueError):Observation(y,self.e.commands,self.e.valid)
    def test_missing_context(self):
        v=self.e.valid.copy();v[20]=False
        with self.assertRaises(ValueError):Observation(self.e.measurements,self.e.commands,v)
    def test_constant_channel(self):
        y=self.e.measurements.copy();y[:,0]=1
        with self.assertRaises(ValueError):fit([Observation(y,self.e.commands,self.e.valid)],self.spec,100)
    def test_unstable_rejected(self):
        self.f['radius']=np.array(1.)
        with self.assertRaises(ValueError):predict(self.e,self.f,100)
    def test_stage_allowlist(self):
        c=config();r=NormalReader(c,{})
        for name,stage in [('eval_E_Q1_17_normal.npz','train'),('train_Q1_0.npz','allowance')]:
            with self.assertRaises(ValueError):r.read(name,stage)
    def test_splits_disjoint(self):
        c=config();rows=normal_catalog(c);self.assertEqual(len(rows),66);self.assertEqual(len({r['name'] for r in rows}),66)
        c['allowance_indices']=[0]
        with self.assertRaises(ValueError):normal_catalog(c)
    def test_selection_rule(self):
        rows=[dict(id='a',kind='arx',status='eligible',worst_development_q99=2,mean_development_rmse=1,parameter_count=4),dict(id='b',kind='fir',status='eligible',worst_development_q99=1,mean_development_rmse=2,parameter_count=9)]
        self.assertEqual(select(rows),'b');self.assertEqual(select(rows,'arx'),'a')
    def test_infeasible_allowance(self):
        c=config();r=opportunities(np.zeros(1200),.11,c);self.assertFalse(r['algebraically_feasible']);self.assertEqual(r['cleared_probes'],0)
    def test_exact_dwell(self):
        c=config();r=opportunities(np.zeros(1200),0,c);self.assertEqual([v['delay_steps'] for v in r['probes']],[9]*4)
    def test_strict_b_admission_and_inclusive_error(self):
        c=config();r=opportunities(np.zeros(1200),.1,c);self.assertFalse(r['algebraically_feasible']);self.assertEqual(r['cleared_probes'],4)
    def test_dwell_reset_and_deadline(self):
        c=config();s=np.ones(1200);s[100:109]=0;s[110:120]=0
        r=opportunities(s,0,c);self.assertEqual(r['probes'][0]['cleared_at'],119);self.assertIsNone(r['probes'][1]['cleared_at'])
    def test_metrics(self):
        y=np.zeros((120,4));p=y.copy();p[100:,2]=2;s,r=errors(y,p,np.ones(4),100);self.assertEqual(r['maximum'],2);self.assertEqual(r['standardized_rmse'],1)
    def test_finite_bank(self):self.assertEqual(len(bank(config())),21)

if __name__=='__main__':unittest.main(verbosity=2)
