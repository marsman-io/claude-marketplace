---
name: altitude-name
description: Name a UI screen's organization altitude — data-model, action, intent, or state. Foundation for the intent-altitude-gap and intent-drift-audit skills. Triggers on "what altitude is this", "how is this organized", "is the data model leading", "what dominates this screen".
---

# Name the altitude

Read `${CLAUDE_PLUGIN_ROOT}/docs/Intent as a Design Lens.md`.

## Procedure

Examine how the target screen is **organized** — what it leads with, what gets the most weight, what dominates the eye. Then match to one of the canonical altitudes:

- **Data-model altitude** — schema-organized. A flat list of every field, every token, every row. The screen surfaces what the data layer has, in roughly that shape.
- **Action altitude** — operation-organized. A toolbar of buttons; verbs first. The screen surfaces what the user can do, in that order.
- **Intent altitude** — outcome-organized. A small set of decisions, or a guided flow that moves toward an outcome. The screen surfaces *the user's goal*.
- **State altitude** — what's-happening-organized. A dashboard of live values. The screen surfaces *current condition*.

Cite the file:line for what dominates.

## Output

```
Altitude:  <data-model | action | intent | state>
Evidence:
  - <file:line> — <what's leading the screen, what gets most visual weight>
  - <file:line> — <secondary signal>

Hybrid?  <yes | no>
  If hybrid: <which altitudes mix, in what ratio>
```

A screen at intent altitude that's grown an action toolbar at the top is now a hybrid — name it. Hybrids are not failures by default; they're failures when the mix isn't intentional.
