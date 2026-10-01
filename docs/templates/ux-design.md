---
id: '{{PREFIX-NNN}}'
type: ux-design
title: '{{Title}}'
status: draft
author_seat: Designer
challenger_seat: Product
approver: Intent Owner
parents:
- UC-001
approved_at: null
---

# {{Title}}

Floor rows D4, D13. If the product has no user interface, sign not-applicable in the checklist.
Diagrams are Mermaid code, tagged on the line above the fence. Replace each sample.

## Experience intent
{{What the user should feel and be able to do, in one paragraph. This is the north star
the design system serves.}}

## User flows
One flow per main path, with its failure paths. Each step names what the user sees.

<!-- diagram: user-flows -->
```mermaid
flowchart TD
  Start([Open the app]) --> Form[Fill in the form]
  Form --> Submit{Submit valid?}
  Submit -->|yes| Done[Confirmation with reference]
  Submit -->|no| Error[Inline error naming the field and the fix]
  Error --> Form
```

## Navigation

<!-- diagram: navigation -->
```mermaid
flowchart LR
  Home --> List[Item list]
  List --> Detail[Item detail]
  Detail --> Edit[Edit item]
  Home --> Settings
```

## Design system
{{Type, colour, spacing, components. Brand treatment, if any.}}
