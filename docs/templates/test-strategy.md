---
id: '{{PREFIX-NNN}}'
type: test-strategy
title: '{{Title}}'
status: draft
author_seat: Verifier
challenger_seat: Architect
approver: Engineering Lead
parents:
- NFR-001
- UC-001
approved_at: null
---

# {{Title}}

Floor rows D5, D9, D10.

## Test levels (D9)
| Level | Proves | Tool (ADR) | Runs | Author seat |
| --- | --- | --- | --- | --- |
| Unit | | | pre-push | Builder |
| Contract | | | pre-push, CI | Verifier |
| Integration | | | CI | Verifier |
| End to end | | | CI | Verifier |
| Performance | | | dedicated runner | Verifier |
| Security | | | CI | Operator |

## NFR to test type (D5)
| NFR | Test type |
| --- | --- |

## Use case acceptance approach (D5)
| Use case | Approach |
| --- | --- |

## Test data standard (D10)
Owner, how fixtures are generated from the schema, the classification rule, and how seeding
is checked at test start.
