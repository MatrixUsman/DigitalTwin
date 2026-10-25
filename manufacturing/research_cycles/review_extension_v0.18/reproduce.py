"""Explicit fresh-destination replay under unchanged limits; not auto-executed."""
import argparse,json,sys
from datetime import datetime,timezone
from common import HERE,PROJECT,check,sha
from mfg_twin.supervisor import Limits,BudgetWriter,supervise
p=argparse.ArgumentParser();p.add_argument('--attempt',required=True,help='New basename under this cycle/runs');args=p.parse_args()
if not args.attempt or '/' in args.attempt or '\\' in args.attempt or args.attempt in ['.','..']:p.error('simple new basename required')
f=check();limits=Limits(**f['configuration']['limits']);out=HERE/'runs'/args.attempt
out.mkdir(parents=True,exist_ok=False);w=BudgetWriter(out,limit_bytes=limits.output_bytes)
command=[sys.executable,str(HERE/'worker.py'),'--output',str(out)]
w.write_json('launch.json',dict(utc=datetime.now(timezone.utc).isoformat(),command=command,cwd=str(PROJECT),
  reproduction_source_sha256=sha(HERE/'reproduce.py'),freeze_sha256=sha(HERE/'FREEZE.json'),
  scope='exact replay of exposed saved synthetic data; no model fitting or new simulation'))
r=supervise(command,cwd=PROJECT,output_dir=out,limits=limits,env={'PYTHONDONTWRITEBYTECODE':'1'})
w.write_json('supervisor.json',r);print(json.dumps(r,indent=2));raise SystemExit(0 if r['status']=='completed' else 1)
