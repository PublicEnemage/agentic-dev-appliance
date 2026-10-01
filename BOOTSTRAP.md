# Bootstrap

How a new project starts from this template. Cycle 1 builds no product code. Cycle 1 is
setup, the smoke cycle and the discovery track.

Steps 1 to 3 and 6 are for the human. Steps 4, 5 and 8 are agent sessions, each in a
fresh session. Step 9 is shared.

The files on disk are the truth. If text placed in a session's context, such as a copy of
the constitution or notes about the person, differs from the files, the files win. The
session records the difference in its log and carries on.

## Steps

1. **Create the repository** from this template ("Use this template" on GitHub). Make it
   public, or use a plan that enforces rulesets on private repositories.
2. **Protect every lane.** Rulesets do not copy from the template. Add a ruleset on the
   default branch, and on every other long-lived branch pattern, that requires the
   `checks` job and a pull request, blocks force pushes and deletions, and has an empty
   bypass list. Until check E1 ships, agents push under the human's GitHub authorization:
   keep `single_principal: true` and the disclosure in `CLAUDE.md`.
3. **Name the human seats.** Tell the bootstrap session who holds the Intent Owner and
   Engineering Lead seats. The session writes the names; it never invents them.

4. **Bootstrap session.** The session holds the **Architect** seat.

   **Input manifest:** `CLAUDE.md`, `STATE.md`, this file, `appliance.yml`,
   `docs/roles.yml`, `docs/standards/data/`, `docs/dor/checklist.yml`,
   `docs/enforcement.yml`, `.github/CODEOWNERS`, and the product description the human
   gives. Read the floor (`docs/dor/floor.yml`) for context only; no floor row is
   expected to be met at bootstrap.

   The session:
   - copies the product description, as the human gave it, into `STATE.md` under
     "Product description". Later sessions cannot receive it any other way
   - fills the mission and principles in `CLAUDE.md`, marked as drafts for the Intent
     Owner to approve, and replaces the "Slots ... are filled at bootstrap" sentence
   - renames the human holder in `docs/roles.yml` to the person's name or handle
   - reads each seat's job description in `docs/roles.yml` against the product, and edits
     the ones the project changes. Every seat keeps one, and the check refuses a roster
     with a seat that has none
   - narrows each seat's `qualified_layers` to what its holder can judge. **Never adds a
     qualification to make a check pass.** If no seat can judge `domain-core` or a domain
     area, it leaves the list empty and records a crew review as the first open decision
     in `STATE.md`. No check fails at bootstrap for this; row C8 holds the case gate
     until a seat qualified for the domain exists
   - proposes a grade in `appliance.yml`. Standard is the default for anything with real
     users or their data. The business case confirms the grade later (floor row C6)
   - sets merge autonomy, and the contracts and migrations folders if the stack is known.
     If not, leaves the defaults and lists the choice as open
   - updates `.github/CODEOWNERS` with the right handles
   - adapts each draft data standard in `docs/standards/data/`, or marks it
     not-applicable in `docs/dor/checklist.yml` with a reason and `approver: Engineering Lead`.
     The checklist has one row, D11, for all five standards, so a standard is marked as a
     child row of D11 with its own rule:
     `D11.1: {rule: "STD-003 is not applicable because ...", status: not-applicable, reason: "...", approver: Engineering Lead}`.
     The Engineering Lead's merge in step 6 is the signature. Adapted standards stay
     `draft`; they are challenged and approved through the chain before the design gate
     (floor row D11). On each standard it edits, the session sets `author_seat: Architect`
     and `challenger_seat: Verifier`
   - records whether a Data Architect seat is needed now in `docs/standards/data/README.md`,
     against the triggers listed there
   - writes every question it would have asked a human into `STATE.md` under "Open
     decisions", with the assumption it made
   - runs the checks, commits on a `bootstrap` branch, and updates `STATE.md`

5. **Challenge the bootstrap.** A fresh session holding the **Verifier** seat reviews the
   bootstrap branch: everything changed since the template commit. It is asked to find
   what is wrong, missing or inconsistent, not to confirm.

   The template commit is the first commit of the repository
   (`git rev-list --max-parents=0 HEAD`), because a repository made from the template
   starts with one squashed commit.

   **Input manifest:** the same as step 4, plus `git diff` against the template commit,
   plus `docs/templates/review.md`. The product description is in `STATE.md`.

   The challenger writes its findings to `docs/bootstrap.review.md`, using the review
   template and its severity scale, and commits it to the `bootstrap` branch. The
   bootstrap has no artifact id, so this file is exempt from the review template's naming.
   It reviews against the constitution, `docs/roles.yml` (including each seat's job
   description, checked for gaps against the product), `appliance.yml`, the data
   standards and this file. It does not judge the draft standards' clauses in detail; their own
   challenge comes before the design gate.

   A fresh session holding the **Architect** seat then answers each finding in the Answer
   column: fixed, or declined with a reason. **Input manifest:** the review file, the
   files its findings name, and `docs/templates/review.md`. High findings must be fixed.
   A low finding may be deferred by recording it as an open decision in `STATE.md`, with
   a note in the Answer column. Write Yes in the Closed? column once a finding is answered.
   When every finding is answered and `open_findings` is 0, the branch is ready for
   step 6. If any high finding was fixed, a fresh Verifier session re-reads those fixes
   first and records its verdict in the review file.
6. **Approve.** The Engineering Lead reads the review, opens a pull request from
   `bootstrap`, and merges it. The merge approves the mission, principles, roles, grade
   proposal and any not-applicable rows.
7. **Install the hooks:** `git config core.hooksPath .githooks`. The setting applies to
   every worktree of the clone, which is intended. The hook refuses to run while the
   working tree has uncommitted or untracked changes, so a session keeps its notes outside
   the working tree or writes them at the end.
8. **Smoke cycle.** A fresh session, on a throwaway branch cut from the merged `main`,
   breaks each check on purpose and confirms it refuses, one item at a time:
   Each item is run on its own, with the one check it targets, and with a passing control
   first. For E10 and SEATS, make the artifact from a root type such as `role-proposal`
   (its template needs no parents), so the break fails for one reason only.

   - an artifact in the wrong folder, and one outside every artifact folder (E10)
   - an artifact whose author seat is also its approver seat (SEATS)
   - a deleted floor row in `docs/dor/checklist.yml` (DOR)
   - a test with an early return (E3)
   - a registry entry with a gap in its IDs (E11)
   - a contract file with no consumers (E14)
   - an edit to a migration already committed on the base: commit a migration, edit it,
     commit the edit, then run `python3 tools/checks/check_migrations.py --base <the
     migration's commit>`. An uncommitted edit passes by design (E15)
   - an architecture artifact in review with no data-model diagram (E16)
   - a role proposal in review whose verifier is its author, and a seat in
     `docs/roles.yml` with its job description removed (E17)
   - the pre-push hook, run directly, with one breaking change committed, such as a
     deleted floor row. The hook stops at its first failing command, so the tests do not
     run in the refused case

   The session writes the results to `docs/archive/smoke-<date>.md`, then discards the
   breaking changes. The results file goes to `main` through a small pull request, and
   `STATE.md` links to it. The throwaway branch is deleted.
9. **Discovery track.** Write the intent and business case with the Intent Owner, then
   users, use cases, NFRs and the risk assessment. Start with the open decisions in
   `STATE.md`. Run `python3 tools/checks/check_dor.py --gate case` until the case gate passes.

Delivery starts once the case and design gates pass and there is baselined work to pull.

## Checks

```
pip install -r tools/checks/requirements.txt
python3 tools/checks/run_all.py              # every implemented check
python3 tools/checks/run_all.py --gate case  # also require the case gate rows
python3 -m pytest -q tests                   # the checks' own tests
```

The checks' tests use fixed defaults in `tests/fixtures/defaults/`, so a project's own
roles, settings and constitution never break them. What each check enforces, and what is
still advisory, is in `docs/enforcement.yml`.
