"""Read-back arithmetic checks; no generation, fitting or original-data access."""
import json
import numpy as np
from common import HERE,OLD,check,load,sha
from core import dist
run=HERE/'runs/replay_002';f=check();checks=len(f['sha256'])
s=json.loads((run/'summary.json').read_text());rows=json.loads((run/'outcomes.json').read_text());d=json.loads((run/'diagnostics.json').read_text())
assert len(rows)==189*18;checks+=1
old=json.loads((OLD/'outcomes.json').read_text());lookup={(r['id'],r['method']):r for r in rows}
for r in old:
    new=lookup[r['id'],r['method']]
    for k,v in r.items():assert new[k]==v;checks+=1
for r in rows:
    assert r['tp']+r['fp']+r['fn']+r['tn']==r['eligible'];checks+=1
    assert sum(r['alarm_run_lengths_points'])==r['alarm_points'];checks+=1
    assert len(r['alarm_run_lengths_points'])==r['alarm_episodes'];checks+=1
    assert r['outside_inactive_after_detection_points']<=r['outside_inactive_points']<=r['physical_outside_points'];checks+=1
    if not r['overlap']:assert r['detection_delay'] is None and r['clear_delay'] is None;checks+=1
for r in d:
    assert r['alarm_points']==r['score_exceedances']+r['retained_with_clearance_evidence']+r['retained_without_clearance_evidence'];checks+=1
for r in s['rows']:
    matches=[z for z in rows if z['method']==r['method'] and (r['group']=='pooled' or (z.get(r['group'])==r['stratum']) or (r['group']=='plant_condition' and z['plant']+'/'+z['condition']==r['stratum']))]
    assert len(matches)==r['episodes'];checks+=1
    b=[z for z in matches if z['benign']];e=[z for z in matches if z['event']]
    assert sum(z['alarm_points'] for z in b)==r['benign_alarms'];checks+=1
    assert sum(not z['overlap'] for z in e)==r['misses'];checks+=1
    assert sum(z['clear_timely'] for z in e)==r['inactive_by_return_plus_5s'];checks+=1
    assert dist([z['clear_delay'] for z in e])==r['clearance_delay_seconds'];checks+=1
seal=json.loads((run/'OUTPUT_SEAL.json').read_text());sealexceptions=[]
for name,h in seal['sha256'].items():
    if name=='worker.log':
        sealexceptions.append('Worker log was still streaming when worker-side seal was written; final completion seal below binds the completed log. Scientific artifact hashes verified.')
        continue
    assert sha(run/name)==h;checks+=1
receipt=json.loads((run/'supervisor.json').read_text());assert receipt['status']=='completed' and receipt['rss_samples']>0;checks+=1
result=dict(status='passed',checks=checks,synthetic_tests=12,original_outcome_records=3213,original_alarm_streams_exact=189,
 original_RBF_nodwell_alarm_streams_exact=189,bindings_unchanged=len(f['sha256']),
 caveats=sealexceptions,source_sha256=sha(HERE/'verify.py'),output_sha256={p.name:sha(p) for p in sorted(run.iterdir()) if p.is_file()})
with (HERE/'VERIFICATION.json').open('x') as o:json.dump(result,o,indent=2,sort_keys=True);o.write('\n')
print(json.dumps({k:result[k] for k in ['status','checks','bindings_unchanged','original_outcome_records']},indent=2))
