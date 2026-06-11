---
name: project-constraint-audit
description: Audit a MATURE in-flight project's constraint cascade for drift — find pinned constraints that have been silently broken, soft inputs that drifted without explicit decision, dependencies that were skipped or doubled, slack budgets exhausted. For execute/replan phase.
---

# Audit a mature project cascade

Read `${CLAUDE_PLUGIN_ROOT}/docs/Constraint-based project management.md` and `${CLAUDE_PLUGIN_ROOT}/docs/Project lifecycle.md` (execute/replan phases).

## Procedure

For the target project's constraint cascade:

1. **Locate the original charter / plan.** Identify the declared soft inputs and hard pins as they were when the project started.

2. **Find broken pins.** Pins are supposed to be hard. Has any of them quietly shifted? (The "contractual deadline" got renegotiated without re-baselining; the "must include feature X" silently became "X v2 in a later release.") Each broken pin without a re-baseline is a finding.

3. **Find drifted soft inputs.** Has scope expanded without explicit decision? Has the budget overspent? Has the timeline slipped without a CR being filed? Drift without naming is the canonical signal of a project that has lost its plan.

4. **Find broken or doubled dependencies.** Where has a downstream workstream proceeded without its upstream's checkpoint? Where have two workstreams duplicated work because the dependency map wasn't shared?

5. **Find exhausted slack budgets.** Slack is the buffer between plan and reality. If slack is spent before the milestone, the project is in trouble even if the dashboard is green.

6. **Find silent priorities.** Which soft input has been absorbing all the drift — usually the one nobody named as the buffer? The absorbing input is the de-facto soft constraint; surface it.

## Output

```
Project: <name>
Original charter date: <date>

Broken pins (declared hard, silently shifted):
  - <pin>: <cite> — <how it shifted, when>
  - ...

Drifted soft inputs (changed without explicit decision):
  - <input>: <original value → current> — <cite>
  - ...

Broken/doubled dependencies:
  - <A → B>: <how it broke or where it doubled>

Exhausted slack:
  - <phase>: <how much slack was budgeted, how much remains>

Absorbing input (which soft constraint is silently taking the drift):
  - <input> — the project is treating this as the buffer; surface and decide

Recommended re-baseline next step:
  Which ONE pin or input to re-decide first, with cite.
```
