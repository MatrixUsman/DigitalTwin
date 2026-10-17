"""Software checks using synthetic fixtures, never benchmark observations."""
import dataclasses
import unittest
import numpy as np
from control import Contract, mean_variance, upper_bounds, certificate


class ControlTests(unittest.TestCase):
    def setUp(self):
        self.c = Contract((.03,.04), (.8,.5), (.01,.02), (.001,.002), (.1,.1), (1,3,5))
        self.e = np.arange(40, dtype=float).reshape(20,2)/1000
        self.ok = np.ones(20, bool)

    def test_covariance_matrix_identity(self):
        for m in (1,3,11,41):
            idx=np.arange(m)
            expected=[s*s*np.sum(r**np.abs(idx[:,None]-idx[None,:]))/(m*m) for s,r in zip(self.c.sigma,self.c.rho)]
            np.testing.assert_allclose(mean_variance(self.c.sigma,self.c.rho,m),expected,rtol=1e-14)

    def test_iid_variance(self):
        np.testing.assert_allclose(mean_variance([.1,.2],[0,0],17),np.square([.1,.2])/17)

    def test_correlation_inflates_variance(self):
        a=mean_variance([1],[0],21); b=mean_variance([1],[.8],21); c=mean_variance([1],[.95],21)
        self.assertTrue(a[0]<b[0]<c[0]<1)

    def test_current_drift_term_is_necessary_and_exact(self):
        e=np.arange(9,dtype=float)[:,None]*.1
        c=Contract((0,),(0,),(0,),(.1,),(1,),(5,))
        u=upper_bounds(e,np.ones(9,bool),c)[5]
        np.testing.assert_allclose(u[4:], e[4:],atol=1e-15)
        without=upper_bounds(e,np.ones(9,bool),dataclasses.replace(c,drift=(0,)))[5]
        self.assertTrue(np.all(without[4:] < e[4:]))

    def test_future_isolation(self):
        before=upper_bounds(self.e,self.ok,self.c)
        e=self.e.copy(); e[12:]+=100
        after=upper_bounds(e,self.ok,self.c)
        for m in before: np.testing.assert_array_equal(before[m][:12],after[m][:12])

    def test_no_input_mutation(self):
        e=self.e.copy(); ok=self.ok.copy(); upper_bounds(e,ok,self.c)
        np.testing.assert_array_equal(e,self.e); np.testing.assert_array_equal(ok,self.ok)

    def test_invalid_windows_do_not_impute(self):
        ok=self.ok.copy(); ok[7]=False; e=self.e.copy(); e[7]=np.nan
        u=upper_bounds(e,ok,self.c)[5]
        self.assertTrue(np.isinf(u[7:12]).all()); self.assertTrue(np.isfinite(u[12:]).all())

    def test_clock_not_reset_after_gap(self):
        ok=self.ok.copy(); ok[4]=False
        g=upper_bounds(self.e,ok,self.c)[5]; a=upper_bounds(self.e,self.ok,self.c)[5]
        np.testing.assert_allclose(g[9:],a[9:],rtol=0,atol=1e-15)

    def test_global_time_spending(self):
        a=upper_bounds(self.e,self.ok,self.c)[5]
        b=upper_bounds(self.e,self.ok,self.c,global_start=1001)[5]
        self.assertTrue(np.all(b[4:] > a[4:]))

    def test_short_input_returns_no_certificate(self):
        c=dataclasses.replace(self.c,windows=(41,))
        u=upper_bounds(self.e,self.ok,c)
        self.assertFalse(certificate(u,c.tolerance)[1].any())

    def test_registered_window_allocation(self):
        single=dataclasses.replace(self.c,windows=(5,))
        a=upper_bounds(self.e,self.ok,single)[5]; b=upper_bounds(self.e,self.ok,self.c)[5]
        self.assertTrue(np.all(b[4:] > a[4:]))

    def test_iid_control_equivalence(self):
        c=dataclasses.replace(self.c,rho=(0,0))
        a=upper_bounds(self.e,self.ok,c); b=upper_bounds(self.e,self.ok,c,assume_iid=True)
        for m in a: np.testing.assert_array_equal(a[m],b[m])

    def test_envelope_channel_intersection(self):
        arrays={1:np.array([[.05,.2]]),3:np.array([[.2,.05]])}
        u,yes=certificate(arrays,[.1,.1]); self.assertTrue(yes[0]); np.testing.assert_array_equal(u,[[.05,.05]])

    def test_exact_boundary_acceptance(self):
        self.assertTrue(certificate({1:np.array([[.1]])},[.1])[1][0])
        self.assertFalse(certificate({1:np.array([[.100001]])},[.1])[1][0])

    def test_nonfinite_valid_observations_rejected(self):
        for v in (np.nan,np.inf,-np.inf):
            e=self.e.copy();e[8,0]=v
            with self.assertRaises(ValueError): upper_bounds(e,self.ok,self.c)

    def test_bad_contract_rejected(self):
        for kwargs in ({'sigma':(-1,1)},{'rho':(1,0)},{'rho':(-.1,0)},{'drift':(np.nan,0)},
                       {'alpha':0},{'alpha':True},{'windows':(1,1)},{'windows':(3,1)},{'windows':(True,)},
                       {'windows':(1.5,)},{'tolerance':(0,1)},{'bias':(0,)}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError): dataclasses.replace(self.c,**kwargs)

    def test_bad_shapes_and_clock_rejected(self):
        for e,ok,start in ((self.e[:,0],self.ok,1),(self.e,self.ok.astype(int),1),(self.e,self.ok,0),(self.e,self.ok,1.5),(self.e,self.ok,2**53)):
            with self.assertRaises(ValueError): upper_bounds(e,ok,self.c,global_start=start)

    def test_large_constant_cannot_clear(self):
        e=np.full_like(self.e,.4)
        self.assertFalse(certificate(upper_bounds(e,self.ok,self.c),self.c.tolerance)[1].any())

    def test_zero_noise_bias_accounting(self):
        c=Contract((0,),(0,),(.02,),(0,),(.1,),(3,))
        e=np.full((7,1),-.02)
        np.testing.assert_allclose(upper_bounds(e,np.ones(7,bool),c)[3][2:],.04)

    def test_contract_copies_mutable_vectors(self):
        sigma=[.03,.04];c=dataclasses.replace(self.c,sigma=sigma);sigma[0]=99
        self.assertEqual(c.sigma[0],.03)

if __name__ == '__main__': unittest.main()
