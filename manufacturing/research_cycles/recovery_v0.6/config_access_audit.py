"""Check numerical independence from unused evaluation metadata in config."""
from datetime import datetime,timezone
import json
import numpy as np
from support import LOCAL,sha,arrays,check_freeze,roster
from core import components,score_matrix,decision,following_predictions,bank_predictions

if __name__=='__main__':
    cfg=check_freeze()['configuration'];run=LOCAL/'runs/simulation_001';fit=arrays(run/'fit.npz')
    thresholds=json.loads((run/'calibration.json').read_text())['records']
    keys=['nominal','bank','dt','substeps','kp','kd','torque_limit','amplitude','phase_offset','observer_gain',
          'ar_order','cusum_cap','cusum_drift','mode_duration','mode_position_jump','mode_velocity_jump',
          'noise_margin_sigma','physical_tolerance','sensor_sigma','recovery_dwell']
    checks=0
    for item in roster(cfg):
        task=next(t for t in cfg['tasks'] if t['id']==item['task'])
        c=dict(cfg);c.update(task);limited={k:c[k] for k in keys}
        ep=arrays(run/(item['id']+'.npz'))
        comp=components(ep['measurements'],ep['available'],ep['valid'],ep['following'],ep['bank'],fit,limited)
        np.testing.assert_array_equal(score_matrix(comp,fit['mode_scales']),ep['scores']);checks+=1
        for j in range(13):
            a,u=decision(ep['scores'][:,j],j,ep['valid'],comp['return_ok'],thresholds[j]['threshold'],limited)
            np.testing.assert_array_equal(a,ep['alarm'][:,j]);np.testing.assert_array_equal(u,ep['unknown'][:,j]);checks+=2
        # Strict mappings also exercise model propagation, without the scenario roster.
        np.testing.assert_array_equal(following_predictions(ep['measurements'][:16],ep['available'][:16],limited),ep['following'][:16]);checks+=1
        np.testing.assert_array_equal(bank_predictions(ep['available'][:16],limited),ep['bank'][:16]);checks+=1
    result=dict(utc=datetime.now(timezone.utc).isoformat(),status='passed',checks=checks,permitted_keys=keys,
        clarification='The worker passes a full configuration dictionary containing unused scenario metadata. Exact output replay with restricted keys confirms no numerical dependence; this is not an OS/capability isolation guarantee.',
        scores_seal_sha256=sha(run/'SCORES_SEALED.json'))
    with (LOCAL/'config_access_audit.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(result,indent=2))
