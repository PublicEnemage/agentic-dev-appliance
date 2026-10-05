"""Escalation queue tools: the Engineering Lead's inbox and the aging job.

    python tools/escalations.py inbox [--root PATH] [--repo OWNER/NAME] [--issues-json FILE]
    python tools/escalations.py aging [--root PATH] [--repo OWNER/NAME] [--issues-json FILE]
                                      [--apply] [--now ISO]

The inbox lists what waits for a human: in-review artifacts whose type needs a human
approver (computed from the repository) and open issues labelled needs-human (from GitHub).
The aging job flags an escalation as overdue, then stalled, and says so once on the issue.
Without --apply it only prints what it would do. See docs/method/escalation.md.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "checks"))
from lib import load_artifacts, load_config, load_yaml  # noqa: E402

LABEL = "needs-human"
OVERDUE = "overdue"
STALLED = "stalled"
API = "https://api.github.com"
SECTION = re.compile(r"^### (.+?)[ \t]*\n\n(.*?)(?=\n### |\Z)", re.S | re.M)


def parse_body(body: str | None) -> dict[str, str]:
    """Read the fields of an issue form from the markdown GitHub renders: '### Label' then text."""
    return {m.group(1).strip(): m.group(2).strip() for m in SECTION.finditer(body or "")}


def parse_time(text: str) -> dt.datetime:
    return dt.datetime.fromisoformat(text.replace("Z", "+00:00"))


def age_days(created_at: str, now: dt.datetime) -> int:
    return max(0, (now - parse_time(created_at)).days)


def state(age: int, respond: int, stalled: int) -> str:
    if age > stalled:
        return STALLED
    if age > respond:
        return OVERDUE
    return "ok"


def limits(root: Path) -> tuple[int, int]:
    esc = load_yaml(root / "appliance.yml").get("escalation") or {}
    return int(esc.get("respond_within_days", 3)), int(esc.get("stalled_after_days", 7))


def open_escalations(issues: list[dict]) -> list[dict]:
    """Open issues carrying the label, never pull requests."""
    out = []
    for i in issues:
        names = {(l["name"] if isinstance(l, dict) else l) for l in i.get("labels", [])}
        if LABEL in names and i.get("state", "open") == "open" and "pull_request" not in i:
            out.append({**i, "label_names": names})
    return out


def plan_aging(issues: list[dict], now: dt.datetime, respond: int, stalled: int) -> list[dict]:
    """The labels and one comment each issue still needs. Re-running adds nothing twice."""
    plan = []
    for i in open_escalations(issues):
        a = age_days(i["created_at"], now)
        s = state(a, respond, stalled)
        if s == "ok":
            continue
        add = [n for n in ([OVERDUE] if s == OVERDUE else [OVERDUE, STALLED]) if n not in i["label_names"]]
        if not add:
            continue
        decider = parse_body(i.get("body")).get("Decider", "the decider")
        when = f"{respond} days" if s == OVERDUE else f"{stalled} days"
        plan.append({
            "number": i["number"], "state": s, "age": a, "labels": add,
            "comment": f"Waiting {a} days for {decider}, past the {when} limit. Answer here, then record the "
                       "decision in a repository file through a pull request that closes this issue. "
                       "Until then the parked work stays parked.",
        })
    return plan


def git_age(root: Path, rel: str, now: dt.datetime) -> int | None:
    try:
        out = subprocess.run(["git", "-C", str(root), "log", "-1", "--format=%cI", "--", rel],
                             capture_output=True, text=True, timeout=20).stdout.strip()
        return age_days(out, now) if out else None
    except (OSError, subprocess.SubprocessError, ValueError):
        return None


def approvals_queue(root: Path, now: dt.datetime) -> list[dict]:
    """In-review artifacts whose type needs a human approver."""
    cfg = load_config(root)
    types = cfg["types"].get("types", {})
    seats = {**(cfg["roles"].get("optional_seats") or {}), **(cfg["roles"].get("seats") or {})}
    rows = []
    for a in load_artifacts(root, cfg["types"]):
        if a.status != "in-review" or not types.get(a.meta.get("type"), {}).get("human_approver"):
            continue
        approvers = a.meta.get("approver")
        approvers = approvers if isinstance(approvers, list) else [approvers]
        humans = [x for x in approvers if (seats.get(x) or {}).get("kind") == "human"]
        rows.append({"id": a.id, "path": a.rel, "approver": ", ".join(humans) or "unnamed",
                     "age": git_age(root, a.rel, now)})
    return sorted(rows, key=lambda r: -(r["age"] or 0))


def render_inbox(approvals: list[dict], issues: list[dict], now: dt.datetime, respond: int, stalled: int) -> str:
    lines = [f"Approvals waiting: {len(approvals)}"]
    for r in approvals:
        age = "age unknown" if r["age"] is None else f"{r['age']} days"
        lines.append(f"  {r['id']}  {r['approver']}  {age}  {r['path']}")
    esc = open_escalations(issues)
    lines.append(f"Escalations waiting: {len(esc)}")
    for i in sorted(esc, key=lambda i: i["created_at"]):
        a = age_days(i["created_at"], now)
        decider = parse_body(i.get("body")).get("Decider", "unnamed")
        lines.append(f"  #{i['number']}  {decider}  {a} days  {state(a, respond, stalled)}  {i['title']}")
    return "\n".join(lines)


def request(method: str, url: str, token: str, payload: dict | None = None):
    req = urllib.request.Request(url, method=method, data=None if payload is None else json.dumps(payload).encode(),
                                 headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json",
                                          "Content-Type": "application/json", "User-Agent": "appliance-escalations"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read() or b"null")


def fetch_issues(repo: str, token: str) -> list[dict]:
    issues, page = [], 1
    while True:
        batch = request("GET", f"{API}/repos/{repo}/issues?labels={LABEL}&state=open&per_page=100&page={page}", token)
        issues += batch
        if len(batch) < 100:
            return issues
        page += 1


def default_repo(root: Path) -> str | None:
    if os.environ.get("GITHUB_REPOSITORY"):
        return os.environ["GITHUB_REPOSITORY"]
    url = subprocess.run(["git", "-C", str(root), "remote", "get-url", "origin"],
                         capture_output=True, text=True).stdout.strip()
    m = re.search(r"github\.com[:/](.+?)(?:\.git)?$", url)
    return m.group(1) if m else None


def option(argv: list[str], name: str) -> str | None:
    return argv[argv.index(name) + 1] if name in argv else None


def main(argv: list[str]) -> int:
    if not argv or argv[0] not in ("inbox", "aging"):
        print(__doc__)
        return 2
    cmd, rest = argv[0], argv[1:]
    root = Path(option(rest, "--root") or ".").resolve()
    now = parse_time(option(rest, "--now")) if option(rest, "--now") else dt.datetime.now(dt.timezone.utc)
    respond, stalled = limits(root)

    source = option(rest, "--issues-json")
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""
    repo = option(rest, "--repo") or default_repo(root)
    if source:
        issues = json.loads(Path(source).read_text())
    elif repo and token:
        issues = fetch_issues(repo, token)
    else:
        print("escalations: no issue source. Pass --issues-json, or --repo with GH_TOKEN set.", file=sys.stderr)
        return 2

    if cmd == "inbox":
        print(render_inbox(approvals_queue(root, now), issues, now, respond, stalled))
        return 0

    plan = plan_aging(issues, now, respond, stalled)
    for p in plan:
        print(f"#{p['number']} {p['state']} ({p['age']} days): add {', '.join(p['labels'])}")
    if "--apply" in rest:
        if source:
            print("escalations: --apply works on live issues only, not on --issues-json", file=sys.stderr)
            return 2
        if not (repo and token):
            print("escalations: --apply needs --repo and GH_TOKEN", file=sys.stderr)
            return 2
        for p in plan:
            request("POST", f"{API}/repos/{repo}/issues/{p['number']}/labels", token, {"labels": p["labels"]})
            request("POST", f"{API}/repos/{repo}/issues/{p['number']}/comments", token, {"body": p["comment"]})
    print(f"{len(plan)} escalation(s) flagged")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
