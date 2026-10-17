"""Explicitly synthetic fixtures; no saved observations are read."""
import inspect
import json
import unittest
import numpy as np
from support import config,roster,scaled_plant
from core import (envelope_score,stateful,decision,calibrate,command_mode,trajectory,
                  following_predictions,components,score_matrix)
from plant import advance,mass
from metrics import evaluate,aggregate

class Tests(unittest.TestCase):
    def setUp(self): self.c=config()

    def test_envelope_zero_inside(self):
        b=np.tile(np.array([-1.,0.,1.])[None,:,None],(20,1,4))
        np.testing.assert_array_equal(envelope_score(np.zeros((20,4)),b,np.ones(4)),0)

    def test_envelope_outside_distance(self):
        b=np.tile(np.array([-1.,0.,1.])[None,:,None],(2,1,4)); y=np.zeros((2,4)); y[0,2]=3
        np.testing.assert_array_equal(envelope_score(y,b,[1,1,2,1]),[1,0])

    def test_envelope_bad_data(self):
        with self.assertRaises(ValueError): envelope_score(np.full((2,4),np.nan),np.zeros((2,3,4)),[1]*4)

    def test_separate_recovery_not_envelope_hysteresis(self):
        s=np.r_[2.,np.zeros(12)]; ok=np.ones(13,dtype=bool)
        h=stateful(s,ok,1,3); c=stateful(s,ok,1,3,np.zeros(13,dtype=bool))
        self.assertFalse(h[-1]); self.assertTrue(c[-1])

    def test_fixed_return_dwell(self):
        a=stateful(np.array([2,0,0,0.]),np.ones(4,dtype=bool),1,3,np.ones(4,dtype=bool))
        np.testing.assert_array_equal(a,[True,True,True,False])

    def test_entry_priority(self):
        a=stateful(np.ones(10)*2,np.ones(10,dtype=bool),1,1,np.ones(10,dtype=bool))
        self.assertTrue(a.all())

    def test_unknown_holds_and_resets(self):
        a=stateful(np.array([2,0,0,0,0.]),np.array([1,1,0,1,1],dtype=bool),1,2,np.ones(5,dtype=bool))
        np.testing.assert_array_equal(a,[1,1,1,1,0])

    def test_unknown_not_counted_positive(self):
        a,u=decision(np.ones(4)*2,12,np.zeros(4,dtype=bool),np.ones(4,dtype=bool),1,self.c)
        self.assertEqual(np.count_nonzero(a&~u),0); self.assertTrue(u.all())

    def test_contextfree_still_known(self):
        _,u=decision(np.ones(4),0,np.zeros(4,dtype=bool),np.ones(4,dtype=bool),1,self.c)
        self.assertFalse(u.any())

    def test_monotonic_stateful_thresholds(self):
        rng=np.random.default_rng(77)
        for _ in range(30):
            s=rng.uniform(0,4,100);v=rng.random(100)>.1;r=rng.random(100)>.3
            for recovery in [None,r]:
                counts=[stateful(s,v,h,3,recovery).sum() for h in np.linspace(0,4,25)]
                self.assertTrue(np.all(np.diff(counts)<=0))

    def test_calibration_exact_exhaustive(self):
        rng=np.random.default_rng(8); c=dict(self.c,warmup=2,recovery_dwell=3,calibration_alarm_budget=12)
        eps=[dict(scores=rng.uniform(0,3,(40,13)),valid=np.ones(40,dtype=bool),return_ok=rng.random(40)>.2) for _ in range(3)]
        for j in range(13):
            got=calibrate(eps,j,c)
            grid=np.unique(np.r_[0,np.concatenate([e['scores'][:,j] for e in eps])])
            expected=next(h for h in grid if sum(decision(e['scores'][:,j],j,e['valid'],e['return_ok'],h,c)[0][2:].sum() for e in eps)<=12)
            self.assertEqual(got['threshold'],expected)

    def test_strict_entry_and_zero_scores(self):
        c=dict(self.c,warmup=0,calibration_alarm_budget=0)
        e=dict(scores=np.zeros((20,13)),valid=np.ones(20,dtype=bool),return_ok=np.ones(20,dtype=bool))
        for j in range(13): self.assertEqual(calibrate([e],j,c)['threshold'],0)

    def test_warmup_carryover_in_calibration(self):
        c=dict(self.c,warmup=1,recovery_dwell=10,calibration_alarm_budget=0)
        s=np.zeros((20,13));s[0,:]=2
        e=dict(scores=s,valid=np.ones(20,dtype=bool),return_ok=np.zeros(20,dtype=bool))
        self.assertEqual(calibrate([e],12,c)['threshold'],2)

    def test_mode_causal(self):
        u=np.zeros((100,4)); u[40:,0]=.2;v=np.ones(100,dtype=bool)
        m=command_mode(u,v,self.c); u[60:]=7
        np.testing.assert_array_equal(m[:60],command_mode(u,v,self.c)[:60])
        self.assertEqual(m[40],1);self.assertEqual(m[89],1);self.assertEqual(m[90],0)

    def test_missing_context_not_mode_label(self):
        u=np.zeros((20,4));u[10:,0]=1;v=np.ones(20,dtype=bool);v[10]=False
        self.assertFalse(command_mode(u,v,self.c).any())

    def test_same_physics_no_duplicate_equations(self):
        c=dict(self.c,steps=8);u=np.zeros((8,4));x=np.array([.1,.2,0.,0.]);p=c['nominal']
        states=trajectory(x,u,p,c)
        np.testing.assert_array_equal(states[1],advance(x,u[0],p,c))

    def test_observer_is_prospective(self):
        c=dict(self.c,steps=8);u=np.zeros((8,4));y=np.zeros((8,4));a=following_predictions(y,u,c)
        y[5]=.01;b=following_predictions(y,u,c)
        np.testing.assert_array_equal(a[:6],b[:6]); self.assertFalse(np.array_equal(a[6],b[6]))

    def test_mass_positive(self):
        for factors in self.c['bank']:
            for q in [-np.pi,0,np.pi/2]:
                self.assertTrue(np.all(np.linalg.eigvalsh(mass([0,q],scaled_plant(self.c,*factors)))>0))

    def test_no_label_argument(self):
        self.assertEqual(list(inspect.signature(components).parameters),['y','context','valid','following','bank','fit','cfg'])

    def test_score_roster(self):
        c=dict(base=np.ones((5,8)),envelope=np.ones(5)*2,mode=np.array([0,1,0,1,0]))
        s=score_matrix(c,np.array([1,2.]));self.assertEqual(s.shape,(5,13));self.assertEqual(s[1,8],.5)

    def test_fresh_roster(self):
        r=roster(self.c);self.assertEqual(len(r),144);self.assertEqual(len({i['id'] for i in r}),144)
        self.assertEqual(sum(i['stratum']=='within_range' for i in r),96)
        self.assertTrue(all(i['noise_seed']>=40000 for i in r))
        self.assertEqual(len({i['noise_seed'] for i in r}),18)

    def test_metrics_json_and_miss_preservation(self):
        n=1000; ep=dict(state=np.zeros((n,4)),reference=np.zeros((n,4)),attack=np.zeros(n,dtype=bool),authorized=np.zeros(n,dtype=bool))
        ep['attack'][325:525]=True
        row=evaluate(np.zeros(n,dtype=bool),np.zeros(n,dtype=bool),ep,dict(scale=np.ones(4)),self.c)
        json.dumps(row,allow_nan=False);self.assertEqual(row['fn'],200);self.assertFalse(row['overlap_hit'])
        self.assertIsNone(row['clear_delay_from_return_seconds'])

    def test_relatched_alarm_does_not_hide_premature_clear(self):
        n=1000;ep=dict(state=np.zeros((n,4)),reference=np.zeros((n,4)),attack=np.zeros(n,dtype=bool),authorized=np.zeros(n,dtype=bool))
        ep['attack'][325:525]=True;ep['state'][325:550]=1
        a=np.zeros(n,dtype=bool);a[326:400]=True;a[401:560]=True
        row=evaluate(a,np.zeros(n,dtype=bool),ep,dict(scale=np.ones(4)),self.c)
        self.assertTrue(row['premature_clear']);self.assertEqual(row['gap_before_return_points'],1)

if __name__=='__main__': unittest.main(verbosity=2)
