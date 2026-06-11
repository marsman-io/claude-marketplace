---
name: acceptance-criteria-build
description: Author behavioral acceptance criteria for a task BEFORE delegating it to an agent — given/when/then statements that name observable states, ordered riskiest-first, covering happy path + at least one failure + at least one boundary. Produces criteria you can later refuse a result against. For charter/plan phase, or any time you're about to hand work to an agent. Pairs with built-intent-check (run after the agent builds).
---

# Build acceptance criteria before delegating

Read `${CLAUDE_PLUGIN_ROOT}/docs/Intent verification.md`. The goal is criteria you can *refuse a result against*, not a description of success.

## Procedure

1. **State the intent in one line.** What should become true for the user once this is built? Cite the source (intent note, issue, prompt, your own words). If you can't say it in one line, that's the first finding — the task isn't specified enough to build.

2. **Rank the unknowns riskiest-first.** List what this task is assuming. Score each by *how badly a wrong answer hurts × how unsure you are it's right*. The top of that list gets criteria first; a safe, certain assumption may need none.

3. **Write 3–7 criteria as given/when/then**, each naming an observable state — a response field, a screen, a stored value, an error message, a redirect — provable without asking the agent what it meant. Cover:
   - the **happy path** (1–2)
   - at least one **failure path** (bad input, denied permission, missing dependency)
   - at least one **boundary** (empty, max, duplicate, concurrent, unauthorized)
   Weight effort toward failure and boundary; the happy path is what the agent already optimizes for.

4. **Mark each criterion's risk tier** (from step 2) so the later check knows where to spend attention.

5. **Name what is explicitly out of scope** — behavior the agent must *not* add. This is your pre-registered drift tripwire.

## Output

```
Intent (one line): <what becomes true for the user> — cite: <source>

Acceptance criteria (riskiest-first):
  1. [high]  Given <…>, when <…>, then <observable state>
  2. [high]  Given <…> (failure), when <…>, then <observable error / refusal>
  3. [med]   Given <…> (boundary), when <…>, then <observable state>
  4. [low]   Given <…>, when <…>, then <observable state>

Out of scope (drift tripwires):
  - <behavior the build must NOT introduce>
  - <surface the task must NOT touch>

Unspecified risk: <any top-ranked unknown you could not turn into an observable criterion — flag it; it's the thing most likely to come back wrong>
```

If a high-risk assumption can't be turned into an observable criterion, say so plainly. An unobservable assumption is the one that comes back silently wrong.
