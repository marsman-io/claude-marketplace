---
name: constraint-graph-audit
description: Audit a MATURE constraint cascade for drift — find bypasses (manual overrides where derivation should have happened), introduced cycles, redundant inputs that should collapse, defaults that should actually be pinned. For audit/refactor phase. For new systems use constraint-graph-build; for single-change impact use cascade-impact-trace.
---

# Audit a mature cascade

Read `${CLAUDE_PLUGIN_ROOT}/docs/Constraint-based design.md` and `${CLAUDE_PLUGIN_ROOT}/docs/Design system lifecycle.md` (audit/refactor phases).

## Procedure

For the target cascade:

1. **Locate the cascade engine** in code. Find the derivation function(s) — the place that turns inputs into derived values.

2. **Find bypasses.** Grep for manual overrides of values that should have been derived: hex codes hardcoded where a token should live, explicit assignment to derived fields, "TODO: derive from X" comments. Where does the cascade get bypassed in practice?

3. **Find cycles.** Any input deriving from an output that itself derives from that input? Cycles are silent killers in cascades; surface every one.

4. **Find redundancies.** Inputs that move together always, in every consumer — that's evidence of one underlying decision masquerading as two. Candidates for collapse.

5. **Find pins that aren't pinned.** Values that *should be* hard constraints (their meaning is fixed) but are implemented as overridable defaults. Drift candidates.

6. **Find pins that are over-pinned.** Inverse failure: hard constraints that have no semantic reason to be hard, just legacy. Candidates for becoming soft inputs.

## Output

```
Cascade engine: <file:line>

Bypasses (cascade ignored in practice):
  - <file:line>: <what was hardcoded that should have been derived>
  - ...

Cycles:
  - <input> → <derived> → <input>: <file:line> chain
  - ...

Redundancy candidates (move together → may be one decision):
  - <input A> & <input B>: <evidence they always co-vary>

Pin candidates (default-shaped but semantically fixed):
  - <value>: <reason it should be pinned>

Over-pin candidates (pinned but no semantic reason):
  - <value>: <reason it could become soft>

Recommended refactor next step:
  Which ONE collapse / pin / un-pin would simplify the graph most? With file:line.
```
