"""Seal completed normal-only evidence; no publication or data movement."""
from pathlib import Path
import json,hashlib
from datetime import datetime,timezone
H=Path(__file__).resolve().parent;P=H.parents[1]
files={p for p in H.iterdir() if p.is_file() and p.name!='PACKAGE_MANIFEST.json'}
files.update(p for p in (P/'local/observer_feasibility_v0.21').rglob('*') if p.is_file() and '__pycache__' not in p.parts)
files.add(H.parent/'representation_v0.21/PRIOR_ART_DECISION.md')
m={'utc':datetime.now(timezone.utc).isoformat(),'scope':'Completed normal-only synthetic feasibility and preserved infrastructure failures; original novelty objective unresolved','admission_passed':False,'attack_experiment_run':False,'files':len(files),'sha256':{str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}}
with (H/'PACKAGE_MANIFEST.json').open('x') as f:json.dump(m,f,indent=2);f.write('\n')
print('Sealed',len(files),'files')
