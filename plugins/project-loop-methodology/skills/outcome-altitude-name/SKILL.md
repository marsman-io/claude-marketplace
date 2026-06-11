---
name: outcome-altitude-name
description: Name a project's organization altitude — output, activity, outcome, or status. Foundation for outcome-altitude-gap and outcome-drift-audit. Triggers on "what altitude is this project organized at", "is this output or outcome focused", "is the team tracking activity or change".
---

# Name the project altitude

Read `${CLAUDE_PLUGIN_ROOT}/docs/Intent as a PM Lens.md` (the altitude question section).

## Procedure

Examine how the target project is **organized** — what its status updates lead with, what its dashboards surface, what the team discusses in standup, what the stakeholders are shown. Then match to one of the canonical altitudes:

- **Output altitude** — organized around what got shipped. Release notes, completion lists, "we delivered X." Reports are lists of deliverables.
- **Activity altitude** — organized around what people are doing. Sprint boards, Gantt charts, "here is what the team is working on." Reports are lists of activity.
- **Outcome altitude** — organized around what should become true. OKRs, business value, stakeholder change. "Here is what changed for the customer / business." Reports are claims about state change.
- **Status altitude** — organized around current condition. Health dashboards, RAG status, blocker logs. "Here is where we are right now." Reports are snapshots.

Cite the artifact for what dominates (status doc filename, OKR page, sprint board).

## Output

```
Altitude:  <output | activity | outcome | status>
Evidence:
  - <artifact / cite> — <what leads, what gets the most space>
  - <secondary signal>

Hybrid?  <yes | no>
  If hybrid: <which altitudes mix, in what ratio>
```

A project running at output altitude that's grown an OKR section at the top is now a hybrid — name it. Hybrids are not failures by default; they're failures when the mix isn't intentional.
