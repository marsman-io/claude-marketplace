---
name: project-surface-type
description: Name a portfolio's surface type — discovery, delivery, or operations — per the stakeholder priority budget doc. Portfolio type sets the target priority budget; invoke before priority-budget-walk. Triggers on "what kind of portfolio is this", "is this discovery or delivery", "how should we be allocating priority right now".
---

# Name the portfolio surface type

Read `${CLAUDE_PLUGIN_ROOT}/docs/Stakeholder priority budget.md` for surface-type definitions.

## Procedure

1. **Read what the org is actually trying to do** with this portfolio — not what the roadmap document presents. Cite the relevant strategy doc / OKR set / quarterly plan.

2. **Match to one of**:
   - **Discovery** — early-stage product, ambiguous market, hypothesis-testing. Initiatives are small, parallel, roughly equal. Communication cadence is low. Roadmap position is loose.
   - **Delivery** — executing on validated bets. Roadmap positions are clear. Resourcing is defined. Initiatives ladder to named OKRs. Executive sponsorship and communication cadence rise.
   - **Operations** — steady-state, maintaining a product line. Initiatives group by area. Cadence is small and consistent. Exec sponsorship reserved for cross-cutting bets.

3. **If ambiguous**, name both:
   - Which type the portfolio is *defaulting toward* (right now, by behavior)
   - Which it *should be* (per strategy intent)

## Output

```
Portfolio type (intent):     <discovery | delivery | operations>
Portfolio type (current):    <discovery | delivery | operations>  (may differ)
Reasoning: <one sentence grounded in the strategy intent, with cite for the source doc>
```

If current ≠ intent, name the gap explicitly — that is itself a finding. A "delivery portfolio" being managed as if it were "discovery" overspends on parallelism and underspends on focus; the reverse fails to ship.
