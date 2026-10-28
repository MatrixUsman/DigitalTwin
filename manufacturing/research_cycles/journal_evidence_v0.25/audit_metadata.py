"""Audit the received ROS 2 archive's metadata only; never read bag messages.

Run from manufacturing: python3 research_cycles/journal_evidence_v0.25/audit_metadata.py
This is a source admission check, not a detector experiment.
"""
from pathlib import Path
import datetime
import hashlib
import json
import platform
import re
import sys
import zipfile

PROJECT = Path(__file__).resolve().parents[2]
LOCAL = PROJECT / "local/journal_evidence_v0.25"
ARCHIVE = PROJECT / "datasets/raw/ros2_zenodo_17649537/Experiment_1.zip"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    receipt = json.loads((LOCAL / "ROS2_METADATA_RECEIPT.json").read_text())
    assert digest(ARCHIVE) == receipt["sha256"]
    assert ARCHIVE.stat().st_size == receipt["bytes"]
    records = []
    # Parse only the fixed, inspected rosbag metadata layout, failing closed on
    # mismatched counts. Do not deserialize the YAML or serialized ROS messages.
    with zipfile.ZipFile(ARCHIVE) as archive:
        names = archive.namelist()
        metadata = sorted(n for n in names if n.endswith("/metadata.yaml"))
        assert metadata == ["E1-1/metadata.yaml", "E1-2/metadata.yaml"]
        for name in metadata:
            info = archive.getinfo(name)
            assert info.file_size < 100_000
            raw = archive.read(name)
            text = raw.decode("utf-8")
            duration = int(re.search(r"^    nanoseconds: (\d+)$", text, re.M)[1])
            total = int(re.search(r"^  message_count: (\d+)$", text, re.M)[1])
            topics = []
            for block in text.split("    - topic_metadata:\n")[1:]:
                topic = re.search(r"^        name: (\S+)$", block, re.M)[1]
                kind = re.search(r"^        type: (\S+)$", block, re.M)[1]
                count = int(re.search(r"^      message_count: (\d+)$", block, re.M)[1])
                topics.append({"name": topic, "type": kind, "count": count})
            assert len(topics) == 10
            assert len({t["name"] for t in topics}) == len(topics)
            assert sum(t["count"] for t in topics) == total
            assert next(t["count"] for t in topics if t["name"] == "/imu") == 0
            records.append({"member": name, "sha256": hashlib.sha256(raw).hexdigest(),
                            "duration_ns": duration, "messages": total, "topics": topics})
    original = json.loads((PROJECT / "manuscript_arx_rbf_v1.8/PACKAGE_MANIFEST.json").read_text())
    for name, binding in original["bindings"].items():
        assert digest(PROJECT / name) == binding["sha256"], name
    result = {
        "project": "manufacturing", "operator": "Codex AI assistant",
        "time_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "python": sys.version, "interpreter": sys.executable,
        "platform": platform.platform(), "script_sha256": digest(Path(__file__)),
        "archive_sha256": digest(ARCHIVE), "records": records,
        "preserved_v1_8_bindings": len(original["bindings"]),
        "message_payloads_read": False, "models_fitted": False,
        "detection_metrics_computed": False,
        "scope": "Metadata consistency only; no physical truth, authentication or performance validation",
    }
    output = LOCAL / "METADATA_CHECKS.json"
    with output.open("x") as handle:
        json.dump(result, handle, indent=2)
        handle.write("\n")
    print(json.dumps({"records": len(records), "topic_counts_consistent": True,
                      "preserved_bindings": len(original["bindings"]), "receipt": str(output)}))


if __name__ == "__main__":
    main()
