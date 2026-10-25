from pathlib import Path
import sys,json,hashlib
H=Path(__file__).resolve().parent;P=H.parents[1]
sys.path.insert(0,str(P/'src'))
from mfg_twin.supervisor import Limits,BudgetWriter,supervise,directory_bytes
cfg=json.loads((H/'config.json').read_text());limits=Limits(**cfg['limits'])
out=P/'local/gain_limited_v0.23/normal_001';out.mkdir(parents=True,exist_ok=False)
r=supervise([sys.executable,str(H/'worker.py'),str(out)],cwd=P,output_dir=out,limits=limits,
    env={'PYTHONDONTWRITEBYTECODE':'1','OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','VECLIB_MAXIMUM_THREADS':'1'})
BudgetWriter(out,limit_bytes=limits.output_bytes).write_json('supervisor.json',r)
if r['status']=='completed':
    freeze=json.loads((H/'FREEZE.json').read_text());inputs=all(hashlib.sha256((P/path).read_bytes()).hexdigest()==digest for path,digest in freeze['bindings'].items())
    result=json.loads((out/'result.json').read_text());decision=json.loads((out/'admission.json').read_text());tests=json.loads((H/'TEST_RECEIPT.json').read_text())
    execution=dict(supervisor_completed=True,wall_within_cap=r['wall_seconds']<=limits.wall_seconds,cpu_within_cap=result['usage']['process_cpu_seconds']<=limits.cpu_seconds,
        sampled_rss_within_cap=r['sampled_peak_rss_bytes']<=limits.rss_bytes,outputs_within_cap=directory_bytes(out)<=limits.output_bytes,
        frozen_inputs_unchanged=inputs,synthetic_tests_passed=tests['status']=='passed',complete_methods=result['methods']==33)
    final=dict(passed=decision['passed'] and all(execution.values()),scientific=decision,execution_clauses=execution,
        fresh_attack_admitted=False,novelty_established=False,operational_tolerance_established=False)
    BudgetWriter(out,limit_bytes=limits.output_bytes).write_json('FINAL_ADMISSION.json',final)
print(json.dumps(r,indent=2));raise SystemExit(0 if r['status']=='completed' else 1)
