# claude-marketplace

A Claude Code plugin marketplace published by [marsman-io](https://github.com/marsman-io).

## Install the marketplace

In any Claude Code session:

```
/plugin marketplace add marsman-io/claude-marketplace
```

That registers this repo as a source of plugins; nothing is installed yet.

## What's inside

| Plugin | Status | Description |
|---|---|---|
| [`design-loop-methodology`](./plugins/design-loop-methodology) | v0.2.0 | Phase-aware diagnostic skills that critique UI / design surfaces through five conceptual lenses + a lifecycle taxonomy (bootstrap / apply / audit / tweak / refactor). The `design-loop` orchestrator skill detects phase and composes the right leaf-skill chain; single-lens requests auto-route to the leaf skills. 12 composable skills, no agents. |
| [`project-loop-methodology`](./plugins/project-loop-methodology) | v0.1.0 | Phase-aware diagnostic skills that critique agentic product work through PM-derived lenses + a lifecycle taxonomy (charter / plan / execute / adjust / replan). The `project-loop` orchestrator skill detects phase and composes the right leaf-skill chain. Tuned for indie product builders checking whether agent-built work matches intent. 14 composable skills, no agents. |
| [`meta-prompt-skills`](./plugins/meta-prompt-skills) | v0.1.0 | A flat collection of seven standalone meta-prompt skills: `humanizer`, `video-distill`, `sota-scan`, `session-mine`, `clarify-deep`, `book-to-skill`, `prompt-improver` (auto / interactive mode). No agents — each skill auto-routes on its own triggers. Unrelated to the `*-loop-methodology` plugins; same marketplace only. |

### Install a plugin from the marketplace

```
/plugin install design-loop-methodology@claude-marketplace
```

Then auto-routes on phrasings like *"audit the hierarchy of `Page.tsx`"*,
*"run the design loop on the editor"*, *"what's the intent gap here?"*,
*"map the cascade for this token system"* — the `design-loop` orchestrator
skill fires on full-loop requests, and single-lens phrasings auto-route
straight to the matching leaf skill (e.g. `differentiation-budget-walk`).

## Layout

```
.claude-plugin/marketplace.json    # marketplace manifest
plugins/
  design-loop-methodology/         # one plugin per subdirectory
    .claude-plugin/plugin.json
    skills/                        # orchestrator skill + leaf skills
    docs/                          # conceptual docs the skills reference
    README.md
LICENSE                            # MIT
```

Each plugin's directory is a self-contained Claude Code plugin —
manifest-driven, auto-discovered, portable to any consumer project. Each
skill references its grounding doc via `${CLAUDE_PLUGIN_ROOT}/docs/` so the
plugin works as soon as it's installed, no extra setup.

## Contributing

Issues and PRs welcome. Each plugin has its own README describing what it
does and what conventions its components enforce. New plugins go in
`plugins/<plugin-name>/` and a corresponding entry in
`.claude-plugin/marketplace.json`.

## License

MIT — see [LICENSE](./LICENSE).
