from pathlib import Path
import hashlib,json,numpy as np
H=Path(__file__).resolve().parent;P=H.parents[1];R=P/'local/fivefold_v0.16/runs/validation_002'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
s=json.loads((R/'summary.json').read_text());seal=json.loads((R/'OUTPUT_SEAL.json').read_text());checks=0
for f,d in seal['sha256'].items():assert sha(R/f)==d;checks+=1
rows=[]
for o in s['outcomes']:
    if o['status']!='completed':continue
    with np.load(R/f'{o["plant"]}_fold{o["fold"]}_scores.npz',allow_pickle=False) as z:
        val=np.sqrt(np.mean(z['standardized_error']**2,axis=(0,2)))
        np.testing.assert_array_equal(val,o['standardized_rmse']);checks+=1
        np.testing.assert_array_equal(np.sqrt(np.mean(z['native_error']**2,axis=0)),o['native_channel_rmse']);checks+=1
        assert np.array_equal(z['source_row'],np.tile(np.arange(*o['bounds']['scored']),3));checks+=1
        rows.append((o['fold'],o['plant'],val))
folds=[]
for k in range(1,6):
    vals=np.array([v for f,p,v in rows if f==k])
    folds.append({'fold':k,'arx_rmse':float(np.sqrt(np.mean(vals[:,0]**2))),
                  'arx_rbf_rmse':float(np.sqrt(np.mean(vals[:,1]**2))),'targets':int(300*len(vals))})
v={'checks':checks,'passed':True,'folds':folds,'improved_plant_folds':int(sum(v[1]<v[0] for _,_,v in rows)),
   'total_plant_folds':15,'summary_sha256':sha(R/'summary.json'),'output_seal_sha256':sha(R/'OUTPUT_SEAL.json'),
   'scope':'saved scores recomputed, no model refit','reporting_repair':'Initial report JSON export rejected a numpy.int64 count; converted only that scalar to Python int. Scientific artifacts unchanged.'}
(H/'VERIFICATION.json').write_text(json.dumps(v,indent=2)+'\n')
print(json.dumps(v,indent=2))
