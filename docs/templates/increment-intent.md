---
id: '{{PREFIX-NNN}}'
type: increment-intent
title: '{{Title}}'
status: draft
author_seat: Product
challenger_seat: Verifier
approver: Intent Owner
parents:
- PLAN-001
approved_at: null
dor:
  I1:
    status: open
  I2:
    status: open
  I3:
    status: open
  I4:
    status: open
  I5:
    status: open
  I6:
    status: open
  I7:
    status: open
  I8:
    status: open
---

# {{Title}}

The Verifier must be able to write every test from this file without reading code (I1).

## Use cases in scope
{{UC paths, including at least one failure path (I4).}}

## Observable outcomes
{{What the user or system can see when this increment works.}}

## Acceptance criteria
- Given {{}}, when {{}}, then {{}}.
- Failure path: given {{}}, when {{}}, then {{}}.

## Input manifest (I7)
The artifacts a fresh session reads to work on this increment:
- {{artifact id or path}}
