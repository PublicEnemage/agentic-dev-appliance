"""E19: the escalation path exists and says what it must.

Refuses when:
- the escalation issue form is missing, lacks the needs-human label, or lacks a required
  field (decider, trigger, seat, artifact, decision, options, parked work, consequence)
- appliance.yml has no escalation limits, or they are not whole days with the stalled limit
  above the respond limit
- the aging workflow is missing, has no schedule, does not run the aging tool or cannot
  write issues

The check sees that the path is built. Whether an escalation is well argued, and whether a
human answers it, is for the decider and the Steward.
"""

from __future__ import annotations

import sys
from pathlib import Path

from lib import Report, load_yaml, root_from_argv

FORM = ".github/ISSUE_TEMPLATE/escalation.yml"
WORKFLOW = ".github/workflows/escalation-aging.yml"
LABEL = "needs-human"
REQUIRED = ["decider", "trigger", "seat", "artifact", "decision", "options", "parked", "consequence"]


def check(root: Path) -> Report:
    report = Report()

    form = root / FORM
    if not form.is_file():
        report.add("E19", FORM, "escalation issue form is missing")
    else:
        data = load_yaml(form)
        if LABEL not in (data.get("labels") or []):
            report.add("E19", FORM, f"form does not apply the '{LABEL}' label")
        fields = {i.get("id"): i for i in (data.get("body") or []) if isinstance(i, dict)}
        for name in REQUIRED:
            item = fields.get(name)
            if item is None:
                report.add("E19", FORM, f"form has no '{name}' field")
            elif not (item.get("validations") or {}).get("required"):
                report.add("E19", FORM, f"field '{name}' is not required")

    app = load_yaml(root / "appliance.yml")
    esc = app.get("escalation")
    if not isinstance(esc, dict):
        report.add("E19", "appliance.yml", "no escalation limits; set respond_within_days and stalled_after_days")
    else:
        vals = {k: esc.get(k) for k in ("respond_within_days", "stalled_after_days")}
        for k, v in vals.items():
            if not isinstance(v, int) or isinstance(v, bool) or v < 1:
                report.add("E19", "appliance.yml", f"escalation.{k} must be a whole number of days, at least 1")
        if all(isinstance(v, int) and not isinstance(v, bool) for v in vals.values()) \
                and vals["stalled_after_days"] <= vals["respond_within_days"]:
            report.add("E19", "appliance.yml", "stalled_after_days must be greater than respond_within_days")

    wf = root / WORKFLOW
    if not wf.is_file():
        report.add("E19", WORKFLOW, "aging workflow is missing")
    else:
        data = load_yaml(wf)
        triggers = data.get("on") if "on" in data else data.get(True)
        if not isinstance(triggers, dict) or "schedule" not in triggers:
            report.add("E19", WORKFLOW, "aging workflow has no schedule")
        if "tools/escalations.py aging" not in wf.read_text(encoding="utf-8"):
            report.add("E19", WORKFLOW, "aging workflow does not run tools/escalations.py aging")
        if (data.get("permissions") or {}).get("issues") != "write":
            report.add("E19", WORKFLOW, "aging workflow cannot write issues; set permissions: issues: write")
    return report


if __name__ == "__main__":
    sys.exit(check(root_from_argv()).emit("E19 escalation"))
