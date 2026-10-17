import unittest
import numpy as np
from io14 import Observation,residual13
from audit_core import infer,cusum,calibrate,alarm_scores,ROLES,specification
from evaluation import evaluate,average_precision,primary

class AuditTests(unittest.TestCase):
    def setUp(self):
        g=np.random.default_rng(914);self.y=g.normal(size=(260,4));self.u=g.normal(size=(260,4));self.v=np.ones(260,bool)
        beta=np.zeros((9,4));beta[:4]=np.eye(4)*.5;beta[4:8]=np.eye(4)*.1
        self.m={'base':dict(order=np.array(1),kind=np.array('arx'),radius=np.array(.5),mean=np.zeros(4),scale=np.ones(4),beta=beta)}
        x=g.normal(size=(160,20));e=g.normal(size=(160,4))*.01
        self.m['rbf']=residual13.fit(x,e,kind='rbf',count=8)
        self.m['linear']=residual13.fit(x,e,kind='linear')
        self.c=dict(warmup=100,return_tolerance=.1,dwell=10,recovery_horizon=250)

    def test_inference_causal(self):
        a=infer(Observation(self.y,self.u,self.v),self.m,1.,self.c)
        y=self.y.copy();u=self.u.copy();y[200:]+=20;u[200:]-=10
        b=infer(Observation(y,u,self.v),self.m,1.,self.c)
        for aa,bb in zip(a,b):np.testing.assert_allclose(aa[:200],bb[:200],rtol=1e-12,atol=1e-12)

    def test_reference_protection_and_following_ablation(self):
        a=infer(Observation(self.y,self.u,self.v),self.m,1.,self.c)[0]
        y=self.y.copy();y[150:]+=5
        b=infer(Observation(y,self.u,self.v),self.m,1.,self.c)[0]
        np.testing.assert_array_equal(a[:,:3],b[:,:3]);self.assertFalse(np.array_equal(a[151:,3],b[151:,3]))

    def test_restrict_interface(self):
        with self.assertRaises(TypeError):infer({'measurements':self.y,'attack':self.v},self.m,1.,self.c)

    def test_attack_schedule_not_accepted_in_settings(self):
        with self.assertRaises(ValueError):infer(Observation(self.y,self.u,self.v),self.m,1.,dict(self.c,onset=120))

    def test_immutable_artifacts(self):
        saved={role:{k:v.copy() for k,v in m.items()} for role,m in self.m.items()}
        infer(Observation(self.y,self.u,self.v),self.m,1.,self.c)
        for role,m in self.m.items():
            for k,v in m.items():np.testing.assert_array_equal(saved[role][k],v)

    def test_past_only_controls(self):
        r,_,_=infer(Observation(self.y,self.u,self.v),self.m,1.,self.c)
        np.testing.assert_array_equal(r[100:,5],self.y[99:-1])
        for t in [100,120,259]:np.testing.assert_allclose(r[t,6],self.y[t-21:t].mean(0))

    def test_cusum_by_hand(self):
        np.testing.assert_array_equal(cusum(np.array([0.,2.,4.,0.,0.]),1.,1),[0,1,4,3,2])

    def test_cusum_no_label_reset(self):
        s=np.zeros(160);s[110:140]=2
        c=cusum(s,1.);self.assertEqual(c[140],29.)

    def test_calibration_rank_ties(self):
        t,r=calibrate(np.arange(5500));self.assertEqual(r,5445);self.assertEqual(t,5444)
        t,_=calibrate(np.ones(5500));self.assertFalse(np.any(np.ones(10)>t))

    def test_calibration_nonfinite(self):
        with self.assertRaises(ValueError):calibrate([0,np.nan])

    def test_all_method_specifications(self):
        import json
        from io14 import HERE
        methods=json.loads((HERE/'config.json').read_text())['methods'];self.assertEqual(len(set(methods)),17)
        for name in methods:self.assertIn(specification(name)[0],ROLES)

    def test_unknown_not_admitted(self):
        v=self.v.copy();v[150]=False
        with self.assertRaises(ValueError):Observation(self.y,self.u,v)

    def test_strict_point_and_dwell(self):
        c=dict(self.c,methods=['base_point','base_dual','rbf_dual_nodwell'])
        s=np.zeros((260,8));s[150,0]=2;s[150,2]=2;s[149,0]=1
        e=np.zeros((260,7,4));a=alarm_scores(s,e,self.v,{r:1. for r in ROLES},c)
        self.assertFalse(a[149,0]);self.assertTrue(a[150,0]);self.assertFalse(a[151,0])
        self.assertTrue(a[159,1]);self.assertFalse(a[160,1]);self.assertFalse(a[151,2])

    def record(self,a,returned=150):
        attack=np.zeros(260,bool);attack[120:140]=True;state=np.zeros((260,4));truth=state.copy()
        state[120:returned,0]=1.
        return evaluate(a,attack,state,truth,np.ones(4),self.c)

    def test_clean_contingency(self):
        a=np.zeros(260,bool);a[120:140]=True;r=self.record(a)
        self.assertEqual((r['tp'],r['fp'],r['fn'],r['tn']),(20,0,0,140))

    def test_recovery_retention(self):
        a=np.zeros(260,bool);a[122:154]=True;r=self.record(a)
        self.assertEqual(r['physical_return'],150);self.assertAlmostEqual(r['clear_delay'],.08)
        self.assertFalse(r['premature']);self.assertEqual(r['gap_points'],0)

    def test_premature_and_already_clear(self):
        a=np.zeros(260,bool);a[120:145]=True;r=self.record(a)
        self.assertTrue(r['premature']);self.assertTrue(r['already_clear_at_return']);self.assertEqual(r['gap_points'],5)

    def test_fall_at_return_not_premature(self):
        a=np.zeros(260,bool);a[120:150]=True;self.assertFalse(self.record(a)['premature'])

    def test_missed_event_retained(self):
        r=self.record(np.zeros(260,bool));self.assertFalse(r['overlap']);self.assertFalse(r['returned_detected'])
        self.assertIsNone(r['clear_delay']);self.assertEqual(r['physical_return'],150)

    def test_preexisting_alarm_not_fresh(self):
        a=np.zeros(260,bool);a[110:160]=True;r=self.record(a)
        self.assertTrue(r['overlap']);self.assertFalse(r['fresh']);self.assertEqual(r['detection_delay'],0.)

    def test_absent_return_censored(self):
        a=np.zeros(260,bool);a[120:200]=True;r=self.record(a,260)
        self.assertTrue(r['return_missing']);self.assertFalse(r['clear_timely']);self.assertTrue(r['premature'])

    def test_recovery_dwell(self):
        a=np.zeros(260,bool);a[120:155]=True;attack=np.zeros(260,bool);attack[120:140]=True
        state=np.zeros((260,4));state[120:150]=1;state[154:158]=1
        r=evaluate(a,attack,state,np.zeros_like(state),np.ones(4),self.c);self.assertEqual(r['physical_return'],158)

    def test_ap_tie_and_perfect(self):
        self.assertEqual(average_precision([0,1],[1,1]),.5)
        self.assertEqual(average_precision([0,1],[0,1]),1.)
        self.assertIsNone(average_precision([0,0],[0,1]))

    def test_ap_independent_reference(self):
        from mfg_twin.metrics import average_precision as reference
        y=[0,1,0,1,1,0];s=[1.,2.,2.,4.,3.,0.]
        self.assertAlmostEqual(average_precision(y,s),reference(y,s))

    def test_primary_requires_every_plant(self):
        c=dict(primary_candidate='a',primary_control='b',benefit_fraction=.1)
        rows=[]
        for p in ['Q1','Q2','Q3','pooled']:
            for m in ['a','b']:rows.append(dict(stratum=p,method=m,hits=10,fresh_hits=8,clear_timely=10,premature=0,benign_alarms=50 if m=='a' else 100,gap_points=0))
        self.assertTrue(primary(rows,c)['passed']);rows[0]['hits']=9;self.assertFalse(primary(rows,c)['passed'])

    def test_zero_benefit_denominator(self):
        c=dict(primary_candidate='a',primary_control='b',benefit_fraction=.1)
        rows=[dict(stratum=p,method=m,hits=1,fresh_hits=1,clear_timely=1,premature=0,benign_alarms=0,gap_points=0) for p in ['Q1','Q2','Q3','pooled'] for m in ['a','b']]
        self.assertFalse(primary(rows,c)['passed'])

if __name__=='__main__':unittest.main()
