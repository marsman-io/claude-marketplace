# design-loop-methodology

Four diagnostic agents that critique any design surface through the lens of
four conceptual docs that ship inside the plugin. Read-only critics, not
implementers — each produces a structured finding you (or your main loop)
react to.

| Agent | Lens | Asks |
|---|---|---|
| `design-loop` | `Design Loop.md` | What is happening, what model, what test, what would teach us we were wrong |
| `intent-lens` | `Intent as a Design Lens.md` | Who opens this, what should become true, where's the altitude gap |
| `constraint-cascade` | `Constraint-based design.md` | Inputs, derived, hard vs soft, fails-at-extremes |
| `hierarchy-budget` | `How to arrive at hierarchy clarity.md` | Surface type, 5-mechanism spending, squint test |

## What ships

```
.claude-plugin/plugin.json
agents/                  # four diagnostic agents
docs/                    # four canonical conceptual docs the agents reference
README.md
```

Each agent reads its grounding doc from `${CLAUDE_PLUGIN_ROOT}/docs/`
before answering, so the methodology travels with the plugin into any
consumer project.

## How to use

Once the plugin is installed and enabled in Claude Code, the agents
auto-invoke on phrasing that matches their `description` field. Examples:

- *"Run the design loop on this screen"* → `design-loop`
- *"What's the intent gap here?"* → `intent-lens`
- *"Map the cascade for this token system"* → `constraint-cascade`
- *"Audit the hierarchy of this page"* → `hierarchy-budget`

Or invoke explicitly: `Agent({ subagent_type: "design-loop", ... })`.

## How they compose

`design-loop` is the meta-agent. It walks all four stages of the loop and
may invoke the other three as peer lenses during its abstraction stage.
The other three are single-lens critics — useful on their own when you
already know which lens you want.

A typical sequence on a fresh target:

1. `design-loop` for the full four-stage pass.
2. `intent-lens` or `hierarchy-budget` or `constraint-cascade` if a
   specific finding wants deeper treatment.
3. Iterate, with action+feedback turns between agent calls.

## Conventions all four enforce

- **Read-only.** No `Edit` or `Write` tools. They diagnose; you implement.
- **Doc-grounded.** Each agent must read its lens doc before answering.
- **File-cited.** No finding without a path + line number.
- **Single target.** One screen, one feature, one decision per invocation.
- **No roadmaps.** They propose the smallest next test only, not the next quarter.
- **No invented gaps.** A confirmed alignment is a valid finding.

## Override the methodology in your project

The agents prefer a consumer project's *own* copy of a lens doc when one
exists at the project root. Drop a tuned `Design Loop.md` (or any of the
four) at your project root, and the matching agent will use yours instead
of the plugin's copy. Falls back to the plugin's docs otherwise.

## Editing the lens docs

The four conceptual `.md` files in this plugin's `docs/` directory are the
canonical, install-ready copies. Edit them in place to evolve the
methodology — every agent reads `${CLAUDE_PLUGIN_ROOT}/docs/<lens>.md` at
invocation time, so changes take effect on the next plugin reload.
