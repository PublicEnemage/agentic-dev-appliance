"""DOR: the Definition of Ready checklist against the pinned floor.

Structure (always checked). Refuses when:
- the checklist pins a floor version other than appliance.yml's floor_version
- a floor row is missing from the checklist, or redefines the floor rule (weakening)
- a project row is not a child of a floor row (finer, never coarser)
- a row has no status, or an unknown status
- a met row has no evidence, or cites an artifact id or path that does not exist
- a not-applicable row lacks a reason or an approver
- a parent row is met while one of its children is still open

Gate (with --gate GATE). Also refuses when any row for that gate or an earlier one
is open, or cites evidence that is not approved. Increment rows are checked per
increment intent: every approved increment intent must answer each I row.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from lib import Report, as_list, load_artifacts, load_config, load_yaml, root_from_argv

STATUSES = {"open", "met", "not-applicable"}
CHECKLIST = "docs/dor/checklist.yml"


def floor_parent(row_id: str, floor_ids: set[str]) -> str | None:
    head = row_id.split(".")[0]
    return head if head in floor_ids and row_id != head else None


ART_ID = re.compile(r"^[A-Z]+-\d{3}$")


def evidence_problem(e: str, known_ids: set[str], root: Path) -> str | None:
    """Evidence is an artifact id, a URL, or a path that exists in the repository."""
    if ART_ID.match(e):
        return None if e in known_ids else f"evidence '{e}' is not an artifact id"
    if "://" in e:
        return None
    return None if (root / e).exists() else f"evidence '{e}' is neither an artifact id, a URL, nor an existing path"


def check_entry(report: Report, where: str, rid: str, entry: dict, known_ids: set[str], root: Path) -> None:
    status = entry.get("status")
    if status is None:
        report.add("DOR", where, f"{rid}: blank row; status is required")
        return
    if status not in STATUSES:
        report.add("DOR", where, f"{rid}: status '{status}' is not one of {sorted(STATUSES)}")
        return
    if status == "met":
        ev = as_list(entry.get("evidence"))
        if not ev:
            report.add("DOR", where, f"{rid}: met without evidence")
        for e in ev:
            problem = evidence_problem(str(e), known_ids, root)
            if problem:
                report.add("DOR", where, f"{rid}: {problem}")
    if status == "not-applicable":
        if not entry.get("reason"):
            report.add("DOR", where, f"{rid}: not-applicable needs a reason")
        if not entry.get("approver"):
            report.add("DOR", where, f"{rid}: not-applicable needs an approver")


def check(root: Path, gate: str | None = None) -> Report:
    report = Report()
    cfg = load_config(root)
    floor = cfg["floor"]
    gates = floor["gates"]
    floor_rows = {r["id"]: r for r in floor["rows"]}
    floor_ids = set(floor_rows)
    arts = load_artifacts(root, cfg["types"])
    by_id = {a.id: a for a in arts}

    path = root / CHECKLIST
    if not path.is_file():
        report.add("DOR", CHECKLIST, "checklist is missing")
        return report
    checklist = load_yaml(path)
    pinned = str(checklist.get("floor_version"))
    if pinned != str(cfg["appliance"].get("floor_version")):
        report.add("DOR", CHECKLIST, f"floor_version {pinned} differs from appliance.yml")
    if pinned != str(floor.get("version")):
        report.add("DOR", CHECKLIST, f"floor_version {pinned} differs from the floor file ({floor.get('version')})")
    rows: dict = checklist.get("rows") or {}

    for fid in floor_ids:
        if fid not in rows:
            report.add("DOR", CHECKLIST, f"floor row {fid} is missing; floor rows cannot be deleted")
    for rid, entry in rows.items():
        entry = entry or {}
        if rid in floor_ids:
            if "rule" in entry:
                report.add("DOR", CHECKLIST, f"{rid}: floor rule text is fixed by the floor; remove 'rule'")
        else:
            parent = floor_parent(rid, floor_ids)
            if parent is None:
                report.add("DOR", CHECKLIST, f"{rid}: project rows must be children of a floor row, such as D2.1")
            if not entry.get("rule"):
                report.add("DOR", CHECKLIST, f"{rid}: project rows need their own 'rule'")
        if (floor_rows.get(rid.split(".")[0]) or {}).get("gate") == "increment":
            if entry.get("status") not in (None, "per-increment"):
                report.add("DOR", CHECKLIST, f"{rid}: increment rows take status 'per-increment'; each increment intent answers them")
            continue
        check_entry(report, CHECKLIST, rid, entry, set(by_id), root)

    for rid, entry in rows.items():
        parent = floor_parent(rid, floor_ids)
        if parent and (rows.get(parent) or {}).get("status") == "met" and (entry or {}).get("status") == "open":
            report.add("DOR", CHECKLIST, f"{parent}: met while child {rid} is open")

    if gate:
        if gate not in gates:
            report.add("DOR", CHECKLIST, f"unknown gate '{gate}'; gates are {gates}")
            return report
        upto = set(gates[: gates.index(gate) + 1]) - {"increment"}
        for rid, entry in rows.items():
            fgate = (floor_rows.get(rid.split(".")[0]) or {}).get("gate")
            if fgate not in upto:
                continue
            entry = entry or {}
            if entry.get("status") == "open":
                report.add("DOR", CHECKLIST, f"gate '{gate}' blocked: {rid} is open")
            if entry.get("status") == "met":
                for e in as_list(entry.get("evidence")):
                    a = by_id.get(str(e))
                    if a and a.status != "approved":
                        report.add("DOR", CHECKLIST, f"gate '{gate}' blocked: {rid} cites {e}, which is {a.status}")

    inc_rows = [rid for rid in rows if (floor_rows.get(rid.split(".")[0]) or {}).get("gate") == "increment"]
    for a in arts:
        if a.meta.get("type") != "increment-intent" or a.status != "approved":
            continue
        answers = a.meta.get("dor") or {}
        for rid in inc_rows:
            entry = answers.get(rid)
            if not isinstance(entry, dict):
                report.add("DOR", a.rel, f"{rid}: approved increment intent does not answer this row")
                continue
            if entry.get("status") == "open":
                report.add("DOR", a.rel, f"{rid}: open on an approved increment intent")
            check_entry(report, a.rel, rid, entry, set(by_id), root)
    return report


if __name__ == "__main__":
    args = sys.argv[1:]
    gate = args[args.index("--gate") + 1] if "--gate" in args else None
    sys.exit(check(root_from_argv(), gate).emit(f"DOR{' gate ' + gate if gate else ''}"))
