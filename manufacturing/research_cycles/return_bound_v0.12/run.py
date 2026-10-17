"""One bounded, no-retry synthetic diagnostic; no training or dataset access."""
import sys
from datetime import datetime, timezone
from io_utils import HERE, PROJECT, RUN, check_frozen, sha256
sys.path.insert(0,str(PROJECT/'src'))
from mfg_twin.supervisor import BudgetWriter, Limits, supervise

f=check_frozen(); limits=Limits(**f['configuration']['limits'])
RUN.mkdir(parents=True,exist_ok=False)
writer=BudgetWriter(RUN,limit_bytes=limits.output_bytes)
command=[sys.executable,str(HERE/'worker.py'),'--output',str(RUN)]
writer.write_json('launch.json',dict(utc=datetime.now(timezone.utc).isoformat(),command=command,cwd=str(PROJECT),
                                  freeze_sha256=sha256(HERE/'FREEZE.json'),scope='small synthetic normal diagnostic, no training'))
result=supervise(command,cwd=PROJECT,output_dir=RUN,limits=limits,
                 env=dict(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1'))
writer.write_json('supervisor.json',result)
import json
print(json.dumps(result,indent=2))
raise SystemExit(0 if result['status']=='completed' else 1)
