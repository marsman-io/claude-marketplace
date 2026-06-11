---
name: constraint-graph-build
description: Model a NEW design subsystem's constraint cascade — enumerate soft inputs, hard pins, derivations, dependency graph, what tunes against what, failure modes at extremes. For bootstrap/apply phase. For mature systems use constraint-graph-audit; for tweaks use cascade-impact-trace.
---

# Build the constraint cascade

Read `${CLAUDE_PLUGIN_ROOT}/docs/Constraint-based design.md` and the "knob framework" section of `${CLAUDE_PLUGIN_ROOT}/docs/Intent as a Design Lens.md`.

## Procedure

For the target subsystem:

1. **Soft inputs (3–7).** The decisions a user is actually making. Aim *small* — 3–7 is the holdable-in-head range. If you count more than 7, suspect that several "decisions" are actually derivations and collapse them. For each: name, type, default, one-sentence purpose.

2. **Hard pins.** Values the system refuses to let the cascade touch. Why is each pinned? (Usually: it carries a meaning the user expects to be stable — semantic colors, regulatory floors, contract types.) Note where they're enforced in code.

3. **Dependency graph.** ASCII or table form. For each derived value, show:
   ```
   INPUT  ──→  derived value  (rule: brief description)
   ```
   Group derivations by input. A clean graph reads top-down: inputs at the top, leaf outputs at the bottom, no cycles. Cycles are findings.

4. **What tunes against what.** Pairs of inputs where moving one changes the meaning of the other. For each: pair, relationship, failure mode the relationship guards against. This is what turns "a list of inputs" into "a system."

5. **Failure modes at extremes.** For each input: what breaks at min, what breaks at max? Note which failures the cascade currently catches (clamps, AA floors, collision rotators) and which it does not. Uncaught failures are next-loop targets.

## Output

The five sections in the order above. Diagrammatic where possible — tables and graphs over prose.
