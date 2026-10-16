# Workspace and compute audit

Inspection date: **2026-10-16**, using the user's Asia/Karachi date. Scope: `/Users/matrixusman/CUI/DigitalTwin`, plus read-only local hardware/interpreter checks. No search of unrelated personal directories or cloud accounts.

**Historical scope:** this record describes the original single-water workspace and subsequent skill installation. The workspace now contains three independent project folders; see [workspace decisions](WORKSPACE_DECISIONS.md) and [portfolio brief](../PROJECT_BRIEF.md). Hardware facts remain shared observations, not a fresh capacity or runtime measurement.

## Initial inventory

`ls -la` showed only `.` and `..`. `rg --files` found no files. `git status --short` and `git rev-parse --show-toplevel` reported that this was not a Git repository. Those are observed initial conditions, before the audit documents were created.

| Input | Observed status |
|---|---|
| SWaT raw/processed data, archives, labels | None in workspace; external location/access unknown |
| WADI raw/processed data, archives, labels | None in workspace; external location/access unknown |
| `literature_candidates.md` | Not supplied as a file |
| Conversation notes | Initially absent; user later pasted previous discussion into chat |
| `ijcatr15081004 (1).pdf` | Filename/title mentioned in notes; actual PDF unavailable |
| Code, environments, tests, checkpoints, logs | None initially |
| Git repository/remotes | None; this audit did not initialize or publish a repository |

No dataset manifest can be populated with hashes, row counts, or filenames actually received yet. Provider-described filenames in other documents are expected candidates, not a local inventory.

## Observed hardware and software

| Item | Observation | Implication |
|---|---|---|
| OS/architecture | macOS 27.2, Darwin 27.2.0, arm64 | ARM/macOS compatibility needs checking per upstream method |
| Computer | MacBook Pro / Apple M5 Pro | Local machine only; remote/HPC allocation unknown |
| CPU | 18 cores reported by hardware profile and Python | No throughput benchmark performed |
| Memory | 24 GB unified memory | Avoid materializing every sliding window; actual peak RAM unmeasured |
| GPU | Apple M5 Pro, 20 GPU cores, Metal supported | Not NVIDIA CUDA; MPS execution/determinism untested |
| Workspace volume | 926 GiB total, 816 GiB used, approximately 49 GiB available, 95% capacity reported | APFS figures are as reported; free space is time-sensitive. Do not assume room for all releases/PCAPs |
| Default `python3` | Homebrew Python 3.15.0 | Not selected for baseline compatibility |
| Proposed available interpreter | `/opt/homebrew/bin/python3.11`, Python 3.11.17; `venv` module found | Candidate harness interpreter; no environment created |
| Other interpreter | Miniconda base Python 3.12.9 | Existing base/environment left unchanged |
| Git | 2.54.0 (Apple Git-157) | Available; workspace unversioned |
| `uv`, `nvidia-smi` | Not found on PATH | No assertion about every possible installation |
| ML/test packages in default Python 3.15 | `numpy`, `pandas`, `scipy`, `scikit-learn`, `torch`, `pytest`, `openpyxl`, `pyarrow` not installed there | This is not an inventory of other interpreters; no package installed |

A combined `sysctl` query failed with `Operation not permitted`; hardware was instead read using `system_profiler`. No escalation or system modification was needed. No CUDA server, paid service, or external compute entitlement was verified.

## Read-only audit commands

Commands were run from the workspace. The initial file search used `rg --files` with Markdown/configuration patterns, followed by a hidden-file inventory. Representative exact commands:

```sh
pwd
ls -la
rg --files --hidden -g '!.git' -g '!.DS_Store' /Users/matrixusman/CUI/DigitalTwin
git status --short
git rev-parse --show-toplevel
uname -srm
sw_vers
sysctl -n machdep.cpu.brand_string hw.ncpu hw.memsize
df -h .
system_profiler SPDisplaysDataType
system_profiler SPHardwareDataType | rg 'Model Name|Model Identifier|Chip:|Total Number of Cores|Memory:'
command -v python3 python uv conda nvidia-smi git
python3 --version
python3 -m pip --version
git --version
/opt/homebrew/Caskroom/miniconda/base/bin/python --version
/opt/homebrew/bin/python3.11 --version
```

Small standard-library Python probes read `sys.executable`, `platform.machine()`, `os.cpu_count()`, `shutil.which('nvidia-smi')`, installed distribution metadata, and availability of `venv`. They did not import/train models. Research helpers inspected public sources; any downloaded public manuscript/code audit material is distinct from benchmark data.

## Changes and limits

Created only research documentation and a protective `.gitignore` in this workspace. No environment, application, loader, model, benchmark test, or experiment was implemented. No system-wide packages changed. No raw dataset was present to hash or test; absence is limited to the audited workspace. The final document consistency check is not a benchmark or scientific result.

## Subsequent authorized skill setup — 2026-10-16

The user subsequently authorized installing and using the recommended research skill. ARS-Codex 3.23.1 is now installed under `.agents/skills/academic-research-suite/`, with pinned provenance in [Research skill setup](RESEARCH_SKILL_SETUP.md). Its bundled code, examples, and test fixtures are third-party skill resources; they are not project implementations, SWaT/WADI access, or experimental results. No benchmark-like data/archive files were found outside this vendored skill during the follow-up inventory. No system packages, runtime hooks, research environment, or training runs were added.
