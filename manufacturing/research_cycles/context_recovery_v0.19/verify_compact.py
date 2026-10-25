"""Recover full inference independently; compare every retained score/reference."""
import verify
from io19 import *
original_load=verify.load_npz
models=bases();cal=json.loads((OLD/'calibration.json').read_text())

def load(path):
    z=original_load(path)
    if 'reference_role_indices' in z:
        parent='Q'+Path(path).name.split('_')[2][1:]
        obs=Observation(z['measurements'],z['commands'],z['valid'])
        refs,res,scores=infer(obs,models[parent],cal['cusum_k'][parent],{'warmup':100,'return_tolerance':.1,'dwell':10})
        np.testing.assert_array_equal(z['references'],refs[:,z['reference_role_indices']])
        np.testing.assert_array_equal(z['scores'],scores)
        z['references']=refs
    return z

verify.load_npz=load
if __name__=='__main__':verify.main()
