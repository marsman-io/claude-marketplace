---
name: outcome-drift-audit
description: Audit outcome-altitude drift across MANY features, issues, screens, or agent-produced artifacts. Pairs altitude-naming on each target with cross-artifact pattern detection — where has work drifted into output/activity tracking when delegated intent sits at outcome? where did outcome-anchored work accrete file-change summaries at the top? For execute/replan phase.
---

# Cross-feature outcome drift audit

Read `${CLAUDE_PLUGIN_ROOT}/docs/Intent as a PM Lens.md` and `${CLAUDE_PLUGIN_ROOT}/docs/Project lifecycle.md` (execute/replan phases).

## Procedure

1. **Enumerate target artifacts.** Read the active feature set, issue cluster, PR, changed files, screenshots, tests, logs, and demo notes. List the targets.
2. **For each**: name the likely delegated intent + name the current organization altitude.
3. **Find the drift patterns:**
   - Which targets whose intent is *outcome* now read as activity logs?
   - Which started as outcome-anchored and accreted output lists ("here's everything changed") at the top?
   - Which never had a stated outcome at all — default = activity, accidentally?
   - Which targets have *more* outcome clarity than expected (positive drift)?
4. **Surface the systemic pattern**, not per-target findings. Per-target drift is uninteresting; *root causes that produce drift across the product work* are the finding.

## Output

```
Targets audited: <N>

Drift patterns:
  1. <pattern>: <N targets> — <example: "outcome-anchored issues whose agent summaries surface only file changes">
  2. <pattern>: <N targets> — <example: "acceptance criteria exist, but tests prove implementation details instead">
  ...

Root causes:
  - <pattern -> cause>: <e.g., "the prompt asks 'what did you change' not 'what can the user do now'">
  - ...

Recommended next step:
  Which ONE target to re-anchor first (highest-leverage fix), with cite and what to change about its evidence.
```

The audit's value is in the pattern, not the per-target findings. If the report becomes a 40-line list of individual artifacts, you've under-aggregated — re-cluster.
