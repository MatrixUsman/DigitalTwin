"""Lossless used-reference export adapter; scientific worker remains unchanged.

Only reference roles0(base),2(RBF),3(following) are used by the11 methods.
All scores/observations/commands/alarms/truth remain unchanged. Unused linear,
RBF-following,persistence,mean21 reference arrays are omitted from storage.
"""
import sys,io
import numpy as np
import importlib.util
from pathlib import Path as LocalPath
spec=importlib.util.spec_from_file_location('context_worker19',LocalPath(__file__).with_name('worker.py'))
worker=importlib.util.module_from_spec(spec);spec.loader.exec_module(worker)
from io19 import BudgetWriter,Path,packed

class CompactWriter(BudgetWriter):
    def write_bytes(self,name,value,**kwargs):
        if name.startswith('score_') and name.endswith('.npz'):
            with np.load(io.BytesIO(value),allow_pickle=False) as z:a={k:z[k] for k in z.files}
            a['references']=a['references'][:,[0,2,3]]
            a['reference_role_indices']=np.array([0,2,3],dtype=np.int64)
            value=packed(**a)
        return super().write_bytes(name,value,**kwargs)

if __name__=='__main__':
    worker.BudgetWriter=CompactWriter
    try:worker.main('final',Path(sys.argv[1]))
    except BaseException:
        import traceback
        error=traceback.format_exc();print(error,flush=True)
        try:BudgetWriter(Path(sys.argv[1]),limit_bytes=262144000).write_json('failure.json',dict(traceback=error))
        except Exception:pass
        raise
