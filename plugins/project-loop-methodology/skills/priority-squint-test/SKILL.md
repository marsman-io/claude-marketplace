---
name: priority-squint-test
description: Run the squint test on a product work queue, issue cluster, or feature set — blur labels, urgency words, and task order. What still leads? What dissolves into the middle? What screams without earning it? Pairs with priority-budget-walk; run after.
---

# Run the priority squint test

Read `${CLAUDE_PLUGIN_ROOT}/docs/Priority budget.md`.

## Procedure

Read the target work queue / issue cluster / feature set. Mentally:

1. **Blur the labels.** Strip out "P0/P1/P2", "urgent", emojis, and ordering. Imagine the work as a list of tasks with their actual intent prominence, context allocation, implementation focus, verification coverage, and review cadence.
2. **Identify what still leads** — targets whose *real spend* marks them as clearly more important than the rest.
3. **Identify what vanishes** — targets whose label says "priority" but whose actual spend says "afterthought."
4. **Identify what screams** — targets whose spend is wildly disproportionate to their stated value.

## Output

```
Targets that survive squinting (lead by actual spend):
  - <target>: <cite> — held by <which mechanism is most differentiated>
  - ...

Targets that vanish (under-spent for stated priority):
  - <target>: <cite> — labeled "P0" but no acceptance shape / no verification / no context
  - ...

Targets that scream (over-spent for stated value):
  - <target>: <cite> — low-risk copy issue with full-app context, broad implementation, and repeated review
  - ...

Verdict:
  Work survives squinting? <yes | no | partial>
  Where does it fail? <one sentence>
  Smallest correction: <one specific mechanism to remove from one specific target>
```

The doc's prescription: *remove the weakest separator and check whether priority reappears*. Verdict should favor subtraction. Adding more P0 tags doesn't add clarity; it dilutes the signal that already exists.
