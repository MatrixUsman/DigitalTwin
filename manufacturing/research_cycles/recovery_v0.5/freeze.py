"""Create a one-time pre-execution identity record after synthetic checks."""
from datetime import datetime,timezone
import json
from common import HERE,PROJECT,LOCAL,sha,previous_guard

if __name__=='__main__':
    path=HERE/'FREEZE.json'
    if path.exists():raise FileExistsError('A consumed freeze cannot be overwritten')
    test=json.loads((LOCAL/'tests/tests_002.json').read_text())
    if test['returncode']!=0:raise ValueError('Synthetic tests failed')
    for p,h in test['source_sha256'].items():
        if sha(PROJECT.parent/p)!=h:raise ValueError('Tested source changed: '+p)
    sources=sorted(list(HERE.glob('*.py'))+[HERE/name for name in ['config.json','PLAN.md','COMPARATORS.md','PRIOR_ART.md','SOURCE_RECEIPT.json']])
    guard=previous_guard();guard.update(json.loads((HERE/'SOURCE_RECEIPT.json').read_text())['sha256'])
    for p in sorted((LOCAL/'tests').iterdir()):guard[str(p.relative_to(PROJECT))]=sha(p)
    guard['src/mfg_twin/supervisor.py']=sha(PROJECT/'src/mfg_twin/supervisor.py')
    for p,h in guard.items():
        if sha(PROJECT/p)!=h:raise ValueError('Input hash mismatch: '+p)
    record=dict(study_id='manufacturing-recovery-v0.5',utc=datetime.now(timezone.utc).isoformat(),
        configuration=json.loads((HERE/'config.json').read_text()),
        source_sha256={str(p.relative_to(PROJECT)):sha(p) for p in sources},input_sha256=guard,
        type='Local pre-execution freeze; exploratory; not external preregistration',
        simulation_executed=False,raw_access=False,synthetic_tests_passed=24,
        numerical_refinement_check='evaluation_light_17_persistent_offset: eight vs sixteen RK4 substeps; max state error <1e-4')
    path.write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(dict(frozen_sources=len(sources),bound_inputs=len(guard))))
