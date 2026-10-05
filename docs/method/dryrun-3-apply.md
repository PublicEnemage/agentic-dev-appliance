# Applying the dry run 3 decisions

Plan for turning [dryrun-3-decisions.md](dryrun-3-decisions.md) into `docs/roles.yml`.
Written 2026-10-05. The human pastes each prompt unchanged. The observer starts no session.

## Run protocol (applies to every session below)

These close the gaps dry run 3 left. They are in the protocol and not in each prompt.

- **One fresh clone per session.** No other review or peer file in the folder, and no
  sibling projects in the parent folder.
- **Base branch is named.** A session cuts its branch from the branch the step names, never
  from whatever the clone has checked out.
- **Input manifest is given.** The step lists it. A session reads that and nothing else.
- **First action:** write at the top of the session's output file every project
  instruction file and note about the person in its context.
- **Peers do not read each other.** Each peer branch holds the proposal and its own file
  only. The author copies peer entries in unchanged.
- **Never push to `main`.**

## Sequence

The proposal goes first. The apply session adds the Frontend Architect's roster entry and
wiring that depends on it, and that needs the approved charter. Wiring that does not touch
the new seat could go earlier, but two changes to `docs/roles.yml` in flight at once cost
more than waiting.

1. **Merge this PR.** It adds the draft proposal `RP-001` and these prompts.
2. **Author session** (Product) finalizes RP-001 and sets it in-review.
3. **Peer sessions** (Designer, Architect, Verifier, Delivery, Builder), five fresh clones,
   in parallel.
4. **Author session** copies the peer entries into the proposal unchanged and sets
   `peer_recommendation` no more favourable than the least favourable peer.
5. **Challenge** by the Architect seat in a fresh session. Findings go in
   `RP-001-frontend-architect.review.md`. The author answers item by item.
6. **Engineering Lead approves** by merging.
7. **Apply session** (Architect) edits `docs/roles.yml`.
8. **Challenge and merge** as in BOOTSTRAP steps 5 and 6.

Step 5's challenger is the Architect, who loses the `frontend` layer. The Engineering Lead
reads the review with that in mind.

## Prompt: author session (step 2)

> You are a fresh session in a clone of the project repository. Read `CLAUDE.md` first and
> follow what it says. You hold the **Product** seat. Cut branch `rp-001-author` from
> `main`. Input manifest: `CLAUDE.md`, `STATE.md`,
> `docs/method/dryrun-3-decisions.md`, `docs/crew/RP-001-frontend-architect.md`,
> `docs/templates/role-proposal.md`, `docs/roles.yml`. Read nothing else. Before anything
> else, write at the top of `docs/crew/RP-001-frontend-architect.md`, in a section
> "Session context", every project instruction file and note about the person in your
> context.
>
> Outcome: RP-001 is ready for peer review. Every charter line is true to the decisions and
> to the roster. Where the draft is wrong or unclear, you change it and say why in the body.
> Where your own seat's job overlaps the new seat's (stories), say where the line sits and
> what you would refuse. Leave `peer_review` and `peer_recommendation` blank. Set status
> `in-review`. Commit and push.

## Prompt: peer session (step 3), one per seat

Fill `{SEAT}` with Designer, Architect, Verifier, Delivery or Builder.

> You are a fresh session in a clone of the project repository. Read `CLAUDE.md` first and
> follow what it says. You hold the **{SEAT}** seat. Cut branch `peer-RP-001-{SEAT}` from
> `rp-001-author`. Input manifest: `CLAUDE.md`, `STATE.md`,
> `docs/crew/RP-001-frontend-architect.md`, `docs/roles.yml`,
> `docs/method/dryrun-3-decisions.md`. Read nothing else. Before anything else, write at the
> top of `RP-001-PEER-{SEAT}.md` in the repository root every project instruction file and
> note about the person in your context.
>
> Outcome: your peer entry for RP-001 in that file. It gives your recommendation (accept,
> accept-with-conditions or reject), your demand (what you would hand to the new seat or
> take from it, and what you stop doing yourself), and your evidence (artifacts, findings
> or registry entries, not opinion). Where the charter and your own job description in
> `docs/roles.yml` disagree about what passes between you, list the change each side needs.
> Number your conditions. Do not edit the proposal or `docs/roles.yml`. Commit and push.

## Prompt: apply session (step 7)

> You are a fresh session in a clone of the project repository. Read `CLAUDE.md` first and
> follow what it says. You hold the **Architect** seat. Cut branch `apply-roles` from
> `main`, after RP-001 is approved and merged. Input manifest: `CLAUDE.md`, `STATE.md`,
> `docs/method/dryrun-3-decisions.md`, `docs/method/dryrun-3.md`,
> `docs/crew/RP-001-frontend-architect.md` and its review, `docs/roles.yml`,
> `docs/artifact-types.yml`, `docs/templates/`. Read nothing else. Before anything else,
> write at the top of `APPLY-ROLES.md` in the repository root every project instruction file
> and note about the person in your context.
>
> Outcome: `docs/roles.yml` and `docs/artifact-types.yml` carry the decisions, and nothing
> else, and every check passes. The Frontend Architect's `job` is the approved RP-001
> charter, unchanged. The wiring changes are those under "What follows" in the decisions
> document. In `APPLY-ROLES.md`, give each change a row: what changed, which decision or
> compile finding it comes from, and the seat it touches. Do not decide the items listed
> under "Not decided". Any other wiring change from the compile that you think is needed
> goes in its own commit, labelled, so the Engineering Lead can accept or drop it. Commit
> and push.

## Gaps this plan found

- **The Steward cannot author a proposal.** The role-proposal template said "Any seat or the
  Steward may author", but SEATS refuses the Steward in every artifact field. The template
  now says any agent seat may author and the Steward compiles.
- **An existing seat had no change path.** E17 refused an in-review proposal for a seat that
  already exists, while the Engineering Lead's job said every roles-file change carries an
  approved proposal. Decided 2026-10-05 (decision 8): substantive changes use a proposal
  with `change_of` set and a full peer review, which E17 now accepts. Wiring-only changes
  need no proposal once the reconciliation check exists. Until then the apply session's
  change table, a fresh challenge and the Engineering Lead's merge stand in for it.
- **Author and peers.** E17 forbids the author as a peer, and every seat that sends input or
  takes output must be a peer. The author must therefore be a seat the charter does not
  name. For RP-001 that is Product, which is why the charter has no Product input.
