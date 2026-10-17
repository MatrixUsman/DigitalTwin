import sys,json,subprocess,shutil
from datetime import datetime,timezone
from common9 import HERE,OLD,PROJECT,LOCAL,INPUT,sha,config,normal_catalog,old_check
if (HERE/'FREEZE.json').exists():raise FileExistsError('Consumed freeze exists')
old=old_check();c=config();sources=list(HERE.glob('*.py'))+[HERE/'PLAN.md',HERE/'config.json',HERE/'PRIOR_ART.md']
hashes={str(p.relative_to(PROJECT)):sha(p) for p in sources}
d=LOCAL/'tests';d.mkdir(parents=True,exist_ok=True);n=len(list(d.glob('*.json')))+1
cmd=[sys.executable,str(HERE/'test_core.py')];r=subprocess.run(cmd,cwd=PROJECT,capture_output=True,text=True,timeout=60)
(d/f'tests_{n:03d}.log').write_text(r.stdout+r.stderr);(d/f'tests_{n:03d}.json').write_text(json.dumps(dict(command=cmd,returncode=r.returncode,source_sha256=hashes),indent=2)+'\n');print(r.stdout+r.stderr)
if r.returncode:raise SystemExit(r.returncode)
g=dict(old['source_sha256']);g.update(old['input_sha256'])
# Bind historic scientific package without treating mutable current handoffs as immutable data.
prior=json.loads((OLD/'PACKAGE_MANIFEST.json').read_text());history=PROJECT/'local/recovery_v0.8/title_revision/prior_handoff'
for key,h in prior['sha256'].items():
    path=PROJECT/key
    if sha(path)!=h:path=history/key
    assert sha(path)==h,key;g[str(path.relative_to(PROJECT))]=h
for p in [OLD/'FREEZE.json',OLD/'PACKAGE_MANIFEST.json',OLD/'HANDOFF_AUDIT.json']:
    g[str(p.relative_to(PROJECT))]=sha(p)
# Preserve latest title and handoff bytes before future mutable status/log edits.
for name in ['AGENTS.md','STATUS.md','README.md','docs/WORK_LOG.md','docs/PAPER_ROADMAP.md']:
    src=PROJECT/name;dst=LOCAL/'prior_handoff'/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst);g[str(dst.relative_to(PROJECT))]=sha(dst)
for name in ['docs/WORK_LOG.md','docs/RESEARCH_PLAYBOOK.md']:
    src=PROJECT.parent/name;dst=LOCAL/'prior_workspace'/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst);g[str(dst.relative_to(PROJECT))]=sha(dst)
for path in (PROJECT/'manuscript_recovery_v0.8r1').rglob('*'):
    if path.is_file():g[str(path.relative_to(PROJECT))]=sha(path)
p=PROJECT/'output/pdf/after-robotic-digital-twins.pdf';g[str(p.relative_to(PROJECT))]=sha(p)
normal={r['name']:sha(INPUT/r['name']) for r in normal_catalog(c)}
for name,h in normal.items():g[str((INPUT/name).relative_to(PROJECT))]=h
for plant in ['Q1','Q2','Q3']:
    p=INPUT/f'fit_{plant}.npz';g[str(p.relative_to(PROJECT))]=sha(p)
for root in [d,LOCAL/'sources']:
    for path in root.rglob('*'):
        if path.is_file():g[str(path.relative_to(PROJECT))]=sha(path)
for key,h in {**g,**hashes}.items():assert sha(PROJECT/key)==h,key
record=dict(utc=datetime.now(timezone.utc).isoformat(),configuration=c,source_sha256=hashes,input_sha256=g,normal_files=normal,normal_catalog=normal_catalog(c),
            prospective_scope='Finite model bank, normal-only selection/allowance/check protocol; fresh normal conditions ungenerated. Old v0.8 attacks exposed but not loaded for modeling.')
with (HERE/'FREEZE.json').open('x') as f:json.dump(record,f,indent=2);f.write('\n')
print(json.dumps(dict(sources=len(hashes),inputs=len(g),normal_files=len(normal))))
