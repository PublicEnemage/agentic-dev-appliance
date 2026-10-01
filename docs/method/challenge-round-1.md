# Challenge round 1

A blind challenger reviewed the appliance on 2026-09-30 from a copy with the author's backtest removed. Every finding was accepted by the Intent Owner, three with refinements, and each disposition is applied in [appliance-design.md](appliance-design.md).

| ID | Finding | Verdict | Disposition |
| --- | --- | --- | --- |
| C1 | Seat separation rests on self-declared identities | Accept | Rule 5 rewritten; check E1, one Git identity per seat with harness-written approvals |
| C2 | Red-first testing deadlocks required green checks | Accept | Rule 2 rewritten; check E2, strict expected-fail on a test-only PR with a red record per test |
| C3 | No machine for the no-op test pattern | Accept | Check E3, lint ban on early return and catch-to-false, zero-assertion runtime check |
| H1 | Controls git hooks cannot run | Accept | Rule 3 rewritten; check E7, agent-harness hooks |
| H2 | Gates proven once, then trusted | Accept | Rule 4 amended; check E6, gate canary every cycle on every lane |
| H3 | Only `main` protected, though the method creates lanes | Accept | Check E5; setup step 2 and day-one checklist updated |
| H4 | DoR rows can be filled with any text | Accept, refined | Seat charters list qualified layers and D6 is checked against them; D2 gains a domain or computation core layer |
| H5 | Verifier authored the validation verdict | Accept | Product drafts from Verifier evidence, Verifier challenges, Intent Owner approves |
| H6 | No rule for a parent amended after child approval | Accept | Check E10, children marked stale until re-challenged |
| M1 | Skip registry legitimises blanket skips (NM-018) | Accept, refined | Skips per test only; file-level and blanket skips banned; I6 updated |
| M2 | Completion claims not machine-derived | Accept | Check E8, story test manifest and CI-derived exit counts |
| M3 | Document-to-code drift uncovered | Accept | Check E10, code registries generated or tested against code |
| M4 | Validation on local stacks escapes parity | Accept | Check E12, validation environment built from CI definitions |
| M5 | Front-loaded artifact cost | Accept | Light grade: one consolidated artifact and one challenger session per phase; cost stated |
| M6 | Constitution budget cannot hold per-session rules | Accept, refined | Rule 8: the constitution holds only what no machine can enforce |
| M7 | Seat-swap evidence is circular | Accept | Primary measure is output passing verify and challenge |
| M8 | Non-required job decay; registry integrity | Accept | Check E11 |
| L1 | G0 headline not in the registry | Accept | Rule 1 and Summary cite the Engineering Lead's account as the source |
| L2 | Rule 9 cites unrelated entries | Accept | Rule 9 cites the Engineering Lead's account; entries kept as related only |
| L3 | Class counts from titles only | Accept | Noted; the hazard chart caption states classification by title |
| L4 | Release gate has no DoR rows | Accept | Rows R1 to R3 added |
| L5 | Pipelines have two owners | Accept | Builder owns pipeline code under the Operator's CI/CD approach |
| L6 | Hygiene, usability protocol, real-user evidence | Accept in part | Row C9 requires real-user evidence; repository hygiene left to project rules; usability protocol left to the UX module |

The challenger also found a defect in WorldSIM itself: entries NM-061 to NM-100 sit inside an unclosed markdown fence in the registry. Check E11 catches this class in an appliance project.
