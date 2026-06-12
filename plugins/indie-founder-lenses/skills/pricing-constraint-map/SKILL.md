---
name: pricing-constraint-map
description: Map a pricing page's constraints into PINNED (must not silently move — named buyer per tier, anchor, free→paid gate, one CTA per tier, the upstream price promise) vs FLEXING (tune freely — amounts, tier count, feature placement, billing framing, row order), then check each flex against the doc's failure modes at the extremes. Recasts pinned-vs-flexes constraint thinking onto pricing. Pairs with pricing-decision-walk (reads each tier as a decision). For draft/live phases; for tuning-era pin drift use pricing-drift-audit.
---

# Map the pricing page's pins and flexes

Read `${CLAUDE_PLUGIN_ROOT}/docs/Pricing as a Decision Surface.md`. Assumes the pricing phase has been named and the target located (in-repo or pasted markup / URL / Stripe export).

## Procedure

Every pricing page is a set of constraints whether the founder said so or not. Sort them, then check the flexes for mistuning.

1. **List the pins.** For each, state whether it is *decided* and where:
   - **Named buyer per tier** — who each tier is for.
   - **Anchor** — what the anchor tier anchors to (tier above, competitor, manual cost, struck-out price).
   - **Free→paid gate** — the single line between free and paid; what the first paid thing is.
   - **One CTA per tier** — exactly one primary action per tier.
   - **Upstream price promise** — what the landing page already promised about price.

   For each pin: decided / undecided / drifted, with cite. An undecided pin at draft is an open question; an undecided pin live is a gap.

2. **List the flexes** and check each against the failure modes at the extremes (from the doc):
   - **Dollar amounts** — too low (product reads trivial, upgrade has nowhere to go) / too high with no anchor (no reference to judge against).
   - **Tier count** — too few (distinct buyers forced into one box) / too many (decision becomes a spreadsheet).
   - **Feature placement** — gates too granular (reads as nickel-and-diming) / free tier too generous (free tier *is* the product) / too thin (paywall with extra steps).
   - **Billing framing** — monthly vs annual default; is the framing tuned or accidental?
   - **Row order / grouping** — does the order help the decision or bury it?

   For each flex: in-range / mistuned (which extreme), with cite.

3. **Name the boundary cases**: any pin being treated like a flex (the dangerous one), or any flex frozen into a pin for no remembered reason.

## Output

```
Phase: <draft | live | iterating>
Target: <pricing page / tier set / pasted table>

Pinned (must not silently move):
  | Pin                    | State     | Evidence                              |
  | Named buyer per tier   | decided   | each tier names a real buyer (pricing.tsx) |
  | Anchor                 | undecided | no referent on any tier               |
  | Free→paid gate         | drifted   | gate moved from sharing to export, page not re-decided |
  | One CTA per tier       | decided   | one primary action per tier           |
  | Upstream price promise | decided   | "free to start" honored by Free tier  |

Flexing (tune freely; flagged only if past an extreme):
  - Tier count: mistuned — 5 tiers, decision reads as a spreadsheet (failure: too many)
  - Amounts: in-range
  - Feature placement: mistuned — free tier covers the core value (failure: too generous)

Boundary cases:
  - Pin treated as a flex: <which> — <the re-decision that wasn't made>
  - Flex frozen as a pin: <which> — <no remembered reason>
```

The doc's discipline: changing a pin is a re-decision of the whole surface; changing a flex is a tweak. The most important finding is a pin that has been treated like a flex.
