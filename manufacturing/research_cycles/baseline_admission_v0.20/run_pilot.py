from pathlib import Path
import sys,json
H=Path(__file__).resolve().parent;P=H.parents[1]
sys.path.insert(0,str(P/'src'))
from mfg_twin.supervisor import Limits,BudgetWriter,supervise
out=P/'local/baseline_admission_v0.20/pilot_001';out.mkdir(parents=True,exist_ok=False)
lim=Limits(wall_seconds=60,cpu_seconds=50,rss_bytes=1073741824,output_bytes=5242880)
command=[sys.executable,str(H/'pilot_worker.py'),str(out)]
result=supervise(command,cwd=P,output_dir=out,limits=lim,env={'PYTHONDONTWRITEBYTECODE':'1','OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','VECLIB_MAXIMUM_THREADS':'1'})
BudgetWriter(out,limit_bytes=lim.output_bytes).write_json('supervisor.json',result)
print(json.dumps(result,indent=2))
raise SystemExit(0 if result['status']=='completed' else 1)
