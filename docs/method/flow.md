# Flow management: GitHub-native

**Status:** decided 2026-10-05 by the Engineering Lead. The escalation path is built
(`escalation.md`). The other checks below are designed and not built.

## Decision

Use GitHub for dispatch, tracking, views and queues, as far as the platform goes. The
appliance accepts the platform lock-in. The gain is attention on outcomes, not on
integrations between tools or on portability. There is no tracker adapter. The template
names GitHub features directly.

Domain-agnostic still holds for the product domain. The appliance runs any kind of product.
It runs it on GitHub.

## What counts as evidence

GitHub holds two kinds of fact, and a gate trusts only one.

- **Evidence:** repo files, and facts GitHub enforces itself: a merge by a human under a
  protected-branch rule, a required review, an environment approval, a CI result, and the
  event timestamps of all of these.
- **Not evidence:** free text anyone with write access can edit silently. That covers issue
  and PR bodies, comments and board positions. They dispatch and show the work. A gate does
  not rely on them.

The repo stays the record for approvals, statuses and test evidence. Design rule 9 holds.

## Object map

| Need | GitHub feature | Rule |
| --- | --- | --- |
| Epic, story, task | Issues linked as sub-issues, with a `level:` label | A task is one seat and one session. Issue types need an organization, so labels carry the level on a personal account |
| Dispatch a task | Issue form per seat and task type | Fields: seat, outcome, base branch, input manifest as repo paths, parent artifact id, acceptance |
| Do the work | Pull request on branch `seat/N-slug` | The PR closes the issue. A session prompt is "take issue N" |
| Report the result | PR description in a fixed shape, plus a comment on the issue | Done, evidence links, what is left, questions. A squash merge copies the PR text into git history |
| See the work | Projects board with fields Seat, Track, Status, Cycle, Size | Columns Ready, In progress, In review, Blocked, Validated. Done means validated, not closed. Actions move the cards from events and nobody drags them |
| Cap WIP | Board view by Track | The cap is `track_cap` in `appliance.yml` |
| Backlog | Issue form with label `backlog` | Built. See [backlog.md](backlog.md). Fields: seat, outcome, acceptance, inputs, parent |
| Escalate | Issue form with label `needs-human` and a Decider field | Built. See [escalation.md](escalation.md). Fields: decider, trigger, seat, artifact, decision, options with a recommendation, work parked, consequence of delay |
| Approve | CODEOWNERS and a branch ruleset | A human merge approves. Check E1 will bind the identity |
| Release | Environment with a required reviewer | The release decision. The post-deploy check (E13) runs as an Actions job |
| Measure | Actions job over git, issue and PR timestamps | Delivery owns the metrics and the Steward recomputes them |
| Chase | Scheduled Action | Flags escalations and approvals past their age limit |
| Notify | GitHub notifications and mobile | For the human seats |
| Trace | Commit trailer `Claude-Session` to the session, PR to issue to story to use case to business case | A check walks the chain |

## Queues for the human seats

- **Approvals queue.** Computed from the repo: every in-review artifact whose type needs a
  human approver. No issue is created for it.
- **Escalations.** Issues with the `needs-human` label. Triggers: a second rejection of an
  artifact, a gap no seat can judge, an exception request, a blocked item past its limit,
  and the validation and release gates.
- **One inbox** (`python tools/escalations.py inbox`) shows both. The Decider field splits
  the queue between the Engineering Lead and the Intent Owner when a second person exists.
- **While a human is unreachable**, sessions park the work and record it in `STATE.md`.
  Agents never approve for a human (decision 7).

## Checks to build

Names, not ids. Ids are assigned when each is built.

1. **Task intake.** A PR references an issue whose form fields are filled in and whose
   manifest paths exist. The form is built as the backlog item (E21), see
   [backlog.md](backlog.md). The PR-to-issue check is not.
2. **Summary shape.** The PR description has the four parts.
3. **Escalation aging.** Built as E19 and `tools/escalations.py`. See
   [escalation.md](escalation.md).
4. **Board sync.** Actions set Status from events and refuse a hand-moved card.
5. **Metrics.** A script computes the delivery metrics from git and GitHub timestamps.
6. **Chain walk.** Every PR traces to the business case through approved artifacts.

For the pilot, build 1 to 3 first. The board can wait until there is volume.

## Accepted risks and limits

- **Platform dependence.** An outage or a policy change stops the flow. Accepted.
- **Plan level.** Some features, such as rulesets and environment reviewers on private
  repositories, depend on the GitHub plan. Check the pilot repository's plan before relying
  on one.
- **Agent access.** Sessions reach issues through the API with a token. Until E1 binds
  identity, agent actions run under the human's authorization (single-principal disclosure).
- **Volume.** One issue per task creates many issues. The board filters by track and cycle.

## Open

- The pilot repository's plan, and which features it allows.
- Who authors task issues. Proposed: Delivery for planned tasks, and any seat for an
  escalation.
- Whether a cycle is a GitHub milestone or a Projects iteration.
