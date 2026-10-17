"""Bounded export recovery from sealed scores; no fitting or simulation rerun."""
import argparse
from datetime import datetime,timezone
import json
import re
import sys
import time
import numpy as np
from common import HERE,PROJECT,LOCAL,sha,arrays,check_freeze
from observer import outcome
from mfg_twin.supervisor import BudgetWriter,Limits,supervise,install_worker_limits,worker_usage

def portable(value):
    if isinstance(value,np.generic):return value.item()
    if isinstance(value,dict):return {k:portable(v) for k,v in value.items()}
    if isinstance(value,list):return [portable(v) for v in value]
    return value

def recovery_identity():
    receipt=json.loads((HERE/'REPORTING_RECOVERY_FREEZE.json').read_text())
    for p,h in receipt['sha256'].items():
        if sha(PROJECT/p)!=h:raise ValueError('Recovery input changed: '+p)
    return receipt

def recover(output):
    start=time.monotonic();recovery_identity();f=check_freeze();cfg=f['configuration'];limits=Limits(**cfg['limits'])
    install_worker_limits(limits);writer=BudgetWriter(output,limit_bytes=limits.output_bytes,reserve_bytes=limits.parent_reserve_bytes)
    source=LOCAL/'runs/simulation_001';seal=json.loads((source/'SCORES_SEALED.json').read_text())
    for name,h in seal['sha256'].items():
        if sha(source/name)!=h:raise ValueError('Sealed original changed')
        writer.write_bytes(name,(source/name).read_bytes())
    for name in ['SCORES_SEALED.json','provenance.json','failure.json','supervisor.json','launch.json','worker.log']:
        destination=name if name=='SCORES_SEALED.json' else 'origin_'+name
        writer.write_bytes(destination,(source/name).read_bytes())
    writer.write_json('provenance.json',dict(utc=datetime.now(timezone.utc).isoformat(),command=sys.argv,
        purpose='Export recovery only; original scores copied byte-for-byte; no model/threshold/score changes',
        origin='simulation_001',origin_provenance_sha256=sha(source/'provenance.json'),
        recovery_freeze_sha256=sha(HERE/'REPORTING_RECOVERY_FREEZE.json'),synthetic=True))
    roster=json.loads((output/'roster.json').read_text());fit=arrays(output/'fit.npz');records=[];types={}
    if len(roster['evaluation'])!=48:raise ValueError('Incomplete source evaluation')
    for item in roster['evaluation']:
        ep=arrays(output/(item['id']+'.npz'))
        for j,name in enumerate(cfg['decision_names']):
            row=dict(**item,method=name,**outcome(ep['alarm'][:,j],ep['unknown'][:,j],ep['attack'],ep['authorized'],
                ep['state'],ep['reference'],fit['scale'],cfg))
            for k,v in row.items():
                if isinstance(v,np.generic):types[k]=type(v).__name__
            records.append(portable(row))
    writer.write_json('outcomes.json',records);check_freeze()
    origin=json.loads((source/'supervisor.json').read_text());failure=json.loads((source/'failure.json').read_text())
    writer.write_json('summary.json',dict(status='completed',synthetic=True,training_episodes=18,calibration_episodes=18,
        evaluation_episodes=48,methods=11,outcomes=len(records),eligible_per_method=43200,candidate_is_classical_hysteresis=True,
        costs=dict(generation_attempt_wall_seconds=origin['wall_seconds'],generation_attempt_cpu_seconds=failure['usage']['process_cpu_seconds'],
                   reporting_recovery_wall_seconds=time.monotonic()-start),
        usage=worker_usage(),generation_attempt_usage=failure['usage'],wall_seconds=time.monotonic()-start,
        origin_attempt='simulation_001',origin_status='failed during JSON export after complete score seal',
        serialized_numpy_fields=types,scores_seal_sha256=sha(output/'SCORES_SEALED.json')))
    print(json.dumps(dict(status='reporting_completed',outcomes=len(records),converted_fields=types)),flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--attempt',required=True);parser.add_argument('--worker',action='store_true');args=parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_]+',args.attempt):raise ValueError('Invalid attempt')
    output=LOCAL/'runs'/args.attempt
    if args.worker:recover(output)
    else:
        recovery_identity();f=check_freeze();limits=Limits(**f['configuration']['limits']);output.mkdir(parents=True,exist_ok=False)
        writer=BudgetWriter(output,limit_bytes=limits.output_bytes)
        command=[sys.executable,str(HERE/'recover_reporting.py'),'--attempt',args.attempt,'--worker']
        writer.write_json('launch.json',dict(utc=datetime.now(timezone.utc).isoformat(),command=command,cwd=str(PROJECT)))
        result=supervise(command,cwd=PROJECT,output_dir=output,limits=limits)
        writer.write_json('supervisor.json',result);print(json.dumps(result,indent=2))
        raise SystemExit(0 if result['status']=='completed' else 1)
