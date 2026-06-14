---
name: contract-drift
description: Frontier-model workflow for finding where an HTTP boundary has drifted from your schema source of truth (Zod / JSON Schema / OpenAPI / protobuf / etc.). Finds routes that hand-roll a shape, widen a type with a cast, parse loosely, or respond with fields the schema doesn't declare — and producer/consumer pairs that silently disagree. Triggers on "where did this contract drift", "does this route match the schema", "find boundaries that bypass validation", "which consumers diverged after the contract change", "this API response looks untrustworthy". NOT for authoring a new schema, NOT for bugs runtime validation already rejects, NOT for a boundary with full parse-on-both-sides coverage — drift hides where validation is PARTIAL.
---

# Contract drift

A boundary surface — one schema module plus the routes that produce and consume
it — drifts in the gaps validation doesn't cover. The cheap signal is honest:
where `.parse()` is called, the runtime already enforces the contract and there
is nothing to find. The expensive signal is the inverse — where a value is
trusted, cast, or hand-assembled, and the schema is decoration rather than a
gate. Seeing that requires holding the schema, every producer, and every
consumer in one head and reasoning about whether the shapes actually agree
across a layered chain (entrypoint -> service -> domain/core -> adapter ->
external boundary). A cheap model reads each file in isolation and reports
"looks fine" per file while the divergence lives *between* them. That cross-file
shape reconciliation is the frontier call. Spend it once, on one surface.

## When to spend a frontier model here

**Do** spend it when:
- You're auditing ONE boundary surface — one schema module plus the routes that
  produce/consume it — not the whole API.
- A contract just changed and you need to know which producers/consumers
  silently diverged.
- Responses look untrustworthy: fields appear that the schema doesn't declare,
  or declared fields go missing intermittently.
- Validation is PARTIAL — parsed on one side, trusted-and-cast on the other.
  That asymmetry is where drift lives.

**Don't** spend it when:
- You're authoring a new schema (no producers/consumers to reconcile yet).
- The bug is something runtime validation already rejects — that's a test run,
  not a reasoning problem.
- The boundary has full parse-on-both-sides coverage — there's no gap to drift
  into.

## Procedure

### 1. Gather cheap (no frontier tokens)

Assemble the surface with ordinary tools — grep, read, your editor. No frontier
model yet:
- The schema module and its exported/inferred types — your source of truth.
- The producer routes: where responses are built and where incoming requests
  are read.
- The consumer call sites: the SDK/client code and anywhere a response is
  destructured or relied on.
- A note on every boundary: is `.parse()` / `.safeParse()` actually called, or
  is the value trusted and cast (`as`, a hand-written interface, a bare JSON
  body)? Mark validated vs trusted.

If you can't name the schema, the producers, and the consumers, you're not ready
to spend the expensive call — keep gathering.

### 2. Think expensive (the frontier call)

Hand the frontier model the schema, the producers, and the consumers in one
prompt. Demand a DRIFT LIST, not prose — a table it must fill per endpoint:

- **Request in** — validated against the schema, or read raw / cast with `as`?
- **Response out** — built from the schema-inferred type, or hand-assembled with
  fields the schema doesn't declare (or missing ones it does)?
- **Widening** — any `as any` / `as unknown as` / looser hand-written type that
  defeats the schema at this boundary?
- **Optionality drift** — does the producer omit a field the consumer treats as
  required, or does the consumer ignore a field the producer always sends?

Every finding cites `route file:line`, the specific schema field, and the
concrete drift. A row with no citation is prose pretending to be a finding —
reject it and make the model point at code.

### 3. Capture durably (spend once)

Turn the findings into enforcement so the next divergence can't hide:
- Make the schema the gate: `.parse()` requests on entry; validate responses on
  the way out, or in a test that exercises the route.
- Add a round-trip test — feed a built response through the schema and assert it
  parses. That pins the producer to the contract permanently.
- Replace hand-rolled shapes with the schema-inferred contract type at the call
  sites, so the type system catches the next drift at compile time instead of in
  production.

## Output shape

A per-endpoint drift table:

| Route (file:line) | Request validated? | Response source | Widening | Optionality drift |
|---|---|---|---|---|

Followed by:
- **Fixes** — the specific parse/validate calls to add and where.
- **Round-trip tests** — one per producer that currently hand-assembles a
  response.
