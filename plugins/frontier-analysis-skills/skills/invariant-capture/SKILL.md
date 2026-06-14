---
name: invariant-capture
description: Frontier-model workflow that turns expensive reasoning into a durable asset — find the unstated invariant a subsystem silently relies on, then bank it as a one-line rule (in your conventions doc) plus a characterization test that fails if it's violated. The "spend once, enforce forever" move. Use after any frontier analysis (seam-conformance, layer-trace, contract-drift, boundary-judgment) to capture what you learned, or when a subsystem has a fragile assumption nobody wrote down. Triggers on "what is this code silently assuming", "capture the unwritten invariant", "the next edit here would break something nobody documented", "bank what we just learned into a rule and a test", "what load-bearing assumption has no test". NOT for restating what types or existing tests already guarantee, NOT for writing aspirational rules nobody follows, NOT for invariants the code doesn't actually rely on yet.
---

# Invariant capture

Every subsystem leans on assumptions nobody wrote down. `destroy()` is
idempotent. The core never imports from an adapter. Every response is
schema-validated before it leaves the process. These are true today, everything
near them silently depends on them, and no type or comment states them. The next
careless edit breaks one and the build stays green until production. This skill
finds those load-bearing invariants and converts them into something the repo
enforces forever — for the price of one frontier call.

A cheap model restates what the types already guarantee and invents aspirational
rules nobody follows. Surfacing a *real* invariant means holding the code that
holds the assumption and the code that depends on it holding in one head at once,
then reasoning about which specific edit would violate it and what breaks
downstream. That "what is true here that nothing states, and what would shatter
it" reasoning is the expensive call. The capture step then turns it into an asset
so you never pay for it twice.

## When to spend a frontier model here

**Do** spend it when:
- You want the IMPLICIT contract code depends on — true today, assumed
  everywhere, stated by no type or comment, breakable by the next careless edit.
- You just finished a frontier analysis (seam-conformance, layer-trace,
  contract-drift, boundary-judgment) and want to bank the finding before it
  evaporates and gets re-discovered next quarter at full price.
- A subsystem has a fragile assumption nobody wrote down and you can feel that an
  innocent refactor would land on it.

**Don't** spend it when:
- The invariant is already guaranteed by a type or an existing test — capturing
  it again is busywork.
- You'd be writing an aspirational rule nobody actually follows. Capture what the
  code relies on NOW, not what you wish it did.
- Nothing actually depends on the assumption yet — there's no blast radius to
  protect.

## Procedure

### 1. Gather cheap — no frontier tokens

Assemble the raw material with grep/Read (or a cheap subagent) before any
frontier call. Or, if this follows a preceding analysis skill, reuse its
dossier — you already paid to pull the code:
- The subsystem holding the assumption — the actual code, not summaries.
- Its callers — the code that depends on the assumption holding.

You want both halves: the assumption and everything betting on it. If you only
have one, you can't reason about the blast radius. Keep gathering until you have
both.

### 2. Think expensive — the frontier call

Hand over the subsystem and its callers and demand the LOAD-BEARING but unstated
invariants — as a **table, not prose**. One row per candidate invariant; the
columns force specificity:

- **Statement** — the invariant in one plain sentence (`destroy()` is
  idempotent; every response is schema-validated before send; the core never
  imports from an adapter).
- **Evidence** — the specific code that relies on it. What assumes this is true?
- **Breaking edit** — the concrete change that violates it, plus the downstream
  damage. Not "if someone changed this" — name the edit.
- **Blast radius** — how much breaks when it's violated. Rank by this.

Then cut: keep the few invariants whose violation causes real damage; drop the
trivially-true and anything types or tests already pin. A generic "here are some
assumptions in this code" is a failed call — every row must name evidence and a
breaking edit, or it's prose pretending to be a finding.

### 3. Capture durably — spend once

This is the whole point. A frontier insight you don't write down gets
re-discovered later at full price. For each kept invariant, produce BOTH:

- **A rule line** in the right home — your repo's conventions doc (e.g.
  CLAUDE.md / AGENTS.md / CONTRIBUTING), a package-local doc, or the interface's
  own doc comment, whichever scope the invariant actually lives at. One
  imperative, testable sentence: `destroy() MUST be idempotent and MUST NOT
  throw if the target is already gone.`
- **A characterization test** that encodes current behavior and fails the moment
  the invariant breaks. You've already stated the invariant and its breaking
  edit, so a cheap model can fill in the cases and the test body — keep the
  frontier call for *naming* the invariant, not for typing assertions. Wire it
  into your test runner.

The pair is the move: the rule line tells a human what not to break; the test
fails the build when they do anyway.

## Output shape

A short table of the kept invariants:

| Invariant (one sentence) | Evidence (what relies on it) | Breaking edit | Blast radius |
|---|---|---|---|

Followed by, for each kept row:
- **The exact rule line** and the file it goes in (conventions doc, package doc,
  or interface comment).
- **A characterization test stub** that fails if the invariant is violated.

If the result is prose, or lists assumptions without naming evidence and a
concrete breaking edit, the frontier call failed — re-run step 2 with a tighter
subsystem and its callers.
