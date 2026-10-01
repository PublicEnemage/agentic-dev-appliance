# Dry run 3: seats review their own job descriptions

**Status:** plan, not yet run. Written 2026-10-01 before any session starts.
**Depends on:** pull requests #6 (dry run 2 fixes) and #7 (job descriptions and E17) merged.

## Why

Dry run 2 tested the bootstrap procedure. It could not test whether the job descriptions
are right, because the person who drafted them (the template's author) was the only one
who had read them. This run puts the descriptions in front of the seats they describe, and
asks each seat to say how it will help others and how it will ask for help.

It also fixes a flaw in run 2: the sessions were launched from an observer session whose
context leaked into them. This run uses the session boundary of Claude Code instead.

## Prerequisites (human)

1. Merge #6, then #7, in the template repository.
2. Create `PublicEnemage/appliance-dryrun-3` from the template. Public, with the ruleset
   from BOOTSTRAP step 2.
3. Optional: turn account memory off for the run (Settings, "Generate memory from chats"),
   since the memory notes load in every session and cannot be removed per session.

## Isolation protocol

- One directory per session: `~/dryrun-3/<seat>/`, each a fresh clone of the dry-run repo.
  `~/dryrun-3/` holds no `CLAUDE.md` and no other repository. Claude Code loads instruction
  files from the working directory and its parents, so a sibling project there would leak.
- Start each session from its own directory. Never from the template repo, and never with
  an added directory.
- The human pastes each prompt unchanged. The observer starts no session and reads outputs
  only after the run.
- First action of every session, before any other work: list in its log every project
  instruction file and every note about the person that is in its context. A leak that is
  recorded is a measured leak.

## Sequence

1. **Bootstrap** (BOOTSTRAP step 4), Architect seat, same prompt as run 2. Branch `bootstrap`.
2. **Seat review round.** One session per agent seat: Product, Delivery, Architect,
   Designer, Verifier, Builder, Operator, Steward. The Data Architect is optional and is
   reviewed by the Architect and Verifier sessions. Each writes `DRYRUN-JOBREVIEW-<seat>.md`
   on a branch `jobreview-<seat>`, cut from `bootstrap`. Sessions run in parallel and see
   each other's work only through the repository, after they have written their own.
3. **Compile.** A fresh Steward session merges the eight reviews into
   `DRYRUN-JOBREVIEW-COMPILED.md` on branch `jobreview-compiled`: changes proposed to each
   description, peer ratings, wiring mismatches, overlaps, and the help protocol drafts.
   The Steward compiles because it holds no artifact seat. It does not judge the
   findings.
4. **Decide.** The Engineering Lead reads the compiled review and says which changes apply.
   A fresh Architect session applies them to `docs/roles.yml` on `bootstrap`.
5. **Challenge, merge, smoke** as BOOTSTRAP steps 5, 6 and 8.

## Seat review prompt

Paste with `{SEAT}` filled in. The preamble matches the earlier runs.

> You are a fresh session in a clone of the project repository. Read `CLAUDE.md` first and
> follow what it says. You hold the **{SEAT}** seat. Do not read any directory outside this
> repository. Before anything else, write at the top of `DRYRUN-JOBREVIEW-{SEAT}.md` every
> project instruction file and note about the person that is in your context.
>
> Task, in order:
> 1. **Your own job.** Read your `job` in `docs/roles.yml`. For each line (trigger, inputs,
>    value, outputs, standards, templates, verifier) say keep or change, and why. Say
>    what you cannot do as written, and what you would refuse to accept as an input.
> 2. **The others.** For every other seat, read its `job`. Give a recommendation (accept,
>    accept-with-conditions, reject), what you would hand to it or take from it, and any
>    overlap with your own job. Check wiring: where another seat says it sends you an
>    artifact, do you list it as an input from that seat, and the reverse?
> 3. **Help protocol.** Say what you will offer each seat, and when. Say what you will ask
>    of each seat, where you will write the request so it survives the session, and how
>    long you will wait for a response before escalating, and to whom.
> 4. **Authority.** State what you decide alone, what you decide only after consulting
>    which seat, when you ask before acting, and what you would refuse to accept or do.
>    Say where the procedure left you less room than your job description implies.
> 5. Log every point where the procedure left you guessing, labelled PRODUCT or METHOD.
>
> Commit to branch `jobreview-{SEAT}` and push it. Never push to `main`. Do not edit
> `docs/roles.yml`; propose changes in your file.

## Predictions

| Measure | Predicted |
| --- | --- |
| Agent seats that propose a change to their own description | at least 6 of 8 |
| Peer ratings | 0 to 2 rejects; most descriptions rated accept-with-conditions |
| Unmatched outputs found by peers (16 on the baseline below) | at least 10 |
| Overlaps flagged | Product and Delivery (stories, work plans); Verifier and Steward (audit) |
| Help asks with no matching offer on the first draft | at least a third |
| Authority statements that claim more than the descriptions give | at least 4 of 8; the Steward and Verifier claim the right to refuse |
| Sessions reporting other projects' files in context | none; memory notes only, if memory is on |

## Baseline measured on the drafts

Measured on the template at the time of writing, with a script, before any seat saw the
descriptions:

- 27 outputs: 16 are not listed as an input by the seat they name as consumer.
- 40 inputs: 29 have no matching output on the sending seat.
- 15 output names are not artifact-type ids from `docs/artifact-types.yml`.

E17 does not catch these. It checks that the seats named exist, not that sender and
consumer agree. An earlier statement that E17 confirms the wiring was too strong.

## What the authority question tests

NM-014 in the WorldSIM registry names the cost of over-prescribing: a lead who answers
every mistake with a longer instruction gets a team that is compliant but not capable.
The appliance's remedy is to carry rules in standing documents and let the job
description carry identity. This run asks each seat to say what authority it takes before
any rule is written, so a block that grants authority is built from what the seats claim.

## Build list after the run

Each item waits for what the run teaches.

0. **Authority block** in every job description: what the seat decides alone, decides after
   consulting, asks before doing, and may refuse. E17 checks that it exists and that each
   escalation names a real seat.
1. **Help block** in every job description: offers (to which seat, what, when) and asks
   (of which seat, where written, response time, escalation). E17 refuses an ask with no
   matching offer from the seat asked.
2. **Wiring reconciliation:** every output a seat lists must appear as an input of its
   consumer from that seat, and the reverse. Artifact names become artifact-type ids,
   or a named non-type, so the match is exact.
3. **Seat library.** One versioned file per seat in the template repository. A project's
   roster references a file and version, and records any tuning as an override with a
   reason. Instantiation runs the reconciliation check against the seats chosen, which is
   what confirms the wiring for that context. New seats join the library through a
   peer-reviewed proposal.
