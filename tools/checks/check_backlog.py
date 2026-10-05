"""E21: the backlog process exists and says what it must.

Refuses when the backlog item issue form is missing, does not apply the backlog label, or
lacks a required field (seat, outcome, acceptance, inputs, parent).

The check sees that the intake is built. Whether an item is well argued, and the order of the
backlog, are for the seat that files it and the Engineering Lead. A check that a pull request
closes a filled-in item is designed and not built (docs/method/flow.md, task intake).
"""

from __future__ import annotations

import sys
from pathlib import Path

from lib import Report, load_yaml, root_from_argv

FORM = ".github/ISSUE_TEMPLATE/backlog-item.yml"
LABEL = "backlog"
REQUIRED = ["seat", "outcome", "acceptance", "inputs", "parent"]


def check(root: Path) -> Report:
    report = Report()
    form = root / FORM
    if not form.is_file():
        report.add("E21", FORM, "backlog item form is missing")
        return report
    data = load_yaml(form)
    if LABEL not in (data.get("labels") or []):
        report.add("E21", FORM, f"form does not apply the '{LABEL}' label")
    fields = {i.get("id"): i for i in (data.get("body") or []) if isinstance(i, dict)}
    for name in REQUIRED:
        item = fields.get(name)
        if item is None:
            report.add("E21", FORM, f"form has no '{name}' field")
        elif not (item.get("validations") or {}).get("required"):
            report.add("E21", FORM, f"field '{name}' is not required")
    return report


if __name__ == "__main__":
    sys.exit(check(root_from_argv(sys.argv[1:])).emit("E21 backlog"))
