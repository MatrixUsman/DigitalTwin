"""Offline build with the existing verified compiler; preserve every attempt."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, os, shutil, subprocess

M=Path(__file__).resolve().parent; P=M.parent
LOCAL=P/'local/pdf_build_v0.1'
ROOT=P/'local/manuscript_after_v1.0/pdf_build'
OUTPUT=P/'output/pdf/AFTER-manuscript.pdf'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
parser=argparse.ArgumentParser()
parser.add_argument('--allow-resource-downloads',action='store_true',help='Fetch missing compiler fonts/resources into this study cache; no manuscript upload.')
args=parser.parse_args()
release=json.loads((LOCAL/'tectonic_release.json').read_text())
asset=next(a for a in release['assets'] if a['name']=='tectonic-0.17.0-aarch64-apple-darwin.tar.gz')
assert 'sha256:'+sha(LOCAL/'tectonic.tar.gz')==asset['digest']
ROOT.mkdir(parents=True,exist_ok=True)
attempt=ROOT/f'attempt_{len(list(ROOT.glob("attempt_*")))+1:03d}'
attempt.mkdir()
files=sorted([p for p in M.rglob('*') if p.suffix in ['.tex','.pdf','.py'] and p.is_file()])
sources={str(p.relative_to(M)):sha(p) for p in files}
cache=P/'local/recovery_v0.7/pdf_build/cache'
if not cache.exists():shutil.copytree(LOCAL/'cache',cache)
env=dict(os.environ);env['TECTONIC_CACHE_DIR']=str(cache)
cmd=[str(LOCAL/'bin/tectonic'),'--untrusted','--keep-logs','--keep-intermediates','--outdir',str(attempt)]
if not args.allow_resource_downloads:cmd.append('--only-cached')
cmd.append('main.tex')
receipt=dict(started_utc=datetime.now(timezone.utc).isoformat(),command=cmd,cwd=str(M),
    compiler_sha256=sha(LOCAL/'bin/tectonic'),compiler_version=subprocess.check_output([str(LOCAL/'bin/tectonic'),'--version'],text=True).strip(),
    offline=not args.allow_resource_downloads,source_sha256=sources,attempt=str(attempt.relative_to(P)))
with (attempt/'stdout.log').open('w') as f:
    result=subprocess.run(cmd,cwd=M,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=180)
receipt.update(returncode=result.returncode,completed_utc=datetime.now(timezone.utc).isoformat(),
               sources_unchanged=all(sha(M/k)==v for k,v in sources.items()))
if result.returncode==0:
    assert receipt['sources_unchanged']
    pdf=attempt/'main.pdf';assert pdf.read_bytes().startswith(b'%PDF-')
    OUTPUT.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(pdf,OUTPUT)
    receipt.update(pdf=str(OUTPUT.relative_to(P)),pdf_sha256=sha(OUTPUT),bytes=OUTPUT.stat().st_size,
                   visual_review='Pending separate rendered-page inspection')
(attempt/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
if result.returncode:raise SystemExit('Build failed; preserved '+str(attempt/'stdout.log'))
(M/'BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:receipt[k] for k in ['attempt','returncode','pdf','pdf_sha256','bytes']}))
