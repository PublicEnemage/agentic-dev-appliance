---
id: '{{PREFIX-NNN}}'
type: architecture
title: '{{Title}}'
status: draft
author_seat: Architect
challenger_seat: Builder
approver: Engineering Lead
parents:
- CD-001
- NFR-001
approved_at: null
layers:
  data:
    author_seat: '{{seat}}'
    challenger_seat: '{{seat}}'
  domain-core:
    author_seat: '{{seat}}'
    challenger_seat: '{{seat}}'
  services-apis:
    author_seat: '{{seat}}'
    challenger_seat: '{{seat}}'
  frontend:
    author_seat: '{{seat}}'
    challenger_seat: '{{seat}}'
  integration:
    author_seat: '{{seat}}'
    challenger_seat: '{{seat}}'
  deployment-runtime:
    author_seat: '{{seat}}'
    challenger_seat: '{{seat}}'
  operations:
    author_seat: '{{seat}}'
    challenger_seat: '{{seat}}'
---

# {{Title}}

Floor rows D2, D6, D7, D8. Each layer has its own author and challenger in front matter
`layers`, and both must be qualified for that layer in `docs/roles.yml`. Check D6 refuses
a layer no qualified seat covers. That refusal opens a crew review.

## Data
{{System of record, schema ownership, and how the schema changes.}}
Data standards live in `docs/standards/data/` (full data discipline arrives in v0.2).

## Domain or computation core
{{The domain logic or computation the product depends on.}}

## Services and APIs
{{}}

## Frontend and presentation
{{}}

## Integration
{{Every exchange between components. Each one needs a contract test (D9).}}

## Deployment and runtime
{{}}

## Operations
{{}}

## Failure modes (D7)
For each layer: missing, late, duplicate or malformed input, dependency down, partial
success. Each mode needs a handling rule and a signal that makes the failure loud.

| Layer | Mode | Handling rule | Loud signal |
| --- | --- | --- | --- |

## Decision tables (D8)
Logic with more than three interacting conditions goes here as a table with no empty cells.
