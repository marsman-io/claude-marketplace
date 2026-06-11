---
name: priority-budget-audit
description: Audit priority drift ACROSS MANY features, issues, or tasks. Walks each target's spending then finds cross-work patterns — where mechanisms drift in usage, where the same targets accumulate all five mechanisms, where one mechanism has lost its single job. For execute/replan phase. Use priority-budget-walk for single-target analysis.
---

# Cross-feature priority budget audit

Read `${CLAUDE_PLUGIN_ROOT}/docs/Priority budget.md` and `${CLAUDE_PLUGIN_ROOT}/docs/Project lifecycle.md` (execute/replan phases).

## Procedure

1. **Enumerate target work.** Read the active issue cluster, PR, changed files, TODOs, prompts, screenshots, tests, and any optional planning artifacts. List the targets.
2. **For each target**: name its work mode (per `project-surface-type`) and sample its budget spending across the five mechanisms (per `priority-budget-walk`). Sampling is fine; full walk on every target is not the goal — patterns are.
3. **Aggregate cross-work**:
   - How many targets are labeled "P0" / "urgent" / "top priority"? More than 3-4 means the label has lost meaning.
   - Which mechanisms are being applied to the same targets (stacking patterns)?
   - Which targets have *zero* differentiation — no mechanism marks them as more or less important than the rest?
   - Has intent prominence become decorative (every issue says critical, none names the user outcome)?
   - Has context allocation become decorative (everything gets broad context by default)?
   - Has verification coverage become decorative (every target gets generic "tests pass" instead of outcome evidence)?
   - Has review cadence become reactive (reviewing from anxiety instead of risk)?
4. **Surface the systemic drift**, not per-target findings.

## Output

```
Targets audited: <N>
Work mode: <from project-surface-type at the product area level>

Drift patterns:
  1. <pattern>: <N targets> — <e.g., "urgent-label inflation: 11 of 14 issues are P0">
  2. <pattern>: <N targets> — ...

Mechanism-job violations (mechanism doing two jobs across the work):
  - Context allocation: now applied broadly to <count> targets — has lost its "this needs more context" job
  - Verification coverage: <count> targets use generic tests-pass evidence — has lost its "this proves the outcome" job
  - ...

Recommended subtractive next step:
  Pick the most-spent mechanism (<which>), strip it from one cluster of targets (<which>), see if priority reappears. Subtract before re-prioritize.
```

The doc's discipline: priority clarity comes from spending the budget well, not from adding more P0 tags. Audits should resolve to *what to remove*.
