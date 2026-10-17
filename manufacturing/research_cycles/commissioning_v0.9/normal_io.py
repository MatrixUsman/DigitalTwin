"""Only enumerated archived normal files and three observation members may load."""
from pathlib import Path
import numpy as np
from common9 import INPUT,normal_catalog,sha
from models import Observation

class NormalReader:
    def __init__(self,c,expected):
        self.allowed={r['name']:r for r in normal_catalog(c)};self.expected=expected;self.access=[]
    def read(self,name,stage):
        if name not in self.allowed or self.allowed[name]['stage']!=stage:raise ValueError('Unadmitted file or stage')
        path=INPUT/name
        if sha(path)!=self.expected[name]:raise ValueError('Normal input changed')
        with np.load(path,allow_pickle=False) as z:
            obs=Observation(z['measurements'],z['available'],z['valid'])
        self.access.append(dict(name=name,stage=stage,members=['measurements','available','valid']))
        return obs

def observation_from_synthetic(ep):
    return Observation(ep['measurements'],ep['available'],ep['valid'])
