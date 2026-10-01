"""E11: registry integrity.

The registry (docs/registry.md) is append-only institutional memory. Refuses when:
- code fences are unbalanced, so later entries would render as code
- an entry heading is malformed, or IDs are not unique and ascending without gaps
- an entry misses a required field, or its Type is not near-miss or external
- a near-miss entry names no check as its countermeasure (design rule 7)

Entries look like:

    ## RG-001 — Short title
    **Type:** near-miss
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

REGISTRY = "docs/registry.md"
HEADING = re.compile(r"^## (?P<id>RG-(?P<n>\d{3})) — \S")
FIELDS = ["Type", "Date", "What happened", "What was at risk", "What caught it", "Countermeasure", "Check"]
TYPES = {"near-miss", "external"}


def strip_comments(text: str) -> str:
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)


def check(root: Path, rel: str = REGISTRY) -> Report:
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
            m = HEADING.match(ln)
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
            report.add("E11", rel, f"{rid}: expected RG-{expected:03d}; ids are ascending without gaps")
        expected = n + 1
        body = "\n".join(lines)
        values = {}
        for f in FIELDS:
            m = re.search(rf"^\*\*{re.escape(f)}:\*\*\s*(.+)$", body, re.M)
            if not m or not m.group(1).strip():
                report.add("E11", rel, f"{rid}: missing field '{f}'")
            else:
                values[f] = m.group(1).strip()
        t = values.get("Type")
        if t and t not in TYPES:
            report.add("E11", rel, f"{rid}: Type '{t}' is not one of {sorted(TYPES)}")
        if t == "near-miss" and values.get("Check", "").lower() in {"none", "n/a", "tbd", "be more careful"}:
            report.add("E11", rel, f"{rid}: a near-miss countermeasure must ship as a check")
    return report


if __name__ == "__main__":
    sys.exit(check(root_from_argv()).emit("E11 registry"))
