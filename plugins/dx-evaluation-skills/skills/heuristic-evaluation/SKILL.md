---
name: heuristic-evaluation
description: >-
  Judges a surface against recognized usability principles and logs each violation with the principle it breaks and a severity 0–4. Uses Nielsen's 10 heuristics PLUS a developer-experience supplement (Nielsen sanctions category-specific heuristics), shifting weight for dev tools toward system status, consistency, error prevention, and error recovery — covering idempotency, copy-pasteable runnable examples, observable state, structured output as a versioned contract, actionable machine-readable errors, safe mutation, safe upgrades, and dual DX+AX (human and agent) usability. Use for an expert principle-level pass over one surface. Triggers on "heuristic evaluation", "nielsen heuristics", "usability review", "expert review", "evaluate against usability principles", "dx heuristics". NOT for walking one task flow's learnability step by step (→ cognitive-walkthrough) or building a structured error inventory (→ failure-state-matrix).
---

# Heuristic Evaluation

Heuristic evaluation is an expert inspection: you examine one surface against a checklist of recognized usability principles and log every violation with the principle it breaks and a severity from 0 (not a problem) to 4 (catastrophic). It is fast, broad, and finds the diffuse problems a single task flow misses. Nielsen explicitly sanctions adding category-specific heuristics, so pair his 10 with a DX supplement — for developer tools the weight shifts hard toward system status, consistency, error prevention, and error recovery, because failure UX dominates real usage and because agents are first-class users that consume your output as a contract. This skill DIAGNOSES against principles; it does not edit product code — you intervene. A logged violation is not automatically a defect: context can justify it, so say so in the recommendation.

## When to use

**Do**
- Run 3–5 independent evaluator passes (or 3–5 framings) and merge; one pass finds a fraction of issues.
- Cite each violation with a location (file:line, command, exact help/error text, schema field, URL).
- Weight the DX supplement heavily for CLI/SDK/API/MCP/installer targets.
- Accept a pasted artifact (a `--help` dump, an OpenAPI spec, a tool schema, pasted markup). "Not in repo" is normal.

**Don't**
- Don't trace a single end-to-end task — that is cognitive-walkthrough.
- Don't list every error case as a row — that belongs in failure-state-matrix; here, log only the principle the error handling violates.
- Don't treat every violation as mandatory-fix; note where context justifies it.

## Procedure
1. Pick ONE surface and its persona (human, agent, or CI).
2. Pass 1 — Nielsen's 10: visibility of system status; match system & real world; user control & freedom; consistency & standards; error prevention; recognition over recall; flexibility & efficiency; aesthetic & minimalist design; help users recognize/diagnose/recover from errors; help & documentation.
3. Pass 2 — DX supplement: idempotent/re-runnable commands; copy-pasteable runnable examples in help/docs/errors; observable state (stdout=data, stderr=messages, report state changes); structured output as a versioned contract + semantic exit codes; actionable machine-readable errors (stable type/code + human description + a fix suggestion that is a runnable command + a `retryable` flag + echo of the failing input); safe mutation (`--dry-run`, confirm destructive, `--yes` for headless); version-compatibility clarity & safe upgrades (non-breaking by default, reversible); dual DX+AX (respect TTY detection and `NO_COLOR`/headless); non-interactive auth from env/CI.
4. Log each violation: location, issue, heuristic(s) broken, severity 0–4, recommendation.
5. Merge evaluator passes, dedupe, sort by severity.

## Output
```
Surface: <…>   persona: human|agent|CI   evaluators/passes: <n>

| # | Location / element | Issue | Heuristic(s) violated | Severity 0–4 | Recommendation |
|---|--------------------|-------|-----------------------|--------------|----------------|
| 1 |                    |       |                       |              |                |

Severity key: 0 none · 1 cosmetic · 2 minor · 3 major · 4 catastrophic
```

Failure mode: a single evaluator confirms their own taste and calls personal preference a "violation" — without 3–5 passes the log is one opinion wearing ten heuristics.

Sources: NN/g 10 usability heuristics; clig.dev (Command Line Interface Guidelines).
