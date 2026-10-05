"""The inbox and the aging job."""

import datetime as dt

import escalations

NOW = dt.datetime(2026, 10, 10, 12, 0, tzinfo=dt.timezone.utc)
BODY = "### Decider\n\nEngineering Lead\n\n### Trigger\n\nA gap no seat can judge\n\n### Decision needed\n\nWhich layer?\n"


def issue(n, days, labels=("needs-human",), **over):
    created = (NOW - dt.timedelta(days=days)).isoformat().replace("+00:00", "Z")
    base = {"number": n, "title": f"Escalation {n}", "body": BODY, "created_at": created, "state": "open",
            "labels": [{"name": x} for x in labels]}
    base.update(over)
    return base


def test_parses_the_issue_form_body():
    f = escalations.parse_body(BODY)
    assert f["Decider"] == "Engineering Lead"
    assert f["Decision needed"] == "Which layer?"


def test_a_fresh_escalation_is_left_alone():
    assert escalations.plan_aging([issue(1, 2)], NOW, 3, 7) == []


def test_flags_overdue_after_the_respond_limit():
    plan = escalations.plan_aging([issue(1, 4)], NOW, 3, 7)
    assert [(p["number"], p["state"], p["labels"]) for p in plan] == [(1, "overdue", ["overdue"])]
    assert "Engineering Lead" in plan[0]["comment"]


def test_flags_stalled_after_the_stalled_limit():
    plan = escalations.plan_aging([issue(1, 9)], NOW, 3, 7)
    assert plan[0]["state"] == "stalled" and plan[0]["labels"] == ["overdue", "stalled"]


def test_the_limit_day_itself_is_not_late():
    assert escalations.plan_aging([issue(1, 3), issue(2, 7, labels=("needs-human", "overdue"))], NOW, 3, 7) == []


def test_running_twice_adds_nothing_twice():
    flagged = issue(1, 9, labels=("needs-human", "overdue", "stalled"))
    assert escalations.plan_aging([flagged], NOW, 3, 7) == []


def test_a_stalled_issue_already_overdue_only_gains_stalled():
    plan = escalations.plan_aging([issue(1, 9, labels=("needs-human", "overdue"))], NOW, 3, 7)
    assert plan[0]["labels"] == ["stalled"]


def test_ignores_closed_issues_pull_requests_and_other_labels():
    items = [issue(1, 9, state="closed"), issue(2, 9, pull_request={}), issue(3, 9, labels=("bug",))]
    assert escalations.plan_aging(items, NOW, 3, 7) == []


def test_inbox_lists_in_review_artifacts_that_need_a_human(repo):
    repo.artifact("architecture", 1, status="in-review", approver="Engineering Lead", review=False)
    repo.artifact("story", 1, status="in-review", approver="Engineering Lead", review=False)  # no human needed
    repo.artifact("business-case", 1, status="approved")
    rows = escalations.approvals_queue(repo.root, NOW)
    assert [r["id"] for r in rows] == ["ARCH-001"]
    assert rows[0]["approver"] == "Engineering Lead"


def test_inbox_shows_escalations_oldest_first_with_their_state(repo):
    out = escalations.render_inbox([], [issue(2, 5), issue(1, 9)], NOW, 3, 7)
    lines = [l for l in out.splitlines() if l.startswith("  #")]
    assert lines[0].startswith("  #1") and "stalled" in lines[0]
    assert "overdue" in lines[1]


def test_limits_come_from_appliance_yml(repo):
    assert escalations.limits(repo.root) == (3, 7)
    repo.edit_yaml("appliance.yml", lambda d: d.update(escalation={"respond_within_days": 1, "stalled_after_days": 3}))
    assert escalations.limits(repo.root) == (1, 3)


def test_apply_refuses_to_run_on_a_file_so_a_test_never_writes_to_a_live_repo(repo, tmp_path, monkeypatch, capsys):
    import json
    src = tmp_path / "issues.json"
    src.write_text(json.dumps([issue(1, 9)]))
    monkeypatch.setenv("GH_TOKEN", "token-that-must-never-be-used")
    monkeypatch.setattr(escalations, "request", lambda *a, **k: (_ for _ in ()).throw(AssertionError("wrote to GitHub")))
    code = escalations.main(["aging", "--root", str(repo.root), "--issues-json", str(src), "--apply", "--now", NOW.isoformat()])
    assert code == 2
    assert "live issues only" in capsys.readouterr().err
