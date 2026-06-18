# design-loop-methodology

Phase-aware diagnostic skills that critique any design surface through
five conceptual lenses. Read-only critics, not implementers — each produces
a structured finding you (or your main loop) react to.

## What's new in 0.2.0

This plugin is now **all skills, no agents**. The `design-loop` orchestrator
skill detects which lifecycle phase your design system is in (bootstrap /
apply / audit / tweak / refactor) and composes the right leaf-skill chain
for that phase. Single-lens requests auto-route straight to the matching
leaf skills — no orchestrator round-trip needed.

The same lens reads very differently at different phases. The constraint
lens in bootstrap = *model the cascade* (`constraint-graph-build`); in tweak
= *trace blast radius* (`cascade-impact-trace`). The phase-detect-and-branch
pattern is explicit in the orchestrator skill's abstraction table.

## The orchestrator + the three lenses

`design-loop` is the meta-skill: it walks perception → abstraction → action
→ feedback, composing the lens skills the phase needs. To run a single lens
end-to-end, jump straight to its leaf skills:

| Lens | Grounding doc | Leaf skills (phase-aware) |
|---|---|---|
| intent | `Intent as a Design Lens.md` | `altitude-name` + `intent-altitude-gap` (bootstrap/apply), `intent-drift-audit` (audit) |
| constraint | `Constraint-based design.md` | `constraint-graph-build` (bootstrap), `constraint-graph-audit` (audit/refactor), `cascade-impact-trace` (tweak) |
| hierarchy | `How to arrive at hierarchy clarity.md` | `surface-type-name` + `differentiation-budget-walk` + `squint-test` (single screen), `differentiation-budget-audit` (cross-screen drift) |

## Skills (procedures)

| Skill | When invoked |
|---|---|
| `design-loop` | The orchestrator — phase-detects, then composes the lens skills below |
| `design-system-phase` | First in the orchestrator — detects bootstrap/apply/audit/tweak/refactor |
| `surface-type-name` | Name reading/operating/monitoring before walking the budget |
| `differentiation-budget-walk` | Walk the 5 mechanisms on one screen |
| `squint-test` | Validate that the spending is actually working |
| `differentiation-budget-audit` | Cross-screen drift detection (mature systems) |
| `altitude-name` | Name data-model / action / intent / state altitude |
| `intent-altitude-gap` | Single-screen gap check |
| `intent-drift-audit` | Cross-screen drift detection |
| `constraint-graph-build` | Model a new cascade — soft, hard, deps, tradeoffs, failures |
| `constraint-graph-audit` | Find bypasses, cycles, redundancies, missing pins |
| `cascade-impact-trace` | Blast-radius for a single proposed change |

## Lens docs (the grounding)

| Doc | Codifies |
|---|---|
| `Design Loop.md` | perception → abstraction → action → feedback |
| `Intent as a Design Lens.md` | the knob framework; altitude (data-model/action/intent/state) |
| `Constraint-based design.md` | hard vs soft constraints, dependency graphs |
| `How to arrive at hierarchy clarity.md` | the differentiation budget, 5 mechanisms, squint test |
| `Design system lifecycle.md` | bootstrap / apply / audit / tweak / refactor — and how each lens reads per phase |

All five travel with the plugin under `docs/`, referenced by the skills
via `${CLAUDE_PLUGIN_ROOT}/docs/`.

## Layout

```
.claude-plugin/plugin.json
skills/                              # orchestrator + composable procedures
  design-loop/SKILL.md               # the phase-routing orchestrator
  design-system-phase/SKILL.md
  surface-type-name/SKILL.md
  ...
docs/                                # five conceptual lens docs
  Design Loop.md
  Intent as a Design Lens.md
  Constraint-based design.md
  How to arrive at hierarchy clarity.md
  Design system lifecycle.md
README.md
```

## Conventions all the skills enforce

- **Read-only.** They diagnose; you implement.
- **Phase-aware.** The orchestrator runs `design-system-phase` first, then branches.
- **Doc-grounded.** Skills read their lens doc before executing.
- **File-cited.** No finding without a path + line number.
- **Single target.** One screen, feature, or subsystem per invocation.
- **No roadmaps.** Smallest next test only.
- **No invented gaps.** A confirmed alignment is a valid finding.

## Override the methodology in your project

The skills prefer a consumer project's *own* copy of any lens doc when one
exists at the project root. Drop a tuned `Design Loop.md` (or any of the
five) at your project root, and the matching skill will use yours instead
of the plugin's copy. Falls back to the plugin's docs otherwise.

## Editing the lens docs

The five conceptual `.md` files in this plugin's `docs/` directory are the
canonical, install-ready copies. Edit them in place to evolve the
methodology — every skill reads
`${CLAUDE_PLUGIN_ROOT}/docs/<lens>.md` at invocation time, so changes take
effect on the next plugin reload.
