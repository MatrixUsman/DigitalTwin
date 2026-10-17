"""Fresh-process hash, calibration, scoring and outcome checks; no simulation."""
import argparse
from datetime import datetime,timezone
import json
from pathlib import Path
import numpy as np
from support import HERE,PROJECT,sha,arrays,check_freeze,roster
from core import components,score_matrix,calibrate,decision
from metrics import evaluate,aggregate
from mfg_twin.metrics import average_precision

def verify(run):
    f=check_freeze();cfg=f['configuration'];count=0
    for name in ['BEFORE_FRESH_GENERATION.json','SCORES_SEALED.json']:
        for p,h in json.loads((run/name).read_text())['sha256'].items():
            assert sha(run/p)==h;count+=1
    before=json.loads((run/'BEFORE_FRESH_GENERATION.json').read_text())
    seal=json.loads((run/'SCORES_SEALED.json').read_text())
    assert before['utc']<seal['utc'];count+=1
    fit=arrays(run/'fit.npz');cal=json.loads((run/'calibration.json').read_text())
    assert cal['population']==16200 and cal['budget']==162;count+=1
    eps=[arrays(p) for p in sorted(run.glob('calibration_*.npz'))]
    for j in range(13):
        assert calibrate(eps,j,cfg)==cal['records'][j];count+=1
    modes=[]
    train=[arrays(p) for p in sorted(run.glob('train_*.npz'))]
    for mode in [0,1]:
        values=np.concatenate([e['base'][100:,7][e['mode'][100:]==mode] for e in train])
        modes.append(np.sort(values)[int(np.ceil(.99*len(values)))-1])
    np.testing.assert_array_equal(modes,fit['mode_scales']);count+=1
    records=[];pooled={s:[] for s in ['within_range','extrapolation']}
    assert json.loads((run/'roster.json').read_text())==roster(cfg);count+=1
    for item in roster(cfg):
        ep=arrays(run/(item['id']+'.npz'));c=dict(cfg);c.update(next(t for t in cfg['tasks'] if t['id']==item['task']))
        comp=components(ep['measurements'],ep['available'],ep['valid'],ep['following'],ep['bank'],fit,c)
        np.testing.assert_array_equal(score_matrix(comp,fit['mode_scales']),ep['scores']);count+=1
        assert np.isfinite(ep['scores']).all() and ep['scores'].shape==(1000,13);count+=1
        np.testing.assert_array_equal(ep['reference'],ep['bank'][:,1]);count+=1
        noise=np.random.default_rng(item['noise_seed']).normal(size=ep['state'].shape)*np.asarray(c['sensor_sigma'])
        np.testing.assert_array_equal(ep['measurements'],ep['state']+noise);count+=1
        for j,name in enumerate(cfg['methods']):
            a,u=decision(ep['scores'][:,j],j,ep['valid'],comp['return_ok'],cal['records'][j]['threshold'],cfg)
            np.testing.assert_array_equal(a,ep['alarm'][:,j]);np.testing.assert_array_equal(u,ep['unknown'][:,j]);count+=2
            row=dict(**item,method=name,**evaluate(a,u,ep,fit,cfg));records.append(row)
            # Independent contingency arithmetic on fixed eligible support.
            observed=a[100:] & ~u[100:];y=ep['attack'][100:]
            assert row['tp']==int(observed[y].sum()) and row['fn']==int((~observed[y]).sum())
            assert row['fp']==int(observed[~y].sum()) and row['eligible']==900;count+=2
        pooled[item['stratum']].append((ep['attack'][100:],np.where(ep['unknown'],-1.,ep['scores'])[100:]))
    assert records==json.loads((run/'outcomes.json').read_text());count+=1
    result=aggregate(records,cfg)
    for stratum,items in pooled.items():
        y=np.concatenate([x[0] for x in items]).astype(int).tolist();s=np.concatenate([x[1] for x in items])
        for j,name in enumerate(cfg['methods']):
            row=next(r for r in result['rows'] if r['stratum']==stratum and r['method']==name)
            row['average_precision_unknown_ranked_last']=average_precision(y,s[:,j].tolist());count+=1
    assert result==json.loads((run/'aggregate.json').read_text());count+=1
    assert len(records)==1872;count+=1
    assert json.loads((run/'supervisor.json').read_text())['status']=='completed';count+=1
    check_freeze()
    return dict(status='passed',checks=count,utc=datetime.now(timezone.utc).isoformat(),
        outcomes=len(records),freeze_sha256=sha(HERE/'FREEZE.json'),
        run_sha256={p.name:sha(p) for p in sorted(run.iterdir()) if p.is_file()},
        scope='Fresh-process arithmetic/replay verification; no independent physical validation')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    result=verify(a.run)
    with a.output.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k!='run_sha256'},indent=2))
