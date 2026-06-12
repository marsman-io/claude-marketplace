---
name: founder-focus-squint
description: Run the squint test on a founder's roadmap, backlog, or bet shortlist — blur impact labels, "must-do" tags, and ordering. Which bet still leads by actual spend? Which dissolves into the middle? Which screams without earning it? Pairs with founder-focus-walk; run after.
---

# Run the founder focus squint test

Read `${CLAUDE_PLUGIN_ROOT}/docs/Founder focus budget.md`.

## Procedure

Read the target roadmap / backlog / bet shortlist. Mentally:

1. **Blur the labels.** Strip out "high impact", "P0", "must-do", emojis, the date added, and the ordering. Imagine the bets as a flat list carrying only their actual outcome prominence, evidence backing, scope commitment, validation coverage, and attention cadence.
2. **Identify what still leads** — bets whose *real spend* (a named outcome with evidence behind it) marks them as clearly more important than the rest.
3. **Identify what vanishes** — bets whose label says "high impact" but whose actual spend says afterthought: no named outcome, no evidence, no validation target.
4. **Identify what screams** — bets whose spend is wildly disproportionate to the outcome they'd move: a quarter of scope behind one customer email, daily attention on a copy tweak.

## Output

```
Bets that survive squinting (lead by actual spend):
  - <bet>: <cite> — held by <which mechanism is most differentiated>
  - ...

Bets that vanish (under-spent for stated impact):
  - <bet>: <cite> — labeled "high impact" but no named outcome / no evidence / no validation target
  - ...

Bets that scream (over-spent for the outcome they'd move):
  - <bet>: <cite> — quarter of scope behind one email, or daily attention on a low-risk tweak
  - ...

Verdict:
  Roadmap survives squinting? <yes | no | partial>
  Where does it fail? <one sentence>
  Smallest correction: <one specific mechanism to remove from one specific bet>
```

The doc's prescription: *remove the weakest separator and check whether focus reappears*. Verdict should favor subtraction — taking a bet off the board, not adding another must-do tag. Adding tags dilutes the signal that's already there.
