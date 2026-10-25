"""Post-run read-back only; reproduces saved neural corrections without fitting."""
from pathlib import Path
import hashlib,json,time,sys,platform
from datetime import datetime,timezone
import numpy as np
import torch
H=Path(__file__).resolve().parent;P=H.parents[1];out=P/'local/gain_limited_v0.23/normal_001'
torch.set_num_threads(1);torch.set_num_interop_threads(1);torch.use_deterministic_algorithms(True)
from models23 import Adapter,adapter_predict_many
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
started=datetime.now(timezone.utc).isoformat();tick=time.perf_counter();cpu=time.process_time()
freeze=json.loads((H/'FREEZE.json').read_text());checks=0
for path,digest in freeze['bindings'].items():assert sha(P/path)==digest,path;checks+=1
cfg=json.loads((H/'config.json').read_text());rows=json.loads((out/'methods.json').read_text())
with np.load(out/'normalized_records.npz',allow_pickle=False) as z:
    zs=list(z['fit_y']-z['fit_base'])+list(z['development_y']-z['development_base']);cs=list(z['fit_context'])+list(z['development_context'])
replays=[]
for row in rows:
    if row['family'] not in ['context','constrained','unconstrained']:continue
    cert=row['metrics']['certificate'];model=Adapter(row['kappa_budget'],cert['rho_budget'],cfg['tanh']['width'],cfg['model_seed'],row['family'])
    model.load_state_dict(torch.load(out/('model_'+row['id']+'.pt'),map_location='cpu',weights_only=True));model.eval()
    with np.load(out/('model_'+row['id']+'.npz'),allow_pickle=False) as z:
        for key,value in model.state_dict().items():assert np.array_equal(value.numpy(),z[key]);checks+=1
    predicted=np.stack(adapter_predict_many(model,zs,cs)[9:])
    with np.load(out/('prediction_'+row['id']+'.npz'),allow_pickle=False) as z:saved=z['correction']
    exact=bool(np.array_equal(predicted,saved));maximum=float(np.max(np.abs(predicted-saved)))
    assert exact,(row['id'],maximum);checks+=1
    assert model.certificate()==cert;checks+=1
    replays.append(dict(id=row['id'],scalars=int(saved.size),exact=exact,maximum_difference=maximum))
assert len(replays)==9;checks+=1
for path,digest in freeze['bindings'].items():assert sha(P/path)==digest,path;checks+=1
record=dict(utc=started,completed_utc=datetime.now(timezone.utc).isoformat(),command=sys.argv,cwd=str(P),interpreter=sys.executable,python=sys.version,
    platform=platform.platform(),torch=torch.__version__,numpy=np.__version__,checks=checks,models=9,exact_prediction_scalars=sum(r['scalars'] for r in replays),
    replays=replays,wall_seconds=time.perf_counter()-tick,cpu_seconds=time.process_time()-cpu,training=False,new_data_access=False,
    input_freeze_sha256=sha(H/'FREEZE.json'),verifier_sha256=sha(Path(__file__)),independent_implementation=False)
with (H/'RELOAD_VERIFICATION.json').open('x') as f:json.dump(record,f,indent=2);f.write('\n')
print(json.dumps(dict(checks=checks,models=9,exact_prediction_scalars=record['exact_prediction_scalars'],wall_seconds=record['wall_seconds'])))
