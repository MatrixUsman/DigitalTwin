import json,subprocess
from datetime import datetime,timezone
from common import HERE,PROJECT,OLD,MODELS,sha
paths=list(HERE.glob('*.py'))+[HERE/'PLAN.md',HERE/'config.json']
paths += list(OLD.glob('score_*.npz'))+list(OLD.glob('truth_*.npz'))
paths += [OLD/p for p in ['outcomes.json','catalog.json','calibration.json','summary.json']]
paths += [MODELS/f'base_{p}.npz' for p in ['Q1','Q2','Q3']]
paths += [PROJECT/'research_cycles/residual_twin_v0.13/model.py',PROJECT/'src/mfg_twin/supervisor.py']
for filename in ['audit_core.py','evaluation.py','io14.py','config.json']:
    paths.append(PROJECT/'research_cycles/attack_audit_v0.14'/filename)
paths += [PROJECT/'research_cycles/commissioning_v0.9/models.py']
f=dict(utc=datetime.now(timezone.utc).isoformat(),configuration=json.loads((HERE/'config.json').read_text()),
  git_revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=PROJECT,text=True).strip(),
  sha256={str(p.relative_to(PROJECT)):sha(p) for p in sorted(set(paths))})
with (HERE/'FREEZE.json').open('x') as out:json.dump(f,out,indent=2,sort_keys=True);out.write('\n')
print('Frozen bindings',len(f['sha256']))
