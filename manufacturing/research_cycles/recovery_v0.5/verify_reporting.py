"""Additional postprocessing checks for physical-return interpretation and costs."""
import json
from common import HERE,LOCAL,sha,arrays,check_freeze
from recover_reporting import recovery_identity
import numpy as np

if __name__=='__main__':
    check_freeze();recovery_identity();run=LOCAL/'runs/reporting_001';origin=LOCAL/'runs/simulation_001'
    cfg=json.loads((HERE/'config.json').read_text());fit=arrays(run/'fit.npz');rows=json.loads((run/'outcomes.json').read_text());checks=[]
    def check(name,ok):
        checks.append({'name':name,'passed':bool(ok)})
        if not ok:raise AssertionError(name)
    for item in json.loads((run/'roster.json').read_text())['evaluation']:
        ep=arrays(run/(item['id']+'.npz'));where=np.flatnonzero(ep['attack'])
        if not len(where):continue
        end=int(where[-1])+1;distance=np.max(np.abs((ep['state']-ep['reference'])/fit['scale']),axis=1)
        stable=np.convolve((distance[end:end+250]<=.1).astype(int),np.ones(10,dtype=int),mode='valid')==10
        loc=np.flatnonzero(stable);expected=int(loc[0]) if len(loc) else None
        for row in [r for r in rows if r['id']==item['id']]:check('physical-return '+item['id']+row['method'],row['physical_return_steps']==expected)
    for name,h in json.loads((origin/'SCORES_SEALED.json').read_text())['sha256'].items():check('unchanged source '+name,sha(run/name)==h==sha(origin/name))
    a=json.loads((origin/'supervisor.json').read_text());b=json.loads((run/'supervisor.json').read_text())
    original_usage=json.loads((origin/'failure.json').read_text())['usage']
    recovered_usage=json.loads((run/'summary.json').read_text())['usage']
    check('combined wall below original cap',a['wall_seconds']+b['wall_seconds']<600)
    check('combined CPU below original cap',original_usage['process_cpu_seconds']+recovered_usage['process_cpu_seconds']<300)
    check('both sampled RSS bounded',max(a['sampled_peak_rss_bytes'],b['sampled_peak_rss_bytes'])<1073741824)
    check('both getrusage RSS bounded',max(original_usage['peak_rss_bytes'],recovered_usage['peak_rss_bytes'])<1073741824)
    check('both output budgets honored',a['output_bytes']<52428800 and b['output_bytes']<52428800)
    v={'status':'passed','total':len(checks),'passed':sum(c['passed'] for c in checks),'checks':checks,
       'reporting_script_sha256':sha(HERE/'verify_reporting.py'),'interpretation':'Physical return is the declared diagnostic, not a safety certificate.'}
    out=LOCAL/'verification/reporting_001';out.mkdir(parents=True,exist_ok=False)
    (out/'verification.json').write_text(json.dumps(v,indent=2)+'\n');print(json.dumps({k:v[k] for k in ['status','total','passed']}))
