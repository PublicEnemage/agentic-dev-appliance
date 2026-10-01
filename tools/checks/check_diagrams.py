"""E16: required diagrams, as Mermaid code inside the artifact (floor row D13).

Text can be read several ways; an entity relationship or a flow can be read one way.
Each artifact type lists the diagrams it must carry in docs/artifact-types.yml. Once an
artifact is in review or approved, this check refuses when:
- a required diagram is missing and not declared not-applicable with a reason and approver
- a tagged diagram uses an unknown tag, or the wrong Mermaid form for its tag
  (for example, a data model that is not an erDiagram)
- a diagram is too thin to mean anything: fewer nodes, entities or participants than the
  tag's minimum, or no edges, relationships, messages or transitions at all

Drafts are exempt. The check sees presence and shape, not correctness: whether the
diagram matches the text and the code is the challenger's call.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from lib import Report, load_artifacts, load_config, root_from_argv

TAG = re.compile(r"^\s*<!--\s*diagram:\s*([a-z0-9-]+)\s*-->\s*$")
FENCE_OPEN = re.compile(r"^\s*```\s*mermaid\s*$")
FENCE_CLOSE = re.compile(r"^\s*```\s*$")
SKIP_WORDS = {"subgraph", "end", "classDef", "class", "style", "linkStyle", "click", "direction"}
FLOW_ARROW = re.compile(r"\s*(?:--\s+[^-|>]+?\s+-->|<?-{2,}>?|<?={2,}>?|<?-\.+->?|~~~)\s*(?:\|[^|]*\|\s*)?")
ER_REL = re.compile(r"^\s*([\w-]+)\s+[|}][|o](?:--|\.\.)[|o][|{]\s+([\w-]+)")
ER_BLOCK = re.compile(r"^\s*([\w-]+)\s*\{")
SEQ_PART = re.compile(r"^\s*(?:participant|actor)\s+(\w+)")
SEQ_MSG = re.compile(r"^\s*(\w+)\s*-{1,2}(?:>>|>|x|\))[+-]?\s*(\w+)\s*:")
STATE_EDGE = re.compile(r"^\s*(\[\*\]|[\w-]+)\s*-->\s*(\[\*\]|[\w-]+)")
NODE_ID = re.compile(r"^([A-Za-z_][\w-]*)")


def extract(body: str) -> list[tuple[str | None, list[str]]]:
    """Return (tag, lines) for every Mermaid block. The tag is on the nearest
    non-blank line above the opening fence, if that line is a diagram comment."""
    lines = body.splitlines()
    out = []
    i = 0
    while i < len(lines):
        if FENCE_OPEN.match(lines[i]):
            tag = None
            j = i - 1
            while j >= 0 and not lines[j].strip():
                j -= 1
            if j >= 0:
                m = TAG.match(lines[j])
                tag = m.group(1) if m else None
            k = i + 1
            block = []
            while k < len(lines) and not FENCE_CLOSE.match(lines[k]):
                block.append(lines[k])
                k += 1
            out.append((tag, block))
            i = k + 1
        else:
            i += 1
    return out


def content(block: list[str]) -> list[str]:
    return [ln for ln in block if ln.strip() and not ln.strip().startswith("%%")]


def form_of(block: list[str], forms: dict) -> str | None:
    lines = content(block)
    if not lines:
        return None
    head = lines[0].split()[0]
    for form, keywords in forms.items():
        if head in keywords:
            return form
    return None


def measure(form: str, block: list[str]) -> tuple[int, int]:
    """Return (things, links): nodes and edges, entities and relationships,
    participants and messages, or states and transitions."""
    lines = content(block)[1:]
    things: set[str] = set()
    links = 0
    for ln in lines:
        s = ln.strip()
        if form == "flowchart":
            if s.split()[0] in SKIP_WORDS:
                continue
            parts = [p for p in FLOW_ARROW.split(s) if p.strip()]
            if len(parts) > 1:
                links += len(parts) - 1
            for p in parts:
                m = NODE_ID.match(p.strip())
                if m:
                    things.add(m.group(1))
        elif form == "er":
            m = ER_REL.match(s)
            if m:
                links += 1
                things.update([m.group(1), m.group(2)])
            else:
                b = ER_BLOCK.match(s)
                if b:
                    things.add(b.group(1))
        elif form == "sequence":
            p = SEQ_PART.match(s)
            if p:
                things.add(p.group(1))
            m = SEQ_MSG.match(s)
            if m:
                links += 1
                things.update([m.group(1), m.group(2)])
        elif form == "state":
            m = STATE_EDGE.match(s)
            if m:
                links += 1
                things.update(x for x in (m.group(1), m.group(2)) if x != "[*]")
    return len(things), links


def diagram_problems(body: str, required: list[str], declared: dict, types_cfg: dict) -> list[str]:
    """Problems for one artifact body. Shared with the template test."""
    forms = types_cfg["diagram_forms"]
    tags = types_cfg["diagram_tags"]
    problems = []
    found: dict[str, int] = {}
    for tag, block in extract(body):
        if tag is None:
            continue
        if tag not in tags:
            problems.append(f"unknown diagram tag '{tag}'; tags are {sorted(tags)}")
            continue
        want = tags[tag]["form"]
        got = form_of(block, forms)
        if got != want:
            problems.append(f"diagram '{tag}' must be a {want} diagram ({', '.join(forms[want])}), found {got or 'nothing'}")
            continue
        n, links = measure(want, block)
        if n < tags[tag]["min"] or links == 0:
            problems.append(f"diagram '{tag}' is too thin: {n} parts and {links} links; it needs at least {tags[tag]['min']} parts and one link")
            continue
        found[tag] = found.get(tag, 0) + 1
    for tag in required:
        if tag in found:
            continue
        entry = declared.get(tag) if isinstance(declared, dict) else None
        if isinstance(entry, dict) and entry.get("not_applicable"):
            if not entry.get("approver"):
                problems.append(f"diagram '{tag}' is not-applicable without an approver")
            continue
        problems.append(f"missing required diagram '{tag}' ({tags[tag]['shows']})")
    return problems


def check(root: Path) -> Report:
    report = Report()
    cfg = load_config(root)
    types_cfg = cfg["types"]
    required = types_cfg.get("required_diagrams") or {}
    for a in load_artifacts(root, types_cfg):
        if a.status not in ("in-review", "approved"):
            continue
        t = a.meta.get("type")
        body_has_tags = "diagram:" in a.body
        if t not in required and not body_has_tags:
            continue
        for p in diagram_problems(a.body, required.get(t, []), a.meta.get("diagrams") or {}, types_cfg):
            report.add("E16", a.rel, p)
    return report


if __name__ == "__main__":
    sys.exit(check(root_from_argv()).emit("E16 diagrams"))
