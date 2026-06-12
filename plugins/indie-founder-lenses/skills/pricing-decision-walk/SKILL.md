---
name: pricing-decision-walk
description: Walk ONE pricing page tier by tier as a decision surface — for each tier name its buyer, its anchor, its free→paid relationship, its single primary action, and its coherence with the landing page's price promise. Reports under-decided / well-decided / over-decided per tier. Pairs with pricing-constraint-map (run first to know what's pinned) and pricing-drift-audit (for a live page being tuned). For draft/live phases; for tuning-era drift use pricing-drift-audit.
---

# Walk the pricing page as a decision

Read `${CLAUDE_PLUGIN_ROOT}/docs/Pricing as a Decision Surface.md`. Assumes the pricing phase has been named and the target located (in-repo or pasted markup / URL / Stripe export — a pasted table is a normal target).

## Procedure

For each tier on the page, read it as a decision the visitor has to make — not as a row of features:

1. **Named buyer** — who is this tier *for*? A real buyer ("a freelancer billing clients"), or a non-buyer ("Pro", "you", "growing teams")? If the visitor has to do the sorting the page should have done, the tier is under-decided.
2. **Anchor** — what does this tier's price mean *against*? The tier above, a competitor, a manual cost, a struck-out price. A price with no reference leaves the visitor guessing whether it's cheap or dear.
3. **Free→paid relationship** — for the free/cheapest tier, what is the *first thing a visitor must pay to do*? Is that gate on the core value (free tier is a demo) or on a feature nobody reaches in their first session (page converts nobody)?
4. **Single primary action** — does this tier have exactly one thing it wants the visitor to do? Two equally-weighted CTAs ("start free" + "talk to sales") is one CTA doing two jobs — no decision designed.
5. **Coherence with the upstream promise** — does this tier honor what the landing page already promised about price ("free to start", "simple pricing", "\$X/mo")? A "free" CTA landing on a card wall breaks the decision at the boundary.

For each tier and each of the five reads: status (under-decided / well-decided / over-decided), with artifact cite.

**Spot the catalog tell**: is the page a price *list* rather than a decision surface? (Every tier "for you", no anchor anywhere, the free→paid gate unnamed, three equal buttons — the visitor has to make the whole decision themselves.) If so, that's the headline finding, above any single tier.

## Output

```
Phase: <draft | live | iterating>
Target: <pricing page / tier set / pasted table>

| Tier | Named buyer | Anchor | Free→paid | One CTA | Promise coherence |
|------|-------------|--------|-----------|---------|-------------------|
| Free | well-decided: "solo trying it out" | n/a | gate on team-sharing (pricing.tsx:40) | well-decided | matches "free to start" |
| Pro  | under-decided: "you" | over-decided: struck-out $99 with no referent | — | over-decided: 3 equal buttons | breaks "simple pricing" |

Catalog tell (if present):
  - Page reads as a price list, not a decision: <which reads are missing across all tiers>

Weakest decision on the page:
  - <tier>: <which read fails> — <cite>
```

The doc says: a price list answers "what do you sell?"; a decision surface answers "which one is for me, and what do I lose by picking cheaper?" If a tier can't answer the second question, that's the finding.
