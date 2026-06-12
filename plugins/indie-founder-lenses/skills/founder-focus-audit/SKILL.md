---
name: founder-focus-audit
description: Audit focus drift ACROSS MANY bets on a founder's roadmap. Walks each bet's spending then finds cross-bet patterns — where mechanisms drift in usage, where the same bets accumulate all five mechanisms, where one mechanism has lost its single job (every bet "high impact", every bet "ship and see"). For in-flight/pivoting phase. Use founder-focus-walk for single-bet analysis.
---

# Cross-bet founder focus audit

Read `${CLAUDE_PLUGIN_ROOT}/docs/Founder focus budget.md` (and re-confirm the phase is in-flight or pivoting — many bets live at once).

## Procedure

1. **Enumerate the live bets.** Read the roadmap, backlog, open issues, in-progress branches/PRs, partial diffs, and any pasted bet list. List the bets. If they aren't in-repo, ask for the pasted roadmap.
2. **For each bet**: name its work mode (per `founder-work-mode`) and sample its spending across the five mechanisms (per `founder-focus-walk`). Sampling is fine; a full walk on every bet is not the goal — patterns are.
3. **Aggregate cross-bet**:
   - How many bets are tagged "high impact" / "must-do" / "P0"? More than 2-3 in flight means the tag has lost meaning.
   - Which bets accumulate multiple mechanisms (stacking patterns)?
   - Which bets have *zero* differentiation — no mechanism marks them as more or less important than the rest?
   - Has outcome prominence become decorative (every bet says high impact, none names a number on a surface)?
   - Has evidence backing become decorative (every bet justified by "a customer asked")?
   - Has scope commitment gone undeclared across the board (no bet states weeks or surface)?
   - Has validation coverage become decorative (every bet is "ship and see" instead of a metric target)?
   - Has attention cadence become reactive (revisiting bets from anxiety instead of from how much the result can't be trusted)?
4. **Surface the systemic drift**, not per-bet findings.

## Output

```
Bets audited: <N>
Work mode: <from founder-work-mode at the roadmap level>

Drift patterns:
  1. <pattern>: <N bets> — <e.g., "impact-adjective inflation: 9 of 12 bets are 'high impact'">
  2. <pattern>: <N bets> — ...

Mechanism-job violations (mechanism doing two jobs across the roadmap):
  - Validation coverage: <count> bets are "ship and see" — has lost its "this proves the outcome moved" job
  - Outcome prominence: <count> bets lead with an adjective, not a number on a surface — has lost its "this is the outcome we're betting on" job
  - ...

Recommended subtractive next step:
  Pick the most-spent mechanism (<which>), strip it from one cluster of bets (<which>), see if focus reappears. Subtract before you reprioritize.
```

The doc's discipline: focus comes from spending the budget well, not from adding more must-do tags. Audits should resolve to *what to take off the board*.
