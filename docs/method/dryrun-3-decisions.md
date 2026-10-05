# Dry run 3: decisions

**Date:** 2026-10-01. **Decided by:** the Engineering Lead, on the options in
[dryrun-3.md](dryrun-3.md) ("Left open"). **Status:** decided, not yet applied. Nothing in
`docs/roles.yml` has changed. A decision counts once it is written here, and it takes effect
when the change below is merged.

## Decisions

| # | Question | Decision |
| --- | --- | --- |
| 1 | Who authors stories | **Product** authors story content. Delivery owns the template, the order and the input manifest. See the reading under 2 |
| 2 | Frontend section | **Split the Architect.** A Frontend Architect seat is proposed beside the general Architect. The Designer's work flows to the Frontend Architect, who challenges the frontend design and authors the frontend stories |
| 3 | Integration and deployment-runtime | The **Architect** authors integration. The **Operator** authors deployment-runtime. Each challenges the other |
| 4 | Verifier layers against D6 | Keep the Verifier's `qualified_layers` narrow. Put a qualified challenger on each layer: the Data Architect for data, the Operator for integration and runtime, the Frontend Architect or Designer for frontend |
| 5 | `domain-core` | Open a crew review for a domain seat if the pilot has real business rules. Otherwise mark it not applicable with a reason |
| 6 | `benefits-check` | **Product** authors it, the **Operator** supplies post-deploy evidence, the **Intent Owner** approves. Add it to Product's outputs |
| 7 | Blocked human seat | Now: sessions park work and record it in `STATE.md`, and agents never approve in a human's place. Before real users arrive: name a deputy for the Engineering Lead seat |
| 8 | Changing an existing seat's job description | **Every change takes a peer review before merge**, as every code change does. Substantive changes take the full review a new seat takes. Wiring-only changes take one peer and the seat on the other end of each changed line. Both are role proposals with `change_of` and `change_kind`. Decided 2026-10-05 |

### Reading of 1 and 2, to confirm

The Engineering Lead's words: "Designer's story for Frontend Architect, and Frontend
Architect's stories plus Architect stories with manifests for Builder." The reading used
here:

- The Designer's approved `ux-design` goes to the Frontend Architect, not straight to the
  Builder.
- The Frontend Architect turns it into the frontend design and its stories.
- Delivery takes those stories and the Architect's stories, orders them and attaches the
  input manifest for each. The Builder receives the ordered stories from Delivery.

Who authors the technical frontend section, and who challenges it, is for the Frontend
Architect proposal's peer review to settle. The decision names the seat and its place in the
chain. It does not fix the author and challenger pair.

## What follows

1. **Frontend Architect proposal.** A new seat goes through a role proposal with peer
   review (E17). Peers must include every agent seat that sends it input or consumes its
   output: the Designer, the Architect, Delivery and the Builder. The charter takes
   `frontend` out of the Architect's `qualified_layers`, so the proposal must say what
   the Architect keeps.
2. **Wiring changes to existing seats**, from the compile and these decisions: Product
   outputs `story`, `increment-intent`, `users-use-cases` for the Designer and
   `benefits-check`; Delivery outputs ordered stories with manifests for the Builder;
   the Designer's consumer becomes the Frontend Architect; the Verifier's review outputs
   for the Designer, Builder and Operator; the Operator's `risk-assessment` and `cicd`
   consumers. A fresh Architect session applies them to `docs/roles.yml` (plan step 4),
   and each roster change carries its approved proposal.
3. **Data Architect adoption**, since decision 4 depends on it for the data layer.
4. **Constitution line for 7.** One rule about blocked human seats, kept short because
   `CLAUDE.md` has a byte budget.
5. **Wiring reconciliation and review independence checks** stay next on the build list
   and decide whether any of this can be trusted.

## Not decided

- Batching. A change that touches many seats needs one proposal per seat. Whether one
  proposal may carry several seats' wiring is open. The apply session's cost depends on it.
- `[Builder, Operator]` and `[Designer, Verifier]` in `incompatible_pairs`. Recommended,
  not yet confirmed. `[Builder, Delivery]` is not recommended.
- Which of the smaller questions (peer review of exceptions, exception parameters under one
  principal, Intent Owner advice or approval on security exceptions, build licence review
  scope and holder) apply. Recommended in conversation, not recorded as decided.
- The pilot: its app and grade decide decision 5 and the timing of the deputy in 7.
