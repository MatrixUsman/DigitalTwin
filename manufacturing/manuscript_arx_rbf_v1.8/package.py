"""Package only the editable manuscript's transitive inputs; check clean extraction."""
from pathlib import Path, PurePosixPath
import datetime
import hashlib
import json
import os
import re
import subprocess
import tempfile
import zipfile

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
TARGET = PROJECT / "output/ARX-RBF-Muhammad-Usman-v1.8-latex.zip"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    selected = {"references.bib", "README.md", "AUTHOR_ACTIONS.md"}
    pending = ["main.tex"]
    while pending:
        name = pending.pop()
        if name in selected:
            continue
        path = (HERE / name).resolve()
        assert path.is_relative_to(HERE) and path.is_file(), name
        selected.add(name)
        source = path.read_text()
        for child in re.findall(r"\\(?:input|include)\{([^}]+)\}", source):
            pending.append(child if child.endswith(".tex") else child + ".tex")
        for child in re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", source):
            assert child.endswith(".pdf") and (HERE / child).is_file(), child
            selected.add(child)
    assert len([x for x in selected if x.startswith("figures/")]) == 6
    members = {name: digest(HERE / name) for name in sorted(selected)}
    if not TARGET.exists():
        with zipfile.ZipFile(TARGET, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for name in members:
                info = zipfile.ZipInfo(name, (2026, 10, 24, 0, 0, 0))
                info.external_attr = 0o100644 << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, (HERE / name).read_bytes())
    parent = PROJECT / "local/manuscript_arx_rbf_v1.8"
    with tempfile.TemporaryDirectory(prefix="source_check_", dir=parent) as temporary:
        root = Path(temporary)
        with zipfile.ZipFile(TARGET) as archive:
            assert archive.testzip() is None
            assert sorted(archive.namelist()) == sorted(members)
            for name in archive.namelist():
                path = PurePosixPath(name)
                assert not path.is_absolute() and ".." not in path.parts
            archive.extractall(root)
        assert all(digest(root / n) == h for n, h in members.items())
        compiler = PROJECT / "local/pdf_build_v0.1/bin/tectonic"
        command = [str(compiler), "--untrusted", "--only-cached", "main.tex"]
        env = dict(os.environ)
        env["TECTONIC_CACHE_DIR"] = str(PROJECT / "local/recovery_v0.7/pdf_build/cache")
        built = subprocess.run(command, cwd=root, env=env, text=True, capture_output=True)
        number = len(list(parent.glob("source_archive_build*.log"))) + 1
        build_log = parent / f"source_archive_build_{number:03}.log"
        build_log.write_text(built.stdout + built.stderr)
        assert built.returncode == 0, built.stderr
        subprocess.run(["pdftotext", "-layout", str(root / "main.pdf"), str(root / "main.txt")], check=True)
        original = parent / "manuscript.txt"
        assert (root / "main.txt").read_bytes() == original.read_bytes()
        extracted_pdf = digest(root / "main.pdf")
    record = {
        "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "archive": str(TARGET.relative_to(PROJECT)), "sha256": digest(TARGET),
        "bytes": TARGET.stat().st_size, "member_count": len(members), "members_sha256": members,
        "clean_extraction_and_member_checks": True, "offline_compile_returncode": built.returncode,
        "extracted_build_pdf_sha256": extracted_pdf,
        "extracted_build_text_identical_to_delivered_pdf": True,
        "build_command": command, "build_log": str(build_log.relative_to(PROJECT)),
        "cache": str(Path(env["TECTONIC_CACHE_DIR"]).relative_to(PROJECT)),
        "prior_attempt": "Initial archive compile lacked the existing project cache environment variable and was denied access to the default user cache. Its log is preserved as local/manuscript_arx_rbf_v1.8/source_archive_build.log. No scientific or document input changed.",
        "scope": "Editable manuscript only; not an experimental rerun archive or public release",
        "passed": True,
    }
    (HERE / "SOURCE_ARCHIVE.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({k: v for k, v in record.items() if k not in ("members_sha256", "build_command")}, indent=2))


if __name__ == "__main__":
    main()
