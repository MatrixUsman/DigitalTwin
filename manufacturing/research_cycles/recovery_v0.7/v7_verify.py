import argparse
from datetime import datetime,timezone
import json
from pathlib import Path
import numpy as np
from v7_common import HERE,LOCAL,RUN6,sha,arrays,check,roster,permitted
from v7_core import make_components,decide,calibrate7,commands7
from v7_metrics import evaluate,summarize

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    c=check()['configuration'];fit=arrays(a.run/'fit.npz');count=0
    assert sha(a.run/'fit.npz')==sha(RUN6/'fit.npz');count+=1
    for name in ['BEFORE_FRESH_GENERATION.json','SCORES_SEALED.json']:
        for name,h in json.loads((a.run/name).read_text())['sha256'].items():assert sha(a.run/name)==h;count+=1
    cal=json.loads((a.run/'calibration.json').read_text());old=json.loads((RUN6/'calibration.json').read_text())
    normal=[arrays(p) for p in sorted(a.run.glob('calibration_*.npz'))]
    for j in range(23):
        if j<13:assert cal['records'][j]['threshold']==old['records'][j]['threshold']
        elif j in [18,19,20,21]:assert cal['records'][j]['threshold']==old['records'][11]['threshold']
        else:
            r=calibrate7(normal,j,c)
            for k,v in r.items():assert cal['records'][j][k]==v
        n=sum(int((decide(e,j,cal['records'][j]['threshold'],permitted(c))[0]&~decide(e,j,cal['records'][j]['threshold'],permitted(c))[1])[100:].sum()) for e in normal)
        assert n==cal['records'][j]['actual_normal_alarms'];count+=2
    records=[];pools=[]
    for item in roster(c):
        ep=arrays(a.run/(item['id']+'.npz'));task=next(t for t in c['tasks7'] if t['id']==item['task']);cc=dict(c);cc.update(task)
        expected=commands7(c,task,item['condition'])
        for key,value in expected.items():np.testing.assert_array_equal(value,ep[key]);count+=1
        comp=make_components(ep['measurements'],ep['available'],ep['valid'],ep['following'],ep['bank'],fit,permitted(cc))
        np.testing.assert_array_equal(comp['scores'],ep['scores']);count+=1
        assert ep['scores'].shape==(1200,23) and np.isfinite(ep['scores']).all();count+=1
        for j,name in enumerate(c['methods7']):
            alarm,unknown=decide(comp,j,cal['records'][j]['threshold'],permitted(cc))
            np.testing.assert_array_equal(alarm,ep['alarm'][:,j]);np.testing.assert_array_equal(unknown,ep['unknown'][:,j]);count+=2
            row=dict(**item,method=name,**evaluate(alarm,unknown,ep,fit,c));records.append(row)
            y=ep['attack'][100:];observed=alarm[100:]&~unknown[100:]
            assert row['tp']==int(observed[y].sum()) and row['fn']==int((~observed[y]).sum());count+=1
            assert row['fp']==int(observed[~y].sum()) and row['eligible']==1100;count+=1
        pools.append((item,ep))
    assert len(records)==3312 and records==json.loads((a.run/'outcomes.json').read_text());count+=1
    assert summarize(records,pools,c)==json.loads((a.run/'aggregate.json').read_text());count+=1
    assert json.loads((a.run/'supervisor.json').read_text())['status']=='completed';count+=1
    check();result=dict(status='passed',utc=datetime.now(timezone.utc).isoformat(),checks=count,outcomes=len(records),
        scope='Fresh-process saved-artifact replay and independent contingency counts; not external validation',
        freeze_sha256=sha(HERE/'FREEZE.json'),run_sha256={p.name:sha(p) for p in a.run.iterdir() if p.is_file()})
    with a.output.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k!='run_sha256'},indent=2))
