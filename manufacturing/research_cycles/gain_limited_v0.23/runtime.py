from pathlib import Path
import sys,json
H=Path(__file__).resolve().parent;P=H.parents[1]
sys.path.insert(0,str(P/'src'))
from mfg_twin.supervisor import Limits,BudgetWriter,supervise
out=P/'local/gain_limited_v0.23/synthetic_runtime_001';out.mkdir(parents=True,exist_ok=False)
limits=Limits(wall_seconds=45,cpu_seconds=30,rss_bytes=1073741824,output_bytes=5242880)
r=supervise([sys.executable,str(H/'runtime_worker.py'),str(out)],cwd=P,output_dir=out,limits=limits,
    env={'PYTHONDONTWRITEBYTECODE':'1','OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','VECLIB_MAXIMUM_THREADS':'1'})
BudgetWriter(out,limit_bytes=limits.output_bytes).write_json('supervisor.json',r)
print(json.dumps(r,indent=2));raise SystemExit(0 if r['status']=='completed' else 1)