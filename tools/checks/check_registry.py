"""E11: registry integrity.

Two append-only registries are institutional memory. Refuses, in each, when:
- code fences are unbalanced, so later entries would render as code
- an entry heading is malformed, or IDs are not unique and ascending without gaps
- an entry misses a required field

The near-miss registry (docs/near-miss-registry.md, ids RG-NNN) also refuses a countermeasure
that names no check (design rule 7). The known issues registry (docs/known-issues-registry.md,
ids KI-NNN) holds limitations we cannot design away and refuses an empty workaround.

A near-miss entry looks like:

    ## RG-001 — Short title
    **Date:** 2026-10-01
    **What happened:** ...
    **What was at risk:** ...
    **What caught it:** ...
    **Countermeasure:** ...
    **Check:** E3
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from lib import Report, root_from_argv

REGISTRY = "docs/near-miss-registry.md"
KNOWN_ISSUES = "docs/known-issues-registry.md"
NEAR_MISS_FIELDS = ["Date", "What happened", "What was at risk", "What caught it", "Countermeasure", "Check"]
KNOWN_ISSUE_FIELDS = ["Date", "What the limitation is", "Who or what it affects", "Why we cannot solve it",
                      "Workaround", "Revisit when"]


EMPTY = {"none", "n/a", "tbd"}


def strip_comments(text: str) -> str:
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)


def check(root: Path, rel: str | None = None) -> Report:
    """Check one registry file, or both project registries when none is named."""
    if rel is None:
        report = check(root, REGISTRY)
        report.findings += check(root, KNOWN_ISSUES).findings
        return report
    known = rel.endswith("known-issues-registry.md")
    prefix, fields = ("KI", KNOWN_ISSUE_FIELDS) if known else ("RG", NEAR_MISS_FIELDS)
    heading = re.compile(rf"^## (?P<id>{prefix}-(?P<n>\d{{3}})) — \S")
    report = Report()
    path = root / rel
    if not path.is_file():
        report.add("E11", rel, "registry is missing")
        return report
    raw = path.read_text(encoding="utf-8")
    fences = [ln for ln in raw.splitlines() if ln.lstrip().startswith("```")]
    if len(fences) % 2:
        report.add("E11", rel, "unbalanced code fence; entries after it render as code")

    text = strip_comments(raw)
    entries: list[tuple[str, int, list[str]]] = []
    current: list[str] | None = None
    for ln in text.splitlines():
        if ln.startswith("## "):
            m = heading.match(ln)
            if not m:
                report.add("E11", rel, f"malformed entry heading: '{ln.strip()}'")
                current = None
                continue
            current = []
            entries.append((m.group("id"), int(m.group("n")), current))
        elif current is not None:
            current.append(ln)

    expected = 1
    seen: set[str] = set()
    for rid, n, lines in entries:
        if rid in seen:
            report.add("E11", rel, f"{rid}: duplicate id")
        seen.add(rid)
        if n != expected:
            report.add("E11", rel, f"{rid}: expected {prefix}-{expected:03d}; ids are ascending without gaps")
        expected = n + 1
        body = "\n".join(lines)
        values = {}
        for f in fields:
            m = re.search(rf"^\*\*{re.escape(f)}:\*\*\s*(.+)$", body, re.M)
            if not m or not m.group(1).strip():
                report.add("E11", rel, f"{rid}: missing field '{f}'")
            else:
                values[f] = m.group(1).strip()
        if known:
            if values.get("Workaround", "").lower() in EMPTY:
                report.add("E11", rel, f"{rid}: a known issue needs a written workaround")
        elif values.get("Check", "").lower() in EMPTY | {"be more careful"}:
            report.add("E11", rel, f"{rid}: a near-miss countermeasure must ship as a check")
    return report


if __name__ == "__main__":
    sys.exit(check(root_from_argv()).emit("E11 registry"))
