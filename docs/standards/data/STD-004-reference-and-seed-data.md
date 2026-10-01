---
id: STD-004
type: standard
title: Reference and seed data
status: draft
author_seat: Architect
challenger_seat: Verifier
approver: Engineering Lead
parents: []
approved_at: null
---

# Reference and seed data

- **Kind:** craft standard
- **Owning seat:** Architect owns this standard; each reference dataset names its owner
- **Applies to:** lookup tables, code lists, configuration data, and the seed data each
  environment starts with

A draft default. Adapt the clauses at bootstrap, then challenge and approve this file.
A rejection must cite a clause number.

## Clauses

1. **Every reference dataset has a named owner seat.** The owner approves every change.
2. **Reference data is versioned in the repository.** Changes go through a pull request,
   never a manual edit to an environment.
3. **Seeding is a script, and the script is idempotent.** Running it twice leaves the same
   state. Each environment records the seed version it holds.
4. **Seed presence is checked, not assumed.** Startup, the health endpoint (floor row P8)
   and tests check that required seed data is present, and fail loudly when it is not.
   A test never skips because data is missing. (WorldSIM NM-097: tests skipped on a
   connection check while the database was under-seeded.)
5. **Test seeds are synthetic.** No production personal data is used as seed data in any
   non-production environment.
