import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import time

from bounded_run import HERE, PROJECT, LIMITS
from mfg_twin.supervisor import BudgetWriter, install_worker_limits, worker_usage

if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    installed_limits = install_worker_limits(LIMITS)
    started = datetime.now(timezone.utc).isoformat(); start = time.monotonic()
    writer = BudgetWriter(args.output, limit_bytes=LIMITS.output_bytes,
                          reserve_bytes=LIMITS.parent_reserve_bytes)
    import numpy as np
    import tensorflow as tf
    from diagnostics import cells_from_verified_notebook, source_diagnostics
    notebook = PROJECT / "local/comparator_admission_20261017/replacements/edge_main.ipynb"
    sources = PROJECT / "local/contribution_v0.2/sources"
    result = source_diagnostics(cells_from_verified_notebook(notebook))
    writer.write_bytes('source_diagnostics.json',(json.dumps(result,indent=2)+'\n').encode())
    models=[]
    for name in ["edge_cnn.tflite", "edge_lstm.tflite"]:
        path=sources/name
        interpreter=tf.lite.Interpreter(model_path=str(path), num_threads=1)
        interpreter.allocate_tensors()
        inp, out = interpreter.get_input_details()[0], interpreter.get_output_details()[0]
        runs=[]
        for seed in [17,42,2026]:
            interpreter.reset_all_variables()
            fixture=np.random.default_rng(seed).normal(0,0.1,tuple(inp['shape'])).astype(inp['dtype'])
            interpreter.set_tensor(inp['index'],fixture);interpreter.invoke()
            value=interpreter.get_tensor(out['index']).copy()
            interpreter.set_tensor(inp['index'],fixture);interpreter.invoke()
            repeat=interpreter.get_tensor(out['index'])
            interpreter.reset_all_variables()
            interpreter.set_tensor(inp['index'],fixture);interpreter.invoke()
            reset_value=interpreter.get_tensor(out['index']).copy()
            fresh=tf.lite.Interpreter(model_path=str(path),num_threads=1)
            fresh.allocate_tensors();fi=fresh.get_input_details()[0];fo=fresh.get_output_details()[0]
            fresh.set_tensor(fi['index'],fixture);fresh.invoke()
            fresh_value=fresh.get_tensor(fo['index']).copy()
            assert all(np.isfinite(x).all() for x in [value,repeat,reset_value,fresh_value])
            runs.append({'seed':seed,'synthetic':True,'finite':True,
                         'repeat_equal_without_reset':bool(np.array_equal(value,repeat)),
                         'repeat_max_absolute_change':float(np.max(np.abs(value-repeat))),
                         'reset_max_absolute_change':float(np.max(np.abs(value-reset_value))),
                         'fresh_interpreter_max_absolute_change':float(np.max(np.abs(value-fresh_value))),
                         'input_sha256':hashlib.sha256(fixture.tobytes()).hexdigest(),
                         'output_sha256':hashlib.sha256(value.tobytes()).hexdigest()})
        models.append({'name':name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                       'input_shape':inp['shape'].tolist(),'output_shape':out['shape'].tolist(),
                       'input_dtype':str(inp['dtype']),'output_dtype':str(out['dtype']),
                       'bytes':path.stat().st_size,'runs':runs})
    result['D5']=models
    result['provenance']={'start_utc':started,'end_utc':datetime.now(timezone.utc).isoformat(),
       'wall_seconds':time.monotonic()-start,'usage':worker_usage(),'limits':installed_limits,
       'interpreter':sys.version,'platform':platform.platform(),'tensorflow':tf.__version__,
       'numpy':np.__version__,'command':sys.argv,'cwd':str(Path.cwd()),
       'git_head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
       'git_status':subprocess.check_output(['git','status','--porcelain'],text=True),
       'source_sha256':{str(p.relative_to(PROJECT)):hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in [HERE/'PLAN.md',HERE/'diagnostics.py',HERE/'run_diagnostics.py',
                                 HERE/'bounded_run.py',PROJECT/'src/mfg_twin/supervisor.py',notebook]},
       'raw_data_opened':False,'training':False}
    writer.write_bytes('diagnostics.json',(json.dumps(result,indent=2)+'\n').encode())
    print('Completed synthetic source-path diagnostics and two author-model smoke checks.')
