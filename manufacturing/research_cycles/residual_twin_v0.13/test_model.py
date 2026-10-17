import unittest
import io
import numpy as np
from model import features, fit, correct, basis, return_evidence, alarm_machine


class ModelTests(unittest.TestCase):
    def setUp(self):
        g = np.random.default_rng(123)
        self.x = g.normal(size=(150, 20)); self.y = g.normal(size=(150, 4))*.02

    def test_linear_exact_training_solution(self):
        m = fit(self.x, self.y, kind='linear', ridge=.01)
        z = (self.x-self.x.mean(0))/self.x.std(0)
        a = np.column_stack([z,np.ones(len(z))]);pen=np.eye(21)*.01;pen[-1,-1]=0
        expected=np.linalg.solve(a.T@a/150+pen,a.T@self.y/150)
        np.testing.assert_allclose(m['beta'],expected,rtol=1e-12,atol=1e-14)

    def test_determinism(self):
        a=fit(self.x,self.y,kind='rbf',count=16);b=fit(self.x,self.y,kind='rbf',count=16)
        for k in a:np.testing.assert_array_equal(a[k],b[k])

    def test_fitted_arrays_readonly(self):
        m=fit(self.x,self.y,kind='rbf',count=16)
        self.assertTrue(all(not v.flags.writeable for v in m.values()))

    def test_training_only_and_no_mutation(self):
        x=self.x.copy();y=self.y.copy();m=fit(x,y,kind='rbf',count=16)
        saved={k:v.copy() for k,v in m.items()};basis(np.ones((10,20))*999,m)
        for k in m:np.testing.assert_array_equal(saved[k],m[k])
        np.testing.assert_array_equal(x,self.x);np.testing.assert_array_equal(y,self.y)

    def test_constant_features(self):
        x=self.x.copy();x[:,3]=4
        m=fit(x,self.y,kind='rbf',count=16)
        self.assertEqual(m['feature_scale'][3],1.)
        self.assertTrue(np.isfinite(basis(x,m)).all())

    def test_invalid_fit(self):
        for bad in [np.nan,np.inf]:
            x=self.x.copy();x[0,0]=bad
            with self.assertRaises(ValueError):fit(x,self.y,kind='linear')
        with self.assertRaises(ValueError):fit(self.x,self.y,kind='rbf',count=151)
        with self.assertRaises(ValueError):fit(self.x,self.y,kind='linear',ridge=0)

    def test_save_reload(self):
        a=fit(self.x,self.y,kind='rbf',count=16);stream=io.BytesIO();np.savez(stream,**a);stream.seek(0)
        with np.load(stream,allow_pickle=False) as z:b={k:z[k] for k in z.files}
        np.testing.assert_array_equal(basis(self.x,a)@a['beta'],basis(self.x,b)@b['beta'])

    def test_causal_correction(self):
        g=np.random.default_rng(9);r=g.normal(size=(230,4));u=g.normal(size=(230,4))
        x=features(r,u);m=fit(x,g.normal(size=(130,4))*.01,kind='rbf',count=16)
        original=correct(r,u,m,np.ones(4));u2=u.copy();u2[190:]+=100;r2=r.copy();r2[190:]-=100
        changed=correct(r2,u2,m,np.ones(4))
        np.testing.assert_array_equal(original[:190],changed[:190])
        np.testing.assert_array_equal(original[:100],r[:100])

    def test_no_live_measurement_argument(self):
        import inspect
        self.assertNotIn('measurements',inspect.signature(correct).parameters)
        self.assertNotIn('truth',inspect.signature(correct).parameters)

    def test_complete_reference_ignores_later_measurements(self):
        import sys
        from io13 import OLD
        sys.path.insert(0,str(OLD))
        from models import Observation,predict
        g=np.random.default_rng(63);y=g.normal(size=(230,4));u=g.normal(size=(230,4))
        beta=np.zeros((9,4));beta[:4]=np.eye(4)*.5;beta[4:8]=np.eye(4)*.1
        base=dict(order=np.array(1),kind=np.array('arx'),radius=np.array(.5),
                  mean=np.zeros(4),scale=np.ones(4),beta=beta)
        a=predict(Observation(y,u,np.ones(230,bool)),base,100)
        m=fit(features(a,u),g.normal(size=(130,4))*.01,kind='rbf',count=16)
        y2=y.copy();y2[100:]+=999
        b=predict(Observation(y2,u,np.ones(230,bool)),base,100)
        np.testing.assert_array_equal(a,b)
        np.testing.assert_array_equal(correct(a,u,m,np.ones(4)),correct(b,u,m,np.ones(4)))

    def test_bound(self):
        m=fit(self.x,self.y,kind='rbf',count=16);z=basis(self.x*100,m)
        self.assertTrue(np.all((z[:,:-1]>=0)&(z[:,:-1]<=1)))
        self.assertTrue(np.all(np.abs(z@m['beta'])<=np.sum(np.abs(m['beta']),axis=0)+1e-15))

    def test_return_window_and_future(self):
        e=np.zeros((180,4));v=np.ones(180,bool)
        a,k=return_evidence(e,v);self.assertFalse(a[:140].any());self.assertTrue(a[140:].all())
        e[160:]=5;b,_=return_evidence(e,v)
        np.testing.assert_array_equal(a[:160],b[:160]);self.assertFalse(b[160:].any())

    def test_short_window_prevents_long_average_mask(self):
        e=np.zeros((180,4));e[170:175]=.5;v=np.ones(180,bool)
        long,_=return_evidence(e,v,windows=(41,));dual,_=return_evidence(e,v)
        self.assertTrue(long[174]);self.assertFalse(dual[174])

    def test_running_sum_matches_direct_window_means(self):
        g=np.random.default_rng(37);e=g.normal(size=(600,4))*.12;valid=np.ones(600,bool)
        actual,_=return_evidence(e,valid)
        direct=np.array([t>=140 and all(np.max(np.abs(e[t-w+1:t+1].mean(0)))<=.1
                          for w in (5,41)) for t in range(600)])
        np.testing.assert_array_equal(actual,direct)

    def test_missing_context_abstains(self):
        e=np.zeros((180,4));v=np.ones(180,bool);v[150]=False
        ok,known=return_evidence(e,v)
        self.assertFalse(known[150:].any());self.assertFalse(ok[150:].any())

    def test_nonfinite_valid_rejected(self):
        e=np.zeros((180,4));e[150,0]=np.nan
        with self.assertRaises(ValueError):return_evidence(e,np.ones(180,bool))

    def test_alarm_entry_priority_and_dwell(self):
        s=np.zeros(20);s[0]=2;s[5]=2;k=np.ones(20,bool);e=k.copy()
        a=alarm_machine(s,k,e,1.,dwell=3)
        self.assertTrue(a[0]);self.assertTrue(a[2]);self.assertFalse(a[3])
        self.assertTrue(a[5]);self.assertFalse(a[8])
        s[0]=1.;self.assertFalse(alarm_machine(s[:4],k[:4],e[:4],1.).any())

    def test_unknown_preserves_active_alarm(self):
        s=np.zeros(20);s[0]=2;k=np.ones(20,bool);k[1:]=False
        self.assertTrue(alarm_machine(s,k,np.ones(20,bool),1.).all())


if __name__=='__main__':unittest.main()
