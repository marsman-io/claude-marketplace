---
name: differentiation-budget-walk
description: Walk the five mechanisms of visual hierarchy spending on ONE screen — whitespace, border, background contrast, shadow, color. Reports under-spent / well-spent / over-spent per mechanism with file:line citations. Pairs with surface-type-name (run first) and squint-test (run after). For bootstrap/apply/tweak phases; for cross-screen audit use differentiation-budget-audit.
---

# Walk the five mechanisms

Read `${CLAUDE_PLUGIN_ROOT}/docs/How to arrive at hierarchy clarity.md`. Assumes the surface type has been named.

## Procedure

For each of the five mechanisms, examine the target screen's source (JSX/TSX, CSS, the tokens it consumes):

1. **Whitespace** — rhythm and grouping. Are there visible gaps between groups? Does padding decay with hierarchy depth? Or is everything equidistant?
2. **Border** — structural division between regions. Where are borders, and what's on the other side of each? Is every region bordered?
3. **Background contrast** — grouping things that belong together. Where do background changes mark a region?
4. **Shadow** — elevation; "this floats above the page." Is shadow reserved for true overlays, or applied to ordinary cards?
5. **Color** — state and meaning. Where does color carry semantic weight (active state, status, destructive)? Where is it decorative?

For each: status (under-spent / well-spent / over-spent), with file:line citations.

Additionally **spot the stacking**: any boundary marked with multiple mechanisms? (Border AND background AND shadow on the same region is the canonical failure.) List every stacking violation.

## Output

```
Surface type: <from surface-type-name>

| Mechanism | Status | Evidence |
|-----------|--------|----------|
| Whitespace | well-spent | 24px between cards at Spike.tsx:182 |
| Border | over-spent | borders on every card, section, AND group container |
| Background contrast | … | … |
| Shadow | … | … |
| Color | … | … |

Stacking violations:
  - <file:line>: border + background + shadow on same boundary
  - …
```

The doc says: each mechanism does *exactly one job*. If a mechanism is doing two, that's the finding.
