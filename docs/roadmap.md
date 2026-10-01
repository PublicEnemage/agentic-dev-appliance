# Roadmap

Each version turns more rules into running checks. Status per check: `docs/enforcement.yml`.

## v0.1 — baseline (this version)

- Templates for all 21 artifact types, the review file and the registry entry
- Definition of Ready floor and the project checklist
- Seats, charters, incompatible pairs and the minimum crew (`docs/roles.yml`)
- Checks that read files: E10 artifacts and trace, SEATS with D6 and C8, DOR, E9 caps,
  E11 registry, E3 static no-op lint
- Tests that show each check refusing what it should
- CI on every branch and a pre-push hook that works in worktrees

## v0.2 — identities, harness and data

Shipped so far:

- **Data discipline:** five draft data standards (schema change, contracts, quality,
  reference and seed data, governance), floor rows D11, D12 and I8, check E14 for data
  contracts, check E15 for append-only migrations, and an optional Data Architect seat
  with written adoption triggers.
- **Required diagrams:** architecture, conceptual design and UX artifacts carry Mermaid
  diagrams for context, components, data model, key interactions, deployment, user flows
  and navigation. Floor row D13 and check E16. The floor is now 41 rows.

- **Dry run 1 fixes:** the bootstrap rewritten for a cold start (seats, manifests, the
  challenge, answering findings, the smoke record), tests isolated from project settings,
  the hook hardened against redirected git (RG-001) and dirty trees, E10 finds stray
  artifacts, standard grade by default. Report: `docs/method/dryrun-1.md`.

- **Dry run 2 fixes:** the bootstrap names the template commit, records the product
  description in `STATE.md`, gives the answering session a seat and manifest, shows the
  not-applicable row shape, says the files on disk win over injected context, and the
  smoke items are runnable from their text. Report: `docs/method/dryrun-2.md`.

- **Crew proposals (E17):** a role proposal states a trigger, inputs and senders, value,
  outputs and consumers, standards and templates, and an independent verifier with
  evidence. Peers recommend on demand, and the Engineering Lead approves with that
  endorsement. Every seat in `docs/roles.yml`, human or agent, core or optional, carries
  the same job description, and the check refuses a roster without them. The core
  descriptions are drafts written from the artifact register. Open: peer review of them.

- **Agency and exceptions (design):** design rule 10 (prescribe outcomes and gates, let the
  job description carry judgment) and a constitution line. The exception mechanism is
  designed in `docs/method/exceptions.md`: a time-boxed, capped, priced artifact, with
  expiry that fails the build, one renewal, repeat detection, a live budget and a short
  non-waivable list. Build follows dry run 3.

Still to come:

- **Build licence (design):** a renewable, computed approval to build, renewed by a
  conformance review that measures code, features and standards against what was approved.
  Design in `docs/method/build-licence.md`. First review run by hand in the pilot; build
  the checks from what it finds.
- **Exceptions (E18):** the artifact type, template and check, then the runner's waiver
  matching. Design in `docs/method/exceptions.md`.
- **Registry check target:** E11 refuses "none" or "TBD" as a countermeasure but accepts any
  other text, so a prompt tweak passes. The Check field should name an existing check or
  repository path.
- **Bootstrap-complete check:** the untouched template passes every check with all slots
  unfilled, so nothing catches a missed bootstrap edit. A flag in `appliance.yml` would let
  a check refuse unfilled slots once bootstrap is declared done.

- **E1:** one Git identity per agent seat; approvals bound to identity
- **E5:** rulesets on every lane, admins included; trigger-coverage check
- **E7:** agent-harness hooks: worktree pin, stash and checkout filter, commit on stop, recovery
- **E8:** story test manifest checked at integration; exit counts from CI
- **E4:** test IDs checked against the component contract file
- **E12:** validation environment built from CI definitions
- **E13:** post-deploy verification: health OK, reported version matches the build shipped,
  seeded smoke test per use case in scope; output is the release evidence (P8, R2)
- Second blind backtest against the WorldSIM registry
- Dry run 2 from the fixed template, to see whether the method questions fall

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
