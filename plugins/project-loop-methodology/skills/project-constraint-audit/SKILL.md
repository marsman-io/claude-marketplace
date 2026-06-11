---
name: project-constraint-audit
description: Audit a MATURE in-flight product work cascade for drift — find pinned constraints that have been silently broken, soft inputs that drifted without explicit decision, dependencies that were skipped or doubled, verification budgets exhausted. For execute/replan phase.
---

# Audit a mature project cascade

Read `${CLAUDE_PLUGIN_ROOT}/docs/Constraint-based project management.md` and `${CLAUDE_PLUGIN_ROOT}/docs/Project lifecycle.md` (execute/replan phases).

## Procedure

For the target work's constraint cascade:

1. **Locate the original intent / plan.** Identify the declared soft inputs and hard pins as they were when the work started.

2. **Find broken pins.** Pins are supposed to be hard. Has any of them quietly shifted? (The "must preserve saved data" pin became a migration; the "only this route" pin became cross-app edits; the accessibility floor disappeared.) Each broken pin without a re-baseline is a finding.

3. **Find drifted soft inputs.** Has scope expanded without explicit decision? Has the context budget ballooned? Has verification thinned out? Has review depth changed without being named? Drift without naming is the canonical signal of work that has lost its plan.

4. **Find broken or doubled dependencies.** Where has a downstream behavior proceeded without its upstream contract? Where have two artifacts duplicated work because the dependency map wasn't shared?

5. **Find exhausted verification budgets.** Verification is the buffer between plausible output and product confidence. If verification is spent before the demo path, the work is in trouble even if tests are green.

6. **Find silent priorities.** Which soft input has been absorbing all the drift — usually the one nobody named as the buffer? The absorbing input is the de-facto soft constraint; surface it.

## Output

```
Project: <name>
Original intent / plan date: <date or artifact>

Broken pins (declared hard, silently shifted):
  - <pin>: <cite> — <how it shifted, when>
  - ...

Drifted soft inputs (changed without explicit decision):
  - <input>: <original value -> current> — <cite>
  - ...

Broken/doubled dependencies:
  - <A -> B>: <how it broke or where it doubled>

Exhausted verification:
  - <path / behavior>: <what evidence was expected, what remains>

Absorbing input (which soft constraint is silently taking the drift):
  - <input> — the work is treating this as the buffer; surface and decide

Recommended re-baseline next step:
  Which ONE pin or input to re-decide first, with cite.
```
