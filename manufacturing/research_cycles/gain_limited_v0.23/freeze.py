"""Freeze once after independent review; hashes only, no normal-array loading."""
from pathlib import Path
import hashlib,json
from datetime import datetime,timezone
H=Path(__file__).resolve().parent;P=H.parents[1]
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
test=json.loads((H/'TEST_RECEIPT.json').read_text())
if test['status']!='passed':raise ValueError('Passing tests required')
for path,digest in test['bindings'].items():
    if sha(P/path)!=digest:raise ValueError('Changed tested source '+path)
review=json.loads((H/'REVIEW_RELEASE.json').read_text())
if not review.get('admitted'):raise ValueError('Independent review release required')
for path,digest in review['bindings'].items():
    if sha(P/path)!=digest:raise ValueError('Changed reviewed source '+path)
manifest=json.loads((H/'INPUT_MANIFEST.json').read_text());bindings={r['path']:r['sha256'] for r in manifest['files']}
for path,digest in bindings.items():
    if sha(P/path)!=digest:raise ValueError('Changed admitted normal input')
files=list(H.glob('*.py'))+[H/n for n in ['PROTOCOL.md','config.json','INPUT_MANIFEST.json','TEST_RECEIPT.json','REVIEW_RELEASE.json','RUNTIME_ADMISSION.json']]
files += [P/'src/mfg_twin/supervisor.py',P/'.venv-analysis-v022/bin/python',P/'.venv-analysis-v022/pyvenv.cfg',P/'.venv-analysis-v022/lib/python3.12/site-packages/forecast_v016_bridge.pth',P/'research_cycles/novelty_v0.22/decomposition/RUNTIME_BRIDGE.json',P/'local/gain_limited_v0.23/synthetic_runtime_001/runtime.json',P/'local/gain_limited_v0.23/synthetic_runtime_001/supervisor.json']
for path in files:bindings[str(path.relative_to(P))]=sha(path)
record=dict(utc=datetime.now(timezone.utc).isoformat(),configuration=json.loads((H/'config.json').read_text()),bindings=bindings)
with (H/'FREEZE.json').open('x') as f:json.dump(record,f,indent=2,sort_keys=True);f.write('\n')
print(json.dumps(dict(bindings=len(bindings),freeze_sha256=sha(H/'FREEZE.json'))))
