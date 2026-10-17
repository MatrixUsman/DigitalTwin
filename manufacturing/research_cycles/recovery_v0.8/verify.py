"""Post-run verification. Does not alter models, choices or observations."""
import argparse,json,time
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
from common import HERE,PROJECT,sha,arrays,check,write_json
from mechanism import fit_reference,reference,scalar,decide
from metrics8 import evaluate,summarize

def main(run):
    started=time.monotonic();c=check()['configuration'];checks=0
    def ok(v,label):
        nonlocal checks
        if not v:raise AssertionError(label)
        checks+=1
    for sealname in ['BEFORE_FRESH_GENERATION.json','SCORES_SEALED.json']:
        seal=json.loads((run/sealname).read_text())
        for n,h in seal['sha256'].items():ok(sha(run/n)==h,n)
    fits={};cal=json.loads((run/'calibration.json').read_text())['plants']
    for p in c['plants8']:
        pid=p['id'];train=[arrays(run/f'train_{pid}_{i}.npz') for i in range(3)]
        fit=arrays(run/f'fit_{pid}.npz');rebuilt=fit_reference(train,c['order'],c['ridge'],c['warmup']);fits[pid]=fit
        for k in fit:ok(np.array_equal(fit[k],rebuilt[k]),'fit '+pid+k)
        normal=[arrays(run/f'cal_{pid}_{i:02d}.npz') for i in range(19)]
        b=float(max(e['learned_error'][100:].max() for e in normal));ok(b==cal[pid]['allowance'],'allowance')
        for j,r in enumerate(cal[pid]['records']):
            count=sum(int((decide(e,j,r['threshold'],b,c)[0]&~decide(e,j,r['threshold'],b,c)[1])[100:].sum()) for e in normal)
            ok(count==r['actual_alarms'],'calibration count')
            if j not in [10,11,12]:ok(count<=209,'calibration budget')
    roster=json.loads((run/'roster.json').read_text());saved=json.loads((run/'outcomes.json').read_text());rows=[];pools=[];truth_diagnostics=[]
    ok(len(roster)==216,'episode coverage');ok(len(saved)==2808,'outcome coverage')
    for item in roster:
        ep=arrays(run/(item['id']+'.npz'));pools.append((item,ep));fit=fits[item['plant']];b=cal[item['plant']]['allowance']
        rr=reference(ep['measurements'],ep['available'],fit);ok(np.array_equal(rr,ep['reference']),'free reference replay')
        ok(np.isfinite(ep['scores']).all(),'finite scores')
        ok(np.array_equal(ep['learned_error'],scalar(ep['measurements'],rr,fit['scale'])),'score replay')
        if not ep['attack'].any():ok(np.array_equal(ep['state'],ep['truth_reference']),'clean counterfactual identity')
        dist=np.max(np.abs((ep['state']-ep['truth_reference'])/fit['scale']),axis=1)
        positions=np.flatnonzero(ep['attack']);manual_return=None
        if len(positions):
            end=positions[-1]+1;stop=min(len(dist),end+250)
            for t in range(end,stop-c['dwell']+1):
                if max(dist[t:t+c['dwell']])<=.1:manual_return=int(t-end);break
        truth_diagnostics.append(dict(id=item['id'],has_attack=bool(len(positions)),max_attack_effect=float(dist.max()),counterfactual_return_steps=manual_return,
            reference_envelope_covered=bool(np.all(scalar(ep['truth_reference'],ep['reference'],fit['scale'])[100:]<=b))))
        for j,method in enumerate(c['methods8']):
            a,u=decide(ep,j,cal[item['plant']]['records'][j]['threshold'],b,c)
            ok(np.array_equal(a,ep['alarm'][:,j]) and np.array_equal(u,ep['unknown'][:,j]),'alarm replay')
            r=evaluate(a,u,dict(ep,reference=ep['truth_reference']),fit,c)
            ok(r['physical_return_steps']==manual_return,'independent return scan')
            tp=fp=fn=0
            for t in range(100,len(a)):
                predicted=bool(a[t] and not u[t]);label=bool(ep['attack'][t]);tp+=predicted and label;fp+=predicted and not label;fn+=label and not predicted
            ok((tp,fp,fn)==(r['tp'],r['fp'],r['fn']),'independent confusion counts')
            rows.append(dict(**item,method=method,**r))
    ok(rows==saved,'all outcomes');ok(summarize(rows,pools,c)==json.loads((run/'aggregate.json').read_text()),'aggregate replay')
    # Selected physics controls independently replay to bound verification cost.
    from simulation import monitor_inputs
    for i in [0,80,160]:
        item=roster[i];ep=arrays(run/(item['id']+'.npz'));comp=monitor_inputs(ep,fits[item['plant']],c)
        for key in ['following','nominal_reference','scores']:ok(np.array_equal(comp[key],ep[key]),'selected physical replay')
    check();record=dict(utc=datetime.now(timezone.utc).isoformat(),status='passed',checks=checks,episodes=216,outcomes=2808,seconds=time.monotonic()-started,
        verification_scope='All hashes/fits/calibration counts/free references/alarms/outcomes, independent count/return arithmetic; selected 3 physics propagations. Same code replay is not independent physical validation.',
        run=str(run.relative_to(PROJECT)),freeze_sha256=sha(HERE/'FREEZE.json'),source_sha256=sha(__file__),truth_diagnostics=truth_diagnostics)
    write_json(HERE/'VERIFICATION.json',record);print(json.dumps({k:v for k,v in record.items() if k!='truth_diagnostics'}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);a=p.parse_args();main(a.run.resolve())
