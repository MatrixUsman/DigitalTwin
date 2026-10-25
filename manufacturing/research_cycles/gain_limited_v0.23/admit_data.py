"""Metadata/identity admission only; never loads arrays."""
from pathlib import Path
import hashlib,json
from datetime import datetime,timezone
H=Path(__file__).resolve().parent;P=H.parents[1]
source=P/'research_cycles/rapt_protocol_v0.21/INPUT_MANIFEST.json'
old=json.loads(source.read_text());rows=[r for r in old['files'] if r['plant']=='Q1' and r['role'] in ['fit','development']]
expected={(role,condition,seed) for role in ['fit','development'] for condition in ['normal','authorized_offset','authorized_slow'] for seed in [17,42,2026]}
assert len(rows)==18 and {(r['role'],r['condition'],r['episode_seed']) for r in rows}==expected
for row in rows:
    assert row['task']==('K13' if row['role']=='fit' else 'M13')
    assert hashlib.sha256((P/row['path']).read_bytes()).hexdigest()==row['sha256']
record=dict(utc=datetime.now(timezone.utc).isoformat(),synthetic=True,exposed_development=True,source_manifest=str(source.relative_to(P)),source_manifest_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),signal_arrays_opened=False,calibration_excluded=True,files=rows)
with (H/'INPUT_MANIFEST.json').open('x') as f:json.dump(record,f,indent=2);f.write('\n')
print(json.dumps(dict(admitted_files=len(rows),array_access=False)))
