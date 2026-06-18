# dx-evaluation-skills

A flat collection of eleven codebase-neutral, **read-only** skills for
**evaluating the developer experience of a multi-surface tool** — a product that
spans a CLI, an SDK, a REST API, an MCP server, a desktop/Electron dashboard, an
installer/upgrade flow, and docs. Each skill diagnoses one surface (or the seam
between surfaces) and emits a structured finding; **you intervene** — the skills
never edit product code.

This is the critique half of a pair. Its sibling,
[`experience-mapping-skills`](../experience-mapping-skills), *builds* the maps;
these skills *grade* the result. The intended workflow is **map first, then
evaluate**.

No agents, no shared docs. Each skill stands alone — install the plugin and the
skills fire on the phrasings in their descriptions, or invoke one directly. Each
accepts an **in-repo target or a pasted/external artifact** (a `--help` dump, an
OpenAPI spec, a URL, pasted markup); "not in the repo" is a normal path.

Two convictions run through every skill, because the research is emphatic about
them for developer tools: **failure UX outweighs happy-path UX** (most real time
is spent on sad paths), and **agents are first-class users** — the MCP surface's
"user" is an LLM, and structured errors are its only recovery signal.

## Skills

### Cross-cutting methods (point them at any surface)

| Skill | Does | Fires on |
|---|---|---|
| `task-analysis` | Hierarchical task analysis + DX metrics (step/decision count, cross-surface context switches, copy-paste handoffs, time-to-first-hello-world). | "task analysis", "HTA", "how many steps to first call", "count the decision points" |
| `cognitive-walkthrough` | The four learnability questions per step; all-yes = pass. Agent-as-user variant for MCP. | "cognitive walkthrough", "will a new user know what to do", "learnability review" |
| `heuristic-evaluation` | Nielsen's 10 heuristics **plus a DX supplement** (idempotency, machine-readable errors, observable state, safe upgrades), with severity 0–4. | "heuristic evaluation", "nielsen heuristics", "usability review", "dx heuristics" |
| `golden-path` | The one canonical route to first value — install → auth → first call → verify — expressible headless and idempotently. | "golden path", "happy path", "the paved road to hello world", "time to first call" |
| `failure-state-matrix` | **The flagship.** Every failure × step: what the user sees, root cause, recovery path, owner, + machine error type / retryable / exit code. | "failure state mapping", "error state matrix", "audit the error handling", "recovery paths" |
| `experience-principles` | A testable DX contract — 3–6 "X over Y" principles, each with concrete behaviors and a checklist item. | "experience principles", "ux contract", "design principles", "quality bar" |

### Per-surface conformance audits

| Skill | Audits against | Fires on |
|---|---|---|
| `cli-conformance` | The Command Line Interface Guidelines (clig.dev) — taxonomy, exit codes, streams, `--json`, `NO_COLOR`, `--dry-run`. | "cli review", "clig.dev", "command line usability", "audit the cli" |
| `api-error-model-audit` | RFC 9457 problem+json, cursor pagination, idempotency keys, semver + `Sunset`, `Retry-After`. | "api review", "error model audit", "pagination versioning idempotency audit", "problem+json" |
| `sdk-ergonomics` | The Azure SDK Design Guidelines — naming, auto-pagination, typed exceptions, optional-vs-zero, cross-language parity. | "sdk review", "client library ergonomics", "is the sdk idiomatic", "sdk parity" |
| `mcp-server-ux` | MCP tools as an LLM's UI — workflow-shaped tools, namespacing, the never-write-stdout rule, host compatibility. | "mcp server review", "mcp tool design", "are the tools well-named for the model" |
| `installer-upgrade-audit` | The install / upgrade / migrate / rollback state machine — journal, user-data protection, compatibility matrix. | "installer review", "upgrade flow audit", "migration safety", "rollback review" |

`cli-conformance` and `installer-upgrade-audit` produce matrices that can be
turned into automated CI conformance tests.

## A note on the methods

Each skill is grounded in an authoritative source — Nielsen Norman Group (the 10
heuristics, the cognitive walkthrough, error-message guidelines), the Cognitive
Walkthrough practitioners' guide, clig.dev, RFC 9457 / Google AIP / Stripe for
APIs, the Azure SDK Design Guidelines, and modelcontextprotocol.io — then weighted
for developer tools, where the same task crosses surfaces, errors are the agent's
only recovery signal, and version compatibility and safe upgrades are explicit
concerns. Each skill cites its sources.

## Conventions all skills share

- **Read-only.** They diagnose; you intervene. No skill edits product code. (No
  agents either — these are skills, so the discipline is held in prose.)
- **Structured output.** Each emits a fixed table / matrix and a verdict, never
  loose prose. Each ends by naming its own failure mode.
- **Codebase-neutral.** No product is hardcoded; the surfaces are the generic
  CLI / SDK / REST API / MCP / dashboard / installer / docs.
- **Accepts external / pasted artifacts.** A `--help` dump, an OpenAPI spec, a
  URL, or pasted output is a first-class target.
- **Single target.** One surface, one flow, one task per invocation.
- **Cite-or-it-didn't-happen.** Every finding ties to a `file:line`, a pasted
  block, or a URL.

## Layout

```
.claude-plugin/plugin.json
README.md
skills/
  task-analysis/SKILL.md
  cognitive-walkthrough/SKILL.md
  heuristic-evaluation/SKILL.md
  golden-path/SKILL.md
  failure-state-matrix/SKILL.md
  experience-principles/SKILL.md
  cli-conformance/SKILL.md
  api-error-model-audit/SKILL.md
  sdk-ergonomics/SKILL.md
  mcp-server-ux/SKILL.md
  installer-upgrade-audit/SKILL.md
```

## Install

```
/plugin install dx-evaluation-skills@claude-marketplace
```

## License

MIT.
