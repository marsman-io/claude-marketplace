---
name: priority-squint-test
description: Run the squint test on a portfolio or roadmap — blur the labels and the P0/P1/P2 tags. What initiatives still lead? What dissolves into the middle? What screams without earning it? Pairs with priority-budget-walk; run after.
---

# Run the priority squint test

Read `${CLAUDE_PLUGIN_ROOT}/docs/Stakeholder priority budget.md`.

## Procedure

Read the target portfolio / roadmap. Mentally:

1. **Blur the labels.** Strip out the "P0/P1/P2" tags, the "🔥" emojis, the ordering. Imagine the portfolio as just a list of initiatives with their actual resourcing, sponsorship, OKR alignment, and cadence.
2. **Identify what still leads** — initiatives whose *real spend* (people, exec attention, communication) marks them as clearly more important than the rest.
3. **Identify what vanishes** — initiatives whose label says "priority" but whose actual spend says "afterthought."
4. **Identify what screams** — initiatives whose spend is wildly disproportionate to their stated priority.

## Output

```
Initiatives that survive squinting (lead by actual spend):
  - <initiative>: <cite> — held by <which mechanism is most differentiated>
  - ...

Initiatives that vanish (under-spent for stated priority):
  - <initiative>: <cite> — labeled "P0" but no resourcing / no sponsor / no OKR
  - ...

Initiatives that scream (over-spent for stated value):
  - <initiative>: <cite> — labeled "P2" but has 8 FTE, exec sponsor, and weekly all-hands
  - ...

Verdict:
  Portfolio survives squinting? <yes | no | partial>
  Where does it fail? <one sentence>
  Smallest correction: <one specific mechanism to remove from one specific initiative>
```

The doc's prescription: *remove the weakest separator and check whether priority reappears*. Verdict should favor subtraction. Adding more P0 tags doesn't add clarity; it dilutes the signal that already exists.
