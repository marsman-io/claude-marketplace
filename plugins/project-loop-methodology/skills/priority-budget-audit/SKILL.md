---
name: priority-budget-audit
description: Audit priority drift ACROSS A PORTFOLIO over multiple quarters or many initiatives. Walks each initiative's spending then finds cross-portfolio patterns — where mechanisms drift in usage, where the same initiatives accumulate all five mechanisms, where one mechanism has lost its single job. For execute/replan phase. Use priority-budget-walk for single-initiative analysis.
---

# Cross-portfolio priority budget audit

Read `${CLAUDE_PLUGIN_ROOT}/docs/Stakeholder priority budget.md` and `${CLAUDE_PLUGIN_ROOT}/docs/Project lifecycle.md` (execute/replan phases).

## Procedure

1. **Enumerate target initiatives.** Read the active portfolio (roadmap, OKR set, the list of in-flight projects). List them.
2. **For each initiative**: name its portfolio type (per `project-surface-type`) and sample its budget spending across the five mechanisms (per `priority-budget-walk`). Sampling is fine; full walk on every initiative is not the goal — patterns are.
3. **Aggregate cross-portfolio**:
   - How many initiatives are labeled "P0" / "top priority"? More than 3-4 means the label has lost meaning.
   - Which mechanisms are being applied to the same initiatives (stacking patterns)?
   - Which initiatives have *zero* differentiation — no mechanism marks them as more or less important than the rest?
   - Has exec sponsorship become decorative (sponsored by default rather than for cause)?
   - Has OKR alignment become decorative (every initiative ladders to some OKR)?
4. **Surface the systemic drift**, not per-initiative findings.

## Output

```
Initiatives audited: <N>
Portfolio type: <from project-surface-type at the portfolio level>

Drift patterns:
  1. <pattern>: <N initiatives> — <e.g., "P0 inflation: 11 of 14 initiatives are P0">
  2. <pattern>: <N initiatives> — ...

Mechanism-job violations (mechanism doing two jobs across the portfolio):
  - Executive sponsorship: now applied to <count> initiatives — has lost its "this needs air cover" job
  - OKR alignment: <count> initiatives wired to OKRs through stretch interpretations — has lost its "this ladders to a named outcome" job
  - …

Recommended subtractive next step:
  Pick the most-spent mechanism (<which>), strip it from one cluster of initiatives (<which>), see if priority reappears. Subtract before re-prioritize.
```

The doc's discipline: priority clarity comes from spending the budget well, not from adding more P0 tags. Audits should resolve to *what to remove*.
