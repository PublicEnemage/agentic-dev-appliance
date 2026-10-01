"""Shared helpers for the appliance checks.

Every check reports findings as `CHECK path: message` and exits non-zero when any
finding is an error. Checks read files only; none of them change the repository.
"""

from __future__ import annotations

import datetime as _dt
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

FRONT_MATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.S)


@dataclass
class Finding:
    check: str
    path: str
    message: str

    def __str__(self) -> str:
        return f"{self.check} {self.path}: {self.message}"


@dataclass
class Report:
    findings: list[Finding] = field(default_factory=list)

    def add(self, check: str, path: Path | str, message: str) -> None:
        self.findings.append(Finding(check, str(path), message))

    @property
    def ok(self) -> bool:
        return not self.findings

    def emit(self, label: str) -> int:
        for f in self.findings:
            print(f)
        status = "PASS" if self.ok else f"FAIL ({len(self.findings)})"
        print(f"[{label}] {status}")
        return 0 if self.ok else 1


def clean_git_env() -> dict[str, str]:
    """The environment without variables that redirect git to another repository.

    Git sets GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE while a hook runs. A git command
    started from inside the hook inherits them and acts on the hooked repository, whatever
    its working directory. Registry entry RG-001: tests run by the pre-push hook committed
    into the real repository and flipped it to a bare repository, while reporting a pass.
    GIT_CONFIG_* variables are kept; they carry proxy and credential settings.
    """
    import os
    return {k: v for k, v in os.environ.items() if not k.startswith("GIT_") or k.startswith("GIT_CONFIG")}


def repo_root(start: Path | None = None) -> Path:
    """Find the repository root: the nearest folder holding appliance.yml."""
    here = (start or Path.cwd()).resolve()
    for candidate in [here, *here.parents]:
        if (candidate / "appliance.yml").is_file():
            return candidate
    raise SystemExit("appliance.yml not found; run from inside an appliance repository")


def root_from_argv(argv: list[str] | None = None) -> Path:
    args = sys.argv[1:] if argv is None else argv
    for i, a in enumerate(args):
        if a == "--root" and i + 1 < len(args):
            return Path(args[i + 1]).resolve()
    return repo_root()


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def read_front_matter(path: Path) -> tuple[dict | None, str]:
    """Return (front matter, body). Front matter is None when absent or invalid."""
    text = path.read_text(encoding="utf-8")
    m = FRONT_MATTER.match(text)
    if not m:
        return None, text
    try:
        data = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return None, text
    if not isinstance(data, dict):
        return None, text
    return data, text[m.end():]


def to_datetime(value: Any) -> _dt.datetime | None:
    """Accept a YAML date, datetime or ISO string; return a naive UTC datetime."""
    if value is None:
        return None
    if isinstance(value, _dt.datetime):
        dt = value
    elif isinstance(value, _dt.date):
        dt = _dt.datetime(value.year, value.month, value.day)
    else:
        try:
            dt = _dt.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        except ValueError:
            return None
    if dt.tzinfo is not None:
        dt = dt.astimezone(_dt.timezone.utc).replace(tzinfo=None)
    return dt


def as_list(value: Any) -> list:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


@dataclass
class Artifact:
    path: Path
    rel: str
    meta: dict
    body: str

    @property
    def id(self) -> str:
        return str(self.meta.get("id", ""))

    @property
    def status(self) -> str:
        return str(self.meta.get("status", ""))


def artifact_dirs(types: dict) -> set[str]:
    return {t["dir"] for t in types["types"].values()}


def iter_artifact_files(root: Path, types: dict):
    """Yield every artifact file: markdown under an artifact directory,
    excluding README.md and review files."""
    seen: set[Path] = set()
    for d in sorted(artifact_dirs(types)):
        base = root / d
        if not base.is_dir():
            continue
        for p in sorted(base.rglob("*.md")):
            if p in seen or p.name.lower() == "readme.md" or p.name.endswith(".review.md"):
                continue
            seen.add(p)
            yield p


def load_artifacts(root: Path, types: dict, report: Report | None = None) -> list[Artifact]:
    out = []
    for p in iter_artifact_files(root, types):
        meta, body = read_front_matter(p)
        rel = str(p.relative_to(root))
        if meta is None:
            if report is not None:
                report.add("E10", rel, "missing or invalid front matter")
            continue
        out.append(Artifact(p, rel, meta, body))
    return out


def load_config(root: Path) -> dict:
    return {
        "appliance": load_yaml(root / "appliance.yml"),
        "types": load_yaml(root / "docs/artifact-types.yml"),
        "roles": load_yaml(root / "docs/roles.yml"),
        "floor": load_yaml(root / "docs/dor/floor.yml"),
    }
