---
name: layer-trace
description: Frontier-model workflow for tracing ONE operation end-to-end across architectural layers to find where an error gets swallowed, re-typed into something vaguer, loses its cause, or silently changes meaning at a hop. Bounded to one operation so the whole chain fits context and reasoning stays sharp. Triggers on "works but the error is useless", "the failure loses its root cause crossing module/package boundaries", "why is this error so vague by the time it surfaces", "trace where this operation drops its cause". NOT for "read the whole repo" — one operation, one trace. NOT for happy-path tracing or general code review.
---

# Layer Trace

Some errors arrive useless. The thing failed for a real reason deep in the
stack, but by the time it reaches you it's a `null`, a `false`, an empty list,
or a flat "request failed" — the cause got dropped at some hop on the way up.
Finding that hop is not a lookup. It needs a model that can hold the whole
ordered chain at once and reason about how the *error* mutates at each boundary:
where it's preserved, where it's re-wrapped, where a catch quietly eats it. That
is frontier work — a cheap model loses the thread across hops and starts
guessing. Bound it to one operation so the entire chain fits and the reasoning
stays sharp.

## When to spend a frontier model here

Do:
- One concrete operation — a create, a delete, a job submission, a single
  request — where errors arrive vague or context vanishes across module/package
  boundaries.
- A "works but the error is useless" bug, where the failure is real but the
  message tells you nothing.

Don't:
- Treat it as "read the whole repo." One operation, one trace. If you're
  tempted to feed five operations, pick the one that hurts.
- Trace the happy path. The whole value here is following the *error* path.

## Procedure

### 1. Gather cheap (no frontier tokens yet)

Assemble the call chain for ONE operation by grep/Read or a subagent — walk the
generic layered chain: entrypoint (the command/handler) -> service or SDK/client
layer -> domain/core -> the abstract interface method and the concrete
implementation behind it -> any HTTP/process hop and the contract at that
boundary. A typical interface fans out to several implementations (think several
storage backends behind one `Store` interface, or payment adapters behind a
`PaymentGateway`) — follow only the implementation this operation actually hits.

Collect each hop's try/catch, throw, and return site — not whole files. You want
the exact spots where the error could change shape, nothing else.

### 2. Think expensive (the frontier call)

Hand the model the ordered hops and ask it to trace the ERROR path, not the
happy path. At each hop, classify the failure's fate:

- **Preserved** — the original cause propagates intact.
- **Re-typed** — wrapped into something vaguer. Is the cause retained (chained /
  `cause:` / inner error) or dropped?
- **Swallowed** — caught and turned into a sentinel (`null`, `false`, `[]`) or
  an empty catch.
- **Translated at a boundary** — does the contract's error shape (your schema
  source of truth — Zod / JSON Schema / OpenAPI / protobuf / etc.) carry detail,
  or flatten to a bare status string?

Demand a hop-by-hop **table**, not prose. The table forces the model to commit a
verdict at every hop and mark the EXACT line where context is first lost — prose
lets it hand-wave past the one hop that matters.

### 3. Capture durably (spend the frontier reasoning once)

- Fix the first loss point — preserve the cause, propagate a typed error instead
  of a sentinel.
- Add a regression test that asserts the ERROR, not success, so the root cause
  is forced to surface through the whole chain. Run it with your test runner.
- If the same lossy hop pattern recurs, add a one-line rule to the nearest
  conventions doc (e.g. CLAUDE.md / AGENTS.md / CONTRIBUTING) so the next
  implementation behind that interface doesn't repeat it.

## Output shape

1. **Hop table** — ordered, one row per hop: layer · file:line · fate of the
   error (Preserved / Re-typed / Swallowed / Translated).
2. **The single line** where root cause is first lost.
3. **The fix** at that line, plus an error-asserting regression test that proves
   the cause now reaches the top.
