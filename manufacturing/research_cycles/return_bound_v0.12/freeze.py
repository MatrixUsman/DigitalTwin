"""Run only synthetic software tests, then seal the unexecuted design."""
import json
import argparse
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from io_utils import HERE, PROJECT, LOCAL, sha256

if (HERE/'FREEZE.json').exists(): raise ValueError('Freeze already exists; preserve it.')
parser=argparse.ArgumentParser();parser.add_argument('--test-attempt',default='test_001');args=parser.parse_args()
if not re.fullmatch(r'test_[0-9]{3}',args.test_attempt): raise ValueError('invalid test attempt')
out=LOCAL/'tests'/args.test_attempt; out.mkdir(parents=True, exist_ok=False)
files=sorted(list(HERE.glob('*.py'))+[HERE/'PLAN.md',HERE/'PRIOR_ART.md',HERE/'config.json'])
files.append(HERE/'TEST_DEVELOPMENT.md')
files += [PROJECT/'src/mfg_twin/supervisor.py', PROJECT/'src/mfg_twin/__init__.py']
prior=['research_cycles/commissioning_v0.9/PACKAGE_MANIFEST.json',
       'research_cycles/casper_comparison_v0.10/PACKAGE_MANIFEST.json',
       'research_cycles/casper_convergence_v0.11/PACKAGE_MANIFEST.json',
       'manuscript_after_v1.0/PACKAGE_MANIFEST.json']
files += [PROJECT/name for name in prior]
sources={str(p.relative_to(PROJECT)):sha256(p) for p in files}
command=[sys.executable,'-m','unittest','discover','-s',str(HERE),'-p','test_*.py','-v']
env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
tick=time.monotonic()
with (out/'tests.log').open('x') as stream:
    result=subprocess.run(command,cwd=PROJECT,env=env,stdout=stream,stderr=subprocess.STDOUT,timeout=60)
content=(out/'tests.log').read_text(); match=re.search(r'Ran (\d+) tests',content)
receipt=dict(utc=datetime.now(timezone.utc).isoformat(),returncode=result.returncode,
             tests=int(match.group(1)) if match else None,command=command,cwd=str(PROJECT),
             wall_seconds=time.monotonic()-tick,synthetic=True,raw_data_access=False,log_sha256=sha256(out/'tests.log'),source_sha256=sources)
(out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n'); print(content)
if result.returncode: raise SystemExit(result.returncode)
assert all(sha256(PROJECT/name)==digest for name,digest in sources.items())
freeze=dict(utc=datetime.now(timezone.utc).isoformat(),configuration=json.loads((HERE/'config.json').read_text()),
            source_sha256=sources,prior_packages=prior,test_receipt=str((out/'receipt.json').relative_to(PROJECT)),
            test_receipt_sha256=sha256(out/'receipt.json'),python=sys.version,
            dependencies=subprocess.check_output([sys.executable,'-m','pip','freeze'],text=True),
            scientific_status='standard control; prospective synthetic normal diagnostic; no generated study outcomes yet')
with (HERE/'FREEZE.json').open('x') as stream: json.dump(freeze,stream,indent=2);stream.write('\n')
print('Frozen',len(sources),'identities after',receipt['tests'],'tests; no study signals generated.')
