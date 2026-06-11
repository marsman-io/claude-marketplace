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
| [`design-loop-methodology`](./plugins/design-loop-methodology) | v0.1.0 | Four read-only diagnostic agents (`design-loop`, `intent-lens`, `constraint-cascade`, `hierarchy-budget`) that critique any design surface through grounded conceptual lenses. Ships the four lens docs so the methodology travels with the plugin. |

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
.claude-plugin/marketplace.json    # marketplace manifest
plugins/
  design-loop-methodology/         # one plugin per subdirectory
    .claude-plugin/plugin.json
    agents/                        # 4 diagnostic agents
    docs/                          # 4 conceptual docs the agents reference
    README.md
LICENSE                            # MIT
```

Each plugin's directory is a self-contained Claude Code plugin —
manifest-driven, auto-discovered, portable to any consumer project. Each
agent references its grounding doc via `${CLAUDE_PLUGIN_ROOT}/docs/` so the
plugin works as soon as it's installed, no extra setup.

## Contributing

Issues and PRs welcome. Each plugin has its own README describing what it
does and what conventions its components enforce. New plugins go in
`plugins/<plugin-name>/` and a corresponding entry in
`.claude-plugin/marketplace.json`.

## License

MIT — see [LICENSE](./LICENSE).
