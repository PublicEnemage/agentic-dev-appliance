# Backtest, round 1

Two classifications of WorldSIM's 100 near-misses. The author's pass credited stated rules; the blind challenger's pass required a named check, and chose the weaker label when unsure. They agree on 29 entries. The author's own rule-or-gap notes are superseded by the challenger's, shown here.

| Entry | What happened | Author label | Challenger label | Challenger's rule or gap |
| --- | --- | --- | --- | --- |
| NM-001 | Recency Bias Creating Scope Spiral | Seat judgment | Partial | Cycle "new work enters only through the backlog"; no check enforces it |
| NM-002 | Silent Artifact Placement in Wrong Directory | Partial | Mechanical | Traceability: CI checks location and file name against type |
| NM-003 | Field Name Assumptions Without Reading the Schema | Mechanical | Partial | D9 contract tests and Builder-not-acceptance-author; contract coverage is a metric, not a gate |
| NM-004 | Smoke Testing Not Institutionalized After Discovering Its Value | Mechanical | Partial | Rule 7 redesign; nothing checks that a discovered practice reaches CI |
| NM-005 | Agent Consultation Was Confirmatory, Not Generative | Partial | Partial | Five duties: consulted before author; no evidence of ordering is checked |
| NM-006 | ADR Panel Omitted the Implementing Agent | Mechanical | Partial | Register names Builder as architecture challenger; CI does not check front-matter seats against the register |
| NM-007 | Schema Files Committed Without Data Architect Review | Mechanical | Partial | Rule 5 CODEOWNERS; collapses under one GitHub identity (WorldSIM's own CODEOWNERS says so) |
| NM-008 | Domain Expertise Gap: No Real-World Economist in the Room | Not covered | Mechanical | C8 domain knowledge needs a qualified challenger seat |
| NM-009 | Groupthink Risk: No Counter-Perspective in the Council | Partial | Mechanical | C8 counter-perspective where judgment is contested |
| NM-010 | UX North Star Had No Owner | Partial | Mechanical | D4 experience intent; D6 author and challenger seat |
| NM-011 | Schema Had No Owner: Data Architect Role Created | Mechanical | Mechanical | D2 data section; D6 seat |
| NM-012 | Matrix Compute Needed a Different Knowledge Profile | Seat judgment | Seat judgment | D2 layer list has no domain or compute-core layer, so D6 never asks; only a challenger declaring itself unqualified |
| NM-013 | The DIC Had Never Been Asked the Foundational Question | Partial | Seat judgment | Business case cold review; no row requires evidence from real users |
| NM-014 | File Edit Reported as Complete Without Commit | Partial | Partial | P7 fires only at session exit; mid-session false "done" is unchecked |
| NM-015 | CI Gate Job Not a Required Status Check | Mechanical | Partial | P3 smoke test once at setup; no re-audit when the workflow graph changes |
| NM-016 | Lint Gate Absent from Agent Prompts: Two PRs Failed CI on Trivially-Preventable Errors | Mechanical | Mechanical | Rule 4: pre-push hook |
| NM-017 | Story–Test–Implementation Decomposition Mismatch: 16 ACs Suppressed by Blanket Skip | Mechanical | Partial | Right-sizing check 2 is a refinement judgment; I6 still allows a blanket skip that has an expiry entry |
| NM-018 | Hammer-Nail: Technical Panel Produced Engineering Solutions to a Process Problem | Partial | Seat judgment | Five duties: consulted set by root-cause domain |
| NM-019 | Named Deliverables Invisible on the Board for an Entire Milestone | Mechanical | Partial | Traceability runs child to parent; nothing checks that every named commitment has a work item |
| NM-020 | Phase 1 Baseline Benchmarks Never Tracked: Backend Compute Latency Gap Before Matrix… | Mechanical | Partial | P6 covers only the baseline before the first increment; later prerequisite measurements are untracked |
| NM-021 | File Authority Rule Not Applied Under EXECUTE Task Pressure: Two PRs Wrote to Unowned… | Mechanical | Partial | CODEOWNERS identity gap; registry ordering unchecked |
| NM-022 | No Standing Process for Detecting Stale Cross-References in Authoritative Documents | Partial | Partial | Live-ID check passes a reference to a live but wrong ID; header-vs-table contradictions unchecked |
| NM-023 | CONTRIBUTING.md "Branch from develop" Stale Instruction | Partial | Not covered | No check on content staleness outside the artifact chain |
| NM-024 | Playwright Sequence Phases 3–4 Not CI-Enforceable | Mechanical | Partial | Rule 4 labels the gate advisory but does not close it |
| NM-025 | Demo Story Ownership Gap | Partial | Partial | Demo standard is an opt-in module; P1 asks only for "demonstrable" |
| NM-026 | Issue Closed as Completed Without Delivery: #514 Phase 1 Benchmark | Mechanical | Partial | "Done when validated" stated; nothing ties issue closure to evidence |
| NM-027 | Performance Tests Silently No-Op: AC-007 and AC-008 Measured Nothing for One Milestone | Mechanical | Partial | I2 "seen red" is per increment, not per test ID; a guarded no-op beside red tests passes |
| NM-028 | IR-004 Trajectory Tick Year Test Was a Silent No-Op for One Milestone | Mechanical | Partial | "No pass on timeout" is a craft rule with no lint or check named |
| NM-029 | GovernanceModule Event_Type Contract: Unit Tests Provided False Positive Coverage | Mechanical | Partial | D9 contract tests required; coverage tracked as a metric only |
| NM-030 | EcologicalModule Temporal Guard Silently Blocked Retroactive CO2 Proximity Analysis | Seat judgment | Seat judgment | Domain rule; D7 loud signal works only if someone lists this mode |
| NM-031 | Demo Review Files Named with Descriptive Suffixes Instead of Canonical Convention | Partial | Mechanical | CI file-name check |
| NM-032 | Demo Screenshot Capture Viewport (1280×720) Mismatches Live Demo and Legibility Gate… | Mechanical | Mechanical | Craft rule: one source for viewport with CI parity check |
| NM-033 | Usability Session Coordinator Broke Observer-Silence Rule During Cold-Start Session | Stack-specific | Not covered | No usability-session protocol in scope |
| NM-034 | PM Agent / Coordinator Filed Near-Miss Registry Entries Without PI Agent Activation | Mechanical | Partial | Steward-files-registry pair; CODEOWNERS identity gap |
| NM-035 | CI Workflow Not Triggered for PRs Targeting Release Branches | Mechanical | Partial | Setup protects only `main`; new branch patterns not re-audited |
| NM-036 | Branch Snapshot Copy Omitted ia1_disclosure — NOT NULL Violation in Mode 3 Golden Path | Mechanical | Seat judgment | Verifier integration coverage of a secondary write path |
| NM-037 | Demo Script Pool Initialization Gap: ASGITransport Does Not Trigger Lifespan | Stack-specific | Stack-specific | Framework quirk |
| NM-038 | ExternalSectorModule Emitted Events With No Consumer: Reserves and Unemployment Frozen | Mechanical | Seat judgment | Needs someone to name the downstream effect in a use case; I5 explain-back |
| NM-039 | demo-narrated.spec.ts Used Non-Existent testid as App-Ready Sentinel | Mechanical | Partial | Selector contract file; no check that every locator exists in the contract |
| NM-040 | playwright.demo.config.ts Had No testMatch Guard; Pattern Invocation Triggered… | Stack-specific | Stack-specific | Playwright config quirk |
| NM-041 | demo.sh Syntax Error Undetected Through Full Milestone Lifecycle; Blocked Post-Closure… | Partial | Mechanical | Craft rule: every executable file is linted |
| NM-042 | Agent Generated UX Designer Sign-Off Without Independent Review; EL Caught It Before… | Mechanical | Partial | Seat in front matter is self-declared; one session can write another seat's approval |
| NM-043 | G4 Sprint Closed Issue #27 in Session State With Two ACs Unsatisfied; Caught at M13… | Mechanical | Partial | One story, one PR; no AC-to-test mapping check |
| NM-044 | G7 and G8b Implementation Changed Observable Zone 1B and Mode Indicator State;… | Mechanical | Partial | E2E runs in CI, but branch protection covers only `main` |
| NM-045 | AC-3 E2E Test Passed on Generic Regex Fallback; Source Citation Field Name Mismatch… | Mechanical | Seat judgment | Assertion strength; mutation testing is specified for unit tests only |
| NM-046 | Stale Vite Module Cache in Docker Container Masked G4 Fix During Post-Sprint EL… | Stack-specific | Stack-specific | Tooling quirk |
| NM-047 | G5 Playwright AC-3 Test Timing-Dependent; n_steps/step_index Mismatch Passed CI Due to… | Mechanical | Partial | "No pass on timeout"; unenforced |
| NM-048 | G5 AC-2 Test Read annotation.textContent() Before data-quality Fetch Completed; Source… | Seat judgment | Partial | Same guard class; the race itself is test craft |
| NM-049 | Docker Dev DB Migration Lag: Alembic Migration Not Applied to Persistent Dev Stack… | Mechanical | Partial | CI parity check cannot see the local stack where validation ran |
| NM-050 | Step 6c Audience Simulation Run Before Step 7 IR Review; Simulation Also Conducted… | Stack-specific | Partial | Sequence lives in the opt-in demo module; parent-before-child CI applies only to register artifacts |
| NM-051 | QA Test Mock Used Wrong Field Names (alert_id/indicator_id vs mda_id/indicator_key);… | Mechanical | Mechanical | Test data rule 1: fixtures generated from schema, CI-validated |
| NM-052 | Pre-Push mypy Gate Non-Executable Locally: No Python 3.13 Venv with Deps; Gate… | Mechanical | Partial | Hooks "seen to block" once at setup; no recurring canary |
| NM-053 | CM Sign-Off Artifact Filed Post-Implementation: Component 3 Gate Bypassed | Mechanical | Partial | Parent-before-child CI, but approval status is self-asserted front matter |
| NM-054 | UI Contract Change (select → combobox) Broke Six Existing E2E Tests; Not Caught Pre-Push | Mechanical | Mechanical | E2E required check (CI caught it as designed) |
| NM-055 | G4 QA Test Files and Process Documents Not Committed in Implementation PRs | Partial | Partial | I2 has no story-to-test-ID link; CI cannot see an absent file |
| NM-056 | E2E Test Soft-Skipping Masked a Mock Bug; Backend Startup Failure Made Coverage Appear… | Mechanical | Partial | Test data rule 3 "fail loudly" unenforced; `if (!x) return` is invisible to skip counts |
| NM-057 | CA-Condition Follow-Up Issues Not Assigned to a Sprint Group at Sprint Exit Time | Seat judgment | Partial | Backlog-only rule; no check |
| NM-058 | AC-009 Testid Mismatch: Mode 3 Performance Gate Silent No-Op Since M12 | Mechanical | Partial | Selector contract; check unnamed |
| NM-059 | AC-009 CI Measurement Methodology: Multi-CDP Round-Trip Contaminates Performance Window | Mechanical | Stack-specific | Measurement method quirk; dedicated runner mitigates |
| NM-060 | Startup Observability Gap: Empty simulation_entities Table Produces Silent 422 with No… | Mechanical | Partial | D7 and P4 require loud signals; nothing tests startup with an empty seed |
| NM-061 | AC-F8 Silent No-Op: Scenario Created via API But Never Selected in UI; 60-Second… | Mechanical | Partial | Catch-to-false guard; "no pass on timeout" unenforced |
| NM-062 | Demo Spec getByText("Step N") Collides with Projection Panel Step Axis Spans; Every… | Mechanical | Partial | Selector contract implies testid locators; unenforced |
| NM-063 | CohortImpactSection Text Overflow Not Covered by Legibility Spec; Same Gap Class as NM-056 | Mechanical | Seat judgment | Designer challenge or visual baseline approval |
| NM-064 | AC-009 Performance Test Consistently Exceeds 200ms Threshold on GHA Shared Runners;… | Mechanical | Mechanical | P6 baseline plus dedicated performance runner |
| NM-065 | No SOP for Intentionally-Red Pre-Implementation QA Tests; Ad-Hoc Resolution Required | Mechanical | Partial | I2 mandates red-first but gives no way for red tests to coexist with required green checks |
| NM-066 | SESSION_STATE.md Exceeds Claude Code Read Ceiling; Session Continuity Guarantee… | Mechanical | Partial | STATE.md is "capped" with no check named; by Rule 4 that is advisory |
| NM-067 | No Sprint Group Isolation Protocol for Parallel Workstreams; Unregulated Release… | Mechanical | Partial | Track cap and shared-state lane stated; no check |
| NM-068 | Prior NM Process Improvements Not Verified at Sprint Entry; NM-027 Pattern Class Has… | Seat judgment | Partial | Rule 7 recheck is a principle with no mechanism |
| NM-069 | Gitignore Missing Playwright and Test Artifact Directories; Accidental Staging Would… | Stack-specific | Not covered | No repository hygiene rule |
| NM-070 | Pre-Push Gates Enforced by Documentation Only; No Git Hook Enforcement; Gates… | Mechanical | Mechanical | Rule 4; day-one "hooks seen to block a bad push" |
| NM-071 | No Sprint Group Concurrency Ceiling at Sprint Planning; Unbounded Parallelism Upstream… | Mechanical | Partial | Track cap in constitution; no check |
| NM-072 | Artifact 5 (Scope Decision Gate) Authored and EL-Approved Before Prerequisite Design… | Partial | Mechanical | CI: child cannot be approved before its parents |
| NM-073 | Sprint Sub-Branches Have No Required CI Checks; Auto-Merge Fires Before Playwright E2E… | Mechanical | Partial | Protection scope is `main` only |
| NM-074 | Required Check Added to Ruleset Without Verifying Workflow Trigger Coverage;… | Mechanical | Partial | Smoke test confirms gates refuse, not that each check reports on each lane |
| NM-075 | Multiple Claude Code Sessions Sharing One Git Working Tree; Branch Switches from Other… | Mechanical | Partial | Rule 3 says "hook-enforced" but names no hook; git has none that fires on another process's checkout |
| NM-076 | Testid Renames in G4 Implementation Not Cross-Checked Against Full E2E Corpus; Three… | Mechanical | Partial | Rename check unnamed; lane unprotected |
| NM-077 | gh pr create Infers Head Branch from Shell CWD, Not Worktree Branch; PR Created with… | Stack-specific | Stack-specific | CLI quirk |
| NM-078 | Milestone Test Files in tests/ Root Never Discovered by CI; 17 Files Silently Excluded… | Mechanical | Mechanical | I6 and craft rule: collected count compared with tests present |
| NM-079 | G1 CI Bands Implementation Committed to G3 Feature Branch; Wrong-Branch Commit Not… | Mechanical | Partial | Worktree-per-agent lowers risk; no branch-identity check before commit |
| NM-080 | Admin-Rights Direct Commit to release/m18; release-branch-ci-gate Ruleset Does Not… | Mechanical | Partial | No push restriction for admins or non-main branches |
| NM-081 | Sprint Branch Cut Before Predecessor ADR Scope Was Finalized on release/m18; G3… | Mechanical | Partial | "Scope locks before a branch is cut" stated; no rule invalidates approved children when a parent changes |
| NM-082 | CI Band Fill Geometry Incorrect in TrajectoryView.tsx; Shipped in G1 With Tests Green;… | Seat judgment | Seat judgment | Geometric invariant test; visual review |
| NM-083 | Demo-Spec ↔ Component-Contract Integration Gap: Seven CRITICAL Step 6b Findings Had No… | Mechanical | Seat judgment | Verifier writing contract-level assertions |
| NM-084 | CM Sign-Off Obtained After Feature PRs Opened; Auto-Merge Could Have Fired Before… | Mechanical | Partial | A required review blocks auto-merge only with a distinct reviewer identity |
| NM-085 | Co-Dependent Fixture PRs Produce Transient Cross-Test Failure; Pattern Not Documented… | Mechanical | Partial | "Independently red and green" rule; red-first plus required checks would deadlock |
| NM-086 | E2E Mock Route Not Verified Against api_contracts.yml; CI Caught Contract Mismatch… | Mechanical | Mechanical | Contract level: mocks generated from the contract |
| NM-087 | Agent Used git stash --include-untracked as Recovery Action; Stashed EL In-Progress… | Mechanical | Partial | "No stash; hook-enforced", but git has no stash hook |
| NM-088 | Parallel Claude Code Sessions Share Main Working Tree; Branch Displacement Causes Lost… | Mechanical | Partial | Same as NM-075 |
| NM-089 | Shared-State File Changes Lost on Branch Switch; Session Summary Permanent Artifact… | Partial | Partial | P7 fires at session exit only; mid-session branch switch uncovered |
| NM-090 | DemographicModule Has Two Additional Dead Event Subscriptions Beyond capital_controls;… | Mechanical | Partial | D9 contract tests; no emitted-vs-subscribed check |
| NM-091 | EmergencyInstrument Enum Has 7 Variants; ADR-020 Canonical Registry Listed 10; 3… | Seat judgment | Seat judgment | Live-ID check covers document IDs, not code identifiers |
| NM-092 | Pre-Push Hook Uses CWD-Relative Paths; venv and node_modules Not Found in Linked… | Mechanical | Partial | No recurring canary; Rule 3 worktrees caused the break |
| NM-093 | chore/m19-state-sync-025 Accumulated Sprint Implementation Commits; Shared-State Lane… | Partial | Partial | Lane rule stated one way and unenforced |
| NM-094 | G2C QA Test File (1394 Lines) Missing from release/m19 After Sprint Confirmation;… | Mechanical | Partial | No check that a story's tests reach the target branch; collected count never rose |
| NM-095 | #1657 QA Tests Authored in Same PR as Implementation; RED-Before State Observed Only… | Mechanical | Mechanical | I2 tests seen red in CI before implementation |
| NM-096 | #1657 Elasticity Rows Not Added; NM-090 Hazard Partially Unresolved; Two G6 Tests Skip… | Mechanical | Mechanical | I6: new skip without expiry entry fails the build |
| NM-097 | CM Sprint A/B/C MAGNITUDE Tests Run Against Under-Seeded CI Database; Skip Guard… | Mechanical | Partial | Seed check rule unenforced; no rule for non-required job health |
| NM-098 | _classify_direction Accepts primary_indicator Parameter but Never Uses It; CM AC-1… | Seat judgment | Seat judgment | I5 explain-back; unused-argument lint not named |
| NM-099 | asgi_client Fixture in test_m19_cm_b Does Not Initialise asyncpg Pool; Test Fails in… | Mechanical | Mechanical | Test data rule 4: random order, pass in isolation |
| NM-100 | AEA Agent Definition Not Committed Before PR Opened; Session Ended Mid-Task With… | Partial | Partial | P7 cannot fire on context exhaustion; no PR-description-vs-diff check |
