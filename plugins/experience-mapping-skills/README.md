# experience-mapping-skills

A flat collection of ten codebase-neutral skills for **mapping the experience
of a multi-surface developer tool** — a product that spans a CLI, an SDK, a REST
API, an MCP server, a desktop/Electron dashboard, an installer/upgrade flow, and
docs. The UX of such a product is not one interface; it is a multi-surface
system, and these skills build the picture of it.

These skills are **generative** — each one *produces* a structured artifact (a
map, a matrix, an inventory). That is the opposite posture to its sibling
plugin, [`dx-evaluation-skills`](../dx-evaluation-skills), whose skills are
read-only critics. The intended workflow is **map first, then evaluate**:
understand the system with these, then critique it with those.

No agents, no shared docs. Each skill stands alone — install the plugin and the
skills fire on the phrasings in their descriptions, or invoke one directly. Each
accepts an **in-repo target or a pasted/external artifact** (a `--help` dump, an
OpenAPI spec, a URL, pasted markup), because these surfaces rarely all live in
one repo — "not in the repo" is a normal path, not an error.

## Skills

| Skill | Produces | Fires on |
|---|---|---|
| `experience-map` | Product-**agnostic** baseline: how a developer accomplishes the goal today across DIY / OSS / a competitor — phases × actions/thoughts/friction. Finds white space. | "experience map", "how do developers solve this today", "where does our tool fit" |
| `journey-map` | One actor, one scenario across the adoption funnel; the channel/touchpoint lane and the surface handoffs are the core insight. | "journey map", "map the developer journey", "where does the experience break" |
| `service-blueprint` | The org-side view — evidence / frontstage / line-of-visibility / backstage / support — tracing a developer-visible failure to its backstage root cause. | "service blueprint", "frontstage backstage", "trace this failure to its root cause" |
| `current-future-state` | As-is (incl. workarounds) vs to-be, plus the delta as a prioritized DevEx backlog. | "current vs future state", "as-is to-be", "gap analysis", "devex roadmap" |
| `jtbd-map` | Job statements + the four-forces switch grid + measurable desired outcomes — no persona. | "jobs to be done", "jtbd", "what job are developers hiring this for", "switch interview" |
| `touchpoint-inventory` | The catalog: every surface × device × task × **owner**, including non-GUI touchpoints (exit codes, `--help`, error bodies, MCP tool descriptions). Flags orphans. | "touchpoint inventory", "what surfaces do we have", "who owns each surface" |
| `ecosystem-map` | The system as a node-edge graph (surfaces + systems + the agent), typed value edges, and the **broken loops** between surfaces. | "ecosystem map", "system map", "how do the surfaces connect", "broken loops" |
| `concept-terminology-audit` | The cross-surface term matrix + a concept model + controlled vocabulary; separates label conflicts from concept conflicts. Partly machine-checkable. | "terminology audit", "concept model", "do we call the same thing different names", "vocabulary drift" |
| `surface-information-architecture` | Each surface's structure (CLI tree, API resource nesting, SDK namespaces, docs tree) checked as a projection of one shared concept model. | "information architecture", "IA", "command taxonomy", "organize the commands / endpoints / docs" |
| `cross-surface-synthesis` | **The master artifact**: a JTBD × surface matrix showing which surfaces support each job and where the experience fragments. Composes the others. | "cross-surface synthesis", "master matrix", "which surfaces support each job", "where is it fragmented" |

## A note on the methods

Every skill is grounded in an established UX / product-research method (Nielsen
Norman Group's mapping family, Ulwick/Moesta on jobs-to-be-done, Dan Brown and
Abby Covert on concept models and controlled vocabularies, Service Design Tools
on ecosystem maps) and then adapted for a developer tool — where the "channels"
are mostly machine-to-machine and text-based (exit codes, JSON, schemas), the
emotion line is partly data-driven (time-to-first-call, error rates), and one of
the actors on the MCP surface is an LLM. Each skill cites its sources.

## Conventions all skills share

- **Generative.** Each skill produces a named artifact with a fixed structure (a
  table, matrix, or node-edge map) — template-ready, not prose.
- **Codebase-neutral.** No product is hardcoded; the surfaces are the generic
  CLI / SDK / REST API / MCP / dashboard / installer / docs.
- **Accepts external / pasted artifacts.** A `--help` dump, an OpenAPI spec, a
  URL, or pasted markup is a first-class target; "not in-repo" is normal.
- **Single target.** One map, one scenario, one concept domain per invocation.
- **Artifact-cited.** Every claim ties to a `file:line`, a pasted block, or a URL.
- **Shared vocabulary.** Skills reference the same surfaces and the same dev-tool
  lifecycle — discover → install → authenticate → first-success → integrate →
  operate/debug → upgrade → rollback — so their artifacts compose.

## Layout

```
.claude-plugin/plugin.json
README.md
skills/
  experience-map/SKILL.md
  journey-map/SKILL.md
  service-blueprint/SKILL.md
  current-future-state/SKILL.md
  jtbd-map/SKILL.md
  touchpoint-inventory/SKILL.md
  ecosystem-map/SKILL.md
  concept-terminology-audit/SKILL.md
  surface-information-architecture/SKILL.md
  cross-surface-synthesis/SKILL.md
```

## Install

```
/plugin install experience-mapping-skills@claude-marketplace
```

## License

MIT.
