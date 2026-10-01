---
id: '{{PREFIX-NNN}}'
type: business-case
title: '{{Title}}'
status: draft
author_seat: Product
challenger_seat: Verifier
approver: Intent Owner
parents:
- INTENT-001
approved_at: null
domain_areas:
- area: '{{area-name}}'
---

# {{Title}}

Floor rows: C2, C6, C8, C9. The challenger reviews cold, in a fresh session.

## Worthwhile conditions
Measurable thresholds that make the effort worth doing.

| Kind | Threshold | Source |
| --- | --- | --- |
| Market | {{for example, 40 paying users by month 3}} | {{evidence}} |
| Business | {{margin, revenue or cost ceiling}} | {{evidence}} |
| Schedule | {{date after which the window closes}} | {{evidence}} |

## Kill boundaries
Crossing any of these stops the work. The benefits check tests them after release.

- {{boundary, as a number and a date}}

## Evidence from real users or the market (C9)
{{Interviews, usage data, behaviour. Agent opinion alone does not count.}}

## Domain areas (C8)
List each area of domain knowledge the use cases depend on in front matter
`domain_areas`. Check C8 refuses an area no seat is qualified to challenge.

## Rigor grade (C6)
{{light | standard | assured}}, because {{reason}}. Approved by the Intent Owner.
