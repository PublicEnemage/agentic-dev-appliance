"""E20: a file name says what the file is for."""

import pytest

import check_file_names
from conftest import messages


def test_the_real_repo_passes(repo):
    report = check_file_names.check(repo.root)
    assert report.ok, messages(report)


@pytest.mark.parametrize("name", [
    "docs/registry.md", "docs/notes.md", "docs/method/misc.md", "docs/final.md",
    "docs/new-notes.md", "docs/old_draft.yml", ".github/data.yml", "TODO.md", "docs/crew/RP-009-draft.md",
])
def test_refuses_a_generic_name(repo, name):
    path = repo.root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("x\n")
    assert "generic file name" in messages(check_file_names.check(repo.root))


@pytest.mark.parametrize("name", [
    "docs/near-miss-registry.md", "docs/crew/RP-009-frontend-architect.md", "docs/method/flow.md",
    "README.md",
])
def test_accepts_a_descriptive_name(repo, name):
    path = repo.root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("x\n")
    assert check_file_names.check(repo.root).ok


@pytest.mark.parametrize("name", ["tools/notes.md", "tests/data.yml", "docs/notes.json"])
def test_ignores_code_folders_and_other_suffixes(repo, name):
    path = repo.root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("x\n")
    assert check_file_names.check(repo.root).ok
