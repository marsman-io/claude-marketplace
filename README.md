# claude-marketplace

A Claude Code and Codex plugin marketplace published by [marsman-io](https://github.com/marsman-io).

## Install the Claude Code marketplace

In any Claude Code session:

```
/plugin marketplace add marsman-io/claude-marketplace
```

That registers this repo as a source of plugins; nothing is installed yet.

## Install the Codex marketplace

From a local checkout of this repo:

```
codex plugin marketplace add /path/to/claude-marketplace
```

The Codex marketplace manifest lives at `.agents/plugins/marketplace.json`.
The Codex manifests expose each plugin's `skills/` directory. Claude Code
subagents under `agents/` remain part of the Claude plugin surface.

## What's inside

| Plugin | Status | Description |
|---|---|---|
| [`design-loop-methodology`](./plugins/design-loop-methodology) | v0.2.0 | Four phase-aware diagnostic agents (`design-loop`, `intent-lens`, `constraint-cascade`, `hierarchy-budget`) that critique UI / design surfaces through five conceptual lenses + a lifecycle taxonomy (bootstrap / apply / audit / tweak / refactor). 11 composable skills. |
| [`project-loop-methodology`](./plugins/project-loop-methodology) | v0.2.0 | Five phase-aware diagnostic agents (`project-loop`, `intent-verify`, `outcome-altitude`, `project-cascade`, `priority-budget`) that critique agentic product work through PM-derived lenses + a lifecycle taxonomy (charter / plan / execute / adjust / replan). Tuned for indie product builders checking whether agent-built work matches intent. 13 composable skills. |
| [`meta-prompt-skills`](./plugins/meta-prompt-skills) | v0.1.0 | A flat collection of seven standalone meta-prompt skills: `humanizer`, `video-distill`, `sota-scan`, `session-mine`, `clarify-deep`, `book-to-skill`, `prompt-improver` (auto / interactive mode). No agents — each skill auto-routes on its own triggers. Unrelated to the `*-loop-methodology` plugins; same marketplace only. |

### Install a plugin from the marketplace

```
/plugin install design-loop-methodology@claude-marketplace
```

Then auto-routes on phrasings like *"audit the hierarchy of `Page.tsx`"*,
*"run the design loop on the editor"*, *"what's the intent gap here?"*,
*"map the cascade for this token system"*. Or invoke explicitly:

```
Agent({ subagent_type: "design-loop", prompt: "..." })
```

## Layout

```
.claude-plugin/marketplace.json    # Claude Code marketplace manifest
.agents/plugins/marketplace.json   # Codex marketplace manifest
plugins/
  design-loop-methodology/         # one plugin per subdirectory
    .claude-plugin/plugin.json
    .codex-plugin/plugin.json
    agents/                        # 4 diagnostic agents
    docs/                          # conceptual docs the agents reference
    skills/                        # Codex-visible skill procedures
    README.md
LICENSE                            # MIT
```

Each plugin's directory is self-contained. Claude Code reads
`.claude-plugin/plugin.json` and can use both agents and skills. Codex reads
`.codex-plugin/plugin.json` and can use the plugin's skills.

## Contributing

Issues and PRs welcome. Each plugin has its own README describing what it
does and what conventions its components enforce. New plugins go in
`plugins/<plugin-name>/` with corresponding entries in
`.claude-plugin/marketplace.json` and `.agents/plugins/marketplace.json`.

## License

MIT — see [LICENSE](./LICENSE).
