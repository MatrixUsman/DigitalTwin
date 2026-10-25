from pathlib import Path
import sys,json
H=Path(__file__).resolve().parent;P=H.parents[2]
sys.path.insert(0,str(P/'src'))
from mfg_twin.supervisor import Limits,BudgetWriter,supervise
out=P/'local/novelty_v0.22/decomposition_001'
out.mkdir(parents=True,exist_ok=False)
limits=Limits(wall_seconds=60,cpu_seconds=45,rss_bytes=1073741824,output_bytes=26214400)
result=supervise([sys.executable,str(H/'worker.py'),str(out)],cwd=P,output_dir=out,limits=limits,
    env={'PYTHONDONTWRITEBYTECODE':'1','OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','VECLIB_MAXIMUM_THREADS':'1'})
BudgetWriter(out,limit_bytes=limits.output_bytes).write_json('supervisor.json',result)
print(json.dumps(result,indent=2));raise SystemExit(0 if result['status']=='completed' else 1)
