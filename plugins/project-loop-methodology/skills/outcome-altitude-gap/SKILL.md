---
name: outcome-altitude-gap
description: Check ONE product work target's gap between delegated intent altitude and actual organization altitude. For charter/plan/adjust phase, where you're examining whether one target aligns. For mature cross-feature work use outcome-drift-audit.
---

# Check the outcome altitude gap

Read `${CLAUDE_PLUGIN_ROOT}/docs/Intent as a PM Lens.md`. Assumes the altitude is named (see `outcome-altitude-name` skill).

## Procedure

1. **Name the intent owner and intended user.** The intent owner may be the builder. The intended user may be an end user, buyer, operator, admin, developer, or the builder using their own tool. Include role + what triggered the work.
2. **Name the intent.** What should become true for the intended user or builder? Outcome, not output. List sub-intents in rough priority order:
   - The primary outcome
   - The secondary outcomes
   - The "if-everything-goes-well" upside
3. **Get the current altitude** (from `outcome-altitude-name`).
4. **Calculate the gap.** In one sentence: "This is at *X* altitude when intent sits at *Y* altitude."
5. **Name the consequence.** What does the builder have to infer manually because of the mismatch? What can the user not do, understand, decide, trust, avoid, or recover from?

If the gap is zero, say so plainly. A confirmed alignment is a valid finding.

## Output

```
Intent owner:  <builder / requester / other>
Intended user: <role + why they care>
Intent:        <outcomes they want, in priority order>
Current altitude:  <from outcome-altitude-name>
Intent altitude:   <what the work *should* be organized around>

Gap:          "This is at <X> altitude when intent sits at <Y> altitude."
Consequence:  <what the builder must infer manually, or what the user still cannot do / understand / decide / trust>
```

Do not propose how to close the gap. That is the next loop's action stage; this skill only *names* the gap.
