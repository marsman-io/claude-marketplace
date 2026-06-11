---
name: intent-drift-audit
description: Audit altitude drift across MANY screens in a mature design system. Pairs altitude-naming on each screen with cross-screen pattern detection — where has the data model leaked back into screens that should be intent-organized? where did guided flows accrete action toolbars? For audit/refactor phase.
---

# Cross-screen intent drift audit

Read `${CLAUDE_PLUGIN_ROOT}/docs/Intent as a Design Lens.md` and `${CLAUDE_PLUGIN_ROOT}/docs/Design system lifecycle.md` (audit phase).

## Procedure

1. **Enumerate target screens.** Glob for screens/pages/routes in the project.
2. **For each, name the intent altitude and the current altitude.** The intent altitude is *what the screen should be organized around given who opens it*; the current is *what it actually leads with*.
3. **Find the drift patterns:**
   - Which screens that *should be* intent-altitude now read as data-model lists?
   - Which started as guided flows and accreted action-altitude toolbars at the top?
   - Which never had a stated intent at all — default = data model, accidentally?
   - Which screens have *more* altitude clarity than expected (positive drift)?
4. **Surface the systemic pattern**, not per-screen findings. Per-screen drift is uninteresting; *root causes that produce drift across the product* are the finding.

## Output

```
Screens audited: <N>

Drift patterns:
  1. <pattern>: <N screens> — <example: "intent screens that grew an action toolbar at the top">
  2. <pattern>: <N screens> — <example: "data-model leakage on screens where every new field gets surfaced as a token row">
  ...

Root causes:
  - <pattern → cause>: <e.g., "every PR that adds a setting adds a row; nobody owns the intent grouping">
  - …

Recommended next step:
  Which ONE screen to re-ground first (highest-leverage fix), with file:line and what to change about its organization.
```

The audit's value is in the pattern, not the per-screen findings. If the report becomes a 40-line list of individual problems, you've under-aggregated — re-cluster.
