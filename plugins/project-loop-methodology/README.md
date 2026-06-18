# project-loop-methodology

Phase-aware diagnostic skills that critique agentic product work
through six PM-derived lenses. Read-only critics, not implementers —
each produces a structured finding the builder can act on.

This plugin is tuned for an indie product builder / vibe-coder who
delegates work to agents and then needs product judgment: did the thing
the agents built match the intent? The PM skillset still matters, but the
default artifacts are prompts, issues, diffs, screenshots, tests, logs,
demos, and acceptance notes. Linear issues, OKRs, stakeholders, roadmaps,
and status reports are useful only when they actually exist; the skills
must not require them or infer an institutional operating system.

## What's new

This plugin is now **all skills, no agents**. The `project-loop` orchestrator
skill detects the phase (charter / plan / execute / adjust / replan) and
composes the right leaf-skill chain. Single-lens requests auto-route straight
to the matching leaf skills.

## The orchestrator + the four lenses

`project-loop` is the meta-skill: it walks perception → abstraction → action
→ feedback, composing the lens skills the phase needs. To run a single lens
end-to-end, jump straight to its leaf skills:

| Lens | Grounding doc | Leaf skills (phase-aware) |
|---|---|---|
| intent verification | `Intent verification.md` | `acceptance-criteria-build` (before a build), `built-intent-check` (gaps + drift after) |
| outcome altitude | `Intent as a PM Lens.md` | `outcome-altitude-name` + `outcome-altitude-gap` (charter/plan), `outcome-drift-audit` (execute/replan) |
| constraint | `Constraint-based project management.md` | `project-constraint-build` (charter/plan), `project-constraint-audit` (execute/replan), `project-impact-trace` (adjust) |
| priority | `Priority budget.md` | `project-surface-type` + `priority-budget-walk` + `priority-squint-test` (single initiative), `priority-budget-audit` (cross-feature drift) |

## Skills (procedures)

| Skill | When invoked |
|---|---|
| `project-loop` | The orchestrator — phase-detects, then composes the lens skills below |
| `project-phase-detect` | First in the orchestrator — detects charter / plan / execute / adjust / replan |
| `acceptance-criteria-build` | Author behavioral, riskiest-first acceptance criteria before delegating a task |
| `built-intent-check` | Check a built artifact against intent — gaps (missing) + drift (unasked-for) |
| `project-surface-type` | Name discovery / delivery / operations mode before walking the budget |
| `priority-budget-walk` | Walk the 5 mechanisms on one feature / issue / bet |
| `priority-squint-test` | Validate that the priority spending reads |
| `priority-budget-audit` | Cross-feature / cross-issue drift detection (mature) |
| `outcome-altitude-name` | Name output / activity / outcome / status altitude |
| `outcome-altitude-gap` | Single-project gap check |
| `outcome-drift-audit` | Cross-feature / cross-surface altitude drift |
| `project-constraint-build` | Model a new project's constraint cascade |
| `project-constraint-audit` | Find broken pins / drifted inputs / exhausted slack |
| `project-impact-trace` | Blast-radius for a single proposed change request |

## Lens docs (the grounding)

| Doc | Codifies |
|---|---|
| `Project Loop.md` | perception → abstraction → action → feedback, PM-framed |
| `Intent as a PM Lens.md` | intent owner + intended user, the PM knob framework, outcome altitude |
| `Intent verification.md` | acceptance criteria as a refusal mechanism, generator ≠ critic, gap vs drift, riskiest-first |
| `Constraint-based project management.md` | hard pins vs soft inputs, the PM triangle, dependency graphs |
| `Priority budget.md` | finite builder attention / agent-cycle budget, 5 mechanisms, squint test |
| `Project lifecycle.md` | charter / plan / execute / adjust / replan — and how each lens reads per phase |

All six travel with the plugin under `docs/`, referenced by the skills
via `${CLAUDE_PLUGIN_ROOT}/docs/`.

## Layout

```
.claude-plugin/plugin.json
skills/
  project-loop/SKILL.md              # the phase-routing orchestrator
  project-phase-detect/SKILL.md
  acceptance-criteria-build/SKILL.md
  built-intent-check/SKILL.md
  project-surface-type/SKILL.md
  ...
docs/
  Project Loop.md
  Intent as a PM Lens.md
  Intent verification.md
  Constraint-based project management.md
  Priority budget.md
  Project lifecycle.md
README.md
```

## Conventions all the skills enforce

- **Read-only.** They diagnose; you intervene.
- **Phase-aware.** The orchestrator runs `project-phase-detect` first, then branches.
- **Doc-grounded.** Skills read their lens doc before executing.
- **Artifact-cited.** No finding without an artifact reference (prompt, issue, diff, screenshot, test output, demo note, trace, or optional planning artifact).
- **Institution-light.** Do not assume Linear, Jira, OKRs, stakeholders, roadmaps, analytics, or a large user base. Use them only when the workspace provides them.
- **Single target.** One project, feature, issue, change request, or product area per invocation.
- **No roadmaps.** Smallest next intervention only, not a grand plan.
- **No invented gaps.** A confirmed alignment is a valid finding.

## Override the methodology in your workspace

The skills prefer a consumer workspace's *own* copy of any lens doc when
one exists at the workspace root. Drop a tuned `Project Loop.md` (or any
of the five) at your workspace root, and the matching skill will use
yours instead of the plugin's copy. Falls back to the plugin's docs
otherwise.

## Sibling plugin

The peer plugin in this marketplace, `design-loop-methodology`, applies the
same four lenses to UI / design surfaces. Both are derived from the same
underlying four conceptual lenses (loop, intent, constraint, hierarchy)
plus a lifecycle taxonomy — but framed for different surfaces: UI design
work on one side, agentic product-building work on the other. The PM side
adds a sixth lens the design side doesn't need — `intent-verification`,
for checking that a build delegated to a black-box agent actually matches
what was asked.
