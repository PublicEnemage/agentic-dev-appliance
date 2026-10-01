"""E10: front matter, trace, location, naming, approval order and staleness.

Refuses when:
- an artifact has missing or invalid front matter, or a required field is missing
- the type is unknown, or the file sits outside its type's folder, including files with
  artifact front matter saved outside every artifact folder
- the file name does not match {PREFIX}-{NNN}-{slug}.md, or the id does not match the file name
- two artifacts share an id
- a parent, or an ID referenced in the body, does not exist (live-ID check)
- a non-root artifact has no parents
- an approved artifact lacks approved_at, has a parent that is not approved,
  or was approved before a parent was (re)approved: the child is stale
- an approved artifact has no review file, or its review has open findings
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from lib import Report, artifact_dirs, as_list, load_artifacts, load_config, read_front_matter, root_from_argv, to_datetime

NAME = re.compile(r"^(?P<id>(?P<prefix>[A-Z]+)-\d{3})-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")


SKIP_PARTS = {".git", "node_modules", ".venv", "venv", "__pycache__"}


def stray_artifacts(root: Path, types: dict):
    """Markdown files with artifact front matter (a known type and an id) that sit
    outside every artifact folder. Templates and test fixtures are excluded."""
    dirs = artifact_dirs(types)
    tdefs = types["types"]
    for p in root.rglob("*.md"):
        rel = p.relative_to(root)
        if SKIP_PARTS & set(rel.parts) or rel.parts[:2] in (("docs", "templates"), ("tests", "fixtures")):
            continue
        rel_s = rel.as_posix()
        if any(rel_s.startswith(d + "/") for d in dirs):
            continue
        meta, _ = read_front_matter(p)
        if meta and meta.get("type") in tdefs and meta.get("id"):
            yield rel_s, meta["type"]


def check(root: Path) -> Report:
    report = Report()
    cfg = load_config(root)
    types = cfg["types"]
    tdefs = types["types"]
    statuses = set(types["statuses"])
    required = types["required_fields"]
    prefixes = {d["prefix"]: name for name, d in tdefs.items()}
    id_pattern = re.compile(r"\b(?:%s)-\d{3}\b" % "|".join(sorted(prefixes)))

    arts = load_artifacts(root, types, report)
    for rel, t in stray_artifacts(root, types):
        report.add("E10", rel, f"looks like a '{t}' artifact but sits outside the artifact folders; it belongs in {tdefs[t]['dir']}/")
    by_id: dict[str, object] = {}

    for a in arts:
        m = a.meta
        for f in required:
            if f not in m or m[f] in (None, "") and f != "parents":
                report.add("E10", a.rel, f"missing required field '{f}'")
        t = m.get("type")
        if t not in tdefs:
            report.add("E10", a.rel, f"unknown type '{t}'")
            continue
        tdef = tdefs[t]
        rel_dir = Path(a.rel).parent.as_posix()
        if not (rel_dir == tdef["dir"] or rel_dir.startswith(tdef["dir"] + "/")):
            report.add("E10", a.rel, f"type '{t}' belongs in {tdef['dir']}/")
        nm = NAME.match(a.path.name)
        if not nm:
            report.add("E10", a.rel, "file name must be {PREFIX}-{NNN}-{slug}.md in lower-case kebab slug")
        else:
            if nm.group("prefix") != tdef["prefix"]:
                report.add("E10", a.rel, f"type '{t}' uses prefix {tdef['prefix']}")
            if nm.group("id") != a.id:
                report.add("E10", a.rel, f"id '{a.id}' does not match file name")
        if a.status not in statuses:
            report.add("E10", a.rel, f"status '{a.status}' is not one of {sorted(statuses)}")
        if a.id in by_id:
            report.add("E10", a.rel, f"duplicate id '{a.id}' (also {by_id[a.id].rel})")
        else:
            by_id[a.id] = a

    for a in arts:
        t = a.meta.get("type")
        if t not in tdefs:
            continue
        parents = [str(p) for p in as_list(a.meta.get("parents"))]
        if not parents and not tdefs[t].get("root"):
            report.add("E10", a.rel, "needs at least one parent: every artifact traces upstream")
        for p in parents:
            if p not in by_id:
                report.add("E10", a.rel, f"parent '{p}' does not exist")
        for ref in sorted(set(id_pattern.findall(a.body))):
            if ref not in by_id:
                report.add("E10", a.rel, f"references '{ref}', which does not exist")

        if a.status != "approved":
            continue
        approved_at = to_datetime(a.meta.get("approved_at"))
        if approved_at is None:
            report.add("E10", a.rel, "approved artifacts need approved_at")
        for p in parents:
            parent = by_id.get(p)
            if parent is None:
                continue
            if parent.status != "approved":
                report.add("E10", a.rel, f"approved before parent '{p}' is approved (parent status: {parent.status})")
                continue
            p_at = to_datetime(parent.meta.get("approved_at"))
            if approved_at and p_at and p_at > approved_at:
                report.add("E10", a.rel, f"stale: parent '{p}' was approved after this artifact; re-challenge and re-approve")

        review = a.path.with_name(a.path.name[:-3] + ".review.md")
        if not review.is_file():
            report.add("E10", a.rel, f"approved without a review file ({review.name})")
        else:
            rmeta, _ = read_front_matter(review)
            rrel = str(review.relative_to(root))
            if rmeta is None:
                report.add("E10", rrel, "review file has missing or invalid front matter")
            else:
                if str(rmeta.get("artifact")) != a.id:
                    report.add("E10", rrel, f"review names artifact '{rmeta.get('artifact')}', expected '{a.id}'")
                if rmeta.get("challenger_seat") != a.meta.get("challenger_seat"):
                    report.add("E10", rrel, "review challenger_seat differs from the artifact's challenger_seat")
                if rmeta.get("open_findings") != 0:
                    report.add("E10", rrel, "approval blocked: open_findings must be 0")
    return report


if __name__ == "__main__":
    sys.exit(check(root_from_argv()).emit("E10 artifacts"))
