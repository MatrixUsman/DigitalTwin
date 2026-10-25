"""Explicit pre-execution freezes; never invoke the final generator."""
import argparse,json
from datetime import datetime,timezone
from io19 import *
p=argparse.ArgumentParser();p.add_argument('phase',choices=['development','pilot','final']);a=p.parse_args()
bindings=source_bindings();c=json.loads((HERE/'config.json').read_text())
inputs=[MODELS/'selection.json',OLD/'calibration.json',HERE.parent/'recovery_v0.8/FREEZE.json']
chosen=json.loads((MODELS/'selection.json').read_text())
for plant in ['Q1','Q2','Q3']:
    inputs.append(MODELS/f'base_{plant}.npz')
    for role in ['linear','rbf']:inputs.append(MODELS/f'fit_{plant}_{chosen["models"][plant][role]}.npz')
inputs+=list(NORMAL.glob('normal_*.npz'))
if len(list(NORMAL.glob('normal_*.npz')))!=81:raise ValueError('Unexpected development population')
if a.phase in ['pilot','final']:
    dev=LOCAL/'development_001';inputs += [dev/'selected.json',dev/'development.json',dev/'supervisor.json']
    if json.loads((dev/'supervisor.json').read_text())['status']!='completed':raise ValueError('Incomplete development')
if a.phase=='final':
    pilot=LOCAL/'pilot_001';inputs += [pilot/'pilot.json',pilot/'supervisor.json']
    x=json.loads((pilot/'pilot.json').read_text())
    if not x['admitted']:raise ValueError('Pilot not admitted')
for path in inputs:bindings[str(path.relative_to(PROJECT))]=sha(path)
write(HERE/(a.phase.upper()+'_FREEZE.json'),dict(utc=datetime.now(timezone.utc).isoformat(),phase=a.phase,
    configuration=c,bindings=bindings,outcomes_generated=False,
    selection_rule='M13 benign points, starts, mean envelope width, memory, ascending',
    final_criterion='PLAN.md and mechanism19.py:criterion fixed before final outcomes',synthetic=True))
print(a.phase,'frozen bindings',len(bindings))
