---
name: founder-work-mode
description: Name a solo founder's work mode — searching, growing, or sustaining — per the founder focus budget doc. Work mode sets how much a roadmap should differentiate between bets; invoke before founder-focus-walk. Triggers on "what mode am I in", "is this pre-PMF or growth", "how much should my bets differ right now", "are we searching or growing".
---

# Name the founder work mode

Read `${CLAUDE_PLUGIN_ROOT}/docs/Founder focus budget.md` for work-mode definitions.

## Procedure

1. **Read what the founder is actually trying to do** with this roadmap or bet — not what the impact labels say. Cite the relevant roadmap entry, README, `CLAUDE.md`, intent note, analytics dashboard, or pasted backlog. If the bets aren't in-repo, ask for the pasted roadmap.

2. **Match to one of**:
   - **Searching** — pre-PMF; you don't yet know what moves the number. Bets are small, parallel, cheap probes against activation and retention. Evidence-gathering and fast validation matter more than deep scope or daily attention; bets should be roughly equal.
   - **Growing** — you've found something that works and are pushing on it. One or two bets carry clear outcome prominence and committed scope; the rest stay flat. Validation coverage rises on the revenue/retention paths that matter.
   - **Sustaining** — steady revenue; the job is to not lose it. Bets group by retention-defense and reliability. Attention cadence is light and consistent; deep scope is reserved for the rare existential fix; most bets stay small.

3. **If ambiguous**, name both:
   - Which mode the founder is *defaulting toward* (right now, by behavior — what the bets actually look like)
   - Which it *should be* (per the outcome they say they're chasing)

## Output

```
Work mode (intent):     <searching | growing | sustaining>
Work mode (current):    <searching | growing | sustaining>  (may differ)
Reasoning: <one sentence grounded in the named outcome, with cite for the source artifact>
```

If current != intent, name the gap explicitly — that is itself a finding. A growing founder running their roadmap like searching overspends on probes and under-commits to the bet that's working; the reverse over-commits a quarter before learning anything.
