"""Fresh checkpoint-to-score verification; no fitting or new observations."""
from pathlib import Path
import sys,json
from datetime import datetime,timezone
H=Path(__file__).resolve().parent;P=H.parents[2]
sys.path[:0]=[str(H),str(P/'baselines/vendor/rapt_v020')]
import numpy as np,torch
torch.set_num_threads(1);torch.set_num_interop_threads(1)
from replay21 import check,sha,decisions,validate_population
from rapt import RaptConfig,RaptModel,NormStats,score_sequence
from rapt.detector import Calibration,risk_trajectory
f=check();checks=len(f['bindings']);manifest=json.loads((H/'INPUT_MANIFEST.json').read_text());validate_population(manifest['episodes']);checks+=1
out=P/'local/rapt_protocol_v0.21/exploratory_Q1_001';md=P/manifest['model_directory']
read=lambda n:json.loads((out/n).read_text())
sealed=read('SCORES_SEALED.json');assert not sealed['truth_opened'] and sealed['episodes']==36 and sealed['mode_outputs']==72;checks+=1
for name,digest in sealed['bindings'].items():assert sha(out/name)==digest;checks+=1
access=read('access.json');assert len(access)==73 and all(r['phase']=='score' for r in access[:36]) and all(r['phase']=='evaluation' for r in access[36:]);checks+=1
assert all(r['members']==['measurements','commands','valid'] for r in access[:36]);checks+=1
cfg=RaptConfig.from_json(md/'config.json');model=RaptModel(cfg);model.load_state_dict(torch.load(md/'model.pt',map_location='cpu',weights_only=True));model.eval()
stats=NormStats.from_dict(json.loads((md/'obs_stats.json').read_text()));cal=Calibration.from_dict(json.loads((md/'calibration.json').read_text()))
for row in manifest['episodes']:
    with np.load(P/row['score_path'],allow_pickle=False) as z:y=z['measurements'].astype(np.float32);u=z['commands'].astype(np.float32)
    loss=score_sequence(model,stats,y,u)
    with np.load(out/('score_'+row['id']+'.npz'),allow_pickle=False) as z:
        np.testing.assert_array_equal(z['loss'],loss);checks+=1
        for j,mode in enumerate([False,True]):
            risk=risk_trajectory(loss,y,cal,use_range=mode);np.testing.assert_array_equal(z['risk'][:,j],risk);checks+=1
            np.testing.assert_array_equal(z['alarm'][:,j],decisions(risk));checks+=1
assert read('result.json')['eligible_rows']==126000 and read('result.json')['events_per_mode']==24;checks+=1
assert read('supervisor.json')['status']=='completed';checks+=1
check();checks+=len(f['bindings'])
receipt=dict(utc=datetime.now(timezone.utc).isoformat(),status='passed',checks=checks,checkpoint_replayed_episodes=36,mode_outputs=72,command=sys.argv,cwd=str(P),training=False,fresh_confirmation=False,
    freeze_sha256=sha(H/'FREEZE.json'),output_bindings={str(p.relative_to(P)):sha(p) for p in sorted(out.iterdir()) if p.is_file()})
with (H/'VERIFICATION.json').open('x') as stream:json.dump(receipt,stream,indent=2);stream.write('\n')
print(json.dumps(dict(status='passed',checks=checks,checkpoint_replayed_episodes=36)))
