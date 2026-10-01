# Dry run 2: bootstrap from the fixed template

**Date:** 2026-10-01. **Repository:** [PublicEnemage/appliance-dryrun-2](https://github.com/PublicEnemage/appliance-dryrun-2).
**Template commit:** `7a3b62f` (v0.1 plus the dry run 1 fixes, PR #5).
**Product:** Shelf, the same invented neighbourhood tool-lending web app as run 1.

Purpose: show whether the 19 method questions from [dryrun-1.md](dryrun-1.md) drop when a
cold session starts from the fixed template. The product questions (11 in run 1) should not
drop, because only the Intent Owner can answer them.

## Product description given to the bootstrap session

Run 1's paragraph was not saved. This is a reconstruction from the Shelf mission that run 1
produced, so the inputs match in substance, not word for word:

> Shelf is a web app for a neighbourhood tool-lending library. Members list the tools they
> will lend, borrow from each other, and return on time with reminders. A volunteer
> coordinator sees at a glance what is out and what is overdue.

Human seats: PublicEnemage holds Intent Owner and Engineering Lead. No human is available to
answer questions during the run.

## Predictions

Written before any session starts.

| Measure | Predicted |
| --- | --- |
| Method questions logged by the bootstrap session | 4 to 8, down from 19 |
| Product questions logged | 8 to 12, about the same as run 1 |
| Checks failing after the bootstrap session | 1 expected: C8 or a seat check, if the session leaves domain-core unqualified as the rule now says |
| Challenge findings | 8 to 14, with 0 to 2 high, down from 22 with 4 high |
| Grade chosen | standard |
| Qualification declared to pass a check | none |
| Smoke cycle refusals | all 9 items refuse, E15 with an explicit base commit |
| Agent time to a challenged setup | under 15 minutes |

## What would count as a template failure

- Any high finding that repeats a run 1 high finding.
- A method question the template now claims to answer.
- A smoke item that cannot be run from the text of BOOTSTRAP.md alone.

## Results

To be filled after the run.
