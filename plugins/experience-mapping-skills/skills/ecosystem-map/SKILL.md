---
name: ecosystem-map
description: Draws a node-and-edge graph of the whole system a user experiences, treating a dev tool's ecosystem as a literal technical system graph — nodes are SYSTEMS not just people (CLI, SDK, REST API, MCP server, dashboard, auth/identity provider, package registry, CI runners, webhook consumers, the user's own codebase, docs site, status page, telemetry/billing backend) with the agent/LLM as a first-class actor on the MCP node, and edges carry concrete typed payloads (tokens, JSON, webhooks, OAuth redirects, telemetry, package downloads, config) mapped as a give AND a receive, exposing broken loops and bottlenecks. Use when you need to see how surfaces interconnect and where loops break. Triggers on "ecosystem map", "system map", "map the whole system", "how do the surfaces connect", "broken loops between surfaces", "what exchanges data with what", "show the data flows between surfaces". NOT for a flat catalog of surfaces (use touchpoint-inventory), step-by-step front/backstage delivery (use surface-information-architecture or cross-surface-synthesis), or reconciling names (use concept-terminology-audit).
---

# Ecosystem Map

An ecosystem map is a directed graph of every system the user experiences, and for a developer tool that ecosystem IS a technical system graph: the nodes are not just personas but running systems — CLI, SDK, REST API, MCP server, dashboard, auth/identity provider, package registry (npm/PyPI), CI runners, webhook consumers, the user's own codebase, docs site, status page, telemetry/billing backend — and on the MCP node the actor is an LLM agent, a first-class participant. Edges carry concrete, TYPED payloads (auth / data / event-webhook / billing) and must be drawn as a give AND a receive, because the value of the map is exposing BROKEN LOOPS: a token minted in the dashboard the CLI can't read from the env var it expects; an SDK pinned to an API version the docs no longer describe; an MCP tool exposing an action the API rate-limits without telling the agent. Put the user's primary actor at the center — do not auto-center your own org.

## When to use

**Do** use to reveal interconnections, data flows, and broken loops between surfaces; use after a touchpoint-inventory exists so the nodes are already enumerated.

**Don't** use to merely list surfaces (touchpoint-inventory), to reconcile terminology (concept-terminology-audit), or to map JTBD coverage (cross-surface-synthesis).

## Procedure

1. Fix ONE primary actor (the developer/integrator/agent whose experience this maps). Place them at center. One target per invocation.
2. List nodes in two classes: actors (human roles, the LLM agent) and systems (every surface plus backing services: auth, registry, CI, webhook consumers, the user's own codebase, telemetry/billing, status, docs).
3. Cluster nodes by role (your product's surfaces, third-party/platform systems, the user's own systems, identity/registry infra).
4. For every connection draw TWO directed edges (give and receive). For each edge record the concrete payload and type: `auth` (tokens, OAuth redirects, keys), `data` (JSON requests/responses, config files, package downloads), `event` (webhooks, callbacks), `billing` (usage, telemetry, invoices).
5. Trace each loop end to end. A loop is broken when a give has no matching receive, names/versions/contracts mismatch, or one side imposes a limit the other never learns about.
6. Flag broken loops, bottlenecks (single node many surfaces depend on), and unowned links (no system clearly responsible).
7. Cite each node and edge: `file:line`, pasted config, or URL. External/registry nodes cited by URL are normal.

## Output

```
# Ecosystem Map — central actor: <actor>  (source: <repo | pasted | URL>)

## Nodes (clustered by role)
- Central actor: <developer / integrator / LLM agent>
- Our surfaces: CLI, SDK, REST API, MCP server, Dashboard, Docs site
- Identity/registry: auth provider, npm/PyPI registry
- Platform/3rd-party: CI runners, webhook consumers, status page
- User-owned: user's codebase, user's CI config
- Backend: telemetry/billing

## Edges (directed, typed — give AND receive)
| From            | To              | Payload / value        | Type    | Cite             |
|-----------------|-----------------|------------------------|---------|------------------|
| Dashboard       | User            | API token (minted)     | auth    | dash/keys.tsx:12 |
| User            | CLI             | sets TOOL_TOKEN env    | auth    | <pasted env>     |
| CLI             | REST API        | Bearer token + JSON    | auth    | cli/client.ts:30 |
| REST API        | CLI             | 429 + rate-limit hdrs  | data    | <OpenAPI url>    |
| MCP server      | LLM agent       | tool result JSON       | data    | mcp/tools.json   |
| REST API        | Webhook consumer| event payload          | event   | api/hooks.ts:8   |
| Registry        | User codebase   | package download       | data    | <npm url>        |

## Broken loops / bottlenecks / unowned links
- BROKEN: Dashboard mints token as `API_TOKEN`, CLI reads `TOOL_TOKEN` — give/receive name mismatch (dash/keys.tsx:12 vs cli/client.ts:30).
- BROKEN: SDK pins API v1; docs describe v2 only — version loop unclosed.
- BOTTLENECK: auth provider — every surface depends on it; no degraded mode.
- UNOWNED: MCP→agent rate-limit signal — API limits the action, agent never told.
```

Failure mode: the map is drawn org-centered with single arrows, so it shows what your product emits but never traces the return path — and broken loops, which only appear when give and receive are matched, stay invisible.
