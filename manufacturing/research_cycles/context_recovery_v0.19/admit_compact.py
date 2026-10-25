"""Admit unchanged science with measured compact result representation."""
import sys,json,io
from datetime import datetime,timezone
from io19 import *
from mechanism19 import alarms
from worker_compact import CompactWriter
check(HERE/'DEVELOPMENT_FREEZE.json');check(HERE/'PILOT_FREEZE.json')
old=LOCAL/'resource_check_001/resource_admission.json';r=json.loads(old.read_text())
models=bases();env=json.loads((LOCAL/'development_001/selected.json').read_text())['models'];cal=json.loads((OLD/'calibration.json').read_text());records=[]
out=LOCAL/'compact_check_001';out.mkdir(parents=True,exist_ok=False);w=CompactWriter(out,limit_bytes=5242880)
for plant in models:
    for path in sorted((LOCAL/'pilot_001').glob('pilot_*.npz')):
        z=load_npz(path);obs=Observation(z['measurements'],z['available'],z['valid']);refs,res,scores=infer(obs,models[plant],cal['cusum_k'][plant],{'warmup':100,'return_tolerance':.1,'dwell':10})
        a,b,lo,hi=alarms(res,scores,obs.valid,cal['thresholds'][plant],models[plant]['base']['scale'],obs.commands,env[plant],residual13)
        target=w.write_bytes(f'score_{plant}_{path.name}',packed(measurements=obs.measurements,commands=obs.commands,valid=obs.valid,references=refs,scores=scores,alarms=a,width=b,lower=lo,upper=hi,context_extrapolation=np.zeros(len(a),bool)))
        saved=load_npz(target);np.testing.assert_array_equal(saved['references'],refs[:,[0,2,3]])
        for key,value in [('scores',scores),('alarms',a),('width',b),('lower',lo),('upper',hi)]:np.testing.assert_array_equal(saved[key],value)
        records.append(dict(plant=plant,pilot=path.name,bytes=target.stat().st_size,points=len(a)))
estimate=max(v['bytes']/v['points'] for v in records)*777600+777600*70+5000000
admitted=r['numeric_gate'] and r['conservative_total_estimate_seconds']<250 and estimate<250*1024**2
w.write_json('COMPACT_ADMISSION.json',dict(utc=datetime.now(timezone.utc).isoformat(),admitted=admitted,estimated_output_bytes=estimate,
    conservative_seconds=r['conservative_total_estimate_seconds'],records=records,checks=36,
    scientific_change=False,omitted_roles='Unused linear,RBF-following,persistence,mean21 reference arrays only; all scores retained',
    previous_failed_resource_admission_sha256=sha(old),previous_failed_pilot_sha256=sha(LOCAL/'pilot_001/pilot.json')))
print('Compact estimate bytes',estimate,'admitted',admitted)
if not admitted:raise ValueError('Compact representation does not fit; no final run admitted')
f=check(HERE/'PILOT_FREEZE.json');bindings=dict(f['bindings']);bindings.update(source_bindings())
for path in [out/'COMPACT_ADMISSION.json',old,LOCAL/'resource_check_001/supervisor.json',LOCAL/'pilot_001/pilot.json',LOCAL/'pilot_001/supervisor.json']:
    bindings[str(path.relative_to(PROJECT))]=sha(path)
write(HERE/'FINAL_FREEZE.json',dict(utc=datetime.now(timezone.utc).isoformat(),phase='final',configuration=f['configuration'],bindings=bindings,
    outcomes_generated=False,scientific_configuration_changed=False,worker='worker_compact.py',
    serialization='Three used reference roles0,2,3 retained exactly; all scores and other arrays unchanged',
    criterion='Unchanged PLAN.md and mechanism19.py:criterion',resource_admission=str((out/'COMPACT_ADMISSION.json').relative_to(PROJECT))))
