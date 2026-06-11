---
name: priority-budget-walk
description: Walk the five mechanisms of priority spending on ONE feature, issue, or task — intent prominence, context allocation, implementation focus, verification coverage, review cadence. Each mechanism has one job; this skill reports under-spent / well-spent / over-spent. Pairs with project-surface-type (run first) and priority-squint-test (run after). For charter/plan/adjust phases; for cross-feature audit use priority-budget-audit.
---

# Walk the five mechanisms

Read `${CLAUDE_PLUGIN_ROOT}/docs/Priority budget.md`. Assumes the work mode has been named.

## Procedure

For each of the five mechanisms, examine the target feature / issue / task:

1. **Intent prominence** — what sits at the top of the issue, prompt, or acceptance note. Is the intended user outcome clear? Or is everything labeled urgent without a named change?
2. **Context allocation** — which files, docs, screenshots, traces, and prior attempts the agent receives. Is context matched to risk? Or is a small fix loaded with the whole app?
3. **Implementation focus** — how much surface area the agent is allowed to touch. Is the focus matched to the intent? Or is the task allowed to sprawl?
4. **Verification coverage** — which tests, screenshots, demos, or manual checks prove the outcome. Does verification prove user behavior, or only file changes / test existence?
5. **Review cadence** — how closely and how often the builder inspects what comes back. Is review matched to uncertainty and risk, or driven by anxiety / neglect?

For each: status (under-spent / well-spent / over-spent), with artifact cite.

**Spot the stacking**: any target marked with all five mechanisms? (Top prompt prominence + broad context + large implementation surface + deep verification + repeated review is the canonical "this task will starve everything else" failure.) List every stacking violation.

## Output

```
Work mode: <from project-surface-type>
Target: <feature / issue / task>

| Mechanism | Status | Evidence |
|-----------|--------|----------|
| Intent prominence | well-spent | acceptance criterion is first in issue.md |
| Context allocation | over-spent | prompt includes whole app context for one copy fix |
| Implementation focus | under-spent | issue says "checkout flow" but diff only edits button text |
| Verification coverage | well-spent | screenshot + happy-path test prove the intended path |
| Review cadence | over-spent | repeated reviews of same low-risk copy path |

Stacking violations:
  - <target>: 4+ mechanisms applied — will starve <other targets>
```

The doc says: each mechanism does *exactly one job*. If a mechanism is doing two, that's the finding.
