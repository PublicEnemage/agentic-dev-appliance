"""E20: a file name says what the file is for.

Refuses a text artifact (.md, .yml, .yaml, .txt) in the repository root, docs/ or .github/
whose name is generic: its stem, or every word of it, is one of a short list such as
registry, notes, misc, temp, final, draft or data. The slug of a numbered name
(`RP-001-frontend-architect`) is judged the same way.

The check refuses the worst names only. Whether a name is the briefest that makes the purpose
unambiguous, given its folder, is for the author and the challenger. Code and tests are out of
scope: their folders and language conventions carry the meaning.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from lib import Report, root_from_argv

GENERIC = {
    "registry", "notes", "misc", "temp", "tmp", "stuff", "data", "info", "doc", "docs", "file",
    "files", "new", "old", "final", "draft", "untitled", "todo", "scratch", "general", "other",
    "things", "thing", "text", "list", "log", "backup", "copy", "test", "tests", "example",
}
SUFFIXES = {".md", ".yml", ".yaml", ".txt"}
SCOPE = ("docs", ".github")
NUMBERED = re.compile(r"^[A-Za-z]+-\d+-(.+)$")


def generic(stem: str) -> bool:
    m = NUMBERED.match(stem)
    words = re.split(r"[-_. ]+", (m.group(1) if m else stem).lower())
    return all(w in GENERIC for w in words if w) and any(words)


def candidates(root: Path):
    for p in root.iterdir():
        if p.is_file():
            yield p
    for d in SCOPE:
        base = root / d
        if base.is_dir():
            yield from (p for p in base.rglob("*") if p.is_file())


def check(root: Path) -> Report:
    report = Report()
    for p in sorted(candidates(root)):
        if p.suffix.lower() in SUFFIXES and generic(p.stem):
            report.add("E20", p.relative_to(root), "generic file name; name what the file is for "
                       "(for example near-miss-registry.md, not registry.md)")
    return report


if __name__ == "__main__":
    sys.exit(check(root_from_argv(sys.argv[1:])).emit("E20 file names"))
