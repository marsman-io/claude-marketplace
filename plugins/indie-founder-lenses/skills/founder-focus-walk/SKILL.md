---
name: founder-focus-walk
description: Walk the five mechanisms of focus spending on ONE bet — outcome prominence, evidence backing, scope commitment, validation coverage, attention cadence. Each mechanism has one job; this skill reports under-spent / well-spent / over-spent against the outcome the bet claims (revenue / retention / activation). Pairs with founder-work-mode (run first) and founder-focus-squint (run after). For scoping/committed phases; for cross-bet drift use founder-focus-audit.
---

# Walk the five founder mechanisms

Read `${CLAUDE_PLUGIN_ROOT}/docs/Founder focus budget.md`. Assumes the work mode has been named.

## Procedure

For each of the five mechanisms, examine the target bet:

1. **Outcome prominence** — which named outcome the bet leads with. Does it name a number on a surface ("lift trial→paid activation on pricing")? Or is it "improve X" / "v2", led by recency or an impact adjective rather than an outcome?
2. **Evidence backing** — what makes the founder believe this bet moves that outcome. A churn cohort, support tickets, a funnel drop in the analytics wiring, a teardown — versus a hunch or one loud customer. Is the backing proportional to the weeks the bet will cost?
3. **Scope commitment** — how many weeks, how much surface, how reversible. Is scope declared at all, and matched to the evidence? Or is a "quick" bet quietly a quarter?
4. **Validation coverage** — what would prove the outcome moved, decided *before* building: which metric, on which surface, by how much, by when. Does it prove the *outcome* moved, or just that the feature shipped ("ship it and see")?
5. **Attention cadence** — how often the founder will revisit this bet while live: check-weekly, glance-monthly, or set-and-forget. Is the cadence matched to how much the result can't otherwise be trusted, or driven by anxiety / neglect?

For each: status (under-spent / well-spent / over-spent), with artifact cite.

**Spot the stacking**: is one bet marked with all five mechanisms? (Leads the roadmap + the only one with real evidence + scoped to a quarter + the only one with a validation target + checked daily is the canonical "this bet will starve every other one" failure.) List every stacking violation.

## Output

```
Work mode: <from founder-work-mode>
Target bet: <bet name + the outcome it claims>

| Mechanism | Status | Evidence |
|-----------|--------|----------|
| Outcome prominence | well-spent | leads with "lift trial→paid on pricing" (roadmap.md:3) |
| Evidence backing | over-spent | six-week rebuild backed by one customer email |
| Scope commitment | under-spent | "redo onboarding" — no weeks, no surface declared |
| Validation coverage | under-spent | "ship and see" — no metric, no surface, no target date |
| Attention cadence | over-spent | low-risk copy bet re-opened every standup |

Stacking violations:
  - <bet>: 4+ mechanisms applied — will starve <other bets>
```

The doc says: each mechanism does *exactly one job*. If a mechanism is doing two — prominence carrying urgency, validation meaning "it shipped" — that's the finding.
