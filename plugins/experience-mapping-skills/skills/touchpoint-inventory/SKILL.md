---
name: touchpoint-inventory
description: Builds an exhaustive catalog of every point a user touches the product, where a touchpoint = channel × device/runtime × task, hunting the non-GUI surfaces everyone forgets (--help output, man pages, shell completions, error messages + exit codes, stack traces, log lines, deprecation warnings, HTTP error bodies, rate-limit headers, the npm/PyPI page, changelog/release notes, MCP tool descriptions, installer prompts, upgrade migration notices) and flagging surfaces no team owns. Use when you need to enumerate surfaces before mapping or auditing them. Triggers on "touchpoint inventory", "what surfaces do we even have", "catalog every touchpoint", "find orphaned surfaces", "who owns each surface", "ownership gaps", "list all the places users interact with us". NOT for how surfaces connect as a graph (use ecosystem-map), naming consistency across surfaces (use concept-terminology-audit), or which surfaces support each job (use cross-surface-synthesis).
---

# Touchpoint Inventory

A touchpoint inventory is a row-per-surface catalog where a touchpoint is defined as `channel × device/runtime × task` — so the same CLI in an interactive TTY and in a CI runner are two touchpoints, not one, because the user, the job, and the failure modes differ. For a developer tool the value is not in cataloging the obvious GUI; it's in dragging the invisible surfaces into the light: the `--help` block someone wrote in 2021, the exit code a CI script branches on, the rate-limit header an integrator parses, the MCP tool description whose "reader" is an LLM. The Owner column is the load-bearing one: inconsistency, rot, and broken promises live exactly where no team owns a surface. Flag every unowned row loudly — an orphaned surface is a defect even when it works today.

## When to use

**Do** use to enumerate the full surface area before running ecosystem-map, concept-terminology-audit, or cross-surface-synthesis; use when you suspect surfaces have drifted without an owner.

**Don't** use to model how surfaces exchange data (ecosystem-map), to reconcile names (concept-terminology-audit), or to judge findability within a surface (surface-information-architecture).

## Procedure

1. Fix ONE target (a product, a CLI binary, an API). One target per invocation.
2. Enumerate channels: CLI, SDK/library, REST/GraphQL API, MCP server, desktop/Electron dashboard, web app, docs site, installer/upgrader, package registry page, status page, email/notifications, changelog/release notes.
3. For each channel, split by device/runtime: interactive TTY vs CI runner vs piped/non-TTY; browser vs desktop shell; human reader vs LLM agent (MCP). Each split is its own row.
4. Hunt the non-GUI touchpoints explicitly — walk this list and create a row for each that exists: `--help`/usage, man page, shell completions, error messages, exit codes, stack traces, log lines, deprecation warnings, HTTP error bodies, rate-limit/quota headers, npm/PyPI/registry page, MCP tool descriptions, installer prompts, upgrade/migration notices.
5. For each row, place it on the lifecycle stage: discover → install → authenticate → first-success → integrate → operate/debug → upgrade → rollback.
6. Record entry points (how the user arrives) and exit/next step (where it sends them).
7. Note dependencies and direction: uni-directional (output only, e.g. a log line) or bi-directional (e.g. an installer prompt).
8. Assign an OWNER per row. If none, write `none` and flag the row. Do not guess an owner.
9. Cite each row: `file:line`, a pasted block, or a URL. "Not in repo" (a pasted `--help` dump or an external registry URL) is normal — cite the artifact.
10. Sort by lifecycle stage, then surface every `none`-owner and high-pain row at the top.

## Output

```
# Touchpoint Inventory — <target>  (source: <repo path | pasted | URL>)

| ID | Touchpoint (name)        | Channel   | Device/Runtime      | User type   | Primary job(s)          | Journey stage | Entry points          | Exit / next step       | Dependencies        | Direction | OWNER          | Health/pain          | Cite              |
|----|--------------------------|-----------|---------------------|-------------|-------------------------|---------------|-----------------------|------------------------|---------------------|-----------|----------------|----------------------|-------------------|
| 1  | `tool --help`            | CLI       | interactive TTY     | new dev     | discover commands       | discover      | `tool` w/ no args     | runs first command     | none                | uni       | DevRel         | stale flags          | cli/help.ts:42    |
| 2  | `tool` in CI            | CLI       | CI runner (non-TTY) | CI script   | run in pipeline         | operate       | CI config             | exit code branch       | exit codes          | uni       | **none** ⚠     | colors leak to logs  | <pasted CI run>   |
| 3  | exit codes              | CLI       | any                 | CI script   | branch on success/fail  | operate/debug | command return        | retry / fail build     | error taxonomy      | uni       | **none** ⚠     | undocumented         | cli/exit.ts:8     |
| 4  | rate-limit headers      | REST API  | server runtime      | integrator  | back off on 429         | integrate     | any API call          | retry with backoff     | quota service       | uni       | Platform       | header name drift    | <OpenAPI url>     |
| 5  | MCP tool descriptions   | MCP       | LLM agent           | LLM/agent   | choose right tool       | integrate     | agent tool listing    | tool invocation        | API contract        | bi        | **none** ⚠     | vague descriptions   | mcp/tools.json    |

## Orphaned / unowned surfaces (OWNER = none)
- #2 CLI-in-CI, #3 exit codes, #5 MCP descriptions — no team owns; route to ownership review.

## Highest-pain touchpoints
- #1 stale --help, #4 rate-limit header drift.
```

Failure mode: the inventory looks complete because every GUI screen is listed, while the unglamorous, machine-read, owner-less surfaces — exit codes, headers, MCP descriptions — were never enumerated, so the catalog certifies coverage it doesn't have.
