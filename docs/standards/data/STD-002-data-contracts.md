---
id: STD-002
type: standard
title: Data contracts
status: draft
author_seat: Architect
challenger_seat: Verifier
approver: Engineering Lead
parents: []
approved_at: null
---

# Data contracts

- **Kind:** input contract between components
- **Owning seat:** Architect owns this standard; each contract is owned by its producer
- **Applies to:** every exchange between components: API calls, events, messages, files,
  and tables one component writes and another reads

A draft default. Adapt the clauses at bootstrap, then challenge and approve this file.
A rejection must cite a clause number.

## Clauses

1. **Every exchange has a contract file.** Contracts live in the contracts folder named in
   `appliance.yml`, one YAML file per exchange. Check E14 validates every file.
2. **A contract names its parties.** Each contract states `producer`, at least one entry in
   `consumers`, `kind` (api, event, file or table), `version`, `compatibility` and a
   `schema`. A contract with no consumer is dead output; a consumer of no contract is a
   dead subscription. Check E14 refuses both. (WorldSIM NM-038 and NM-090: events emitted
   with no consumer, and subscriptions to events no one emitted.)
3. **Names come from the contract, not from memory.** Field and event names in code and in
   tests are taken from the contract file or generated from it. (WorldSIM NM-091: a
   registry in an ADR listed event names the code did not have.)
4. **Both sides are tested against the contract.** The producer tests that its output
   matches the schema. Each consumer tests that it accepts the schema. Mocks are generated
   from the contract (floor row D9).
5. **Breaking changes get a new major version.** The old version stays available for a
   stated deprecation window. Each consumer moves to the new version in its own story.
6. **The producer owns the contract.** Consumers propose changes. The producer's seat
   authors the change, and a consumer's seat challenges it.

## Contract file shape

```yaml
id: orders.created
kind: event                 # api | event | file | table
producer: order-service
consumers: [billing-service, analytics]
version: 1.2.0
compatibility: backward     # backward | forward | full | none
schema:
  type: object
  required: [order_id, total, currency]
  properties:
    order_id: {type: string}
    total: {type: number}
    currency: {type: string}
```
