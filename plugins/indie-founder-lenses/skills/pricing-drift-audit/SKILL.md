---
name: pricing-drift-audit
description: Audit a LIVE pricing page that's being tuned for pin drift — find where a pinned constraint (named buyer, anchor, free→paid gate, one CTA per tier, the upstream price promise) has silently become a flex while the founder tuned amounts/tiers, and where a flex has frozen into a pin for no remembered reason. Surfaces the re-decision the founder made without noticing it was a re-decision of the whole surface. For the iterating phase. Use pricing-decision-walk for a single read of a draft/live page, and pricing-constraint-map to establish the pins first.
---

# Audit the pricing page for pin drift

Read `${CLAUDE_PLUGIN_ROOT}/docs/Pricing as a Decision Surface.md`. For the iterating phase — a live page the founder is actively tuning. Assumes the target is located (in-repo or pasted markup / URL / Stripe export) and ideally that `pricing-constraint-map` has named the current pins.

## Procedure

The danger in a tuned pricing page is not a wrong number — amounts are flexes. The danger is a **pin that drifted into a flex** while the founder thought they were making a tweak.

1. **Establish the current pins** (per `pricing-constraint-map`): named buyer per tier, anchor, free→paid gate, one CTA per tier, the upstream price promise.
2. **Reconstruct what each pin *was*.** Use git history on the pricing files (`git log -p -- <pricing route/component/constants>`), Stripe Price history if visible, prior pasted versions, or the landing page's still-standing promise. For each pin, compare then vs now.
3. **Find the silent re-decisions** — a pin that moved without the rest of the surface being re-decided:
   - The **anchor** vanished (a struck-out "\$99" became a bare "\$49") — the reference that gave the price meaning is gone.
   - The **free→paid gate** quietly shifted to a different feature — the free tier now demos something else, or paywalls the core value.
   - A tier's **named buyer dissolved into "you"** — the tier no longer sorts anyone.
   - A second equal **CTA** crept in — the tier's one action became two.
   - The page now **contradicts the landing promise** — "simple pricing" upstream, four tiers plus an add-on grid here.
4. **Find frozen flexes** — a flex (an amount, a tier count, a billing default) treated as untouchable for no reason anyone remembers, blocking a tune that would help.
5. **Name the systemic drift**, not a per-tier list. The deliverable is *which pin the founder moved while calling it a tweak* — the re-decision made without noticing.

## Output

```
Phase: iterating
Target: <pricing page / tier set>
Compared against: <git history / Stripe Price history / prior pasted version / landing promise>

Pin drift (pins that silently became flexes):
  1. <pin>: was <then> -> now <now> — re-decided the surface without re-deciding it (cite)
  2. ...

Frozen flexes (flexes treated as pins for no remembered reason):
  - <flex>: held at <value> blocking <the tune it prevents>

Systemic drift (the headline):
  <the one pin moved-as-a-tweak — what re-decision it silently forced>

Recommended next step (re-decide, don't just re-tune):
  Re-decide <which pin> on purpose, then let the flexes follow. Subtract a tier / a CTA before adding one.
```

The doc's discipline: the issue list is a projection of the decision model, not the model. Tuning amounts while the buyer, the anchor, and the gate drift unnoticed is the failure this audit exists to catch.
