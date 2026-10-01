"""SEATS: seat separation on every artifact, holder conflicts, and the D6 and C8 matches.

Refuses when:
- roles.yml names an unknown seat, a non-optional seat has no holder, a holder holds an incompatible pair, or the
  Steward shares a holder with another seat
- the Intent Owner and Engineering Lead share a holder without single_principal: true
- an artifact names an unknown seat, or its author, challenger and approver are
  not three different seats on three different holders
- the Steward authors, challenges or approves an artifact
- an artifact names an optional seat that no holder has adopted
- a type that needs a human approver has an agent approver
- an architecture artifact misses a D2 layer, or a layer's author and challenger
  are not distinct, qualified seats on different holders (D6)
- a business case names a domain area that no seat is qualified to challenge (C8)

These checks read declared seats. Binding a seat to a real identity is check E1 (v0.2).
"""

from __future__ import annotations

import sys
from pathlib import Path

from lib import Report, as_list, load_artifacts, load_config, root_from_argv

STEWARD = "Steward"


def holder_index(roles: dict) -> dict[str, str]:
    idx: dict[str, str] = {}
    for holder, seats in (roles.get("holders") or {}).items():
        for s in seats:
            idx[s] = holder
    return idx


def check(root: Path) -> Report:
    report = Report()
    cfg = load_config(root)
    roles = cfg["roles"]
    optional = roles.get("optional_seats") or {}
    seats = {**optional, **(roles.get("seats") or {})}
    tdefs = cfg["types"]["types"]
    layers = cfg["types"]["layers"]
    pairs = [frozenset(p) for p in roles.get("incompatible_pairs") or []]
    holders = roles.get("holders") or {}
    held_by = holder_index(roles)
    roles_rel = "docs/roles.yml"

    # Roster integrity.
    for pair in pairs:
        for s in pair:
            if s not in seats:
                report.add("SEATS", roles_rel, f"incompatible pair names unknown seat '{s}'")
    for holder, hs in holders.items():
        for s in hs:
            if s not in seats:
                report.add("SEATS", roles_rel, f"holder '{holder}' holds unknown seat '{s}'")
        hset = set(hs)
        for pair in pairs:
            if pair <= hset:
                a, b = sorted(pair)
                report.add("SEATS", roles_rel, f"holder '{holder}' holds incompatible seats {a} and {b}")
        if STEWARD in hset and len(hset) > 1:
            report.add("SEATS", roles_rel, f"holder '{holder}' holds the Steward seat with other seats")
    for s in seats:
        if s not in held_by and s not in optional:
            report.add("SEATS", roles_rel, f"seat '{s}' has no holder")
    if held_by.get("Intent Owner") and held_by.get("Intent Owner") == held_by.get("Engineering Lead"):
        if not cfg["appliance"].get("single_principal"):
            report.add("SEATS", roles_rel, "Intent Owner and Engineering Lead share a holder; set single_principal: true and keep the disclosure")

    def qualified(seat: str, layer: str) -> bool:
        return layer in (seats.get(seat) or {}).get("qualified_layers", [])

    def is_human(seat: str) -> bool:
        return (seats.get(seat) or {}).get("kind") == "human"

    for a in load_artifacts(root, cfg["types"]):
        m = a.meta
        author = m.get("author_seat")
        challenger = m.get("challenger_seat")
        approvers = [str(x) for x in as_list(m.get("approver"))]
        named = [("author_seat", author), ("challenger_seat", challenger)] + [("approver", x) for x in approvers]
        unknown = False
        for field, s in named:
            if s not in seats:
                report.add("SEATS", a.rel, f"{field} '{s}' is not a seat in {roles_rel}")
                unknown = True
            elif s == STEWARD:
                report.add("SEATS", a.rel, f"the Steward holds no artifact seat ({field})")
        if unknown:
            continue
        for field, s in named:
            if s in optional and s not in held_by:
                report.add("SEATS", a.rel, f"{field} '{s}' is an optional seat no one holds; adopt it through a role proposal")
        if author == challenger:
            report.add("SEATS", a.rel, "author and challenger are the same seat")
        if author in approvers:
            report.add("SEATS", a.rel, "author and approver are the same seat")
        if challenger in approvers:
            report.add("SEATS", a.rel, "challenger and approver are the same seat")
        if held_by.get(author) == held_by.get(challenger) and author != challenger:
            report.add("SEATS", a.rel, f"author and challenger seats share holder '{held_by.get(author)}'")
        for ap in approvers:
            if ap != author and held_by.get(ap) == held_by.get(author):
                report.add("SEATS", a.rel, f"author and approver seats share holder '{held_by.get(author)}'")
        t = m.get("type")
        if t in tdefs and tdefs[t].get("human_approver") and not any(is_human(x) for x in approvers):
            report.add("SEATS", a.rel, f"type '{t}' needs a human approver")

        if t == "architecture":
            section = m.get("layers") or {}
            for layer in layers:
                entry = section.get(layer)
                if not isinstance(entry, dict):
                    report.add("D6", a.rel, f"layer '{layer}' has no section (floor row D2)")
                    continue
                if entry.get("not_applicable"):
                    if not entry.get("approver"):
                        report.add("D6", a.rel, f"layer '{layer}' is not-applicable without an approver")
                    continue
                la, lc = entry.get("author_seat"), entry.get("challenger_seat")
                if la == lc:
                    report.add("D6", a.rel, f"layer '{layer}' needs different author and challenger seats")
                for role, s in (("author", la), ("challenger", lc)):
                    if s not in seats:
                        report.add("D6", a.rel, f"layer '{layer}' {role} '{s}' is not a seat")
                    elif s in optional and s not in held_by:
                        report.add("D6", a.rel, f"layer '{layer}': {s} is an optional seat no one holds; adopt it through a role proposal")
                    elif not qualified(s, layer):
                        report.add("D6", a.rel, f"layer '{layer}': {s} is not qualified for this layer in its charter; open a crew review")
                if la in seats and lc in seats and la != lc and held_by.get(la) == held_by.get(lc):
                    report.add("D6", a.rel, f"layer '{layer}' author and challenger share holder '{held_by.get(la)}'")

        if t == "business-case":
            domains = roles.get("qualified_domains") or {}
            for area in as_list(m.get("domain_areas")):
                name = area.get("area") if isinstance(area, dict) else area
                if not domains.get(name):
                    report.add("C8", a.rel, f"no seat is qualified to challenge domain area '{name}'; open a crew review")
    return report


if __name__ == "__main__":
    sys.exit(check(root_from_argv()).emit("SEATS"))
