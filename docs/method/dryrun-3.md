# Dry run 3: seats review their own job descriptions

**Date:** 2026-10-01. **Repository:** [PublicEnemage/appliance-dryrun-3](https://github.com/PublicEnemage/appliance-dryrun-3).
**Template:** `docs/roles.yml` in the run repository is identical to the template at `6c49816`.
**Plan:** [dryrun-3-plan.md](dryrun-3-plan.md). The human ran the sessions in Claude Code. The
observer started none and read the outputs after the run.

Purpose: have each agent seat review its own job description, peer-review the others, draft
how it offers and asks for help, and state its authority. The Steward compiles. The run asks
whether the descriptions agree with each other, and whether seats claim authority the
descriptions do not give.

## What ran

Eight seat sessions, one after the other: Product 19:59, Delivery 20:50, Architect 20:57,
Designer 21:39, Verifier 21:46, Builder 21:52, Operator 21:57, Steward 22:04. The Steward
compile followed at 22:25 on `jobreview-compiled` (54 KB). The plan said the seat sessions
run in parallel. They did not.

Deviations from the plan, all recorded here and none hidden:

- **Bootstrap did not run.** The plan's step 1 was skipped. The repository still has the
  template slots, so there is no `bootstrap` branch. The seats reviewed the template's own
  `docs/roles.yml`, so the review is not affected. Step 4 of the plan has no base branch.
- **No input manifest.** CLAUDE.md tells every session to read its task manifest. The seat
  review prompt did not supply one. All eight sessions reported this. The cause is the
  prompt, not the sessions.
- **Delivery wrote to the Product branch.** The Delivery prompt carried the Product branch
  name.
- **The compile prompt was written after the run began.** The plan had no prompt for step 3.
  It is now in the plan.

## Validity: the sessions were not independent

The plan expected context leaks and isolated each session by folder. The leak that happened
went through git, which the plan did not guard.

| Session | Branch cut from | Other reviews in its tree | Cites another review |
| --- | --- | --- | --- |
| Product | main | none | no |
| Delivery | Product's branch | Product | yes, by name and gap number |
| Architect | Delivery's commit | Product, Delivery | yes, "mirror of PRODUCT gap 5" |
| Designer | main | none | yes, Product and Architect reviews |
| Verifier | Designer's branch | Designer | yes, "same gap Designer gap 8" |
| Builder | main | none | not found by text search |
| Operator | Builder's branch | Builder | yes, "BUILDER gap 15" |
| Steward | Operator's branch | Builder, Operator | yes, both |

Six of eight sessions cite or sat on another review. Only Product and Builder are clean.
The compile's leak log found Delivery for certain, called the Steward unclear, and reported
"no evidence" for the other five. It missed four explicit citations and did not read git
ancestry, which explains the Steward at once. Its "also raised by" columns count
sessions that were not independent. Treat "three sessions agree" as one session plus
readers.

The compile also miscounts its own rating notes: Verifier 6 sessions add conditions, not 7;
Builder 5, not 6; Designer 3, not 4; Engineering Lead 4, not 5. The matrix is right.
A compile with no check produced a confident, wrong summary of itself.

## Predictions and results

| Measure | Predicted | Result |
| --- | --- | --- |
| Seats proposing a change to their own description | at least 6 of 8 | **Hit.** 8 of 8, from 4 to 15 changes each |
| Peer ratings | 0 to 2 rejects, most accept-with-conditions | **Hit, weakly.** 0 rejects, 42 of 72 ratings accept-with-conditions. No seat rejected a description with a verified structural defect (below), so the scale does not discriminate |
| Unmatched outputs found by peers (at least 10) | 10 or more | **Not cleanly scored.** The compile lists about 20 mismatch rows. A seat-pair recount (below) finds 6 of 10 unmatched outputs. The 16 baseline used a rule I cannot reproduce |
| Overlaps flagged | Product and Delivery; Verifier and Steward | **Half.** Product and Delivery on stories, yes. Verifier and Steward on audit, not raised. Found instead: Architect and Designer on frontend, Architect and Operator on integration |
| Help asks with no matching offer | at least a third | **Miss.** Most asks have a matching offer. By eye, fewer than 5 of about 40 do not. The sessions shared one source, and six read each other, so matching is weak evidence |
| Authority statements claiming more than the description gives | at least 4 of 8; Steward and Verifier claim the right to refuse | **Hit on count, miss on the claim.** All 8 seats. The Steward said it has no merge-blocking authority. The compile shows no refusal claim from the Verifier |
| Sessions reporting other projects' files | none | **Hit.** Every session listed only CLAUDE.md, STATE.md, the email and git user |

Not predicted: the git channel for leakage, the missing manifest, the unowned
`benefits-check`, the circular dependency in `risk-assessment` (the Operator produces it
only after the Architect's NFR is approved), and the Steward and Engineering Lead verifying
each other.

## Wiring recount

The compile counts mismatches by artifact name. A stricter test asks only whether the
consumer lists any input from the sender. On this roster it finds 10 outputs and 20 inputs
unmatched. The earlier baseline (16 and 29) used a different rule and cannot be reproduced
from the notes. Pin the rule before E-wiring ships.

By my reading of the compile, peers found 18 of those 30 (12 of 20 inputs, 6 of 10
outputs). Excluding the Data Architect, which no session reviewed as itself, 18 of 25.
Missed:

- Intent Owner to Delivery, the stop or continue decision
- Steward to Engineering Lead, the registry entry
- Architect to Designer, architecture
- Architect to Operator, NFR and architecture
- Delivery to Steward, delivery-system
- Intent Owner to Product, the problem statement
- Data Architect's two outputs and three inputs

Peers also found mismatches the pair test cannot see, such as the review the Verifier owes
Designer, Builder and Operator, and `verification evidence` against `increment verify
evidence`. A tool needs both tests. Peers, all one model reading one file, find about two
thirds of what a script finds and add the naming problems the script cannot.

## Defects confirmed against the files

These were checked in `docs/roles.yml`, `docs/artifact-types.yml` and `docs/dor/floor.yml`,
not taken from the sessions:

- `[Builder, Operator]` and `[Designer, Verifier]` are not in `incompatible_pairs`.
- The Verifier's `qualified_layers` is `[deployment-runtime, operations]`. Floor D6 needs a
  challenger qualified for each layer. The Verifier challenges data, services-apis, integration
  and frontend work.
- No seat is qualified for `domain-core`. D6 cannot pass for that layer.
- `design system` is an output of the Designer with no artifact type.
- `benefits-check` is an artifact type and appears in two seats' templates. No seat lists it
  as an input or output.

## What this changes

1. **The reconciliation check moves to the top of the build list.** Both tests, pair level
   and name level, with a pinned rule. The seats did not find all of it, and a seat library
   cannot be trusted without it.
2. **New check: review independence.** A review branch holds no other seat's review in its
   ancestry, and the file names its base. Cheap, and it would have caught six sessions.
3. **A compile is checked, not trusted.** Its counts and its leak log come from a script.
4. **The prompts name the base branch and supply a manifest.** Per design rule 10, the fix
   goes in the standing procedure. Add both to the run protocol in the plan.
5. **Peer rating needs a rule.** A description with a verified structural defect cannot be
   rated accept. Today nothing stops it.

## Left open

- The Engineering Lead has not decided which changes apply. The plan's steps 4 and 5 are not
  done, and no change to `docs/roles.yml` is made here.
- Decisions the sessions raised that the file cannot settle: who authors the frontend
  section, who authors integration and deployment-runtime, whether Product or Delivery
  authors stories, whether the Verifier's layers widen or D6 gets a designated-verifier
  exception, and who owns `benefits-check`.
- The escalation gap for blocked human seats was raised by seven sessions. The
  single-principal disclosure in CLAUDE.md already states it, and every session read that
  paragraph. Count it as read, not as found.
- The Data Architect was not reviewed as itself.
- A cold rerun with one clone per session and each branch cut from `main` would show how
  much of the 18 of 30 holds without cross-reading.
