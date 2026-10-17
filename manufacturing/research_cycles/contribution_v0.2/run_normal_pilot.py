import argparse
from datetime import datetime,timezone
import hashlib
import io
import json
from pathlib import Path
import platform
import subprocess
import sys
import time
from bounded_run import HERE,PROJECT,LIMITS
from mfg_twin.supervisor import BudgetWriter,install_worker_limits,worker_usage

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    install_worker_limits(LIMITS);start=time.monotonic();utc=datetime.now(timezone.utc).isoformat()
    writer=BudgetWriter(a.output,limit_bytes=LIMITS.output_bytes,reserve_bytes=LIMITS.parent_reserve_bytes)
    import numpy as np
    import pandas as pd
    import tensorflow as tf
    from pilot_data import FEATURES,prepare_prefix
    tf.keras.utils.set_random_seed(17)
    tf.config.experimental.enable_op_determinism()
    raw=PROJECT/'datasets/raw/casper12/v2/nominal/IMU_10Hz.csv'
    expected='1221df9be80c229969f3f21f820837e68ad28f4ccb3949bf4013f00d6d69d62c'
    digest=hashlib.sha256()
    with raw.open('rb') as stream:
        while block:=stream.read(1048576):digest.update(block)
    if digest.hexdigest()!=expected:raise ValueError('Dataset identity mismatch')
    # Author load skips 99 numeric rows then trims 120; preserve that origin.
    prefix=pd.read_csv(raw,nrows=10549)
    data=prefix.iloc[219:10549].copy()
    if len(data)!=10330 or list(data.columns)!=['name','time']+FEATURES:raise ValueError('Schema/population')
    if data.isna().any().any() or not (np.diff(data['time'].to_numpy())>0).all():raise ValueError('Invalid prefix clock/data')
    arrays=prepare_prefix(data[FEATURES].to_numpy())
    scaler_before=hashlib.sha256(arrays['mean'].tobytes()+arrays['scale'].tobytes()).hexdigest()
    model=tf.keras.Sequential([
      tf.keras.layers.Input(shape=(45,9)),
      tf.keras.layers.Conv1D(8,3,activation='relu'),
      tf.keras.layers.Conv1D(8,3,activation='relu'),
      tf.keras.layers.MaxPooling1D(3),tf.keras.layers.Flatten(),
      tf.keras.layers.Dense(9,kernel_initializer='zeros'),tf.keras.layers.Reshape((1,9))])
    model.compile(optimizer=tf.keras.optimizers.Adamax(learning_rate=0.001),loss='mse')
    # Explicit bounded batches avoid tf.data worker/autotuning changes.
    losses=[]
    for first in range(0,len(arrays['train_x']),256):
        last=first+256
        losses.append(float(model.train_on_batch(arrays['train_x'][first:last],arrays['train_y'][first:last,None,:])))
    weights_before=hashlib.sha256(b''.join(x.tobytes() for x in model.get_weights())).hexdigest()
    predictions=np.concatenate([model(arrays['dev_x'][i:i+256],training=False).numpy()[:,0,:]
                                for i in range(0,2048,256)])
    weights_after=hashlib.sha256(b''.join(x.tobytes() for x in model.get_weights())).hexdigest()
    scaler_after=hashlib.sha256(arrays['mean'].tobytes()+arrays['scale'].tobytes()).hexdigest()
    scores=np.sqrt(np.mean((predictions-arrays['dev_y'])**2,axis=1))
    assert len(scores)==2048 and np.isfinite(scores).all()
    assert weights_before==weights_after and scaler_before==scaler_after
    model_path=a.output/'pilot_cnn.keras';model.save(model_path)
    buf=io.BytesIO();np.savez(buf,scores=scores,indices=arrays['dev_target_indices']+219,
                            mean=arrays['mean'],scale=arrays['scale'])
    writer.write_bytes('pilot_artifacts.npz',buf.getvalue())
    summary={'status':'successful normal-only feasibility pilot; not paper reproduction',
      'synthetic':False,'attack_metrics':None,'threshold':None,'final_test_opened':False,
      'dataset_sha256':expected,'numeric_row_origin':219,'training_raw_range':[219,8456],
      'development_raw_range':[8456,10549],'training_target_range':[264,8456],
      'development_target_range':[8501,10549],'history':45,'train_targets':8192,'dev_targets':2048,
      'epochs':1,'batch_size':256,'shuffle':False,'seed':17,'parameters':model.count_params(),
      'dev_standardized_mse':float(np.mean((predictions-arrays['dev_y'])**2)),
      'dev_persistence_standardized_mse':float(np.mean((arrays['dev_x'][:,-1,:]-arrays['dev_y'])**2)),
      'dev_zero_standardized_mse':float(np.mean(arrays['dev_y']**2)),
      'finite_scores':int(np.isfinite(scores).sum()),'weights_unchanged_during_development':weights_before==weights_after,
      'weights_sha256':weights_after,'scaler_unchanged_during_development':scaler_before==scaler_after,
      'model_file_sha256':hashlib.sha256(model_path.read_bytes()).hexdigest(),
      'start_utc':utc,'end_utc':datetime.now(timezone.utc).isoformat(),'wall_seconds':time.monotonic()-start,
      'usage':worker_usage(),'interpreter':sys.version,'platform':platform.platform(),'tensorflow':tf.__version__,
      'command':sys.argv,'cwd':str(Path.cwd()),'git_head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
      'git_status':subprocess.check_output(['git','status','--porcelain'],text=True),
      'source_sha256':{str(x.relative_to(PROJECT)):hashlib.sha256(x.read_bytes()).hexdigest()
          for x in [HERE/'PLAN.md',HERE/'run_normal_pilot.py',HERE/'pilot_data.py',HERE/'bounded_run.py',
                    HERE/'requirements-macos-arm64.lock.txt',PROJECT/'src/mfg_twin/supervisor.py']},
      'limitations':['One seed/epoch on a prefix; no published score reproduction','No paper checkpoint or training-scaler lineage',
                     'Clock units/acquisition versus arrival semantics not independently established','No attack or physical-generalization evidence']}
    writer.write_bytes('pilot_summary.json',(json.dumps(summary,indent=2)+'\n').encode())
    print('Normal pilot complete; 8192 training targets, 2048 development scores, no attacks/calibration/final access.')
