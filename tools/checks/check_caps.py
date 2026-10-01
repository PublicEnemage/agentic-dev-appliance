"""E9: stated caps.

Refuses when:
- CLAUDE.md exceeds the constitution byte budget
- STATE.md exceeds the line cap, or has no front matter
- STATE.md lists more active delivery tracks than the track cap
- single_principal is true but CLAUDE.md lacks the single-principal disclosure

Shared-state lane checks arrive with E7 (v0.2).
"""

from __future__ import annotations

import sys
from pathlib import Path

from lib import Report, as_list, load_yaml, read_front_matter, root_from_argv

DISCLOSURE = "No independent review is available at this governance stage."


def check(root: Path) -> Report:
    report = Report()
    app = load_yaml(root / "appliance.yml")
    caps = app.get("caps") or {}

    constitution = root / "CLAUDE.md"
    if not constitution.is_file():
        report.add("E9", "CLAUDE.md", "constitution is missing")
    else:
        size = len(constitution.read_bytes())
        budget = int(caps.get("constitution_bytes", 16000))
        if size > budget:
            report.add("E9", "CLAUDE.md", f"{size} bytes exceeds the {budget}-byte budget; move enforced rules into checks")
        if app.get("single_principal") and DISCLOSURE not in constitution.read_text(encoding="utf-8"):
            report.add("E9", "CLAUDE.md", "single_principal is true but the single-principal disclosure is missing")

    state = root / "STATE.md"
    if not state.is_file():
        report.add("E9", "STATE.md", "state file is missing")
    else:
        lines = state.read_text(encoding="utf-8").count("\n") + 1
        cap = int(caps.get("state_lines", 200))
        if lines > cap:
            report.add("E9", "STATE.md", f"{lines} lines exceeds the {cap}-line cap; archive to docs/archive/")
        meta, _ = read_front_matter(state)
        if meta is None:
            report.add("E9", "STATE.md", "missing front matter")
        else:
            tracks = as_list(meta.get("active_tracks"))
            track_cap = int(caps.get("track_cap", 2))
            if len(tracks) > track_cap:
                report.add("E9", "STATE.md", f"{len(tracks)} active tracks exceeds the cap of {track_cap}")
    return report


if __name__ == "__main__":
    sys.exit(check(root_from_argv()).emit("E9 caps"))
