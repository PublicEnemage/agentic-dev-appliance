# Registry: development of the template itself

Near-misses found while building and testing the appliance template. Projects keep their
own registry in `docs/registry.md`; this file records the template's. Same format, checked
by E11 through the template's tests.

## RG-001 — Tests run by the pre-push hook committed into the real repository
**Type:** near-miss
**Date:** 2026-10-01
**What happened:** In dry run 1, the pre-push hook ran the template's tests. Git sets GIT_DIR and GIT_WORK_TREE while a hook runs. The E15 tests start their own git commands in scratch folders, but those commands inherited the variables and acted on the hooked repository instead. They added throwaway commits to the branch being pushed and set core.bare to true, so the clone stopped working as a working tree. Every test still reported a pass, and the polluted branch was pushed.
**What was at risk:** Silent corruption of any branch pushed with the hook installed, and a green test run that measured nothing, because its git commands hit the wrong repository.
**What caught it:** The observer of the dry run, checking the clone's state after the push. No check caught it.
**Countermeasure:** Every git command started by a check or a test runs with the redirecting GIT_* variables removed (tools/checks/lib.py clean_git_env). The hook also clears them before running anything, and refuses to run on a dirty working tree.
**Check:** tests/test_check_data.py::test_git_from_inside_a_hook_never_touches_the_hooked_repository, seen to fail without the countermeasure
