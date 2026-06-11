---
name: squint-test
description: Run the squint test from the hierarchy doc — imagine the screen blurred or stripped of color and labels. What structure survives, what dissolves, what screams? Validates whether the budget spending is actually working. Pairs with differentiation-budget-walk; run after.
---

# Run the squint test

Read `${CLAUDE_PLUGIN_ROOT}/docs/How to arrive at hierarchy clarity.md`.

## Procedure

Read the target screen's source. Mentally render it, then:

1. **Blur or strip out color and labels.** Imagine the screen as a grayscale, label-free arrangement of shapes.
2. **Identify which boundaries survive** — these are clearly drawn through whitespace, border, or background.
3. **Identify which boundaries vanish** — these are under-spent. Two groups bleed into each other.
4. **Identify which boundaries scream** — these are over-spent. A region demands attention even with no semantic reason to.

## Output

```
Boundaries that survive (clearly drawn):
  - <region>: <file:line> — held by <which mechanism>
  - ...

Boundaries that vanish (under-spent):
  - <region>: <file:line> — nothing separates this from <neighbor>
  - ...

Boundaries that scream (over-spent):
  - <region>: <file:line> — competing for attention with <neighbor>
  - ...

Verdict:
  Hierarchy survives squinting? <yes | no | partial>
  Where does it fail? <one sentence>
  Smallest subtraction that would fix it: <one specific mechanism to remove from one specific region>
```

The doc's prescription: when in doubt, *remove the weakest separator and check whether hierarchy reappears*. Verdict should favor subtraction.
