import json
import unittest
import numpy as np
from v7_common import config,roster,permitted
from v7_core import path,commands7,physical,lag_derivative,decide,calibrate7
from plant import advance

class Tests(unittest.TestCase):
    def setUp(self):self.c=config();self.s=permitted(self.c)
    def test_trajectory_derivative(self):
        for task in self.c['tasks7']:
            t=np.linspace(.1,20,50);e=1e-5
            derivative=(path(t+e,np.ones(50),task)[:,:2]-path(t-e,np.ones(50),task)[:,:2])/(2*e)
            np.testing.assert_allclose(derivative,path(t,np.ones(50),task)[:,2:],atol=1e-8)
    def test_lagfree_exact(self):
        u=np.tile([.1,.2,0,0],(8,1));initial=np.zeros(4);x=physical(initial,u,self.c['nominal'],self.s,0)
        for t in range(7):np.testing.assert_array_equal(x[t+1,:4],advance(x[t,:4],u[t],self.c['nominal'],self.s))
    def test_equilibrium(self):
        np.testing.assert_array_equal(physical(np.zeros(4),np.zeros((10,4)),self.c['nominal'],self.s,.04),0)
    def test_actuator_derivative(self):
        x=np.zeros(6);u=np.array([.1,0,0,0]);d=lag_derivative(x,u,self.c['nominal'],self.s,.04)
        self.assertAlmostEqual(d[4],45);self.assertEqual(d[5],0)
    def test_integration_refinement(self):
        # Synthetic constant command only; no reserved task/plant generated.
        u=np.tile([.1,-.15,0,0],(100,1));a=physical(np.zeros(4),u,self.c['nominal'],self.s,.06)
        b=physical(np.zeros(4),u,self.c['nominal'],dict(self.s,substeps=16),.06)
        self.assertLess(np.max(np.abs(a-b)),1e-4)
    def test_roster_and_seed(self):
        r=roster(self.c);self.assertEqual(len(r),144);self.assertEqual(len({x['id'] for x in r}),144)
        self.assertEqual(len({x['noise_seed'] for x in r}),18);self.assertTrue(all(x['noise_seed']>=80000 for x in r))
    def test_permitted_keys(self):
        self.assertFalse(set(self.s)&{'onset','end','plants7','tasks7','methods7'})
    def comp(self):
        return dict(scores=np.zeros((30,23)),valid=np.ones(30,dtype=bool),return_ok=np.ones(30,dtype=bool),
                    return_nomargin=np.ones(30,dtype=bool),jump=np.zeros(30,dtype=bool))
    def test_no_dwell(self):
        e=self.comp();e['scores'][0]=2
        a,_=decide(e,13,1,self.s);b,_=decide(e,11,1,self.s)
        self.assertFalse(a[1]);self.assertTrue(b[1]);self.assertFalse(b[10])
    def test_margin_ablation(self):
        e=self.comp();e['scores'][0]=2;e['return_ok'][:]=False
        a,_=decide(e,14,1,self.s);b,_=decide(e,11,1,self.s)
        self.assertFalse(a[-1]);self.assertTrue(b[-1])
    def test_reset_and_unknown(self):
        e=self.comp();e['scores'][0]=2;e['scores'][1:]=.75;e['jump'][3]=True
        a,_=decide(e,16,1,self.s);self.assertTrue(a[2]);self.assertFalse(a[3])
        e['valid'][3]=False;a,u=decide(e,16,1,self.s);self.assertTrue(a[3]);self.assertTrue(u[3])
    def test_reset_does_not_suppress_entry(self):
        e=self.comp();e['jump'][3]=True;e['scores'][3]=2
        self.assertTrue(decide(e,16,1,self.s)[0][3])
    def test_causal_reset(self):
        e=self.comp();e['scores'][0]=2;a,_=decide(e,16,1,self.s);e['jump'][20]=True
        np.testing.assert_array_equal(a[:20],decide(e,16,1,self.s)[0][:20])
    def test_threshold_monotonic(self):
        rng=np.random.default_rng(11)
        for j in [13,14,15,16,17,22]:
            e=self.comp();e['scores']=rng.uniform(0,2,(30,23));e['return_ok']=rng.random(30)>.2;e['jump'][[5,15]]=True
            counts=[decide(e,j,h,self.s)[0].sum() for h in np.linspace(0,2,25)]
            self.assertTrue(np.all(np.diff(counts)<=0))
    def test_threshold_no_attacks(self):
        e=self.comp();e['scores'][:]=1;c=dict(self.c,warmup=0)
        r=calibrate7([e],16,c);self.assertEqual(r['threshold'],0);json.dumps(r)

if __name__=='__main__':unittest.main(verbosity=2)
