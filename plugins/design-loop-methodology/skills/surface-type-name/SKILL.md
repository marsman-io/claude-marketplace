---
name: surface-type-name
description: Name a UI screen's surface type — reading, operating, or monitoring — per the hierarchy clarity doc. Surface type sets the target differentiation budget; invoke this BEFORE differentiation-budget-walk. Triggers on "what kind of surface is this", "is this a reading or operating screen", "what should this screen be".
---

# Name the surface type

Read `${CLAUDE_PLUGIN_ROOT}/docs/How to arrive at hierarchy clarity.md` for surface-type definitions.

## Procedure

1. **Read what the user came to do** on the target screen — not what the screen currently presents. Cite the route, the navigation context, the persona's likely intent.
2. **Match to one of**:
   - **Reading** — settings, docs, profiles, terms-of-service. Needs little differentiation; whitespace + typography carry it. Borders and color stay minimal.
   - **Operating** — data tables, work queues, admin consoles. Needs a lot of differentiation at low whitespace. Borders and background do the heavy lifting.
   - **Monitoring** — dashboards, status boards. Heavy grouping; cards and background contrast define regions.
3. **If ambiguous**, name both:
   - Which surface type it's *defaulting toward* (visually, right now)
   - Which it *should be* (per the user's actual intent altitude)

## Output

```
Surface type (intent):      <reading|operating|monitoring>
Surface type (current):     <reading|operating|monitoring>  (may differ)
Reasoning: <one sentence grounded in what the user came to do, with file:line cite for the screen entry point>
```

If current ≠ intent, name the gap explicitly — that is itself a finding.
