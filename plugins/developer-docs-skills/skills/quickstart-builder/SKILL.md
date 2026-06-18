---
name: quickstart-builder
description: >-
  Write the one canonical quickstart — the install → authenticate → first call → verify route that gets a developer to their first real success as fast as possible. Headless, copy-pasteable, ONE path, every step shows expected output, with an explicit time-to-first-success target scored against the Ably rubric. Grounds the page in a single highest-value first call and cuts every prerequisite, branch, and concept that delays it. Works from a pasted `--help` dump, an OpenAPI spec, or an existing getting-started page. Triggers on "write a quickstart", "getting started page", "time to first call", "TTFC", "first hello world", "5-minute setup", "first successful API call", "onboarding doc for the SDK". NOT for the full how-to library (use how-to-recipe), NOT for defining which route is golden (use the golden-path skill in dx-evaluation-skills), NOT for reference docs (use reference-from-spec).
---

# Quickstart Builder

A quickstart has exactly one job: the fastest path to a developer's first real success. This skill is GENERATIVE — it produces the page. Every prerequisite, choice, or branch you add pushes that first success later and costs adoption, so the posture is ruthless subtraction: install, authenticate, make one call that returns a real result, verify it, done. There is ONE happy path — one OS, one language, one auth method — and everything else gets footnoted elsewhere. The target is up and running in five minutes; you will measure against that and say so on the page. If a developer cannot copy-paste their way to a real response, it is not a quickstart.

## When to use
**Do**
- Write the single canonical first-success page for a CLI, SDK, REST API, MCP server, or installer.
- Turn a pasted `--help` dump, OpenAPI spec, or sprawling getting-started page into one linear route.
- Replace a getting-started page that branches on OS/language/auth or front-loads concepts.
- Set and score an explicit time-to-first-success target.

**Don't**
- Define which route IS the golden path or score the broader DX — use the `golden-path` skill in dx-evaluation-skills.
- Document every flag, endpoint, or option — use reference-from-spec.
- Cover the second, third, and advanced tasks — use how-to-recipe.
- Explain architecture or "why" — use a concepts/explanation page.

## Procedure
1. Identify the single highest-value **first success**: the one call that returns a real result the developer wanted (a created resource, a real query response — not `--version`, not a 200 on a health check).
2. Pick ONE happy path: one OS, one language/runtime, one auth method, one install channel. Footnote alternatives ("on Windows, see …") — never branch inline.
3. Write copy-pasteable blocks for each step: install, authenticate (via env var or stdin — never a secret on the command line where it leaks into shell history), the first call, and an explicit **Verify** step. Every command block is paired with a fenced expected-output block.
4. Estimate time-to-first-success end to end and score it on the Ably rubric: <30 min = 5/5, 30–60 min = 4/5, 1–2 hr = 3/5, 2–4 hr = 2/5, 4+ hr = 1/5. Aim for 5/5; state the number on the page.
5. Cut anything that does not move the developer toward the first call: optional config, concept detours, "you may also want to", multi-platform tables. If it does not advance the call, it leaves the quickstart.

## Output
```markdown
# Quickstart

By the end of this page you'll have made your first authenticated call and seen a real result back.

**Prerequisites:** a terminal and an account ([sign up](#) — takes 1 min).

### Step 1 — Install

```bash
curl -fsSL https://get.example.dev/install.sh | sh
```

```text
Installed example-cli v2.4.0 to /usr/local/bin/example
Run `example --help` to get started.
```

### Step 2 — Authenticate

Paste your token from the dashboard. It's read from stdin, so it never lands in your shell history.

```bash
example auth login
# paste token when prompted, then press Enter
```

```text
Token accepted. Authenticated as you@example.com (workspace: default).
```

### Step 3 — Make your first call

```bash
example items create --name "hello-world"
```

```json
{
  "id": "itm_8Qx2",
  "name": "hello-world",
  "status": "active",
  "created_at": "2026-06-18T14:02:11Z"
}
```

### Verify

Confirm the item exists by reading it back:

```bash
example items get itm_8Qx2
```

```json
{
  "id": "itm_8Qx2",
  "name": "hello-world",
  "status": "active"
}
```

If you see this object, you're done — you've authenticated and made a real round-trip call.

---

> Other OS, language, or auth method? See [Install options](#) and [Authentication](#).

**Time-to-first-success target: 5 min (Ably score 5/5).**
```

Failure mode: a quickstart padded with prerequisites, OS/language branches, and concept explanation that pushes the first successful call past 30 minutes — at which point it is no longer a quickstart.

Sources: Postman, "The most important API metric is time to first call" (https://blog.postman.com/the-most-important-api-metric-is-time-to-first-call/); Nordic APIs, "Why Time to First Call Is a Vital API Metric" — Time to First Hello World + Ably rubric (https://nordicapis.com/why-time-to-first-call-is-a-vital-api-metric/); Twilio's "up and running in 5 minutes" goal; Diátaxis (getting-started as a constrained tutorial/how-to hybrid).
