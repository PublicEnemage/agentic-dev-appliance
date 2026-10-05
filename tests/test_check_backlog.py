"""E21: the backlog process exists and says what it must."""

import pytest

import check_backlog
from conftest import messages


def test_the_real_form_passes(repo):
    report = check_backlog.check(repo.root)
    assert report.ok, messages(report)


def test_refuses_a_missing_form(repo):
    (repo.root / check_backlog.FORM).unlink()
    assert "backlog item form is missing" in messages(check_backlog.check(repo.root))


def test_refuses_a_form_without_the_label(repo):
    repo.edit_yaml(check_backlog.FORM, lambda d: d.update(labels=["enhancement"]))
    assert "does not apply the 'backlog' label" in messages(check_backlog.check(repo.root))


@pytest.mark.parametrize("field", check_backlog.REQUIRED)
def test_refuses_a_form_missing_a_field(repo, field):
    repo.edit_yaml(check_backlog.FORM, lambda d: d.update(body=[i for i in d["body"] if i.get("id") != field]))
    assert f"form has no '{field}' field" in messages(check_backlog.check(repo.root))


@pytest.mark.parametrize("field", check_backlog.REQUIRED)
def test_refuses_an_optional_field(repo, field):
    def relax(d):
        for i in d["body"]:
            if i.get("id") == field:
                i["validations"] = {"required": False}
    repo.edit_yaml(check_backlog.FORM, relax)
    assert f"field '{field}' is not required" in messages(check_backlog.check(repo.root))
