---
name: golden-path
description: >-
  Defines the single most direct, error-free route to first value — for a dev tool that is install → authenticate → first successful call (hello-world) → verify, with TTV measured as time-to-first-hello-world. The route is drawn as one branch-free flow that makes surface transitions and copy-paste handoffs explicit, friction-bearing steps, and is required to be expressible HEADLESS (env-var auth, `--yes`, scriptable) and IDEMPOTENTLY (re-running is safe) because agents and CI walk it too. Use to pin down the one canonical flow to first success. Triggers on "golden path", "happy path", "define the ideal path to first value", "the paved road to hello world", "what's the one canonical flow", "time to first call". NOT for error and recovery paths (→ failure-state-matrix) or the full branching task tree (→ task-analysis). Note the naming clash: the engineering "golden path / paved road" (a sanctioned internal workflow) is a DIFFERENT meaning — this is the UX one.
---

# Golden Path

The golden path is the single most direct, error-free route a user takes to first value: for a dev tool, install → authenticate → first successful call (hello-world) → verify, and the time-to-value metric here is time-to-first-hello-world (TTFHW). Keep it branch-free — one canonical sequence, no conditionals — because its job is to be the spine everything else hangs off. The happy path almost always crosses surfaces, so draw every surface transition and every copy-paste handoff as its own explicit, friction-bearing step rather than hiding them inside "authenticate". And because agents and CI walk this same path, it must be expressible headless (auth from env vars, `--yes` for prompts, fully scriptable) and idempotently (re-running causes no harm). One honest caveat to state up front: for dev tools the happy path is the least of your worries — most real user time is spent on failure paths — so define it cleanly, mark where the sad paths would branch off, hand those to failure-state-matrix, and do not over-invest here. This skill DIAGNOSES and defines the route; it does not edit product code — you intervene.

## When to use

**Do**
- Keep it to one branch-free sequence; if you are writing "if", you are in task-analysis or failure-state-matrix territory.
- Make each surface transition and copy-paste handoff its own row.
- Flag the whole path for headless-capable and idempotent, and estimate TTFHW.
- Mark the points where alternate/sad paths WOULD branch, and hand them off.
- Accept a pasted artifact (a quickstart URL, a `--help` dump, an OpenAPI spec). "Not in repo" is normal.

**Don't**
- Don't enumerate errors or recovery — that is failure-state-matrix.
- Don't model every variation of the goal — that is task-analysis.
- Don't over-invest; the golden path is the cheap part of DX.
- Don't confuse this with the engineering "paved road" sense.

## Procedure
1. State the persona (human / agent / CI) and the "first value" outcome (the hello-world).
2. Lay out one branch-free sequence: discover → install → authenticate → first-success → verify.
3. For each step record: user action, system response, entry condition, success signal — all cited.
4. Insert a discrete row for every surface transition and every copy-paste handoff.
5. Assess the whole path: headless-capable? idempotent? Estimate TTFHW.
6. Mark each point where an alternate or sad path would branch; label it for failure-state-matrix.

## Output
```
Persona: <…>   First value (hello-world): <…>
Path-level: headless-capable [Y/N] · idempotent [Y/N] · TTFHW estimate: <…>

| Step | User action | System response | Entry condition | Success signal |
|------|-------------|-----------------|-----------------|----------------|
| 1    | install …   |                 |                 |                |
| 2    | [SURFACE TRANSITION → dashboard] |   |       |                |
| 3    | [COPY-PASTE HANDOFF: API key]    |   |       |                |
| …    |             |                 |                 |                |

Sad-path branch points (→ failure-state-matrix):
- after step <n>: <what would go wrong here>
```

Failure mode: a golden path that quietly assumes an interactive TTY and a logged-in human is useless to the agents and CI runners that actually walk it first.

Sources: Google Design Sprint Kit (golden path); happy/golden/sad path literature.
