"""The pre-push hook must check what is being pushed. It refuses to run with uncommitted
or untracked changes, because the checks read the working tree (dry run 1, smoke note 6)."""

import shutil
import subprocess

from conftest import REPO
from lib import clean_git_env


def run(cwd, *args):
    return subprocess.run(list(args), cwd=cwd, capture_output=True, text=True, env=clean_git_env())


def test_hook_refuses_a_dirty_working_tree(tmp_path):
    (tmp_path / ".githooks").mkdir()
    shutil.copy(REPO / ".githooks/pre-push", tmp_path / ".githooks/pre-push")
    run(tmp_path, "git", "init", "-q", "-b", "main")
    run(tmp_path, "git", "-c", "user.name=t", "-c", "user.email=t@t", "add", "-A")
    run(tmp_path, "git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "base")
    (tmp_path / "stray.txt").write_text("not committed")
    result = run(tmp_path, "bash", ".githooks/pre-push")
    assert result.returncode == 1
    assert "uncommitted or untracked changes present" in result.stderr
