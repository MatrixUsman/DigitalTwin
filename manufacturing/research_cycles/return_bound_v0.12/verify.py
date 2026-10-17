"""Independent saved-array arithmetic verification; no fit or new signals."""
import json
import math
import sys
from datetime import datetime, timezone
import numpy as np
from io_utils import HERE, PROJECT, RUN, check_frozen, sha256

f=check_frozen();c=f['configuration'];s=json.loads((RUN/'summary.json').read_text())
supervision=json.loads((RUN/'supervisor.json').read_text())
assert s['status']=='completed' and supervision['status']=='completed'
assert s['configuration']==c
checks=0
def check(value):
    global checks
    if not bool(value): raise AssertionError('verification check '+str(checks+1)+' failed')
    checks+=1

expected_traces={f'{ns["id"]}_{p["id"]}_s{seed}' for ns in c['noise_settings'] for p in c['profiles'] for seed in c['seeds']}
check(len(s['records'])==216);check(set(s['artifacts'])=={x+'.npz' for x in expected_traces})
check(json.loads((RUN/'launch.json').read_text())['freeze_sha256']==sha256(HERE/'FREEZE.json'))
names=['fixed_1','fixed_41','fixed_201','multiwindow','iid_assumption_41','iid_assumption_201']
check({(r['trace'],r['method']) for r in s['records']}=={(x,m) for x in expected_traces for m in names})
start=max(c['windows'])-1;n=c['samples'];d=4;k=len(c['windows']);t=np.arange(1,n+1)
logarithm=np.log(2*d*k*np.pi**2/(6*c['alpha']))+2*np.log(t)
for filename,digest in s['artifacts'].items():
    check(sha256(RUN/filename)==digest)
    receipt=json.loads((RUN/(filename[:-4]+'_receipt.json')).read_text());con=receipt['contract']
    check(receipt['sha256']==digest)
    with np.load(RUN/filename,allow_pickle=False) as z:
        a={key:z[key] for key in z.files}
    check(np.array_equal(a['valid'],np.ones(n,dtype=bool)))
    check(np.allclose(a['residual'],a['delta']+a['bias']+a['noise'],rtol=0,atol=1e-16))
    check(np.all(np.abs(a['delta']) <= c['tolerance']))
    check(np.all(np.abs(a['bias']) <= np.asarray(con['bias'])+1e-14))
    check(np.all(np.abs(np.diff(a['delta'],axis=0)) <= np.asarray(con['drift'])+1e-14))
    independent={}
    for m in c['windows']:
        # Direct convolution, not the implementation's cumulative sums.
        means=np.stack([np.convolve(a['residual'][:,j],np.ones(m)/m,mode='valid') for j in range(d)],axis=1)
        covariance=np.array([sum(rho**abs(i-j) for i in range(m) for j in range(m))*sig**2/m**2
                             for sig,rho in zip(con['sigma'],con['rho'])])
        for iid in (False,True):
            variance=np.square(con['sigma'])/m if iid else covariance
            bound=np.full((n,d),np.inf)
            bound[m-1:]=np.abs(means)+np.asarray(con['bias'])+np.sqrt(2*logarithm[m-1:,None]*variance)+np.asarray(con['drift'])*(m-1)/2
            name=('iid_assumption_' if iid else 'fixed_')+str(m)
            if name in a:
                check(np.allclose(bound,a[name],rtol=1e-12,atol=1e-12))
                independent[name]=bound
    independent['multiwindow']=np.minimum.reduce([independent['fixed_'+str(m)] for m in c['windows']])
    check(np.allclose(independent['multiwindow'],a['multiwindow'],rtol=1e-12,atol=1e-12))
    for method,bound in independent.items():
        record=next(r for r in s['records'] if r['trace']==filename[:-4] and r['method']==method)
        yes=np.all(bound[start:]<=np.asarray(c['tolerance']),axis=1);ix=np.flatnonzero(yes)
        violations=np.abs(a['delta'][start:])>bound[start:]+1e-12
        check(record['eligible']==n-start)
        check(record['certified']==int(yes.sum()))
        check(record['fraction']==float(yes.mean()))
        check(record['first_certificate_sample']==(int(ix[0]+start+1) if len(ix) else None))
        check(record['coverage_violation_channels']==int(violations.sum()))
        check(record['any_coverage_violation']==bool(violations.any()))
        check(record['feasibility_pass']==bool(yes.mean()>=c['feasibility_fraction']))
        check(record['assumptions_satisfied']==(not(method.startswith('iid_assumption') and any(r>0 for r in con['rho']))))
check(s['overall_feasibility_pass']==all(r['feasibility_pass'] for r in s['records'] if r['method']=='multiwindow'))
check(s['usage']['process_cpu_seconds']<=c['limits']['cpu_seconds'])
check(s['usage']['peak_rss_bytes']<=c['limits']['rss_bytes'])
receipt=json.loads((PROJECT/f['test_receipt']).read_text());check(receipt['returncode']==0)
check(sha256(PROJECT/f['test_receipt'].replace('receipt.json','tests.log'))==receipt['log_sha256'])
prior_counts={}
for manifest in f['prior_packages']:
    bindings=json.loads((PROJECT/manifest).read_text())['sha256']
    for name,digest in bindings.items(): check(sha256(PROJECT/name)==digest)
    prior_counts[manifest]=len(bindings)
result=dict(status='passed',utc=datetime.now(timezone.utc).isoformat(),checks=checks,traces=36,outcomes=216,
            command=[sys.executable,str(HERE/'verify.py')],python=sys.version,numpy=np.__version__,
            verifier_sha256=sha256(HERE/'verify.py'),freeze_sha256=sha256(HERE/'FREEZE.json'),summary_sha256=sha256(RUN/'summary.json'),
            preserved_prior_packages=prior_counts,independent_arithmetic=True,no_raw_access=True)
with (HERE/'VERIFICATION.json').open('x') as stream: json.dump(result,stream,indent=2);stream.write('\n')
print(json.dumps(result,indent=2))
