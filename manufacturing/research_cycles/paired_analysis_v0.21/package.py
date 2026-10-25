"""Build a local explicit-allowlist addendum and verify clean portable replay."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
import zipfile
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def main():
    tick = time.monotonic()
    archive = HERE / "manufacturing-paired-analysis-v0.21.zip"
    validation = HERE / "clean_validation_001"
    if archive.exists() or validation.exists():
        raise ValueError("Refusing to replace consumed archive/validation paths")
    manifest = json.loads((HERE / "INPUT_MANIFEST.json").read_text())
    names = ["analyze.py", "test_analysis.py", "make_report.py", "package.py", "README.md",
             "REPORT.md", "INPUT_MANIFEST.json", "ATTEMPT_HISTORY.json", "PROVENANCE.json",
             "PRIOR_ARCHIVE_AUDIT.json"]
    names += ["inputs/" + name for name in sorted(manifest["files"])]
    names += ["results_002/" + name for name in ("paired.json", "paired_effects.csv", "episode_pairs.csv", "REPLAY.json")]
    bindings = {name: dict(sha256=digest(HERE / name), bytes=(HERE / name).stat().st_size) for name in names}
    write(HERE / "PACKAGE_MANIFEST.json", dict(scope="saved synthetic outcome descriptive analysis addendum",
          files=bindings, raw_real_data=False, network_required=False, original_v17_modified=False))
    names.append("PACKAGE_MANIFEST.json")
    with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as out:
        for name in names:
            out.write(HERE / name, arcname="paired_analysis_v0.21/" + name)
    validation.mkdir()
    with zipfile.ZipFile(archive) as inp:
        if inp.testzip() is not None:
            raise ValueError("CRC check failed")
        if set(inp.namelist()) != {"paired_analysis_v0.21/" + name for name in names}:
            raise ValueError("Unexpected archive member")
        inp.extractall(validation)
    root = validation / "paired_analysis_v0.21"
    for name, record in bindings.items():
        if digest(root / name) != record["sha256"]:
            raise ValueError("Extracted artifact differs: " + name)
    commands = []
    for label, cmd in (
        ("synthetic_tests", [sys.executable, "-I", "test_analysis.py"]),
        ("saved_result_replay", [sys.executable, "-I", "analyze.py", "--output", "clean_replay"]),
    ):
        completed = subprocess.run(cmd, cwd=root, capture_output=True, text=True, timeout=30)
        log = validation / (label + ".log")
        log.write_text(completed.stdout + completed.stderr)
        commands.append(dict(label=label, command=cmd, cwd=str(root), returncode=completed.returncode,
                             log_sha256=digest(log)))
        if completed.returncode:
            write(validation / "FAILURE.json", dict(commands=commands, failed=label))
            raise RuntimeError("Clean command failed: " + label)
    replay_files = ("paired.json", "paired_effects.csv", "episode_pairs.csv", "REPLAY.json")
    for name in replay_files:
        if (root / "clean_replay" / name).read_bytes() != (root / "results_002" / name).read_bytes():
            raise ValueError("Clean replay differs: " + name)
    receipt = dict(status="passed", utc=datetime.now(timezone.utc).isoformat(),
                   archive=archive.name, archive_bytes=archive.stat().st_size, archive_sha256=digest(archive),
                   archive_members=len(names), bound_files=len(bindings), exact_replay_files=list(replay_files),
                   synthetic_tests=8, replay_checks=json.loads((root / "clean_replay/REPLAY.json").read_text())["checks"],
                   commands=commands, wall_seconds=time.monotonic() - tick,
                   training=False, new_simulation=False, raw_data=False, network=False,
                   original_archive_mutation=False, publication=False)
    write(HERE / "BUILD_AND_REPLAY_RECEIPT.json", receipt)
    print(json.dumps({k: receipt[k] for k in ("status", "archive_bytes", "archive_sha256", "archive_members", "synthetic_tests", "replay_checks")}))


if __name__ == "__main__":
    main()
