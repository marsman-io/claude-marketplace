---
name: boundary-judgment
description: Frontier-model workflow for the architectural judgment a grep can't make — is the boundary between two modules in the right place, or is one leaking responsibility into the other? Produces an argued verdict plus the smallest change that fixes it, not a rewrite. Triggers on "is this boundary in the right place", "should I split/merge these two modules", "this dependency points the wrong way", "two packages both seem to own this concern", "which module should own X". NOT for mechanical moves you can already name, NOT for a vague "review the architecture" with no two specific units in tension, NOT for line-level code review.
---

# Boundary judgment

This is the call you spend a frontier model on. A cheap model — or a grep — can
tell you *what* imports what. It can't tell you whether the seam between two
units is in the *right place*, or argue a committed position when two modules
both seem to own one concern. That is a judgment about responsibility and
direction, and it needs the expensive model. So make the call worth it: come
with exactly two units in tension and a question, not a request to "look at the
architecture."

## When to spend a frontier model here

**Do** spend it when:
- Two units (modules, packages, services) seem to share ownership of one concern.
- A dependency points against your intended direction (e.g. an inner layer
  reaching out to an outer one).
- You're weighing whether to split one unit in two, or merge two into one.

**Don't** spend it when:
- You already know the move and can name it — that's a mechanical refactor, just
  do it.
- You haven't identified the *two specific units* in tension. A vague "review the
  architecture" burns the call on a generic essay. Name the two units first.

## Procedure

### 1. Gather cheap (no frontier tokens yet)

Assemble JUST the two units in tension. Keep it to the two — the whole dependency
graph dilutes the judgment.

- Each unit's **public surface**: its exported symbols / index, what it offers to
  the outside.
- Each unit's **dependency manifest**: what it depends on.
- The **import edges between them**: grep cross-module imports in *both*
  directions, so you can see who reaches into whom.
- The **stated rule they may violate**: the layer map or dependency-direction
  rule from your repo's conventions doc (e.g. CLAUDE.md / AGENTS.md /
  CONTRIBUTING), if one exists.

A useful mental frame for direction: a layered chain like *entrypoint → service →
domain/core → adapter → external boundary*, where dependencies are supposed to
point one way. Note where these two units sit on your own chain.

### 2. Think expensive (the frontier call)

This is the one frontier call. Ask the model to **take a position and argue it**,
then converge on the minimum change. Demand a table, not prose — force it to fill
each row rather than write a generic essay:

| Question | Answer |
| --- | --- |
| What concern does each unit own? | … |
| Where do they overlap, or one reach into the other's responsibility? | … |
| Which direction *should* the dependency point — and does it? | … |
| Is the boundary right, slightly wrong, or structurally wrong? | … |

Classify the verdict into one of three:
- **Right** — the seam is correctly placed; nothing to do.
- **Slightly wrong** — a few misplaced symbols; the boundary is fine, some
  members are on the wrong side.
- **Structurally wrong** — the split itself is in the wrong place; the two units
  are carved along the wrong line.

Then the **smallest change that fixes it** — move these N symbols, invert this one
dependency, extract this one port/interface. NOT a rewrite.

Reject "it depends." Force a committed recommendation with the trade-offs named.
If the model hedges, push it back to a single position.

### 3. Capture durably (spend once, keep it)

The call cost frontier tokens; don't pay it twice. Record the decision so it
holds:

- A short ADR, or a single line in the owning module's conventions doc: "X lives
  here, not in Y, because…".
- If the rule is enforceable, add a dependency / import-boundary lint rule so the
  next violation fails CI instead of needing this judgment again.

## Output shape

```
Verdict: <right | misplaced symbols | structurally wrong> — <one paragraph>

Reasoning:
  - <concern each unit owns; where they overlap; correct vs actual direction>
  - <trade-offs of the recommendation, named — not "it depends">

Smallest fix:
  - <move these N symbols | invert this dependency | extract this one port>

Captured:
  - ADR / conventions line: "<X lives here, not in Y, because …>"
  - Lint rule (if enforceable): <the import-boundary rule to add>
```

A verdict with no committed position, or a "fix" that is really a rewrite, is the
failure mode. One argued position, one minimal change, one durable record.
