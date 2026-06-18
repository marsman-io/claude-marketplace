---
name: concept-terminology-audit
description: Audits whether the same concept is named consistently across every surface of a multi-surface tool — the signature failure is one concept wearing different names (--org in the CLI, Account in the SDK, team_id in the API, workspace in the MCP tool, "Organization" in the dashboard) — and it is partly machine-checkable by diffing the CLI --help, the OpenAPI field/resource names, the SDK public symbols, the MCP tool schema, and the dashboard labels against one canonical concept model, distinguishing a label conflict (a rename) from a worse concept conflict (two surfaces mean genuinely different things by the same word). Use when names feel inconsistent across surfaces. Triggers on "terminology audit", "concept model", "consistent naming across surfaces", "do we call the same thing different names", "vocabulary drift", "glossary", "controlled vocabulary". NOT for how surfaces connect (use ecosystem-map), per-surface findability and structure (use surface-information-architecture), or enumerating surfaces (use touchpoint-inventory).
---

# Concept Terminology Audit

This is the flagship audit for a multi-surface tool, because its signature failure is brutal and common: one concept wears a different name on every surface — `--org` in the CLI, `Account` in the SDK, `team_id` in the REST API, `workspace` in the MCP tool, "Organization" in the dashboard — so a user who learns one surface is a beginner again on the next. The audit is partly MACHINE-CHECKABLE: you can diff the CLI `--help`, the OpenAPI field and resource names, the SDK's public symbols, the MCP tool schema, and the dashboard labels, then map every name to one canonical concept. Crucially, distinguish a LABEL conflict (same thing, different word — a rename fixes it) from a CONCEPT conflict (the API's `project` and the dashboard's `project` denote genuinely different things — far worse, and a rename hides it). Deliver both a concept model (the canonical spine) and a controlled vocabulary (the enforced names with owners).

## When to use

**Do** use to reconcile names across CLI/SDK/API/MCP/dashboard/docs and to surface concept-vs-label conflicts; use when onboarding to a new surface feels like starting over.

**Don't** use to map data flows (ecosystem-map) or to judge structure/findability within a surface (surface-information-architecture).

## Procedure

1. Fix ONE concept domain to audit (e.g. the org/tenant/identity cluster). One target per invocation.
2. Harvest names mechanically from each surface and cite each: CLI flags/commands from `--help`; resources/fields from the OpenAPI spec; public symbols from the SDK; tool/param names from the MCP schema; labels from the dashboard; terms from the docs.
3. Build the concept model: nodes = concepts (nouns), edges = relationships (verbs). Keep under 25 nodes. Pick a layout: hub-and-spoke, backbone, core-concepts, or relationship-focused.
4. Fill the cross-surface term matrix: one row per concept, one column per surface.
5. For each row mark Consistent? and, where not, classify the conflict as LABEL-change (rename to canonical) or CONCEPT-conflict (same word, different meaning — escalate; renaming would mask it).
6. Write the controlled vocabulary: per concept, the approved term, definition, do-NOT-say list, synonym ring, owner, status.
7. Flag every concept with no owner.

## Output

```
# Concept Terminology Audit — <domain>  (source: <repo | pasted | URL>)

## (a) Concept model  (layout: hub-and-spoke | backbone | core-concepts | relationship-focused; <25 nodes)
Nodes (concepts/nouns):  Organization, Project, Member, ApiKey
Edges (relationships/verbs):
  Organization --contains--> Project
  Organization --has--> Member
  Member --owns--> ApiKey

## (b) Cross-surface term matrix
| Concept      | CLI flag/cmd | SDK symbol | REST field/resource | MCP tool name | Dashboard label | Docs term     | Consistent? | Conflict type      |
|--------------|--------------|------------|---------------------|---------------|-----------------|---------------|-------------|--------------------|
| Organization | `--org`      | `Account`  | `team_id`           | `workspace`   | "Organization"  | "Org"         | NO          | LABEL-change       |
| Project      | `--project`  | `Project`  | `project`           | `project`     | "Project"       | "Project"     | partial     | CONCEPT-conflict ⚠ |
Cite: cli/help.ts:18 · sdk/account.ts:4 · <OpenAPI url> · mcp/tools.json · dash/nav.tsx:22 · docs/concepts.md

### Conflict classification
- Organization: LABEL-change — five names, one concept. Pick canonical, rename.
- Project: CONCEPT-conflict — API `project` = deploy unit; dashboard `project` = billing container. NOT a rename; resolve the meaning first.

## (c) Controlled vocabulary
| Concept      | Approved term | Definition                          | Do-NOT-say                  | Synonym ring          | Owner     | Status   |
|--------------|---------------|-------------------------------------|-----------------------------|-----------------------|-----------|----------|
| Organization | Organization  | Top-level tenant owning projects    | account, team, workspace,org| org, tenant           | Platform  | approved |
| Project      | (blocked)     | TBD — resolve concept conflict first| —                           | —                     | **none** ⚠| blocked  |
```

Failure mode: the audit renames everything to one label and declares victory, while a CONCEPT-conflict — two surfaces meaning different things by the same word — is now hidden behind a shared name, making the deeper bug harder to ever find.
