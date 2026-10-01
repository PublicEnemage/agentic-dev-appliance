"""Shared fixtures. Each test builds a small appliance repository in a temp folder from
the appliance's own files plus fixed project defaults, and adds the artifacts it needs.

Every check has at least one test where the check passes and several where it must
refuse. A check that has never been seen to refuse is not trusted (design rule 2).
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tools" / "checks"))

FIXTURES = REPO / "tests" / "fixtures" / "defaults"

# Files the appliance owns. Projects do not edit them, so tests read the real ones.
APPLIANCE_FILES = [
    "docs/artifact-types.yml",
    "docs/enforcement.yml",
    "docs/dor/floor.yml",
]

# Files each project edits at bootstrap. Tests use fixed defaults instead, so a project's
# own choices never break the template's tests (dry run 1, Q11).
PROJECT_DEFAULTS = {
    "appliance.yml": "appliance.yml",
    "CLAUDE.md": "CLAUDE.md",
    "STATE.md": "STATE.md",
    "docs/roles.yml": "roles.yml",
    "docs/registry.md": "registry.md",
    "docs/skips.yml": "skips.yml",
}


def default_checklist() -> str:
    floor = yaml.safe_load((REPO / "docs/dor/floor.yml").read_text())
    rows = {r["id"]: {"status": "per-increment" if r["gate"] == "increment" else "open"} for r in floor["rows"]}
    return yaml.safe_dump({"floor_version": floor["version"], "rows": rows}, sort_keys=False)


TYPES = yaml.safe_load((REPO / "docs/artifact-types.yml").read_text())["types"]


class Repo:
    def __init__(self, root: Path):
        self.root = root

    def write(self, rel: str, text: str) -> Path:
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        return p

    def artifact(self, type_: str, n: int, slug: str = "item", body: str = "Body.\n",
                 review: bool | dict = True, folder: str | None = None, **meta) -> Path:
        """Write an artifact. Approved artifacts get a clean review file unless review=False."""
        t = TYPES[type_]
        aid = meta.pop("id", f"{t['prefix']}-{n:03d}")
        fm = {
            "id": aid,
            "type": type_,
            "title": f"{type_} {n}",
            "status": "approved",
            "author_seat": "Product",
            "challenger_seat": "Architect",
            "approver": "Intent Owner",
            "parents": [],
            "approved_at": "2026-10-01T10:00:00",
        }
        fm.update(meta)
        name = f"{t['prefix']}-{n:03d}-{slug}.md"
        rel = f"{folder or t['dir']}/{name}"
        path = self.write(rel, "---\n" + yaml.safe_dump(fm, sort_keys=False) + "---\n\n" + body)
        if fm["status"] == "approved" and review is not False:
            rmeta = {"artifact": aid, "challenger_seat": fm["challenger_seat"], "open_findings": 0}
            if isinstance(review, dict):
                rmeta.update(review)
            self.write(rel[:-3] + ".review.md", "---\n" + yaml.safe_dump(rmeta, sort_keys=False) + "---\n\nNo findings.\n")
        return path

    def edit_yaml(self, rel: str, fn) -> None:
        p = self.root / rel
        data = yaml.safe_load(p.read_text())
        fn(data)
        p.write_text(yaml.safe_dump(data, sort_keys=False))


@pytest.fixture
def repo(tmp_path: Path) -> Repo:
    for rel in APPLIANCE_FILES:
        dst = tmp_path / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(REPO / rel, dst)
    for rel, name in PROJECT_DEFAULTS.items():
        dst = tmp_path / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(FIXTURES / name, dst)
    (tmp_path / "docs/dor/checklist.yml").write_text(default_checklist())
    return Repo(tmp_path)


def messages(report) -> str:
    return "\n".join(str(f) for f in report.findings)
