import argparse
import json
import platform
import subprocess
import sys
import time
import traceback
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from io_utils import HERE, PROJECT, check_frozen, packed, sha256
sys.path.insert(0,str(PROJECT/'src'))
from mfg_twin.supervisor import BudgetWriter, Limits, install_worker_limits, worker_usage


def main(out):
    f=check_frozen();c=f['configuration'];limits=Limits(**c['limits']);install_worker_limits(limits)
    writer=BudgetWriter(out,limit_bytes=limits.output_bytes,reserve_bytes=limits.parent_reserve_bytes)
    import numpy as np
    from study import catalog,contract_for,generate,score,evaluate
    now=lambda:datetime.now(timezone.utc).isoformat()
    writer.write_json('provenance.json',dict(utc=now(),owner='Haiqa Mushtaq',operator='Codex',study_id=c['study_id'],
        command=sys.argv,executable=sys.executable,cwd=str(Path.cwd()),python=sys.version,numpy=np.__version__,platform=platform.platform(),
        configuration=c,freeze_sha256=sha256(HERE/'FREEZE.json'),dependencies=f['dependencies'],
        git_head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
        git_status=subprocess.check_output(['git','status','--short'],text=True),source_sha256=f['source_sha256'],
        classification='synthetic residual-level normal feasibility; standard Gaussian control; oracle-informed uncertainty'))
    writer.write_json('access.json',dict(raw_data=[],saved_model_inputs=[],attack_observations=[],protected_final_access=False,
                                       synthetic_only=True,truth_used_only_by_evaluator=True))
    start=time.monotonic();records=[];artifacts={};costs=[]
    for row in catalog(c):
        data=generate(c,row);con=contract_for(c,row)
        assert np.all(np.abs(data['delta']) <= np.asarray(con.tolerance))
        assert np.all(np.abs(data['bias']) <= np.asarray(con.bias)+1e-14)
        assert np.all(np.abs(np.diff(data['delta'],axis=0)) <= np.asarray(con.drift)+1e-14)
        cpu=time.process_time();wall=time.monotonic()
        scores=score(data['residual'],data['valid'],con)
        costs.append(dict(trace=row['id'],six_method_cpu_seconds=time.process_time()-cpu,six_method_wall_seconds=time.monotonic()-wall))
        records.extend(evaluate(c,row,data['delta'],scores))
        filename=row['id']+'.npz';writer.write_bytes(filename,packed(**data,**scores))
        artifacts[filename]=sha256(out/filename)
        writer.write_json(row['id']+'_receipt.json',dict(row=row,contract=asdict(con),artifact=filename,sha256=artifacts[filename]))
    assert len(records)==216 and len(artifacts)==36
    check_frozen()
    writer.write_json('summary.json',dict(status='completed',utc=now(),configuration=c,records=records,artifacts=artifacts,costs=costs,
        overall_feasibility_pass=all(r['feasibility_pass'] for r in records if r['method']=='multiwindow'),
        usage=worker_usage(),worker_wall_seconds=time.monotonic()-start,
        thresholds_fitted=False,real_data_access=False,synthetic=True,scientific_claim='conditional normal feasibility only'))
    print('Completed 36 synthetic traces and all 216 outcomes; no fitting or attack evaluation.',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);out=parser.parse_args().output
    try: main(out)
    except BaseException:
        error=traceback.format_exc();print(error,flush=True)
        try: BudgetWriter(out,limit_bytes=20971520).write_json('failure.json',dict(error=error,usage=worker_usage()))
        except Exception: pass
        raise
