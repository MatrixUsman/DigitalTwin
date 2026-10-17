"""Create a local editable archive and sealed revision inventory; never publish."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,zipfile,shutil
M=Path(__file__).resolve().parent;P=M.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
archive=P/'output/AFTER-Muhammad-Usman-v1.3-latex.zip'
selected=sorted(p for p in M.rglob('*') if p.is_file() and (
    p.suffix in ['.tex','.bib'] or (p.parent.name=='figures' and p.suffix=='.pdf') or
    p.name in ['README.md','REFERENCE_AUDIT.md','REVIEW_RESPONSE.md','CLAIM_LEDGER.md','build_pdf.py','generate_assets.py','render_references.py','ASSET_RECEIPT.json','REFERENCE_INDEX.json']))
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for p in selected:z.write(p,'AFTER-v1.3/'+str(p.relative_to(M)))
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for p in selected:assert hashlib.sha256(z.read('AFTER-v1.3/'+str(p.relative_to(M)))).hexdigest()==sha(p)
(M/'SOURCE_ARCHIVE.json').write_text(json.dumps({'path':str(archive.relative_to(P)),'sha256':sha(archive),'bytes':archive.stat().st_size,'files':len(selected),'contents':{str(p.relative_to(M)):sha(p) for p in selected},'raw_data_or_third_party_manuscripts_included':False},indent=2)+'\n')
snap=P/'local/manuscript_after_v1.3/completed_handoff';snap.mkdir(parents=True,exist_ok=True)
for name in ['AGENTS.md','STATUS.md','docs/WORK_LOG.md','docs/TEACHER_REVIEW_ACTIONS_V0.13.md']:
    dst=snap/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(P/name,dst)
files=[p for p in M.rglob('*') if p.is_file() and p.name!='PACKAGE_MANIFEST.json']
files+=list(p for p in snap.rglob('*') if p.is_file())
files+=[archive,P/'output/pdf/AFTER-Muhammad-Usman-v1.3.pdf',P/'output/pdf/AFTER-Muhammad-Usman-v1.3-supplement.pdf']
bindings={str(p.relative_to(P)):sha(p) for p in sorted(files)}
manifest={'utc':datetime.now(timezone.utc).isoformat(),'scope':'local manuscript revision; no submission or public release','files':len(bindings),'sha256':bindings}
(M/'PACKAGE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
assert all(sha(P/k)==v for k,v in bindings.items())
print(json.dumps({'archive':str(archive),'archive_files':len(selected),'package_bindings':len(bindings),'manifest_sha256':sha(M/'PACKAGE_MANIFEST.json')}))
