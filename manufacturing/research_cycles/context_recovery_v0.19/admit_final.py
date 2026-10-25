"""Separately recorded resource repair; no scientific retry or configuration edit."""
import sys,json
from datetime import datetime,timezone
from io19 import *
check(HERE/'DEVELOPMENT_FREEZE.json');check(HERE/'PILOT_FREEZE.json')
out=LOCAL/'resource_check_001';out.mkdir(parents=True,exist_ok=False)
lim=Limits(wall_seconds=30,cpu_seconds=20,rss_bytes=1073741824,output_bytes=5242880);w=BudgetWriter(out,limit_bytes=lim.output_bytes)
bindings=source_bindings();inputs=[LOCAL/'pilot_001/pilot.json',LOCAL/'pilot_001/supervisor.json',LOCAL/'development_001/selected.json']
inputs+=list((LOCAL/'pilot_001').glob('pilot_*.npz'))
for path in inputs:bindings[str(path.relative_to(PROJECT))]=sha(path)
w.write_json('RESOURCE_FREEZE.json',dict(utc=datetime.now(timezone.utc).isoformat(),bindings=bindings,
    reason='Initial un-cached doubled physics extrapolation exceeded admission. Measure inference/compression and count actual cache reuse.',scientific_change=False))
cmd=[sys.executable,str(HERE/'resource_check.py'),str(out)];w.write_json('launch.json',dict(command=cmd,cwd=str(PROJECT)))
r=supervise(cmd,cwd=PROJECT,output_dir=out,limits=lim,env={'PYTHONDONTWRITEBYTECODE':'1','OPENBLAS_NUM_THREADS':'1'})
w.write_json('supervisor.json',r)
if r['status']!='completed':raise ValueError('Resource check failed')
admission=json.loads((out/'resource_admission.json').read_text());print(json.dumps(admission,indent=2))
if not admission['admitted']:raise ValueError('Original final budget still not admitted; do not generate final')
# Existing full scientific freeze utility cannot admit a failed conservative cost
# check; preserve it and bind the separate measured admission explicitly here.
f=check(HERE/'PILOT_FREEZE.json');bindings=dict(f['bindings']);bindings.update(source_bindings())
for path in [out/'RESOURCE_FREEZE.json',out/'resource_admission.json',out/'supervisor.json',LOCAL/'pilot_001/pilot.json',LOCAL/'pilot_001/supervisor.json']:
    bindings[str(path.relative_to(PROJECT))]=sha(path)
write(HERE/'FINAL_FREEZE.json',dict(utc=datetime.now(timezone.utc).isoformat(),phase='final',configuration=f['configuration'],bindings=bindings,
    outcomes_generated=False,scientific_configuration_changed=False,resource_admission=str((out/'resource_admission.json').relative_to(PROJECT)),
    original_failed_pilot=str((LOCAL/'pilot_001').relative_to(PROJECT)),criterion='Unchanged PLAN.md and mechanism19.py:criterion'))
print('Final scientific protocol frozen; no final observations generated.')
