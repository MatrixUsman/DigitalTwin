"""Fresh-process verification of the completed normal-only run; no training."""
from pathlib import Path
import sys,json
from datetime import datetime,timezone
H=Path(__file__).resolve().parent;P=H.parents[1]
sys.path[:0]=[str(H),str(P/'baselines/vendor/rapt_v020')]
import numpy as np,torch
torch.set_num_threads(1);torch.set_num_interop_threads(1)
from protocol21 import check,load_role,calibrate_eligible,curve_summary,sha,START
from rapt import RaptConfig,RaptModel,NormStats,score_sequence
from rapt.detector import risk_trajectory

f=check();checks=len(f['bindings']);out=P/'local/rapt_protocol_v0.21/raw_Q1_seed17_001'
read=lambda n:json.loads((out/n).read_text())
cfg=RaptConfig.from_json(out/'config.json');model=RaptModel(cfg)
model.load_state_dict(torch.load(out/'model.pt',map_location='cpu',weights_only=True));model.eval()
stats=NormStats.from_dict(read('obs_stats.json'));manifest=json.loads((H/'INPUT_MANIFEST.json').read_text());access=[]
for name,h in read('SELECTION_SEALED.json')['bindings'].items():assert sha(out/name)==h;checks+=1
assert curve_summary(read('history.json'))==read('selection.json');checks+=1
recorded=read('access.json');roles=[r['role'] for r in recorded]
assert roles[:18]==['fit']*9+['development']*9 and roles[18:27]==['calibration']*9;checks+=1
tr=load_role(manifest,'Q1','fit',access,trim=True);recomputed=NormStats.from_data(tr)
for key in ['mean','std','min','max']:np.testing.assert_array_equal(getattr(stats,key),getattr(recomputed,key));checks+=1
caldata=load_role(manifest,'Q1','calibration',access);losses=[score_sequence(model,stats,y,u) for y,u in zip(caldata.obs,caldata.actions)]
cal=calibrate_eligible(losses,caldata.obs,cfg);assert cal.to_dict()==read('calibration.json');checks+=1
dev=load_role(manifest,'Q1','development',access);rows=[]
with np.load(out/'normal_development_scores.npz',allow_pickle=False) as saved:
 for i,(y,u) in enumerate(zip(dev.obs,dev.actions)):
  loss=score_sequence(model,stats,y,u);np.testing.assert_array_equal(saved[f'loss_{i:02d}'],loss);checks+=1
  for mode in [False,True]:
   key='hybrid' if mode else 'model';risk=risk_trajectory(loss,y,cal,use_range=mode)
   np.testing.assert_array_equal(saved[f'{key}_{i:02d}'],risk.astype(np.float32));checks+=1
   rows.append(dict(episode=dev.names[i],method=key,eligible=1100,point_alarms=int((risk[START:]>1).sum()),max_risk=float(risk[START:].max())))
assert rows==read('result.json')['rows'];checks+=1
log=(out/'worker.log').read_text();assert sum(line.startswith('epoch ') for line in log.splitlines())==100;checks+=1
assert read('supervisor.json')['status']=='completed';checks+=1
receipt=dict(utc=datetime.now(timezone.utc).isoformat(),checks=checks,status='passed',normal_only=True,
    command=sys.argv,cwd=str(P),freeze_sha256=sha(H/'FREEZE.json'),
    output_bindings={str(p.relative_to(P)):sha(p) for p in sorted(out.iterdir()) if p.is_file()},
    raw_source_access=['synthetic K13','synthetic M13','synthetic L13'],training_performed=False,final_test_access=False)
with (H/'VERIFICATION.json').open('x') as stream:json.dump(receipt,stream,indent=2);stream.write('\n')
print(json.dumps({'checks':checks,'status':'passed','normal_development_points':9900,'alarms_per_method':313}))
