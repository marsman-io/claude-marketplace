---
name: landing-altitude-name
description: Name a landing / conversion surface's organization altitude — feature, action, outcome, or identity. Foundation for the conversion-intent-gap and conversion-intent-drift-audit skills. Triggers on "what altitude is this landing page", "is the hero leading with features or the outcome", "how is this page organized", "what dominates this landing page", "is this page built around the product or the visitor".
---

# Name the landing altitude

Read `${CLAUDE_PLUGIN_ROOT}/docs/Intent as a Conversion Lens.md`.

## Procedure

Examine how the target page is **organized** — what the hero leads with, what gets the most weight, what a skimming stranger registers first, what the page is built around. Then match to one of the canonical altitudes:

- **Feature altitude** — product-organized. A grid of capabilities, a UI tour, a noun about the product in the hero ("the all-in-one X platform"). The page surfaces what the product *has*, leaving the visitor to translate it into what they get.
- **Action altitude** — operation-organized. CTAs first and everywhere; "Sign up / Start free / Book a demo" competing for weight. The page surfaces what the visitor *can do*, often before earning a reason to.
- **Outcome altitude** — change-organized. The hero is a promise about the visitor in their language ("ship your side project this weekend"), with one primary action falling out as the obvious conclusion. The page surfaces *what becomes true for the visitor*.
- **Identity altitude** — belonging-organized. A movement, a tribe, a stance ("for builders who ship", "join 40,000 founders"). The page surfaces *who the visitor becomes or belongs to*.

Cite the file:line, route, or pasted-line for what leads and what dominates.

## Output

```
Altitude:  <feature | action | outcome | identity>
Evidence:
  - <file:line / route / pasted line> — <what the hero leads with, what gets most weight>
  - <file:line / route / pasted line> — <secondary signal>

Hybrid?  <yes | no>
  If hybrid: <which altitudes mix, in what ratio — e.g. outcome hero over a feature-grid body>
```

An outcome-altitude hero sitting on a body that's a flat feature grid is a hybrid — name it. Hybrids are not failures by default; they're failures when the mix isn't intentional, or when a lower altitude is what the skimming visitor actually registers first.
