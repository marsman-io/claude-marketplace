# claude-marketplace

A Claude Code plugin marketplace published by [marsman-io](https://github.com/marsman-io).

## Install the marketplace

In any Claude Code session:

```
/plugin marketplace add marsman-io/claude-marketplace
```

That registers this repo as a source of plugins; nothing is installed yet.

## What's inside

All plugins auto-route on their own triggers. Most are skills-only; the two `*-loop-methodology` plugins additionally ship a single **drift-audit agent** that sweeps many targets in an isolated context and composes the leaf skills (the one place a subagent earns its keep — context isolation + the main thread can fan several out concurrently).

| Plugin | Status | Description |
|---|---|---|
| [`design-loop-methodology`](./plugins/design-loop-methodology) | v0.2.0 | Phase-aware diagnostic skills that critique UI / design surfaces through five conceptual lenses + a lifecycle taxonomy (bootstrap / apply / audit / tweak / refactor). The `design-loop` orchestrator skill detects phase and composes the right leaf-skill chain; single-lens requests auto-route to the leaf skills. 12 composable skills + a `design-system-audit` agent for whole-system cross-screen drift. |
| [`design-craft-skills`](./plugins/design-craft-skills) | v0.1.0 | The **generative** counterpart to `design-loop-methodology`: `ui-designer` (visual craft — spacing, color, typography, design tokens, component systems, pixel-perfect polish) and `ux-designer` (experience strategy — flows, information architecture, interaction design, the psychology behind decisions). Each ships progressive-disclosure references and can implement, not just propose. |
| [`project-loop-methodology`](./plugins/project-loop-methodology) | v0.2.0 | Phase-aware diagnostic skills that critique agentic product work through PM-derived lenses + a lifecycle taxonomy (charter / plan / execute / adjust / replan). The `project-loop` orchestrator skill detects phase and composes the right leaf-skill chain. Tuned for indie product builders checking whether agent-built work matches intent. 14 composable skills + a `project-work-audit` agent for whole-workstream cross-feature drift. |
| [`indie-founder-lenses`](./plugins/indie-founder-lenses) | v0.1.0 | Four independent, phase-aware, read-only lens skills for the surfaces a solo founder lives on — `launch-readiness-lens`, `pricing-page-lens`, `conversion-intent-lens`, and `founder-focus-budget`. Not a loop and not a methodology: no orchestrator, no shared lifecycle — each lens detects its own phase and accepts in-repo or pasted/external artifacts. |
| [`meta-prompt-skills`](./plugins/meta-prompt-skills) | v0.1.0 | A flat collection of seven standalone meta-prompt skills: `humanizer`, `video-distill`, `sota-scan`, `session-mine`, `clarify-deep`, `book-to-skill`, `prompt-improver` (auto / interactive mode). Each skill auto-routes on its own triggers. |
| [`frontier-analysis-skills`](./plugins/frontier-analysis-skills) | v0.1.0 | Five codebase-neutral skills for spending an expensive frontier reasoning model well — `seam-conformance`, `layer-trace`, `contract-drift`, `boundary-judgment`, `invariant-capture`. Each gathers evidence cheaply, makes one focused reasoning call, then captures the verdict as a durable rule + test: spend once, enforce forever. |
| [`experience-mapping-skills`](./plugins/experience-mapping-skills) | v0.1.0 | Ten generative skills for mapping the experience of a multi-surface developer tool (CLI, SDK, REST API, MCP server, dashboard, installer, docs) — `experience-map`, `journey-map`, `service-blueprint`, `jtbd-map`, `ecosystem-map`, and more. Each produces one structured artifact grounded in an established UX method. Pairs with `dx-evaluation-skills`: map first, then evaluate. |
| [`dx-evaluation-skills`](./plugins/dx-evaluation-skills) | v0.1.0 | Eleven read-only skills for evaluating the developer experience of a multi-surface tool — `task-analysis`, `cognitive-walkthrough`, `heuristic-evaluation`, `golden-path`, the flagship `failure-state-matrix`, and per-surface audits (`cli-conformance`, `api-error-model-audit`, `sdk-ergonomics`, `mcp-server-ux`, `installer-upgrade-audit`). Built on the conviction that for dev tools failure UX outweighs happy-path and agents are first-class users. |
| [`developer-docs-skills`](./plugins/developer-docs-skills) | v0.1.0 | Ten skills for writing and auditing developer-tool documentation, built on Diátaxis — the flagship `docs-diataxis-audit`, generative mode-builders (`quickstart-builder`, `tutorial-scaffold`, `how-to-recipe`, `explanation-doc`, `reference-from-spec`), and read-only critics (`readme-audit`, `doc-surface-drift`, `style-conformance`, `code-sample-audit`). Completes the trio with experience-mapping and dx-evaluation: map, evaluate, document. |
| [`release-flow-skills`](./plugins/release-flow-skills) | v0.1.0 | Git / PR / release-lifecycle skills for shipping software; the first is `changelog-from-diff`, which turns a git diff into a clean, grouped changelog / release-notes entry — user-invoked and never rewriting history. |

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
