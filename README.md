# Agentic Development Appliance

A template for governed agentic software development. Humans and agents hold seats. Every
piece of work traces back through written, challenged and approved artifacts to a business
case. Checks enforce the rules, so the process holds whoever, or whatever, does the work.

The method was harvested from [WorldSIM](https://github.com/PublicEnemage/worldsim) and its
100-entry near-miss registry. The design rationale is in
[docs/method/appliance-design.md](docs/method/appliance-design.md).

## Status: v0.1 baseline, with the v0.2 data discipline

v0.1 ships the templates and the checks that read files. Rules that need identities,
harness hooks or CI history are still advisory, and each names the check that will replace
it. A rule without a running check is a suggestion, so the status of every check is public:

| Check | Enforces | v0.1 |
| --- | --- | --- |
| E10 | Front matter, trace, location, naming, approval order, staleness | Implemented |
| SEATS | Author, challenger and approver on different seats and holders; D6 layer charters; C8 domains | Implemented (declared seats) |
| DOR | Definition of Ready floor: complete, finer never coarser, no blank rows, gate checks | Implemented |
| E9 | Constitution size, state file size, track cap, single-principal disclosure | Partial |
| E11 | Registry integrity | Partial |
| E3 | No-op test lint: early return, catch-to-false, blanket and unregistered skips | Partial (static) |
| E14 | Data contracts: producer, consumers, kind, version, compatibility, schema | Implemented |
| E15 | Append-only migrations: no edit, delete or rename of a merged migration | Implemented |
| E16 | Required diagrams as Mermaid code: present, right form, not empty | Implemented |
| E17 | Every seat has a job description; role proposals add an independent verifier and a peer review with demand | Implemented |
| E1, E4, E5, E7, E8, E12, E13 | Identities, contracts, rulesets, harness hooks, manifests, validation env, post-deploy verification | v0.2 |
| E2, E6 | Red record per test, gate canary | v0.3 |

Full detail: [docs/enforcement.yml](docs/enforcement.yml). Plan: [docs/roadmap.md](docs/roadmap.md).

## Start a project

See [BOOTSTRAP.md](BOOTSTRAP.md). In short: create a repository from this template and
protect its lanes, run a bootstrap session in the Architect seat, have a fresh Verifier
session challenge it, answer the findings, approve, then run the smoke cycle. Cycle 1 builds
no product code.

## Layout

```
CLAUDE.md                 constitution: only the rules no check enforces yet
STATE.md                  cockpit card, capped at 200 lines
appliance.yml             grade, autonomy, caps, pinned floor version
docs/roles.yml            seats, charters, incompatible pairs, holders
docs/artifact-types.yml   artifact folders, prefixes, approval rules
docs/dor/                 Definition of Ready floor and this project's checklist
docs/enforcement.yml      every check and its status
docs/templates/           templates for every artifact type
docs/standards/data/      data standards (draft defaults to adapt) and the Data Architect trigger
docs/registry.md          near-misses and external issues
docs/method/              design rationale, challenge record, backtest, dry runs, template registry
tools/checks/             the checks
tests/                    tests showing each check refusing what it should
```

## Governance of this repository

The template repository is developed by one person with agent help. Agents work on
branches and open pull requests; the owner reviews and merges. Agent work is pushed under the
owner's GitHub authorization until check E1 ships. No independent review is available at this
governance stage. The challenge round recorded in
[docs/method/challenge-round-1.md](docs/method/challenge-round-1.md) was run by a fresh
session with no access to the author's reasoning. The first cold-start test of the
template is in [docs/method/dryrun-1.md](docs/method/dryrun-1.md).
