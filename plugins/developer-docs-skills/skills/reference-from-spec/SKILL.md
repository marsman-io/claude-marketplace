---
name: reference-from-spec
description: >-
  Produce reference documentation by GENERATING it from a machine source of truth — an OpenAPI spec, a CLI `--help`/parser tree, or SDK type signatures and docstrings — instead of hand-writing it, so the reference can never drift from the code it describes. Reference is information-oriented: complete, accurate, uniformly structured, describe-and-only-describe. Use when you need an exhaustive, neutral catalogue of every endpoint, command, flag, parameter, or symbol for a CLI, SDK, REST API, MCP server, dashboard, or installer — and you have, or can paste, the spec that defines it. Triggers on "generate API reference", "document every endpoint / flag / parameter", "reference docs from OpenAPI", "CLI reference from --help", "SDK reference from type signatures", "auto-generate docs from the spec", "keep docs in sync with the code". NOT for teaching a newcomer a first success (use tutorial-scaffold), NOT for getting a competent user to a concrete goal (use how-to-recipe), NOT for explaining why or how something works (use explanation-doc), NOT for judging which Diátaxis mode a page belongs in (use docs-diataxis-audit).
---

# Reference From Spec

Reference is the one documentation mode you should NOT write by hand. Its job is to describe the product exhaustively and neutrally — every endpoint, every flag, every field — and hand-written prose describing code is drift waiting to happen: the moment either side changes, the page lies. Diátaxis is explicit that reference is "information-oriented", that the imperative is to "describe, and only describe", and that "reference material is led by the product it describes" — which is exactly why "some reference material (such as API documentation) can be generated automatically by the software it describes, which is a powerful way of ensuring that it remains faithfully accurate to the code." So generate it from a single source of truth, wire that generation into CI, and keep teaching, motivating, and goal-orientation out — those belong to the other three modes.

## When to use
**Do**
- Generate reference from the machine source of truth: OpenAPI for a REST API, the `--help`/parser tree for a CLI, type signatures and docstrings for an SDK.
- Give every entry the SAME schema — uniform fields make the page complete, scannable, and regenerable.
- Wire generation into CI so docs rebuild on every change to the spec or code.

**Don't**
- Hand-write reference prose describing code — that drifts the instant either changes.
- Teach a first-timer or guarantee a safe first success → `tutorial-scaffold`.
- Walk a competent user to a concrete goal → `how-to-recipe`.
- Explain why a design exists or how a subsystem works → `explanation-doc`.

## Procedure
1. **Identify the machine source of truth** for the surface: OpenAPI/JSON-Schema for a REST API, the argument-parser/`--help` tree for a CLI, exported type signatures + docstrings for an SDK.
2. **Confirm the source is complete and authoritative.** Every public endpoint/command/symbol must be present and described in the spec itself. If the spec is wrong or thin, fix the spec — never patch the docs to compensate.
3. **Choose a generator and a consistent entry schema.** Every entry of a kind gets the identical set of fields. Recommended generators: Redoc (`npx @redocly/cli build-docs openapi.yaml`) or Stoplight Elements for OpenAPI→HTML; the parser/`--help` tree for CLI; typedoc-style extraction for SDK type signatures.
4. **Generate, then wire it into CI** so the docs rebuild on every change and a stale or spec-divergent build fails the pipeline.
5. **Keep prose out.** No tutorials, no rationale, no "you'll want to" — link to how-to and explanation pages instead of embedding them, so the page stays describe-only and stays generatable.

## Output
```markdown
# Reference

<!-- GENERATED — do not edit by hand. Edit the source of truth and regenerate. -->

## REST endpoint entry (one schema for every endpoint)

### `POST /v1/tasks`
**Summary:** Create a task and enqueue it for execution.

**Parameters**
| In    | Name     | Type   | Required | Description                  |
|-------|----------|--------|----------|------------------------------|
| query | `dryRun` | bool   | no       | Validate only; do not enqueue|
| header| `Idempotency-Key` | string | no | Dedup key for safe retries |

**Request body** (`application/json`)
| Field      | Type   | Required | Description              |
|------------|--------|----------|--------------------------|
| `name`     | string | yes      | Human-readable task name |
| `priority` | int    | no        | 0–9; default `0`        |

**Responses**
| Status | Schema     | Description            |
|--------|------------|------------------------|
| 201    | `Task`     | Task created           |
| 400    | `Error`    | Validation failed      |
| 409    | `Error`    | Idempotency-Key reused |

**Errors:** `400 invalid_field`, `409 duplicate_request`, `429 rate_limited`.

**Example**
```http
POST /v1/tasks
Content-Type: application/json

{ "name": "nightly-export", "priority": 5 }
```
```http
201 Created

{ "id": "tsk_001", "name": "nightly-export", "state": "queued" }
```

## CLI command entry (one schema for every command)

### `tool task create`
**Synopsis:** `tool task create <name> [--priority <n>] [--dry-run]`
**Description:** Create a task and enqueue it.

**Options**
| Flag           | Type | Default | Description               |
|----------------|------|---------|---------------------------|
| `--priority`   | int  | `0`     | Scheduling priority, 0–9  |
| `--dry-run`    | bool | `false` | Validate only; do not run |

**Exit codes**
| Code | Meaning            |
|------|--------------------|
| 0    | Task created       |
| 2    | Invalid arguments  |
| 4    | Server unreachable |

**Example**
```
$ tool task create nightly-export --priority 5
created tsk_001 (queued)
```
```

```text
Generation
- Source of truth : openapi.yaml  (REST)  /  `tool --help` parser tree (CLI)  /  exported .d.ts + docstrings (SDK)
- Generator       : npx @redocly/cli build-docs openapi.yaml -o site/reference.html
                    (or Stoplight Elements for embedded HTML; typedoc for the SDK)
- CI hook         : on every PR, regenerate and fail if the committed reference
                    differs from the freshly generated output, e.g.
                      npx @redocly/cli build-docs openapi.yaml -o /tmp/ref.html
                      git diff --exit-code site/reference.html   # non-zero = drift
- Drift guard     : reference is build output, never hand-edited; the spec is the
                    only thing humans change, and the docs are derived from it.
```

Failure mode: hand-writing reference (which silently drifts from the code the moment either side changes), or smuggling tutorials and explanation into entries so the describe-and-only-describe contract breaks and the page can no longer be generated from the spec at all.
Sources: Diátaxis — Reference (https://diataxis.fr/reference/); Redoc (https://github.com/Redocly/redoc); Stoplight Elements (https://stoplight.io/open-source/elements).
