---
name: project-constraint-build
description: Model a NEW project's constraint cascade — enumerate soft inputs (scope/speed/quality/cost/risk/coordination/engagement), hard pins (regulatory/contractual/brand), dependency graph, what tunes against what, failure modes at extremes. For charter/plan phase. For mature projects use project-constraint-audit; for change-request impact use project-impact-trace.
---

# Build the project constraint cascade

Read `${CLAUDE_PLUGIN_ROOT}/docs/Constraint-based project management.md` and the "PM knob framework" section of `${CLAUDE_PLUGIN_ROOT}/docs/Intent as a PM Lens.md`.

## Procedure

For the target project:

1. **Soft inputs (3–7).** The decisions the team is actually making — usually some subset of:
   - Scope (which deliverables in / out)
   - Speed (calendar pressure)
   - Quality (polish / reliability / completeness bar)
   - Cost (budget envelope, headcount)
   - Risk tolerance (how big a bet)
   - Coordination overhead (how cross-team)
   - Stakeholder engagement (how much review at each milestone)

   Aim for *small* — 3–7 is the holdable-in-head range. For each: name, type, current value, one-sentence purpose.

2. **Hard pins.** Values the project refuses to let the cascade touch. Why each is pinned (regulatory deadline, contractual commitment, brand obligation, executive promise). Note where they're documented.

3. **Dependency graph.** ASCII or table form:
   ```
   DELIVERABLE A  ──→  DELIVERABLE B  (rule: B needs A's API contract)
   DELIVERABLE A  ──→  DELIVERABLE C  (rule: C uses A's data model)
   ```
   Group by upstream. Identify the critical path. A clean graph has no cycles; cycles are findings.

4. **What tunes against what.** Pairs of soft inputs where moving one changes the meaning of the other. The classic triangle (scope/time/cost/quality, where any three pinned forces the fourth to absorb). Name the pair, the relationship, the failure mode the relationship guards against.

5. **Failure modes at extremes.** For each soft input: what breaks at min, what breaks at max? Note which failures the project's process currently catches (gate reviews, slack budgets, milestone checkpoints) and which it does not.

## Output

The five sections in the order above. Diagrammatic where possible — tables and graphs over prose.
