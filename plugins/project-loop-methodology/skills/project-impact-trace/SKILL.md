---
name: project-impact-trace
description: Trace the blast radius of a proposed change request against a project's constraint cascade. Input — which constraint is being moved, by how much. Output — every dependency + commitment affected, with migration cost. For adjust/replan phase. Use to answer "is this a small change or a hidden replan?" before agreeing to it.
---

# Trace project change-request impact

Read `${CLAUDE_PLUGIN_ROOT}/docs/Constraint-based project management.md` and `${CLAUDE_PLUGIN_ROOT}/docs/Project lifecycle.md` (adjust phase).

## Procedure

Given a target constraint (a date, a deliverable, a budget, a resource assignment) and a proposed change:

1. **Find direct consumers.** Read the plan / charter / dependency map. What downstream deliverables, milestones, or commitments depend directly on this constraint?

2. **Classify each consumer:**
   - **Re-derives automatically** — downstream work that adjusts in its own planning loop without action from the PM (e.g., team backlog reshuffles when scope shrinks).
   - **Re-plans manually** — work that requires a planning conversation per affected milestone.
   - **External commitments** — promises to stakeholders / customers / regulators / contracts. Cannot be unilaterally re-planned.

3. **Find transitive consumers.** Downstream of downstream. The change might fan out 3-4 levels — a date slip on workstream A delays workstream B which delays the customer commitment.

4. **Estimate migration cost.**
   - Number of milestones / deliverables / commitments affected
   - Per-class breakdown (auto / manual / external)
   - Approximate effort (PM hours + team disruption + stakeholder communication)

5. **Identify alternative paths.** Could re-pinning a different constraint absorb this change at lower cost? Could de-scoping a deliverable that was already droppable insulate the rest?

## Output

```
Target constraint: <name>
Proposed change: <description>

Direct consumers (<N> total):
  - Auto-rederives (<N>):  <list>
  - Manual replan (<N>):  <list>
  - External commitments (<N>):  <list>

Transitive consumers: <N> additional milestones / deliverables

Migration cost estimate:
  - PM hours: <estimate>
  - Stakeholder conversations required: <list>
  - Team disruption: <by team / workstream>
  - Verdict: <"true adjust — under N consumers, no external impact" | "hidden replan — N external commitments need re-negotiation" | "intermediate">

Alternative paths to reduce blast radius:
  - <alternative 1>: <effect>
  - <alternative 2>: <effect>
```

The cost classification is the deliverable. A change request that touches 4 external commitments is not an adjust; it's a replan dressed as a small ask. Name it as such.
