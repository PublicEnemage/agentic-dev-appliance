---
id: STD-005
type: standard
title: Data governance
status: draft
author_seat: Architect
challenger_seat: Verifier
approver: Engineering Lead
parents: []
approved_at: null
---

# Data governance

- **Kind:** craft standard
- **Owning seat:** Operator, who owns the classification rule (floor row C5). The template
  draft was written in the Architect seat; the Operator maintains it once approved
- **Applies to:** all data the system stores, processes or exports

A draft default. Adapt the clauses at bootstrap, then challenge and approve this file.
A rejection must cite a clause number.

## Clauses

1. **Classification drives handling.** Every dataset carries a class from the risk
   assessment: public, internal, confidential or regulated. Each class has a written rule
   for access, encryption at rest and in transit, and export.
2. **Retention is a schedule, not a habit.** Each class has a retention period that meets
   the NFR in floor row C4. Data past its period is deleted or anonymised by a scheduled job.
3. **Deletion is tested.** A user or legal deletion request removes the data from every
   store that holds it, including derived data and backups within their stated window.
   The deletion path has its own test.
4. **Lineage is recorded.** Every derived dataset names its inputs, so the effect of a
   bad input or a deletion can be traced forward.
5. **Access to confidential and regulated data is logged.** The log records who, what,
   when and why, and is kept for the audit period.
6. **Agents get least privilege.** No agent seat holds credentials to production data it
   does not need for its charter.
