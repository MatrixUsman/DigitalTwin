import hashlib
import io
import json
from pathlib import Path
import numpy as np


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        while block := stream.read(1024 * 1024): digest.update(block)
    return digest.hexdigest()


def array_hash(values):
    values = np.asarray(values)
    digest = hashlib.sha256()
    digest.update(str(values.shape).encode())
    digest.update(values.dtype.str.encode())
    digest.update(values.tobytes(order="C"))
    return digest.hexdigest()


def npz_bytes(**arrays):
    stream = io.BytesIO()
    np.savez(stream, **arrays)
    return stream.getvalue()


def load_prefix(path, expected_sha256, nrows, columns):
    import pandas as pd
    if sha256(path) != expected_sha256:
        raise ValueError("Raw nominal-file identity mismatch")
    frame = pd.read_csv(path, nrows=nrows, on_bad_lines="error")
    if list(frame.columns) != ["name", "time"] + columns or len(frame) != nrows:
        raise ValueError("Unexpected schema or prefix size")
    if frame[columns + ["time"]].isna().any().any():
        raise ValueError("Missing prefix observations")
    if not np.issubdtype(frame["time"].dtype, np.integer):
        raise ValueError("Timestamp must be integral native units")
    return frame


def verify_frozen(project, freeze):
    for relative, expected in freeze["source_sha256"].items():
        if sha256(project / relative) != expected:
            raise ValueError("Frozen source changed: " + relative)
    receipt = json.loads((project / freeze["test_receipt"]).read_text())
    if sha256(project / freeze["test_receipt"]) != freeze["test_receipt_sha256"] or receipt["returncode"] != 0:
        raise ValueError("Invalid test receipt")
