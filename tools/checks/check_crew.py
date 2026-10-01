"""E17: a role proposal carries a job description the peer group can scrutinise.

A new seat arrives through a role proposal (docs/crew). Once the proposal is in review or
approved, this check refuses when:
- the charter lacks a trigger, inputs with their senders, the value added, outputs with
  their consumers, standards, templates, or an independent verifier with evidence
- an input comes from, or an output goes to, a seat that does not exist or is the
  proposed seat itself (work nobody else consumes has no demand)
- a standard or template under docs/ does not exist
- the verifier is the author, the proposed seat, or on the author's holder
- the peer review has fewer than two peers, a peer who is the author, the proposed seat or
  a human seat, a peer without a recommendation, demand statement and evidence, or leaves
  out an agent seat that sends the new seat input or consumes its output
- the peer group's recommendation is more favourable than its least favourable member
- the proposal is approved while the peer group recommends rejection

The check sees completeness and independence. Whether the job description is sound, and
whether the evidence is real, is the peers' and the Engineering Lead's call.
"""

from __future__ import annotations

import sys
from pathlib import Path

from lib import Report, load_artifacts, load_config, root_from_argv
from check_seats import holder_index

RANK = {"reject": 0, "accept-with-conditions": 1, "accept": 2}
HUMAN_KINDS = {"human"}


def blank(v) -> bool:
    return v is None or (isinstance(v, str) and (not v.strip() or "{{" in v)) or v == [] or v == {}


def check(root: Path) -> Report:
    report = Report()
    cfg = load_config(root)
    roles = cfg["roles"]
    optional = roles.get("optional_seats") or {}
    base_seats = roles.get("seats") or {}
    seats = {**optional, **base_seats}
    held_by = holder_index(roles)

    def kind(seat: str) -> str | None:
        return (seats.get(seat) or {}).get("kind")

    for a in load_artifacts(root, cfg["types"]):
        if a.meta.get("type") != "role-proposal" or a.status not in ("in-review", "approved"):
            continue
        m, rel = a.meta, a.rel

        def bad(msg: str) -> None:
            report.add("E17", rel, msg)

        proposed = m.get("proposed_seat")
        author = m.get("author_seat")
        if blank(proposed):
            bad("proposed_seat is missing")
            proposed = None
        elif proposed in base_seats:
            bad(f"proposed seat '{proposed}' already exists; change a charter through its own proposal, not as a new seat")

        charter = m.get("charter")
        if not isinstance(charter, dict):
            bad("charter is missing")
            charter = {}
        for key in ("trigger", "value"):
            if blank(charter.get(key)):
                bad(f"charter.{key} is missing")

        consumers: set[str] = set()
        senders: set[str] = set()
        inputs = charter.get("inputs")
        if not isinstance(inputs, list) or not inputs:
            bad("charter.inputs needs at least one input, each with the artifact and the seat it comes from")
        else:
            for i, item in enumerate(inputs, 1):
                item = item if isinstance(item, dict) else {}
                if blank(item.get("artifact")) or blank(item.get("from")):
                    bad(f"charter.inputs #{i} needs 'artifact' and 'from'")
                elif item["from"] == proposed:
                    bad(f"charter.inputs #{i} comes from the proposed seat itself; name the seat that supplies it")
                elif item["from"] not in seats:
                    bad(f"charter.inputs #{i} comes from '{item['from']}', which is not a seat")
                else:
                    senders.add(item["from"])

        outputs = charter.get("outputs")
        if not isinstance(outputs, list) or not outputs:
            bad("charter.outputs needs at least one output, each with the artifact and the seat that consumes it")
        else:
            for i, item in enumerate(outputs, 1):
                item = item if isinstance(item, dict) else {}
                if blank(item.get("artifact")) or blank(item.get("for")) or blank(item.get("acceptance")):
                    bad(f"charter.outputs #{i} needs 'artifact', 'for' and 'acceptance' (how the consumer tells it is good enough)")
                elif item["for"] == proposed:
                    bad(f"charter.outputs #{i} is for the proposed seat itself; work nobody else consumes has no demand")
                elif item["for"] not in seats:
                    bad(f"charter.outputs #{i} is for '{item['for']}', which is not a seat")
                else:
                    consumers.add(item["for"])

        for key in ("standards", "templates"):
            vals = charter.get(key)
            if not isinstance(vals, list) or not vals or any(blank(v) for v in vals):
                bad(f"charter.{key} needs at least one entry")
                continue
            for v in vals:
                if isinstance(v, str) and v.startswith("docs/") and not (root / v).exists():
                    bad(f"charter.{key}: '{v}' does not exist")

        ver = charter.get("verifier")
        ver = ver if isinstance(ver, dict) else {}
        vseat = ver.get("seat")
        if blank(vseat) or blank(ver.get("evidence")):
            bad("charter.verifier needs 'seat' and 'evidence' (what the verifier inspects to confirm the process is followed)")
        elif vseat not in seats:
            bad(f"charter.verifier '{vseat}' is not a seat")
        else:
            if vseat == author:
                bad("the verifier is the author; verification must be independent")
            if vseat == proposed:
                bad("the verifier is the proposed seat; it cannot verify itself")
            if held_by.get(vseat) and held_by.get(vseat) == held_by.get(author):
                bad(f"verifier '{vseat}' and author '{author}' share holder '{held_by[vseat]}'")

        peers = m.get("peer_review")
        if not isinstance(peers, list):
            bad("peer_review is missing")
            peers = []
        seen: set[str] = set()
        ranks: list[int] = []
        for i, p in enumerate(peers, 1):
            p = p if isinstance(p, dict) else {}
            seat = p.get("seat")
            if seat not in seats:
                bad(f"peer_review #{i}: '{seat}' is not a seat")
                continue
            if seat in seen:
                bad(f"peer_review #{i}: '{seat}' appears twice")
            seen.add(seat)
            if seat == author:
                bad(f"peer_review #{i}: the author cannot be a peer")
            if seat == proposed:
                bad(f"peer_review #{i}: the proposed seat cannot review itself")
            if kind(seat) in HUMAN_KINDS:
                bad(f"peer_review #{i}: '{seat}' is a human seat; humans approve, peers recommend")
            if held_by.get(seat) and held_by.get(seat) == held_by.get(author):
                bad(f"peer_review #{i}: '{seat}' shares holder '{held_by[seat]}' with the author")
            rec = p.get("recommendation")
            if rec not in RANK:
                bad(f"peer_review #{i}: recommendation must be one of {sorted(RANK)}")
            else:
                ranks.append(RANK[rec])
            if blank(p.get("demand")) or blank(p.get("evidence")):
                bad(f"peer_review #{i}: needs 'demand' (what this seat would hand over or take) and 'evidence'")
        if len(seen) < 2:
            bad("peer_review needs at least two distinct peers")
        for s in sorted(senders | consumers):
            if kind(s) == "agent" and s != proposed and s not in seen:
                bad(f"seat '{s}' sends input to or consumes output from the proposed seat but gave no peer review")

        group = m.get("peer_recommendation")
        if group not in RANK:
            bad(f"peer_recommendation must be one of {sorted(RANK)}")
        elif ranks and RANK[group] > min(ranks):
            bad("peer_recommendation is more favourable than its least favourable peer")
        if a.status == "approved" and group == "reject":
            bad("approved while the peer group recommends rejection")
    return report


if __name__ == "__main__":
    sys.exit(check(root_from_argv()).emit("E17 crew"))
