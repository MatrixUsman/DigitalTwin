"""Read-back verification; replays decision rules, not physics/training."""
import json,sys
from io19 import *
from mechanism19 import *

def main():
    out=LOCAL/'final_001';f=check(HERE/'FINAL_FREEZE.json');n=0
    seal=json.loads((out/'SCORES_SEALED.json').read_text())
    for name,h in seal['bindings'].items():assert sha(out/name)==h;n+=1
    models=bases();envelopes=json.loads((LOCAL/'development_001/selected.json').read_text())['models']
    threshold=json.loads((OLD/'calibration.json').read_text());dc={'warmup':100,'return_tolerance':.1,'dwell':10,'recovery_horizon':250}
    catalog=json.loads((out/'catalog.json').read_text());saved=json.loads((out/'outcomes.json').read_text());rows=[]
    for item in catalog:
        z=load_npz(out/('score_'+item['id']+'.npz'));t=load_npz(out/('truth_'+item['id']+'.npz'));parent=item['parent'];scale=models[parent]['base']['scale']
        residual=(z['measurements'][:,None,:]-z['references'])/scale
        a,b,lower,upper=alarms(residual,z['scores'],z['valid'],threshold['thresholds'][parent],scale,z['commands'],envelopes[parent],residual13)
        for key,value in [('alarms',a),('width',b),('lower',lower),('upper',upper)]:np.testing.assert_array_equal(value,z[key]);n+=1
        assert len(a)==(6000 if item['condition'] in ['normal','authorized_changes'] else 2400);assert not a[:100].any();n+=2
        for j,method in enumerate(METHODS):
            row=evaluate(a[:,j],t['attack'],t['state'],t['counterfactual'],scale,dc)
            extra=extra_metrics(a[:,j],t['attack'],t['state'],t['counterfactual'],scale)
            joint=bool(row['overlap'] and extra['outside_inactive']==0 and row['clear_timely'] and not row['return_missing'])
            rows.append(dict(**item,method=method,**row,**extra,joint=joint,context_extrapolation_points=int(z['context_extrapolation'][START:].sum())))
    assert rows==saved;n+=len(rows)
    summary=summarize(rows);result=json.loads((out/'results.json').read_text());assert summary==result['summary'];assert criterion(summary)==result['primary'];n+=2
    supervisor=json.loads((out/'supervisor.json').read_text());assert supervisor['status']=='completed';n+=1
    result=dict(status='passed',checks=n,episodes=len(catalog),outcomes=len(rows),read_only=True,physics_rerun=False,
        frozen_bindings=len(f['bindings']),all_originals_preserved=True,
        bindings={str(p.relative_to(PROJECT)):sha(p) for p in [out/'results.json',out/'outcomes.json',out/'supervisor.json',HERE/'FINAL_FREEZE.json']})
    write(HERE/'VERIFICATION.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()
