"""E15: append-only migrations (standard STD-001, clause 2).

A merged migration is never edited or deleted; a fix is a new migration. Compares the
current commit with a base ref and refuses any modified, deleted or renamed file under
the migrations folder named in appliance.yml (data.migrations_dir).

Base ref, in order: --base REF, the APPLIANCE_BASE environment variable, origin/main.
A project with no migrations folder passes. When the folder exists but the base cannot
be resolved, the check fails: a gate that silently skips is not a gate.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from lib import Report, clean_git_env, load_yaml, root_from_argv


def git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, env=clean_git_env())


def check(root: Path, base: str | None = None) -> Report:
    report = Report()
    data_cfg = (load_yaml(root / "appliance.yml").get("data") or {})
    mdir = data_cfg.get("migrations_dir", "migrations")
    if not (root / mdir).is_dir():
        return report
    base = base or os.environ.get("APPLIANCE_BASE") or "origin/main"
    if git(root, "rev-parse", "--verify", "--quiet", base + "^{commit}").returncode != 0:
        report.add("E15", mdir, f"cannot resolve base ref '{base}'; fetch it or pass --base, the check cannot run")
        return report
    merge_base = git(root, "merge-base", base, "HEAD")
    since = merge_base.stdout.strip() if merge_base.returncode == 0 else base
    diff = git(root, "diff", "--name-status", "--no-renames", f"{since}..HEAD", "--", mdir)
    if diff.returncode != 0:
        report.add("E15", mdir, f"git diff failed: {diff.stderr.strip()}")
        return report
    for line in diff.stdout.splitlines():
        status, _, path = line.partition("\t")
        if status.startswith("M"):
            report.add("E15", path, "merged migration edited; migrations are append-only, add a new one")
        elif status.startswith("D"):
            report.add("E15", path, "merged migration deleted; migrations are append-only, add a new one")
    return report


if __name__ == "__main__":
    args = sys.argv[1:]
    base = args[args.index("--base") + 1] if "--base" in args else None
    sys.exit(check(root_from_argv(), base).emit("E15 migrations"))
