# Backlog

**Status:** decided and built 2026-10-05 (form, label, check E21). Part of [flow.md](flow.md).

The backlog is the list of work that needs attention and is not being done now. It is GitHub
issues with the label `backlog`, filed from the **Backlog item** form. Nothing else is a
backlog.

## Filing

Anyone with a seat, human or agent, files an item. A concern raised in conversation counts
as tracked only once it is an issue (constitution, session protocol step 3).

The form requires:

| Field | Says |
| --- | --- |
| Seat | The seat that should do it, or "unassigned" |
| Outcome | What is true when it is done. One outcome per issue |
| Acceptance | A checklist a reviewer can tick from the repository |
| Inputs | Repository paths to read, or "none" |
| Parent | The artifact id, issue or decision record it traces to, or "none" |

Split an item that has two outcomes. Two seats, two standards, or two reviewers are signs of
two items.

## Order

The Engineering Lead orders the backlog and decides what is picked next. Until a Projects
board exists, the order is the issue list sorted by the label and by milestone, and the
Engineering Lead names the next item in `STATE.md` under Next.

## Doing the work

1. The seat takes the item on a branch `seat/N-slug`, where N is the issue number.
2. The pull request description says `Closes #N`, and the acceptance checklist is ticked
   in the pull request, with a link to the evidence for each line.
3. The merge closes the issue. A human merge under the ruleset is the approval (flow.md,
   evidence rule).

An item that is escalated, because it needs a decision only a human can make, moves to the
[escalation path](escalation.md). The item stays open and says which escalation it waits on.

## Enforced and not

| Part | Status |
| --- | --- |
| Form exists, applies the label, requires every field | E21 |
| A pull request closes a filled-in item (task intake) | Not built. Designed in flow.md |
| Order, and an item that sits too long | Not built. The Steward counts items older than one cycle at each cycle exit |

## Open

- Whether items belong on a Projects board with a Cycle field once volume warrants it.
- Whether the Steward may close an item that is no longer wanted. Until decided, only the
  Engineering Lead closes without a merge, and says why in a comment.
