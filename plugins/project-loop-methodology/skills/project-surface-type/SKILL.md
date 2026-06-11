---
name: project-surface-type
description: Name a product work mode — discovery, delivery, or operations — per the priority budget doc. Work mode sets the target priority budget; invoke before priority-budget-walk. Triggers on "what kind of work is this", "is this discovery or delivery", "how should we allocate priority right now".
---

# Name the work mode

Read `${CLAUDE_PLUGIN_ROOT}/docs/Priority budget.md` for work-mode definitions.

## Procedure

1. **Read what the builder is actually trying to do** with this target — not what the issue label or prompt urgency says. Cite the relevant intent note, issue, prompt, README, demo note, screenshot, `CLAUDE.md`, or optional strategy artifact.

2. **Match to one of**:
   - **Discovery** — ambiguous idea, unknown user behavior. Bets are small, parallel probes. Context and fast evidence matter more than broad implementation or deep review.
   - **Delivery** — executing on validated behavior. Intent prominence should be clear. Implementation focus should be defined. Verification coverage rises on the paths that matter.
   - **Operations** — steady-state bugs, reliability, cleanup. Work groups by area. Review cadence is small and consistent. Broad context is reserved for rare cross-cutting failures.

3. **If ambiguous**, name both:
   - Which mode the work is *defaulting toward* (right now, by behavior)
   - Which it *should be* (per delegated intent)

## Output

```
Work mode (intent):     <discovery | delivery | operations>
Work mode (current):    <discovery | delivery | operations>  (may differ)
Reasoning: <one sentence grounded in the delegated intent, with cite for the source artifact>
```

If current != intent, name the gap explicitly — that is itself a finding. A delivery feature being managed as discovery overspends on probes and underspends on verification; the reverse over-commits before learning.
