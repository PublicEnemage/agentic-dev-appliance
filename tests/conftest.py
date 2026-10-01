"""Shared fixtures. Each test builds a small appliance repository in a temp folder,
copies this repository's configuration into it, and adds the artifacts it needs.

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

CONFIG_FILES = [
    "appliance.yml",
    "CLAUDE.md",
    "STATE.md",
    "docs/artifact-types.yml",
    "docs/roles.yml",
    "docs/enforcement.yml",
    "docs/dor/floor.yml",
    "docs/dor/checklist.yml",
    "docs/registry.md",
    "docs/skips.yml",
]

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
    for rel in CONFIG_FILES:
        dst = tmp_path / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(REPO / rel, dst)
    return Repo(tmp_path)


def messages(report) -> str:
    return "\n".join(str(f) for f in report.findings)
