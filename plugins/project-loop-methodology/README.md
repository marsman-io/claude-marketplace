# project-loop-methodology

Four phase-aware diagnostic agents that critique any project or portfolio
through five conceptual PM lenses. Read-only critics, not implementers —
each produces a structured finding you (or the team) react to.

This plugin mirrors the design-loop-methodology shape, translated for the
PM persona: same perception/abstraction/action/feedback loop, the same
constraint-cascade and altitude framings, the same differentiation-budget
discipline — but the targets are projects, portfolios, charters, change
requests, and roadmaps instead of UI screens and design tokens.

## Agents (workflows)

| Agent | Lens | Phase-aware behavior |
|---|---|---|
| `project-loop` | the meta-loop | walks perception/abstraction/action/feedback, composing the lens skills the phase needs |
| `outcome-altitude` | `Intent as a PM Lens.md` | gap-check (charter/plan), drift-audit (execute/replan), before/after (adjust) |
| `project-cascade` | `Constraint-based project management.md` | constraint-build (charter/plan), constraint-audit (execute/replan), impact-trace (adjust) |
| `priority-budget` | `Stakeholder priority budget.md` | walk + squint (single initiative), audit (cross-portfolio drift) |

## Skills (procedures)

| Skill | When invoked |
|---|---|
| `project-phase-detect` | First in every agent — detects charter / plan / execute / adjust / replan |
| `project-surface-type` | Name discovery / delivery / operations portfolio before walking the budget |
| `priority-budget-walk` | Walk the 5 mechanisms on one initiative |
| `priority-squint-test` | Validate that the priority spending reads |
| `priority-budget-audit` | Cross-portfolio drift detection (mature) |
| `outcome-altitude-name` | Name output / activity / outcome / status altitude |
| `outcome-altitude-gap` | Single-project gap check |
| `outcome-drift-audit` | Cross-portfolio altitude drift |
| `project-constraint-build` | Model a new project's constraint cascade |
| `project-constraint-audit` | Find broken pins / drifted inputs / exhausted slack |
| `project-impact-trace` | Blast-radius for a single proposed change request |

## Lens docs (the grounding)

| Doc | Codifies |
|---|---|
| `Project Loop.md` | perception → abstraction → action → feedback, PM-framed |
| `Intent as a PM Lens.md` | stakeholder intent, the PM knob framework, outcome altitude |
| `Constraint-based project management.md` | hard pins vs soft inputs, the PM triangle, dependency graphs |
| `Stakeholder priority budget.md` | finite priority budget, 5 mechanisms, squint test |
| `Project lifecycle.md` | charter / plan / execute / adjust / replan — and how each lens reads per phase |

All five travel with the plugin under `docs/`, referenced by agents and
skills via `${CLAUDE_PLUGIN_ROOT}/docs/`.

## Layout

```
.claude-plugin/plugin.json
agents/
  project-loop.md
  outcome-altitude.md
  project-cascade.md
  priority-budget.md
skills/
  project-phase-detect/SKILL.md
  project-surface-type/SKILL.md
  ...
docs/
  Project Loop.md
  Intent as a PM Lens.md
  Constraint-based project management.md
  Stakeholder priority budget.md
  Project lifecycle.md
README.md
```

## Conventions all four agents enforce

- **Read-only.** No `Edit`/`Write` tools. They diagnose; you intervene.
- **Phase-aware.** Every agent runs `project-phase-detect` first, then branches.
- **Doc-grounded.** Skills read their lens doc before executing.
- **Artifact-cited.** No finding without an artifact reference (charter doc, status report, sprint board, OKR page).
- **Single target.** One project, initiative, change request, or portfolio cluster per invocation.
- **No roadmaps.** Smallest next intervention only, not the next quarterly plan.
- **No invented gaps.** A confirmed alignment is a valid finding.

## Override the methodology in your workspace

The agents prefer a consumer workspace's *own* copy of any lens doc when
one exists at the workspace root. Drop a tuned `Project Loop.md` (or any
of the five) at your workspace root, and the matching skill will use
yours instead of the plugin's copy. Falls back to the plugin's docs
otherwise.

## Sibling plugin

The peer plugin in this marketplace, `design-loop-methodology`, applies the
same four lenses to UI / design surfaces. Both are derived from the same
underlying four conceptual lenses (loop, intent, constraint, hierarchy)
plus a lifecycle taxonomy — but framed for different practitioners
(designer vs. PM) with different surface types and different artifact
forms.
