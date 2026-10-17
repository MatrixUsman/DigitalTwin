"""Post-run numerical QA on declared conditions; never changes saved observations."""
from datetime import datetime,timezone
import json
import resource
import time
import numpy as np
from support import HERE,LOCAL,sha,arrays,check_freeze,scaled_plant
from core import trajectory

if __name__=='__main__':
    resource.setrlimit(resource.RLIMIT_CPU,(60,60));start=time.monotonic()
    cfg=check_freeze()['configuration'];run=LOCAL/'runs/simulation_001';rows=[]
    # All six deterministic task/plant pairs, both normal and authorized offset.
    # Chosen as post-run numerical QA, not an additional performance experiment.
    for task in cfg['tasks']:
        for plant in cfg['fresh_plants']:
            for condition in ['normal','authorized_offset']:
                path=run/f'eval_{task["id"]}_{plant["id"]}_17_{condition}.npz'
                ep=arrays(path);c=dict(cfg);c.update(task);c['substeps']=16
                p=scaled_plant(c,plant['mass_factor'],plant['damping_factor'])
                state=trajectory(ep['state'][0],ep['executed'],p,c)
                rows.append(dict(task=task['id'],plant=plant['id'],condition=condition,
                    input_sha256=sha(path),max_absolute_state_difference=float(np.abs(state-ep['state']).max())))
    maximum=max(r['max_absolute_state_difference'] for r in rows)
    receipt=dict(utc=datetime.now(timezone.utc).isoformat(),status='passed' if maximum<1e-4 else 'failed',
        scope='Post-run integration refinement QA; no new condition or scientific modification',
        comparison='8 versus 16 RK4 substeps, all 1000 states',reference_tolerance=1e-4,
        maximum=maximum,rows=rows,wall_seconds=time.monotonic()-start,
        cpu_seconds=resource.getrusage(resource.RUSAGE_SELF).ru_utime+resource.getrusage(resource.RUSAGE_SELF).ru_stime)
    with (LOCAL/'numerical_audit.json').open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
    print(json.dumps({k:v for k,v in receipt.items() if k!='rows'},indent=2))
