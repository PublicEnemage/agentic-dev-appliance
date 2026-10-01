<!-- Exported 2026-10-01 from the working design document. This file is the design rationale
for the appliance: why each rule exists. The machine-readable rules live in docs/dor/,
docs/roles.yml, docs/artifact-types.yml and docs/enforcement.yml; where they differ, those win. -->

# Governed Agentic Development Appliance — Core vs Contextual Decision Log

Sep 30, 2026 · @Imran

## Summary

WorldSIM grew about 30 agent roles, a 52 KB constitution, a 157 KB roster and 100 near-miss entries by July 2026. The appliance proposed here runs on 2 human seats and 5 agents, with 4 phase gates above 4 increment gates and a 41-row Definition of Ready floor. Everything else becomes an optional module or a project-level rule. A blind challenger backtested the draft against WorldSIM's 100 near-misses and found only 19 caught by a named check. Twelve enforcement checks now name the missing mechanisms.

The near-miss registry changes the emphasis of the charter. The lessons the charter headlines, such as generative consultation and panel-to-root-cause matching, account for about 6 of 100 entries. Roughly half of all entries fall into three mechanical classes: tests that pass without measuring anything, parallel agent sessions corrupting each other's work, and gates that existed only on paper. These three classes are universal to agentic development and can be closed by machinery rather than by instruction. The appliance should lead with them.

One more lesson sits above the registry. WorldSIM added a Business PO agent at M9, and business intent ownership was still retrofitted late. A simulated owner cannot kill a product. The appliance therefore puts a named human intent owner, with a written kill criterion, at gate zero. This lesson comes from the Engineering Lead's account of WorldSIM, not from a registry entry.

Source: shallow clone of `PublicEnemage/worldsim`, last commit 2026-07-07. Note that the charter's "27 entries" figure is stale; the registry now runs to NM-100.

## What the WorldSIM evidence shows

*[Diagram in the live document: WorldSIM near-miss registry NM-001 to NM-100, classified by title; one class per entry, a judgement call at the edges]*

The largest class is false green. A test skips softly, a selector matches nothing, a timeout expires silently, or an issue closes without delivery. CI stays green while nothing is measured. NM-027 records the pattern recurring four times after a countermeasure was filed, so a written fix did not hold.

The second class is specific to agents. Several sessions shared one working tree, switched branches under each other, stashed each other's work, or reported edits done that were never committed. Human teams rarely hit this at the same rate, because humans do not run five of themselves in one folder.

The third class is gates that lived in documents. Pre-push checks, required status checks and branch rules were written down but not wired into hooks or rulesets. NM-070 is the turning point, where the gates moved into git hooks.

The remaining classes are real but smaller. Contract drift and environment issues are mostly domain and stack detail. Consultation and authority lessons are the most transferable in spirit, and the cheapest to encode.

## Design rules for the appliance

Each rule answers a hazard class above. Together they are the appliance's constitution in compressed form.

1. **Intent has a human owner before any code exists.** The owner writes the business intent, the success measure and the kill criterion. An agent can draft the intent; only the owner can sign or kill it. (Engineering Lead's account of WorldSIM; no registry entry records this directly)
2. **A check counts only after it has been seen to fail.** Tests land on a test-only PR as strict expected-fail, so CI records each test red without blocking merges. The implementation PR flips each marker, and a strict expected-fail fails the build if the test passes early. A zero-assertion test, a missing selector or a blanket skip fails the build. (False green, 27 entries)
3. **One agent, one worktree, one branch.** Sessions never share a working tree. Git hooks cannot enforce this, so the agent harness does: the worktree is pinned at session start, and stash and foreign checkouts are blocked. (Parallel sessions, 17 entries)
4. **A gate that is not in tooling is a suggestion.** Every gate names the hook, required check or ruleset that enforces it. A gate without one is listed as advisory. Gates are re-proven every cycle by a canary, never trusted after setup. (Paper gates, 8 entries)
5. **Ownership is checked by the machine, against real identities.** Each agent seat holder works under its own Git identity. Required reviews must come from a different identity, so an agent cannot approve its own work or sign for another seat. Without distinct identities, CODEOWNERS is an honour system. (Authority, 10 entries; NM-042)
6. **Reviewers are asked before the decision is framed, and one of them starts cold.** Consultation is generative. Independent review runs in a fresh session with no access to the author's reasoning. (Consultation, 6 entries)
7. **Every near-miss produces a redesign, and every redesign ships as a check.** The countermeasure is never "be more careful". A recurrence then fails the build instead of waiting for someone to recheck. (NM-027, NM-068)
8. **The constitution holds only what no machine can enforce.** Agents read the constitution at every session start, so it has a size budget. A rule enforced by a check lives in the check. WorldSIM's session file outgrew the read limit (NM-066).
9. **Context is disposable; the repository is the memory.** No work depends on what a session remembers. Each task is sized to one seat and one session, reads only the artifacts named in its input manifest, and leaves everything the next session needs in the repository. A long session is a risk to be cut, not a convenience. (Engineering Lead's account of why WorldSIM moved from milestones to sprints; related entries NM-014, NM-066, NM-089)
10. **Prescribe outcomes and gates, and let the job description carry the judgment.** Standing documents (the constitution, job descriptions, standards) carry the rules. A task carries its outcome and acceptance criteria. A prompt names the task and nothing more. When an agent errs, the fix goes upstream into a standing document or a check, never into a longer prompt, because a lead who answers each mistake with more instruction gets a team that is compliant but not capable. Cold-start evidence sets the limit: a seat given too little standing procedure asks for it (dry run 1, 19 method questions), so the cure is a better standing document, not a thicker prompt. (NM-014, NM-016, NM-018)

## Enforcement: every rule names its machine

The first challenge round found that most rules were stated but not specified. A rule without a named check is advisory under rule 4. The checks below are the mechanisms the template repository must ship. Tool names are examples; each project confirms its tools by ADR.

| ID | Check | Where it runs | Closes |
| --- | --- | --- | --- |
| E1 | One Git identity per agent seat holder. Required reviews come from a different identity. Approval records are written by the harness from the authenticated identity, and CI checks front-matter seats against commit and review identities | Repository settings, CI | NM-007, 021, 034, 042, 053, 084 |
| E2 | Test-only PR lands tests as strict expected-fail. CI keeps a red record per test ID. The implementation PR must flip every marker, and a test with no red record fails | CI | NM-017, 065, 085, 095 |
| E3 | Lint bans early return, conditional assertions and catch-to-false in test files. A runtime check fails any test that finishes with zero assertions | Pre-push, CI | NM-027, 028, 047, 048, 056, 061 |
| E4 | Every test ID used in a test exists in the component contract file and in source. A rename fails until the tests follow | CI | NM-039, 058, 062, 076 |
| E5 | Rulesets on every branch pattern, admins included, with direct push blocked. A check confirms every required check triggers on every lane | Repository settings, CI | NM-035, 044, 073, 074, 080 |
| E6 | Gate canary: each cycle, a known-bad change is pushed on every lane and from a worktree, and must be refused. A canary that passes files a registry entry | Scheduled CI | NM-015, 052, 092 |
| E7 | Harness hooks: worktree and branch pinned at session start; stash, force push and foreign checkout blocked; work in progress committed to the session branch on stop; abnormal end detected and recovered at the next start | Agent harness, not git | NM-014, 075, 079, 087, 088, 089, 100 |
| E8 | Each story carries a manifest of its test IDs. At integration, CI checks every listed test is present, collected, and was red before green. Exit counts come from CI, and a PR's file list is checked against its description | CI | NM-026, 043, 055, 094, 096 |
| E9 | Scripts check the stated caps: state file size, shared-state lane paths in both directions, and the track count | CI | NM-066, 067, 071, 093 |
| E10 | Amending an approved parent marks its children stale until re-challenged. Registries that describe code are generated from code, or tested against it | CI | NM-022, 058, 081, 091 |
| E11 | A non-required job failing on consecutive runs opens an issue. The registry is checked for unique ascending IDs and well-formed markdown | Scheduled CI | NM-097 |
| E12 | Validation runs on an environment built from the same definitions as CI, with migration and seed state checked at start | CI, validation environment | NM-046, 049, 060 |

## Core vs contextual decision log

Of 32 elements reviewed, 17 are universal, 11 become optional modules and 4 are WorldSIM artifacts. The classification is a first pass from reading the source; each row is open to challenge.

| Element | WorldSIM source | Classification | Appliance form |
| --- | --- | --- | --- |
| Standing constitution | `CLAUDE.md` | Universal | Core file capped near 15 KB; mission and principles become fill-in slots |
| Intent owner and kill criterion | `Business PO agent (added M9)` | Universal | Named human signs intent and kill criterion at gate zero |
| Five-step lifecycle: intent, test, code, verify, validate | `agent-execution-lifecycle.md` | Universal | Kept whole; the spine of the appliance |
| Rejection artifact that returns to intent | `agent-execution-lifecycle.md` | Universal | Kept; failed verify or validate reopens the intent, not the code |
| Cycle entry and exit invariants | `CLAUDE.md §Entry and Exit Invariants` | Universal | Generalized from sprint to any work cycle |
| Intent test for the user | `North Star Test` | Universal | Owner names a real scenario the change improves; domain wording removed |
| File authority RACI | `agent-raci.md §File Ownership` | Universal | Nine seats plus the Steward; enforced by CODEOWNERS and required reviews |
| Independent review in a fresh session | `independent-review-prompt.md` | Universal | Kept; reviewer gets artifacts, never the author's reasoning |
| Near-miss registry | `near-miss-registry.md` | Universal | Kept; merged with known issues via a Type column |
| Known issues registry | `known-issues-registry.md` | Universal | Merged into the near-miss file as Type = external |
| Session state file | `SESSION_STATE.md` | Universal | Capped at 200 lines; archived at each cycle exit |
| Git working tree protocol | `agents.md §Git Working Tree Protocol` | Universal | One worktree per agent; no stash; hook-enforced |
| Pre-push and required-check gates | `CLAUDE.md, .githooks/pre-push` | Universal | Every gate names its hook or ruleset |
| PR merge gate | `CLAUDE.md §PR merge gate` | Universal | Kept as an autonomy setting: human merge, auto-merge on green, or release-branch only |
| Canonical artifact locations | `CLAUDE.md §Canonical Artifact Locations` | Universal | Kept; table ships pre-filled for the core artifacts |
| Architecture decision records | `CLAUDE.md, docs/adr/template.md` | Universal | Short template; tier field kept |
| Single-principal disclosure | `CLAUDE.md §Governance` | Universal | Kept verbatim in shape; states when review is not independent |
| ADR persona trace, asymmetry and mission fields | `docs/adr/template.md` | Optional module | Optional section for user-facing products |
| Decision-type RACI (10 types) | `agent-raci.md §Decision Type Grounding` | Optional module | Start with 3 types: architecture, scope, release |
| Layer 3 quality gate and Customer Agent | `agent-execution-lifecycle.md` | Optional module | Module for products with end users |
| Sprint group isolation | `sprint-group-isolation.md` | Optional module | Folded into the delivery system as the track cap and branch lanes |
| Insights log | `docs/insights-log.md` | Optional module | Module; the registry covers most of it early on |
| Socratic Agent | `agents.md §Socratic Agent` | Optional module | Recommended module; becomes a gate at the Assured grade |
| Audit prompt pack | `blind-code-audit-prompt.md, intent-block-author-prompt.md` | Optional module | Module for milestone audits |
| UX, UX Design Thinking and Frontend Architect roles | `agents.md` | Optional module | Designer seat is core where a UI exists; dedicated roles are a module |
| Data Architect and Data Quality roles | `agents.md` | Optional module | Data layer owned by the Architect seat; a dedicated data role is a module |
| Demo preparation and stakeholder reviews | `demo-preparation-standard.md` | Optional module | Module when external demos are a gate |
| Domain council pattern | `docs/agents/domain-intelligence-council.md` | Optional module | Pattern kept as a module; members supplied per domain |
| Nine council members (economists, analysts) | `agents.md §Domain Intelligence Council` | Domain artifact | Dropped |
| Guiding principles (human cost ledger, defense not offense) | `CLAUDE.md §Guiding Principles` | Domain artifact | Dropped; slot for the project's own principles |
| Simulation framework and data standards | `simulation-framework.md, DATA_STANDARDS.md` | Domain artifact | Dropped |
| External Intelligence Layer | `agents.md §External Intelligence Layer` | Domain artifact | Dropped |

## Minimal viable appliance

The minimal appliance is 2 human seats and 5 agents, 4 phase gates above 4 increment gates, and 7 artifact homes, plus the hooks and checks that enforce them. The test for inclusion is simple. An element stays in the core only if removing it reopens one of the large hazard classes or the intent-ownership gap.

### Minimum crew

| Holder | Seats | Why this split holds |
| --- | --- | --- |
| Human | Intent Owner | Accountable seat; cannot be an agent |
| Human | Engineering Lead | Accountable seat; may be the same person as the Intent Owner |
| Agent A | Product, Delivery, Operator | None of these seats challenges another in the artifact register |
| Agent B | Architect, Designer | Neither seat challenges the other |
| Agent C | Builder | Conflicts with Product, Architect, Designer and Verifier |
| Agent D | Verifier | Conflicts with Product, Architect, Operator and Builder |
| Agent E | Steward | Holds no seat; audits the process and keeps the registry |

This is one valid assignment under the incompatible pairs, not the only one. Each seat still works in its own session, and larger work splits seats across more agents through a crew review.

One person will often hold both human seats on a small venture. The single-principal disclosure from WorldSIM covers that case honestly.

### Gates

*[Diagram in the live document: proposed gate flow · 4 gates, 1 build step, 1 rejection loop]*

G0 is highlighted because it is the gate WorldSIM lacked longest. Each gate names its enforcing mechanism, so a gate without one shows up as a gap rather than a promise.

These four gates run inside each increment. Four phase gates sit above them (case, design, plan and release), shown in the artifact chain below.

### Artifacts

| Artifact home | Location | Update rule |
| --- | --- | --- |
| Constitution | `CLAUDE.md` | Engineering Lead only; size-capped |
| Roles and ownership | `docs/roles.md` + `CODEOWNERS` | Changed together or not at all |
| Definition of Ready | `docs/dor.yml` | Floor rows pinned by version; project rows only finer |
| Standards | `docs/standards/` | Input contracts owned by the consuming seat; craft standards by the producing seat |
| Artifact chain | `docs/case/`, `docs/design/`, `docs/plan/`, `docs/intents/`, `docs/adr/` | Front matter with ID, seats, status and parents; a review file beside each artifact |
| Registry | `docs/registry.md` | Append only; Type = near-miss or external |
| State | `STATE.md` | Size-capped; rewritten each session; archived each cycle |

### Deliberately left out of the core

- Domain councils, demo standards and audit packs. Each is an optional module with its own trigger. Row C8 decides when domain expertise needs a seat.
- Dedicated UX, data and frontend roles beyond the core seats. These arrive through a crew review when a Definition of Ready row cannot be filled.
- The ten-type decision RACI. Three decision types cover the first cycles.
- An insights log. The registry and issue tracker absorb it early on.

## Separation of concerns: the artifact chain

Separation of concerns is enforced per artifact, not per agent. Every artifact in the chain has an author, a challenger and an approver, and no role holds two of those seats on the same artifact. The minimum crew stays small. The seats are what create checks and balances.

### Five duties on every artifact

- **Consulted** seats contribute before the author drafts. Each writes an independent input cold, without seeing the others or a draft, so consultation is generative rather than confirmatory (NM-005, NM-013). The consulted set is chosen by the problem's likely root-cause domain, not its surface domain (NM-018).
- **Author** produces the artifact from named upstream artifacts and the consulted inputs, and from nothing else.
- **Challenger** is a different role in a fresh session, asked to find what is wrong or missing before approval. Findings are written and answered item by item.
- **Approver** accepts on behalf of the concern the artifact serves. Business artifacts need a human approver.
- **Consumer** is the next stage. If its author must ask a question the artifact should have answered, the artifact goes back. WorldSIM's rule that QA must be able to test from the intent alone is this duty, generalized.

### The chain

*[Diagram in the live document: proposed artifact chain · 5 phases, 4 gates, 2 loops]*

The earlier G0 to G3 gates run inside each increment. The phase gates above them decide whether increments start at all.

### Concern seats

Nine concern seats cover the chain. The Steward sits outside them, keeps the registry and gate checks, and holds no seat on any artifact. On small work a few agents hold several seats each; the incompatible pairs below decide which combinations are allowed. The minimum crew table above shows one valid assignment. Each seat's charter in the roles file lists the layers that seat is qualified for, and row D6 is checked against those charters.

| Seat | Concern | Default holder |
| --- | --- | --- |
| Intent Owner | Is this still worth doing? | Named human |
| Engineering Lead | Is this sound and governed? | Named human |
| Product | Who uses this, and for what? | Agent |
| Architect | How is the system shaped, and does it meet its NFRs? | Agent |
| Designer | How does it look and behave for users? | Agent, if applicable |
| Verifier | Does it do what the artifacts say? | Agent, fresh session |
| Builder | Code, pipeline code and implementation design, under the Operator's CI/CD approach | Agent |
| Operator | Security, privacy, deployment and run | Agent |
| Delivery | Is the work cut, ordered and flowing well? | Agent |

### Artifact register

Your list, in order, with four additions marked. Each row names the seats; "traces to" is the parent the artifact must cite.

| Artifact | Author | Challenger | Approver | Traces to |
| --- | --- | --- | --- | --- |
| Intent statement | Product | Architect | Intent Owner | Root |
| Business case, with worthwhile conditions and kill boundaries | Product | Independent cold review | Intent Owner | Intent |
| Business and system users | Product | Designer | Intent Owner | Business case |
| Business and system use cases | Product | Verifier | Intent Owner | Users |
| Non-functional requirements | Architect | Operator | Intent Owner and Engineering Lead | Use cases, business case |
| Risk, security and privacy assessment (added) | Operator | Architect | Engineering Lead | Use cases, NFRs |
| Conceptual system design | Architect | Independent cold review | Engineering Lead | Use cases, NFRs |
| Target-state architecture and ADRs | Architect | Operator and Builder | Engineering Lead | Conceptual design |
| UX design, if applicable | Designer | Product | Intent Owner | Use cases |
| UX treatments, brand and design system, if applicable | Designer | Builder | Intent Owner | UX design |
| Test strategy | Verifier | Architect | Engineering Lead | NFRs, use cases |
| Increment plan, G0 to MVP, each increment demonstrable against named use cases | Product | Builder | Intent Owner | Use cases, architecture |
| Architecture backlog | Architect | Builder | Engineering Lead | Architecture, increment plan |
| Test backlog | Verifier | Product | Engineering Lead | Test strategy, increment plan |
| Implementation design and backlog | Builder | Architect | Engineering Lead | Architecture, increment plan |
| Branching and CI/CD approach | Operator | Verifier | Engineering Lead | Test strategy, deployment targets |
| Operational readiness: observability, SLOs, runbooks, rollback (added) | Operator | Verifier | Engineering Lead | NFRs |
| Increment work plan | Product | Builder | Engineering Lead | Increment plan |
| Increment verify evidence | Builder | Verifier | Engineering Lead | Increment intent, tests |
| Increment validation verdict | Product, from the Verifier's evidence | Verifier | Intent Owner | Use cases in scope |
| Release decision (added) | Operator | Verifier | Intent Owner and Engineering Lead | Validation verdicts, readiness |
| Benefits check against the business case (added) | Product | Independent cold review | Intent Owner | Business case |

The benefits check closes the loop. The business case set kill boundaries at the start, and the benefits check tests them after release.

### Incompatible pairs

- The author of an artifact never approves the artifact.
- The Builder never writes the acceptance tests for its own work, nor challenges or verifies them. Unit tests are the Builder's craft, and mutation testing checks them.
- NFR conformance is verified by the Verifier, not by the Architect who set the NFRs.
- The author of the business case cannot sign the benefits check alone.
- The registry entry for an incident is filed by the Steward, never by the role whose work produced the incident.
- One agent in one session holding two seats on the same artifact is a violation, whatever the seats are called. With one human in both human seats, the single-principal disclosure applies.
- The Delivery seat owns the delivery process; the Steward audits adherence to the process. Neither holds the other's seat.

### Grades of rigor

Rigor changes the depth of each artifact, never the chain. Skipping an artifact silently is never allowed. "Not applicable" is itself a written entry, with a reason and an approver.

| Grade | When | Artifacts | Challenger |
| --- | --- | --- | --- |
| Light | Spike, internal tool, throwaway prototype | One consolidated artifact per phase covers every register row for that phase; a few lines per row is enough | One challenger session per phase; may share a session if disclosed |
| Standard | Default for anything with users | Full artifacts | Fresh session, different role |
| Assured | Regulated, safety-related, or handling money | Full artifacts plus retained evidence | Adds an external human on business case, architecture and security |

The grade is chosen in the business case and approved by the Intent Owner. Raising the grade later is allowed; lowering the grade needs a written reason.

The Light grade exists because the chain is expensive at full depth. At Standard grade, the register's 22 artifacts mean about 44 agent sessions and 22 sign-offs before the first increment. A small venture testing an idea should start Light and raise the grade when the case survives first contact with users.

### How traceability gets teeth

- Every artifact carries front matter: ID, stage, author seat, challenger seat, approver, status, and parent IDs.
- CI refuses a merge when a change cannot trace to a use case, when a use case cannot trace to the business case, or when author and approver are the same.
- Challenge findings live in a review file beside the artifact. An unanswered finding blocks approval.
- The trace matrix is generated from front matter at every gate. Nobody maintains the matrix by hand.
- A missing artifact is a failing check, not a reminder.
- A child artifact cannot be approved before all of its parents are approved (NM-072).
- CI checks each artifact's location and file name against its type, and checks that every cross-document reference resolves to a live ID (NM-002, NM-022).

### Standards and the right to reject

Every artifact type is governed by two standards, owned by different seats. A seat that owned the standard for its own output would be marking its own work.

| Standard | Answers | Owned by | Example |
| --- | --- | --- | --- |
| Input contract | Can the next stage work from this alone? | The consuming seat | The Verifier defines what an intent must contain to be testable |
| Craft standard | Is this well made by the norms of the discipline? | The producing seat, challenged by a peer seat | The Builder owns coding standards; the Architect challenges them |

WorldSIM already had the input contract in one place: the QA Lead had to be able to write tests from the intent alone, or the intent was incomplete. The appliance makes that pattern universal.

Any seat may refuse an input that breaks the input contract. The refusal stops the line for that artifact, not for the project. Four rules keep refusal from becoming a veto:

1. **No clause, no rejection.** A rejection cites the specific clause breached. A concern without a clause is a challenge finding, answered in the review file.
2. **Standards are pinned.** Work is judged against the standard version in force when the work started. A standard changed mid-stream cannot fail work already in flight.
3. **Two rejections escalate.** A second rejection of the same artifact goes to the approver, who decides between the producer and the consumer in writing.
4. **A gap in the standard is not a rejection.** When a rejection exposes something the standard never asked for, the fix is a standard change, and the artifact is judged by the old version.

Standards change through the same chain as any artifact: the owning seat authors, another seat challenges, and the Engineering Lead approves. The floor rule applies here too. Project standards may be finer than the appliance's floor, never coarser. Every rejection is logged, and rejection counts per artifact type tell the Steward which standards are unclear.

## Definition of Ready: the floor template

The Definition of Ready template is the operational checklist for every phase gate. Each row is a rule with a stable ID. A project may make the rules finer, never coarser, than this floor. Detection of gaps comes from rows that cannot be filled, not from anyone's insight.

### The floor rule

- A project may split a floor row into children (D2.1, D2.2) or add rows under a floor parent.
- A project may not delete, merge or weaken a floor row.
- "Not applicable" is an answer with a reason and an approver. The row stays.
- CI refuses a gate when the project checklist is missing any floor ID, holds an added ID with no floor parent, or has a blank row.
- The floor is versioned with the appliance, and each project pins a version. A project rule that proves itself in two instances can be promoted into the floor.

### Floor rows

| ID | Gate | Rule |
| --- | --- | --- |
| C1 | Case | Intent statement names the problem, the users and the Intent Owner |
| C2 | Case | Business case states worthwhile conditions and kill boundaries as measurable thresholds: market, business and schedule |
| C3 | Case | Every business and system user is listed, and every use case names its user |
| C4 | Case | NFRs give a target or signed "not applicable" for: deployment targets, availability, resilience and recovery, performance at low, average, high and stress load, data retention, security, privacy, cost to run |
| C5 | Case | Risk, security and privacy assessment covers data classification and the main threats |
| C6 | Case | Rigor grade chosen and approved by the Intent Owner |
| C7 | Case | Every use case lists its main path, alternate paths and failure paths, each with an expected outcome |
| C8 | Case | Domain knowledge the use cases depend on is named. Each area has a seat qualified to challenge it, with a counter-perspective where judgment is contested |
| C9 | Case | The business case cites evidence from real users or the market, such as interviews, usage data or behaviour, not agent opinion alone |
| D1 | Design | Conceptual design maps every use case to a system capability |
| D2 | Design | Target architecture has one section per layer: data, domain or computation core, services and APIs, frontend and presentation, integration, deployment and runtime, operations |
| D3 | Design | Every cross-cutting choice has an ADR with an owning seat: framework, state, storage, messaging, identity, styling |
| D4 | Design | UX design, including its experience intent, and design system exist, or are signed "not applicable" |
| D5 | Design | Test strategy names a test type for each NFR and an acceptance approach for each use case |
| D6 | Design | Every D-row section has an author seat and a different challenger seat, each qualified for that layer as listed in the seat's charter; CI checks the match against the roles file |
| D7 | Design | Each layer has a failure-mode list: missing, late, duplicate or malformed input, dependency down, partial success. Each mode has a handling rule and a signal that makes the failure loud |
| D8 | Design | Logic with more than three interacting conditions is specified as a decision table or state diagram, with no empty cells |
| D9 | Design | Each test level has a purpose, tool, runner and owning seat, decided by ADR. Contract tests are required wherever two components exchange data |
| D10 | Design | A test data standard names its owner, how fixtures are generated from the schema, the data classification rule, and how seeding is checked |
| D11 | Design | The data standards are approved, or each is signed not-applicable: schema change policy, data contracts, data quality, reference and seed data, data governance |
| D12 | Design | Every exchange named in the architecture's integration section has a contract file with a producer and at least one consumer |
| D13 | Design | Conceptual design, architecture and UX artifacts carry their required diagrams as Mermaid code: capability map, context, components, data model with relationships, key interactions, deployment, user flows and navigation. Where a diagram and its text disagree, the diagram governs structure and the gap is a challenge finding |
| P1 | Plan | Each increment from G0 to MVP names the use cases it will demonstrate |
| P2 | Plan | Architecture, test and implementation backlogs trace to increments |
| P3 | Plan | Branching and CI/CD approach is written, and every gate is wired and smoke-tested |
| P4 | Plan | Operational readiness covers observability, SLOs and rollback |
| P5 | Plan | Delivery system is written and owned: hierarchy, story template, prioritization rule, cadence, track cap and metrics |
| P6 | Plan | Performance baseline is captured on a stable runner before the first increment starts |
| P7 | Plan | A session-exit check refuses to end a session with uncommitted changes or an unwritten state file. Shared-state files change only on their own lane |
| P8 | Plan | Every deployment exposes machine-readable health and version endpoints, and a seeded smoke test covers one main path per use case in scope. The version identifies the build, so a check can confirm the running build is the one shipped |
| I1 | Increment | Increment intent is signed, with acceptance criteria testable without reading code |
| I2 | Increment | Tests are committed and seen red in CI |
| I3 | Increment | Every dependency, top-level folder or cross-cutting pattern the increment introduces has an ADR |
| I4 | Increment | At least one acceptance criterion per use case in scope exercises a failure path |
| I5 | Increment | A fresh-session reader explains the code's behaviour, failures included, without seeing the intent; the explanation matches the intent |
| I6 | Increment | No new per-test skip without an expiry entry, no file-level or blanket skip, no drop in collected test count, and fixtures still validate against the schema |
| I7 | Increment | Every task carries an input manifest: the artifacts a fresh session reads to do the task. No task depends on prior conversation, and a decision made in conversation counts only once written to a named artifact |
| I8 | Increment | Every schema change in the increment is a new migration that follows the expand, migrate, contract policy. Merged migrations are never edited or deleted |
| R1 | Release | Every increment in scope has an approved validation verdict, with no open rejection |
| R2 | Release | Operational readiness is proven in the target environment by the automated post-deploy check (E13): health OK, reported version matches the build shipped, seeded smoke tests pass. Monitoring is live, SLOs measured, rollback rehearsed |
| R3 | Release | Release notes and user documentation are written and approved by the Intent Owner |

D2 and D6 together are the mechanism that answers the WorldSIM frontend question. D2 forces a frontend section to exist. D6 then asks who is qualified to author and challenge that section. With no Frontend Architect on the roster, D6 cannot be filled, and the blank row opens a crew review at the design gate.

The template does not catch concerns no row names. The backtest found one such entry in 100, a missing domain expert (NM-008), now covered by row C8. Concerns like this remain a human call, and each one found becomes a candidate floor row for the next version.

## Legibility and the unhappy path

Agents optimize toward the case they are shown, and the case they are shown is usually the happy path. WorldSIM's registry shows the cost: modules emitting events nobody consumed (NM-038), a guard that silently blocked valid analysis (NM-030), and an empty table producing a bare 422 with no diagnostic (NM-060). None of these broke the happy path, and all of them passed CI. The fix is to make failure paths a required input and legibility a tested output, so neither depends on an agent's attention.

### Failure paths as required inputs

- **Use cases carry their failure paths (C7).** Each use case lists the main path, the alternate paths and the failure paths, each with an expected outcome. An agent cannot build only the happy path when the intent it builds from names the others.
- **Each layer carries a failure-mode list (D7).** The list is fixed: missing, late, duplicate or malformed input, dependency down, partial success. Each mode needs a handling rule and a signal that makes the failure loud. A silent failure mode becomes a blank cell, and blank cells fail the gate.
- **Branching logic is drawn as a table (D8).** A decision table or state diagram exposes every combination, and an empty cell is a missing case that nobody has to notice. Prose hides the same gap.
- **Acceptance criteria include failure (I4).** At least one criterion per use case exercises a failure path, so the Verifier's tests cover the failure paths by construction.

### Legibility as a tested output

- **Explain-back check (I5).** A fresh-session reader sees only the code and writes what the code does, failure behaviour included. The Verifier compares that account with the intent. A mismatch is a finding: either the code does something unintended, or the code is too opaque to read. Both are worth knowing. WorldSIM's blind code audit is the source of this check.
- **Adversarial pass.** The Verifier runs one pass framed as "make this fail" rather than "confirm this works". Mutation testing then shows whether the tests would notice a broken branch, which also attacks the false-green class directly.
- **Complexity budget.** Lint limits branch count and function size, so logic too tangled to explain is refused before review.
- **The lead's own understanding.** At the Assured grade, the Socratic check becomes a gate. The Engineering Lead explains the architecture back before a phase gate passes. The check guards against the quiet risk that the work gets done while the human judgment behind the work stops developing.

## Delivery system: backlog to sprint

The delivery system gets its own seat. The **Delivery** seat owns the repeatable process: hierarchy, story template, refinement, prioritization rule, cadence, work-in-progress limits and metrics. The Steward audits whether the process was followed. The owner of a process never audits its own adherence. Product still owns backlog content, and the Intent Owner approves the priority order.

WorldSIM's registry shows why this needs an owner. A story cut across three tasks forced a blanket test skip that hid 16 acceptance criteria (NM-017). An issue closed with two criteria unmet (NM-043). Parallel groups ran with no concurrency ceiling and lost updates (NM-067, NM-071). A sprint branch was cut before the upstream scope was final (NM-081).

### Decomposition rules

Sizing is decided by rules that can be checked, never by a sense of complexity. WorldSIM's binary spawning rule is the model.

| Level | Unit | Traces to | Split when |
| --- | --- | --- | --- |
| Epic | One capability, for roadmap tracking only; no commits | One or more use cases | Never split by size; split by capability |
| Story | One demonstrable slice, one PR, one acceptance owner | One use case path: main, alternate or failure | More than one seat or more than one PR needed |
| Task | One seat, one session, binary done | One story | Never; a task that grows becomes a story |

Three right-sizing checks apply to every story before it is Ready:

1. **One path per story.** Failure paths get their own stories, so they are prioritized in the open instead of dropped at the end of a cycle.
2. **Independently red, independently green.** Every acceptance criterion can fail and pass without another story shipping. A criterion that must wait for another story means the story was cut wrong. This is the NM-017 lesson as a rule.
3. **Demonstrable.** The story produces an observable state named in its intent, one the Intent Owner can see.

### Story template and refinement

The story template is the Verifier's input contract, and each task under a story carries an input manifest (row I7). Each story names its user and use case path ID, the observable outcome, acceptance criteria in given, when, then form with at least one failure case, the NFRs it touches, its ADR references and dependencies, and its owning seat.

Refinement is a written step with the four duties. Product authors the story. The Verifier challenges testability, the Builder challenges size and feasibility, and the Architect confirms ADR prerequisites. A story leaves refinement Ready only when rows I1 to I5 of the Definition of Ready can be met. Any consuming seat may reject a story that breaks the template, citing the clause.

### Prioritization rule

The order follows a written rule, and every change to the order is logged:

1. Stories that test a business-case assumption or a kill boundary come first. The cheapest time to learn the case is wrong is the first cycle.
2. Enablers that unblock other stories, especially architecture work, come next.
3. Remaining stories are ordered by value per use case, using weighted shortest job first where estimates exist.

### Staggered tracks

*[Diagram in the live document: illustrative staggered tracks · 1 discovery track, 2 delivery tracks, 4 cycles]*

Discovery and architecture for the next body of work runs while delivery builds the current one. Track B stays empty until Epic 2 is baselined, even if capacity is free.

- A delivery track pulls only stories whose upstream artifacts are baselined. Scope locks before a branch is cut.
- The number of parallel delivery tracks is capped in the constitution. Each track runs in its own branch lane and worktrees.
- The discovery track aims to stay one cycle ahead, and the gap between the two tracks is itself a metric.

### Cycle planning and execution

- **Entry:** every pulled story is Ready, capacity is stated in sessions, and the track cap holds.
- **During:** new work enters only through the backlog. A scope change mid-cycle is a logged decision by the Intent Owner.
- **Exit:** stories count as done when validated, not when closed. Unfinished stories return to the backlog with a note on why.

### Metrics

The Delivery seat owns the metrics, but they are computed from the repository and never self-reported. The Steward reviews them at each cycle exit.

| Measure | What it shows | Direction |
| --- | --- | --- |
| Cycle time, Ready to validated | Flow speed | Down, with no rise in rejections |
| Stories validated vs planned | Predictability | Near 1.0 |
| Stories split after Ready | Refinement quality | Near zero |
| Input-contract rejections per story | Template clarity | Down over time |
| Stories blocked by another story | Decomposition quality | Near zero |
| Rejections at Validate | Intent-to-build fidelity | Near zero |
| Skipped or no-op tests | False-green exposure | Zero, enforced by CI |
| Ready backlog ahead of delivery, in cycles | Discovery lead | At least 1 |
| Agent sessions per validated story | Cost of the method | Tracked, not targeted |

No single measure is a target on its own. Cycle time alone rewards cutting corners, which is why each measure is paired with a quality measure in the same review.

## Quality engineering standard

Testing was the thinnest part of this draft, and the most dangerous gap. False green, contract drift and environment issues together account for 48 of WorldSIM's 100 near-misses. WorldSIM's own testing strategy listed API contract, UI, performance and security testing as "planned" domains while near-misses accumulated in exactly those areas. The appliance treats quality engineering as a floor requirement, not a later module.

### Test levels

The appliance fixes the levels and their purpose. The tools are defaults a project confirms or replaces by ADR (row D9), so the appliance stays stack-neutral.

| Level | Proves | Default tooling | Runs | Author | Challenger |
| --- | --- | --- | --- | --- | --- |
| Unit | Logic, including every decision-table cell | Stack native, such as pytest or Vitest | Pre-push | Builder | Verifier, via mutation score |
| Contract | Producer and consumer agree on every exchanged shape; mocks are generated from the contract | Schema-first API spec, with Schemathesis or Pact | Pre-push and CI | Verifier, against the Architect's contract | Architect |
| Integration | Components work against real dependencies | Testcontainers with a real database | CI | Verifier | Builder |
| End to end | Each use case path works through the real interface | Playwright | CI on every PR; full suite nightly | Verifier | Designer, for user-facing paths |
| Performance | NFR load levels: low, average, high and stress | k6 or Locust | Dedicated runner, nightly and before release | Verifier | Operator |
| Security | Code, dependency and runtime weaknesses | SAST, dependency scan, DAST | CI and before release | Operator | Architect |
| Accessibility and visual, if a UI exists | Legibility and layout at declared viewports | axe, screenshot comparison | CI | Verifier | Designer |

### Test data ownership

The Verifier owns the test data standard. The Architect owns the schema it must match, and the Operator owns the classification rule. Five rules follow from the registry:

1. Fixtures are generated from the schema, and CI validates them against the schema. Hand-written mocks with guessed field names caused NM-051 and NM-086.
2. No production personal data in any test environment. Synthetic data is the default.
3. Each environment declares its seed. Tests check the seed at start and fail loudly if data is missing, instead of skipping quietly (NM-097).
4. Tests run in random order and pass in isolation. A test that passes only in the full suite is a defect (NM-099).
5. Fixture changes are reviewed by the Verifier, because a fixture is shared input for many tests.

### Craft rules that close the false-green class

- **Skips expire.** A skip or fixme applies to one test, never a file, and needs a registry entry with an owner and an expiry date. Blanket skips hide a decomposition fault and are banned (NM-018). A strict expected-fail used for red-first tests is not a skip (rule 2). CI fails on an expired entry (NM-064, NM-065).
- **The collected-test count cannot fall silently.** CI compares tests collected against tests present. Seventeen files went undiscovered for five milestones in WorldSIM (NM-078).
- **No pass on timeout.** A guard that passes when its wait times out is forbidden (NM-047, NM-061).
- **Selectors are a contract.** Test IDs live in a component contract file, and a rename is checked across the whole test corpus (NM-039, NM-062, NM-076).
- **Performance is relative to a baseline.** Baselines are captured before the first increment on a stable runner (row P6). Thresholds compare with the baseline, never with a shared runner's absolute numbers (NM-020, NM-059, NM-064).
- **One source for environment settings.** Viewport, configuration and migration state come from one file, and CI checks parity (NM-032, NM-049).
- **Flaky tests are quarantined, not ignored.** A quarantined test has an owner and an expiry, and the quarantine count is a metric.
- **Every executable file is linted.** Scripts, configuration and test files get the same syntax check as application code (NM-041).

### Quality metrics

These join the delivery metrics and are computed the same way: collected-test count per cycle, mutation score, flaky rate, active skips past expiry (target zero), contract tests per data exchange (target full coverage), and performance against baseline at each NFR load level.

## Data discipline (added in v0.2)

The baseline left data to the Architect seat and a few floor rows. That covered ownership of the data layer but not how data changes, moves or is trusted. Ten WorldSIM near-misses sit in that gap: guessed field names (NM-003), a schema with no owner (NM-011), a copy path missing a required column (NM-036), events with no consumer (NM-038, NM-090), registries that disagreed with code (NM-091), a migration never applied (NM-049), mocks with wrong field names (NM-051, NM-086), and missing seed data behind a silent error (NM-060, NM-097).

Five draft standards now ship in `docs/standards/data/`: schema change policy, data contracts, data quality, reference and seed data, and data governance. Each project adapts them at bootstrap. Floor row D11 requires each one approved or signed not-applicable. D12 requires a contract file for every exchange in the architecture. I8 requires every schema change to be a new migration.

Two checks enforce what a machine can see. E14 refuses a contract with no consumer, a missing producer, or an incomplete schema. E15 refuses any edit, deletion or rename of a merged migration, and fails rather than skips when it cannot find the base to compare against.

A Data Architect seat is chartered but not held by default. The seat check refuses any artifact that names it until a role proposal adopts it. Five written triggers say when to raise that proposal, so the question comes before the first schema mistake rather than after it.

## Diagrams as the contract for structure

In WorldSIM, architecture decisions written as prose were read several ways at implementation time (Engineering Lead's account). Prose hides master-detail, hierarchy and sum-of-parts relationships that a picture shows at once. An entity relationship can be read only one way.

Conceptual design, architecture and UX artifacts now carry required diagrams, written as Mermaid code inside the artifact. Code rather than images, because GitHub renders it, agents read and write it, pull requests show exactly which entity or arrow moved, and a check can parse it.

| Artifact | Required diagrams |
| --- | --- |
| Conceptual design | Capability map |
| Architecture | Context, components, data model (erDiagram), key interactions (sequenceDiagram), deployment |
| UX design | User flows, navigation |
| Any artifact with stateful logic | States (stateDiagram), when used |

Floor row D13 makes the diagrams part of the design gate, and says the diagram governs structure when it and the text disagree. Check E16 refuses an artifact in review or approved when a required diagram is missing, uses the wrong form, or has no parts and links worth reading. A diagram that does not apply is declared not-applicable with a reason and an approver. Templates ship with tagged starter diagrams, so an artifact starts from a picture rather than a blank.

E16 sees presence and shape, not correctness. Whether the diagram matches the text and the code is the challenger's call. A later check can cross-reference data-model entities with the schema, and component links with contract files.

## Elastic crew: how the team grows and shrinks

In WorldSIM, every new role arrived after damage. The Frontend Architect came after UI decisions failed to scale, and the DevSecOps role came after repeated build failures and lost commits. Both times, the Engineering Lead was the only detector. The appliance moves detection into the process, makes proposals a written artifact any seat can author, and leaves the Engineering Lead as the approver.

### Three triggers that open a crew review

1. **Definition of Ready seat gap (anticipatory).** The DoR template requires a section per architecture layer, and each section needs an author seat and a different challenger seat. A required section with no qualified seat is a role gap by construction. This is where the Frontend Architect would have appeared, at the design gate rather than after the damage.
2. **Unowned decision (reactive).** CI fails a PR that adds a dependency, a top-level folder or a cross-cutting pattern without an ADR reference. The Steward logs each such failure; repeated failures in one layer point to a missing seat.
3. **Registry cluster (systemic).** Three or more registry entries of one hazard class in a cycle open a review. The DevSecOps role would have appeared here.

A challenger can also open a review by declaring an artifact outside its competence. That declaration is a finding, not a failure.

### Role, rule or tool

The first question in every review is whether a new agent is the right answer at all. WorldSIM's lost commits were finally closed by git hooks and worktree rules (NM-070, NM-092), not by an agent. A role is justified only when the gap needs judgment. A repeatable check becomes a tool or a gate instead.

| Gap needs | Answer | Example |
| --- | --- | --- |
| Judgment on decisions nobody owns | New role | UI architecture for a growing module set |
| A fixed check applied every time | Tool or gate | Pre-push hooks, required checks |
| A standard people keep forgetting | Rule in the constitution, enforced by a check | Canonical artifact locations |
| Expertise for one phase only | Surge role, time-boxed | Security review before first release |

### The role proposal artifact

A proposal follows the same four duties as any other artifact. Any seat or the Steward can author; a different seat challenges on the role, rule or tool test and on overlap with the roster; the Engineering Lead approves. The Intent Owner also approves when the added cost touches the business case.

Every proposal states:

- the evidence: registry IDs, challenger findings or the unowned decision
- why a rule or tool will not close the gap
- the type: standing, surge with an end date, or advisory (consulted only)
- the cost in sessions per cycle
- the success measure and the review date
- the job description, in front matter so a check can read it:
  - the **trigger** that puts the seat to work
  - the **inputs**, each with the artifact and the seat that supplies it
  - the **value**: what the seat does with the inputs that no other seat does
  - the **outputs**, each with the seat that consumes it and the acceptance test that
    consumer applies
  - the **standards and templates** it follows
  - an independent **verifier**: a seat other than the author, the proposed seat and the
    author's holder, with the evidence it inspects to confirm the seat follows its own
    process
- a **peer review**: the seats that send it input, consume its output or give up work to it
  each recommend accept, accept with conditions or reject, and say what they would hand
  over or take, with evidence. The group's recommendation is no more favourable than its
  least favourable member.

The peer review is how demand is shown. A seat that no peer would feed or consume has no
demand. The Engineering Lead reads the peer recommendation before approving, and approves
or declines for the concerns the peers cannot judge: cost, overlap and governance. Check
E17 enforces that the job description is complete and the review independent. It does not
judge whether either is right. That stays with the peers, the challenger and the
Engineering Lead.

### A job description is mandatory for every seat

WorldSIM's convention carries over: no seat exists without a written job description.
This covers the human seats, the Steward and optional seats, not only new proposals. Each
seat in `docs/roles.yml` has a `job` block with the same lines a proposal states, and E17
refuses a roster in which any seat lacks one, names a phantom seat as a sender or
consumer, cites a standard or template that does not exist, or has a verifier on the
seat's own holder.

Two sources keep the descriptions honest. The artifact register above says who authors,
challenges and approves each artifact, so a seat's outputs and verifier follow from it
and cannot contradict it. A project's bootstrap challenge reviews every job description
against the product, and a seat added later passes the peer review. When a proposal is
approved, its charter is copied into the roles file unchanged, and E17 refuses a roster
whose job differs from the approved charter.

The core descriptions are drafts for the Intent Owner and Engineering Lead, written from
the register and the floor. They have not been through peer review as proposals. Peers
should challenge them the first time a project runs a crew review.

### Retirement keeps the crew honest

At each cycle exit, the Steward lists roles that were not activated or whose trigger stopped firing. Each listed role gets a keep or retire decision, with the same approval path as a new role. Surge roles retire on their end date unless renewed in writing. The roster also carries a size budget set in the constitution; a proposal that exceeds the budget must name a role to merge or retire.

*[Diagram in the live document: proposed role lifecycle · 1 test, 2 outcomes, retirement at cycle exit]*

The Engineering Lead appears once in this flow, as the signature on a proposal someone else wrote and someone else challenged.

## Evidence plan: the seat-swap drill

The worker-agnostic claim holds only if any doing seat can change hands mid-stream with the repository as the sole briefing. Accountable seats, the Intent Owner and the business approvers, stay human and are outside the claim.

Agent-to-agent handoff is tested continuously at no extra cost. Every fresh session is a cold start. The Steward logs each clarification a fresh session asks for, and each one traces to an artifact that failed its input contract. The rare and expensive test is a human cold start, which needs a deliberate drill.

| Drill | How cold | What it proves | Cost |
| --- | --- | --- | --- |
| Fresh agent session | Fully cold | Artifacts are explicit enough for an agent | None; runs every session |
| Engineering Lead takes a seat he did not author, such as Verifier on an agent-built module | Warm: knows the method, not the module | Artifacts are sized and legible for a human reader | A few hours |
| A new human contributor takes a doing seat with no briefing | Fully cold | The full claim, human side | Contributor time, on a second instance |

The Engineering Lead drill carries a disclosure, in the same spirit as the single-principal rule. The drill is not independent, because the author of the method is running it. The result is still useful evidence on artifact size and legibility.

The primary measure is whether the newcomer's output passes verify and challenge on first submission, because a cold reader does not ask about what it cannot see is missing. Time to first useful output comes second. Questions asked are logged against the artifact that should have answered them, as a supporting signal. Predictions for these measures are written before the drill, so the gap is measured rather than described.

## Backtest against WorldSIM

Two backtests replayed all 100 WorldSIM near-misses against the draft. The author's pass counted 66 as mechanical. A blind challenger counted 19, because it required each check to be named rather than intended. Under rule 4 the challenger's standard is the right one. Checks E1 to E12 now name the missing mechanisms, and the challenger estimated they would raise the count to about 60. Neither figure counts checks that exist; none are built yet.

*[Diagram in the live document: WorldSIM near-miss registry NM-001 to NM-100; author pass and blind challenger pass, 2026-09-30, both before checks E1 to E12 were added]*

The two passes agree on 29 entries. The largest disagreement is 48 entries the author called mechanical and the challenger called partial: the same rule, judged by a different standard of proof. Seven entries the challenger called mechanical were gaps the author had closed after the first pass, which independently confirms those fixes. Both classifications are in [backtest-round-1.md](backtest-round-1.md). The challenge findings and their dispositions are in [challenge-round-1.md](challenge-round-1.md).

### Gaps found in the author's pass, and the fixes made

| Gap | Entries | Fix in this draft |
| --- | --- | --- |
| Work left uncommitted or state left unwritten at session end | NM-014, 055, 089, 093, 100 | Floor row P7: session-exit check and shared-state lane |
| Consultation after drafting, not before | NM-005, 009, 013, 018 | New Consulted duty: independent cold input before the author drafts, panel chosen by root-cause domain |
| Artifact location, naming and stale references | NM-002, 022, 023, 031 | CI checks location and name by type, and that every reference resolves |
| Child approved before its parents | NM-072 | CI refuses approval out of order |
| Domain expertise and experience intent unowned | NM-008, 010 | Floor row C8; D4 now requires experience intent |
| Scripts outside the lint gate | NM-041 | Craft rule: every executable file is linted |
| Demo ownership | NM-025 | Left to the optional demo module and crew review |

The nine seat-judgment entries depend on how well a challenger or explain-back reader does the job. The seven stack-specific entries are tool quirks no floor can anticipate; the registry is the right home for those, as known issues.

## Setup sequence and first-run checklist

The order matters. Ownership and enforcement come before any agent writes code, because WorldSIM added both after the fact and paid for the retrofit.

1. Start from the appliance template repository, pinned to a floor version. The template carries the constitution, roles and artifact templates, the Definition of Ready as a machine-readable checklist with IDs, and the CI checks as scripts.
2. Create one Git identity per agent seat holder, then create the repository with rulesets on every branch pattern, admins included, starting with `main` and required checks turned on.
3. Name the Intent Owner and Engineering Lead. Record the single-principal disclosure if one person holds both.
4. A bootstrap session fills the constitution slots, `docs/roles.md` with the matching `CODEOWNERS`, and the autonomy setting for merges.
5. A fresh session challenges the bootstrap output against the floor, and the Engineering Lead approves. The bootstrap author never approves its own setup.
6. Install the hooks and checks shipped in the template, including the session-exit check.
7. Run a smoke cycle on a trivial intent, inside a worktree. Confirm each gate refuses when its condition is missing. The same canary then runs every cycle (E6).

The first cycle builds no product code. Cycle 1 is setup, the smoke cycle and the discovery track: intent, business case, users and use cases, worked through with the Intent Owner. Delivery starts once the case and design gates pass and there is baselined work to pull.

Day-one checklist:

- [ ] Intent Owner and Engineering Lead named in `docs/roles.md`
- [ ] `CODEOWNERS` matches the roles file
- [ ] One identity per agent seat holder, with rulesets and required checks active on every lane, including `main`
- [ ] Hooks installed and seen to block a bad push
- [ ] A deliberately skipped test fails the build
- [ ] First intent signed, with a kill criterion
- [ ] Tests for the first intent seen red in CI before any code
- [ ] Registry holds its first entry, even if anticipatory

The smoke cycle is the step most likely to be skipped. It is also the only proof that the gates enforce anything. WorldSIM's own registry shows gates that looked active for several milestones and were not.

## Open questions for the next session

- Once checks E1 to E12 exist in the template repository, a second blind backtest should confirm the Mechanical count rises as predicted. Which agent harnesses can host the E7 hooks is also open.
- What is the default autonomy setting for merges? WorldSIM moved from human merge to auto-merge on release branches. The appliance needs one sane default.
- Agent-specific controls are not yet in the floor: least-privilege tool permissions per seat, prompt injection through repository content, and a policy for when the underlying model version changes.
- An outside taxonomy check found areas not yet covered: secrets management, incident response after launch, data migration and dependency licensing.
- Floor governance across instances is open: who approves a floor change, and how a project upgrades its pinned version.
- Transfer evidence for a second instance needs predictions written before that build starts, for both the bootstrap dry run and the seat-swap drill.
