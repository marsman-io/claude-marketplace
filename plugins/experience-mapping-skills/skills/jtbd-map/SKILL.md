---
name: jtbd-map
description: >-
  Models WHY developers "hire" a tool — situation + motivation + outcome with
  deliberately NO persona (Ulwick ODI + Moesta switch/forces) — producing a job
  statement with functional/emotional/social layers, a four-forces switch grid
  (Push / Pull / Anxiety / Habit, each with a verbatim quote and a 1-5 strength;
  the switch fires when Push+Pull > Anxiety+Habit, where for dev tools Anxiety =
  migration cost / lock-in / breaking changes and Habit = existing scripts / muscle
  memory), and measurable desired-outcome statements mapped to DX KPIs. The switch
  is usually FROM a competitor SDK, a homegrown script, or raw curl, and there are
  often two distinct jobs (integrating developer vs operator/admin). Use when you
  need to understand adoption motivation rather than features or personas. Triggers
  on "jobs to be done", "jtbd", "what job are developers hiring this for", "switch
  interview", "why did they adopt", "desired outcomes", "forces of progress". NOT
  for persona work or feature lists — JTBD explicitly rejects personas.
---

# JTBD Map

A jobs-to-be-done map explains WHY a developer adopts a tool by modeling the situation, the motivation, and the desired outcome — with no persona, because JTBD holds that the job, not the demographic, predicts behavior (Ulwick ODI; Moesta switch/forces). It matters because dev-tool adoption is almost always a SWITCH away from something that already works well enough — a competitor SDK, a homegrown script, raw curl — and switches obey a force balance: progress happens only when Push (pain of the old) + Pull (draw of the new) outweighs Anxiety (migration cost, lock-in, breaking changes) + Habit (existing scripts, muscle memory). Map only Push and Pull and you'll predict adoptions that never happen, because for engineers Anxiety and Habit are huge. Often there are two jobs — the integrating developer and the operator/admin want different things — so map per surface where the jobs diverge.

## When to use

**Do**
- Use when you need the motivation and force balance behind adoption, not features.
- Use verbatim quotes from switch interviews for every force; strength 1-5 each.
- Use two job statements when integrator and operator have distinct jobs.

**Don't**
- Don't introduce personas, demographics, or roles-as-identity — JTBD rejects them.
- Don't write a feature list; outcomes are metrics to move, not capabilities to ship.
- Don't map only Push/Pull; Anxiety and Habit decide dev-tool switches.

## Procedure
1. Identify the job(s). If integrator and operator differ, write two. Cite the source (switch interview, review, issue, pasted transcript).
2. Write each job statement: `When [situation/trigger], I want to [motivation], so I can [expected outcome]`. Add Functional / Emotional / Social layers.
3. Name the FROM: what they switch away from (competitor SDK, homegrown script, raw curl). Cite it.
4. Build the four-forces grid: Push, Pull, Anxiety, Habit — each with a verbatim quote and a 1-5 strength. For dev tools, Anxiety = migration cost/lock-in/breaking changes; Habit = existing scripts/muscle memory.
5. Compute the balance: switch fires when Push+Pull > Anxiety+Habit. State whether it does, and which force blocks it.
6. Write measurable desired-outcome statements: `[minimize|increase] + [metric] + [object of control] + [context]`. Map each to a DX KPI (time-to-first-successful-call, time-to-detect-error, steps-to-authenticate).
7. If jobs differ by surface (CLI/SDK/REST/MCP), tag each job and outcome with its surface.

## Output
```
(a) Job statement(s)  [no persona]
  Job 1 (integrating developer): When <situation/trigger>, I want to <motivation>, so I can <outcome>.
    Functional: ...   Emotional: ...   Social: ...   Source: <cite>
  Job 2 (operator/admin), if distinct: When ..., I want to ..., so I can ...

(b) Four-forces switch grid   FROM: <competitor SDK | homegrown script | raw curl>  (cite)
  | Force                        | Verbatim quote                  | Strength 1-5 |
  | Push (pain of current)       | "..."                           | 4            |
  | Pull (draw of new)           | "..."                           | 4            |
  | Anxiety (migration/lock-in/  | "..."                           | 3            |
  |   breaking changes)          |                                 |              |
  | Habit (scripts/muscle memory)| "..."                           | 3            |
  Balance: Push+Pull (8) vs Anxiety+Habit (6) → switch likely; blocker = Anxiety (migration)

(c) Desired-outcome statements (→ DX KPI)   [surface tag where jobs differ]
  O1: minimize  time   to first successful call   when integrating   → time-to-first-successful-call  [SDK]
  O2: minimize  steps  to authenticate            on first run       → steps-to-authenticate          [CLI]
  O3: increase  speed  to detect an error         while operating    → time-to-detect-error           [dashboard]
```
*If a persona appears, any force lacks a verbatim quote or strength, or outcomes read as features instead of `[verb]+[metric]+[object]+[context]`, it isn't a JTBD map — redo steps 1, 4, and 6.*
