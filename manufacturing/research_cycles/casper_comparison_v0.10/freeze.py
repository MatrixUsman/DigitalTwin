from pathlib import Path
from datetime import datetime,timezone
import json,os,subprocess,sys,time,re
from io_utils import sha256
HERE=Path(__file__).resolve().parent;P=HERE.parents[1];target=HERE/'FREEZE.json'
if target.exists():raise ValueError('Preserve existing freeze')
out=P/'local/casper_comparison_v0.10/tests/test_001';out.mkdir(parents=True,exist_ok=False)
files=sorted(list(HERE.glob('*.py'))+[HERE/'PLAN.md',HERE/'config.json'])
files += [P/'src/mfg_twin/supervisor.py',P/'research_cycles/contribution_v0.2/requirements-macos-arm64.lock.txt',
          P/'baselines/casper/artifacts/casper_corrected_vor_v1.1.pdf',P/'local/contribution_v0.2/sources/edge_paper.pdf',
          P/'research_cycles/commissioning_v0.9/PACKAGE_MANIFEST.json',P/'manuscript_after_v1.0/PACKAGE_MANIFEST.json']
sources={str(f.relative_to(P)):sha256(f) for f in files};env=dict(os.environ,TF_NUM_INTRAOP_THREADS='1',TF_NUM_INTEROP_THREADS='1',TF_CPP_MIN_LOG_LEVEL='2',CUDA_VISIBLE_DEVICES='-1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1')
cmd=[sys.executable,'-m','unittest','discover','-s',str(HERE),'-p','test_*.py','-v'];start=time.monotonic()
with (out/'tests.log').open('w') as stream:r=subprocess.run(cmd,cwd=P,env=env,stdout=stream,stderr=subprocess.STDOUT,timeout=120)
content=(out/'tests.log').read_text();print(content[-4500:]);count=re.search(r'Ran (\d+) tests',content)
receipt=dict(utc=datetime.now(timezone.utc).isoformat(),returncode=r.returncode,command=cmd,cwd=str(P),wall_seconds=time.monotonic()-start,
             synthetic=True,raw_data_access=False,tests=int(count.group(1)) if count else None,log_sha256=sha256(out/'tests.log'))
(out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
if r.returncode:raise SystemExit(r.returncode)
assert all(sha256(P/k)==v for k,v in sources.items())
target.write_text(json.dumps(dict(utc=datetime.now(timezone.utc).isoformat(),configuration=json.loads((HERE/'config.json').read_text()),source_sha256=sources,
    test_receipt=str((out/'receipt.json').relative_to(P)),test_receipt_sha256=sha256(out/'receipt.json'),data_access=False,
    environment=subprocess.check_output([sys.executable,'-m','pip','freeze'],text=True),command='freeze.py before run.py'),indent=2)+'\n')
print('Frozen before data access:',len(sources),'sources;',receipt['tests'],'synthetic tests.')
