"""E17: every seat has a job description, and a new seat's proposal survives peer review.

The job description is a seat's charter in front matter, so a check can read it:
trigger, inputs with their senders, value, outputs with their consumers and an acceptance
test, standards, templates, and an independent verifier with the evidence it inspects.

Refuses when:
- any seat in docs/roles.yml, core or optional, human or agent, has no complete job
  description
- a role proposal in review or approved has an incomplete charter (same rules)
- an input comes from, or an output goes to, a seat that does not exist or is the seat itself
- a standard or template under docs/ does not exist
- the verifier is the seat itself, or on the same holder as the seat (for a proposal: the
  author or the author's holder)
- a proposal's peer review has fewer than two peers, a peer who is the author, the
  proposed seat or a human seat, a peer without a recommendation, demand statement and
  evidence, or leaves out an agent seat that sends the new seat input or consumes its output
- the peer group's recommendation is more favourable than its least favourable member
- a proposal is approved while the peer group recommends rejection, or without a matching
  job description in docs/roles.yml

The check sees completeness and independence. Whether a job description is sound, and
whether evidence is real, is for the peers, the challenger and the Engineering Lead.
"""

from __future__ import annotations

import sys
from pathlib import Path

from lib import Report, load_artifacts, load_config, root_from_argv
from check_seats import holder_index

RANK = {"reject": 0, "accept-with-conditions": 1, "accept": 2}
ROSTER = "docs/roles.yml"


def blank(v) -> bool:
    return v is None or (isinstance(v, str) and (not v.strip() or "{{" in v)) or v == [] or v == {}


def job_problems(job, *, label: str, subject: str | None, seats: dict, held_by: dict,
                 root: Path, author: str | None = None) -> tuple[list[str], set[str], set[str]]:
    """Problems with one job description, plus the seats that send it input and consume
    its output. `subject` is the seat the job describes. `author` is set for a proposal."""
    out: list[str] = []
    senders: set[str] = set()
    consumers: set[str] = set()
    if not isinstance(job, dict):
        return [f"{label} is missing"], senders, consumers
    for key in ("trigger", "value"):
        if blank(job.get(key)):
            out.append(f"{label}.{key} is missing")

    inputs = job.get("inputs")
    if not isinstance(inputs, list) or not inputs:
        out.append(f"{label}.inputs needs at least one input, each with the artifact and the seat it comes from")
    else:
        for i, item in enumerate(inputs, 1):
            item = item if isinstance(item, dict) else {}
            if blank(item.get("artifact")) or blank(item.get("from")):
                out.append(f"{label}.inputs #{i} needs 'artifact' and 'from'")
            elif item["from"] == subject:
                out.append(f"{label}.inputs #{i} comes from the seat itself; name the seat that supplies it")
            elif item["from"] not in seats:
                out.append(f"{label}.inputs #{i} comes from '{item['from']}', which is not a seat")
            else:
                senders.add(item["from"])

    outputs = job.get("outputs")
    if not isinstance(outputs, list) or not outputs:
        out.append(f"{label}.outputs needs at least one output, each with the artifact and the seat that consumes it")
    else:
        for i, item in enumerate(outputs, 1):
            item = item if isinstance(item, dict) else {}
            if blank(item.get("artifact")) or blank(item.get("for")) or blank(item.get("acceptance")):
                out.append(f"{label}.outputs #{i} needs 'artifact', 'for' and 'acceptance' (how the consumer tells it is good enough)")
            elif item["for"] == subject:
                out.append(f"{label}.outputs #{i} is for the seat itself; work nobody else consumes has no demand")
            elif item["for"] not in seats:
                out.append(f"{label}.outputs #{i} is for '{item['for']}', which is not a seat")
            else:
                consumers.add(item["for"])

    for key in ("standards", "templates"):
        vals = job.get(key)
        if not isinstance(vals, list) or not vals or any(blank(v) for v in vals):
            out.append(f"{label}.{key} needs at least one entry")
            continue
        for v in vals:
            if isinstance(v, str) and v.startswith("docs/") and not (root / v).exists():
                out.append(f"{label}.{key}: '{v}' does not exist")

    ver = job.get("verifier")
    ver = ver if isinstance(ver, dict) else {}
    vseat = ver.get("seat")
    if blank(vseat) or blank(ver.get("evidence")):
        out.append(f"{label}.verifier needs 'seat' and 'evidence' (what the verifier inspects to confirm the process is followed)")
    elif vseat not in seats:
        out.append(f"{label}.verifier '{vseat}' is not a seat")
    else:
        if vseat == subject:
            out.append(f"{label}.verifier is the seat itself; it cannot verify itself")
        if author is not None:
            if vseat == author:
                out.append("the verifier is the author; verification must be independent")
            ref = author
        else:
            ref = subject
        if ref and held_by.get(vseat) and held_by.get(vseat) == held_by.get(ref):
            out.append(f"verifier '{vseat}' and '{ref}' share holder '{held_by[vseat]}'")
    return out, senders, consumers


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

    # Every seat on the roster has a job description.
    for name, spec in seats.items():
        problems, _, _ = job_problems((spec or {}).get("job"), label=f"seat '{name}' job",
                                      subject=name, seats=seats, held_by=held_by, root=root)
        for p in problems:
            report.add("E17", ROSTER, p)

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
        elif a.status == "in-review" and proposed in base_seats:
            bad(f"proposed seat '{proposed}' already exists; change a job description through its own proposal, not as a new seat")

        charter = m.get("charter")
        problems, senders, consumers = job_problems(charter, label="charter", subject=proposed,
                                                    seats=seats, held_by=held_by, root=root, author=author)
        for p in problems:
            bad(p)

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
            if kind(seat) == "human":
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
        if a.status == "approved":
            if group == "reject":
                bad("approved while the peer group recommends rejection")
            if proposed:
                adopted = (seats.get(proposed) or {}).get("job")
                if proposed not in seats:
                    bad(f"approved, but seat '{proposed}' is not in {ROSTER}; the approved job description belongs there")
                elif adopted != charter:
                    bad(f"approved charter differs from the job description of '{proposed}' in {ROSTER}")
    return report


if __name__ == "__main__":
    sys.exit(check(root_from_argv()).emit("E17 crew"))
