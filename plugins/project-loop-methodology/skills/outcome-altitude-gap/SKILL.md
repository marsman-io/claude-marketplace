---
name: outcome-altitude-gap
description: Check ONE project's gap between stakeholder intent altitude and the project's actual organization altitude. For charter/plan/adjust phase, where you're examining whether one project aligns. For mature portfolios use outcome-drift-audit.
---

# Check the outcome altitude gap

Read `${CLAUDE_PLUGIN_ROOT}/docs/Intent as a PM Lens.md`. Assumes the altitude is named (see `outcome-altitude-name` skill).

## Procedure

1. **Name the stakeholders.** Who is this project for? Customer segment, internal team, exec, board, regulator. Role + level of expertise + what triggered the project.
2. **Name the intent.** What should become true for those stakeholders? Outcome, not output. List sub-intents in rough priority order:
   - The primary outcome
   - The secondary outcomes
   - The "if-everything-goes-well" upside
3. **Get the current altitude** (from `outcome-altitude-name`).
4. **Calculate the gap.** In one sentence: "This is at *X* altitude when intent sits at *Y* altitude."
5. **Name the consequence.** What does the stakeholder have to do *extra* because of the mismatch? What story can they not tell? What decision can they not make?

If the gap is zero, say so plainly. A confirmed alignment is a valid finding.

## Output

```
Stakeholders: <list with role + expertise + why they care>
Intent:       <outcomes they want, in priority order>
Current altitude:  <from outcome-altitude-name>
Intent altitude:   <what the project *should* be organized around>

Gap:          "This is at <X> altitude when intent sits at <Y> altitude."
Consequence:  <what the stakeholder has to do extra, what decision they can't make, what story they can't tell>
```

Do not propose how to close the gap. That is the next loop's action stage; this skill only *names* the gap.
