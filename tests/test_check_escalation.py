"""E19: the escalation path exists and says what it must."""

import pytest
import yaml

import check_escalation
from conftest import messages


def test_the_real_path_passes(repo):
    report = check_escalation.check(repo.root)
    assert report.ok, messages(report)


def test_refuses_a_missing_form(repo):
    (repo.root / check_escalation.FORM).unlink()
    assert "escalation issue form is missing" in messages(check_escalation.check(repo.root))


def test_refuses_a_form_without_the_label(repo):
    repo.edit_yaml(check_escalation.FORM, lambda d: d.update(labels=["bug"]))
    assert "does not apply the 'needs-human' label" in messages(check_escalation.check(repo.root))


@pytest.mark.parametrize("field", check_escalation.REQUIRED)
def test_refuses_a_form_missing_a_field(repo, field):
    repo.edit_yaml(check_escalation.FORM, lambda d: d.update(body=[i for i in d["body"] if i.get("id") != field]))
    assert f"form has no '{field}' field" in messages(check_escalation.check(repo.root))


def test_refuses_an_optional_field(repo):
    def relax(d):
        for i in d["body"]:
            if i.get("id") == "options":
                i["validations"] = {"required": False}
    repo.edit_yaml(check_escalation.FORM, relax)
    assert "field 'options' is not required" in messages(check_escalation.check(repo.root))


def test_refuses_missing_limits(repo):
    repo.edit_yaml("appliance.yml", lambda d: d.pop("escalation"))
    assert "no escalation limits" in messages(check_escalation.check(repo.root))


@pytest.mark.parametrize("respond,stalled,expected", [
    (0, 7, "must be a whole number of days"),
    ("3", 7, "must be a whole number of days"),
    (7, 3, "stalled_after_days must be greater"),
    (3, 3, "stalled_after_days must be greater"),
])
def test_refuses_bad_limits(repo, respond, stalled, expected):
    repo.edit_yaml("appliance.yml", lambda d: d.update(escalation={"respond_within_days": respond, "stalled_after_days": stalled}))
    assert expected in messages(check_escalation.check(repo.root))


def test_refuses_a_missing_workflow(repo):
    (repo.root / check_escalation.WORKFLOW).unlink()
    assert "aging workflow is missing" in messages(check_escalation.check(repo.root))


def test_refuses_an_unscheduled_workflow(repo):
    repo.edit_yaml(check_escalation.WORKFLOW, lambda d: d.update({True: {"workflow_dispatch": None}}) if True in d else d.update(on={"workflow_dispatch": None}))
    assert "aging workflow has no schedule" in messages(check_escalation.check(repo.root))


def test_refuses_a_workflow_that_cannot_write_issues(repo):
    repo.edit_yaml(check_escalation.WORKFLOW, lambda d: d.update(permissions={"contents": "read"}))
    assert "cannot write issues" in messages(check_escalation.check(repo.root))


def test_refuses_a_workflow_that_does_not_run_the_tool(repo):
    p = repo.root / check_escalation.WORKFLOW
    p.write_text(p.read_text().replace("tools/escalations.py aging", "echo skipped"))
    assert "does not run tools/escalations.py aging" in messages(check_escalation.check(repo.root))
