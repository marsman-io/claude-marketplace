---
name: differentiation-budget-audit
description: Audit visual hierarchy drift ACROSS MANY screens in a mature design system. Walks each screen's spending then finds cross-screen patterns — where mechanisms drift in usage, where surface types are inconsistently treated, where one mechanism has lost its single job. For audit/refactor phase. Use differentiation-budget-walk for single-screen analysis.
---

# Cross-screen differentiation budget audit

Read `${CLAUDE_PLUGIN_ROOT}/docs/How to arrive at hierarchy clarity.md` and `${CLAUDE_PLUGIN_ROOT}/docs/Design system lifecycle.md` (audit phase).

## Procedure

1. **Enumerate target screens.** Glob for screens/pages/routes in the project. List them.
2. **For each screen**: name the surface type (per `surface-type-name` skill), then sample its budget spending across the five mechanisms (per `differentiation-budget-walk`). Sampling is fine; full walk on every screen is not the goal — patterns are.
3. **Aggregate cross-screen**:
   - Which surface types appear with which budget patterns?
   - Where do "reading" surfaces over-spend (cards on a settings page)?
   - Where do "operating" surfaces under-spend (no row separators in a queue)?
   - Where is shadow used decoratively (no longer means elevation)?
   - Where is color used as ornament (no longer means state)?
4. **Surface the systemic drift**, not individual screen findings.

## Output

```
Screens audited: <N> (list)

Drift patterns:
  1. <pattern>: <count> screens — <e.g., "7 reading-surface screens use cards+borders+shadows together">
  2. <pattern>: <count> screens — ...

Mechanism-job violations (mechanism doing two jobs across the product):
  - Shadow: now used decoratively in <list> — has lost its "this floats" job
  - Color: <count> ornamental uses — lost its "state and meaning" job
  - …

Recommended subtractive next step:
  Pick the most-spent mechanism (<which>), remove from one cluster of screens (<which>), see if hierarchy survives. Subtract before add.
```

The doc's discipline: hierarchy clarity comes from spending the budget well, not from spending more. Audits should resolve to *what to remove*.
