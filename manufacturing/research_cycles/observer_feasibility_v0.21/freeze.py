import sys,json
from datetime import datetime,timezone
from io21 import *
import observers
if __name__=='__main__':
    bases();files=set(HERE.glob('*.py'))|{HERE/'PLAN.md',HERE.parent/'recovery_v0.8/FREEZE.json'}
    for m in list(sys.modules.values()):
        p=getattr(m,'__file__',None)
        if p:
            p=Path(p).resolve()
            if p.is_relative_to(PROJECT) and p.suffix=='.py' and ('research_cycles' in p.parts or 'mfg_twin' in p.parts):files.add(p)
    files.update(NORMAL.glob('normal_*.npz'));files.update(NORMAL.glob('base_*.npz'));files.update(NORMAL.glob('fit_*.npz'));files.add(NORMAL/'selection.json')
    f={'utc':datetime.now(timezone.utc).isoformat(),'phase':'normal_only','protocol':'PLAN.md','bindings':{str(p.relative_to(PROJECT)):sha(p) for p in sorted(files)},'limits':LIMITS.__dict__,'interpreter':sys.executable,'study':'manufacturing-observer-feasibility-v0.21'}
    with (HERE/'FREEZE.json').open('x') as stream:json.dump(f,stream,indent=2);stream.write('\n')
    print('Frozen',len(f['bindings']),'identities; no fresh observations generated')
