---
name: outcome-altitude-name
description: Name a product work target's organization altitude — output, activity, outcome, or status. Foundation for outcome-altitude-gap and outcome-drift-audit. Triggers on "what altitude is this organized at", "is this output or outcome focused", "is the agent tracking activity or user change".
---

# Name the project altitude

Read `${CLAUDE_PLUGIN_ROOT}/docs/Intent as a PM Lens.md` (the altitude question section).

## Procedure

Examine how the target work is **organized** — what its prompt leads with, what its issue emphasizes, what the diff changes, what screenshots / tests prove, what the agent summary reports, and what the intended user is shown. Then match to one of the canonical altitudes:

- **Output altitude** — organized around what got produced. Commits, changed files, generated components, release notes. Reports are lists of deliverables.
- **Activity altitude** — organized around what happened during work. prompts, task lists, agent logs, issue transitions, TODOs. Reports are lists of actions.
- **Outcome altitude** — organized around what should become true. Acceptance checks, demo paths, user-visible behavior, before/after screenshots. Reports are claims about state change for the user.
- **Status altitude** — organized around current condition. Failing tests, blockers, known gaps, unresolved questions. Reports are snapshots.

Cite the artifact for what dominates (prompt, issue, file, diff, screenshot, test output, demo note, or optional planning artifact).

## Output

```
Altitude:  <output | activity | outcome | status>
Evidence:
  - <artifact / cite> — <what leads, what gets the most space>
  - <secondary signal>

Hybrid?  <yes | no>
  If hybrid: <which altitudes mix, in what ratio>
```

A target running at output altitude that's grown an acceptance checklist at the top is now a hybrid — name it. Hybrids are not failures by default; they're failures when the mix isn't intentional.
