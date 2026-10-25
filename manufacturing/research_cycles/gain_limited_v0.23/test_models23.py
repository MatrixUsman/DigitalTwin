import unittest
import numpy as np
import torch
from models23 import Adapter,adapter_predict,adapter_predict_many,context,lagged,l1_project,fir_fit,fir_predict,windows,metrics,leaky,kalman,reference_fit,reference_predict,fit_scale
from data23 import checked_arrays,ALLOWED
from pilot23 import admission
import copy,json
from pathlib import Path

class Tests(unittest.TestCase):
    def setUp(self):self.rng=np.random.default_rng(2317)
    def test_projected_weight_certificate(self):
        for k in [.25,.5,.75]:
            for rho in [.25,.75]:
                m=Adapter(k,rho)
                with torch.no_grad():
                    m.wh.mul_(100);m.wz.mul_(100);m.wo.mul_(100)
                m.project();c=m.certificate();self.assertLessEqual(c['K'],k);self.assertLessEqual(c['C'],k);self.assertLess(c['rho'],rho)
    def test_context_branch_has_zero_observation_gain(self):
        m=Adapter(None,.25,kind='context');z=self.rng.normal(size=(130,4));c=self.rng.normal(size=(130,8));a=adapter_predict(m,z,c);b=adapter_predict(m,z+100,c)
        np.testing.assert_array_equal(a,b);self.assertEqual(m.certificate()['K'],0)
    def test_causal_prefix_and_reset(self):
        m=Adapter(.5,.25);z=self.rng.normal(size=(130,4));c=context(z);a=adapter_predict(m,z,c);zz=z.copy();zz[70:]+=50
        b=adapter_predict(m,zz,c);np.testing.assert_array_equal(a[:71],b[:71]);np.testing.assert_array_equal(a,adapter_predict(m,z,c))
    def test_fading_memory_inequality(self):
        m=Adapter(.5,.75);z=self.rng.normal(size=(140,4));c=self.rng.normal(size=(140,8));d=self.rng.normal(size=(140,4));d[:30]=0
        a=adapter_predict(m,z,c);b=adapter_predict(m,z+d,c);cert=m.certificate();bound=0.
        for t in range(140):
            if t:bound=cert['rho']*bound+cert['beta']*np.max(np.abs(d[t-1]))
            self.assertLessEqual(np.max(np.abs(a[t]-b[t])),cert['gamma']*bound+2e-7)
    def test_plateau_gain_and_cap_floors(self):
        m=Adapter(.5,.25);z=self.rng.normal(size=(140,4));c=context(z);d=np.zeros_like(z);d[30:,0]=.8
        a=adapter_predict(m,z,c);b=adapter_predict(m,z+d,c);cert=m.certificate();contrast=d-(b-a)
        self.assertGreaterEqual(np.max(np.abs(contrast[30:]),axis=1).min(),(1-cert['K'])*.8-2e-7)
        self.assertLessEqual(np.max(np.abs(b-a)),2*cert['C']+2e-7)
    def test_prior_larger_offset_requires_history_bound(self):
        z=np.zeros((5,4));d=z.copy();d[1,0]=10.;d[2,0]=.1;a=leaky(d,.75,.25)
        self.assertGreater(abs(a[2,0]),.75*.1)
    def test_l1_projection_and_fir_gain(self):
        np.testing.assert_allclose(l1_project(np.array([3.,-2.,1.]),2.),[1.5,-.5,0.])
        z=self.rng.normal(size=(400,4));c=self.rng.normal(size=(400,8));m=fir_fit([z],[c],.5,max_iterations=5000)
        self.assertTrue(m['converged']);self.assertLessEqual(m['K'],.5+1e-10)
        delta=self.rng.normal(size=z.shape);diff=fir_predict(z+delta,c,m)-fir_predict(z,c,m)
        self.assertLessEqual(np.max(np.abs(diff)),m['K']*np.max(np.abs(delta))+1e-10)
    def test_equal_cap_clips_only_observation_branch(self):
        z=self.rng.normal(size=(400,4));c=self.rng.normal(size=(400,8));m=fir_fit([z],[c],None)
        a=fir_predict(z,c,m,cap=.25);b=fir_predict(z+100,c,m,cap=.25)
        self.assertLessEqual(np.max(np.abs(a-b)),.5+1e-10)
    def test_training_window_coverage(self):
        z=np.repeat(np.arange(1200.)[:,None],4,axis=1);c=np.zeros((1200,8));p,cc,y,m=windows([z],[c]);covered=y[:,:,0][m[:,:,0].bool()].numpy()
        np.testing.assert_array_equal(covered,np.arange(100,1200));self.assertTrue(torch.equal(p[:,:,0][m[:,:,0].bool()],torch.arange(99,1199,dtype=torch.float32)))
    def test_reference_uses_only_preceding_commands(self):
        u=self.rng.normal(size=(300,4));y=self.rng.normal(size=(300,4));w=reference_fit([y],[u]);a=reference_predict(u,w);uu=u.copy();uu[150:]+=9;b=reference_predict(uu,w)
        np.testing.assert_array_equal(a[:151],b[:151])
    def test_radius_formulas_quantile(self):
        r=np.ones((1200,4))*.1;m=metrics([r],dict(K=.5,C=.25));self.assertAlmostEqual(m['gain_radius'],.4);self.assertAlmostEqual(m['cap_radius'],.7);self.assertEqual(m['rank'],1088)
        self.assertIsNone(metrics([r],dict(K=1.,C=None))['primary_radius'])
    def test_kalman_score_before_update(self):
        z=np.zeros((130,4));z[70,0]=1;a,g=kalman(z,1.);self.assertEqual(a[70,0],0.);self.assertAlmostEqual(a[71,0],g)
    def test_invalid_inputs_block(self):
        y=np.zeros((1200,4));v=np.ones(1200,bool);v[100]=False
        with self.assertRaises(ValueError):checked_arrays(y,y,v)
        v[:]=True;y[0,0]=np.nan
        with self.assertRaises(ValueError):checked_arrays(y,y,v)
        self.assertEqual(ALLOWED,('measurements','commands','valid'))
    def test_independent_batch_states(self):
        m=Adapter(.5,.25);zs=[self.rng.normal(size=(130,4)) for _ in range(2)];cs=[context(x) for x in zs];batched=adapter_predict_many(m,zs,cs)
        for z,c,a in zip(zs,cs,batched):np.testing.assert_allclose(a,adapter_predict(m,z,c),rtol=1e-5,atol=1e-8)
        changed=zs[1].copy()+90;again=adapter_predict_many(m,[zs[0],changed],cs);np.testing.assert_array_equal(again[0],batched[0])
    def test_nonfinite_metrics_and_weights_block(self):
        r=np.ones((1200,4));r[101,0]=np.nan
        with self.assertRaises(ValueError):metrics([r],dict(K=.5,C=.2))
        m=Adapter(.5,.25)
        with torch.no_grad():m.wc[0,0]=float('nan')
        with self.assertRaises(ValueError):m.certificate()
    def test_admission_equality_failure_and_ties(self):
        cfg=json.loads((Path(__file__).parent/'config.json').read_text());conditions={k:1. for k in cfg['conditions']}
        def row(name,radius,rmse,family='direct',simple=True,k=None):
            return dict(id=name,family=family,simple_comparator=simple,kappa_budget=k,metrics=dict(primary_radius=radius,rmse=rmse,episode_rmse=[rmse]*9),condition_rmse={x:rmse for x in conditions},extra=dict(underfit_flag=False))
        rows=[row('candidate',.95,.98,'constrained',False,.25),row('a_simple',1.,1.),row('b_simple',1.,1.),row('same_fir',1.1,1.1,'fir',True,.25)]
        rows += [row('filler'+str(i),2.+i,2.+i) for i in range(29)]
        status=[dict(converged=True)];a=admission(rows,status,cfg);self.assertTrue(a['passed']);self.assertEqual(a['simple_comparator'],'a_simple')
        self.assertFalse(admission(rows,[dict(converged=False)],cfg)['passed'])
        bad=copy.deepcopy(rows);bad[3]['metrics']['primary_radius']=.94;self.assertFalse(admission(bad,status,cfg)['clauses']['same_budget_fir_radius_lower'])
        bad=copy.deepcopy(rows);bad[0]['metrics']['episode_rmse'][0]=1.051;self.assertFalse(admission(bad,status,cfg)['clauses']['all_episodes_within_5pct'])

if __name__=='__main__':unittest.main()
