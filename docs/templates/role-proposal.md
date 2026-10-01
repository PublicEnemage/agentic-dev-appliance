---
id: '{{PREFIX-NNN}}'
type: role-proposal
title: '{{Title}}'
status: draft
author_seat: Delivery
challenger_seat: Architect
approver: Engineering Lead
parents: []
approved_at: null
proposed_seat: '{{Name of the new seat}}'
charter:
  trigger: '{{The event or condition that puts this seat to work}}'
  inputs:
    - {artifact: '{{artifact type or id}}', from: '{{seat that supplies it}}'}
  value: '{{What the seat does with the inputs, and why that needs judgment}}'
  outputs:
    - {artifact: '{{artifact type}}', for: '{{seat that consumes it}}', acceptance: '{{how the consumer tells it is good enough}}'}
  standards: ['{{docs/standards/... or the standard it will follow}}']
  templates: ['{{docs/templates/...}}']
  verifier:
    seat: '{{A seat other than the author and the proposed seat, on a different holder from the author}}'
    evidence: '{{What the verifier inspects to confirm the seat follows its own process}}'
peer_review:
  - {seat: '{{peer seat}}', recommendation: accept, demand: '{{What this seat would hand to or take from the new seat}}', evidence: '{{Registry ids, findings or artifacts that show the need}}'}
  - {seat: '{{second peer seat}}', recommendation: accept, demand: '{{}}', evidence: '{{}}'}
peer_recommendation: accept
---

# {{Proposed role}}

Any seat or the Steward may author. Another seat challenges on the role, rule or tool test.
The Engineering Lead approves, and reads the peer review first.

The front matter is the job description. The check E17 reads it, so keep each value to
what the seat actually does. A seat that cannot fill a line has not yet been defined.

## The case

- **Evidence of the gap:** {{registry ids, challenger findings, a failing D6 or C8 check}}
- **Why a rule or tool will not close the gap:** {{}}
- **Type:** standing / surge until {{date}} / advisory
- **Cost:** {{sessions per cycle}}
- **Success measure and review date:** {{}}

## Job description

Say it in prose where the front matter is too short to carry it.

- **Trigger:** what starts the seat, and who or what raises it.
- **Inputs:** each artifact, the seat it comes from, and what the seat does when an input
  is late, malformed or missing. The seat has the right to reject an input that does not
  meet the standard.
- **Value:** what the seat does with the inputs that no other seat does, and what would
  go wrong without it.
- **Outputs:** each artifact, the seat that consumes it, and the acceptance test the
  consumer applies.
- **Standards and templates:** which it follows, and which it authors. A new standard
  goes through the chain as its own artifact.
- **Roster entry:** on approval, copy the charter unchanged into the seat's `job` in
  `docs/roles.yml`, with its concern, qualified layers or domains and incompatible pairs.
  The check refuses a roster whose job differs from the approved charter.

## Independent verification

The verifier is a seat that is not the author, not the proposed seat and not on the
author's holder. It confirms that the seat does what this proposal says it does.

- **What it inspects:** {{files, review records, CI results}}
- **How often:** {{each cycle, each artifact, at the first use}}
- **What a failure looks like:** {{}}

## Peer review

Each peer is a seat that sends the new seat input, consumes its output, or owns the work
the new seat would take from it. Every agent seat named in the charter must appear. Peers
answer for demand: would they use it, and what do they stop doing themselves.

| Peer | Recommendation | Demand | Evidence |
| --- | --- | --- | --- |
| {{seat}} | accept / accept-with-conditions / reject | {{}} | {{}} |

The group's recommendation is no more favourable than its least favourable member.
Conditions go here and are answered item by item.

## For the Engineering Lead

{{Two or three sentences: what the seat will do, who wants it, what the peers said,
what remains open.}}
