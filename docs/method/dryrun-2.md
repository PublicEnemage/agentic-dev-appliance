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

Raw records in the dry-run repository:
[bootstrap PR](https://github.com/PublicEnemage/appliance-dryrun-2/pull/1) with
`DRYRUN-QUESTIONS.md`, `DRYRUN-QUESTIONS-CHALLENGER.md` and `docs/bootstrap.review.md`;
[smoke PR](https://github.com/PublicEnemage/appliance-dryrun-2/pull/2) with
`docs/archive/smoke-2026-10-01.md` and `DRYRUN-QUESTIONS-SMOKE.md`.

| Measure | Predicted | Run 1 | Run 2 |
| --- | --- | --- | --- |
| Method questions, bootstrap session | 4 to 8 | 19 | 7 |
| Product questions, bootstrap session | 8 to 12 | 11 | 7 |
| Checks failing after bootstrap | 1 | 0 | 0 |
| Challenge findings | 8 to 14, 0 to 2 high | 22, 4 high | 15, 0 high (8 medium, 7 low) |
| Grade chosen | standard | light | standard |
| Qualification declared to pass a check | none | one | none; `domain-core` left empty and a crew review listed first |
| Smoke refusals | all 9 items | all 8 | all, E15 only once the edit is committed |

The method questions fell from 19 to 7 and the high findings from 4 to 0. The two
repeats of the run 1 failures (a light grade, a qualification declared to pass a check)
did not recur. The check count miss is mine: I predicted one failing check, but no check
fails when `domain-core` is left empty. BOOTSTRAP.md had told the session to expect one;
that sentence is corrected.

## Validity: the run was not fully cold

The first attempt's bootstrap session had the filled-in run 1 constitution in its
context. This session's own context reached every agent it started, and it cannot be
stripped from inside it. After the leaking clones were moved aside, the second attempt
still wrote the same four principles as run 1, with light rewording. Four of the five sessions reported other projects' constitutions and the person's memory
notes in their context; the smoke session did not say.

What this affects: the product choices (principles, assumptions) are not independent
evidence. The method counts, the findings and the smoke results come from the procedure
and the checks, and are usable. A clean product-side test needs a session started
directly in the new repository, not by an observer.

Attempt 1 (discarded, 14 method and 8 product questions) is kept out of the repository.
Both attempts had leaked context, so the leak does not separate them. The drop from 14 to
7 between them shows how much one run varies, and the fall from run 1's 19 should be read
as a direction, not a measured size.

## What the run found

| Gap | Disposition |
| --- | --- |
| Step 4 manifest omitted `docs/dor/checklist.yml` and `docs/enforcement.yml` | Added |
| Not-applicable row shape was only in `check_dor.py`; one D11 row covers five standards | BOOTSTRAP.md shows a child-row example |
| Product description reached the challenger by no route | Bootstrap copies it into `STATE.md`; new section in the template |
| Template commit not named for the diff | First commit of the repository |
| Review file name conflicted with the review template | Exemption stated in both |
| Answering session had no seat, manifest or re-check; Closed? undefined | Architect seat, manifest, Verifier re-read after high fixes, Closed? defined |
| "Let the check fail" for `domain-core` described a failure that does not happen | Reworded |
| Injected context disagreed with files on disk | Files win; difference logged |
| Smoke item wording: uncommitted E15 edit passes; artifact types unnamed; hook refuses untracked log files | Reworded in step 8 and step 7 |
| Checks do not verify that bootstrap happened | Roadmap: bootstrap-complete check |

## Left open

- Whether a seat's charter alone qualifies it for a layer, or a holder's evidence is
  needed. The answering session picked a rule for Shelf. This is a design decision for the
  Intent Owner, and binding qualifications to evidence waits for E1.
- Retrying with a session started directly in a new repository, to test the product side.
