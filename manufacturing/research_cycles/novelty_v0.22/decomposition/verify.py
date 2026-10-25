"""Saved-array verification; no model inference or core summary helpers."""
from pathlib import Path
import hashlib,json,math
from datetime import datetime,timezone
import numpy as np
H=Path(__file__).resolve().parent;P=H.parents[2]
out=P/'local/novelty_v0.22/decomposition_001'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
freeze=json.loads((H/'FREEZE.json').read_text());count=0
for path,digest in freeze['bindings'].items():
    assert sha(P/path)==digest,path;count+=1
manifest=json.loads((H/'INPUT_MANIFEST.json').read_text())
sealed=json.loads((out/'DECOMPOSITION_SEALED.json').read_text())
summaries={r['id']:r for r in json.loads((out/'episode_summary.json').read_text())}
max_error=0.
for row in manifest['episodes']:
    path=out/('decomposition_'+row['id']+'.npz')
    assert sha(path)==sealed['bindings'][path.name];count+=1
    with np.load(path,allow_pickle=False) as z:arrays={k:z[k] for k in z.files}
    with np.load(P/row['prior_rapt_score_path'],allow_pickle=False) as z:old=z['loss']
    assert np.array_equal(arrays['loss'],old);count+=1
    n=len(old);assert np.array_equal(arrays['defined'],np.arange(n)>0);count+=1
    assert np.array_equal(arrays['eligible'],np.arange(n)>=100);count+=1
    for k in ['mean','logvar','squared_error','loss']:
        assert arrays[k].shape==(n,4) and np.isfinite(arrays[k]).all();count+=1
    mse=arrays['squared_error'].astype(float);lv=arrays['logvar'].astype(float);loss=arrays['loss'].astype(float)
    mask=(mse>0)&(loss>0)
    error=np.max(np.abs(np.log(loss[mask])-np.log(mse[mask])+lv[mask]));max_error=max(max_error,float(error))
    assert error<2e-5;count+=1
    for region in ['first','last','eligible_all']:
        record=summaries[row['id']][region];lo,hi=record['lo'],record['hi'];assert record['points']==hi-lo;count+=1
        for j,c in enumerate(record['channels']):
            for key,expected in [('mean_prediction',np.mean(arrays['mean'][lo:hi,j].astype(float))),
                                 ('mean_log_variance',np.mean(lv[lo:hi,j])),('mean_variance',np.mean(np.exp(lv[lo:hi,j]))),
                                 ('mean_squared_error',np.mean(mse[lo:hi,j])),('mean_score',np.mean(loss[lo:hi,j]))]:
                assert math.isclose(c[key],float(expected),rel_tol=1e-12,abs_tol=1e-12),(row['id'],region,key);count+=1
            positive=mask[lo:hi,j];d=c['log_decomposition'];assert d['points']==int(positive.sum());count+=1
            assert d['excluded_zero']==int((~positive).sum());count+=1
            if positive.any():
                for key,expected in [('mean_log_squared_error',np.log(mse[lo:hi,j][positive]).mean()),
                                     ('mean_log_variance',lv[lo:hi,j][positive].mean()),('mean_log_score',np.log(loss[lo:hi,j][positive]).mean())]:
                    assert math.isclose(d[key],float(expected),rel_tol=1e-12,abs_tol=1e-12);count+=1
    for j,change in enumerate(summaries[row['id']]['log_changes']):
        aa=summaries[row['id']]['first']['channels'][j]['log_decomposition'];bb=summaries[row['id']]['last']['channels'][j]['log_decomposition']
        for key in ['mean_log_squared_error','mean_log_variance','mean_log_score']:
            expected=bb[key]-aa[key] if aa['points'] and bb['points'] else None
            assert change['delta_'+key]==expected;count+=1
result=json.loads((out/'result.json').read_text());assert result['episodes']==36 and result['rows']==129600 and result['eligible_rows']==126000;count+=1
record=dict(utc=datetime.now(timezone.utc).isoformat(),checks=count,episodes=36,maximum_log_identity_roundoff=max_error,
            inference=False,helper_import=False,freeze_sha256=sha(H/'FREEZE.json'),result_sha256=sha(out/'result.json'),
            interpretation='Saved-array identities/arithmetic, not independent experiments or human review')
with (H/'VERIFICATION.json').open('x') as stream:json.dump(record,stream,indent=2);stream.write('\n')
print(json.dumps(record))
