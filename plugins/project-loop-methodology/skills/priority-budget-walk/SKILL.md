---
name: priority-budget-walk
description: Walk the five mechanisms of priority spending on ONE initiative or one quarter's roadmap — roadmap position, resourcing, executive sponsorship, OKR alignment, communication cadence. Each mechanism has one job; this skill reports under-spent / well-spent / over-spent. Pairs with project-surface-type (run first) and priority-squint-test (run after). For charter/plan/adjust phases; for cross-portfolio audit use priority-budget-audit.
---

# Walk the five mechanisms

Read `${CLAUDE_PLUGIN_ROOT}/docs/Stakeholder priority budget.md`. Assumes the portfolio surface type has been named.

## Procedure

For each of the five mechanisms, examine the target initiative (or roadmap quarter):

1. **Roadmap position** — what comes first, what comes second. Is the initiative's position clear? Or is everything labeled "P0"?
2. **Resourcing** — how many people, dedicated or shared. Is the resourcing matched to the position? Or is a "high priority" initiative actually staffed at 0.5 of one engineer?
3. **Executive sponsorship** — whose name is on it. Is sponsorship reserved for the few that truly need air cover, or sprinkled across every initiative?
4. **OKR alignment** — does this ladder to a named outcome the org committed to? Or is the alignment retrofitted ("strategy doc page 14")?
5. **Communication cadence** — how often does the org hear about it. Are the updates matched to the work, or stale / over-frequent?

For each: status (under-spent / well-spent / over-spent), with artifact cite.

**Spot the stacking**: any initiative marked with all five mechanisms? (Top roadmap position + dedicated team + exec sponsor + central OKR + weekly all-hands update is the canonical "this initiative is going to starve everything else" failure.) List every stacking violation.

## Output

```
Portfolio type: <from project-surface-type>
Target initiative: <name>

| Mechanism | Status | Evidence |
|-----------|--------|----------|
| Roadmap position | well-spent | "P1, after Initiative X" in Q3-roadmap.md |
| Resourcing | over-spent | dedicated team of 8 + 2 PMs + designer = 11 FTE on a 6-week effort |
| Exec sponsorship | well-spent | sponsor named in charter |
| OKR alignment | over-spent | linked to 3 OKRs; alignment now means nothing |
| Communication cadence | well-spent | bi-weekly to internal, monthly external |

Stacking violations:
  - <initiative>: 4+ mechanisms applied — will starve <other initiatives>
```

The doc says: each mechanism does *exactly one job*. If a mechanism is doing two, that's the finding.
