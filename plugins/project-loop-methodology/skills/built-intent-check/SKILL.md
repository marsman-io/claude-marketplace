---
name: built-intent-check
description: Check a built artifact against stated intent — walk the acceptance criteria for GAPS (asked-for behavior missing) and walk the inverse for DRIFT (behavior present that nobody asked for). Verifies against intent + observable behavior, never the building agent's own account of what it did. For execute/adjust phase, after an agent has built something. Pairs with acceptance-criteria-build (run first, ideally before the build).
---

# Check the built thing against intent

Read `${CLAUDE_PLUGIN_ROOT}/docs/Intent verification.md`. You verify against two things — the stated intent and the observable behavior — and never against the building agent's summary of what it did.

## Inputs

- The **intent / acceptance criteria** (from `acceptance-criteria-build`, an issue, or the original prompt). If none exist, reconstruct them from the stated intent first — you can't check against a bar that was never set.
- The **built artifact** — the diff, the running behavior, the screen, the response, the stored state. Prefer observed behavior over the agent's description of behavior.

## Procedure

1. **Walk the criteria for GAPS.** For each acceptance criterion, find the evidence that it holds — a test you ran, a screen you saw, a response field, a stored value. Mark each: met / unmet / unverifiable. "The agent says it works" is *unverifiable*, not met. Spend most attention on the high-risk-tier criteria.

2. **Walk the inverse for DRIFT.** Now ignore the criteria and ask: what does this build *do that nothing asked for*? Read the diff for behavior outside the intent — extra fields, silent defaults, new side effects, scope the agent expanded into, surfaces it touched that were marked out of scope. Drift won't show up in a criteria walk; this is the step that catches it.

3. **Separate verified from asserted.** Anything you couldn't confirm by behavior or intent goes in its own bucket. Do not launder the agent's self-report into a pass.

4. **Trace drift to a cause** where you can — usually under-specified intent (the agent filled a gap you left) rather than disobedience. That tells you whether to fix the spec or reject the build.

## Output

```
Intent checked against: <criteria source>
Artifact: <diff / running behavior / screen>

GAPS (asked for, not delivered):
  - [high] <criterion> — unmet: <what's missing, with evidence>
  - [med]  <criterion> — unverifiable: <why you couldn't confirm>

DRIFT (delivered, never asked for):
  - <behavior / field / side effect> — <where in the diff> — likely cause: <under-specified intent | scope expansion>

Verified-met:
  - <criterion> — evidence: <test / screen / value you observed>

Verdict: <matches intent | gaps only | drift only | gaps + drift>
Smallest next step: <re-spec one criterion | reject + constrain scope | accept | one behavior to verify by hand>
```

A build that passes every criterion can still be wrong — the verdict isn't clean until the drift walk comes back empty too.
