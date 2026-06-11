# Design system lifecycle

A design system is not a static artifact. It passes through phases, and
the questions that matter — and the answers that work — shift with each.
The four lenses (intent, constraint, hierarchy, design loop) still apply
at every phase, but they read very differently in a bootstrap-stage system
vs. one that's been in production for two years.

Naming the phase first lets the right procedure run. Asking
"model the cascade" of a system whose cascade already exists wastes the
loop on a question that's already been answered. Asking "what's the blast
radius" of a system that doesn't have downstream consumers yet is
incoherent.

## The five phases

### 1. Bootstrap

Zero to one. No system exists. The decisions are first-order: what
primitives? what slots? what's pinned? what's derived? You're working in
pure abstraction; no production state to honor.

**What dominates**: identifying the small set of decisions that matter
(the knob framework from `Intent as a Design Lens.md`), naming the hard
constraints, designing the cascade.

**Failure mode — bootstrap-without-bounds**: producing a 200-token system
before seeing one screen is over-spending in the abstraction direction.
The whole point of the loop is that abstraction without feedback is
thrashing-at-the-model-level.

### 2. Apply

Tokens exist; you're putting them to work in the first real screens.
The decisions are about whether your abstractions hold under contact with
content. This is where most bugs surface — the cascade you designed in
bootstrap meets actual UI requirements and either holds or breaks.

**What dominates**: testing the cascade by *using* it. Identifying which
primitives don't survive contact, which screens want decisions you didn't
model.

**Failure mode — adding to fix instead of refining**: every time a screen
breaks, the temptation is to add another token. The right move is usually
to fix the few primitives that didn't survive, not to grow the system.

### 3. Audit

System is in production across many screens. The decisions are about
drift: where has the cascade been bypassed? where are mechanisms
double-spending? where does intent diverge from data-model altitude in
screens that started intent-aligned?

**What dominates**: cross-screen pattern detection. Individual screens
look fine; the *patterns* across the surface area reveal where the system
has slipped.

**Failure mode — per-screen blame**: each screen reviewed in isolation
looks correctable. The systemic pattern — "shadow is decorative across
80% of screens" or "every new field gets surfaced as a token row" — is
invisible if you don't aggregate.

### 4. Tweak

System is stable. You want to change one node. The decisions are about
blast radius and migration cost: what depends on this? how many
components rely on the old value? is the change worth the disruption?

**What dominates**: impact tracing and cost estimation. The lens isn't
"what should this be?" — that was answered phases ago — it's "what
breaks if I move this?"

**Failure mode — small-feeling tweaks that aren't**: a "minor color
adjustment" that affects 40 components is not a tweak. Failing to trace
impact means absorbing more migration work than budgeted.

### 5. Refactor

Significant drift has accumulated. You're rebuilding parts. The decisions
are about preservation: what survives? what gets reborn? what's the
migration path? which inputs collapse into a single underlying decision?

**What dominates**: triage. Distinguishing the substructure that's still
load-bearing from the accreted layer that's become dead weight.

**Failure mode — rewrite-from-scratch**: discarding the cascade and
rebuilding from primitives is rarely correct. Most mature drift is
fixable surgically — collapse three redundant inputs into one,
re-pin a value that became a default, audit the bypasses and re-route.

## How each lens reads per phase

The lenses don't change; the procedures do. The same `constraint-cascade`
lens runs `graph-build` in bootstrap and `impact-trace` in tweak.

| Lens         | Bootstrap                        | Apply                             | Audit                             | Tweak                             | Refactor                          |
|--------------|----------------------------------|-----------------------------------|-----------------------------------|-----------------------------------|-----------------------------------|
| Intent       | design from intent               | first screens match intent?       | where has data-model leaked back? | does this move us toward intent?  | what was the original intent?     |
| Constraint   | model the cascade                | test the cascade                  | find bypasses                     | trace blast radius                | collapse redundant inputs         |
| Hierarchy    | name surface, allocate budget    | walk five mechanisms              | cross-screen drift                | what does this change spend?      | systemic overspending             |
| Design loop  | what's the first test?           | iterate fast                      | where did we stop looping?        | is this worth a loop?             | merge multiple loops              |

## Detecting the phase

Heuristic — what evidence shows in the repo?

- **No design tokens, no UI components, no production users** → Bootstrap
- **Tokens + 1–5 screens, active token changes, defaults shifting** → Apply
- **Many screens, infrequent token changes, conformance/drift discussions** → Audit
- **Single targeted change request against an established baseline, no PR migration scripts** → Tweak
- **Migration plan, deprecation discussion, version bump, multi-PR series** → Refactor

A repo can be in **multiple phases at once**: the token system might be
in Audit while a brand-new feature within it is in Apply. Phase per
subsystem, not per repo.

## Why this taxonomy exists

Without phase awareness, a critic asks the bootstrap questions of a
mature system. The result is a useless answer: "you should model your
decisions as a cascade" is true at zero-state, useless when the cascade
already exists and the question is which input to change.

Each agent in this plugin starts by detecting phase, then composes the
skill set that matches the phase. The skills are the verbs (one
procedure each); the agents are the workflows (compose skills, detect
phase, branch).
