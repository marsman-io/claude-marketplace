---
name: cascade-impact-trace
description: Trace the downstream blast radius of changing ONE node in a mature constraint cascade. Input — which node, what change. Output — every direct + transitive consumer with the cost of migration. For tweak/refactor phase. Use to answer "is this a tweak or actually a refactor?" before committing to a change.
---

# Trace cascade impact

Read `${CLAUDE_PLUGIN_ROOT}/docs/Constraint-based design.md` and `${CLAUDE_PLUGIN_ROOT}/docs/Design system lifecycle.md` (tweak phase).

## Procedure

Given a target node (a token, a decision, a derivation rule) and a proposed change:

1. **Find direct consumers.** Grep + read for everything that references this node by name.

2. **Classify each consumer:**
   - **Derivations** — consumers that re-run automatically on the next cascade pass. Zero migration cost.
   - **Hard-coded references** — consumers that capture the *value* (a hex, a number), not the reference. These need manual migration on every change.
   - **Overrides** — consumers that take the value and then modify it. Migration depends on whether the override depends on the specific value or just the role.

3. **Find transitive consumers.** For derivations that consume this node, recursively check *their* consumers. The graph might fan out 3 levels.

4. **Estimate migration cost.**
   - Number of files / components affected
   - Per-class breakdown (derivations vs hard-coded vs overrides)
   - Approximate effort (mechanical find/replace vs case-by-case judgment)

5. **Identify alternative paths.** Could introducing a new pin somewhere insulate downstream consumers? Could collapsing two inputs make this change unnecessary?

## Output

```
Target node: <name> at <file:line>
Proposed change: <description>

Direct consumers (<N> total):
  - Derivations (<N>):  <list, file:line>
  - Hard-coded refs (<N>):  <list>
  - Overrides (<N>):  <list>

Transitive consumers: <N> additional files / components

Migration cost estimate:
  - Mechanical updates: <N> sites
  - Case-by-case judgment needed: <N> sites
  - Verdict: <"true tweak — under N consumers" | "actually a refactor — over N consumers" | "intermediate">

Alternative paths to reduce blast radius:
  - <alternative 1>: <effect>
  - <alternative 2>: <effect>
```

The cost classification is the deliverable. A change with a 200-file blast radius is a refactor wearing a tweak's clothing — name it as such.
