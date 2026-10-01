# Constitution

Every session reads this file first, human or agent. The file holds only the rules no
machine can enforce yet. A rule that a check enforces lives in the check (design rule 8).
Budget: 16,000 bytes, enforced by check E9.

Slots in `{{double braces}}` are filled at bootstrap. See `BOOTSTRAP.md`.

## Mission

{{One or two sentences: what this product exists to do, and for whom.}}

## Principles

{{Three to five project principles. Each is a value that decides trade-offs, not a slogan.}}

## Seats

| Seat | Held by |
| --- | --- |
| Intent Owner | {{name}} |
| Engineering Lead | {{name}} |

Agent seats, their charters and holders are in `docs/roles.yml`. The Steward holds no
artifact seat. On any artifact, the author, challenger and approver are three different
seats on three different holders. Check SEATS refuses anything else.

## Session protocol

1. Read, in order: this file, `STATE.md`, and the input manifest of your task.
   Read nothing else unless the manifest names it.
2. Work only in your own worktree and branch. Never use `git stash`. Never check out
   a branch in a tree another session is using.
3. Treat conversation as disposable. A decision counts only once it is written to a
   named artifact in the repository.
4. Before ending a session: commit your work to your branch, update `STATE.md`, and
   say what is left. A session that ends mid-task leaves a note in `STATE.md`.

Steps 2 and 4 become harness hooks in v0.2 (check E7). Until then they are advisory.

## The chain

Every unit of work traces back through approved artifacts to the business case.

- Artifact types, folders and naming: `docs/artifact-types.yml`
- Templates: `docs/templates/`
- Definition of Ready floor: `docs/dor/floor.yml`; this project's answers: `docs/dor/checklist.yml`
- Enforcement status of every check: `docs/enforcement.yml`

Duties on every artifact:

- **Consulted** seats give independent input cold, before the author drafts.
- **Author** writes from named upstream artifacts and the consulted input, nothing else.
- **Challenger** is a different seat in a fresh session. Findings go in the review file
  beside the artifact and are answered item by item.
- **Approver** accepts for the concern the artifact serves. Business artifacts need a human.
- **Consumer** is the next stage. If it must ask what the artifact should have said,
  the artifact goes back.

## Rules no check enforces yet

These are advisory until their check ships. Each names the check that will replace it.

- Tests for an increment land on a test-only PR before implementation, and are seen red
  in CI per test. (E2, v0.3)
- A gate that has not been seen to refuse is not trusted. Run the smoke cycle after any
  change to CI or branch rules. (E6, v0.3)
- Every test ID used in a test exists in the component contract file. (E4, v0.2)
- Exit counts come from CI, not from a summary. (E8, v0.2)
- Validation runs on an environment built from CI definitions. (E12, v0.2)

## Rules that stay with judgment

- Consult before framing. Choose the consulted seats by the problem's likely root cause,
  not its surface.
- The countermeasure to a near-miss is never "be more careful". It is a redesign that
  ships as a check. File every near-miss in `docs/registry.md`.
- Where a diagram and its text disagree, the diagram governs structure. Raise the gap as
  a challenge finding (floor row D13).
- A gap that no seat can judge opens a crew review (`docs/templates/role-proposal.md`).
  Prefer a rule or a tool to a new role.
- Prescribe outcomes and gates, not steps. Rules live in standing documents and job
  descriptions; a prompt names the outcome. When an agent errs, fix the standing document
  or the check, never the prompt.
- Never declare a qualification, a seat or an approval to make a check pass. A failing
  check that tells the truth is worth more than a passing one that does not.

## Governance

Autonomy for merges is set in `appliance.yml`. Agents work on branches and open pull
requests. Agents never push to `main`.

<!-- single-principal disclosure: keep while appliance.yml has single_principal: true -->
**Single-principal disclosure.** The Intent Owner and Engineering Lead seats are held by
one person, and agent work is pushed under that person's GitHub authorization until check E1
ships. This exception was approved by the same individual who holds full repository
authority. No independent review is available at this governance stage. Approvals in
front matter are declared, not bound to identities.
