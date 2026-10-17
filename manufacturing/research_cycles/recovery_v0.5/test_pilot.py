"""Synthetic physics, chronology, uncertainty and recovery-contract tests."""
import copy
import json
from pathlib import Path
import unittest
import numpy as np
from plant import mass,coriolis,derivative,advance,kinetic,tip,commands,simulate
from observer import predictions,hysteresis,candidate,outcome,fit_linear,design,scores,decisions

class Checks(unittest.TestCase):
    def setUp(self):
        self.c=json.loads((Path(__file__).parent/'config.json').read_text());self.p=self.c['nominal']

    def test_mass_spd_and_symmetry(self):
        for q in np.linspace(-np.pi,np.pi,41):
            m=mass([.4,q],self.p);np.testing.assert_array_equal(m,m.T)
            self.assertGreater(np.linalg.eigvalsh(m).min(),0)

    def test_mass_from_cartesian_kinetic_energy(self):
        q=np.array([.2,-.6]);v=np.array([.3,.8]);l1,l2=self.p['l1'],self.p['l2']
        v1=l1*v[0]*np.array([-np.sin(q[0]),np.cos(q[0])])
        v2=v1+l2*(v[0]+v[1])*np.array([-np.sin(q.sum()),np.cos(q.sum())])
        expected=.5*self.p['m1']*(v1@v1)+.5*self.p['m2']*(v2@v2)
        self.assertAlmostEqual(kinetic(np.r_[q,v],self.p),expected,places=13)

    def test_energy_balance(self):
        x=np.array([.2,-.3,.4,-.2]);dx=derivative(x,np.zeros(4),self.p,self.c,free=True);eps=1e-6
        gradient=np.array([(kinetic(x+np.eye(4)[i]*eps,self.p)-kinetic(x-np.eye(4)[i]*eps,self.p))/(2*eps) for i in range(4)])
        self.assertAlmostEqual(float(gradient@dx),-float(np.asarray(self.p['b'])@(x[2:]**2)),places=9)

    def test_free_energy_conservation(self):
        p={**self.p,'b':[0.,0.]};x=np.array([.2,.4,.3,-.2]);initial=kinetic(x,p)
        for _ in range(100):x=advance(x,np.zeros(4),p,self.c,free=True)
        self.assertLess(abs(kinetic(x,p)-initial),1e-9)

    def test_equilibrium(self):
        x=np.array([.2,-.4,0.,0.]);np.testing.assert_array_equal(advance(x,x,self.p,self.c),x)

    def test_inverse_dynamics_and_saturation(self):
        x=np.array([.2,-.3,.1,-.4]);command=np.array([100.,-100.,0.,0.]);dx=derivative(x,command,self.p,self.c)
        reconstructed=mass(x[:2],self.p)@dx[2:]+coriolis(x[:2],x[2:],self.p)+np.asarray(self.p['b'])*x[2:]
        np.testing.assert_allclose(reconstructed,[20.,-20.],atol=1e-12)

    def test_step_convergence(self):
        x=np.array([.1,.2,-.1,.3]);u=np.array([.3,.4,.2,-.1]);ref=advance(x,u,self.p,self.c,substeps=32)
        e1=np.linalg.norm(advance(x,u,self.p,self.c,substeps=4)-ref)
        e2=np.linalg.norm(advance(x,u,self.p,self.c)-ref)
        self.assertLess(e2,e1/8);self.assertLess(e2,1e-5)

    def test_geometry_known_points(self):
        np.testing.assert_allclose(tip([0.,0.],self.p),[.9,0.],atol=1e-15)
        np.testing.assert_allclose(tip([0.,np.pi],self.p),[.1,0.],atol=1e-15)

    def short(self):
        c=copy.deepcopy(self.c);c.update(steps=70,warmup=10,onset=20,end=40,context_gap_end=30);return c

    def test_synthetic_determinism(self):
        c=self.short();a=simulate(c,self.p,'normal',17,'train');b=simulate(c,self.p,'normal',17,'train')
        for key in a:np.testing.assert_array_equal(a[key],b[key])

    def test_role_noise_separation(self):
        c=self.short();a=simulate(c,self.p,'normal',17,'train');b=simulate(c,self.p,'normal',17,'calibration')
        np.testing.assert_array_equal(a['state'],b['state']);self.assertFalse(np.array_equal(a['measurements'],b['measurements']))

    def test_authorization_identifiability_pair(self):
        c=self.short();a=simulate(c,self.p,'authorized_offset',17,'evaluation');b=simulate(c,self.p,'persistent_offset',17,'evaluation')
        np.testing.assert_array_equal(a['measurements'],b['measurements'])
        self.assertFalse(np.array_equal(a['available'],b['available']))
        self.assertEqual(a['attack'].sum(),0);self.assertEqual(b['attack'].sum(),20)

    def test_context_hold_does_not_reveal_approved_change(self):
        c=self.short();_,available,_,valid,_,_=commands(c,'context_gap_offset')
        np.testing.assert_array_equal(available[20:30],np.tile(available[19],(10,1)))
        self.assertFalse(valid[20:30].any())

    def test_command_duration_and_future_support(self):
        c=self.short();a=commands(c,'normal');b=commands(c,'brief_offset')
        np.testing.assert_array_equal(a[2][:20],b[2][:20]);np.testing.assert_array_equal(a[2][25:],b[2][25:])
        self.assertEqual(b[4].sum(),5)

    def test_observer_scores_before_correction(self):
        c=self.short();y=np.zeros((70,4));u=commands(c,'normal')[1];other=y.copy();other[30:]+=1
        f,r=predictions(y,u,c);ff,rr=predictions(other,u,c)
        np.testing.assert_array_equal(f[:31],ff[:31]);np.testing.assert_array_equal(r,rr)
        self.assertFalse(np.array_equal(f[31:],ff[31:]))

    def test_history_target_alignment(self):
        y=np.arange(40.).reshape(10,4);u=-y;x,t=design(y,u,4,True)
        np.testing.assert_array_equal(x[0,:16],y[:4].reshape(-1));np.testing.assert_array_equal(x[0,16:20],u[3]);self.assertEqual(t[0],4)

    def test_hysteresis_immediate_alarm_dwell_clear(self):
        a,c=hysteresis([2.,.1,.1,.1],np.ones(4,dtype=bool),1,.5,3)
        np.testing.assert_array_equal(a,[True,True,True,False]);np.testing.assert_array_equal(c,[0,1,2,0])

    def test_missing_context_cannot_clear(self):
        a,c=hysteresis([2.,0.,0.,0.],[True,False,True,True],1,.5,2)
        np.testing.assert_array_equal(a,[True,True,True,False])

    def test_candidate_exact_hysteresis_equivalence(self):
        for seed in [17,42,2026]:
            rng=np.random.default_rng(seed);f=rng.uniform(0,2,1000);r=rng.uniform(0,2,1000);valid=rng.uniform(size=1000)>.1
            a,c=candidate(f,r,valid,1,.5,3);b,d=hysteresis(np.maximum(f,r),valid,1,.5,3)
            np.testing.assert_array_equal(a,b);np.testing.assert_array_equal(c,d)

    def test_recovery_prefix_causality(self):
        x=np.arange(100.)%5;y=x.copy();y[50:]=100
        a,_=hysteresis(x,np.ones(100,dtype=bool),2,1,3);b,_=hysteresis(y,np.ones(100,dtype=bool),2,1,3)
        np.testing.assert_array_equal(a[:50],b[:50])

    def test_unknown_attack_targets_count_as_misses(self):
        c=self.short();a=np.ones(70,dtype=bool);unknown=np.zeros(70,dtype=bool);unknown[20:30]=True
        attack=np.zeros(70,dtype=bool);attack[20:40]=True
        row=outcome(a,unknown,attack,np.zeros(70,dtype=bool),np.zeros((70,4)),np.zeros((70,4)),np.ones(4),c)
        self.assertEqual((row['tp'],row['fn']),(10,10));self.assertEqual(row['unknown'],10)
        self.assertEqual(row['delay_steps'],10)
        self.assertFalse(row['fresh_hit'])

    def test_missed_delay_is_null(self):
        c=self.short();a=np.zeros(70,dtype=bool);attack=a.copy();attack[20:40]=True
        row=outcome(a,a,attack,a,np.zeros((70,4)),np.zeros((70,4)),np.ones(4),c)
        self.assertFalse(row['overlap_hit']);self.assertIsNone(row['delay_steps']);self.assertIsNone(row['first_clear_steps'])

    def test_fit_cannot_use_other_role_observations(self):
        c=self.short();ep=simulate(c,self.p,'normal',17,'train')
        mean=ep['measurements'][10:].mean(axis=0);scale=ep['measurements'][10:].std(axis=0)
        initial=fit_linear([ep],mean,scale,c,True)
        development=simulate(c,self.p,'normal',17,'calibration');development['measurements'][:]=1e8
        np.testing.assert_array_equal(initial,fit_linear([ep],mean,scale,c,True))

    def test_strict_threshold_ties(self):
        values=np.array([0.,1.,1.,1.]);rank=int(np.ceil(.75*len(values)));threshold=np.sort(values)[rank-1]
        self.assertEqual(int((values>threshold).sum()),0)

    def test_declared_calibration_count_and_rank(self):
        count=len(self.c['plants'])*len(self.c['seeds'])*len(self.c['normal_conditions'])*(self.c['steps']-self.c['warmup'])
        self.assertEqual(count,16200);self.assertEqual(int(np.ceil(count*self.c['quantile'])),16038)

if __name__=='__main__':unittest.main()
