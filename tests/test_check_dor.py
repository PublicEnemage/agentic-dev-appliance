import check_dor
from conftest import messages


def set_row(repo, rid, entry):
    repo.edit_yaml("docs/dor/checklist.yml", lambda c: c["rows"].update({rid: entry}))


def test_template_checklist_passes_structure(repo):
    report = check_dor.check(repo.root)
    assert report.ok, messages(report)


def test_refuses_deleted_floor_row(repo):
    repo.edit_yaml("docs/dor/checklist.yml", lambda c: c["rows"].pop("D6"))
    assert "floor row D6 is missing" in messages(check_dor.check(repo.root))


def test_refuses_weakened_floor_rule(repo):
    set_row(repo, "C2", {"status": "open", "rule": "Business case exists"})
    assert "floor rule text is fixed" in messages(check_dor.check(repo.root))


def test_refuses_coarser_project_row(repo):
    set_row(repo, "X1", {"status": "open", "rule": "Something extra"})
    assert "must be children of a floor row" in messages(check_dor.check(repo.root))


def test_finer_child_row_passes(repo):
    set_row(repo, "D2.1", {"status": "open", "rule": "Data section names the system of record"})
    assert check_dor.check(repo.root).ok


def test_refuses_blank_row(repo):
    set_row(repo, "C3", {})
    assert "C3: blank row" in messages(check_dor.check(repo.root))


def test_refuses_met_without_evidence(repo):
    set_row(repo, "C1", {"status": "met"})
    assert "C1: met without evidence" in messages(check_dor.check(repo.root))


def test_refuses_evidence_that_does_not_exist(repo):
    set_row(repo, "C1", {"status": "met", "evidence": ["INTENT-004"]})
    assert "'INTENT-004' is not an artifact id" in messages(check_dor.check(repo.root))


def test_refuses_not_applicable_without_reason_or_approver(repo):
    set_row(repo, "D4", {"status": "not-applicable"})
    out = messages(check_dor.check(repo.root))
    assert "D4: not-applicable needs a reason" in out
    assert "D4: not-applicable needs an approver" in out


def test_refuses_met_parent_with_open_child(repo):
    repo.artifact("intent", 1)
    set_row(repo, "C1", {"status": "met", "evidence": ["INTENT-001"]})
    set_row(repo, "C1.1", {"status": "open", "rule": "Intent names the buyer"})
    assert "C1: met while child C1.1 is open" in messages(check_dor.check(repo.root))


def test_refuses_floor_version_drift(repo):
    repo.edit_yaml("docs/dor/checklist.yml", lambda c: c.update({"floor_version": "0.0.9"}))
    assert "differs from appliance.yml" in messages(check_dor.check(repo.root))


def test_gate_blocks_while_case_rows_are_open(repo):
    assert "gate 'case' blocked: C1 is open" in messages(check_dor.check(repo.root, "case"))


def test_gate_blocks_on_unapproved_evidence(repo):
    repo.artifact("intent", 1, status="draft")
    set_row(repo, "C1", {"status": "met", "evidence": ["INTENT-001"]})
    assert "cites INTENT-001, which is draft" in messages(check_dor.check(repo.root, "case"))


def test_case_gate_passes_when_every_case_row_is_answered(repo):
    repo.artifact("intent", 1)
    def answer(c):
        for rid in ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9"]:
            c["rows"][rid] = {"status": "met", "evidence": ["INTENT-001"]}
    repo.edit_yaml("docs/dor/checklist.yml", answer)
    report = check_dor.check(repo.root, "case")
    assert report.ok, messages(report)


def test_refuses_approved_increment_intent_that_skips_increment_rows(repo):
    repo.artifact("intent", 1)
    repo.artifact("increment-intent", 1, parents=["INTENT-001"], challenger_seat="Verifier",
                  dor={"I1": {"status": "met", "evidence": ["INTENT-001"]}})
    out = messages(check_dor.check(repo.root))
    assert "I2: approved increment intent does not answer this row" in out
    assert "I7: approved increment intent does not answer this row" in out


def test_every_floor_row_names_registered_checks():
    import yaml
    from conftest import REPO
    floor = yaml.safe_load((REPO / "docs/dor/floor.yml").read_text())
    registered = set(yaml.safe_load((REPO / "docs/enforcement.yml").read_text())["checks"])
    unknown = {(r["id"], c) for r in floor["rows"] for c in r["enforced_by"] if c not in registered}
    assert not unknown, sorted(unknown)
