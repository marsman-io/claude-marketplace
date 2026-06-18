---
name: mcp-server-ux
description: UX review of an MCP (Model Context Protocol) server where the "user" is an LLM AGENT — tool names, descriptions, and JSON-Schema ARE the interface, and structured errors are the agent's only recovery signal. Use when you have an MCP server (in-repo source, a `tools/list` dump, or pasted tool definitions) and need to judge whether the model can discover, choose, and recover among its tools, and whether it's safe and host-compatible. Triggers on "mcp server review", "mcp tool design", "are the tools well-named for the model", "mcp host compatibility", "audit the mcp surface", "review the mcp tools", "why does the model pick the wrong tool". NOT for the underlying HTTP API the tools wrap (→ api-error-model-audit), NOT for a human-facing SDK (→ sdk-ergonomics), NOT for a command-line tool (→ cli-conformance).
---

# MCP Server UX

An MCP server has no buttons and no docs page — its entire UI is the `tools/list` payload an LLM reads at runtime, and the model's only way to recover from a mistake is the error string you hand back. So tool names that read like internal endpoints, schemas with undocumented fields, and errors like "Error 422" are not cosmetic; they are the difference between an agent completing a task and looping or giving up. This skill reviews one MCP server for agent-facing UX, primitive choice, permissions, transport correctness, and host compatibility. It diagnoses; it does NOT edit the server or its product code. You read the source, the `tools/list` output, or pasted definitions, find the gaps, and hand back the tables — then a human intervenes.

## When to use

**Do** use when:
- You have one MCP server to audit — its source, a `tools/list` JSON dump, or pasted tool definitions.
- You need a cite-backed verdict on whether the model can name-find-call-recover, and whether the surface is safe and host-portable.
- "Not in repo" is fine: a `tools/list` dump or pasted schemas is a valid target.

**Don't** use when:
- The concern is the design/errors/pagination of the HTTP API the tools call (→ api-error-model-audit).
- The surface is a human-facing client library (→ sdk-ergonomics) or a CLI (→ cli-conformance).

## Checklist

Verify each. Cite the proof (`file:line`, a `tools/list` block, or the pasted schema). "Couldn't verify from the artifact" is a valid finding.

**Primitives**
- [ ] Correct primitive per thing: Tools = actions/side-effects; Resources = readable data; Prompts = user-invoked templates.
- [ ] Anything state-changing is a Tool (not a Resource read with a side effect).
- [ ] Capabilities are declared in the `initialize` handshake.

**Tool discovery & design**
- [ ] `tools/list` returns rich metadata per tool: a unique, namespaced `name`; a human `title`; a `description` that says BOTH what it does AND when to use it; a complete JSON-Schema `inputSchema` with required vs. optional documented and each field described.
- [ ] Tools are named for what they DO — `create_github_issue`, not `github_issue_endpoint` / `do_action`.
- [ ] Tools are WORKFLOW-shaped, not raw API endpoints: multi-step operations are collapsed so the model picks correctly and the user approves once, instead of being asked to chain three low-level calls and hit three "Allow" prompts.
- [ ] Tool count is managed — namespacing, dynamic tool loading, and `notifications/tools/list_changed` keep the model from drowning in dozens of similar tools.

**Permissions & security**
- [ ] Host approval is required before a tool runs; destructive operations are explicitly confirmed.
- [ ] AuthN per request; authZ FILTERS `tools/list` to the caller's permissions (the model never sees tools it can't use).
- [ ] Input validation and sandboxing on every tool argument.
- [ ] SSRF and prompt-injection defenses (untrusted tool output is not treated as instructions).
- [ ] Audit logging of tool invocations.

**Transport & compatibility**
- [ ] STDIO servers NEVER write to stdout (it corrupts the JSON-RPC stream) — logs go to stderr or a file.
- [ ] Correct transport for the deployment: stdio for local, Streamable HTTP / SSE for remote.
- [ ] Graceful shutdown (cleans up child processes / connections on signal).
- [ ] Tested across the target hosts — each host interprets schemas and renders approval UX differently.

**Errors & debugging**
- [ ] Errors are caught and returned human/agent-readable so the model can parse and recover — not a bare "Error 422: Unprocessable Entity".
- [ ] An invalid tool name returns a clear message (ideally a suggestion), not a stack trace.
- [ ] Structured stderr logging with levels.
- [ ] Works under the MCP Inspector.
- [ ] Long operations report progress; batch operations report PARTIAL failures (which items succeeded, which failed and why).

## Procedure

Gather the surface cheaply first, then walk the checklist once.
1. Get the interface: capture `tools/list` (or read the tool-registration source, or take the pasted definitions). Note the transport (stdio vs HTTP) and the `initialize` capabilities.
2. Read EACH tool as the model would: from `name` + `title` + `description` + `inputSchema` alone, could you pick it for the right task and call it without guessing? Flag every tool that fails that test.
3. Walk the remaining groups, recording ✓ / ✗ / partial with citations. For stdio servers, explicitly check that nothing logs to stdout.

This audit is partly AUTOMATABLE: a CI test can run the server under the MCP Inspector / a `tools/list` harness and assert every tool has a non-empty `title`, a description containing a "use when" clause, and a fully-described `inputSchema` with required fields marked — plus a stdio test asserting stdout carries only valid JSON-RPC frames.

## Output

```
## Tool catalog
| Tool | Namespace | Workflow vs endpoint | Required permission | Destructive? | Host-approval behavior |
|------|-----------|----------------------|---------------------|--------------|------------------------|
| create_github_issue | github | workflow | issues:write | no | single approve |
| delete_repo | github | endpoint | repo:admin | YES | confirm + approve |

## Host-compatibility matrix
| Host | Transport | Status | Quirks |
|------|-----------|--------|--------|
| Host A | stdio | OK | — |
| Host B | Streamable HTTP | partial | renders schema enums as free text |

## Permissions / RBAC map
| Caller role | Tools visible in tools/list | Tools hidden |
|-------------|-----------------------------|--------------|
| reader | get_*, list_* | create_*, delete_* |
```

Failure mode of this method: judging the tools as an engineer who already knows the backend — the names and schemas can look fine to someone holding the API in their head, while a model with only the `tools/list` text picks the wrong tool or omits a required field, so every "clear" verdict must be made strictly from the runtime metadata, nothing else.
