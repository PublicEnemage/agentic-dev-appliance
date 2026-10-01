# Exceptions: temporary, priced and finite

**Status:** design, not yet built. Written 2026-10-01.

WorldSIM needed a handful of decisions to accept non-compliance with a standard, process,
policy or architecture for a defined time, with a risk analysis and mitigations put to the
Engineering Lead. It also needed to stop that mechanism turning into a loophole for cutting
corners indefinitely. Both needs are design needs here, so the mechanism arrives before the
first exception is asked for.

## Three tools, not one

A seat that cannot comply has three honest answers. Each has a different cost, and the
difference is the first defence against abuse.

| Situation | Tool | Time limit | Approver |
| --- | --- | --- | --- |
| The rule never applies to this project | Not-applicable row, with a reason (exists today) | None; reopened on a named condition | Engineering Lead |
| The rule applies but cannot be met now | **Exception** | Required, capped | Engineering Lead |
| The rule keeps needing exceptions | **Change the rule** through the chain | None | Engineering Lead, and the owning seat's author |

The third row is the one WorldSIM learned late. An exception is a loan against a rule. A
rule that is borrowed against repeatedly is wrong, and the exception record is the evidence
that sends it back for repair.

## The exception artifact

A new artifact type `exception` in `docs/exceptions/`, prefix `EXC`, human approver. Any seat
may author it; a different seat challenges; the Engineering Lead approves. The seat blocked
by the rule raises it. The Engineering Lead does not raise one for their own convenience.

Front matter, so a check can read it:

| Field | Meaning |
| --- | --- |
| `waives` | What is waived: a check ID, a floor row, a standard or ADR id, or a constitution rule, with a path or scope. Exact, never "the process" |
| `reason` | Why the rule cannot be met now |
| `risk` | What can go wrong, likelihood and impact, and who bears it |
| `mitigations` | What reduces the risk while the exception runs, each with an owner |
| `expires` | A date, no later than the cap |
| `exit` | How compliance returns: the owning seat, and the backlog item that does it |
| `renews` | The id of the exception this extends, if any |

The review file beside it answers the risk analysis item by item, like any other artifact.

## An exception is also a diagnosis

In WorldSIM, taking an exception for a failing test to the Intent Owner showed that the
design of the feature was wrong. The failure looked like an engineering problem, and the
cause sat upstream in intent. This is the same pattern as NM-018: the surface domain of a
problem is not always its root-cause domain. A request to waive a rule is often the first
moment anyone has asked whether the rule is right, so the process should use it as a
signal, and not only as a gate.

Two more fields carry that:

| Field | Meaning |
| --- | --- |
| `diagnosis` | The author's first reading of why the rule fails: `implementation`, `rule-wrong`, `design-wrong`, `environment` or `schedule` |
| `consulted` | Seats asked cold before the Engineering Lead decides, each with a reference to the recorded input |

Two rules follow.

1. **Consult by root cause, not surface.** The consulted seats are chosen by the suspected
   cause, as for any artifact. When the waived item traces, through its parents, to a use
   case, a non-functional requirement or the business case, the Intent Owner is consulted
   and the input is recorded before the Engineering Lead decides. The Intent Owner advises;
   the Engineering Lead still approves.
2. **A design finding withdraws the exception.** If the consulted input shows the design is
   wrong, the exception is withdrawn and the upstream artifact goes back through the chain.
   That is the consumer duty working, and it costs less than carrying a waiver.

The Steward reports the spread of diagnoses each cycle. Many `design-wrong` points to weak
discovery. Many `schedule` points to a plan that is wrong. Many `rule-wrong` on one rule is
the repeat signal in defence 3.

The cost is bounded. Only exceptions that trace to intent reach the Intent Owner, so the
human is not asked to triage style or tooling waivers. The trace assumes the waived item
names the artifact it traces to, for example the story or use case id a test belongs to.
Where that link is missing, the check cannot tell whether the Intent Owner is needed, and
refuses the exception until the author supplies it.

## What keeps the register from becoming a loophole

Each defence is a check or a measurable, so it does not depend on anyone being careful.

1. **Expiry fails the build.** An expired exception stops waiving. The rule's own check
   fails again on the next run, the same way an expired skip does today.
2. **One renewal at most.** A renewal is a new exception citing `renews`, with a fresh
   risk analysis and a challenge by a different seat from the first. A second renewal is
   refused. The only route after that is to change the rule or fix the cause.
3. **A repeat is a signal.** The same rule waived twice within a window of cycles opens a
   review of the rule itself. The Steward lists it; the owning seat proposes a change or
   defends the rule.
4. **A budget of live exceptions.** More than the cap open at once blocks new ones until
   one closes. The cap is a project setting.
5. **A short non-waivable list.** Seat separation, human approval of business artifacts,
   append-only migrations, the rule against pushing to `main`, and the exception rules
   themselves cannot be waived. A project may lengthen the list, never shorten it.
6. **Every waiver is loud.** A waived finding is printed on every run with its exception
   id and expiry. `STATE.md` shows the live count. The Steward audits the register at each
   cycle exit and reports the oldest exception and the repeat count.
7. **An exit that exists.** An exception with no exit owner and backlog item is refused,
   so "temporary" has a mechanism and a name.
8. **Exact scope.** A waiver names the check and the path. A waiver for a path does not
   cover a new file in the same folder unless the folder is named.

## Mechanics

A waiver works only if a check's finding can be matched to an exception. Checks already
report a check ID, a path and a message. The runner would drop a finding that an active,
approved exception covers, and print it as waived. The register is then checked by its
own check, E18: front matter complete, the cap and renewal rules met, the non-waivable
list respected, authors, challengers and approvers distinct, the exit named, a diagnosis
given, and the Intent Owner consulted whenever the waived item traces to intent.

## Parameters to settle

Defaults to propose, by grade, in `appliance.yml`:

| Setting | Light | Standard | Assured |
| --- | --- | --- | --- |
| Longest exception | 90 days | 45 days | 30 days |
| Renewals | 1 | 1 | 0 |
| Live exceptions at once | 8 | 5 | 3 |
| Repeats before a rule review | 3 | 2 | 2 |

These are starting points taken from WorldSIM's handful of cases, not measurements. The
Engineering Lead should replace them with what WorldSIM's own register shows.

## Open questions

- Whether the Intent Owner's input should be advice only, as written above, or an approval
  for exceptions that lower a security, privacy or data-protection control. Those trace to
  non-functional requirements, so the consultation rule already reaches them.
- Whether an exception needs a peer review like a role proposal, or only the challenger.
  The first costs more and would catch more.
- How the single-principal disclosure applies: with one person in both human seats, the
  approval is the same signature as the request's sponsor. The challenger and the risk
  analysis carry the independence until E1 binds identities.

## Where it lands in the roadmap

After dry run 3. The artifact type, template and E18 come first. The runner's waiver
matching comes second, because a register that waives nothing is a record, and the
check that makes expiry fail the build is what gives it teeth.
