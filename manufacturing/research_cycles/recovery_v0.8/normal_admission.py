"""Post-study guard for future designs; never changes the consumed v0.8 run."""
import json
from pathlib import Path
from datetime import datetime,timezone
HERE=Path(__file__).resolve().parent;PROJECT=HERE.parents[1]
run=PROJECT/'local/recovery_v0.8/runs/confirmation_002'
c=json.loads((HERE/'FREEZE.json').read_text())['configuration'];cal=json.loads((run/'calibration.json').read_text())['plants']
records=[]
for plant,record in cal.items():
 b=record['allowance'];delta=c['return_tolerance']
 records.append(dict(plant=plant,allowance=b,tolerance=delta,minimum_required_discrepancy=delta-b,
  clearance_inequality_feasible=b<=delta,stable_reference=record['reference_radius']<1))
result=dict(utc=datetime.now(timezone.utc).isoformat(),status='rejected' if any(not r['clearance_inequality_feasible'] for r in records) else 'necessary_conditions_only',
  scope='Post-exposure diagnostic using normal calibration only; not a new confirmatory result. Passing is necessary, not evidence of novelty or guaranteed recovery.',plants=records)
(HERE/'NORMAL_ADMISSION.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
