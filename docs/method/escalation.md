# Escalation to a human seat

**Status:** decided and built 2026-10-05 (form, aging job, inbox, check E19). The closure
check is designed and not built. Part of [flow.md](flow.md).

An escalation is a decision only a human seat can make, raised so the work around it can
carry on. The single-principal setup makes one person the decider for both human seats, so
the queue has to be short, dated and visible. Seven of the dry run 3 sessions raised the
blocked-human gap. This is the answer to it.

## When to escalate

| Trigger | Raised by | Decided by |
| --- | --- | --- |
| A second rejection of one artifact (design rule 3 of the input contract) | The seat that rejected it | The approver of the artifact |
| A gap no seat can judge (opens a crew review) | Any seat | Engineering Lead |
| An exception request (`exceptions.md`) | The seat that needs it | Engineering Lead, with the Intent Owner consulted when the waived item traces to intent |
| Blocked past its limit | The seat that is blocked | The seat that holds the blocking decision, or the Engineering Lead |
| A validation or release gate | Product or Operator | Intent Owner |
| Anything else only a human can decide | Any seat | The form's Decider field |

When not to escalate: a rule, a check or a standard already decides it. A concern without a
clause is a challenge finding, answered in the review file. Escalating is for choices, not
for questions a document answers.

## The shape of an escalation

A GitHub issue from the **Escalation** form. The form applies the label `needs-human` and
requires: Decider, Trigger, Seat raising it, Artifact or task, Decision needed, Options and
recommendation, Work parked meanwhile, Consequence of delay.

- **One decision per issue.** Stated so a yes or a choice answers it.
- **A recommendation is required.** The raising seat says which option it would take and why.
  The decider spends attention on a choice, not on analysis.
- **Decider** is the Engineering Lead or the Intent Owner. Business intent and scope go to the
  Intent Owner. Engineering and governance go to the Engineering Lead. While one person
  holds both seats the queue is one list. The field keeps it splittable.

## What the raising session does

1. Opens the issue.
2. Parks the work that depends on the decision and lists it under **Open decisions** in
   `STATE.md`, with the issue number.
3. Carries on with work that does not depend on the answer.
4. Never approves in a human's place, and never treats silence as a yes.

## Waiting

The limits are in `appliance.yml`, in calendar days, and the grade sets the suggestion
(light 7 and 14, standard 3 and 7, assured 1 and 3).

- Past `respond_within_days`, the scheduled job adds the label `overdue` and one comment.
- Past `stalled_after_days`, it adds `stalled` and one comment.
- The Steward counts overdue and stalled escalations at each cycle exit. A rising count is a
  finding about the process, not about the person.
- The job adds each label once. Running it twice changes nothing.

## Answering

The decider answers in the issue. A comment is not the decision, because anyone with write
access can edit it. The decision counts once it is in a repository file:

- a merged pull request that closes the issue (`Closes #N`) and changes the file the
  decision lives in: the artifact or its review file, `STATE.md`, an ADR or the registry;
- the escalation issue closes with that merge.

**Not built:** a check that refuses to close a `needs-human` issue unless a merged pull
request that changed a repository file closed it. Until then the Steward looks for it.

## What the human sees

`python tools/escalations.py inbox` lists, oldest first:

- **Approvals waiting:** every in-review artifact whose type needs a human approver,
  computed from the repository, with its age from git. No issue is needed for these.
- **Escalations waiting:** open `needs-human` issues, with decider, age and state.

A GitHub Projects view over the same label gives the same list in the browser.

## Setup

Create the labels `needs-human`, `overdue` and `stalled` in the repository once. The issue
form applies `needs-human` only if the label exists. The scheduled workflow
`.github/workflows/escalation-aging.yml` runs daily and needs no secret beyond the default
token.

## Enforced and not

| Part | Status |
| --- | --- |
| Form exists, has the label and every required field | E19 |
| Limits are set, in whole days, stalled above respond | E19 |
| Aging workflow is scheduled, runs the tool, can write issues | E19 |
| Parked work recorded in `STATE.md` | Review. E7 hooks later |
| Closure through a merged pull request | Not built |
| Human answers in time | Nothing can enforce this. The queue makes the wait visible |

## Open

- Whether a stalled escalation should block new increments for the work it parks. It
  does not now. The build licence design suspends new increments on a lapsed review, and
  stalled escalations could feed the same measure.
- A deputy for the Engineering Lead seat before real users arrive (decision 7).
