from pathlib import Path
import hashlib,json
from datetime import datetime,timezone
H=Path(__file__).resolve().parent;P=H.parents[2]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
old=P/'research_cycles/rapt_protocol_v0.21/exploratory'
test=json.loads((H/'TEST_RECEIPT.json').read_text())
if test.get('status')!='passed' or test.get('tests')!=6:raise ValueError('Six passing synthetic tests required')
for path,digest in test['bindings'].items():
    if sha(P/path)!=digest:raise ValueError('Changed source after synthetic tests: '+path)
prior=json.loads((old/'FREEZE.json').read_text());bindings=dict(prior['bindings'])
for p,d in bindings.items():
    if sha(P/p)!=d:raise ValueError('Changed prior freeze '+p)
manifest=json.loads((old/'INPUT_MANIFEST.json').read_text())
out=P/'local/rapt_protocol_v0.21/exploratory_Q1_001'
sealed=json.loads((out/'SCORES_SEALED.json').read_text())
for r in manifest['episodes']:
    name='score_'+r['id']+'.npz';path=out/name
    if sha(path)!=sealed['bindings'][name]:raise ValueError('Changed original replay score '+name)
    r['prior_rapt_score_path']=str(path.relative_to(P))
    bindings[str(path.relative_to(P))]=sha(path)
    # Truth values are excluded from the new loader; schedule comes from the frozen config.
    del r['truth_path']
manifest.pop('evaluation_scale_path',None)
with (H/'INPUT_MANIFEST.json').open('x') as stream:json.dump(manifest,stream,indent=2);stream.write('\n')
for path in list(H.glob('*.py'))+[H/'PROTOCOL.md',H/'TEST_RECEIPT.json',H/'INPUT_MANIFEST.json',H/'RUNTIME_BRIDGE.json',
    P/'.venv-analysis-v022/pyvenv.cfg',P/'.venv-analysis-v022/bin/python',P/'.venv-analysis-v022/lib/python3.12/site-packages/forecast_v016_bridge.pth',
    old/'FREEZE.json',old/'INPUT_MANIFEST.json',out/'SCORES_SEALED.json',P/'research_cycles/context_recovery_v0.19/config.json']:
    bindings[str(path.relative_to(P))]=sha(path)
record=dict(utc=datetime.now(timezone.utc).isoformat(),configuration=dict(study='manufacturing-rapt-score-decomposition-v0.22',
    episodes=36,model_seed=17,selected_epoch=14,warmup=100,wall_seconds=60,cpu_seconds=45,rss_bytes=1073741824,output_bytes=26214400,
    training=False,new_thresholds=False,new_reference=False,fresh_confirmation=False,truth_access=False),bindings=bindings)
with (H/'FREEZE.json').open('x') as stream:json.dump(record,stream,indent=2,sort_keys=True);stream.write('\n')
print(json.dumps(dict(bindings=len(bindings),freeze_sha256=sha(H/'FREEZE.json'))))
