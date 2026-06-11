---
name: intent-altitude-gap
description: Check ONE screen's gap between user intent altitude and the screen's actual organization altitude. For bootstrap/apply phase, where the system is new and you're examining whether one screen aligns. For mature systems (audit), use intent-drift-audit instead.
---

# Check the intent altitude gap

Read `${CLAUDE_PLUGIN_ROOT}/docs/Intent as a Design Lens.md`. Assumes the altitude is named (see `altitude-name` skill).

## Procedure

1. **Name who opens this screen.** Role, level of expertise, what triggered the visit. If multiple plausible personas, name them all and say which one the screen serves by default.
2. **Name the intent.** What should become true for that person? Outcome, not action. List sub-intents in rough likelihood order — primary, secondary, fallback.
3. **Get the current altitude** (from `altitude-name`).
4. **Calculate the gap.** In one sentence: "This is at *X* altitude when intent sits at *Y* altitude."
5. **Name the consequence.** What does the user have to do *extra* because of the mismatch? What are they fighting against?

If the gap is zero, say so plainly. A confirmed alignment is a valid finding.

## Output

```
Who:          <persona — role, expertise, trigger>
Intent:       <outcome they want — in priority order, comma-separated>
Current altitude:  <from altitude-name>
Intent altitude:   <what the screen *should* be organized around>

Gap:          "This is at <X> altitude when intent sits at <Y> altitude."
Consequence:  <what the user has to do extra, in concrete terms>
```

Do not propose how to close the gap. That is the next loop's action stage; this skill only *names* the gap.
