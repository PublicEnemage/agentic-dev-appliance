import check_caps
import check_registry
from conftest import messages

ENTRY = """
## RG-{n:03d} — Lint gate missing from a worktree
**Type:** {type}
**Date:** 2026-10-01
**What happened:** The pre-push hook used a relative path.
**What was at risk:** Unlinted code reaching the lane.
**What caught it:** Gate canary.
**Countermeasure:** Resolve paths from the repository root.
**Check:** {check}
"""


def add_entries(repo, *entries):
    path = repo.root / "docs/registry.md"
    path.write_text(path.read_text() + "".join(entries))


def test_caps_pass_on_template(repo):
    report = check_caps.check(repo.root)
    assert report.ok, messages(report)


def test_refuses_oversized_constitution(repo):
    (repo.root / "CLAUDE.md").write_text("x" * 20000 + "\nNo independent review is available at this governance stage.\n")
    assert "exceeds the 16000-byte budget" in messages(check_caps.check(repo.root))


def test_refuses_missing_single_principal_disclosure(repo):
    (repo.root / "CLAUDE.md").write_text("# Constitution\n")
    assert "single-principal disclosure is missing" in messages(check_caps.check(repo.root))


def test_refuses_state_file_over_cap(repo):
    (repo.root / "STATE.md").write_text("---\nactive_tracks: []\n---\n" + "line\n" * 250)
    assert "exceeds the 200-line cap" in messages(check_caps.check(repo.root))


def test_refuses_too_many_active_tracks(repo):
    (repo.root / "STATE.md").write_text("---\nactive_tracks: [a, b, c]\n---\n")
    assert "3 active tracks exceeds the cap of 2" in messages(check_caps.check(repo.root))


def test_registry_with_valid_entries_passes(repo):
    add_entries(repo, ENTRY.format(n=1, type="near-miss", check="E6"), ENTRY.format(n=2, type="external", check="workaround documented"))
    report = check_registry.check(repo.root)
    assert report.ok, messages(report)


def test_refuses_gap_in_registry_ids(repo):
    add_entries(repo, ENTRY.format(n=1, type="near-miss", check="E6"), ENTRY.format(n=3, type="near-miss", check="E6"))
    assert "expected RG-002" in messages(check_registry.check(repo.root))


def test_refuses_missing_registry_field(repo):
    add_entries(repo, ENTRY.format(n=1, type="near-miss", check="E6").replace("**What caught it:** Gate canary.\n", ""))
    assert "missing field 'What caught it'" in messages(check_registry.check(repo.root))


def test_refuses_near_miss_without_a_check(repo):
    add_entries(repo, ENTRY.format(n=1, type="near-miss", check="be more careful"))
    assert "must ship as a check" in messages(check_registry.check(repo.root))


def test_refuses_unbalanced_code_fence(repo):
    # The WorldSIM registry had NM-061 to NM-100 trapped inside an unclosed fence.
    add_entries(repo, "\n```markdown\n", ENTRY.format(n=1, type="near-miss", check="E6"))
    assert "unbalanced code fence" in messages(check_registry.check(repo.root))


def test_refuses_unknown_registry_type(repo):
    add_entries(repo, ENTRY.format(n=1, type="incident", check="E6"))
    assert "Type 'incident'" in messages(check_registry.check(repo.root))


def test_template_development_registry_is_well_formed():
    from conftest import REPO
    report = check_registry.check(REPO, "docs/method/registry.md")
    assert report.ok, messages(report)
