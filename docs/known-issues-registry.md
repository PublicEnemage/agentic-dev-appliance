# Known issues registry

The known limitations of this product that we cannot solve ourselves: a platform constraint,
a dependency, a decision outside the team. Append only. Checked by E11.

This file is the statement of known limitations. Point an outside reviewer here: due
diligence, audit, a customer's security or procurement review.

A hazard we can design away is a near-miss and goes in `docs/near-miss-registry.md`. A known
issue is one we cannot redesign. Its countermeasure is a workaround, written down.

Each entry uses these single-line fields, in this order:

    ## KI-001 — Short title
    **Date:** YYYY-MM-DD
    **What the limitation is:** one or two sentences, plain
    **Who or what it affects:** users, operators, a feature or a quality
    **Why we cannot solve it:** the constraint, and who holds it
    **Workaround:** what people do meanwhile
    **Revisit when:** a date or an event

IDs run KI-001, KI-002 and so on, ascending without gaps. A resolved issue stays in the
file. Add a line `**Resolved:** date and how`.

<!-- Entries start below this line. -->
