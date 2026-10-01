---
id: '{{PREFIX-NNN}}'
type: delivery-system
title: '{{Title}}'
status: draft
author_seat: Delivery
challenger_seat: Verifier
approver: Engineering Lead
parents:
- PLAN-001
approved_at: null
---

# {{Title}}

Floor row P5.

- **Hierarchy:** epic (capability, no commits) → story (one path, one PR) → task (one seat, one session).
- **Split rule:** a story splits when it needs more than one seat or more than one PR.
- **Story template:** `docs/templates/story.md`.
- **Prioritization rule:** stories that test a business-case assumption first, then enablers, then value per use case.
- **Cadence:** {{cycle length}}.
- **Track cap:** {{n}}, set in `appliance.yml`.
- **Metrics:** computed from the repository, each paired with a quality measure.
