# Near-miss registry: development of the template itself

Near-misses found while building and testing the appliance template. A project keeps its
own in `docs/near-miss-registry.md`. Same format, checked by E11 through the template's
tests. IDs run on without gaps. Where a countermeasure is not yet a check, the Check field
says which check is planned, and the entry stays open until it ships.

## RG-001 — Tests run by the pre-push hook committed into the real repository
**Type:** near-miss
**Date:** 2026-10-01
**What happened:** In dry run 1, the pre-push hook ran the template's tests. Git sets GIT_DIR and GIT_WORK_TREE while a hook runs. The E15 tests start their own git commands in scratch folders, but those commands inherited the variables and acted on the hooked repository instead. They added throwaway commits to the branch being pushed and set core.bare to true, so the clone stopped working as a working tree. Every test still reported a pass, and the polluted branch was pushed.
**What was at risk:** Silent corruption of any branch pushed with the hook installed, and a green test run that measured nothing, because its git commands hit the wrong repository.
**What caught it:** The observer of the dry run, checking the clone's state after the push. No check caught it.
**Countermeasure:** Every git command started by a check or a test runs with the redirecting GIT_* variables removed (tools/checks/lib.py clean_git_env). The hook also clears them before running anything, and refuses to run on a dirty working tree.
**Check:** tests/test_check_data.py::test_git_from_inside_a_hook_never_touches_the_hooked_repository, seen to fail without the countermeasure

## RG-002 — Dry run 2's first attempt was contaminated by injected context
**Type:** near-miss
**Date:** 2026-10-01
**What happened:** The first bootstrap attempt in dry run 2 ran with project instruction files and notes about the person from other work in its context. It answered from them, so its results measured the leaked context and not the template. The attempt was discarded and redone.
**What was at risk:** A method result that looked like evidence and was not. The template's questions-per-bootstrap measure would have been wrong.
**What caught it:** The observer, comparing the session's answers with what its inputs contained.
**Countermeasure:** The bootstrap says the files on disk win over injected context. Dry run 3 isolates each session in its own fresh clone and starts every session by logging the instruction files and notes in its context.
**Check:** Planned: the review-independence check (RG-003). Until then, the context log written in each session's first action

## RG-003 — Dry run 3 review branches were chained, so six of eight sessions were not independent
**Type:** near-miss
**Date:** 2026-10-01
**What happened:** The review prompts did not say which branch to cut from. Later sessions cut from earlier review branches, so their working trees held other seats' reviews. Four reviews cite another review by gap number. Only the Product and Builder sessions are clean.
**What was at risk:** Peer agreement counted as independent evidence when most of it was one session plus readers, and the 'also raised by' columns overstated convergence.
**What caught it:** The observer, reading git ancestry after the Steward's compile reported one leak.
**Countermeasure:** The run protocol names the base branch each session cuts from and requires one fresh clone per session. A check refuses a review branch that holds another seat's review in its ancestry.
**Check:** Planned: review-independence check (docs/roadmap.md, next build). Not built

## RG-004 — The Steward's compile misreported its own leak log and rating counts
**Type:** near-miss
**Date:** 2026-10-01
**What happened:** The compile of the eight reviews named one confirmed leak and one unclear, and said 'no evidence' for five sessions. Four of those cited another review by name, and git ancestry explained the rest. Its rating notes miscounted four seats.
**What was at risk:** A confident, wrong summary, read as the compiled finding, would have steered which job-description changes the Engineering Lead approved.
**What caught it:** The observer, recounting the matrix and reading branch histories.
**Countermeasure:** Counts and the leak log come from a script over git and the review files, never from a session's own reading. The compile's prompt asks for evidence, and the script supplies it.
**Check:** Planned: compile-by-script (docs/method/dryrun-3.md, 'What this changes' 3). Not built

## RG-005 — Seat review prompts carried no input manifest, and one carried the wrong branch
**Type:** near-miss
**Date:** 2026-10-01
**What happened:** CLAUDE.md tells every session to read its task manifest. The seat review prompt supplied none, and all eight sessions reported it. The Delivery prompt still named the Product branch, so Delivery wrote beside Product's review.
**What was at risk:** Sessions reading what they chose, and a review written with another seat's work in the tree.
**What caught it:** The sessions' own reports, then the human on the Delivery prompt.
**Countermeasure:** The run protocol states the base branch, the manifest and the isolation for every session. Task issues carry the manifest and base branch as required fields, and a PR must reference such an issue.
**Check:** Planned: task intake check (docs/method/flow.md). Not built

## RG-006 — The role-proposal template said the Steward may author, and SEATS refuses it
**Type:** near-miss
**Date:** 2026-10-05
**What happened:** The template read 'Any seat or the Steward may author'. SEATS refuses the Steward in every artifact field. A proposal drafted from the template would have failed its own check.
**What was at risk:** A template that teaches an authoring path the checks reject, found only when a proposal reached CI.
**What caught it:** The author of the first proposal (RP-001), reading the SEATS check while drafting.
**Countermeasure:** The template now says any agent seat may author, but not one the charter names, and that the Steward compiles. A template whose guidance contradicts a check is a gap in the check's tests.
**Check:** Planned: a test that each template's authoring guidance agrees with SEATS. Not built

## RG-007 — An existing seat had no path to change its job description
**Type:** near-miss
**Date:** 2026-10-05
**What happened:** E17 refused an in-review proposal for a seat that already exists and told the author to use a proposal. The Engineering Lead's job said every roles-file change carries an approved proposal. Both could not hold, and a proposal could never reach peer review.
**What was at risk:** Roster changes made by merge alone, with no peer review, or by routing around the check.
**What caught it:** The observer, tracing why the Architect's change of layers had no path.
**Countermeasure:** A change to an existing seat is a proposal with change_of and change_kind. A substantive change takes the full peer review. A wiring-only change takes one peer and the seat on the other end of each changed line.
**Check:** tools/checks/check_crew.py (E17), tests/test_check_crew.py

## RG-008 — A test run of the aging tool wrote to a live repository
**Type:** near-miss
**Date:** 2026-10-05
**What happened:** Testing the escalation aging tool on sample data with --apply, with a real token in the environment, added two labels and a comment to a merged pull request in the live repository.
**What was at risk:** Noise and false state on real work items, and a tool whose test run is an action.
**What caught it:** The observer, reading the tool's exit code and checking the repository afterwards.
**Countermeasure:** The tool refuses --apply when the issues come from a file. A test fails if the apply path ever calls the GitHub API with file data.
**Check:** tests/test_escalations_tool.py::test_apply_refuses_to_run_on_a_file_so_a_test_never_writes_to_a_live_repo
