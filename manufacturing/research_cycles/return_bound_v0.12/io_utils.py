"""Identity and local artifact utilities; no dataset loader."""
import hashlib
import io
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
LOCAL = PROJECT/'local/return_bound_v0.12'
RUN = LOCAL/'runs/diagnostic_001'


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024*1024), b''): h.update(chunk)
    return h.hexdigest()


def packed(**arrays):
    import numpy as np
    stream = io.BytesIO(); np.savez_compressed(stream, **arrays); return stream.getvalue()


def check_frozen():
    f = json.loads((HERE/'FREEZE.json').read_text())
    for name, digest in f['source_sha256'].items():
        if sha256(PROJECT/name) != digest: raise ValueError('source changed: '+name)
    if sha256(PROJECT/f['test_receipt']) != f['test_receipt_sha256']:
        raise ValueError('test receipt changed')
    return f
