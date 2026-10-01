import check_artifacts
from conftest import messages


def chain(repo):
    """A minimal valid chain: an intent and a business case that traces to it."""
    repo.artifact("intent", 1, "first-intent")
    repo.artifact("business-case", 1, "first-case", parents=["INTENT-001"],
                  challenger_seat="Verifier", approved_at="2026-10-02T10:00:00")


def test_valid_chain_passes(repo):
    chain(repo)
    report = check_artifacts.check(repo.root)
    assert report.ok, messages(report)


def test_empty_repository_passes(repo):
    assert check_artifacts.check(repo.root).ok


def test_refuses_missing_front_matter(repo):
    repo.write("docs/case/CASE-001-no-front-matter.md", "Just prose.\n")
    assert "missing or invalid front matter" in messages(check_artifacts.check(repo.root))


def test_refuses_missing_required_field(repo):
    repo.artifact("intent", 1, author_seat=None)
    assert "missing required field 'author_seat'" in messages(check_artifacts.check(repo.root))


def test_refuses_wrong_folder(repo):
    repo.artifact("adr", 1, parents=[], folder="docs/case")
    assert "belongs in docs/adr/" in messages(check_artifacts.check(repo.root))


def test_refuses_bad_file_name(repo):
    repo.write("docs/case/intent-one.md", "---\nid: INTENT-001\ntype: intent\n---\n")
    assert "file name must be" in messages(check_artifacts.check(repo.root))


def test_refuses_id_that_differs_from_file_name(repo):
    repo.artifact("intent", 1, id="INTENT-002")
    assert "does not match file name" in messages(check_artifacts.check(repo.root))


def test_refuses_duplicate_id(repo):
    repo.artifact("intent", 1, "one")
    repo.artifact("intent", 1, "two")
    assert "duplicate id" in messages(check_artifacts.check(repo.root))


def test_refuses_missing_parent(repo):
    repo.artifact("business-case", 1, parents=["INTENT-009"], challenger_seat="Verifier")
    assert "parent 'INTENT-009' does not exist" in messages(check_artifacts.check(repo.root))


def test_refuses_orphan_non_root_artifact(repo):
    repo.artifact("business-case", 1, parents=[], challenger_seat="Verifier")
    assert "needs at least one parent" in messages(check_artifacts.check(repo.root))


def test_refuses_dead_reference_in_body(repo):
    repo.artifact("intent", 1, body="See ADR-007 for the storage choice.\n")
    assert "references 'ADR-007'" in messages(check_artifacts.check(repo.root))


def test_refuses_approval_before_parent_is_approved(repo):
    repo.artifact("intent", 1, status="draft")
    repo.artifact("business-case", 1, parents=["INTENT-001"], challenger_seat="Verifier")
    assert "approved before parent 'INTENT-001' is approved" in messages(check_artifacts.check(repo.root))


def test_refuses_stale_child_after_parent_reapproval(repo):
    repo.artifact("intent", 1, approved_at="2026-10-05T09:00:00")
    repo.artifact("business-case", 1, parents=["INTENT-001"], challenger_seat="Verifier",
                  approved_at="2026-10-02T10:00:00")
    assert "stale" in messages(check_artifacts.check(repo.root))


def test_refuses_approval_without_review_file(repo):
    repo.artifact("intent", 1, review=False)
    assert "approved without a review file" in messages(check_artifacts.check(repo.root))


def test_refuses_approval_with_open_findings(repo):
    repo.artifact("intent", 1, review={"open_findings": 2})
    assert "open_findings must be 0" in messages(check_artifacts.check(repo.root))


def test_refuses_review_by_a_different_challenger(repo):
    repo.artifact("intent", 1, review={"challenger_seat": "Builder"})
    assert "challenger_seat differs" in messages(check_artifacts.check(repo.root))


def test_refuses_unknown_status(repo):
    repo.artifact("intent", 1, status="done")
    assert "status 'done'" in messages(check_artifacts.check(repo.root))


def test_refuses_artifact_saved_outside_the_artifact_folders(repo):
    # Dry run 1: an intent saved under docs/misc/ was ignored and passed.
    repo.artifact("intent", 1, folder="docs/misc")
    assert "sits outside the artifact folders; it belongs in docs/case/" in messages(check_artifacts.check(repo.root))
