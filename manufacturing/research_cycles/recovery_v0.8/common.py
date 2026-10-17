from pathlib import Path
import sys,json,hashlib,io
import numpy as np
HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[1]
OLD=HERE.parent/'recovery_v0.7'
LOCAL=PROJECT/'local/recovery_v0.8'
sys.path.insert(0,str(OLD))
from v7_common import permitted
from support import sha,arrays,packed,verify_map

def config():
    c=json.loads((OLD/'FREEZE.json').read_text())['configuration']
    c.update(json.loads((HERE/'config.json').read_text()))
    return c

def guard():
    p=OLD/'PACKAGE_MANIFEST.json';d=json.loads(p.read_text())['sha256']
    d[str(p.relative_to(PROJECT))]=sha(p)
    return d

def check():
    f=json.loads((HERE/'FREEZE.json').read_text())
    verify_map(f['source_sha256']);verify_map(f['input_sha256']);return f

def write_json(path,obj):
    Path(path).write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n')
