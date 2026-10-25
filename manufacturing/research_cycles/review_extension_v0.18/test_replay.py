"""Explicitly synthetic fixtures; no benchmark observations read."""
import unittest
import numpy as np
from common import model,evaluation
from core import replay,extra,runs,dist

class SyntheticTests(unittest.TestCase):
    def test_readiness_and_initial_prefix_excluded(self):
        e=np.zeros((160,4));e[:100]=1e6;s=np.zeros(160);s[100]=1
        a,ev=replay(s,e,np.ones(160,bool),.05)
        self.assertFalse(ev[139]);self.assertTrue(ev[140]);self.assertTrue(a[139]);self.assertFalse(a[140])
    def test_dwell_ten_first_clear(self):
        s=np.zeros(160);s[100]=1;a,_=replay(s,np.zeros((160,4)),np.ones(160,bool),.05,dwell=10)
        self.assertTrue(a[148]);self.assertFalse(a[149])
    def test_entry_priority(self):
        a=model.alarm_machine(np.array([.2,.2,.05]),np.ones(3,bool),np.ones(3,bool),.1,1)
        np.testing.assert_array_equal(a,[True,True,False])
    def test_strict_tie(self):
        a=model.alarm_machine(np.array([.1,.2,.1]),np.ones(3,bool),np.ones(3,bool),.1,1)
        np.testing.assert_array_equal(a,[False,True,False])
    def test_invalid_history_holds(self):
        s=np.zeros(160);s[100]=1;valid=np.ones(160,bool);valid[120]=False
        a,ev=replay(s,np.zeros((160,4)),valid,.05)
        self.assertTrue(a[-1]);self.assertFalse(ev[-1])
    def test_fragmentation(self):
        self.assertEqual(runs([0,1,1,0,1,0]),[2,1]);self.assertEqual(runs([1,1,0],1),[1])
    def test_missing_not_zero_delay(self):
        d=dist([None,0.,.2]);self.assertEqual(d['missing'],1);self.assertEqual(d['n'],2);self.assertEqual(d['median'],.1)
    def setup_event(self):
        n=80;a=np.zeros(n,bool);attack=np.zeros(n,bool);attack[20:40]=1;s=np.zeros((n,4));s[22:45,0]=1
        c=dict(warmup=10,dt=.02,return_tolerance=.1,dwell=10,recovery_horizon=20)
        return a,attack,s,np.zeros_like(s),np.ones(4),c
    def test_misses_preserved(self):
        a,y,s,t,sc,c=self.setup_event();r=evaluation.evaluate(a,y,s,t,sc,c);e=extra(a,y,s,t,sc,c,r)
        self.assertFalse(r['overlap']);self.assertIsNone(r['clear_delay']);self.assertEqual(e['outside_inactive_points'],23)
        self.assertEqual(e['outside_inactive_after_detection_points'],0);self.assertFalse(e['joint_detected_continuous_outside_timely'])
    def test_conditional_clear_does_not_imply_retention(self):
        a,y,s,t,sc,c=self.setup_event();a[20:24]=1;r=evaluation.evaluate(a,y,s,t,sc,c);e=extra(a,y,s,t,sc,c,r)
        self.assertTrue(r['already_clear_at_return']);self.assertEqual(r['clear_delay'],0)
        self.assertEqual(e['outside_inactive_after_detection_points'],21);self.assertFalse(e['joint_detected_continuous_outside_timely'])
    def test_clearance_censoring(self):
        a,y,s,t,sc,c=self.setup_event();a[20:]=1;r=evaluation.evaluate(a,y,s,t,sc,c);e=extra(a,y,s,t,sc,c,r)
        self.assertIsNone(r['clear_delay']);self.assertTrue(e['clearance_censored'])
    def test_return_missing(self):
        a,y,s,t,sc,c=self.setup_event();a[20:]=1;s[22:,0]=1;r=evaluation.evaluate(a,y,s,t,sc,c)
        self.assertTrue(r['return_missing']);self.assertIsNone(r['clear_delay'])
    def test_empty_distributions(self):
        self.assertEqual(dist([])['n'],0);self.assertIsNone(dist([])['median'])

if __name__=='__main__':unittest.main()
