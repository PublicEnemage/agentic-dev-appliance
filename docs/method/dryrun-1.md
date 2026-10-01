# Dry run 1: bootstrap of a new project from the template

**Date:** 2026-10-01. **Repository:** [PublicEnemage/appliance-dryrun](https://github.com/PublicEnemage/appliance-dryrun).
**Product:** Shelf, an invented neighbourhood tool-lending web app.

Three fresh agent sessions ran BOOTSTRAP.md steps 4, 5, 7 and 8 against the v0.2 template,
with no briefing beyond the repository and a one-paragraph product description. Steps 1 to
3 and 6 were the human's. An observer session, the template's author, recorded results and
did not intervene.

Raw records in the dry-run repository:
- [DRYRUN-QUESTIONS.md](https://github.com/PublicEnemage/appliance-dryrun/blob/bootstrap/DRYRUN-QUESTIONS.md): 30 questions logged by the bootstrap session
- [BOOTSTRAP.review.md](https://github.com/PublicEnemage/appliance-dryrun/blob/bootstrap/BOOTSTRAP.review.md): 22 challenge findings
- [SMOKE-RESULTS.md](https://github.com/PublicEnemage/appliance-dryrun/blob/smoke/SMOKE-RESULTS.md): smoke cycle results

## Predictions against actuals

Predictions were written before the run.

| Measure | Predicted | Actual |
| --- | --- | --- |
| Questions the cold session needed answered | 3 to 6 | 30: 11 product decisions only the Intent Owner can make, 19 gaps in the method |
| Checks failing after the bootstrap session | at least 1 | 0, but the session shaped its choices to keep the template's tests passing |
| Challenge findings | not predicted | 22: 4 high, 12 medium, 6 low |
| Smoke cycle refusals | all checks | all 8 refused; E15 only with an explicit base |
| GitHub side | CI runs; rulesets do not copy | both confirmed |
| Agent time to a challenged setup | under 1 hour | about 10 minutes |

The largest miss was the question count. Most of the 19 method gaps sat in BOOTSTRAP.md
itself: no seat or input manifest for the bootstrap session, no home for the challenge,
no rule on who answers findings, and a step that said to record results and then discard
the branch holding them.

## What the run found

| Finding | Severity | Disposition |
| --- | --- | --- |
| Tests run by the pre-push hook committed into the real repository and broke the clone (RG-001) | high | Fixed: git variables cleared in checks, tests and hook; test seen to fail without the fix; registry entry RG-001 in [registry.md](registry.md) |
| The template's tests read the project's own roles and settings, so honest bootstrap choices broke them, which biased the choices (Q11) | high | Fixed: tests use fixed defaults in `tests/fixtures/defaults/`; the checklist is generated from the floor |
| A domain qualification was declared to make check C8 pass, and domain-core went to seats without domain knowledge | high | Judgment rule added to the constitution and roles file: never declare a qualification to pass a check. Binding declarations to evidence waits for E1 |
| The light grade was chosen for a product with real users' data, against the method's own grade table | high | Default is now standard; appliance.yml says when light applies, and that the business case confirms the grade |
| Data standards credited seats that did not write them | high | BOOTSTRAP.md now gives the bootstrap session the Architect seat and says to set it on each standard edited |
| Bootstrap had no seat, no input manifest, and no named challenger seat (Q1, Q2) | medium | BOOTSTRAP.md: Architect authors, Verifier challenges, each with a manifest |
| No home for the bootstrap challenge, no severity scale, no rule on answering findings | medium | Review goes to `docs/bootstrap.review.md`; the review template defines severity and what blocks approval; the author answers each finding |
| Step 8 said to record results, then discard the branch holding them | medium | Results go to `docs/archive/smoke-<date>.md` through their own pull request |
| The pre-push hook checks the working tree, not what is being pushed | medium | Hook refuses to run with uncommitted or untracked changes; test added |
| An artifact saved outside every artifact folder was ignored by E10 | medium | E10 now finds files with artifact front matter anywhere in the repository; test added |
| E15 could not be smoked as written | medium | Step 8 shows how, using an explicit base commit |
| The roles file and the constitution named the human holder differently | low | Bootstrap renames the holder to the person's name |
| E14 reported an empty consumer list twice | low | Fixed; test added |
| Not-applicable rows need an approver the human has not yet given | low | The Engineering Lead's merge of the bootstrap is the signature |

## What held

Every check refused when broken on purpose. CI ran on the new repository without changes.
The challenge session found real problems that every check passed, which is the reason
the method keeps a challenger and does not trust green runs alone.

## What did not transfer to a cold start

The method assumed a reader who already knew why each rule exists. A cold session asked
19 method questions in about five minutes. The template now answers each of them in
BOOTSTRAP.md or in the file it concerns. A second dry run, from the fixed template, should
show whether the count falls.
