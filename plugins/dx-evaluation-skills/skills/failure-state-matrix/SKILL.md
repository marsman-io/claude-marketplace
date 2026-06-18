---
name: failure-state-matrix
description: >-
  Systematically inventories everything that can go wrong at each step of a flow — what the user sees, the real root cause, and how they recover — per (flow step × failure mode), per surface AND across the seam. This is the highest-leverage diagnostic for a dev tool, because failure UX dominates real usage and because errors are an AGENT'S ONLY recovery signal; empirically only ~47% of enterprise error states even offer a recovery action, so missing recovery is the most common gap. Covers CLI exit codes/stderr, SDK typed exceptions, REST stable JSON error codes and `Retry-After`, MCP structured parseable errors, dashboard delivery patterns, and installer/upgrade/rollback. Use to audit error handling and recovery. Triggers on "failure state mapping", "error state matrix", "what happens when it breaks", "audit the error handling", "recovery paths", "sad path review", "error UX". NOT for defining the ideal flow (→ golden-path) or principle-level critique (→ heuristic-evaluation).
---

# Failure State Matrix

The failure-state matrix is a systematic inventory of everything that can go wrong, built one cell per (flow step × failure mode): what triggers it, what the user actually sees, the real root cause underneath that message, and the concrete forward action that gets them unstuck. For a dev tool this is the single highest-leverage diagnostic, because nearly all real time is spent on failure paths and because an error is an agent's ONLY recovery signal — when only about 47% of enterprise error states offer any recovery action, the most common defect you will find is a dead end. Map it per surface and, critically, across the seam where a task hops surfaces. Hold every cell's microcopy to a bar: say WHAT happened, WHY, and HOW to fix it, in human language with no raw codes or jargon, placed near the source — and expose a code only when it maps to a documented resolution. Prioritize by severity × frequency, and require a recovery action on every non-transient row. This skill DIAGNOSES failure handling; it does not edit product code — you intervene.

## When to use

**Do**
- Drive the rows from a flow's steps (use golden-path / task-analysis) crossed with each plausible failure mode.
- Audit per surface AND add explicit rows for the cross-surface seam (expired key copied from dashboard, version drift between CLI and API).
- Demand a recovery path that is a forward action, not "OK" or "try again".
- Fill the machine columns for dev tools: machine-readable error type/code, retryable?, semantic exit code.
- Accept a pasted artifact (error output, an OpenAPI error schema, MCP tool error returns, installer logs). "Not in repo" is normal.

**Don't**
- Don't map the success route — that is golden-path.
- Don't critique against general principles — that is heuristic-evaluation.
- Don't accept a raw code or stack trace as the "message"; that fails the microcopy bar.

## Procedure
1. Lift the ordered flow steps from golden-path or task-analysis.
2. For each step, enumerate failure modes per surface (CLI, SDK, REST, MCP, dashboard, installer/upgrade) and at the seam.
3. For each cell capture: the trigger, exactly what the user sees (message + delivery pattern + exact microcopy), the actual root cause, the recovery path, and the owner.
4. Add machine columns: machine-readable error type/code, retryable?, semantic exit code.
5. Score the microcopy against the bar (what/why/how, human language, near the source).
6. Sort by severity × frequency; ensure every non-transient row has a forward recovery action.

## Output
```
Flow source: <golden-path | task-analysis cite>   Surface(s): <…>

| Flow step | Failure / trigger | What the user sees (message + pattern[inline/toast/banner/modal/full-page] + exact microcopy) | Actual root cause | Recovery path (forward action) | Owner | Machine error type/code | Retryable? | Exit code | Severity×Freq |
|-----------|-------------------|-----------------------------------------------------------------------------------------------|-------------------|--------------------------------|-------|-------------------------|------------|-----------|---------------|
|           |                   |                                                                                               |                   |                                |       |                         |            |           |               |

Per-surface checklist:
- CLI: nonzero exit code, stderr (not stdout), "did you mean?" suggestion
- SDK: typed exception, retryable flag, request-id surfaced
- REST: stable JSON error code, Retry-After, idempotency key honored
- MCP: structured error the model can parse (not bare "Error 422")
- Dashboard: correct toast/modal/banner delivery
- Installer/upgrade: version mismatch, partial upgrade, rollback path
```

Failure mode: a matrix that lists symptoms and codes but leaves the recovery column empty has documented the dead ends instead of removing them.

Sources: NN/g error-message guidelines; clig.dev; agent-CLI design guides.
