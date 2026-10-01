---
artifact: "{{PREFIX-NNN}}"
challenger_seat: "{{seat}}"
session: "{{separate session, date}}"
open_findings: 0
---

# Review of {{PREFIX-NNN}}

Save beside the artifact as `{{PREFIX-NNN}}-{{slug}}.review.md`. The challenger works in a
fresh session and is asked to find what is wrong or missing, not to confirm.
Approval is blocked while `open_findings` is above 0.

Severity:
- **high:** blocks approval until fixed.
- **medium:** blocks approval until the author answers it, with a fix or a reasoned decline.
- **low:** may be deferred to the backlog with a note in the Answer column.

The author answers each finding in the Answer column and writes Yes in Closed? once it is
answered. The bootstrap review is the exception to the file name: it is
`docs/bootstrap.review.md`, because the bootstrap has no artifact id.

The author answers each finding in the Answer column. `open_findings` counts findings
with no answer, plus every high finding not yet fixed.

| # | Finding | Severity | Answer | Closed? |
| --- | --- | --- | --- | --- |
| 1 | | | | |
