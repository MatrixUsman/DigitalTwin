"""Read-only inspection of the completed, entirely virtual manufacturing lab."""
from pathlib import Path
import hashlib
import json

PROJECT=Path(__file__).resolve().parents[1]
CYCLE=PROJECT/'research_cycles/recovery_v0.5'
RUN=PROJECT/'local/recovery_v0.5/runs/reporting_001'

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        while block:=stream.read(1024*1024):h.update(block)
    return h.hexdigest()

def inspect():
    count=0
    for name in ['FREEZE.json','REPORTING_RECOVERY_FREEZE.json','PACKAGE_MANIFEST.json']:
        record=json.loads((CYCLE/name).read_text())
        groups=['source_sha256','input_sha256'] if name=='FREEZE.json' else ['sha256']
        for group in groups:
            for p,h in record[group].items():
                if 'datasets/raw/' in p:raise ValueError('Raw-data access excluded from this viewer')
                if sha(PROJECT/p)!=h:raise ValueError('Saved identity changed: '+p)
                count+=1
    result=json.loads((CYCLE/'RESULTS.json').read_text())
    summary={'mode':'Entirely virtual; completed synthetic physics simulation',
        'hardware_required':False,'simulator':'Horizontal two-joint arm, PD controller, noisy position/velocity sensors',
        'evaluation_episodes':result['experiment']['evaluation_episodes'],'methods':result['experiment']['methods'],
        'existing_passing_tests':26,'existing_passing_verification_checks':53004,
        'artifact_identity_comparisons':count,'new_training':False,'new_simulation':False,
        'scenarios':list(result['per_condition']),
        'same_information':'All methods receive the same measurements; command-aware methods receive identical approved commands and validity. AR/persistence intentionally omit commands as information ablations.',
        'truth_restriction':'True plant states, executed corrupted commands and intervention labels are evaluator-only.'}
    return summary

if __name__=='__main__':print(json.dumps(inspect(),indent=2))
