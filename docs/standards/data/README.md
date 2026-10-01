# Data standards

The data discipline. Five draft standards ship with the template. Each project adapts the
clauses at bootstrap, then a challenger reviews and the Engineering Lead approves them.
Floor row D11 requires each one approved, or signed not-applicable with a reason.

| Standard | Owning seat | Closes (WorldSIM) |
| --- | --- | --- |
| [STD-001 Schema change policy](STD-001-schema-change-policy.md) | Architect | NM-003, 011, 036, 049, 051, 086 |
| [STD-002 Data contracts](STD-002-data-contracts.md) | Architect; each contract by its producer | NM-038, 090, 091 |
| [STD-003 Data quality](STD-003-data-quality.md) | Architect; Verifier challenges | NM-060 |
| [STD-004 Reference and seed data](STD-004-reference-and-seed-data.md) | Architect; each dataset names an owner | NM-097 |
| [STD-005 Data governance](STD-005-data-governance.md) | Operator | (classification, retention, deletion, lineage) |

## Checks

- **E14 data contracts:** every contract file has a producer, at least one consumer, a kind,
  a version, a compatibility mode and a schema. Contract ids are unique.
- **E15 append-only migrations:** a pull request may add migrations, never edit or delete one.

Folders are set in `appliance.yml` under `data`.

## When to adopt a Data Architect seat

By default the Architect seat owns the data layer. A dedicated Data Architect seat is
already chartered in `docs/roles.yml` under `optional_seats`. Open a role proposal
(`docs/templates/role-proposal.md`) to adopt it when any of these is true:

1. The system has more than two persistent stores, or more than five data contracts.
2. Any dataset is classed regulated.
3. External datasets with quality profiles are central to the product's value.
4. Two or more registry entries in one cycle trace to schema, contract or seed data.
5. The architecture's data layer has no qualified challenger other than its author.

WorldSIM adopted its Data Architect after a schema guess shipped (NM-003, NM-011). These
triggers are meant to raise the question before that point.
