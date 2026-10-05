---
id: RP-001
type: role-proposal
title: Frontend Architect seat
status: draft
author_seat: Product
challenger_seat: Architect
approver: Engineering Lead
parents: []
approved_at: null
proposed_seat: Frontend Architect
charter:
  trigger: 'The Intent Owner approves a ux-design for a product with a user interface and the architecture is approved; a challenge finding or a failed gate reopens the frontend design or its stories'
  inputs:
    - {artifact: ux-design, from: Designer}
    - {artifact: design-system, from: Designer}
    - {artifact: architecture, from: Architect}
    - {artifact: nfr, from: Architect}
    - {artifact: review, from: Verifier}
  value: 'Turns the approved ux-design into a buildable frontend: structure, state, data access, accessibility and performance against the NFRs, and the contract with the services layer. Writes the frontend stories Delivery orders, records each cross-cutting frontend choice as an ADR, and challenges the Designer''s frontend section for what can be built and tested. The seat needs judgment because one screen can be built several ways at different cost, and no rule picks between them'
  outputs:
    - {artifact: story, for: Delivery, acceptance: 'Each story names the ux-design flow and the architecture section it implements, and meets floor I1, I4 and I7'}
    - {artifact: review, for: Designer, acceptance: 'Findings on the frontend layer section, each with a reason, answered item by item (E10)'}
    - {artifact: adr, for: Builder, acceptance: 'Each cross-cutting frontend choice has an ADR the Builder can follow without asking (floor I3)'}
  standards: [docs/dor/floor.yml, docs/artifact-types.yml]
  templates: [docs/templates/story.md, docs/templates/adr.md, docs/templates/review.md]
  verifier:
    seat: Verifier
    evidence: 'A review file beside each frontend story set and ADR; every story names its ux-design flow and layer section (floor I7); frontend layer author and challenger qualified and distinct (SEATS)'
peer_review:
  - {seat: Designer, recommendation: '{{accept / accept-with-conditions / reject}}', demand: '{{}}', evidence: '{{}}'}
  - {seat: Architect, recommendation: '{{accept / accept-with-conditions / reject}}', demand: '{{}}', evidence: '{{}}'}
  - {seat: Verifier, recommendation: '{{accept / accept-with-conditions / reject}}', demand: '{{}}', evidence: '{{}}'}
  - {seat: Delivery, recommendation: '{{accept / accept-with-conditions / reject}}', demand: '{{}}', evidence: '{{}}'}
  - {seat: Builder, recommendation: '{{accept / accept-with-conditions / reject}}', demand: '{{}}', evidence: '{{}}'}
peer_recommendation: '{{accept / accept-with-conditions / reject}}'
---

# Frontend Architect seat

Status note: the template author drafted the charter from
`docs/method/dryrun-3-decisions.md`. The Product session that holds the author seat reads
every line against the roster and the decisions before this goes to peer review. The peer
entries are blank on purpose. Each peer writes its own.

## The case

- **Evidence of the gap:** the dry run 3 compile (`docs/method/dryrun-3.md`, overlap B and
  METHOD gap M-5) found that the Architect and the Designer both qualify for `frontend`
  and no seat decides between them. The sessions that raised it were not independent, so the
  decision of 2026-10-01 rests on the Engineering Lead's judgment, not on a count.
- **Why a rule or tool will not close the gap:** an authoring convention would settle who
  writes the section. It would not supply the technical judgment about state, accessibility
  and performance that the Architect's system-wide role does not cover.
- **Type:** standing.
- **Cost:** two sessions per user-facing increment, one for stories and ADRs and one to
  challenge the Designer's section.
- **Success measure and review date:** the Builder pulls frontend stories without asking
  what they should have said, and D6 passes for `frontend` with distinct author and
  challenger. Review after the first user-facing increment.

## Job description

The front matter is the job description. What it leaves out:

- **Late, malformed or missing input.** The seat rejects a `ux-design` that is not approved
  or has no flow for a story it is asked to write. It does not guess the flow.
- **Overlap to settle in peer review.** Product authors story content and Delivery owns
  order and manifests (decision 1). This seat writes frontend stories. Delivery and Product
  say where the line sits.
- **Frontend section authorship.** Who authors the technical frontend section of the
  architecture, and who challenges it, is open. The decision names the seat and its place
  in the chain, not the pair.
- **Roster entry on approval.** Copy the charter unchanged into `job` in `docs/roles.yml`.
  `qualified_layers: [frontend]`. The Architect's list loses `frontend`.
  Proposed incompatible pairs: `[Frontend Architect, Builder]`,
  `[Frontend Architect, Verifier]` and `[Frontend Architect, Designer]`. The holder is
  Agent A, because Agent B holds the Architect and the Designer, and the Designer and this
  seat challenge each other. The Engineering Lead confirms the holder at approval.
- **A frontend standard** is authored through the chain as its own artifact. None exists
  yet.
- **Wiring dependencies.** `design-system` has no artifact type yet. The apply change adds
  it, and adds `ux-design` for this seat to the Designer's outputs.

## Independent verification

The Verifier is not the author (Product), not the proposed seat, and holds a different
holder (Agent D) from the author (Agent A).

- **What it inspects:** review files beside each frontend story set and ADR, the layer
  section's author and challenger, and the flow named in each story.
- **How often:** each artifact.
- **What a failure looks like:** a story with no named flow, an ADR the Builder had to ask
  about, or a frontend section whose author and challenger are the same seat.

## Peer review

Each peer sends this seat input or takes its output. The Designer, Architect and Verifier
send input. Delivery and the Builder take output. Peers write their entries in their own
sessions. The author copies them in unchanged.

| Peer | Recommendation | Demand | Evidence |
| --- | --- | --- | --- |
| Designer | | | |
| Architect | | | |
| Verifier | | | |
| Delivery | | | |
| Builder | | | |

## For the Engineering Lead

{{Written after peer review: what the seat does, who wants it, what the peers said, what
remains open.}}
