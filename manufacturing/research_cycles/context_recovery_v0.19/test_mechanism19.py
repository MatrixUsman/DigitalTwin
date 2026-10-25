"""Explicitly synthetic fixtures; no benchmark observations or network."""
import unittest
import numpy as np
from mechanism19 import context,quantile,fit_envelope,widths,set_alarm,extra_metrics,distributions
from sim19 import path,commands

class Synthetic(unittest.TestCase):
    def test_causal_context(self):
        u=np.zeros((140,4));u[110:,0]=1;v=u.copy();v[125:]=100
        np.testing.assert_array_equal(context(u,np.ones(4),10)[:125],context(v,np.ones(4),10)[:125])
        self.assertAlmostEqual(context(u,np.ones(4),10)[111],np.exp(-.1))
    def test_context_rejects_invalid(self):
        for scale in [np.zeros(4),np.full(4,np.nan)]:
            with self.assertRaises(ValueError):context(np.zeros((120,4)),scale,10)
    def test_quantile_rank_ties(self):
        self.assertEqual(quantile(np.arange(100)),98)
        self.assertEqual(quantile([2]*100),2)
    def test_fit_independence(self):
        u=np.zeros((150,4));s=np.arange(150)/1000
        m=fit_envelope([(u,s)],[(u,s)],np.ones(4),10);before=repr(m)
        widths(np.full((150,4),999.),np.ones(4),m)
        self.assertEqual(before,repr(m));self.assertEqual(sum(m['counts']),50)
    def test_fallback(self):
        u=np.zeros((120,4));s=np.full(120,.2)
        m=fit_envelope([(u,s)],[(u,s)],np.ones(4),10)
        self.assertEqual(m['width'],[.2]*3)
    def test_set_ties_and_unknown(self):
        a,lo,hi=set_alarm([.13,.14,.11,.09,.07],[.03]*5,start=0)
        np.testing.assert_array_equal(a,[False,True,True,True,False])
        np.testing.assert_allclose(lo,[.10,.11,.08,.06,.04])
    def test_matched_entry_clearance(self):
        s=np.array([.15,.10,.08,.06]);b=np.full(4,.03)
        a=set_alarm(s,b,start=0)[0];h=set_alarm(s,b,kind='hysteresis',start=0)[0]
        np.testing.assert_array_equal(a,[1,1,1,0]);np.testing.assert_array_equal(h,[1,0,0,0])
    def test_prefix_never_enters(self):
        s=np.r_[np.ones(100),np.zeros(10)]
        self.assertFalse(set_alarm(s,.01)[0].any())
    def test_outside_counts_and_durations(self):
        state=np.zeros((6,4));state[1:4,0]=.2;truth=np.zeros_like(state)
        a=np.array([0,0,1,1,0,0],bool);attack=np.array([0,1,1,0,0,0],bool)
        r=extra_metrics(a,attack,state,truth,np.ones(4),start=0)
        self.assertEqual(r['outside_points'],3);self.assertEqual(r['outside_inactive'],1)
        self.assertEqual(r['alarm_durations_seconds'],[.04])
    def test_missing_delays_preserved(self):
        d=distributions([None,.1,.3]);self.assertEqual(d['n'],2);self.assertAlmostEqual(d['median'],.2)
        self.assertIsNone(distributions([None])['p95'])
    def test_approved_boundary(self):
        task=dict(kind='lissajous',amplitude=[.2,.3],frequency=.5,phase=.4,onset=150,duration=100,brief=8,offset=.1,slow=.7)
        a=commands(500,task,'persistent_offset');b=commands(500,task,'normal')
        np.testing.assert_array_equal(a['available'],b['available']);self.assertEqual(a['attack'].sum(),100)
        np.testing.assert_allclose(a['executed'][150:250,0]-a['available'][150:250,0],.1)
        np.testing.assert_array_equal(a['executed'][250:],a['available'][250:])
    def test_analytic_velocity(self):
        for kind in ['lissajous','smoothstep']:
            task=dict(kind=kind,amplitude=[.2,.3],frequency=.2,phase=.3)
            t=np.linspace(.3,1.1,50);eps=1e-6
            d=(path(t+eps,np.ones(50),task)[:,:2]-path(t-eps,np.ones(50),task)[:,:2])/(2*eps)
            np.testing.assert_allclose(d,path(t,np.ones(50),task)[:,2:],atol=1e-8)

if __name__=='__main__':unittest.main()
