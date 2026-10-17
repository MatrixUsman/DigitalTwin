import unittest
import numpy as np
from common import config,permitted
from mechanism import features,fit_reference,reference,scalar,bounds,latch,known_context,decide,calibrate
from simulation import commands,path,plant_parameters
from v7_core import physical,lag_derivative
from scipy.integrate import solve_ivp

class MechanismTests(unittest.TestCase):
    def setUp(self):self.c=config()
    def test_future_exclusion(self):
        z=np.arange(240.).reshape(60,4);u=z/100;x,t=features(z,u)
        z2=z.copy();z2[40:]+=1000;x2,_=features(z2,u)
        np.testing.assert_array_equal(x[t<=40],x2[t<=40])
    def test_fit_and_free_reference(self):
        rng=np.random.default_rng(3);eps=[]
        for i in range(3):
            u=rng.normal(size=(300,4));y=np.zeros_like(u)
            for t in range(1,len(y)):y[t]=.7*y[t-1]+.2*u[t-1]
            eps.append(dict(measurements=y,available=u))
        fit=fit_reference(eps,warmup=20);pred=reference(eps[0]['measurements'],eps[0]['available'],fit)
        self.assertLess(np.max(np.abs(pred[10:]-eps[0]['measurements'][10:])),1e-3)
        y=eps[0]['measurements'].copy();y[30:]+=100
        np.testing.assert_array_equal(reference(y,eps[0]['available'],fit),pred)
    def test_bad_channels(self):
        with self.assertRaises(ValueError):fit_reference([dict(measurements=np.ones((200,4)),available=np.ones((200,4)))])
    def test_conditional_bounds(self):
        rng=np.random.default_rng(17)
        for _ in range(100):
            x=rng.normal(size=4);z=rng.normal(size=4);r=rng.normal(size=4);n=rng.normal(size=4)
            d=np.max(np.abs(x-z));lo,hi=bounds(np.max(np.abs(x+n-r)),np.max(np.abs(z-r)),np.max(np.abs(n)))
            self.assertLessEqual(lo,d+1e-12);self.assertGreaterEqual(hi+1e-12,d)
    def test_unknown_cannot_become_clean(self):
        np.testing.assert_array_equal(known_context(np.array([1,1,0,1],bool)),[1,1,0,0])
        np.testing.assert_array_equal(latch(np.array([2.,0,0,0]),np.array([1,1,0,0]),1,2),[1,1,1,1])
    def test_dwell_exact(self):
        np.testing.assert_array_equal(latch(np.array([2.,0,0,0]),np.ones(4,bool),1,3),[1,1,1,0])
    def test_entry_priority(self):
        np.testing.assert_array_equal(latch(np.array([2.,2,0,0]),np.ones(4,bool),1,2,np.ones(4,bool)),[1,1,1,0])
    def test_margin_is_recovery_cost(self):
        c=self.c;er=np.r_[2.,np.full(25,.07)];s=np.tile(er[:,None],(1,13));e=dict(scores=s,valid=np.ones(len(er),bool),learned_error=er,nominal_error=er)
        a,_=decide(e,9,1.,.04,c);b,_=decide(e,11,1.,.04,c)
        self.assertTrue(a[-1]);self.assertFalse(b[-1])
    def test_calibration_minimal(self):
        c=dict(self.c,warmup=0);rng=np.random.default_rng(42);eps=[]
        for i in range(2):
            x=rng.uniform(0,1,200);eps.append(dict(scores=np.tile(x[:,None],(1,13)),valid=np.ones(200,bool),learned_error=x,nominal_error=x))
        for j in [0,7,9]:
            r=calibrate(eps,j,.01,c);self.assertLessEqual(r['alarms'],4);self.assertGreater(r['preceding'],4)
    def test_context_truth_separation(self):
        task=self.c['tasks8'][0];auth=commands(self.c,task,'authorized_offset');bad=commands(self.c,task,'persistent_offset')
        np.testing.assert_array_equal(auth['executed'],bad['executed'])
        self.assertFalse(auth['attack'].any());self.assertTrue(bad['attack'].any());self.assertFalse(np.array_equal(auth['approved'],bad['approved']))
    def test_new_conditions(self):
        self.assertEqual(len(self.c['tasks8'])*len(self.c['plants8'])*len(self.c['seeds'])*len(self.c['conditions']),216)
        self.assertEqual(len(self.c['methods8']),13)
    def test_command_derivative(self):
        t=np.arange(100)*.02+.3
        for task in self.c['tasks8']:
            v=(path(t+1e-6,np.ones(100),task)[:,:2]-path(t-1e-6,np.ones(100),task)[:,:2])/2e-6
            np.testing.assert_allclose(v,path(t,np.ones(100),task)[:,2:],atol=1e-9)
    def test_independent_integrator(self):
        c=self.c;p=plant_parameters(c,c['plants8'][1]);setting=permitted(c);u=np.array([.1,.15,0.,0.]);commands_=np.tile(u,(20,1));initial=np.array([.02,.03,0.,0.])
        rk=physical(initial,commands_,p,setting,.03);y0=np.r_[initial,0.,0.]
        other=solve_ivp(lambda t,x:lag_derivative(x,u,p,setting,.03),(0,19*c['dt']),y0,t_eval=np.arange(20)*c['dt'],rtol=1e-10,atol=1e-12).y.T
        np.testing.assert_allclose(rk,other,atol=2e-6,rtol=2e-5)
    def test_truth_changes_without_detector_input(self):
        e=dict(scores=np.ones((30,13)),valid=np.ones(30,bool),learned_error=np.ones(30),nominal_error=np.ones(30))
        a=decide(e,9,.5,.01,self.c)
        e['truth_reference']=np.full((30,4),1e20);e['attack']=np.ones(30)
        b=decide(e,9,.5,.01,self.c)
        np.testing.assert_array_equal(a[0],b[0]);np.testing.assert_array_equal(a[1],b[1])

if __name__=='__main__':unittest.main(verbosity=2)
