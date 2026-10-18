"""Package the single manuscript and preserve final hashes after visual review."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, re, zipfile

M = Path(__file__).resolve().parent
P = M.parent
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
audit = json.loads((M/'AUDIT.json').read_text())
visual = json.loads((M/'VISUAL_QA.json').read_text())
assert audit['passed'] and visual['passed']
pdf = P/'output/pdf/ARX-RBF-Muhammad-Usman-v1.6.pdf'
assert sha(pdf) == audit['pdf_sha256'] == visual['pdf_sha256']
files = {Path('main.tex'),Path('references.bib'),Path('README.md')}
pending = [Path('main.tex')]
while pending:
    f = pending.pop()
    content = (M/f).read_text()
    for target in re.findall(r'\\input\{([^}]+)\}',content):
        path = Path(target)
        if not path.suffix:
            path = path.with_suffix('.tex')
        assert (M/path).is_file(), path
        if path not in files:
            files.add(path); pending.append(path)
    for target in re.findall(r'\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}',content):
        path = Path(target)
        assert (M/path).is_file(), path
        files.add(path)
archive = P/'output/ARX-RBF-Muhammad-Usman-v1.6-latex.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
    for f in sorted(files):
        z.write(M/f,arcname=str(f))
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert set(z.namelist()) == {str(f) for f in files}
    for f in files:
        assert z.read(str(f)) == (M/f).read_bytes()
receipt = {'utc':datetime.now(timezone.utc).isoformat(),'file':str(archive.relative_to(P)),
    'sha256':sha(archive),'files':len(files),'crc_passed':True,'exact_bytes':True,'all_dependencies_resolved':True,
    'scope':'Single LaTeX document with figures and bibliography; no dataset, upstream checkout or separate supplement',
    'members':{str(f):sha(M/f) for f in sorted(files)}}
(M/'SOURCE_ARCHIVE.json').write_text(json.dumps(receipt,indent=2)+'\n')
targets = [f for f in M.rglob('*') if f.is_file() and f.name!='PACKAGE_MANIFEST.json' and '__pycache__' not in f.parts]
targets += [archive,pdf]
handoff = P/'local/manuscript_arx_rbf_v1.6/completed_handoff'
targets += [f for f in handoff.rglob('*') if f.is_file()]
manifest = {'utc':datetime.now(timezone.utc).isoformat(),'scope':'Completed revision 1.6 and recorded final handoff; underlying scientific packages separately sealed',
    'files':len(targets),'sha256':{str(f.relative_to(P)):sha(f) for f in sorted(targets)}}
(M/'PACKAGE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'archive':receipt['file'],'files':len(files),'manifest_bindings':len(targets),'archive_sha256':sha(archive)}))
