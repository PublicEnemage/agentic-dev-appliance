---
id: '{{PREFIX-NNN}}'
type: ops-readiness
title: '{{Title}}'
status: draft
author_seat: Operator
challenger_seat: Verifier
approver: Engineering Lead
parents:
- NFR-001
approved_at: null
---

# {{Title}}

Floor rows P4, P6, P8, R2.

- **Observability:** {{logs, metrics, traces, alerts}}
- **SLOs:** {{}}
- **Rollback:** {{how, and when it was last rehearsed}}
- **Performance baseline (P6):** {{numbers, runner, date}}

## Post-deploy verification (P8)
Every deployment exposes these, and check E13 runs them after each deploy:

| Endpoint or test | Returns | Pass condition |
| --- | --- | --- |
| Health | {{path, machine-readable status, seed data present}} | OK |
| Version | {{path, build ID or commit}} | Matches the build shipped |
| Seeded smoke test | {{one main path per use case in scope}} | All pass |
