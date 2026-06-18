---
name: surface-information-architecture
description: Applies information architecture across all of a product's surfaces, not just a website, on the insight that each surface's structure is a projection of one shared concept model — the CLI command/sub-command/flag tree is an IA (tool noun verb --flag), the REST resource nesting (/orgs/{id}/projects/{id}/deploys) is an IA, the SDK module/namespace/class layout is an IA for code, the docs tree is the canonical IA surface, the dashboard nav is standard web IA, and the MCP tool set is an IA for an LLM consumer — and checks that the same concept occupies a parallel position and name in each surface. Use when structure or findability across surfaces is in question. Triggers on "information architecture", "IA", "command taxonomy", "is the structure findable", "organize the commands", "organize the endpoints", "organize the docs", "card sort", "tree test". NOT for naming consistency itself (use concept-terminology-audit), the system data-flow graph (use ecosystem-map), or enumerating surfaces (use touchpoint-inventory).
---

# Surface Information Architecture

Information architecture is usually pitched at websites, but a developer tool has many IAs at once, and the key insight is that each surface's structure is a PROJECTION of one shared concept model. The CLI command/sub-command/flag tree is an IA (`tool noun verb --flag`); the REST resource nesting (`/orgs/{id}/projects/{id}/deploys`) is an IA; the SDK module/namespace/class layout is an IA for code; the docs tree (Getting Started / Guides / API Reference / CLI Reference / Concepts) is the canonical IA surface; the dashboard nav is ordinary web IA; the MCP tool set is an IA whose consumer is an LLM. The cross-surface rule that makes the whole thing learnable: the same concept should occupy a PARALLEL position and a parallel name in each surface's structure. When the CLI nests deploys under projects but the API nests them under orgs, the user's mental model breaks at the seam.

## When to use

**Do** use to evaluate or design the structure and findability of one or more surfaces and to check each projection against the shared concept model; pair with a card sort / tree test to validate against users.

**Don't** use to reconcile names (concept-terminology-audit) or to map data flows between surfaces (ecosystem-map).

## Procedure

1. Fix ONE target surface (or a small set sharing a concept model). One target per invocation.
2. Inventory content/functionality: every command, endpoint, namespace, doc page, nav item, or MCP tool — with surface, type, owner, and a keep/cut/merge call. Cite each (`file:line`, OpenAPI URL, pasted tree).
3. Choose an organization scheme using LATCH — Location, Alphabet, Time, Category, Hierarchy — and decide flat vs deep (broad shallow trees beat narrow deep ones for findability).
4. Draw the per-surface structure projection: CLI command tree, API resource tree, SDK namespaces, docs tree, dashboard nav, MCP tool set — whichever apply.
5. Run the alignment check: for each concept, does it sit at a PARALLEL position and name in every surface's projection? Flag every mismatch as a seam.
6. Recommend a validation: a card sort (to derive categories from users) or a tree test (to verify findability of the proposed structure) — name which, and the task to test.

## Output

```
# Surface Information Architecture — <surface(s)>  (source: <repo | pasted | URL>)

## (1) Content / functionality inventory
| Item                         | Surface   | Type      | Owner    | Keep/Cut/Merge | Cite             |
|------------------------------|-----------|-----------|----------|----------------|------------------|
| `tool project deploy`        | CLI       | command   | DevRel   | keep           | cli/project.ts:9 |
| `POST /orgs/{id}/deploys`    | REST API  | endpoint  | Platform | merge          | <OpenAPI url>    |
| Concepts > Deploys           | Docs      | page      | Docs     | keep           | docs/deploys.md  |

## (2) Organization scheme
- Scheme (LATCH): Category + Hierarchy (concept-first).
- Flat vs deep: flat — max 2 levels of nesting; current API is 3 (too deep).

## (3) Per-surface structure projection
CLI:   tool > project > deploy --env
API:   /orgs/{id}/projects/{id}/deploys
SDK:   client.projects.deploys.create()
Docs:  Getting Started / Guides / CLI Reference / API Reference / Concepts
Dash:  Nav: Projects > [project] > Deploys
MCP:   tools: project_list, deploy_create, deploy_status

## (4) Alignment check vs shared concept model
| Concept | CLI position        | API position          | SDK position           | Docs position      | Parallel? |
|---------|---------------------|-----------------------|------------------------|--------------------|-----------|
| Deploy  | project > deploy    | orgs > deploys        | projects.deploys       | Concepts > Deploys | NO ⚠ (API skips project) |

## (5) Validation recommendation
- Tree test: "Where would you cancel a running deploy?" across CLI tree + dashboard nav. n≈15 target users.
```

Failure mode: each surface's IA is tidied in isolation and looks clean, but no one ran the cross-surface alignment check, so the concept sits at a different depth and name per surface and users relearn the structure every time they switch surfaces.
