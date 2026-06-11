---
name: project-constraint-build
description: Model a NEW product work constraint cascade — enumerate soft inputs (scope/fidelity/evidence/context/risk/integration/review), hard pins (user trust/data/API/deployment/accessibility), dependency graph, what tunes against what, failure modes at extremes. For charter/plan phase. For mature work use project-constraint-audit; for change-request impact use project-impact-trace.
---

# Build the project constraint cascade

Read `${CLAUDE_PLUGIN_ROOT}/docs/Constraint-based project management.md` and the "PM knob framework" section of `${CLAUDE_PLUGIN_ROOT}/docs/Intent as a PM Lens.md`.

## Procedure

For the target work:

1. **Soft inputs (3-7).** The decisions the builder is actually making — usually some subset of:
   - Scope (which behaviors / user paths are in or out)
   - Fidelity (scaffold, usable, polished, production-safe)
   - Evidence (tests, screenshots, demo path, logs, manual check)
   - Context budget (which files / docs / prior attempts the agent gets)
   - Risk tolerance (how bad if the agent interpretation is wrong)
   - Integration surface (how many files, workflows, data contracts, prompts, or user paths are touched)
   - Review depth (how much human judgment after the agent finishes)

   Aim for *small* — 3-7 is the holdable-in-head range. For each: name, type, current value, one-sentence purpose.

2. **Hard pins.** Values the work refuses to let the cascade touch. Why each is pinned (user trust, saved data, API contract, deployment constraint, accessibility floor, legal / compliance boundary, existing design convention). Note where they're documented.

3. **Dependency graph.** ASCII or table form:
   ```
   INTENT A  ──>  UI BEHAVIOR B  (rule: B must show the user's next step)
   API SHAPE C  ──>  TEST D       (rule: D proves C supports the demo path)
   ```
   Group by upstream. Identify the critical path. A clean graph has no cycles; cycles are findings.

4. **What tunes against what.** Pairs of soft inputs where moving one changes the meaning of the other. The classic triangle applies as scope / speed / review / quality, where any three pinned forces the fourth to absorb. Name the pair, the relationship, the failure mode the relationship guards against.

5. **Failure modes at extremes.** For each soft input: what breaks at min, what breaks at max? Note which failures the current process catches (tests, screenshots, demo path, acceptance checklist, manual review) and which it does not.

## Output

The five sections in the order above. Diagrammatic where possible — tables and graphs over prose.
