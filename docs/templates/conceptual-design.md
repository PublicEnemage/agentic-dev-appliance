---
id: '{{PREFIX-NNN}}'
type: conceptual-design
title: '{{Title}}'
status: draft
author_seat: Architect
challenger_seat: Verifier
approver: Engineering Lead
parents:
- UC-001
approved_at: null
---

# {{Title}}

Floor rows D1, D13. The challenger reviews cold, in a fresh session.

## Capabilities
| Use case | System capability |
| --- | --- |
| {{UC}} | {{capability}} |

<!-- diagram: capability-map -->
```mermaid
flowchart LR
  UC1[UC-1 Place an order] --> Cap1[Order capture]
  UC2[UC-2 Track an order] --> Cap2[Order status]
  Cap1 --> Cap3[Payment]
  Cap2 --> Cap1
```
