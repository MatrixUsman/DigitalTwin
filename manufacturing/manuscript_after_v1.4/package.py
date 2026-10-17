"""Package the one-paper source locally and seal the completed handoff."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, re, shutil, zipfile
M=Path(__file__).resolve().parent; P=M.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
archive=P/'output/AFTER-Muhammad-Usman-v1.4-latex.zip'
main=(M/'main.tex').read_text()
tex=[M/'main.tex',M/'references.tex']
tex += [M/(n+'.tex') for n in re.findall(r'\\input\{(sections/[^}]+)\}',main)]
alltext='\n'.join(p.read_text() for p in tex)
tex += [M/(n if n.endswith('.tex') else n+'.tex') for n in re.findall(r'\\input\{(generated/[^}]+)\}',alltext)]
figures=[M/n for n in re.findall(r'\\includegraphics\[[^]]+\]\{([^}]+)\}',alltext)]
meta=['references.bib','README.md','STRUCTURE_MAPPING.md','REVIEW_RESPONSE.md','REFERENCE_AUDIT.md','CLAIM_LEDGER.md','REFERENCE_INDEX.json','ASSET_RECEIPT.json','FIGURE_VALUES.json','build_pdf.py','generate_assets.py','render_references.py','assemble_revision.py']
selected=sorted(set(tex+figures+[M/n for n in meta]))
assert len(figures)==7 and all(p.exists() for p in selected)
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for p in selected:z.write(p,'AFTER-v1.4/'+str(p.relative_to(M)))
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for p in selected:assert hashlib.sha256(z.read('AFTER-v1.4/'+str(p.relative_to(M)))).hexdigest()==sha(p)
    names=set(z.namelist())
    for name in names:
        if not name.endswith('.tex'):continue
        for kind,target in re.findall(r'\\(input|includegraphics)(?:\[[^]]*\])?\{([^}]+)\}',z.read(name).decode()):
            if kind=='input' and not target.endswith('.tex'):target+='.tex'
            assert 'AFTER-v1.4/'+target in names,target
    assert all('supplement' not in n and 'bxae132' not in n and 'datasets/' not in n for n in names)
(M/'SOURCE_ARCHIVE.json').write_text(json.dumps({'path':str(archive.relative_to(P)),'sha256':sha(archive),'bytes':archive.stat().st_size,'files':len(selected),'contents':{str(p.relative_to(M)):sha(p) for p in selected},'documents':['main.tex'],'all_LaTeX_inputs_present':True,'raw_data_or_third_party_manuscripts_included':False},indent=2)+'\n')
snap=P/'local/manuscript_after_v1.4/completed_handoff';snap.mkdir(parents=True,exist_ok=True)
for name in ['AGENTS.md','STATUS.md','docs/WORK_LOG.md','docs/TEACHER_REVIEW_ACTIONS_V0.13.md']:
    dst=snap/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(P/name,dst)
files=[p for p in M.rglob('*') if p.is_file() and p.name!='PACKAGE_MANIFEST.json']
files += [p for p in snap.rglob('*') if p.is_file()]
files += [archive,P/'output/pdf/AFTER-Muhammad-Usman-v1.4.pdf']
bindings={str(p.relative_to(P)):sha(p) for p in sorted(files)}
manifest={'utc':datetime.now(timezone.utc).isoformat(),'scope':'single-paper local editorial revision and saved-result plots; no submission or public release','files':len(bindings),'sha256':bindings}
(M/'PACKAGE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
assert all(sha(P/k)==h for k,h in bindings.items())
print(json.dumps({'archive':str(archive),'files':len(selected),'package_bindings':len(bindings),'manifest_sha256':sha(M/'PACKAGE_MANIFEST.json')}))
