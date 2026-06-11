---
name: outcome-drift-audit
description: Audit outcome-altitude drift across MANY projects in a mature portfolio. Pairs altitude-naming on each project with cross-portfolio pattern detection — where has the team drifted into output/activity tracking when stakeholder intent sits at outcome? where did outcome-anchored projects accrete activity-altitude status reports? For execute/replan phase.
---

# Cross-portfolio outcome drift audit

Read `${CLAUDE_PLUGIN_ROOT}/docs/Intent as a PM Lens.md` and `${CLAUDE_PLUGIN_ROOT}/docs/Project lifecycle.md` (execute/replan phases).

## Procedure

1. **Enumerate target projects.** Read the active portfolio. List them.
2. **For each**: name the stakeholders' likely intent + name the current organization altitude.
3. **Find the drift patterns:**
   - Which projects whose stakeholder intent is *outcome* now read as activity dashboards?
   - Which started as outcome-anchored (with OKRs) and accreted output lists ("here's everything we shipped") at the top?
   - Which never had a stated outcome at all — default = activity, accidentally?
   - Which projects have *more* outcome clarity than expected (positive drift)?
4. **Surface the systemic pattern**, not per-project findings. Per-project drift is uninteresting; *root causes that produce drift across the portfolio* are the finding.

## Output

```
Projects audited: <N>

Drift patterns:
  1. <pattern>: <N projects> — <example: "outcome-anchored projects whose status reports surface only activity">
  2. <pattern>: <N projects> — <example: "OKR alignment retrofitted; the projects predate the OKR and were back-mapped">
  ...

Root causes:
  - <pattern → cause>: <e.g., "status report template asks 'what did you ship this week' not 'what changed for the user'">
  - …

Recommended next step:
  Which ONE project to re-anchor first (highest-leverage fix), with cite and what to change about its reporting.
```

The audit's value is in the pattern, not the per-project findings. If the report becomes a 40-line list of individual projects, you've under-aggregated — re-cluster.
