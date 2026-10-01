# Roadmap

Each version turns more rules into running checks. Status per check: `docs/enforcement.yml`.

## v0.1 — baseline (this version)

- Templates for all 21 artifact types, the review file and the registry entry
- Definition of Ready floor (37 rows) and the project checklist
- Seats, charters, incompatible pairs and the minimum crew (`docs/roles.yml`)
- Checks that read files: E10 artifacts and trace, SEATS with D6 and C8, DOR, E9 caps,
  E11 registry, E3 static no-op lint
- Tests that show each check refusing what it should
- CI on every branch and a pre-push hook that works in worktrees

## v0.2 — identities, harness and data

- **E1:** one Git identity per agent seat; approvals bound to identity
- **E5:** rulesets on every lane, admins included; trigger-coverage check
- **E7:** agent-harness hooks: worktree pin, stash and checkout filter, commit on stop, recovery
- **E8:** story test manifest checked at integration; exit counts from CI
- **E4:** test IDs checked against the component contract file
- **E12:** validation environment built from CI definitions
- **E13:** post-deploy verification: health OK, reported version matches the build shipped,
  seeded smoke test per use case in scope; output is the release evidence (P8, R2)
- **Data discipline:** schema change policy, data contracts beyond APIs, data quality,
  reference and seed data ownership, governance, and the trigger for a Data Architect seat
- Second blind backtest against the WorldSIM registry

## v0.3 — the hardest checks

- **E2:** red record per test; strict expected-fail on a test-only PR
- **E6:** gate canary on every lane and worktree each cycle; non-required job health
- Runtime zero-assertion check (completes E3)

## Open questions

- Default merge autonomy
- Least-privilege tool permissions per seat; prompt injection through repository content;
  policy for model version changes
- Secrets management, incident response after launch, data migration, dependency licensing
- Floor governance across instances: who approves a floor change, how projects upgrade
