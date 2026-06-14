---
name: seam-conformance
description: Frontier-model workflow for checking whether multiple implementations behind one interface BEHAVE the same, not just typecheck the same. Use when N implementations sit behind a shared interface/protocol/abstract base and you need behavioral divergence the types can't catch — error semantics, ordering, partial-failure, idempotency. Triggers on "do these implementations actually agree", "behavioral conformance across implementations", "one throws and another returns null", "check the implementations behind this interface behave the same", "conformance table for these adapters". NOT for a single implementation (no seam), NOT for anything the compiler/linter/typechecker already flags, NOT for pure type or signature mismatches.
---

# Seam conformance

When several implementations sit behind one shared interface — several storage
backends behind a `Store`, payment adapters behind a `PaymentGateway`, transport
clients behind one protocol — the types prove they share a *shape*. They do not
prove they share a *behavior*. One `delete()` throws when the row is gone;
another silently no-ops. One `charge()` is idempotent; another double-bills on
retry. The signatures are identical and the build is green. That is exactly the
gap a frontier model is for.

A cheap model can confirm the methods match the interface — the compiler already
did that. Catching behavioral divergence means holding several method bodies in
one head at once, reasoning about what each does at the edges (retry, half-way
failure, missing precondition), and judging whether they *mean* the same thing.
That cross-body, edge-case reasoning is the expensive call. Don't waste it on
anything cheaper tools already catch.

## When to spend a frontier model here

**Do** spend when:
- The implementations typecheck and lint clean, but you suspect they disagree on
  behavior (one throws where another returns a sentinel; one idempotent, one not).
- You need divergence the types structurally cannot express — error semantics,
  ordering, partial-failure state, idempotency.
- The seam is real: two or more implementations behind one interface.

**Don't** spend when:
- There's a single implementation — no seam, nothing to compare.
- The compiler, linter, or typechecker already flags it.
- It's a pure type or signature mismatch (cheap tools own that).

## Procedure

### 1. Gather cheap — no frontier tokens

Assemble the raw material with grep/Read (or a cheap subagent) before any
frontier call:
- The interface definition — the signature, plus any contract already written in
  its doc comment.
- Each implementation's matching method bodies — the actual code, not summaries.

Then narrow: pick **ONE method family at a time** (e.g. the
create/destroy/exists family). Handing over the whole interface dilutes the
reasoning — the frontier model spreads thin across twenty methods instead of
nailing the divergence in one. Spend the expensive call on a tight target.

### 2. Think expensive — the frontier call

Hand over the bodies plus the signature and demand a **conformance table**, not
prose. One row per implementation; columns are the behavioral axes:

- **Error semantics** — throw vs. return a sentinel vs. silent no-op.
- **Idempotency** — call it twice: safe, or does the second call throw / corrupt?
- **Partial failure** — if it dies half-way, what state is left behind?
- **Ordering / preconditions** — does it assume the target already exists /
  is stopped / is started?
- **Return-value meaning** — are `void` / `null` / `false` used consistently to
  mean the same thing across implementations?

For each axis demand a **divergence verdict**: either *all implementations agree*,
or there's an outlier — and if so, **name the outlier and its `file:method`**. A
generic "here are some differences between these" is a failed call. The output
must be specific enough to act on without re-reading the code.

### 3. Capture durably — spend once

A frontier verdict you don't write down gets re-discovered next quarter at full
price. Convert it into two durable artifacts:
- **A one-sentence contract** in the interface's doc comment, pinning the
  intended behavior — e.g. `destroy() MUST be idempotent and MUST NOT throw if
  the target is already gone.`
- **A shared, parametrized conformance test** that runs every implementation
  through the same expectations, so the next divergence fails the build instead
  of shipping. Wire it into your test runner.

## Output shape

- A markdown **conformance table** — implementation × behavioral axis, one cell
  per intersection.
- **Named outliers** with `file:method`, one per diverging axis.
- **Proposed contract sentences** for the interface's doc comment.
- **Test stubs** for the shared parametrized conformance test.

If the result is prose instead of a table, or lists differences without naming
the outlier and its `file:method`, the frontier call failed — re-run step 2 with
a tighter method family.
