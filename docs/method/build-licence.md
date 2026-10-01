# Build licence: a renewable approval to build

**Status:** pending design. Not built. Written 2026-10-01.
**Decision requested from:** Engineering Lead, before the pilot's first cycle exit.

## The need

Approval of the architecture is one event. Standards, features and code move afterwards,
and nothing notices when they leave what was approved. The Engineering Lead's concern is
that standards drift and feature drift stay managed over time, not only at the design gate.

## What the appliance covers today

| Drift | Covered? | By what |
| --- | --- | --- |
| A document changes after its children were approved | Yes | E10 marks the child stale |
| The floor version moves | Partly | `appliance.yml` pins it; a mismatch fails the DOR check; someone must remember to bump it |
| A new dependency, folder or pattern appears | Judged only | Floor row I3 asks for an ADR per increment; no tool compares code to the architecture |
| A feature is built that no use case asked for | No | Each increment names its use cases; nothing detects the rest |
| An approval ages | No | An approved artifact stays approved indefinitely |

## Proposal

The licence is the design gate's standing precondition, recurring, and not a second
system.

1. **Computed, not declared.** A licence is valid when the latest approved conformance
   review is within the cadence and the baseline it recorded still matches. There is no
   stored "licensed" flag, because a flag can be set to pass a check, which the
   constitution forbids.
2. **The renewal is a conformance review.** A Verifier-seat session in a fresh context
   measures drift and writes a report. The Engineering Lead renews it. Each divergence gets
   one disposition: fix the code, amend the architecture through the chain, or take a
   time-boxed exception (`exceptions.md`). A divergence nobody can explain blocks renewal.
3. **What it measures, mostly by machine:**
   - dependencies against ADRs
   - top-level folders against the components diagram
   - contract files against the integration section
   - migrations against the data model
   - built features against the approved use cases
   - the floor version and standards versions against what the architecture was approved under
4. **Cadence by event and cycle.** A renewal falls due on a floor or standard version
   change, after N increments shipped, at a cycle exit, or when the count of new ADRs
   passes a limit. Calendar months do not match how the work flows.
5. **Suspension stops new increment work, not hotfixes.** A lapsed licence blocks pulling
   a new increment on an unchecked base. An urgent fix is never held back by it.

## Risks

- **Ceremony.** A renewal that only checks a date becomes the loophole the exception
  design guards against. The measures above have to be mechanical, or the review will be
  skipped.
- **Cost.** Each review is a session plus the Engineering Lead's time. The more it is
  measured by machine, the cheaper the cadence can be.
- **Overlap.** E10 staleness, I3 and the version pin already catch part of this. The
  licence adds the code comparison and the clock, and should reuse them.

## When to build

Not before the pilot. The pilot's first cycle exit runs one conformance review by hand, as
an ordinary artifact, with the dimensions in item 3. What it finds decides which measures
become checks. Building them first would guess at drift, which is how the first job
descriptions came out mismatched.

Trigger to build: the first by-hand review is done and the Engineering Lead has said which
measures were worth repeating.

## Open questions

- Whether the licence should cover each increment's code or only the architecture as a
  whole. The first is stricter and costs more.
- Who holds the conformance review. The Verifier is the default, but a Data Architect or
  Operator may be better placed for their layers.
- Whether the licence level should depend on grade: at Light, a review at release only; at
  Assured, every cycle.

## Pilot readiness, noted alongside

For a real application with real users, three planned checks matter more than the licence.
E13 (post-deploy verification) should be built before real users arrive. E7 (session hooks)
and E1 (identity-bound approvals) follow. A personal pilot can run under the
single-principal disclosure while E1 is pending.
